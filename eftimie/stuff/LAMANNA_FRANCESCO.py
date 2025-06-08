'''Utilizzato in: E1'''
import math
'''Utilizzato in: E2'''
import random
import libreria_esercizi

def E1_Triangoli():
    lati = libreria_esercizi.E1_Triangoli_ask()
    categoria = libreria_esercizi.E1_Triangoli_classifier(lati)
    if categoria != "N/A":
        area = libreria_esercizi.E1_Triangoli_area(lati)
        perimetro = libreria_esercizi.E1_Triangoli_perimetro(lati)
        print(f"Il perimetro è {perimetro}, e l'area è {area}")


def E2_Range():
    '''Metodo 1'''
    lista = []
    lista.append(2)
    while(lista[-1] != 200):
        lista.append(lista[-1] + 2)
    print("Metodo 1:")
    print(lista)

    '''Metodo 2'''
    lista = []
    for i in range(2, 202, 2):
        lista.append(i)
    print("Metodo 2:")
    print(lista)

    '''Metodo 3'''
    lista = []
    lista.append(2)
    while(len(lista) < 100):
        n = random.randint(2, 200)
        if(n%2 == 0):
            for i in lista:
                if(n == i):
                    n = -1
                    break
            if (n > 0):
                lista.append(n)
    print("Metodo 3:")
    print(lista)
    lista.sort()
    print("Metodo 3 ordinato:")
    print(lista)



def E3_ListaStringa():
    lista = ["Mario", "Luigi", "PrincipessaPeach", "Bowser", "Toad"]
    stringa = libreria_esercizi.E3_ListaStringa(lista)
    print(stringa)



def E4_Cantina():
    parola = input("Scrivi una parola: ")
    lista = [l for l in parola]
    [lista.append(l) for l in reversed(parola[:-1])]
    print(lista)



def E5_FunzioneLista(func):
    
    for i in range(len(L)-1):
        if (i%2 == 0):
            if(func == "abs()"):
                try:
                    L[i] = abs(L[i])
                except :
                    print(f"Error trying to use the abs() function on {L[i]}")
                    break
            if(func == "str.capitalize()"):
                try:
                    L[i] = L[i].capitalize()
                except :
                    print(f"Error trying to use the str.capitalize() function on {L[i]}")
                    break
            if(func == "pow()"):
                try:
                    L[i] = pow(L[i], 2)
                except :
                    print(f"Error trying to use the pow() function on {L[i]}")
                    break
        if(i == len(L)-2):
            print(L)



opt = input("Scegli il numero dell'esercizio: ")
if (opt == '1'):
    print("ESERCIZIO_1: TRIANGOLI")
    E1_Triangoli()
elif (opt == '2'):
    print("ESERCIZIO_2: RANGE")
    E2_Range()
elif (opt == '3'):
    print("ESERCIZIO_3: LISTA_STRINGA")
    E3_ListaStringa()
elif (opt == '4'):
    print("ESERCIZIO_4: CANTINA")
    E4_Cantina()
elif (opt == '5'):
    print("ESERCIZIO_5: FUNZIONE_LISTA")
    L = [-2,-3,-4,-5,-6,-7]
    '''L = list('ciaociao')'''
    E5_FunzioneLista("abs()")
    '''E5_FunzioneLista("str.capitalize()")'''
    '''E5_FunzioneLista("pow()")'''
else:
    print("Comando non riconosciuto")