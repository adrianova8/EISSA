import schedule
import threading
import time
import datetime
from workalendar.europe import Catalonia
from src.app.triggers.send_report_generator import ReportGenerator
from src.app.triggers.mailer import Mailer

class SalesReporter:
    def __init__(self, hour="20:30"):
        self.hour = hour
        self.thread = threading.Thread(target=self._start_scheduler, daemon=True)
        self.calendar = Catalonia()

    def is_working_day(self, date):
        """Comprueba si es día laborable según el calendario español"""
        return self.calendar.is_working_day(date)

    def start(self):
        schedule.every().day.at(self.hour).do(self._check_and_send_report)
        self.thread.start()

    def _start_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check once per minute

    def _check_and_send_report(self):
        """Verifica si es día laborable antes de enviar el reporte"""
        today = datetime.date.today()
        if self.is_working_day(today):
            self._generate_and_send_report()
        else:
            print(f"Hoy ({today}) no es día laborable - no se enviará reporte")

    def _generate_and_send_report(self):
        today = datetime.date.today()
        excel_path, pdf_path = ReportGenerator().generate(today)
        Mailer().send_report(today, excel_path, pdf_path)