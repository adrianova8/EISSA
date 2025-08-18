from datetime import datetime
from tkinter import Toplevel, ttk
import sqlite3
import calendar
import pandas as pd
from pathlib import Path
from datetime import datetime, date
from PIL import Image, ImageTk
from tkinter import ttk, Toplevel, messagebox
from platformdirs import user_desktop_dir
from typing import Optional

from src.app.window_app import AppWindow
from src.utils.common.paths import ProjectPaths
from src.utils.common.logger import CustomLogger
from src.app.utils.frame_manager import FrameManager
from src.app.gadgets_app.gadget_utils import search_image
from src.utils.common.names import METAL_GOLD_COLOR, BEIGE_COLOR

logger = CustomLogger()
paths = ProjectPaths()
DB_NAME = f"{paths.database_dir}/sales.db"


def create_export_directory(year: Optional[str] = None,
                            month: Optional[str] = None,
                            day: Optional[str] = None) -> Optional[Path]:
    """
    Create export directory on desktop for daily sales.

    Args:
        year (Optional[str]): Year as string.
        month (Optional[str]): Month as string ('01'-'12').
        day (Optional[str]): Day as string ('01'-'31').

    Returns:
        Optional[Path]: Path object to the export directory, or None if error occurs.
    """
    try:
        desktop = Path(user_desktop_dir())
        base_path = desktop / "Vendes_diaries_EISSA"

        if year:
            base_path /= year
        if month:
            month_name = calendar.month_name[int(month)]
            base_path /= month_name
        if day:
            weekday_name = calendar.day_name[date(
                int(year), int(month), int(day)).weekday()]
            base_path /= f"{day}_{weekday_name}"

        base_path.mkdir(parents=True, exist_ok=True)
        return base_path

    except Exception as e:
        logger.error(f"Error creating directories: {e}")
        return None


def show_date_selector() -> None:
    """
    Display a GUI window to select year, month, and day, then export sales for that date.
    """
    try:
        def confirm_selection():
            selected_year = year_cb.get()
            selected_month = month_cb.get()
            selected_day = day_cb.get()
            top.destroy()
            export_sales_to_excel(year=selected_year,
                                  month=selected_month, day=selected_day)

        top = Toplevel()
        top.title("Seleccioni Data")

        ttk.Label(top, text="Any:").pack()
        current_year = datetime.now().year
        year_cb = ttk.Combobox(
            top, values=[str(y) for y in range(current_year-5, current_year+1)])
        year_cb.set(str(current_year))
        year_cb.pack()

        ttk.Label(top, text="Mes:").pack()
        months = [datetime(2000, m, 1).strftime('%m') for m in range(1, 13)]
        month_cb = ttk.Combobox(top, values=months)
        month_cb.set(datetime.now().strftime('%m'))
        month_cb.pack()

        ttk.Label(top, text="Dia:").pack()
        days = [str(d).zfill(2) for d in range(1, 32)]
        day_cb = ttk.Combobox(top, values=days)
        day_cb.set(datetime.now().strftime('%d'))
        day_cb.pack()

        ttk.Button(top, text="Confirmar",
                   command=confirm_selection).pack(pady=10)

    except Exception as e:
        logger.error(f"Error showing date selector: {e}")
        messagebox.showerror("Error", f"Failed to open date selector:\n{e}")


