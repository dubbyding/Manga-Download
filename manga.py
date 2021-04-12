from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import os
from databaseControl import databaseControl
from platform import system

class noValueError(Exception):
    pass

class mangaDownload():
    def __init__(self, name_of_manga='', headless_status=True, updating_status=False):
        options = Options()
        if headless_status:
            options.headless = True
        self.name_of_manga = name_of_manga
        self.update_status = updating_status
        # print(self.update_status)
        # print(headless_status)
        geckodriver = "geckodriver/geckodriver"
        if system() =="Windows":
            geckodriver = geckodriver + ".exe"
        self.driver = webdriver.Firefox(options=options, executable_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), geckodriver))
        self.driver.minimize_window()
        self.manga_list_all = []

    def go_to_mangakakalot(self):
        try:
            self.driver.get("https://mangakakalot.com")
            return "loaded",1
        except Exception:
            return "notLoaded", 0

    def search_anime(self, manga_name="", force_search=False):
        if manga_name == "":
            manga_name = self.name_of_manga
        elif not manga_name == self.name_of_manga:
            self.name_of_manga = manga_name
            print("Manga to be searched changed to:- {}".format(manga_name))
        if self.name_of_manga == '':
            raise noValueError
        checkSearchedManga = databaseControl()
        if not checkSearchedManga.getOneDetail("manga", "id", "name", manga_name, one=False) or force_search:
            searching_manga = self.driver.find_element_by_id("search_story")
            del checkSearchedManga
            searching_manga.clear()
            searching_manga.send_keys(manga_name, Keys.RETURN)
            return "loaded", 1
        else:
            del checkSearchedManga
            return "Already in the database", 0

    def all_searched_result(self):
        # self.getAllClass = driver.find_elements_by_xpath('//*[contains(@class,"daily-update")]')
        # getAllLinks = self.getAllClass
        a = True
        while(a):
            try:
                wait = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME,'story_item')), 'Time Out')
                a=False
            except:
                pass

        getAllClass = self.driver.find_elements_by_css_selector("div.story_item a")
        self.classList = []
        for classes in getAllClass:
            a=classes.get_attribute("href")
            if a not in self.classList and "chapter" not in a:
                self.classList.append(a)
    
    def go_to_saved_link(self):
        for links in self.classList:
            self.driver.get(links)
            try:
                anime_name = self.driver.find_element_by_css_selector("div.story-info-right h1").text
            except Exception:
                anime_name = self.driver.find_element_by_css_selector("ul.manga-info-text li h1").text
                # input()
            
            self.manga_list_all.append(anime_name)
            check = 'n'
            if not self.update_status:
                print("Do you want to download {} anime?(y/n/q)(Yes/No/Quit)".format(anime_name))
                check = input()
            else:
                if anime_name == self.name_of_manga:
                    check = 'y'
            if check.lower() == "y" or check.lower() == "yes":
                insert_anime = databaseControl()
                insert_anime.insertIntoAnime(anime_name, links)
                del insert_anime
                getAllClass = self.driver.find_elements_by_css_selector("li.a-h a")
                self.manga_name = []
                self.manga_link = []
                for classes in getAllClass:
                    insertManga = databaseControl()
                    title = classes.get_attribute("innerHTML")
                    link = classes.get_attribute("href")
                    insertManga.insertIntoManga(title, link, anime_name)
                    del insertManga
                    self.manga_link.append(link)
                    self.manga_name.append(title)
                if len(self.manga_name) == 0:
                    getAllClass = self.driver.find_elements_by_css_selector("div.row span a")
                    self.manga_name = []
                    self.manga_link = []
                    for classes in getAllClass:
                        insertManga = databaseControl()
                        title = classes.get_attribute("innerHTML")
                        link = classes.get_attribute("href")
                        insertManga.insertIntoManga(title, link, anime_name)
                        del insertManga
                        self.manga_link.append(link)
                        self.manga_name.append(title)
            elif check.lower() == "q" or check.lower()=="quit":
                break
            else:
                continue
            
    
    def getChapterLink(self):
        getLinks = databaseControl()
        anime_list = getLinks.get_more_details('name', 'manga')
        names=[]
        for i in anime_list:
            names.append(i[0])
        for name in self.manga_list_all:
            if name in names:
                self.result = getLinks.getDetailJoin("chapter", "manga", ["name", "link"], "manga_id", "id", name, one=False)
                # print(self.result)
                self.name_manga = getLinks.getDetailJoin("manga", "chapter", ["name"], "id", "manga_id",name)
        # print(self.name_manga)
        del getLinks
    
    def go_to_chapter_link(self):
        for chapter_name, chapter_link in self.result:
            current_folder = os.path.dirname(os.path.abspath(__name__))
            chap_name = chapter_name.translate({ord(c):" " for c in '!@#$%^&*()[]{};:,./<>?\|`~-=_+"\''}).replace(" ", "-")+".png"
            mangaName = self.name_manga.translate({ord(c):" " for c in '!@#$%^&*()[]{};:,./<>?\|`~-=_+"\''}).replace(" ", "-")
            path = os.path.join(os.path.join(os.path.join(current_folder,"Manga"), mangaName),chap_name).replace('\\',"/")
            if os.path.isfile(path):
                print("{} manga's {} chapter already exists".format(mangaName, chap_name))
                continue
            self.driver.get(chapter_link)
            try:
                image_container = self.driver.find_element_by_css_selector("div.container-chapter-reader")# print(path)
                screenshot = image_container.screenshot_as_png
                with open(path, 'wb') as f:
                    f.write(screenshot)
                print("{} is saved".format(chap_name))
            except Exception as e:
                path = path.split('.')[:-1:][0]+'Error.txt'
                error_container = self.driver.find_element_by_css_selector("div.panel-not-found")
                with open(path, 'w') as f:
                    f.write('{} has occured'.format(error_container.find_element_by_css_selector('p').get_attribute("innerHTML")))
                print('{} has occured'.format(error_container.find_element_by_css_selector('p').get_attribute("innerHTML")))
            
    
    def get_anime_name(self):
        anime_list = databaseControl()
        self.anime_list = anime_list.get_more_details('name', 'manga')
        return [i[0] for i in self.anime_list]

    def __del__(self):
        self.driver.close()

if __name__=='__main__':
    trying = mangaDownload('attack on titan')
    value = trying.get_anime_name()
    for i in value:
        print(i[0])
    
