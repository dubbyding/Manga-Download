from manga import mangaDownload
import time

def new_anime(anime_name, debugging_mode, updating_status):
    # print(updating_status)
    # print(debugging_mode)
    manga = mangaDownload(name_of_manga=anime_name.title(), headless_status=not(debugging_mode), updating_status=updating_status)
    manga.go_to_mangakakalot()
    if updating_status:
        manga.search_anime(force_search=True)
        manga.all_searched_result()
        manga.go_to_saved_link()
        manga.getChapterLink()
        manga.go_to_chapter_link()
    else:
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
    del manga

def update_anime(debugging_status):
    updating = mangaDownload(headless_status=True)
    anime_list = updating.get_anime_name()
    del updating
    index = [i+1 for i in range(len(anime_list))]
    anime_dict = {index[i]: anime_list[i] for i in range(len(anime_list))}
    # print(anime_dict)
    print('Choose Anime to update!(For all type "a")')
    for i, anime in enumerate(anime_list):
        print('{}. {}'.format(index[i], anime_list[i]))
    choosing_status = True
    while choosing_status:
        choosing_anime = input()
        if choosing_anime=='':
            print('Not selected any anime. Try again:- ')
        else:
            choosing_status = False
    if ' ' in choosing_anime:
        number_list = [int(i) for i in choosing_anime.split(' ')]
    elif choosing_anime == 'a':
        number_list = index
    else:
        number_list = [int(choosing_anime)]
    anime_to_update = [anime_dict[i] for i in number_list]
    for anime_names in anime_to_update:
        new_anime(anime_names, debugging_status, True)
    

if __name__ =="__main__":
    print('Do you want to run in debugging mode?(It opens in browser)')
    debugging_status = input()    
    
    try:
        if debugging_status.lower() == 'n' or debugging_status.lower() =='no' or debugging_status.lower() == 'false' or debugging_status.lower()=='f':
            debugging_status=False
        else:
            debugging_status = True
    except AttributeError:
        pass
    Again = True
    while(Again):
        print('Do you want to download new manga or update existing manga?(1=> New manga, 0 => Update)')
        choosing = input()
        if choosing == '1':
            print('Enter Anime that needed to be downloaded:-')
            anime_name = input()
            start_time = time.time()
            new_anime(anime_name, debugging_status, False)
            print('Total Time taken;')
            print("--- %s seconds ---" % (time.time() - start_time))
        else:
            update_anime(debugging_status)
            
        print("Do you want to continue again?(Yes/No)")
        Again = input()
        if Again.lower() == 'yes' or Again.lower() == 'y' or Again.lower() =='true' or Again.lower() == 't':
            Again = True
        else:
            Again = False