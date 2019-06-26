import inputs
import time
import datetime
import sqlite3
import threading

class TypingStats:

    def __init__(self):
        self._run = True
        self._last_save = datetime.datetime.now()
        self._count = 0
        self._thread_main = threading.Thread(target=self._main_loop)
        self._thread_main.start()
        self._thread_save = threading.Thread(target=self._save_loop)
        self._thread_save.start()

    def _main_loop(self):
        while self._run:
            events = inputs.get_key()
            for event in events:
                if event.ev_type == 'Key' and event.state:
                    self._count += 1
                    print(event.ev_type, event.code, event.state)

    def _save_loop(self):
        conn = sqlite3.connect('productivity.db')
        c = conn.cursor()
        c.execute('''create table if not exists Presses(time numeric, count integer)''')
        conn.commit()

        while self._run:
            time.sleep(1)
            current_time = datetime.datetime.now()
            elapsed = current_time - self._last_save
            if elapsed.total_seconds() >= 5:
                self._save(conn)

    def _save(self, conn):
        ts = time.time()
        c = conn.cursor()
        c.execute("insert into Presses values(CURRENT_TIMESTAMP," + str(self._count) + ")")
        self._last_save = datetime.datetime.now()
        self._count = 0
        conn.commit()

    def __del__(self):
        self._run = False
        self._conn.close()
        self._thread_main.join()
        self._thread_save.join()

ts = TypingStats()
