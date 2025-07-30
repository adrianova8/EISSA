import datetime
from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

from src.utils.common.paths import ProjectPaths
from src.data.db.sales_record_db import get_sales_by_date

paths = ProjectPaths()

class ReportGenerator:
    def get_daily_sales(self, date: datetime.date):
        """Obtiene las ventas del día especificado"""
        return get_sales_by_date(date)

    def generate(self, date: datetime.date):
        # Obtener datos reales de ventas
        daily_sales = self.get_daily_sales(date)
        
        # Excel
        excel_path = str(paths.app_dir / "triggers" / "reports" / f"sales_{date}.xlsx")
        wb = Workbook()
        ws = wb.active
        ws.append(['DIA', 'HORA', 'IMPORT', 'METODE DE PAGAMENT'])
        
        # Añadir datos reales
        total_day = 0
        for sale in daily_sales:
            row = [
                date.strftime("%d-%m-%Y"),
                sale[0],
                sale[1],
                sale[2]
            ]
            ws.append(row)
            total_day += sale[1]
            
        # Añadir total del día
        ws.append(["", "TOTAL:", total_day, ""])
        wb.save(excel_path)

        # PDF
        pdf_path = str(paths.app_dir / "triggers" / "reports" / f"sales_{date}.pdf")
        pdf = SimpleDocTemplate(pdf_path)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        story.append(Paragraph(f"Informe de vendes - {date}", styles['Title']))
        
        # Tabla de datos
        data = [['DIA', 'HORA', 'IMPORT', 'METODE DE PAGAMENT']]
        for sale in daily_sales:
            data.append([
                date.strftime("%d-%m-%Y"),
                sale[0],
                f"{sale[1]}€",
                sale[2]
            ])
        data.append(["", "TOTAL:", f"{total_day:.2f}€", ""])
        
        # Crear y estilizar tabla
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        
        pdf.build(story)

        return excel_path, pdf_path