def export_sales_to_excel(year: Optional[str] = None,
                          month: Optional[str] = None,
                          day: Optional[str] = None) -> bool:
    """
    Export sales data from SQLite to Excel based on selected date.

    Args:
        year (Optional[str]): Year to filter sales.
        month (Optional[str]): Month to filter sales.
        day (Optional[str]): Day to filter sales.

    Returns:
        bool: True if export was successful, False otherwise.
    """
    try:
        if not year:
            show_date_selector()
            return False

        export_dir = create_export_directory(year, month, day)
        if not export_dir:
            messagebox.showerror("Error", "Failed to create export directory")
            return False

        conn = sqlite3.connect(DB_NAME)
        query = "SELECT date, time, amount, method FROM sales WHERE 1=1"
        params = []

        if year:
            query += " AND strftime('%Y', date) = ?"
            params.append(year)
        if month:
            query += " AND strftime('%m', date) = ?"
            params.append(month)
        if day:
            query += " AND strftime('%d', date) = ?"
            params.append(day)

        df = pd.read_sql_query(query, conn, params=params)

        if df.empty:
            messagebox.showwarning("Notice", "No sales to export")
            return False

        df.columns = ['DAY', 'TIME', 'AMOUNT', 'PAYMENT METHOD']
        total_sales = df['AMOUNT'].sum()

        if day:
            filename = f"vendes_EISSA_{year}_{month}_{day}.xlsx"
        elif month:
            filename = f"vendes_EISSA_{year}_{month}.xlsx"
        else:
            filename = f"vendes_EISSA_{year}.xlsx"

        full_path = export_dir / filename

        with pd.ExcelWriter(str(full_path), engine='xlsxwriter') as writer:
            sheet_name = f"Vendes {year}-{month}-{day}"
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            workbook = writer.book
            worksheet = writer.sheets[sheet_name]

            header_format = workbook.add_format(
                {'bg_color': '#D3D3D3', 'bold': True, 'border': 1})
            total_format = workbook.add_format(
                {'bold': True, 'bg_color': '#FFD700', 'border': 1, 'num_format': '#,##0.00€'})

            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)

            total_row = len(df) + 1
            worksheet.write(total_row, 0, "TOTAL VENDES:", total_format)
            worksheet.write(total_row, 2, total_sales, total_format)

            for idx, col in enumerate(df.columns):
                series = df[col]
                max_len = max(series.astype(str).map(
                    len).max(), len(str(series.name))) + 2
                worksheet.set_column(idx, idx, max_len)

        messagebox.showinfo("Èxit", f"Arxiu Excel creat:\n{full_path}")
        logger.info(f"Fitxer Excel creat correctament: {full_path}")
        return True

    except Exception as e:
        logger.error(f"Error exportant a Excel: {e}")
        messagebox.showerror("Error", f"Failed to export Excel:\n{e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()


def select_sales_period(app_window: AppWindow) -> None:
    """
    Display a GUI for selecting sales period: Day, Month, or Year.

    Args:
        app_window (AppWindow): The main application window.
    """
    try:
        def confirm_selection():
            choice = period_cb.get()
            top.destroy()
            if choice == "Dia":
                show_date_selector()
            elif choice == "Mes":
                show_month_selector()
            else:
                show_year_selector()

        top = Toplevel()
        top.title("Període de Vendes")

        ttk.Label(top, text="Seleccioni període de vendes:").pack(pady=5)
        period_cb = ttk.Combobox(top, values=["Dia", "Mes", "Any"])
        period_cb.set("Dia")
        period_cb.pack(pady=5)

        ttk.Button(top, text="Confirmar",
                   command=confirm_selection).pack(pady=10)

    except Exception as e:
        logger.error(f"Error showing sales period selector: {e}")
        messagebox.showerror("Error", f"Failed to select sales period:\n{e}")


def show_month_selector() -> None:
    """
    Display GUI to select year and month for sales export.
    """
    try:
        def confirm_selection():
            selected_year = year_cb.get()
            selected_month = month_cb.get()
            top.destroy()
            export_sales_to_excel(year=selected_year, month=selected_month)

        top = Toplevel()
        top.title("Seleccion Mes")

        ttk.Label(top, text="Any:").pack()
        current_year = datetime.now().year
        year_cb = ttk.Combobox(
            top, values=[str(y) for y in range(current_year-5, current_year+1)])
        year_cb.set(str(current_year))
        year_cb.pack()

        ttk.Label(top, text="Mes:").pack()
        months = [datetime(2000, m, 1).strftime('%m') for m in range(1, 13)]
        month_cb = ttk.Combobox(top, values=months)
        month_cb.set(datetime.now().strftime('%m'))
        month_cb.pack()

        ttk.Button(top, text="Confirmar",
                   command=confirm_selection).pack(pady=10)

    except Exception as e:
        logger.error(f"Error showing month selector: {e}")
        messagebox.showerror("Error", f"Failed to open date selector:\n{e}")

def show_year_selector():
    def confirm_selection():
        selected_year = year_cb.get()
        top.destroy()
        export_sales_to_excel(year=selected_year)

    top = Toplevel()
    top.title("Seleccioni any")

    ttk.Label(top, text="Any:").pack()
    current_year = datetime.now().year
    year_cb = ttk.Combobox(
        top, values=[str(y) for y in range(current_year-5, current_year+1)])
    year_cb.set(str(current_year))
    year_cb.pack()

    confirm_button = ttk.Button(
        top, text="Confirmar", command=confirm_selection)
    confirm_button.pack(pady=10)


def export_excel_sales_container(app_window: AppWindow, frame_manager: FrameManager) -> None:
    # Get the center container frame
    center_container = frame_manager.get_frame('center_container')
    
    # Create the export frame
    export_frame = app_window.create_frame(
        center_container,
        bg=BEIGE_COLOR
    )
    
    # Load and resize the Excel icon
    try:
        excel_icon = search_image("excel_logo.jpeg")
        excel_icon = excel_icon.resize((15, 15), Image.Resampling.LANCZOS)
        excel_icon = ImageTk.PhotoImage(excel_icon)
    except Exception as e:
        logger.error(f"Error carregant icona Excel: {str(e)}")
        excel_icon = None
    
    #  Create the export button
    export_button = app_window.create_button(
        export_frame,
        text="Exportar Vendes Excel",
        image=excel_icon,
        compound="top",
        command = lambda: select_sales_period(app_window),

        font=("Times New Roman", 12),
        bg=BEIGE_COLOR,
        fg=METAL_GOLD_COLOR,
        padx=10
    )
    
    # Needed to display the image correctly
    export_button.image = excel_icon
    export_button.pack(pady=5)



# Assuming logger, AppWindow, FrameManager, BEIGE_COLOR, METAL_GOLD_COLOR, search_image, select_sales_period, export_sales_to_excel are already defined elsewhere


def show_year_selector() -> None:
    """
    Opens a popup window for the user to select a year and triggers 
    the export_sales_to_excel function with the selected year.

    Returns:
        None
    """
    try:
        def confirm_selection() -> None:
            """
            Confirms the selected year and triggers the Excel export.
            """
            try:
                selected_year = year_cb.get()
                top.destroy()
                export_sales_to_excel(year=selected_year)
            except Exception as e:
                logger.error(f"Error confirming year selection: {str(e)}")

        top = Toplevel()
        top.title("Seleccioni Any")

        ttk.Label(top, text="Any:").pack()
        current_year = datetime.now().year
        year_cb = ttk.Combobox(
            top, values=[str(y) for y in range(current_year-5, current_year+1)]
        )
        year_cb.set(str(current_year))
        year_cb.pack()

        confirm_button = ttk.Button(
            top, text="Confirmar", command=confirm_selection
        )
        confirm_button.pack(pady=10)

    except Exception as e:
        logger.error(f"Error showing year selector popup: {str(e)}")


def export_excel_sales_container(app_window: "AppWindow", frame_manager: "FrameManager") -> None:
    """
    Creates a container frame in the center of the app window with a button 
    to export sales data to Excel.

    Args:
        app_window (AppWindow): Main application window object.
        frame_manager (FrameManager): Manager for app frames.

    Returns:
        None
    """
    try:
        # Get the center container frame
        center_container = frame_manager.get_frame('center_container')

        # Create the export frame
        export_frame = app_window.create_frame(
            center_container,
            bg=BEIGE_COLOR
        )

        # Load and resize the Excel icon
        try:
            excel_icon = search_image("excel_logo.jpeg")
            excel_icon = excel_icon.resize((15, 15), Image.Resampling.LANCZOS)
            excel_icon = ImageTk.PhotoImage(excel_icon)
        except Exception as e:
            logger.error(f"Error loading Excel icon: {str(e)}")
            excel_icon = None

        # Create the export button
        export_button = app_window.create_button(
            export_frame,
            text="Export Sales to Excel",
            image=excel_icon,
            compound="top",
            command=lambda: select_sales_period(app_window),
            font=("Times New Roman", 12),
            bg=BEIGE_COLOR,
            fg=METAL_GOLD_COLOR,
            padx=10
        )

        # Needed to display the image correctly
        export_button.image = excel_icon
        export_button.pack(pady=5)

    except Exception as e:
        logger.error(f"Error creating export Excel container: {str(e)}")
