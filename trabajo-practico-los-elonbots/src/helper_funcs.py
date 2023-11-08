from datetime import datetime
import json
import os
import shelve

class helpers:
    ''' Clase que contiene funciones helpers (de ayuda) que estaban sueltas por ahi
    y es mejor tenerlas juntas y separadas para poder accederlas desde todo el codigo '''
    def __init__(self):
        pass

    def recuperar_json(self, json_filename):
        """ Abre un archivo json y devuelve su contenido en un Dict """
        with open(json_filename, "r") as arch_json:
            diccionario = json.load(arch_json)
            return diccionario

    def recuperar_shelve(self, shelve_filename):
        """ Abre un archivo shelve y devuelve su contenido en un Dict """
        diccionario = {}
        with shelve.open(shelve_filename) as db:
            """recorro el shelve y voy armando el dicc"""
            for (clave, valor) in db.items():
                diccionario[clave] = valor
            return diccionario

    def obtener_tamanio_de_archivo(self, archivo):
        return os.path.getsize(archivo)

    def generar_fechahora_actual(self):
        ''' Devuelve la fecha y hora actual formateada '''
        formatted_datetime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        return formatted_datetime
    
    def mostrar_tweet(self, tweet):
        created_at = tweet["created_at"]
        username = tweet["username"]
        tweet_text = tweet["text"]
        texto_centrado = tweet_text.center(50, " ")
        
        print(f"Se encontro el Tweet con fecha {created_at} del usuario: *{username}*\n")
        #print(f"del usuario: *{username}*\n")
        print(f'El mismo contiene el siguiente texto:\n')
        lista_texto = tweet_text.split()
        corte = 15
        if (len(lista_texto) > corte) and (len(lista_texto) <= 30):
            variable = " ".join(lista_texto[0:corte])
            print(f"\t**{variable}")
            variable = " ".join(lista_texto[corte:len(lista_texto)])
            print(f"\t{variable}**")
        elif len(lista_texto) > 30:
            variable = " ".join(lista_texto[0:corte])
            print(f"\t**{variable}")
            variable = " ".join(lista_texto[corte:30])
            print(f"\t{variable}")
            variable = " ".join(lista_texto[30:len(lista_texto)])
            print(f"\t{variable}**")
        
        else:
            print(f"\t****{texto_centrado}****")
            
