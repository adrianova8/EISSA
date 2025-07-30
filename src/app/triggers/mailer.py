import yagmail
import datetime

class Mailer:
    def __init__(self):
        self.user = "adrianova8@gmail.com"
        self.password = "kwgu lvia sobd lusr"
        self.receiver = "adrianova8@gmail.com"
        self.yag = yagmail.SMTP(self.user, self.password)

    def send_report(self, date, excel_path, pdf_path):
        subject = f"Informe Diari de Vendes EISSA {date}"
        body = "Adjunt l'informe diari en format Excel i PDF."
        self.yag.send(to=self.receiver, subject=subject, contents=body, attachments=[excel_path, pdf_path])
