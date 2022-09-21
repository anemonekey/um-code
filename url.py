import sqlite3
from strgen import StringGenerator as SG

# create a new shortened url from a valid url and return it
# specify DB here for testing purposes
def create_shortened_url(long_url, db):
    # TODO: validate long_url? 
    # TODO: check if this loops in case the randomly generated string already exists
    while True:
        try:
            # generate a random string and add to base URL
            random_str = shorten()
            baseURL = "https://www.shorty.com/"
            shortenedURL = baseURL + random_str

            # open DB, insert, and close
            con = sqlite3.connect(db)
            cur = con.cursor() 
            sql_query = "INSERT INTO urls(short_url, long_url) VALUES(?, ?)"     
            sql_data = (shortenedURL, long_url)
            cur.execute(sql_query, sql_data)
            con.commit()
            return shortenedURL

        # TODO: how to differentiate error cases here
        # If the long URL is not unique
        except sqlite3.Error as err:
            raise err

        finally:
            if con:
                con.close()
    
# generate an 8 character string of alphanumeric chars
def shorten():
    random_str = SG("[\w\d]{8}").render()
    return random_str

# return the original url given a shortened url
def get_original_url(short_url, db):
    try:
        # check the database
        con = sqlite3.connect(db)
        con.row_factory = sqlite3.Row 
        cur = con.cursor()

        sql = '''SELECT `short_url`, `long_url`
        FROM `urls` WHERE `short_url` = ?'''

        cur.execute(sql, [short_url])
        row = cur.fetchone()

        return row['long_url']

    except sqlite3.Error as error:
        raise error

    finally:
        if con:
            con.close()
