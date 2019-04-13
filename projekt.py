#!/usr/bin/env python
# coding: utf-8

# In[1]:


from math import log2

#wczytanie danych
with open('cw 1/pogoda.txt', 'r') as f:
    element = [line.strip() for line in f]

lista = [el.split(',') for el in element]


# In[2]:


lista


# In[3]:


liczbaAtrybutów = len(lista[0])-1
liczbaAtrybutów


# In[4]:


#lista atrybutów (można ew jak wczytac z pliku)
labels = ["A"+str(nr+1) for nr in range(len(lista[0])-1)]
labels


# In[5]:


liczbaWierszy = len(lista)
liczbaWierszy


# In[6]:


#ostatnia kolumna - decyzje
decyzje = [wiersz[liczbaAtrybutów] for wiersz in lista]
decyzje


# In[7]:


def decyzjeKolumna(dane):
    return [kol[-1] for kol in dane]


# In[8]:


decyzjeKolumna(lista)


# In[9]:


#dla każdej unikalnej wartosci w kolumnie zliczam wystąpienia
def licznikUnikalnychWartosci(nrKolumny,dane):
    unikalne = {}
    for wiersz in dane:
        wartosc = wiersz[nrKolumny]
        if wartosc not in unikalne:
            unikalne[wartosc] = 0
        unikalne[wartosc] +=1
    
    return unikalne


# In[10]:


for nrK in range(liczbaAtrybutów):
    print(licznikUnikalnychWartosci(nrK,lista))


# In[11]:


#ile jest unikalnych wartosci w kolumnie
def ileWartWKolumnie(nrKolumny):
    klucze = list(licznikUnikalnychWartosci(nrKolumny,lista).keys())
    licznik = len(klucze)
    
    return licznik


# In[12]:


for nrK in range(liczbaAtrybutów):
    s1 ={}
    s1[nrK] = ileWartWKolumnie(nrK)
    print(s1)


# In[13]:


#jakie sa unikalne wartosci w kolumnie
def unikalneWartosciWKolumnie(nrKolumny,dane):
    kolumna = [wiersz[nrKolumny] for wiersz in dane]
    unikalne = set([wartosc for wartosc in kolumna])
    return list(unikalne)


# In[14]:


for nrK in range(liczbaAtrybutów):
    print(unikalneWartosciWKolumnie(nrK,lista))


# In[15]:


# tworzy słownik z unikalnymi wartosciami i padajacymi po nich decyzjami
def wartosciDecyzji(k):   # k to kolumna
    dlaKolumny = {}
    for ipk,pk in enumerate(k):
        tab = [decyzje[iel] for iel,el in enumerate(k) if el==pk ] #jakie sa decyzje dla wartosci
        #print(tab)
        dlaKolumny[pk] = {wart : tab.count(wart) for wart in decyzje}
    return dlaKolumny


# In[16]:


k = [wiersz[1] for wiersz in lista]
k


# In[17]:


wartosciDecyzji(k)


# In[18]:


Info = {}
Gain = {}
Split = {}
GainRatio = {}

maxA=0
T= liczbaWierszy


# Entropia

# In[19]:


#entropia
def I(P):
    wynik = (-1)*sum([p*log2(p) for p in P if p!=0])
    return wynik


# In[20]:


podsumowanieDecyzji = licznikUnikalnychWartosci(liczbaAtrybutów,lista) # unikalne decyzje+licznik
print(podsumowanieDecyzji)
zbior = [podsumowanieDecyzji[a]/len(decyzje) for a in podsumowanieDecyzji] #prawdopodobieństo dla całego zbioru
print(zbior)


# In[21]:


def Informacje(numer):
    info=0
    split=0
    print("\n")
    print(labels[numer]) #atrybut
    print(licznikUnikalnychWartosci(numer,lista)) 
    print(liczbaWierszy)
   
    #for w in range(len(licznikUnikalnychWartosci(numer))):
    k = [wiersz[numer] for wiersz in lista] #cala kolumna
    for wart in list(licznikUnikalnychWartosci(numer,lista).keys()):
        licznikDecyzji = wartosciDecyzji(k)        
        print("\n")
        print("\t",'Decyzje:')
        print("\t",wart)
        print("\t",licznikDecyzji[wart]) 
        liczebnosc = [licznikDecyzji[wart][a] for a in licznikDecyzji[wart]]
        Ti = sum(liczebnosc)
        PP = [licznikDecyzji[wart][a]/Ti if Ti!=0 else "0" for a in licznikDecyzji[wart]]
        print("\t",PP)
        print("\t",I(PP),'*', Ti/T)
        
        info += I(PP) * (Ti/T)
        split += ((-1)*(Ti/T)* log2(Ti/T))

        print("\t", info)
        
    gain = I(zbior)-info
    if split > 0:
        gainRatio = gain/split
    
    Info[numer] = info
    Gain[numer] = gain
    Split[numer] = split
    GainRatio[numer] = gainRatio


