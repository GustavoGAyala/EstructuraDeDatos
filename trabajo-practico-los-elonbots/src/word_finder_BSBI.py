from pickle import TRUE
import shelve
from nltk.stem import SnowballStemmer #Stemmer
from nltk.corpus import stopwords #Stopwords
from helper_funcs import helpers
from expresiones import *
import json
import os
import string
import time

class word_finder_BSBI:
    def __init__(self, db_tweets, salida, temp="./temp", blocksize=102400, language='english'):
        ''' tweets: achivo shelve con tweets a indexar
            salida: carpeta donde se guardará el índice invertido'''
        self._db_tweets = db_tweets #tweets es lo que era documentos
        self.salida = salida
        self._blocksize = blocksize
        self._temp = temp
        self._stop_words = frozenset(stopwords.words(language))  # lista de stop words
        self._stemmer = SnowballStemmer(language, ignore_stopwords=False)
        self._term_to_termID = {}
    
        self._generar_docID()
        self.__indexar()
    
    def _generar_docID(self):
        doc_to_docID = {}
        docID_to_doc = {}
        i = 0

        lista_de_tweet_ids = []
        for id_tw in self._db_tweets:
            doc_to_docID[id_tw] = i
            docID_to_doc[i] = id_tw

            lista_de_tweet_ids.append(id_tw)
            i += 1

        self._lista_de_tweet_ids = lista_de_tweet_ids
        self._doc_to_docID = doc_to_docID
        self._docID_to_doc = docID_to_doc
    
    ''' Funcion privada que usa el stemmer para lematizar o recortar la palabra, previamente elimina todos
        los signos de puntuación que pueden aparecer. El stemmer utilizado también se
        encarga de eliminar acentos y pasar todo a minúscula, sino habría que hacerlo
        a mano'''
    def __lematizar(self, palabra):
        palabra = palabra.strip(string.punctuation + "»" + "\x97" + "¿" + "¡" + "\u201c" +\
                               "\u201d" + "\u2014" + "\u2014l" + "\u00bf")
        # "\x97" representa un guión
        
        palabra_lematizada = self._stemmer.stem(palabra)
        return palabra_lematizada
    
    def __indexar(self):
        n = 0
        lista_bloques = []
        for bloque in self.__parse_next_block():
            bloque_invertido = self.__invertir_bloque(bloque)
            lista_bloques.append(self.__guardar_bloque_intermedio(bloque_invertido, n))
            n += 1
        start = time.process_time()
        self.__intercalar_bloques(lista_bloques)
        
        end = time.process_time()
        print("Intercalar Bloques Elapsed time: ", end-start)
        
        self.__guardar_diccionario_terminos()
        self.__guardar_diccionario_documentos()
   
    def __invertir_bloque(self, bloque):
        bloque_invertido={}
        bloque_ordenado = sorted(bloque,key = lambda tupla: (tupla[0], tupla[1]))
        for par in bloque_ordenado:
            posting = bloque_invertido.setdefault(par[0],set())
            posting.add(par[1]) 
        return bloque_invertido
    
    def __guardar_bloque_intermedio(self, bloque, nro_bloque):
        archivo_salida = "b"+str(nro_bloque)+".json"
        archivo_salida = os.path.join(self._temp, archivo_salida)
        for clave in bloque:
            bloque[clave]=list(bloque[clave])
        with open(archivo_salida, "w") as contenedor:
            json.dump(bloque, contenedor)
        return archivo_salida
    
    def __intercalar_bloques(self, temp_files):
        
        lista_termID=[str(i) for i in range(len(self._term_to_termID))]
        posting_file = os.path.join(self.salida,"postings.json")
        
        open_files = [open(f, "r") for f in temp_files]
        dicc ={}
        dicc_de_data = {}
        
        with open(posting_file,"w") as salida:
            lista_term_rango = []
            i = 0
            inicio = 0    
            rango = 1000
            if rango > len(lista_termID):
                fin = len(lista_termID)
            else:        
                fin = rango   
            final = False
            while fin <= len(lista_termID) and not(final):
                lista_term_rango = lista_termID[inicio:fin] 
                #print(lista_term_rango)
                for data in open_files:
                    try:
                        data.seek(0)
                        bloque = json.load(data)
                        for termID in lista_term_rango:
                            posting=set()
                            posting = set(bloque[termID])
                            if termID not in dicc:
                                dicc[termID] = list(posting)
                            else:    
                                dicc[termID] = list( posting.union(set(dicc[termID]))  )
                    except:
                        pass 
                if fin == len(lista_termID):
                    final = True

                if fin + rango > len(lista_termID):
                    inicio = fin
                    fin = len(lista_termID)
                else:
                    inicio = fin
                    fin = fin + rango
                    
                
                #@GUS aca habia un json por linea. Fijate que ahora se guarda en un dicc
                # y al final se manda todo el dicc al json    
                
            json.dump(dicc, salida)
            
    def __guardar_diccionario_terminos(self):
        path = os.path.join(self.salida, "diccionario_terminos.json")
        with open(path, "w") as contenedor:
            json.dump(self._term_to_termID, contenedor)
    
    def __guardar_diccionario_documentos(self):
        path = os.path.join(self.salida, "diccionario_documentos.json")
        with open(path, "w") as contenedor:
            json.dump(self._doc_to_docID, contenedor)

        path = os.path.join(self.salida, "diccionario_ID_documentos.json")
        with open(path, "w") as contenedor2:
            json.dump(self._docID_to_doc, contenedor2)    
    
    def __parse_next_block(self):
        n = self._blocksize #espacio libre en el bloque actual
        termID = 0 #inicializamos el diccionario de términos
        bloque = [] #lista de pares (termID, docID)
        
        """ recorremos la lista de ids de tweet, nos quedamos con el texto de cada tweet, 
        y armamos una lista con las palabras que contiene el texto del tweet """
        for tweet_id in self._lista_de_tweet_ids:
            linea_tweet = self._db_tweets[tweet_id]["text"]
            n -= len(linea_tweet.encode('utf-8'))
            lista_palabras = [palabra for palabra in linea_tweet.split()]
            #doc = fileinput.filename()
            """ procesamos las palabras dentro del texto del tweet """
            for pal in lista_palabras:    
                if pal not in self._stop_words:
                    pal = self.__lematizar(pal)
                    if pal not in self._term_to_termID:
                        self._term_to_termID[pal] = termID
                        termID += 1
                    bloque.append((self._term_to_termID[pal], self._doc_to_docID[tweet_id]))
            """ cortamos el bloque si llegamos al tamaño maximo y devolvemos el bloque con yield """
            if n <=0:
                yield bloque
                n = self._blocksize
                bloque = []
        yield bloque

    def buscar(self, lista_expresiones, cant_tweets = None):
        lista_id_tweet=[]
        #Levantar diccionario de palabras_id
        with open("salida/diccionario_terminos.json", "r") as arch_terminos:
            dicc_palabras_id = json.load(arch_terminos)
        #Levantar diccionario id_interno_tweet/id_tweet  
        with open("salida/diccionario_ID_documentos.json", "r") as arch_id_int_id_tweet:
            dicc_id_int_id_tweet = json.load(arch_id_int_id_tweet)  
        #Levantar diccionario/indice con id_palabras/tweets
        with open("salida/postings.json", "r") as arch_palabras_tweets:
            dicc_palabras_tweets = json.load(arch_palabras_tweets)

        #Recorro los conjuntos de la lista solo mientras no encuentre un match
        i = 0
        encontrado = False
        res_and = set()
        res_not = set()
        res_id_int = set()
        lista_id_tweet = []
        res_id_int_final = set()
        
        while i < len(lista_expresiones):
            #divido al conjunto de not y and para armar la busqueda final
            res_and = set()
            res_not = set()
            res_id_int = set()
            conjunto_palabras = lista_expresiones[i]
            conjunto_and = {palabra for palabra in conjunto_palabras if palabra[0:1] != "!" } 
            conjunto_not = {palabra[1:] for palabra in conjunto_palabras if palabra[0:1] == "!" } 
            
            if conjunto_and is not None:
                for palabra in conjunto_and:  
                    #Primero chequeo que la palabra este en las keys del diccionario de terminos
                    palabra = self.__lematizar(palabra)
                    if palabra in dicc_palabras_id.keys():
                        id_palabra = dicc_palabras_id[palabra]
                        #Busco los tweets donde aparece
                        lista_tweets_id_int =  dicc_palabras_tweets[str(id_palabra)]
                        
                        if len(res_and ) == 0:
                            res_and = set(lista_tweets_id_int)
                        else:    
                            res_and = res_and & set(lista_tweets_id_int)
                    #si la palabra no esta entonces no hay resultado        
                    else: 
                        res_and = set() 
                        break     
            lista_tweets_id_int = []   
            if conjunto_not is not None:             
                for palabra in conjunto_not:
                    palabra = self.__lematizar(palabra)
                    #Primero chequeo que la palabra este en las keys del diccionario de terminos
                    if palabra in dicc_palabras_id.keys():
                        id_palabra = dicc_palabras_id[palabra]
                        #Busco los tweets donde aparece
                        lista_tweets_id_int =  dicc_palabras_tweets[str(id_palabra)]
                        if len(res_not ) == 0:
                            res_not = set(lista_tweets_id_int)
                        else:    
                            res_not = res_not | set(lista_tweets_id_int)   
                     #si la palabra no esta entonces no hay resultado        
                    else:  
                        res_not = set()                      
            if len(res_and) > 0:
                res_id_int = res_and - res_not
            else:#aca quilombo. Si no tiene ninguna restriccion mas que el or, tengo que devolver casi todo 
                if len(res_not) > 0: 
                    res_and = {id for id in dicc_id_int_id_tweet if str(id) not in str(res_not)  }
                    
                res_id_int = res_and
            i += 1    
            if len(res_id_int) > 0: #encontre patron de busqueda
                encontrado = True
                
            if len(res_id_int_final) == 0:
                res_id_int_final = res_id_int
            else:
                res_id_int_final =  res_id_int_final | res_id_int
        #Lo convierto a la lista de id correcto
        if len(res_id_int_final) > 0:
            lista_id_tweet = [dicc_id_int_id_tweet[str(id_tweet_int)] for id_tweet_int in res_id_int_final]
        
        if cant_tweets is not None:
            #ordeno el resultado 
            fin = cant_tweets
            lista_id_tweet.sort()
            if cant_tweets > len(lista_id_tweet):
                fin = len(lista_id_tweet)
            return lista_id_tweet[0:fin]
        else:    
            return lista_id_tweet
            

if __name__ == '__main__':
    h = helpers()
    #texto = "((Rubio AND Pelo) OR Tupla) AND (Cigarro OR Cosa)"
    #texto = "(work OR free) AND (elon)"
    texto = "(work) OR (NOT elon AND NOT elonmusk AND free)"
    #texto = "bless AND historyoarmani2"
    exp = expresiones(texto)
    print(exp.expresion_resuelta)
    """ abrimos el shelve con los tweets recolectados """

    with shelve.open("tweet_shelve.s") as db_shelve:        
        indice_invertido = word_finder_BSBI(db_shelve, "./salida")
        resultado = indice_invertido.buscar(exp.expresion_resuelta, 10)
        
        print(len(resultado))
        if len(resultado)> 0:    
            for id in resultado:
                #print(id,db_shelve[id]["created_at"],db_shelve[id]["username"])
                #print(db_shelve[id]["created_at"], db_shelve[id]["username"],db_shelve[id]["text"])
                print(id,db_shelve[id]["created_at"],db_shelve[id]["text"])
                print("***************************************")
        
   
