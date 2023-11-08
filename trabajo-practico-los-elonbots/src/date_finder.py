from dateutil import parser
import shelve
import csv
import json
from datetime import datetime, timezone, tzinfo

from helper_funcs import helpers


class date_finder:
    ''' Clase que modela un buscador de tweets por rango de fecha '''
    def __init__(self):
        pass

    def filtrar_tweets_por_fecha(self, archivo_shelve, archivo_ids, fecha_ini, fecha_fin, cant_tweets_solicitados, usuario = None ):
        h = helpers()
        ''' Función que recibe un archivo shelve y un csv, y 
        mediante pedirle al usuario que ingrese un rango de fechas para filtrar tweets,
        los agrega a una lista (por ahora) y la devuelve '''
        tweets_filtrados_por_fecha = [] # acá metemos los tweets filtrados
        cant_tweets = 0

        #abrimos el shelve que tiene la informacion completa de los tweets
        with shelve.open(archivo_shelve) as db_shelve: 
            #abrimos el archivo de ids para recorrer los tweets en orden de ingresado 
            with open(archivo_ids, "r") as id_tweets:
                lista_id_tweet = json.load(id_tweets)      
                i = 0    
                for i in range(0,len(lista_id_tweet)):
                    id_tweet = lista_id_tweet[i]
                    tweet_created = str(db_shelve[id_tweet]["created_at"])   
                    tweet_created_datetime = parser.parse(tweet_created)
                    tweet_created_datetime = tweet_created_datetime.replace(tzinfo = None) 
                    #tweet_created_datetime = parser.parse(tweet_created)
                    usuario_tweet= db_shelve[id_tweet]["username"]

                    # Tomamos la fecha de inicio para definir el rango del filtro 
                    # parseamos la fecha por si viene mal formateada
                    fecha_start = self.parsear_datetime(str(fecha_ini))

                    # Tomamos la fecha de fin para cerrar el rango del filtro
                    # parseamos la fecha por si viene mal formateada
                    fecha_end = self.parsear_datetime(str(fecha_fin)) 
                    
                    if usuario is None:
                        if tweet_created_datetime >= fecha_start and tweet_created_datetime <= fecha_end:
                            tweets_filtrados_por_fecha.append(id_tweet)
                            cant_tweets += 1
                    else:  
                        if tweet_created_datetime >= fecha_start and tweet_created_datetime <= fecha_end\
                            and usuario == usuario_tweet :
                            tweets_filtrados_por_fecha.append(id_tweet)   
                            cant_tweets += 1   

                    if cant_tweets == cant_tweets_solicitados:
                        
                        if len(tweets_filtrados_por_fecha)> 0:    
                            print("======================================================================================================================================================")
                            print(f"============================================================ Tweets filtrados por fecha ==============================================================")
                            print("======================================================================================================================================================")
                            print(f"\t\t Fecha inicio: {fecha_start} | Fecha fin: {fecha_end}")
                            print("======================================================================================================================================================")
                            conta = 1
                            for id in tweets_filtrados_por_fecha:
                                print("======================================================================================================================================================")
                                print(f"RESULTADO N°: {conta}")
                                print("======================================================================================================================================================")
                                conta += 1
                                h.mostrar_tweet(db_shelve[id])

                        return tweets_filtrados_por_fecha

            if len(tweets_filtrados_por_fecha)> 0:
                conta = 1    
                for id in tweets_filtrados_por_fecha:
                    print("======================================================================================================================================================")
                    print(f"RESULTADO N°: {conta}")
                    print("======================================================================================================================================================")
                    conta += 1
                    h.mostrar_tweet(db_shelve[id])
                    
        return tweets_filtrados_por_fecha

    def parsear_datetime(self, fecha):
        ''' funcion que recibe un datetime y lo parsea para que tenga el formato correcto '''
        parsed_datetime = datetime.strptime(fecha, '%d/%m/%Y %H:%M:%S')
        #parsed_datetime = parser.parse(fecha)
        return parsed_datetime

if __name__ == '__main__':
      
    df = date_finder()      
    
    #2022-11-01T01:56:23.000Z
    #2022-11-01T01:57:43.000Z
    fecha_end = "01/11/2022 01:56:00"
    fecha_ini = "01/11/2022 00:59:00"

    #dt_str = '27/10/2022 05:23:20' #dt_obj = datetime.strptime(dt_str, '%d/%m/%y %H:%M:%S')

    cant_tweets_solicitados = 10
    resultado = df.filtrar_tweets_por_fecha( "tweet_shelve.s", "ids_ordenados.json", fecha_ini, fecha_end, cant_tweets_solicitados, "KaraCalCurt")
    #resultado = df.filtrar_tweets_por_fecha( "tweet_shelve.s", "ids_ordenados.json", fecha_ini, fecha_end, cant_tweets_solicitados)
    
            