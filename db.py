from operator import truediv
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

def does_the_token_match_the_users_token(token, id):
    try:
        # database connection
        db = make_db_connection()
        cursor = db.cursor()

        cursor.execute('select * from user_info where token = %s and id = %s', (token, id))
        user = cursor.fetchone()

        if user:
            return True
        else:
            return False
        
    finally:
            # close database connection
            cursor.close()
            db.close()
