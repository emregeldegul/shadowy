import pymysql.cursors

db = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    db = 'shadowy',
    charset = 'utf8mb4',
    cursorclass = pymysql.cursors.DictCursor
)

coursor = db.cursor()
