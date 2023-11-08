from ranking import ranking
from searcher import *
import re
from operator import itemgetter
from helper_funcs import helpers
from expresiones import expresiones
from date_finder import *
from word_finder_BSBI import word_finder_BSBI
import unicodedata
import sys



class Menu():

    def __init__(self):
        self.s = searcher()
    """creacion de la clase menu"""

    def __consultar_por_fechas_horas__(self):
        df = date_finder()
        print("Ingrese el usuario, la fecha de inicio y de find (dd/mm/YYYY HH:MM:SS) \
            Si no desea filtrar por usuario, presione enter")

        print("fecha de inicio de la busqueda: ")
        fecha_inicio = str(input())
        print("fecha final de busqueda: ")
        fecha_final =str(input())
        print("cantidad maxima de tweets que desea buscar: ")
        maximo = int(input())

        print("Ingrese el usuario que desea consultar: ")
        usuario = str(input())
        if usuario is None or usuario == "":
            resultado = df.filtrar_tweets_por_fecha( "tweet_shelve.s", "ids_ordenados.json", fecha_inicio, fecha_final, maximo)

        else:
           resultado = df.filtrar_tweets_por_fecha( "tweet_shelve.s", "ids_ordenados.json", fecha_inicio, fecha_final, maximo, usuario)
        



        # por ejemplo los m primeros tweets de un usuario dado en un rango de fechas y horas. Los m primeros
        # tweets de todos los usuarios en un rango de fechas y horas determinados
        # (donde m es un parámetro de la búsqueda)

    # def __mostrar_tweet(self, tweet):
    #     created_at = tweet["created_at"]
    #     username = tweet["username"]
    #     tweet_text = tweet["text"]
    #     texto_centrado = tweet_text.center(50, " ")

    #     print(f"Se encontro el Tweet con fecha {created_at} del usuario: *{username}*\n")
    #     #print(f"del usuario: *{username}*\n")
    #     print(f'El mismo contiene el siguiente texto:\n')
    #     lista_texto = tweet_text.split()
    #     corte = 15
    #     if (len(lista_texto) > corte) and (len(lista_texto) <= 30):
    #         variable = " ".join(lista_texto[0:corte])
    #         print(f"\t**{variable}")
    #         variable = " ".join(lista_texto[corte:len(lista_texto)])
    #         print(f"\t{variable}**")
    #     elif len(lista_texto) > 30:
    #         variable = " ".join(lista_texto[0:corte])
    #         print(f"\t**{variable}")
    #         variable = " ".join(lista_texto[corte:30])
    #         print(f"\t{variable}")
    #         variable = " ".join(lista_texto[30:len(lista_texto)])
    #         print(f"\t{variable}**")

    #     else:
    #         print(f"\t****{texto_centrado}****")


    def __consultar_palabras_o_frases__(self):
        # se debe permitir consultas booleanas (con los operadores and, not y or) de palabras o frases.
        # Estas consultas deben devolver los m primeros tweets correspondientes, donde m es un
        # parámetro de la búsqueda. Por ejemplo: (“Del Potro” and “Murray” and not “Copa Davis”, 10)
        # debería traer los 10 primeros tweets que mencionan a Del Potro y a Andy Murray y que no
        # mencionen a la Copa Davis.
        h = helpers()
        print("Coloque la palabra o frase a buscar, puede utilizar \"NOT\", \"OR\" y/o \"AND\" si es necesario. \
Si no coloca nada, se ejecutará una query default.")
        string_a_buscar = str(input())
        print("Ingrese la cantidad de tweets a filtrar. 0 (cero) para mostrar todos")
        cant_tweets = int(input())
        """ definimos un string default a buscar por si el user no pone nada """
        string_busqueda_default = "(work) OR (NOT elon AND NOT elonmusk AND free)"
        """ si el user no pone nada, instanciamos 'expresiones' con string_busqueda_default, sino, con string_a_buscar """
        exp = expresiones(string_busqueda_default if string_a_buscar == "" else string_a_buscar)
        print(f"Expresión de búsqueda: {exp.expresion_resuelta}")

        """ abrimos el shelve con los tweets recolectados """
        with shelve.open("tweet_shelve.s") as db_shelve:
            indice_invertido = word_finder_BSBI(db_shelve, "./salida")
            if cant_tweets is None or cant_tweets == 0:
                resultado = indice_invertido.buscar(exp.expresion_resuelta)
            else:
                resultado = indice_invertido.buscar(exp.expresion_resuelta, cant_tweets)

            if len(resultado)> 0:
                conta = 1
                for id in resultado:
                    print("======================================================================================================================================================")
                    print(f"RESULTADO N°: {conta}")
                    print("======================================================================================================================================================")
                    conta += 1
                    h.mostrar_tweet(db_shelve[id])


            print("\n======================================================================================================================================================")
            print(f"Se buscó en {len(db_shelve.items())} tweets y se obtuvieron {len(resultado)} resultados.")
            print("======================================================================================================================================================")

    def __ranking__(self):
                # Entregables opcionales
        # Módulo de estadísticas:
        # Ranking de las n palabras más mencionadas en tweets, o usuario de  Twitter.
        # Por ejemplo: las 10 palabras más frecuentes de todos los tweets recopilados.
        # Las 10 palabras más usadas por un usuario determinado de twitter.
        # Ranking de las n palabras más mencionadas en los tweets en forma global. Idem anterior
        with shelve.open("tweet_shelve.s") as db_shelve:

            #diccionario = helpers().recuperar_shelve("tweet_shelve.s")
            tweets = {}
            text_tweets_concatenados = ""
            caracteres = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))
            for tweet in db_shelve.items():
                tweet_text = tweet[1]["text"]
                text_tweets_concatenados +=  tweet_text + " " #tiene un espacio al final para que no se peguen palabras de inicio-fin
            text_tweets_concatenados = re.split(r'[\W]+', text_tweets_concatenados)
            texto_final = ""
            for palabra in text_tweets_concatenados:
                if len(palabra) > 3:
                    texto_final += palabra+" "
            dict_armado = ranking().armar_diccionario_palabras_contadas(texto_final)
            indice_ordenado = sorted(dict_armado.items(), key=itemgetter(1), reverse=True)
            self.mostrar_ranking(indice_ordenado, 100)

    def mostrar_ranking(self, ranking, limite): # ranking es una lista de tuplas (palabra, veces que aparece)
        puesto = 0
        print("\t============================= RANKING ==============================")
        for (palabra, veces_que_aparece) in ranking[:limite]:
            puesto += 1
            print(f"\tPuesto n° {puesto}:\t\tPalabra: \"{palabra}\"\t\t ->  Apariciones: {veces_que_aparece} veces")
        print("\t====================================================================")

    def __recopilar_tweets_desde_twitter(self):
        h = helpers() # objetito que tiene funciones helper

        # EXPLICACION DE LA QUERY
        # todo debe ir entre las comillas, el # significa buscar Hashtag
        # luego busca la palabra SpaceX en el tweet y por ultimo filtra que no sean retweets
        # los paramtros que tienen el - delante, significa que esas palabras las va a excluir
        # para que no se mezclen tweets de la nasa o astronautas en los que buscamos

        QUERY = '( Elon twitter) (lang:en) (-is:retweet)'
        EXPANSIONS = 'author_id,referenced_tweets.id,referenced_tweets.id.author_id,in_reply_to_user_id,attachments.media_keys,attachments.poll_ids,geo.place_id,entities.mentions.username'
        TWEET_FIELDS= 'author_id,conversation_id,created_at,entities,geo,id,lang,public_metrics,source,text'
        USER_FIELDS= 'created_at,description,entities,location,name,profile_image_url,public_metrics,url,username'

        r = self.s.stream_tweets(QUERY, EXPANSIONS, TWEET_FIELDS, USER_FIELDS)

        file_size = h.obtener_tamanio_de_archivo("tweet_shelve.s.dat")
        print(f"Tamaño archivo de datos de: {file_size} bytes\n")

    def __menu_diccionario__(self):
        while True:
            switcher = {'b': self.__consultar_por_fechas_horas__,'c': self.__consultar_palabras_o_frases__, 'd': self.__ranking__, 'a': self.__recopilar_tweets_desde_twitter, }

            print("Opciones: ")
            print("\t a: Recopilar tweets de Twitter")
            print("\t b: Consulta de tweets por fecha y hora")
            print("\t c: Consultas de tweets por palabras o frases")
            print("\t d: Ranking de las 100 palabras mas usadas")
            op = input("Ingrese la opción deseada: \n")
            switcher[op]()
            opcion = input("Desea continuar? ['s' para continuar, 'n' para salir] : ").lower()
            print(opcion)
            if opcion == "n":
                break
            elif opcion == 's':
                pass
            else:
                print("Seleccione una opcion válida")

if __name__ == '__main__':
    m = Menu()
    m.__menu_diccionario__()

