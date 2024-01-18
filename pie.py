import sqlite3
con = sqlite3.connect("history_of_text.db") # подключене к бд
with con:
    cur = con.cursor() # создание курсора
    cur.execute('''CREATE TABLE history(
id INTEGER PRIMARY KEY AUTOINCREMENT ,
user_id INTEGER,
datime DATETIME, 
text TEXT,
user_name INTEGER)''') 
    # взаимодействие с бд
    con.commit() # сохранение результата
    cur.close() # закрытие курсора
