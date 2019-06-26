import sqlite3
 
def basic(start_time=None, end_time=None):
     conn = sqlite3.connect('productivity.db')
     c = conn.cursor()
     c.execute("SELECT * FROM Presses")
     rows = list(c.fetchall())
     print("max presses in 1 min:", max(rows, key=lambda x: x[1]))
     print("total presses: ", sum([row[1] for row in rows]))
     #for row in rows: print(row)
