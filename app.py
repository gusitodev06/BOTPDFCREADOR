import os
import asyncio
import logging
import img2pdf
import shutil
from PIL import Image
from pypdf import PdfWriter
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ContextTypes, 
    CallbackQueryHandler
)

# --- CONFIGURACIÓN ---
TOKEN = '8574955276:AAFQRMQLdn3gUsPc4bQb3RZ2ukvSfDe-DQw'
TEMP_DIR = 'novabot_data'

# Configuración de Logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

if not os.path.exists(TEMP_DIR): 
    os.makedirs(TEMP_DIR)

user_data = {}

# --- UTILIDADES VISUALES ---

def get_progress_bar(percent):
    """Genera una barra de progreso visual."""
    done = int(percent / 10)
    return f"<code>[{'■' * done}{'□' * (10 - done)}] {percent}%</code>"

def main_menu():
    """Genera el teclado de botones."""
    keyboard = [
        [InlineKeyboardButton("💎 Combinar Archivos", callback_data="merge")],
        [InlineKeyboardButton("📉 Comprimir", callback_data="compress"), 
         InlineKeyboardButton("🔐 Proteger", callback_data="protect")],
        [InlineKeyboardButton("🗑️ Limpiar Todo", callback_data="clear")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_panel_text(count, errors, status="Esperando archivos..."):
    """Diseño del panel de control."""
    return (
        "<b>⚡ NOVABOT PDF: PANEL DE CONTROL ⚡</b>\n"
        "<i>Estatus: Online // Dev: GusDev</i>\n"
        "--------------------------------------\n"
        f"📥 <b>Archivos en cola:</b> <code>{count}</code>\n"
        f"❌ <b>Errores:</b> <code>{errors}</code>\n\n"
        f"🔄 <b>Estado:</b> <i>{status}</i>"
    )

# --- FUNCIÓN CLAVE: ACTUALIZAR PANEL ---

async def update_panel(update: Update, context: ContextTypes.DEFAULT_TYPE, uid, status_txt="Agregando..."):
    """
    Borra el panel viejo y envía uno nuevo al final del chat.
    Recibe el objeto 'update' completo para evitar errores de atributos.
    """
    count = len(user_data[uid]['files'])
    errs = user_data[uid]['errors']
    chat_id = update.effective_chat.id # Aquí es donde fallaba antes si pasábamos 'query'
    
    # 1. Intentar borrar el mensaje anterior del bot (el panel viejo)
    if user_data[uid]['main_msg_id']:
        try:
            await context.bot.delete_message(
                chat_id=chat_id, 
                message_id=user_data[uid]['main_msg_id']
            )
        except:
            pass # Si ya no existe, ignoramos

    # 2. Enviar el nuevo panel al final
    msg = await context.bot.send_message(
        chat_id=chat_id,
        text=get_panel_text(count, errs, status_txt),
        parse_mode=constants.ParseMode.HTML,
        reply_markup=main_menu()
    )
    user_data[uid]['main_msg_id'] = msg.message_id

# --- HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    # Limpieza inicial
    shutil.rmtree(os.path.join(TEMP_DIR, str(uid)), ignore_errors=True)
    user_data[uid] = {'files': [], 'errors': 0, 'main_msg_id': None}
    
    msg = await update.message.reply_text(
        get_panel_text(0, 0),
        parse_mode=constants.ParseMode.HTML,
        reply_markup=main_menu()
    )
    user_data[uid]['main_msg_id'] = msg.message_id

async def handle_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in user_data:
        user_data[uid] = {'files': [], 'errors': 0, 'main_msg_id': None}

    u_folder = os.path.join(TEMP_DIR, str(uid))
    if not os.path.exists(u_folder): os.makedirs(u_folder)

    # Borrar el archivo enviado por el usuario para limpiar chat
    try: await update.message.delete()
    except: pass

    try:
        if update.message.photo:
            file = await update.message.photo[-1].get_file()
            f_path = os.path.join(u_folder, f"p_{file.file_id}.pdf")
            tmp_img = os.path.join(u_folder, f"t_{file.file_id}.jpg")
            await file.download_to_drive(tmp_img)
            
            with Image.open(tmp_img) as img:
                img.convert('RGB').save(tmp_img, "JPEG", quality=70, optimize=True)
            with open(f_path, "wb") as f:
                f.write(img2pdf.convert(tmp_img))
            os.remove(tmp_img)
            user_data[uid]['files'].append(f_path)

        elif update.message.document and update.message.document.mime_type == 'application/pdf':
            doc = update.message.document
            f_path = os.path.join(u_folder, f"d_{doc.file_id}.pdf")
            file = await doc.get_file()
            await file.download_to_drive(f_path)
            user_data[uid]['files'].append(f_path)
        else:
            user_data[uid]['errors'] += 1
    except:
        user_data[uid]['errors'] += 1

    # Llamamos a update_panel pasando 'update'
    await update_panel(update, context, uid)

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if query.data == "clear":
        shutil.rmtree(os.path.join(TEMP_DIR, str(uid)), ignore_errors=True)
        user_data[uid] = {'files': [], 'errors': 0, 'main_msg_id': query.message.message_id}
        # CORRECCIÓN: Pasamos 'update' en lugar de 'query'
        await update_panel(update, context, uid, "Cola vaciada.")

    elif query.data == "merge":
        if not user_data.get(uid) or not user_data[uid]['files']:
            return

        # Animación sobre el panel actual
        try:
            for i in range(1, 11, 2):
                await query.edit_message_text(
                    f"🚀 <b>Procesando PDF Maestro...</b>\n{get_progress_bar(i*10)}",
                    parse_mode=constants.ParseMode.HTML
                )
                await asyncio.sleep(0.1)
        except:
            pass # Si falla la edición (usuario impaciente), seguimos

        out_path = os.path.join(TEMP_DIR, f"Nova_{uid}.pdf")
        writer = PdfWriter()
        
        try:
            for f in user_data[uid]['files']:
                writer.append(f)
            with open(out_path, "wb") as f:
                writer.write(f)
            
            # Enviar el documento final
            await query.message.reply_document(
                document=open(out_path, 'rb'),
                filename="NovaPro_Result.pdf",
                caption="✨ <b>¡Tu PDF está listo!</b>",
                parse_mode=constants.ParseMode.HTML
            )
            
            # Resetear y enviar un NUEVO panel al final
            shutil.rmtree(os.path.join(TEMP_DIR, str(uid)), ignore_errors=True)
            user_data[uid]['files'] = []
            user_data[uid]['errors'] = 0
            # CORRECCIÓN: Pasamos 'update' en lugar de 'query'
            await update_panel(update, context, uid, "¡PDF Generado!")

        except Exception as e:
            await query.message.reply_text(f"❌ Error: {e}")
        finally:
            if os.path.exists(out_path): os.remove(out_path)
    
    # Aquí puedes agregar la lógica para 'compress' y 'protect' cuando quieras

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, handle_files))
    app.add_handler(CallbackQueryHandler(callback_handler))
    
    print("🚀 NOVABOT PRO BLACK EDITION (CORREGIDO) ONLINE")
    app.run_polling()

if __name__ == '__main__':
    main()