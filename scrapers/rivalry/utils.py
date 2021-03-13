import time
import logging
import datetime
import psycopg2
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def transcribe_table_data(table):
        """Extract data from raw table and fit to sql schema.

        Parameters
        ----------
        table : list
                List of raw match table data.

        Returns
        -------
        Transcribed data table according to SQL format.
        """
        page = BeautifulSoup(table, 'html.parser')
        dates = page.find_all("h2", class_="bet-center-inner-container")
        matches = page.find_all(class_="bet-line")
        # time
        # invariant: date is the correct date for the current match
        date = datetime.date.today()
        to_insert = []
        for index, match in enumerate(matches):
            temp = dates[index].getText()
            if temp != "false" and temp != "Today":
                if temp == "Tomorrow":
                    # the the entries from the current one up to the one before the next non-false temp have tomorrow's date
                    date = datetime.date.today() + datetime.timedelta(days=1)
                else:
                    # process date text into date
                    date = datetime.datetime.strptime(temp, "%B %d, %Y").date()


            current = match.find(class_="match-time").getText()
            if current == "Live Now":
                continue
            # datetime doesn't have great facilities for parsing est/edt so I will manually compute the offsets
            if(current.split(' ')[1] == "EST"):
                offset = datetime.timedelta(hours=5)
            if(current.split(' ')[1] == "EDT"):
                offset = datetime.timedelta(hours=4)
            if current.split(' ')[1] == "UTC":
                offset = datetime.timedelta(hours = 0)
            # produce timestamp we will write to database
            utctime = datetime.datetime.strptime(current.split(' ')[0], "%H:%M") + offset
            utctime = utctime.time()
            match_start_time_utc = datetime.datetime.combine(date, utctime)
            tournament = match.find_all(class_="tournament-market")
            odds = match.find_all(class_="odds")
            teams = match.find_all(class_="team-name")
            to_insert.append((teams[0].getText(), teams[1].getText(), odds[0].getText(), odds[1].getText(), -1, "winner", int(time.time()), int(datetime.datetime.timestamp(match_start_time_utc)), tournament[0].getText(), "rival"))
        return to_insert

def postgres_db_insert(data, db_credentials):
        """Insert odds data into database.

        PARAMS
        ------
        data : list of tuples
                List of tuples containing ordered entries of team_1, team_2, team_1_winner_odds, team_2_winner_odds,
                scrape_time, match_time, tournament_name, source.
        db_credentials : dict
                A dictionary containing key-value log in credentials for the database.
        """

        conn = None
        insert_statement = """
                INSERT INTO odds (
                        team_1, team_2, team_1_winner_odds, team_2_winner_odds, draw_odds, bet_type, scrape_time, match_time, tournament_name, source
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        try:
                conn = psycopg2.connect(**db_credentials)
                cursor = conn.cursor()
                cursor.executemany(insert_statement, data)
                conn.commit()
                cursor.close()
                logger.info('Inserted %s rows.', len(data))
        except psycopg2.DatabaseError:
                logger.error('Failed to insert %s rows into database.', len(data))
        finally:
                if conn:
                        conn.close()
