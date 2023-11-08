from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError, HydrateType, OAuthType
import json
import shelve
from helper_funcs import helpers
import csv
import os
import bisect

class searcher:

    def __init__(self):
        self.h = helpers()
        self.lista_ordenada_tweets = []

    def __guarda_cabecera(self, archivo, *campos):
        # Si el archivo no existe escribo en el encabezado
        # campos = id_tweet, usuario, fecha_hora
        try:
            os.path.getsize(archivo)
        except FileNotFoundError:
            with open(archivo, "w", newline="") as datos:
                writer = csv.DictWriter(datos, fieldnames=campos, delimiter=";")
                writer.writeheader()

    def __guardar_tweet(self, archivo,  **datos, ):
        campos = ["id_tweet", "usuario", "fecha_hora"]
        with open(archivo, "a", newline="") as archivo:
            writer = csv.DictWriter(archivo, fieldnames= campos, delimiter=";")
            writer.writerow(datos)    

    """ funcion que se encarga de persistir ids de tweets anteriores para acumularlos,\
    si no hay, genera una lista de ids desde cero"""
    def __generar_lista_ordenada_de_id_tweets(self):
        if not os.path.exists("ids_ordenados.json"):
            self.lista_ordenada_tweets = []
        else:
            with open("ids_ordenados.json", "r") as ids:
                ids_recuperados = json.load(ids)
                self.lista_ordenada_tweets = [id for id in ids_recuperados]

    def stream_tweets(self, query, expansions, tweet_fields, user_fields):
        ''' Funcion que stremea los tweets y devuelve un request '''
        ''' Generamos la fecha y hora de inicio '''
        fechahora_inicio = self.h.generar_fechahora_actual()
        ''' Variable para contar los bytes procesados '''
        tweet_data_length_in_bytes = 0
        '''Genero la cabecera del csv para la busqueda por fecha'''
        self.__guarda_cabecera( "tweets_csv.csv","id_tweet", "usuario", "fecha_hora")
        '''Lista ordenada de tweets'''
        self.__generar_lista_ordenada_de_id_tweets()
        '''Primero abro el shelve para guardar los datos'''
        with shelve.open("tweet_shelve.s") as db:
            try:
                o = TwitterOAuth.read_file("credentials.txt")
                api = TwitterAPI(o.consumer_key, o.consumer_secret, auth_type=OAuthType.OAUTH2, api_version='2')
                # DELETE EXISTING RULES
                r = api.request('tweets/search/stream/rules', method_override='GET')
                lista_ids = []
                for tweet in r:
                    id_tweet = tweet["id"]
                    lista_ids.append(str(id_tweet))
                r = api.request('tweets/search/stream/rules',  {"delete": {"ids": lista_ids}}  )
                # ADD STREAM RULES
                r = api.request('tweets/search/stream/rules', {'add': [{'value':query}]})
                if r.status_code != 201:
                    exit()
                # GET STREAM RULES
                r = api.request('tweets/search/stream/rules', method_override='GET')
                print(f'[{r.status_code}] RULES: {json.dumps(r.json(), indent=2)}\n')

                if r.status_code != 200:
                    exit()
                tweet_count = 0
                # START STREAM
                r = api.request('tweets/search/stream', {
                        'expansions': expansions,
                        'tweet.fields': tweet_fields,
                        'user.fields': user_fields,
                    },
                    hydrate_type=HydrateType.APPEND)
                print('================ Start... ================\n')
                print(f'[ HTTP Response status code: {r.status_code} ]')
                if r.status_code != 200:
                    exit()
                for tweet in r:
                    tweet_count += 1
                    '''guardamos el tweet en shelve con clave igual al id del tweet'''
                    data_tweet = tweet["data"]
                    id_tweet = data_tweet["id"]
                    username = data_tweet["author_id_hydrate"]["username"]
                    data_tweet["username"] = username
                    bisect.insort(self.lista_ordenada_tweets, id_tweet)
                    '''guardamos el csv para la busqueda por fecha'''
                    self.__guardar_tweet("tweets_csv.csv", id_tweet = id_tweet, usuario = username, fecha_hora = data_tweet["created_at"])
                    ''' por ahora usamos el tamaño que la data del tweet ocupa en memoria '''
                    tweet_data_length_in_bytes += data_tweet.__sizeof__()
                    db[f"{id_tweet}"] = data_tweet
                    print(f"Tweets procesados hasta el momento: {tweet_count}")

            except KeyboardInterrupt:
                ''' Generamos la fecha y hora de fin en el momento que se hace ctrl-c '''
                with open("ids_ordenados.json", "w") as contenedor:
                    json.dump(self.lista_ordenada_tweets, contenedor)

                fechahora_fin = self.h.generar_fechahora_actual()

                print('\n================ ... Done! ================\n')
                print(f"Fecha y hora de inicio: {fechahora_inicio}")
                print(f"Fecha y hora de finalizacion: {fechahora_fin}")
                print(f"Cantidad de tweets recolectados: {tweet_count} tweets")
                print(f"Cantidad de bytes procesados: {tweet_data_length_in_bytes} bytes")
                return r # TODO: ver para que hacemos este return

            except TwitterRequestError as e:
                print(f"\nTwitter returned: {e.status_code} (status code)")
                for msg in iter(e):
                    print(msg)

            except TwitterConnectionError as e:
                print(f"Exception: {e}")

            except Exception as e:
                print(f"Exception: {e}")
        