from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from databaseControl import databaseControl


class mangaDownload():
    def __init__(self, name_of_manga):
        self.name_of_manga = name_of_manga
        self.driver = webdriver.Firefox()
        self.driver.minimize_window()

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
        wait = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME,'story_item')), 'Time Out')
        getAllClass = self.driver.find_elements_by_css_selector("div.story_item a")
        self.classList = []
        for classes in getAllClass:
            a=classes.get_attribute("href")
            if a not in self.classList and "chapter" not in a:
                self.classList.append(a)
    
    def go_to_saved_link(self):
        for links in self.classList:
            self.driver.get(links)
            anime_name = self.driver.find_element_by_css_selector("div.story-info-right h1").text
            insert_anime = databaseControl()
            insert_anime.insertIntoAnime(anime_name)
            del insert_anime
            getAllClass = self.driver.find_elements_by_css_selector("li.a-h a")
            self.manga_name = []
            self.manga_link = []
            for classes in getAllClass:
                insertManga = databaseControl()
                title = classes.get_attribute("title")
                link = classes.get_attribute("href")
                insertManga.insertIntoManga(title, link, anime_name)
                del insertManga
                self.manga_link.append(link)
                self.manga_name.append(title)
    
    

    def __del__(self):
        self.driver.close()

if __name__ =="__main__":

    manga = mangaDownload("Attack On Titan")
    manga.go_to_mangakakalot()
    status = manga.search_anime()
    if(status[1]):
        manga.all_searched_result()
        manga.go_to_saved_link()
    else:
        print("Already in database! Do check")
    
