import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import Toplevel
from tkinter import messagebox
from tkcalendar import Calendar
from platformdirs import user_desktop_dir

from src.app.window_app import AppWindow
from src.utils.common.paths import ProjectPaths
from src.utils.common.logger import CustomLogger
from src.app.utils.frame_manager import FrameManager
from src.app.gadgets_app.gadget_utils import search_image
from src.utils.common.names import (METAL_GOLD_COLOR, BEIGE_COLOR, BLACK_COLOR)

logger = CustomLogger()
paths = ProjectPaths()

DB_NAME = f"{paths.database_dir}/sales.db"


def create_export_directory():
    try:
        # Get the user's desktop directory
        desktop = Path(user_desktop_dir())
        
        # Get current date components
        now = datetime.now()
        year = str(now.year)
        month = now.strftime('%B').lower()
        
        # Get the export directory path
        base_path = desktop / "Vendes_diaries_EISSA" / year / month
        base_path.mkdir(parents=True, exist_ok=True)
        
        return base_path
    except Exception as e:
        logger.error(f"Error creant directoris: {str(e)}")
        return None


def show_calendar():
    def confirm_date():
        selected_date = cal.get_date()
        top.destroy()
        export_sales_to_excel(selected_date)

    top = Toplevel()
    top.title("Calendari")

    cal = Calendar(
        top,
        selectmode='day',
        date_pattern='yyyy-mm-dd',
        font="Helvetica 12",
        background=BEIGE_COLOR,
        foreground=BLACK_COLOR,
        selectbackground=BEIGE_COLOR,
        selectforeground=METAL_GOLD_COLOR,
        headersbackground=BEIGE_COLOR,
        headersforeground=BLACK_COLOR,
        weekendbackground=BEIGE_COLOR,
        weekendforeground=METAL_GOLD_COLOR
    )
    cal.pack(pady=10)

    confirm_button = ttk.Button(top,
                                text="Confirmar",
                                command=confirm_date)
    confirm_button.pack(pady=10)

def export_sales_to_excel(date=None):
    try:
        if not date:
            show_calendar()
            return

            
        export_dir = create_export_directory()
        if not export_dir:
            messagebox.showerror("Error", "No s'ha pogut crear el directori d'exportació")
            return False

        conn = sqlite3.connect(DB_NAME)
        
        # Query to get the database data
        query = """
        SELECT date, time, amount, method
        FROM sales 
        WHERE date(date) = date(?)
        """
        
        df = pd.read_sql_query(query, conn, params=(date,))
        
        if df.empty:
            messagebox.showwarning("Avís", "No hi ha vendes per exportar avui")
            return False
            
        df.columns = ['DIA', 'HORA', 'IMPORT', 'METODE DE PAGAMENT']
        
        # Total calculus
        total_ventas = df['IMPORT'].sum()
        
        filename = f"vendes_eissa_{date}.xlsx"
        full_path = export_dir / filename
        
        with pd.ExcelWriter(str(full_path), engine='xlsxwriter') as writer:
            sheet_name = f"Vendes del dia {datetime.now().strftime('%d-%m-%Y')}"
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            
            # Header format
            header_format = workbook.add_format({
                'bg_color': '#D3D3D3',
                'bold': True,
                'border': 1
            })
            
            # Total format
            total_format = workbook.add_format({
                'bold': True,
                'bg_color': '#FFD700',  # Gold color
                'border': 1,
                'num_format': '#,##0.00€'
            })
            
            # Apply format to the header row
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Add data to the worksheet
            total_row = len(df) + 1
            worksheet.write(total_row, 0, "TOTAL VENDES:", total_format)
            worksheet.write(total_row, 2, total_ventas, total_format)
            
            # Adjust column widths
            for idx, col in enumerate(df.columns):
                series = df[col]
                max_len = max(
                    series.astype(str).map(len).max(),
                    len(str(series.name))
                ) + 2
                worksheet.set_column(idx, idx, max_len)

        messagebox.showinfo("Èxit", f"Arxiu Excel creat correctament!\nRuta: {full_path}")
        logger.info(f"Arxiu Excel creat exitosament: {full_path}")
        return True
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar l'arxiu Excel:\n{str(e)}")
        logger.error(f"Error a l'exportar a Excel: {str(e)}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

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
        excel_icon = excel_icon.resize((20, 20), Image.Resampling.LANCZOS)
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
        command=export_sales_to_excel,
        font=("Times New Roman", 12),
        bg=BEIGE_COLOR,
        fg=METAL_GOLD_COLOR,
        padx=10
    )
    
    # Needed to display the image correctly
    export_button.image = excel_icon
    export_button.pack(pady=5)