import tkinter as tk
from tkinter import Tk
from PIL import ImageTk

from src.app.window_app import AppWindow
from src.app.utils.frame_manager import FrameManager
from src.utils.common.logger import CustomLogger
from src.app.gadgets_app.gadget_utils import search_image
from src.utils.common.names import BUSINESS_NAME, BROWN_COLOR, METAL_GOLD_COLOR

logger = CustomLogger()

def title_page_container(app: Tk, app_window: AppWindow, frame_manager: FrameManager) -> None:
    """
    Create and configure the title container for the application.
    
    Creates a header frame with the business name displayed in a
    professional format.
    
    Args:
        app (Tk): Main application window instance
        app_window (AppWindow): Window manager instance
        
    Returns:
        None
        
    Raises:
        tk.TclError: If there's an error creating Tkinter widgets
    """
    try:
        # get the header frame
        header_frame = frame_manager.get_frame("header")
        if not header_frame:
            header_frame = app_window.create_frame(
                app, 
                bg=BROWN_COLOR,
                fill="x",
            )
        frame_manager.register_frame("header", header_frame)
    
        # Create title frame
        title_frame = app_window.create_frame(
            header_frame,
            bg=BROWN_COLOR,
            side="bottom",
        )

        # Add an image in the title
        original_image = search_image("style_logo4.png")
        title_image = ImageTk.PhotoImage(original_image)
        
        # Image next to title
        image_label = app_window.create_label(
            title_frame,
            image=title_image,
            bg=BROWN_COLOR
        )
        image_label.image = title_image  # Keep a reference to avoid garbage collection
        image_label.pack(side="left")

        # Create title label
        title_label = app_window.create_label(
            title_frame,
            text=BUSINESS_NAME,
            font=("Times New Roman", 24, "bold"),
            bg=BROWN_COLOR,
            fg=METAL_GOLD_COLOR,
        )
        title_label.pack(side="right")
        
    except tk.TclError as e:
        logger.error(f"Error creating title container: {str(e)}")
        raise