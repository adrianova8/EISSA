import tkinter as tk

from src.app.window_app import AppWindow
from src.utils.common.logger import CustomLogger
from src.app.utils.frame_manager import FrameManager
from src.app.gadgets_app.gadget_utils import current_time
from src.utils.common.names import MEDIUM_GRAY_COLOR, METAL_GOLD_COLOR, BROWN_COLOR

logger = CustomLogger()

def date_container(app_window: AppWindow, frame_manager: FrameManager) -> None:
    """
    Create and configure the date display container.
    
    Creates a frame showing the current date in Catalan format,
    positioned in the top-right corner of the header.
    
    Args:
        app_window (AppWindow): Window manager instance for creating widgets
        frame_manager (FrameManager): Frame manager for accessing existing frames
        
    Returns:
        None
        
    Raises:
        tk.TclError: If there's an error creating Tkinter widgets
        ValueError: If header frame is not found
    """
    try:
        # Get header frame
        header_frame = frame_manager.get_frame('header')
        if not header_frame:
            raise ValueError("Header frame not found in frame manager")

        # Create outer date frame with border
        date_outer_frame = app_window.create_frame(
            header_frame,
            bg=BROWN_COLOR,  
            side="right",
            padx=10
        )

        # Create inner date frame
        date_inner_frame = app_window.create_frame(
            date_outer_frame,
            bg=BROWN_COLOR,
            padx=10
        )
        date_inner_frame.pack()

        # Get current date and create label
        date = current_time()
        date_label = app_window.create_label(
            date_inner_frame,
            text=date,
            font=("Times New Roman",25),
            bg=BROWN_COLOR,
            fg=METAL_GOLD_COLOR
        )
        date_label.pack()

    except tk.TclError as e:
        logger.error(f"Error creating date container: {str(e)}")
        raise
    except ValueError as e:
        logger.error(f"Frame error: {str(e)}")
        raise