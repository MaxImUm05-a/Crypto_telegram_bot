import sqlite3

class bd():
    db = sqlite3.connect('venv/server.db', check_same_thread=False)
    sql = db.cursor()

    def __init__(self):
        self.sql.execute("""CREATE TABLE IF NOT EXISTS users (
            nickname TEXT,
            password TEXT,
            crypto TEXT,
            user_id TEXT,
            vhid INT
        )""")
        self.db.commit()

    def add_to_table(self, add):
        values = []
        for value in self.sql.execute('SELECT * FROM users'):
            values.append(value)
        iters = len(values)
        for x in range(0, iters):
            if add[3] == int(values[x][3]) and values[x][4] == 1:
                return 0
            elif add[3] == int(values[x][3]) and values[x][4] == 0:
                ch = list(values[x])
                nick = ch[0]
                ch[3] = 0
                self.change_acc(ch, nick)             #те що user_id стає 0 це так треба
        self.sql.execute(f"INSERT INTO users VALUES('{add[0]}', '{add[1]}', '{add[2]}', '{add[3]}', {1})")
        self.db.commit()
        return 1

    def info_about_user(self, id):
        values = []
        id = str(id)
        p = False
        for value in self.sql.execute('SELECT * FROM users'):
            values.append(value)
        iter = 0
        iters = len(values)
        while iter < iters:
            if id == values[iter][3]:
                info = values[iter]
                info = list(info)
                p = True
            iter = iter + 1
        if p == True:
            return info
        else:
            return [None]

    def info_about_user_by_nickname(self, nick):
        values = []
        p = False
        for value in self.sql.execute('SELECT * FROM users'):
            values.append(value)
        iter = 0
        iters = len(values)
        while iter < iters:
            if nick == values[iter][0]:
                info = values[iter]
                p = True
            iter = iter + 1
        if p == True:
            return info
        else:
            return [None]

    def vhid_in_acc(self, v, id):
        pp = self.info_about_user(id)
        p = pp[-1]
        n = pp[0]
        if v == 1:
            if p == 1:
                return 0
            else:
                return -1
        else:
            if p == 1:
                self.sql.execute(f'UPDATE users SET vhid = {0} WHERE nickname = "{n}"')
                self.db.commit()
                return 1
            else:
                return 0

    def change_acc(self, change, nick, f = 0):
        if f == 0:
            self.sql.execute(
                f'UPDATE users SET password = "{change[1]}", user_id = "{change[3]}", crypto = "{change[2]}"\
                         WHERE nickname = "{nick}"'
            )
            self.db.commit()
        elif f == 1:
            self.sql.execute(
                f'UPDATE users SET nickname = "{change[0]}", password = "{change[1]}", user_id = "{change[3]}", crypto = "{change[2]}"\
                         WHERE user_id = "{nick}"'
            )
            self.db.commit()
        elif f == 2:
            self.sql.execute(f'UPDATE users SET vhid = {1}, user_id = "{change[2]}" WHERE nickname = "{nick}"')
            self.db.commit()

    def perevirka(self, info):
        id = info[2]
        nick = info[0]
        password = info[1]
        info = self.info_about_user_by_nickname(nick)
        if info[-1] == None:
            return None
        elif info[1] == password:
            return True
        else:
            return False