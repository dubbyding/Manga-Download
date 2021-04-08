from manga import mangaDownload
import time

def new_anime(anime_name):
    manga = mangaDownload(anime_name.title())
    manga.go_to_mangakakalot()
    status = manga.search_anime()
    if(status[1]):
        manga.all_searched_result()
        manga.go_to_saved_link()
        
        manga.getChapterLink()
        manga.go_to_chapter_link()
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
    print('All Operations Completed!!')

if __name__ =="__main__":
    print('Enter Anime that needed to be downloaded:-')
    anime_name = input()
    start_time = time.time()
    new_anime(anime_name)
    print('Total Time taken;')
    print("--- %s seconds ---" % (time.time() - start_time))