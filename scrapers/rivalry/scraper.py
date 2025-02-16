import os
import time
import sentry_sdk
import logging.config
from selenium import webdriver

from config import LOGGING, RIVALRY_URL
from utils import transcribe_table_data, postgres_db_insert


# get os config variables
ENVIRONMENT = os.environ['ENVIRONMENT']
SENTRY_URL = os.environ['SENTRY_URL']
DB_CREDENTIALS = {
        'host': os.environ['DB_HOST'],
        'user': os.environ['DB_USER'],
        'password': os.environ['DB_PASSWORD'],
        'dbname': os.environ['DB_NAME']
}


# initialize logging and monitoring
logging.config.dictConfig(LOGGING)
logger = logging.getLogger(ENVIRONMENT)
if ENVIRONMENT == 'PRODUCTION':
        sentry_sdk.init(SENTRY_URL)


if __name__ == '__main__':

        logger.info('Starting scrape job for rivalry table data')

        # initialize headless selenium webdriver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(chrome_options=chrome_options)

        # load website / raw table data
        driver.get(RIVALRY_URL)
        time.sleep(5)  # give webpage time to load table
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll down to load dynamic content
        time.sleep(1)
        table = driver.find_element_by_id('__nuxt').get_attribute("innerHTML")
        table = transcribe_table_data(table)

        # Output
        if len(table) == 1:
            logger.info('Finished processing of %s row', len(table))
        else:
            logger.info('Finished processing of %s rows', len(table))

        # insert to db
        if ENVIRONMENT ==  "PRODUCTION":
            if len(table) > 0:
                if len(table) == 1:
                    logger.info('Inserting %s row into database', len(table))
                else:
                    logger.info('Inserting %s rows into database', len(table))
                postgres_db_insert(table, DB_CREDENTIALS)
            else:
                logger.warning('rivalry data scrape produced 0 data points')
        elif ENVIRONMENT == "DEVELOPMENT":
                logger.info('Produced data: %s', table)
        else:
                logger.warning("ENVIRONMENT environment variable not set correctly")

        driver.quit()
