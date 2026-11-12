import os
import yt_dlp

def solicitar_datos():
    print("=" * 60)
    print("        📥 DESCARGADOR AUTOMÁTICO DE TIKTOK")
    print("=" * 60)

    # 1. Usuario
    usuario = input("\n👤 Introduce el usuario de TikTok: ").strip().lstrip("@")
    if not usuario:
        print("❌ El usuario no puede estar vacío.")
        return None

    # 2. Carpeta destino
    ruta_defecto = os.path.expanduser(f"~/Descargas/TikTok/{usuario}")
    print(f"\n📁 Carpeta de descarga [Presiona Enter para '{ruta_defecto}']: ")
    carpeta = input("   > ").strip()
    if not carpeta:
        carpeta = ruta_defecto
    else:
        carpeta = os.path.expanduser(carpeta)

    # 3. Límite de vídeos
    print("\n🎬 ¿Cuántos vídeos descargar?")
    print("   [Enter = Todos los vídeos del perfil] o indica un número (ej. 10):")
    limite_input = input("   > ").strip()
    limite = int(limite_input) if limite_input.isdigit() else None

    # 4. Guardar descripciones
    desc_input = input("\n📝 ¿Guardar también la descripción/texto de cada vídeo en .txt? (s/N): ").strip().lower()
    guardar_texto = desc_input == "s"

    return {
        "usuario": usuario,
        "carpeta": carpeta,
        "limite": limite,
        "guardar_texto": guardar_texto,
    }

def descargar_tiktok(config):
    usuario = config["usuario"]
    carpeta = config["carpeta"]
    os.makedirs(carpeta, exist_ok=True)

    url_perfil = f"https://www.tiktok.com/@{usuario}"
    ruta_plantilla = os.path.join(carpeta, "%(upload_date)s_%(id)s.%(ext)s")
    archivo_historial = os.path.join(carpeta, ".historial_descargas.txt")

    opciones = {
        "outtmpl": ruta_plantilla,
        "download_archive": archivo_historial,  # Omite vídeos ya descargados previamente
        "ignoreerrors": True,
        "nooverwrites": True,
        "sleep_interval": 1,
        "max_sleep_interval": 3,
        "retries": 5,
        "fragment_retries": 5,
        "writedescription": config["guardar_texto"],
    }

    if config["limite"]:
        opciones["playlistend"] = config["limite"]

    print("\n" + "=" * 60)
    print(f"🚀 Iniciando descarga de: @{usuario}")
    print(f"📂 Guardando en: {carpeta}")
    if config["limite"]:
        print(f"🔢 Límite: Últimos {config['limite']} vídeos")
    else:
        print("🔢 Modo: Todos los vídeos disponibles")
    print(f"📝 Guardar textos: {'Sí' if config['guardar_texto'] else 'No'}")
    print("=" * 60 + "\n")

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url_perfil])
        print("\n✨ ¡Descarga finalizada con éxito!")
    except Exception as e:
        print(f"\n❌ Error durante la descarga: {e}")

if __name__ == "__main__":
    datos = solicitar_datos()
    if datos:
        descargar_tiktok(datos)
