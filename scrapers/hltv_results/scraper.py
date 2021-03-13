import os
import sentry_sdk
import logging.config
from selenium import webdriver

from config import LOGGING, HLTV_URL
from utils import transcribe_table_data, calc_average_header_date, postgres_db_upsert


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

        logger.info('Starting scrape job for HLTV match results data')

        # initialize headless selenium webdriver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(chrome_options=chrome_options)

        # load website / raw table data
        driver.get(HLTV_URL)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # transcribe raw html to condensed tabular data
        headers = driver.find_elements_by_class_name('standard-headline')
        header_text = [header.text for header in headers]
        match_time = calc_average_header_date(header_text)
        table = driver.find_elements_by_class_name('result')
        result_text = [row.text for row in table]
        match_data = transcribe_table_data(result_text, match_time)
        driver.quit()
        if len(table) == 1:
            logger.info('Finished processing %s row', len(table))
        else:
            logger.info('Finished processing %s rows', len(table))

        # insert to db
        if ENVIRONMENT == "PRODUCTION":
            if len(table) > 0:
                if len(table) == 1:
                    logger.info('Inserting %s row into database', len(table))
                else:
                    logger.info('Inserting %s rows into database', len(table))
                postgres_db_upsert(match_data, DB_CREDENTIALS)
            else:
                logger.warning('HLTV data scrape produced 0 data points')
        elif ENVIRONMENT == "DEVELOPMENT":
            logger.info('Produced data: %s', table)
        else:
            logger.warning("ENVIRONMENT environment variable not set correctly")
 

