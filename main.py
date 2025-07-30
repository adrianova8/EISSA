import tkinter as tk

from src.app.window_app import AppWindow
from src.app.gadgets_app import gadget_manager
from src.utils.common.logger import CustomLogger
from src.app.utils.frame_manager import FrameManager
from src.utils.common.names import BUSINESS_NAME, BEIGE_COLOR
# from src.app.triggers.trigger_daily_sales_report import SalesReporter


def on_escape(event):
    # Disable fullscreen mode when Escape key is pressed
    app.attributes("-fullscreen", False)


def handle_window_state(event):
    # If the window is not fullscreen, reset to full dimensions
    if not app.attributes("-fullscreen"):
        app_window.window_dimensions(width_ratio=1.0, height_ratio=1.0)


if __name__ == "__main__":
    logger = CustomLogger()
    logger.info("Starting the application...")
    app = tk.Tk()
    app.attributes("-fullscreen", True)

    # Managers
    app_window = AppWindow(app)
    frame_manager = FrameManager()

    # Set title, dimensions, background color, and frames for the main window
    app_window.window_title(BUSINESS_NAME)
    app_window.window_dimensions(width_ratio=1.0, height_ratio=1.0)  # Fullscreen mode
    app_window.window_bg_color(BEIGE_COLOR)

    # Load UI components (gadgets)
    # 1.- Title page in the app
    gadget_manager.title_page_container(app, app_window, frame_manager)
    # 2.- Today's date in the app
    gadget_manager.date_container(app_window, frame_manager)
    # 3.- Payment interface
    gadget_manager.payment_container(app, app_window, frame_manager)
    # 4.- Historical sales navigator interface
    gadget_manager.historical_sales_navigator_container(app, app_window, frame_manager)
    # 5.- Sales visualizer interface
    gadget_manager.sales_visualizer_container(app_window, frame_manager)
    # 6.- Close program burron in the app
    gadget_manager.close_program_container(app, app_window, frame_manager)
    # 7.- Export sales to Excel interface
    gadget_manager.export_excel_sales_container(app_window, frame_manager)
    # gadget_manager.app_logo_container(app, app_window, frame_manager) -- deprecated. Logo is now in the title page
    

    # Triggers
    # 1.- Trigger 1: trigger_daily_sales_report (send daily sales reports via email)
    # sales_reporter = SalesReporter()
    # sales_reporter.start()
    # TODO 2.- Trigger 2: monthly trigger to send the monthly sales report. Monthly metrics.
    # TODO 3.- Trigger 3: quarterly trigger to clean the SQLite database

    # Key bindings
    app.bind("<Escape>", on_escape)
    app.bind("<Configure>", handle_window_state)

    # MainLoop (keeps the application running)
    app.mainloop()
