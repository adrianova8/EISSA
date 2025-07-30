import tkinter as tk

from src.app.gadgets_app import gadget_manager
from src.app.window_app import AppWindow
from src.utils.common.logger import CustomLogger
from src.app.utils.frame_manager import FrameManager
# from src.app.triggers.trigger_daily_sales_report import SalesReporter
from src.utils.common.names import BUSINESS_NAME, BEIGE_COLOR

def on_escape(event):
    app.attributes("-fullscreen", False)

def handle_window_state(event):
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

    # Title, dimensions, background color, frames for the window
    app_window.window_title(BUSINESS_NAME)
    app_window.window_dimensions(width_ratio=1.0, height_ratio=1.0)  # Pantalla completa
    app_window.window_bg_color(BEIGE_COLOR)

    # gadgets call
    # gadget_manager.app_logo_container(app, app_window, frame_manager)
    gadget_manager.title_page_container(app, app_window, frame_manager)
    gadget_manager.date_container(app_window, frame_manager)
    gadget_manager.payment_container(app, app_window, frame_manager)
    gadget_manager.historical_sales_navigator_container(app, app_window, frame_manager)
    gadget_manager.sales_visualizer_container(app_window, frame_manager)
    # gadget_manager.open_new_day_container(app, app_window, frame_manager)
    gadget_manager.close_program_container(app, app_window, frame_manager)

    # Añadir un botón que permita descargar en formato Excel los datos de venta que se han hecho a lo largo del dia de hoy
    gadget_manager.export_excel_sales_container(app_window, frame_manager)

    # Triggers
    # 1.- Trigger 1: trigger_daily_sales_report (envio por correo de los reportes de ventas diarios)
    # sales_reporter = SalesReporter()
    # sales_reporter.start()
    # #TODO 2.- Trigger 2: monthly trigger to send the monthly sales report. Monthy metrics.
    # #TODO 3.- Trigger 3: quarterly trigger to clean the sqlite database
    
    # Bindings
    app.bind("<Escape>", on_escape)
    app.bind("<Configure>", handle_window_state)

    # MainLoop (keeps the app running)
    app.mainloop()
    