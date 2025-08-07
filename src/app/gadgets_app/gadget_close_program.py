import tkinter as tk

from src.app.window_app import AppWindow
from src.app.utils.frame_manager import FrameManager
from src.utils.common.names import (BLACK_COLOR, WHITE_COLOR, BEIGE_COLOR)


def close_program_container(app: tk.Tk, app_window: AppWindow, frame_manager: FrameManager) -> None:
    """
    Creates a button that closes the application when clicked.
    """
    # Obtén un frame contenedor
    frame = frame_manager.get_frame("main_container")

    # Crea el botón
    close_button = app_window.create_button(
        frame,
        text="Tancar programa ❌",
        font=("Times New Roman", 10),
        command=app.quit,
        bg=WHITE_COLOR,
        fg=BLACK_COLOR,
        highlightbackground=BEIGE_COLOR,
        padx=10,
        pady=5
    )
    close_button.pack(side="right", anchor="e", padx=10, pady=10)
