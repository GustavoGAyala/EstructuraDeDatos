from nltk.stem import SnowballStemmer #Stemmer
from nltk.corpus import stopwords #Stopwords
from helper_funcs import helpers
import string

class word_finder:

    def __init__(self, tweets):
        ''' Recibe un diccionario con los documentos
        '''
        self.stop_words = frozenset(stopwords.words('english'))  # lista de stop words
        self._tweets = tweets
        self._english_stemmer = SnowballStemmer('english', ignore_stopwords=False)
        self._docID = tweets.keys()
        self.__generar_indice()
    
    def __lematizar_palabra(self, palabra):
        ''' Usa el stemmer para lematizar o recortar la palabra, previamente elimina todos
        los signos de puntuación que pueden aparecer. El stemmer utilizado también se
        encarga de eliminar acentos y pasar todo a minúscula, sino habría que hacerlo
        a mano'''
        
        palabra = palabra.strip(string.punctuation + "»" + "\x97" + "¿" + "¡")
        # "\x97" representa un guión
        
        palabra_lematizada = self._english_stemmer.stem(palabra)
        return palabra_lematizada
        
    def __generar_indice(self):
        ''' Genera los pares la lista de pares (palabra, docID)
        ''' 
        pares = []
        indice={}
        for tweet in self._tweets:
            lista_palabras = [palabra for palabra in self._tweets[tweet].split() if not palabra in self.stop_words]
            lista_palabras = [self.__lematizar_palabra(palabra) for palabra in lista_palabras]
            #print(lista_palabras)
            pares= pares + [(palabra, tweet) for palabra in lista_palabras]
            #print(pares)
        
        for par in pares:
            posting = indice.setdefault(par[0],set())
            posting.add(par[1])
            
        self._indice = indice

    def buscar(self, palabra):
        salida=[]
        palabra_lematizada = self.__lematizar_palabra(palabra)
        if palabra_lematizada in self._indice:
            #print(palabra_lematizada)
            for tweet in self._indice[palabra_lematizada]:
                #print (tweet)
                salida.append(tweet)
        return set(salida)

    
if __name__ == "__main__":
    h = helpers()
    diccionario = h.recuperar_shelve("tweet_shelve.s")
    tweets = {}

    for (id_tweet, tweet) in diccionario.items():
        tweets[id_tweet] =  tweet["text"]
       
    ii = word_finder(tweets)
    resultado = ii.buscar("internet")
    for id in resultado:
        print (id,tweets[id])    
