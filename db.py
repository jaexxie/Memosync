import pymysql

def make_db_connection():
    '''
    This Function Makes The Connection With The Database
    '''
    db = pymysql.connect(
        host="memosync-database1.c784gssighqq.eu-north-1.rds.amazonaws.com",
        user="admin",
        passwd="025536As",
        database="memosync",
    )
    return db

