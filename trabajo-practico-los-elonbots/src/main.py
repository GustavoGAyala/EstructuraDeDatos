import searcher
from menu import Menu
from helper_funcs import helpers
from searcher import *
from expresiones import *



if __name__ == '__main__':

    menu = Menu()
    menu.__menu_diccionario__()
    # h = helpers() # objetito que tiene funciones helper
    # s = searcher()
    # #QUERY = '(#SpaceX OR SpaceX OR @SpaceX) -NASA -ASTRONAUTS (-is:retweet)'  
    # QUERY = '( Elon twitter) (lang:en) (-is:retweet)'      
    # EXPANSIONS = 'author_id,referenced_tweets.id,referenced_tweets.id.author_id,in_reply_to_user_id,attachments.media_keys,attachments.poll_ids,geo.place_id,entities.mentions.username'
    # TWEET_FIELDS= 'author_id,conversation_id,created_at,entities,geo,id,lang,public_metrics,source,text'      
    # USER_FIELDS= 'created_at,description,entities,location,name,profile_image_url,public_metrics,url,username'

    # r = s.stream_tweets(QUERY, EXPANSIONS, TWEET_FIELDS, USER_FIELDS)
    # file_size = h.obtener_tamanio_de_archivo("tweet_shelve.s.dat")
    # print(f"Tamaño archivo de datos de: {file_size} bytes\n")


    
    