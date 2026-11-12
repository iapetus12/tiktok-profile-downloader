import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import yt_dlp

# Configuración visual de CustomTkinter
ctk.set_appearance_mode("System")  # Detecta automáticamente modo Claro u Oscuro del sistema
ctk.set_default_color_theme("blue")


class YtDlpLogger:
    """Redirige las salidas de yt-dlp a la consola visual de la interfaz."""
    def __init__(self, log_callback):
        self.log_callback = log_callback

    def debug(self, msg):
        # yt-dlp envía mucha información de depuración que empieza por [debug]
        if not msg.startswith("[debug]"):
            self.log_callback(msg)

    def info(self, msg):
        self.log_callback(msg)

    def warning(self, msg):
        self.log_callback(f"⚠️ {msg}")

    def error(self, msg):
        self.log_callback(f"❌ {msg}")


class TikTokDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("TikTok Profile Downloader")
        self.geometry("700x680")
        self.minsize(620, 580)

        # Ruta por defecto según sistema operativo (Windows, Linux, macOS)
        carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
        if not os.path.exists(carpeta_descargas):
            carpeta_descargas = os.path.join(os.path.expanduser("~"), "Descargas")
        self.ruta_defecto_base = os.path.join(carpeta_descargas, "TikTok")

        self.esta_descargando = False
        self._crear_interfaz()

    def _crear_interfaz(self):
        # 1. Cabecera
        frame_header = ctk.CTkFrame(self, corner_radius=12)
        frame_header.pack(fill="x", padx=20, pady=(20, 10))

        lbl_titulo = ctk.CTkLabel(
            frame_header, 
            text="📥 TikTok Profile Downloader", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        lbl_titulo.pack(pady=(12, 4))

        lbl_subtitulo = ctk.CTkLabel(
            frame_header,
            text="Descarga vídeos completos o recientes de perfiles públicos sin marcas de agua.",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        lbl_subtitulo.pack(pady=(0, 12))

        # 2. Formulario de configuración
        frame_form = ctk.CTkFrame(self, corner_radius=12)
        frame_form.pack(fill="x", padx=20, pady=10)

        # Usuario
        lbl_user = ctk.CTkLabel(frame_form, text="Usuario de TikTok:", font=ctk.CTkFont(weight="bold"))
        lbl_user.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 2))

        self.entry_usuario = ctk.CTkEntry(frame_form, placeholder_text="ej: itsnikelle o @charlidamelio")
        self.entry_usuario.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 10))
        self.entry_usuario.bind("<KeyRelease>", self._actualizar_ruta_dinamica)

        # Carpeta de destino
        lbl_dir = ctk.CTkLabel(frame_form, text="Carpeta de destino:", font=ctk.CTkFont(weight="bold"))
        lbl_dir.grid(row=2, column=0, sticky="w", padx=15, pady=(5, 2))

        self.entry_dir = ctk.CTkEntry(frame_form)
        self.entry_dir.insert(0, self.ruta_defecto_base)
        self.entry_dir.grid(row=3, column=0, sticky="ew", padx=(15, 5), pady=(0, 10))

        btn_examinar = ctk.CTkButton(frame_form, text="Examinar...", width=100, command=self._seleccionar_directorio)
        btn_examinar.grid(row=3, column=1, sticky="e", padx=(0, 15), pady=(0, 10))

        # Opciones extra
        frame_opciones = ctk.CTkFrame(frame_form, fg_color="transparent")
        frame_opciones.grid(row=4, column=0, columnspan=2, sticky="ew", padx=15, pady=(5, 15))

        lbl_limite = ctk.CTkLabel(frame_opciones, text="Límite de vídeos:")
        lbl_limite.pack(side="left", padx=(0, 5))

        self.entry_limite = ctk.CTkEntry(frame_opciones, width=80, placeholder_text="Todos")
        self.entry_limite.pack(side="left", padx=(0, 25))

        self.check_desc = ctk.CTkCheckBox(frame_opciones, text="Guardar descripción (.txt)")
        self.check_desc.pack(side="left")

        frame_form.columnconfigure(0, weight=1)

        # 3. Botón de Acción Principal
        self.btn_descargar = ctk.CTkButton(
            self, 
            text="🚀 Iniciar Descarga", 
            font=ctk.CTkFont(size=16, weight="bold"),
            height=44,
            command=self._iniciar_descarga_hilo
        )
        self.btn_descargar.pack(fill="x", padx=20, pady=10)

        # 4. Consola / Registro de actividad
        frame_consola = ctk.CTkFrame(self, corner_radius=12)
        frame_consola.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        lbl_consola = ctk.CTkLabel(frame_consola, text="Registro de actividad:", font=ctk.CTkFont(weight="bold"))
        lbl_consola.pack(anchor="w", padx=15, pady=(10, 2))

        self.txt_consola = ctk.CTkTextbox(frame_consola, font=ctk.CTkFont(family="monospace", size=12))
        self.txt_consola.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.txt_consola.configure(state="disabled")

    def _actualizar_ruta_dinamica(self, event=None):
        """Sugiere una subcarpeta con el nombre del usuario si la ruta actual es la por defecto."""
        usuario = self.entry_usuario.get().strip().lstrip("@")
        ruta_actual = self.entry_dir.get().strip()

        # Solo auto-completa si el usuario no ha puesto una ruta arbitraria
        if usuario and (ruta_actual.startswith(self.ruta_defecto_base) or not ruta_actual):
            nueva_ruta = os.path.join(self.ruta_defecto_base, usuario)
            self.entry_dir.delete(0, "end")
            self.entry_dir.insert(0, nueva_ruta)

    def _seleccionar_directorio(self):
        directorio = filedialog.askdirectory(initialdir=self.entry_dir.get() or os.path.expanduser("~"))
        if directorio:
            self.entry_dir.delete(0, "end")
            self.entry_dir.insert(0, directorio)

    def log(self, mensaje):
        """Escribe un mensaje de forma segura en la consola de texto."""
        def _append():
            self.txt_consola.configure(state="normal")
            self.txt_consola.insert("end", f"{mensaje}\n")
            self.txt_consola.see("end")
            self.txt_consola.configure(state="disabled")
        self.after(0, _append)

    def _iniciar_descarga_hilo(self):
        if self.esta_descargando:
            return

        usuario = self.entry_usuario.get().strip().lstrip("@")
        if not usuario:
            messagebox.showwarning("Atención", "Por favor introduce un nombre de usuario de TikTok.")
            return

        carpeta = self.entry_dir.get().strip()
        if not carpeta:
            messagebox.showwarning("Atención", "Por favor selecciona una carpeta de destino.")
            return

        limite_txt = self.entry_limite.get().strip()
        limite = int(limite_txt) if limite_txt.isdigit() else None
        guardar_txt = bool(self.check_desc.get())

        # Bloquear botón para evitar múltiples descargas simultáneas
        self.esta_descargando = True
        self.btn_descargar.configure(state="disabled", text="⏳ Descargando vídeos...")

        # Iniciar proceso en un hilo secundario para que la GUI no se congele
        hilo = threading.Thread(
            target=self._ejecutar_descarga,
            args=(usuario, carpeta, limite, guardar_txt),
            daemon=True
        )
        hilo.start()

    def _ejecutar_descarga(self, usuario, carpeta, limite, guardar_txt):
        try:
            os.makedirs(carpeta, exist_ok=True)
            url_perfil = f"https://www.tiktok.com/@{usuario}"
            ruta_plantilla = os.path.join(carpeta, "%(upload_date)s_%(id)s.%(ext)s")
            archivo_historial = os.path.join(carpeta, ".historial_descargas.txt")

            self.log(f"--- Iniciando tarea para @{usuario} ---")
            self.log(f"Carpeta: {carpeta}")
            if limite:
                self.log(f"Límite fijado: Últimos {limite} vídeos")
            else:
                self.log("Límite: Todos los vídeos")
            self.log("Conectando con TikTok...")

            logger = YtDlpLogger(self.log)

            opciones = {
                "outtmpl": ruta_plantilla,
                "download_archive": archivo_historial,
                "ignoreerrors": True,
                "nooverwrites": True,
                "sleep_interval": 1,
                "max_sleep_interval": 3,
                "retries": 5,
                "fragment_retries": 5,
                "writedescription": guardar_txt,
                "logger": logger,
            }

            if limite:
                opciones["playlistend"] = limite

            with yt_dlp.YoutubeDL(opciones) as ydl:
                ydl.download([url_perfil])

            self.log("✨ ¡Descarga completada con éxito!")
            self.after(0, lambda: messagebox.showinfo("Éxito", f"Descarga finalizada para @{usuario}."))

        except Exception as e:
            self.log(f"❌ Error durante el proceso: {e}")
            self.after(0, lambda: messagebox.showerror("Error", f"Ocurrió un error:\n{e}"))

        finally:
            self.esta_descargando = False
            self.after(0, lambda: self.btn_descargar.configure(state="normal", text="🚀 Iniciar Descarga"))


if __name__ == "__main__":
    app = TikTokDownloaderApp()
    app.mainloop()
