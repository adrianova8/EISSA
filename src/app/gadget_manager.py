import tkinter as tk

from src.app.window_app import AppWindow
from src.app.utils.frame_manager import FrameManager
from src.app.gadgets_app.gadget_logo import app_logo_container
from src.app.gadgets_app.gadget_title import title_page_container
from src.app.gadgets_app.gadget_date import date_container
from src.app.gadgets_app.gadget_register_sales import payment_container
from src.app.gadgets_app.gadget_visualize_sales import sales_visualizer_container


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

