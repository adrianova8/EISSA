import sqlite3
import pandas as pd
from pathlib import Path
from platformdirs import user_desktop_dir
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import messagebox

from src.app.window_app import AppWindow
from src.utils.common.paths import ProjectPaths
from src.utils.common.logger import CustomLogger
from src.app.utils.frame_manager import FrameManager
from src.app.gadgets_app.gadget_utils import search_image
from src.utils.common.names import (METAL_GOLD_COLOR, BEIGE_COLOR)

logger = CustomLogger()
paths = ProjectPaths()

DB_NAME = f"{paths.database_dir}/sales.db"


def create_export_directory():
    try:
        # Obtener ruta del escritorio
        desktop = Path(user_desktop_dir())
        
        # Obtener fecha actual
        now = datetime.now()
        year = str(now.year)
        month = now.strftime('%B').lower()
        
        # Crear estructura de carpetas
        base_path = desktop / "Vendes_diaries_EISSA" / year / month
        base_path.mkdir(parents=True, exist_ok=True)
        
        return base_path
    except Exception as e:
        logger.error(f"Error creando directorios: {str(e)}")
        return None


def export_sales_to_excel(date=None):
    try:
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
            
        export_dir = create_export_directory()
        if not export_dir:
            messagebox.showerror("Error", "No s'ha pogut crear el directori d'exportació")
            return False
            
        conn = sqlite3.connect(DB_NAME)
        
        # Consulta para obtener ventas
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
        
        # Calcular total
        total_ventas = df['IMPORT'].sum()
        
        filename = f"vendes_eissa_{datetime.now().strftime('%Y%m%d')}.xlsx"
        full_path = export_dir / filename
        
        with pd.ExcelWriter(str(full_path), engine='xlsxwriter') as writer:
            sheet_name = f"Vendes del dia {datetime.now().strftime('%d-%m-%Y')}"
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            
            # Formato para la cabecera
            header_format = workbook.add_format({
                'bg_color': '#D3D3D3',
                'bold': True,
                'border': 1
            })
            
            # Formato para el total
            total_format = workbook.add_format({
                'bold': True,
                'bg_color': '#FFD700',  # Color dorado
                'border': 1,
                'num_format': '#,##0.00€'
            })
            
            # Aplicar formato a la cabecera
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Añadir fila de total
            total_row = len(df) + 1
            worksheet.write(total_row, 0, "TOTAL VENDES:", total_format)
            worksheet.write(total_row, 2, total_ventas, total_format)
            
            # Ajustar ancho de columnas
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
        logger.error(f"Error al exportar a Excel: {str(e)}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def export_excel_sales_container(app_window: AppWindow, frame_manager: FrameManager) -> None:
    # Obtener el frame donde colocaremos el botón
    center_container = frame_manager.get_frame('center_container')
    
    # Crear frame para el botón
    export_frame = app_window.create_frame(
        center_container,
        bg=BEIGE_COLOR

    )
    
    # Cargar y redimensionar el icono
    try:
        excel_icon = search_image("excel_logo.jpeg")
        excel_icon = excel_icon.resize((20, 20), Image.Resampling.LANCZOS)
        excel_icon = ImageTk.PhotoImage(excel_icon)
    except Exception as e:
        logger.error(f"Error cargando icono Excel: {str(e)}")
        excel_icon = None
    
    # Crear botón de exportación con icono
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
    
    # Necesario para mantener referencia del icono
    export_button.image = excel_icon
    export_button.pack(pady=5)