
import logging
import os

import mysql.connector

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

DBHOST = os.environ.get("DBHOST")
DBUSER = os.environ.get("DBUSER")
DBPASS = os.environ.get("DBPASS")
DBNAME = os.environ.get("DBNAME")

ALLOWED_COLUMNS = {"id", "group", "last_name", "email", "gender", "ip_address"}


def get_connection():
    logger.info("Connecting to %s on %s", DBNAME, DBHOST)
    return mysql.connector.connect(
        host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME
    )


def get_data_by_group(value):

    query = "SELECT id, `group`, last_name, email, gender, ip_address FROM mock WHERE `group` = %s"
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (value,))  # trailing comma makes it a tuple
        rows = cursor.fetchall()
        logger.info("Found %d rows where group = %r", len(rows), value)
        return rows
    except mysql.connector.Error as err:
        logger.error("Database error in get_data_by_group: %s", err)
        return []
    finally:
        # Always close the connection, even if the query failed
        if conn is not None and conn.is_connected():
            conn.close()


def plot_counts(groupby):
    if groupby not in ALLOWED_COLUMNS:
        raise ValueError(f"Unknown column: {groupby!r}")

    query = (
        f"SELECT `{groupby}`, COUNT(*) AS n FROM mock "
        f"GROUP BY `{groupby}` ORDER BY n DESC"
    )
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        counts = cursor.fetchall()
        logger.info("Counted %d distinct values of %s", len(counts), groupby)
        return counts
    except mysql.connector.Error as err:
        logger.error("Database error in plot_counts: %s", err)
        return []
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


def main():
    group_counts = plot_counts("group")
    print("\nRows per group:")
    for value, n in group_counts:
        print(f"  {value}: {n}")

    print("\nRows per gender:")
    for value, n in plot_counts("gender"):
        print(f"  {value}: {n}")


    if group_counts:
        first_group = group_counts[0][0]
        rows = get_data_by_group(first_group)
        print(f"\nFirst 5 rows where group = {first_group!r}:")
        for row in rows[:5]:
            print(f"  {row}")


if __name__ == "__main__":
    main()