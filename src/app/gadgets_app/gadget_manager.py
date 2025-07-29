import tkinter as tk

from src.app.window_app import AppWindow
from src.app.utils.frame_manager import FrameManager
from src.app.gadgets_app.gadget_date import date_container
from src.app.gadgets_app.gadget_logo import app_logo_container
from src.app.gadgets_app.gadget_title import title_page_container
from src.app.gadgets_app.gadget_register_sales import payment_container
from src.app.gadgets_app.gadget_export_sales import export_excel_sales_container
from src.app.gadgets_app.gadget_visualize_sales import sales_visualizer_container
from src.app.gadgets_app.gadget_history_navigator import historical_sales_navigator_container
from src.app.gadgets_app.gadget_close_program import close_program_container
from src.app.gadgets_app.gadget_open_new_day import open_new_day_container

class GadgetManager:
    """
    Manager class for handling all gadgets in the application.
    Provides methods to create and manage different UI components.
    """
    
    @staticmethod
    def app_logo_container(app: tk.Tk, app_window: AppWindow, frame_manager: FrameManager) -> None:
        """Create and display the application logo"""
        app_logo_container(app, app_window, frame_manager)
    
    @staticmethod
    def title_page_container(app: tk.Tk, app_window: AppWindow) -> None:
        """Create and display the page title"""
        title_page_container(app, app_window)
    
    @staticmethod
    def date_container(app_window: AppWindow, frame_manager: FrameManager) -> None:
        """Create and display the date container"""
        date_container(app_window, frame_manager)
    
    @staticmethod
    def payment_container(app: tk.Tk, app_window: AppWindow, frame_manager: FrameManager) -> None:
        """Create and display the payment management container"""
        payment_container(app, app_window, frame_manager)
    
    @staticmethod
    def sales_visualizer_container(app: tk.Tk, app_window: AppWindow, frame_manager: FrameManager) -> None:
        """Create and display the sales visualizer"""
        sales_visualizer_container(app, app_window, frame_manager)

    @staticmethod
    def historical_sales_navigator_container(app: tk.Tk, app_window: AppWindow, frame_manager: FrameManager) -> None:
        historical_sales_navigator_container(app,  app_window, frame_manager)

    @staticmethod
    def close_program_container(app: tk.Tk, app_window: AppWindow, frame_manager: FrameManager) -> None:
        close_program_container(app, app_window, frame_manager)

    @staticmethod
    def open_new_day_container(app: tk.Tk, app_window: AppWindow, frame_manager: FrameManager) -> None:
        """Create and display the 'open new day' button"""
        open_new_day_container(app, app_window, frame_manager)

    @staticmethod
    def export_excel_sales_container(app_window: AppWindow, frame_manager: FrameManager) -> None:
        """Create and display the 'Export Sales' button"""
        export_excel_sales_container(app_window, frame_manager)