# 📥 TikTok Profile Downloader

Herramienta ligera y automatizada en Python para descargar todos (o los últimos $N$) vídeos de cualquier usuario público de TikTok sin marcas de agua ni restricciones de velocidad.

Incluye suplantación de huella TLS (*browser impersonation* mediante `curl-cffi`) para evitar bloqueos por detección antibot de TikTok.

---

## 🚀 Características

- **Descarga completa o limitada**: Descarga todos los vídeos públicos de un perfil o solo los últimos $N$ vídeos.
- **Ruta personalizable**: Elige la carpeta destino en cada ejecución o usa la ruta por defecto (`~/Descargas/TikTok/<usuario>`).
- **Control de duplicados**: Mediante un historial interno de descargas (`download_archive`), si vuelves a ejecutarlo para el mismo usuario, solo descargará los vídeos nuevos.
- **Descripciones opcionales**: Posibilidad de guardar los títulos/hashtags de cada vídeo en archivos `.txt`.
- **Evasión antibot**: Usa pausas inteligentes entre peticiones y cabeceras TLS nativas para evitar rate-limiting o captchas.

---

## 📦 Requisitos e Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/iapetus12/tiktok-profile-downloader.git
   cd tiktok-profile-downloader
   ```

2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Uso

Ejecuta el script:

```bash
python3 descarga_tiktok.py
```

El asistente interactivo te pedirá:
1. El **usuario de TikTok** (con o sin `@`).
2. La **carpeta de destino** (puedes presionar `Enter` para usar la carpeta por defecto).
3. La **cantidad de vídeos** a bajar (deja vacío para descargarlos todos).
4. Si deseas guardar las **descripciones/textos** de cada publicación.

---

## ⚖️ Descargo de responsabilidad (Disclaimer)

Este proyecto ha sido desarrollado con fines exclusivamente educativos y de copia de seguridad personal. El usuario es responsable de cumplir con los términos de servicio de la plataforma y respetar los derechos de autor del contenido descargado.
