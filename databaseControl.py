import sqlite3
import os

class databaseControl():
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        if not (os.path.isfile(os.path.join(dir_path,"manga.db"))):

            self.con = sqlite3.connect("manga.db")
            self.cur = self.con.cursor()
            self.cur.execute('''CREATE TABLE manga
                (id integer not null primary key autoincrement,
                name varchar(50))''')

            self.cur.execute('''
                CREATE TABLE chapter
                (id integer not null primary key autoincrement,
                name varchar(100),
                link varchar(200),
                manga_id integer references anime(id) on update cascade
                )
            ''')
            self.con.commit()
        else:

            self.con = sqlite3.connect("manga.db")
            self.cur = self.con.cursor()   
        

    def insertIntoAnime(self, name):
        id = self.check_id("manga", name)
        print(id)
        if not id:
            self.cur.execute("INSERT INTO manga (name) values (?)" , [name])
            print("{} added to the database".format(name))
        else:
            print("{} already exists in the database".format(name))
    
    def insertIntoManga(self, name, link, manga_name):
        id = self.check_id("manga", manga_name)
        if not self.check_id("chapter", name):
            self.cur.execute("INSERT INTO chapter (name, link, manga_id) values (?,?,?)",[name, link, id])
            print("{} added to the database".format(name))
        else:
            print("{} already exists in the database".format(name))

    def getLatestId(self, table_name) -> int:
        sql = "SELECT id from {} ORDER BY id DESC LIMIT 1".format(table_name)
        try:
            value = self.cur.execute(sql).fetchone()[0]
        except TypeError:
            return 1
        return value+1

    def check_id(self, table, name, one=True):
        try:
            sql = "SELECT id FROM {} WHERE name LIKE ?".format(table)
            self.cur.execute(sql, ('%'+name+'%',))
            if one:
                try:
                    return self.cur.fetchone()[0]
                except TypeError:
                    return 0
            else:
                return self.cur.fetchall()
    
        except Exception as e:
            print(e)
            return 0
    def __del__(self):
        self.con.commit()
        self.con.close()