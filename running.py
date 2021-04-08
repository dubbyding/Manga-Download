from manga import mangaDownload

if __name__ =="__main__":

    manga = mangaDownload("Attack on Titan")
    manga.go_to_mangakakalot()
    status = manga.search_anime()
    if(status[1]):
        manga.all_searched_result()
        manga.go_to_saved_link()
    else:
        print("Already in database! Do check")
        print("Do you want to check for other similar manga and/or check for updates?(y/n)")
        question = input()
        if question.lower()=="y":
            manga.search_anime(force_search=True)
            manga.all_searched_result()
            manga.go_to_saved_link()
    manga.getChapterLink()
    manga.go_to_chapter_link()