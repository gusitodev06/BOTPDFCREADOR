# 📸 PDF CREATOR Telegram Bot 📄

Un bot potente y minimalista desarrollado en **Python** que transforma tus ráfagas de fotos en documentos PDF organizados en segundos. Ideal para digitalizar apuntes, facturas o documentos rápidamente desde el móvil.

---

## ✨ Características Principales

* 🚀 **Conversión Instantánea:** Envía tus fotos y recibe el PDF al momento.
* 📦 **Soporte Multi-imagen:** Agrupa varias fotos en un solo archivo PDF.
* 🖼️ **Alta Calidad:** Mantiene la resolución original de tus PDF.
* 🖼️ **Calidad estandar:** Comprime imagenes de mas de 3mb de tamaño.
* 🛠️ **Procesamiento Ligero:** Optimizado para no consumir recursos excesivos en el servidor.
* 🤖 **Interfaz Simple:** Comandos intuitivos para una experiencia de usuario fluida.

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** [Python 3.10+](https://www.python.org/)
* **Librerías de Bot:** `python-telegram-bot` `img2pdf` `Pillow pypdf` `httpx`

---

## 🚀 Instalación y Despliegue

Sigue estos pasos para tener tu propio bot funcionando en minutos:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/tu-usuario/nombre-del-repo.git](https://github.com/tu-usuario/nombre-del-repo.git)
cd nombre-del-repo
```

###2. Configurar el entorno virtual (Recomendado)
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
```
### 3. Instalar dependencias
```bash
pip install python-telegram-bot Pillow img2pdf python-dotenv pypdf httpx
```
### 4.Ejecuta el bot
```bash
python app.py
```
###📖 Modo de Uso.

Inicia el bot: Envía el comando /start.

Envía tus fotos: Puedes enviarlas una por una o como un álbum (asegúrate de enviarlas como "Foto" para previsualización o "Archivo").

Genera el PDF: Usa el comando /done (o el que hayas configurado) para finalizar la carga.

Recibe tu archivo: El bot procesará las imágenes y te enviará el documento PDF listo para descargar.

### 🛡️Licencia
Este proyecto está bajo la Licencia MIT. Siéntete libre de usarlo, modificarlo y compartirlo.

Desarrollado con ⚡ por gusdev

