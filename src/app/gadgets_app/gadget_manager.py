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


class GadgetManager:
    """
    Manager class for handling all gadgets in the application.
    Provides methods to create and manage different UI components.
    """

    @staticmethod
    def app_logo_container(app: tk.Tk, app_window: AppWindow, frame_manager: FrameManager) -> None:
        """Create and display the application logo container."""
        app_logo_container(app, app_window, frame_manager)

    @staticmethod
    def title_page_container(app: tk.Tk, app_window: AppWindow) -> None:
        """Create and display the main title of the application."""
        title_page_container(app, app_window)

    @staticmethod
    def date_container(app_window: AppWindow, frame_manager: FrameManager) -> None:
        """Create and display the current date container."""
        date_container(app_window, frame_manager)

    @staticmethod
    def payment_container(app: tk.Tk, app_window: AppWindow, frame_manager: FrameManager) -> None:
        """Create and display the sales registration and payment input container."""
        payment_container(app, app_window, frame_manager)

    @staticmethod
    def sales_visualizer_container(app: tk.Tk, app_window: AppWindow, frame_manager: FrameManager) -> None:
        """Create and display the sales visualizer component."""
        sales_visualizer_container(app, app_window, frame_manager)

    @staticmethod
    def historical_sales_navigator_container(app: tk.Tk, app_window: AppWindow, frame_manager: FrameManager) -> None:
        """Create and display the component for navigating historical sales."""
        historical_sales_navigator_container(app, app_window, frame_manager)

    @staticmethod
    def close_program_container(app: tk.Tk, app_window: AppWindow, frame_manager: FrameManager) -> None:
        """Create and display the button to close the program."""
        close_program_container(app, app_window, frame_manager)

    @staticmethod
    def export_excel_sales_container(app_window: AppWindow, frame_manager: FrameManager) -> None:
        """Create and display the button to export today's sales to an Excel file."""
        export_excel_sales_container(app_window, frame_manager)
