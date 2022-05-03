import datetime
import coloredlogs
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.chrome.service import Service

from loader import bot, db

from vendry_scraper.scraper import Vendry
from utils.notifications.reporter import Reporter

if __name__ == '__main__':
    try:
        # driver
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument("--remote-debugging-port=9222")
        # options.add_argument("--proxy-server=p.webshare.io:10000")
        options.headless = True

        driver = webdriver.Remote('http://localhost:4444/wd/hub', options=options)

        # s = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        # driver = webdriver.Chrome(service=s, options=options)

        PARSING_STARTED = datetime.datetime.now()
        vendry = Vendry(driver, db)
        bot.send_message("Vendry scraper started at: " + str(PARSING_STARTED))
        vendry.start()
        PARSING_FINISHED = datetime.datetime.now()

        print('PARSING FINISHED')

        reporter = Reporter(db, PARSING_STARTED, PARSING_FINISHED)
        reporter.parse_table('vendry')
        driver.quit()
    except Exception as e:
        bot.send_message(
            f"[ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ] Vendry parser filed with error: \n"
            f"{e}")

        print(e)
        try:
            driver.quit()
        except:
            pass