from helper_funcs import helpers
  


    #Arma diccionario que como clave tiene la palabra y como valor
    #la cantidad de veces que esa palabra aparece
class ranking:
    def armar_diccionario_palabras_contadas(self, texto):
        palabras = texto.split(" ") #separo todas las palabras por espacios
        palabras_to_apariciones = {}
        for palabra in palabras:
            if palabra not in palabras_to_apariciones:
                palabras_to_apariciones.setdefault(palabra, 1)
            else:
                palabras_to_apariciones[palabra] += 1
        return palabras_to_apariciones

    if __name__ == '__main__':

       
        diccionario = helpers().recuperar_shelve("tweet_shelve.s")
        tweets = {}
        textos = ""

        for (id_tweet, tweet) in diccionario.items():
            tweets[id_tweet] =  tweet["text"]
        
        for key, value in tweets.items():
            textos += value+" "
         
        

        dict_armado = armar_diccionario_palabras_contadas(textos) # aca tengo la falla 
        print(dict_armado)



    
    