# In[22]:


print("=====")
print(podsumowanieDecyzji)
print(zbior)
print("Entropia:",I(zbior)) # etropia dla całego zbioru
print("=====")

for nr in range(liczbaAtrybutów):  
    Informacje(nr)


# In[23]:


print("\n")
for nr in range(liczbaAtrybutów):
    print(f"Info({labels[nr]},T)= {Info[nr]}   \t Gain({labels[nr]},T)= {Gain[nr]}")

#wyznacza max Gain
for a in Gain:
    if Gain[a]==max(Gain.values()):
        maxA=a

print(f"\nWybrany atrybut {labels[maxA]}, bo w tym przypadku najwyższa jest wartość Gain: {max(Gain.values())}")

print("\n")
for nr in range(liczbaAtrybutów): 
    print(f"Split(D{str(nr+1)},T)= {Split[nr]}   \t Gain Ratio(D{str(nr+1)},T)= {GainRatio[nr]}")


# In[37]:


maxAtryb([0,1,2,3])


# In[43]:


listaNumerow = [nr for nr in range(len(lista[0])-1)]
listaNumerow


# In[38]:


def maxAtryb(lista):
    #maxA=0
    g = [Gain[a] for a in lista]
    maxGain=max(g)

    for ga in Gain:
        if Gain[ga]==max(Gain.values()):
            maxA=ga
    return maxA

        
# def nowaLista(dane, nrWiersza):
#     nowaLista(dane, atryb, w):
#     nowaL = []
#     nowaL.append(dane[nrWiersza])
#     return nowaL

def nowaLista(dane, atryb, value):
    newSet = []
    for wiersz in dane:
        if wiersz[atryb] == value:
            newSetSample = wiersz[:atryb]        #making copy
            newSetSample.extend(wiersz[atryb:])#extends the list by adding all items of a list
            newSet.append(newSetSample)     #add to new Set
    return newSet

def class_counts(rows):
    counts = {}
    for row in rows:
        if row not in counts.keys():
            counts[row] = 0
        counts[row] += 1
    return max(counts)


# In[46]:


import json
drzewo = {}

# atryb, dane
def szukaj(atryb, dane):
    print("\nNajlepszy atrybut: ", labels[atryb])
    tab="\t"*atryb
    
#     k = [wiersz[atryb] for wiersz in dane] 
#     #print(k)
#     #drzewo[atryb] = wartosciDecyzji(k)
#     #print(wartosciDecyzji(k))
#     for nrWiersza,a in enumerate(wartosciDecyzji(k)):
#         print(f"{tab}{labels[atryb]} = {a}")
#         for w in wartosciDecyzji(k)[a]:
#             if wartosciDecyzji(k)[a][w] != 0:

#                 #nowaLista(dane, nrWiersza)
#                 #nowaLista.append(dane[nrWiersza])
#                 print("działam")
#             elif wartosciDecyzji(k)[a][w] == 0:
#                 print(f"\t{tab}: {w}")
# #                 print(nrWiersza)
#                 del dane[nrWiersza]
#             #print(dane)
#             noweA = maxAtryb(atryb)
#             if noweA == None:
#                 continue
#             szukaj(noweA,dane)
    d = decyzjeKolumna(dane)

    #wyswietla decyzje, koniec podziału
    if d.count(d[0]) == len(d):
        print(d[0])
        
    if len(dane[0]) == 1:
        return class_counts(d)
        
    atrybut = labels[atryb]
    drzewo = { atrybut: {} }
    print(drzewo) 

    del(listaNumerow[atryb])
  
    unik = unikalneWartosciWKolumnie(atryb,dane)
    
    for w in unik:
        listaA=listaNumerow[:]
        noweA = maxAtryb(listaA)
        print(nowaLista(dane, atryb, w))
        drzewo[atrybut][w] = szukaj(noweA, nowaLista(dane, atryb, w))
    #print(nowaLista(dane, atryb, w))
        
    return drzewo
    
    
    #for wart in unikalneWartosciWKolumnie(atryb,lista):
        
        #print(f"{tab}{labels[atryb]} = {wart}")
             # ,unikalne[atryb][w],":", [a for a in C[w] if C[w][a]!=0]) 
  
                        
    
def budujDrzewo():
    print("\nDrzwo decyzyjne dla {0} przypadków ({1} atrybutów)".format(liczbaWierszy,liczbaAtrybutów))
    szukaj(maxA,lista) 
    
budujDrzewo()
print(json.dumps(drzewo, indent=4, sort_keys=True))


# In[ ]:


Gain


# In[ ]:




