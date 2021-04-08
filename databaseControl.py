import sqlite3
import os
import platform

class databaseControl():
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        if platform.system()=="Windows":
            self.path = os.path.join(dir_path, "Manga")
        else:
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
            folder = os.path.join(self.path,name.translate({ord(c):" " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})).replace(" ","-")
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
            if "Chapter" in name:
                name = name[name.find("Chapter"):]
            self.cur.execute("INSERT INTO chapter (name, link, manga_id) values (?,?,?)",[name, link, id])
            # folder = os.path.join(os.path.join(self.path,manga_name), name.translate({ord(c):" " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})).replace(" ","-")
            # if not os.path.isdir(folder):
            #     os.mkdir(folder)
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
    
    def getDetailJoin(self, table1, table2, row_to_display, row1, row2, one=True):
        
        select = ""
        for index, row in enumerate(row_to_display):
            select = select + table1 + "." + row
            if not index == len(row_to_display) - 1:
                select = select + ", "
        sql = "SELECT {} FROM {} INNER JOIN {} ON {}.{}={}.{}".format(select, table1, table2, table1, row1, table2, row2)
        self.cur.execute(sql)
        if one:
            return self.cur.fetchall()
        else:
            return self.cur.fetchone()[0]

    def __del__(self):
        self.con.commit()
        self.con.close()