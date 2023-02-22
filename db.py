import sqlite3

def db(fn):
    def _wrapper():
        conn = sqlite3.connect('the_trade_system.db')
        try:
            fn(conn)
            conn.commit()
        except Exception as error:
            # roll back any change if something goes wrong
            conn.rollback()
            print(error)
        finally:
            conn.close()
    return _wrapper

@db
def setup(conn):
    c = conn.cursor()

    with open('CLASSROOM - Trading Platform schema - mySQL.sql', encoding='Latin-1') as file:
        content_file = file.read()
        content_file = content_file\
            .replace("\n", "")\
            .replace("ADDTIME", "DATETIME")\
            .replace("DATE_ADD", "DATETIME")\
            .replace("NOW()", "\'now\'")\
            .replace("INTERVAL ", "")\
            .replace("CURDATE()", "DATE()")\
            .replace(", 0 DAY", "")\
            .replace("-", "\'-")\
            .replace("DAY", "DAY\'")\
            .replace(", \"", ", \"+")\
            .replace(":00", " HOUR")\
            .replace('SET SQL_SAFE_UPDATES = 0', '')\
            .strip().split(";")

    # proceed file execution
    for exe in content_file:
        try:
            c.execute(exe + ";")
        except:
            print(f"fail to execute {exe}")
