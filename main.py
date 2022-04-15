from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from config import URL_currency, DRIVER_PATH, difference
from selenium import webdriver
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

s = Service(DRIVER_PATH)
driver = webdriver.Chrome(service=s)
driver.minimize_window()


class Currency:
    currency_rate_start = 0
    previous_rate = 0

    def get_currency(self):
        driver.get(url=URL_currency)
        time.sleep(2)
        currency_item = driver.find_element(By.XPATH, '//span[@data-role = "stat-average-bid-value"]')
        currency_rate = 0 if currency_item.text == '—' else currency_item.text
        return float(currency_rate)

    def check_currency(self):
        currency_rate = self.get_currency()
        if currency_rate >= self.currency_rate_start + difference and self.currency_rate_start > 0:
            self.currency_rate_start = currency_rate
            self.previous_rate = currency_rate
            self.send_mail(msg_text='Курс змінився більше ніж на {} грн. і становить {}'.format(str(difference), str(currency_rate)), subject='Актуальний курс валют')
        elif self.previous_rate != currency_rate:
            print("Обмінний курс долару становить: " + str(currency_rate))
            self.previous_rate = currency_rate
        time.sleep(10)
        self.check_currency()

    def send_mail(self, msg_text, subject):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('', '')

        msg = MIMEText(msg_text, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')

        server.sendmail(
            '',
            '',
            msg.as_string()
        )
        server.quit()


currency = Currency()
currency.check_currency()
