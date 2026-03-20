# BOTPDFCREADOR


📄 Image2PDF Telegram Bot

Este es un bot de Python diseñado para simplificar la creación de archivos PDF a partir de imágenes. El flujo es sencillo: envías las fotos al bot y este las procesa, las organiza y te devuelve un documento PDF listo para descargar.
✨ Características

    Conversión Directa: Transforma imágenes (JPG, PNG, JPEG) en documentos PDF de alta calidad.

    Soporte Multi-foto: Envía varias imágenes y el bot las agrupará en un solo archivo.

    Procesamiento Eficiente: Utiliza librerías optimizadas para manejar el redimensionado y la compresión de imágenes.

    Interfaz Intuitiva: Comandos sencillos para iniciar, finalizar el documento o cancelar la operación.

🛠️ Tecnologías utilizadas

    Lenguaje: Python 3.x

    Librería de Bot: python-telegram-bot (o la que estés usando, ej. telebot)

    Manejo de Imágenes: Pillow (PIL)

    Generación de PDF: img2pdf o FPDF

🚀 Instalación y Configuración

    Clona el repositorio:

    Bash

git clone https://github.com/tu-usuario/nombre-del-repo.git
cd nombre-del-repo

Instala las dependencias:
Bash

pip install -r requirements.txt

    Configura tu Token:
    Crea un archivo .env o modifica el script principal con el API Token proporcionado por @BotFather.

    Ejecuta el bot:
    Bash

    python bot.py

📖 Modo de Uso

    Inicia el bot con el comando /start.

    Envía las imágenes que deseas incluir en el PDF (puedes enviarlas como "Foto" o como "Archivo").

    Una vez enviadas todas, usa el comando /convertir (o el que hayas programado).

    ¡Recibe tu archivo PDF en segundos!

🛡️ Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.
