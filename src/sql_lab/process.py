import logging
import os

import mysql.connector
import pandas as pd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

DBHOST = os.environ.get("DBHOST")
DBUSER = os.environ.get("DBUSER")
DBPASS = os.environ.get("DBPASS")
DBNAME = os.environ.get("DBNAME")

COLUMNS = ["id", "group", "last_name", "email", "gender", "ip_address"]


def read_data(filename):
    logger.info("Reading data from %s", filename)
    df = pd.read_csv(filename)
    logger.info("Read %d rows and %d columns", df.shape[0], df.shape[1])
    return df


def clean_data(data):
    before = len(data)
    cleaned = data.dropna().reset_index(drop=True)
    logger.info(
        "Cleaned data: %d rows before, %d after (%d dropped)",
        before, len(cleaned), before - len(cleaned),
    )
    return cleaned


def load_data(data, table):


    if not table.isidentifier():
        raise ValueError(f"Invalid table name: {table!r}")

    create_sql = f"""
        CREATE TABLE IF NOT EXISTS `{table}` (
            id          BIGINT       NOT NULL,
            `group`     VARCHAR(50)  NOT NULL,
            last_name   VARCHAR(100) NOT NULL,
            email       VARCHAR(255) NOT NULL,
            gender      VARCHAR(50)  NOT NULL,
            ip_address  VARCHAR(45)  NOT NULL,
            PRIMARY KEY (id)
        )
    """

    insert_sql = (
        f"INSERT INTO `{table}` (id, `group`, last_name, email, gender, ip_address) "
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )

    rows = data[COLUMNS].astype(object).values.tolist()

    conn = None
    try:
        conn = mysql.connector.connect(
            host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME
        )
        cursor = conn.cursor()
        logger.info("Connected to %s on %s", DBNAME, DBHOST)

        cursor.execute(create_sql)
        logger.info("Ensured table `%s` exists", table)

        cursor.execute(f"DELETE FROM `{table}`")

        for row in rows:
            cursor.execute(insert_sql, tuple(row))

        conn.commit()
        logger.info("Inserted %d rows into `%s`", len(rows), table)
    except mysql.connector.Error as err:
        logger.error("Database error: %s", err)
        if conn is not None:
            conn.rollback()
        raise
    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            logger.info("Connection closed")


def main():

    if not all([DBHOST, DBUSER, DBPASS, DBNAME]):
        logger.error("Set DBHOST, DBUSER, DBPASS, and DBNAME before running.")
        return

    df = read_data("MOCK_DATA.csv")
    cleaned = clean_data(df)
    load_data(cleaned, "mock")


if __name__ == "__main__":
    main()