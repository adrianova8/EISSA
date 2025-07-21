import tkinter as tk
from datetime import datetime
from tkinter import messagebox

from src.app.window_app import AppWindow
from src.app.utils.frame_manager import FrameManager
from src.utils.common.names import (
    BROWN_COLOR, METAL_GOLD_COLOR, BEIGE_COLOR
)

def open_new_day_container(app: tk.Tk, app_window: AppWindow, frame_manager: FrameManager) -> None:
    """
    Creates a button that opens a new day (e.g. starts a new sales record).
    """
    frame = frame_manager.get_frame("main_container")

    def open_new_day_logic():
        today = datetime.now().date()

        # Aquí iría tu lógica real para crear un nuevo día
        # Por ejemplo: limpiar datos temporales, crear nueva entrada, etc.
        # Podrías llamar a funciones de negocio del módulo correspondiente

        # Por ahora simplemente muestra un mensaje de confirmación
        messagebox.showinfo("Nou dia obert", f"S'ha obert un nou dia: {today.strftime('%d/%m/%Y')}")

    open_day_button = app_window.create_button(
        frame,
        text="📅 Obrir nou dia",
        command=open_new_day_logic,
        bg=BROWN_COLOR,
        fg=METAL_GOLD_COLOR,
        highlightbackground=BEIGE_COLOR,
        padx=10,
        pady=5
    )
    open_day_button.pack(side="left", anchor="w", padx=10, pady=10)
