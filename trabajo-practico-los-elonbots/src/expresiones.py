import string
from helper_funcs import helpers

class expresiones:

    def __init__(self, expresion):
        ''' Recibe un texto con la expresion logica
        que se va a buscar'''
        self.expresion = expresion
        self.expresion_resuelta = self.__resolver_expresion(self.expresion)    
    
    def __resolver_expresion(self, expresion):
        ''' Le paso la expresion de palabras de busqueda del usuario'''
        #recorrer expresion y si hay un parentesis agregar un espacio
        expresion_parent_separado = self.agregar_espacios_en_parentesis(self.expresion)
        #recorrer expresion y si hay un not crear la palabra negada que identificaremos al buscar
        expresion_final = self.crear_palabras_not(expresion_parent_separado)
        
        conjunto_expresion = self.armar_conj_expresiones(expresion_final)
        return conjunto_expresion

    def armar_conj_expresiones(self,expresion):
        if expresion is None:
            return []
        #convierto la expresion en una lista de palabras    
        lista_expresion = expresion.split()
        if len(lista_expresion) == 1:
            return [{expresion}]
        #tengo que tener al menos palabra operador palabra
        if len(lista_expresion) < 3:
            #voy a devolver vacio pero aca deberia ir una excepcion
            return []
        primera_palabra = lista_expresion[0]
        if primera_palabra == "(":
            #obtener_subexpresion obtiene una tupla con la expresion mas externa con parentesis
            #y el indice de donde termina esa expresion
            res_expresiones = self.obtener_subxpresion(lista_expresion)
            subexpresion1 = res_expresiones[0]
            if res_expresiones[1] >= len(lista_expresion):
                return self.armar_conj_expresiones(subexpresion1)
            operador = lista_expresion[res_expresiones[1]]
            if operador not in {"AND", "OR"}:
                #voy a devolver vacio pero aca deberia ir una excepcion
                return []
            subexpresion2 = ' '.join(lista_expresion[res_expresiones[1] + 1:])
            return self.concatenar(self.armar_conj_expresiones(subexpresion1),self.armar_conj_expresiones(subexpresion2), operador)
        else:
            operador = lista_expresion[1]
            if operador not in {"AND", "OR"}:
                #voy a devolver vacio pero aca deberia ir una excepcion
                return []
            subexpresion = self.armar_conj_expresiones(' '.join(lista_expresion[2 :]))
            return self.concatenar([{primera_palabra}], subexpresion, operador)
    
    def concatenar(self,lista1, lista2, operador):
        res = []
        if operador == "AND":
            for palabras in lista1:
                for mas_palabras in lista2:
                    res.append(palabras | mas_palabras)
        if operador == "OR":
            for palabras in lista1:
                for mas_palabras in lista2:
                    res.append(palabras) 
                    res.append(mas_palabras)
        return res

    '''obtener_subexpresion obtiene una tupla con la expresion mas externa con parentesis
    y el indice de donde termina esa expresion'''
    def obtener_subxpresion(self,lista_expresion):
        cant_parentesis_que_abren = 0
        cant_parentesis_que_cierran = 0
        subexpresion = ""
        i = 0
        for palabra in lista_expresion:
            if palabra == "(":
                cant_parentesis_que_abren += 1
            if palabra == ")":
                cant_parentesis_que_cierran += 1    
            if cant_parentesis_que_abren == cant_parentesis_que_cierran:
                subexpresion = ' '.join(lista_expresion[1 : i ])
                return (subexpresion, i + 1)
            i += 1    
        return (subexpresion, i )

    def agregar_espacios_en_parentesis(self,expresion):
        i = 0
        res = ""
        while i < len(expresion):
            if expresion[i:i+1] == "(" or expresion[i:i+1] == ")":
                if expresion[i:i+1] == "(" :
                    res += expresion[i:i+1] + ' '
                if expresion[i:i+1] == ")":    
                    res += ' '  + expresion[i:i+1] 
            else:    
                res += expresion[i:i+1] 
            i += 1    
        return res

    def crear_palabras_not(self,expresion):
        i = 0
        ini = 0
        fin = len(expresion)
        res = ""
        while expresion.find("NOT", ini, fin) != -1:
            i = expresion.find("NOT", ini, fin)
            if i + 4 < len(expresion):
                res += expresion[ini:i] + "!" + expresion[i+4: i+5] 
            else:
                res += expresion[ini:i] + "!" 
            ini = i + 5

        if ini < len(expresion):
            res += expresion[ini:fin]   
        return res  
    
        
if __name__ == "__main__":
    h = helpers()
    #diccionario = h.recuperar_shelve("tweet_shelve.s")
    texto = "((Rubio AND Pelo) OR Tupla) AND (Cigarro OR NOT Cosa)"
    #texto = "(Rubio AND Pelo) OR Tupla"
    exp = expresiones(texto)
    print(exp.expresion_resuelta)