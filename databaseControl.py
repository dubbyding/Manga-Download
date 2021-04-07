import sqlite3
import os

class databaseControl():
    def __init__(self):
        self.path = "/home/rjmhrj/Documents/Manga"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        if not (os.path.isfile(os.path.join(dir_path,"manga.db"))):

            self.con = sqlite3.connect("manga.db")
            self.cur = self.con.cursor()
            self.cur.execute('''CREATE TABLE manga
                (
                    id integer not null primary key autoincrement,
                    name varchar(50),
                    link varchar(200)
                )
                ''')

            self.cur.execute('''
                CREATE TABLE chapter
                (
                    id integer not null primary key autoincrement,
                    name varchar(100),
                    link varchar(200),
                    manga_id integer references anime(id) on delete cascade
                )
            ''')
            self.cur.execute('''
                CREATE TABLE image
                (
                    id integer not null primary key autoincrement,
                    name varchar(100),
                    chapter_id integer references chapter(id) on delete cascade
                )
            ''')
            self.con.commit()
        else:

            self.con = sqlite3.connect("manga.db")
            self.cur = self.con.cursor()   
        

    def insertIntoAnime(self, name, links):
        """
            Inserts data to the table Anime.

            name => Name of an anime
            links => Links to that anime
        """
        id = self.getOneDetail("manga", "id", "name", name)
        if not id:
            self.cur.execute("INSERT INTO manga (name, link) values (?,?)" , [name, links])
            folder = os.path.join(self.path,name)
            if not os.path.isdir(folder):
                os.mkdir(folder)
            print("{} added to the database".format(name))
        else:
            print("{} already exists in the database".format(name))
    
    def insertIntoManga(self, name, link, manga_name):
        """
            Insert data to the Manga table

            name => Chapter Name
            link => link to that chapter
            manga_name => Anime name
        """
        id = self.getOneDetail("manga", "id", "name",manga_name)
        if not self.getOneDetail("chapter",  "id", "name", name):
            self.cur.execute("INSERT INTO chapter (name, link, manga_id) values (?,?,?)",[name, link, id])
            folder = os.path.join(os.path.join(self.path,manga_name), name)
            if not os.path.isdir(folder):
                os.mkdir(folder)
            print("{} added to the database".format(name))
        else:
            print("{} already exists in the database".format(name))

    def getLatestId(self, table_name) -> int:
        """
            Get the latest id in a table
            table_name => Name of the table
        """
        sql = "SELECT id from {} ORDER BY id DESC LIMIT 1".format(table_name)
        try:
            value = self.cur.execute(sql).fetchone()[0]
        except TypeError:
            return 1
        return value+1

    def getOneDetail(self, table, row, comparitor, name, one=True):
        """
            Get's one row details from table.
            table-> name of the table,
            row -> one row that is needed to be extracted.
            comparitor -> compare to select data
            name -> required data condition
        """
        sql = "SELECT {} FROM {} WHERE {} LIKE ?".format(row, table, comparitor)
        self.cur.execute(sql, ['%'+name+'%'])
        if one:
            try:
                return self.cur.fetchone()[0]
            except TypeError:
                return 0
        else:
            return self.cur.fetchall()

    def __del__(self):
        self.con.commit()
        self.con.close()