from tkinter import Tk
from tkinter import Frame, Label
from PIL import Image, ImageTk

from src.app.window_app import AppWindow
from src.app.utils.frame_manager import FrameManager
from src.utils.common.logger import CustomLogger
from src.app.gadgets_app.gadget_utils import search_image
from src.utils.common.names import BROWN_COLOR, MEDIUM_GRAY_COLOR

logger = CustomLogger()


def app_logo_container(app: Tk, app_window: AppWindow, frame_manager: FrameManager) -> None:
    """
    Create and display the application logo in the main window header.
    
    This function loads a logo image, creates necessary frames and displays
    the logo in the application header.
    
    Args:
        app (Tk): Main Tkinter window instance
        app_window (AppWindow): Window manager instance for frame creation
        
    Returns:
        Optional[Frame]: Header frame containing the logo if successful, None if failed
        
    Raises:
        FileNotFoundError: If logo image file cannot be found
        PIL.UnidentifiedImageError: If image file is invalid
        tk.TclError: If there's an error creating Tkinter widgets
    """
    try:
        # Load and convert logo image
        original_image: Image = search_image(image_name="style_logo4.png")
        logo: ImageTk.PhotoImage = ImageTk.PhotoImage(original_image)
        
        # Create main header container frame
        header_frame = frame_manager.get_frame('header')
        if not header_frame:
            header_frame: Frame = app_window.create_frame(
                app, 
                bg=MEDIUM_GRAY_COLOR,
                fill="x",
                padx=5,
                pady=8
            )
            frame_manager.register_frame('header', header_frame)

        # Create specific frame for logo
        logo_frame: Frame = app_window.create_frame(
            header_frame,
            bg=MEDIUM_GRAY_COLOR,
            side="left",
            padx=5
        )

        # Create and configure logo label
        logo_label: Label = app_window.create_label(
            logo_frame,
            image=logo,
            bg=BROWN_COLOR,
        )
        logo_label.image = logo  # Keep reference to prevent garbage collection
        logo_label.pack()  # Position label in container
        
        return header_frame
        
    except FileNotFoundError as e:
        logger.error(f"Logo image not found: {e}")
        return None
    except Exception as e:
        logger.error(f"Error creating logo: {e}")
        return None
