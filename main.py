import tkinter as tk

from src.app.gadgets_app import gadget_manager
from src.app.window_app import AppWindow
from src.utils.common.logger import CustomLogger
from src.app.utils.frame_manager import FrameManager
from src.utils.common.names import BUSINESS_NAME, MEDIUM_GRAY_COLOR



if __name__ == "__main__":
    logger = CustomLogger()
    logger.info("Starting the application...")
    app = tk.Tk()
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)
    frame_manager = FrameManager()

    # Window configuration
    app_window = AppWindow(app)

    # Title, dimensions, background color, frames for the window
    app_window.window_title(BUSINESS_NAME)
    app_window.window_dimensions(width_ratio=1.0, height_ratio=1.0)  # Pantalla completa
    app_window.window_bg_color(MEDIUM_GRAY_COLOR)

    # # gadgets call
    gadget_manager.app_logo_container(app, app_window, frame_manager)
    gadget_manager.title_page_container(app, app_window)
    gadget_manager.date_container(app_window, frame_manager)
    gadget_manager.payment_container(app, app_window, frame_manager)
    gadget_manager.historical_sales_navigator_container(app, app_window, frame_manager)
    gadget_manager.sales_visualizer_container(app_window, frame_manager)
    gadget_manager.open_new_day_container(app, app_window, frame_manager)
    gadget_manager.close_program_container(app, app_window, frame_manager)

    # MainLoop (keeps the app running)
    app.mainloop()
    