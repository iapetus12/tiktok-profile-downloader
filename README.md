# 📥 TikTok Profile Downloader (CLI & GUI)

Herramienta multiplataforma (Windows, Linux, macOS) en Python para descargar todos (o los últimos $N$) vídeos de cualquier usuario público de TikTok sin marcas de agua.

Cuenta tanto con **interfaz gráfica moderna (GUI)** con modo oscuro como con versión para **línea de comandos (CLI)**.

Incluye suplantación de huella TLS (*browser impersonation* con `curl-cffi`) para evitar bloqueos por detección antibot de TikTok.

---

## 🚀 Características

- 🖥️ **Interfaz Gráfica Moderna (GUI)**: Desarrollada con `CustomTkinter` con tema adaptable (oscuro/claro) y registro de actividad en tiempo real.
- 📁 **Selector de carpetas nativo**: Botón para examinar y elegir la ruta donde guardar los vídeos.
- 🎬 **Descarga completa o limitada**: Descarga todos los vídeos públicos de un perfil o solo los últimos $N$ vídeos.
- 🔄 **Control de duplicados**: Historial inteligente (`download_archive`); si vuelves a ejecutarlo para el mismo usuario, solo bajará los vídeos nuevos.
- 📝 **Descripciones opcionales**: Guarda los textos y hashtags de cada vídeo en archivos `.txt`.
- ⚡ **Sin bloqueos (Anti-bot Bypass)**: Evasión mediante pausas y huella TLS idéntica a la de un navegador web.

---

## 📦 Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/iapetus12/tiktok-profile-downloader.git
   cd tiktok-profile-downloader
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Modos de Uso

### 1. Interfaz Gráfica (Recomendado para Windows / Escritorio)

```bash
python gui.py
```
*(En Linux/macOS: `python3 gui.py`)*

Se abrirá la ventana gráfica donde podrás ingresar el usuario, elegir la carpeta con el explorador de archivos, limitar la cantidad de vídeos y ver el progreso en tiempo real.

---

### 2. Modo Consola (CLI)

```bash
python descarga_tiktok.py
```

---

## 🪟 ¿Cómo generar un `.exe` para Windows?

Si quieres compartir la aplicación o usarla en Windows haciendo **doble clic** (sin necesidad de tener Python instalado):

1. Instala `pyinstaller`:
   ```bash
   pip install pyinstaller
   ```

2. Genera el ejecutable único:
   ```bash
   pyinstaller --noconsole --onefile --name="TikTokDownloader" gui.py
   ```

3. El archivo `TikTokDownloader.exe` estará listo en la carpeta **`dist/`**. ¡Doble clic y listo!

---

## ⚖️ Descargo de responsabilidad (Disclaimer)

Este proyecto ha sido desarrollado con fines exclusivamente educativos y de copia de seguridad personal. El usuario es responsable de cumplir con los términos de servicio de la plataforma y respetar los derechos de autor del contenido descargado.
