
# One function, set_up(), that opens a connection to the SQLite database.
# Used by every other file in this folder.
def set_up():
    try:
        from .db_config import FULL_PATH_DB
    except:
        from db_config import FULL_PATH_DB
    import sqlite3
    connection = sqlite3.connect(FULL_PATH_DB)
    cursor = connection.cursor()
    return connection, cursor


