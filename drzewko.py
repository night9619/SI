from math import log2

with open('cw 1/p.txt', 'r') as f:
    element = [line.strip() for line in f]

lista = [el.split(',') for el in element]

#kazda kolumna tworzy osobna liste
poKolumnach = []
for kolumna in range(len(lista[0])):
    kol = []
    for element in lista:
        kol.append(element[kolumna])
    poKolumnach.append(kol)
    
#kolumna decyzji
decyzja = poKolumnach[-1]

#liczba rekordow
T = len(poKolumnach[-1])

#liczba atrybutów (kolumn)
lAtrybutow= len(lista[0])-1

#unikalne wartosci decyzji
unikalneDecyzje = sorted(set([el for el in decyzja]))

#unikalne wartosci atrybutów (unikalne wart w kazdej kolumnie)
unikalne = {}
for nrK in range(len(lista[0])):
    unikalne[nrK+1] = list(set([el for el in poKolumnach[nrK]]))

#liczba wart w danej kolumnie (w danym atrybucie)
ileWartosciWKolumnie = {}
for nrKolumny in range(len(poKolumnach)):
    kolumna = poKolumnach[nrKolumny]
    wartosci = {i for i in kolumna}
    ileWartosciWKolumnie[nrKolumny+1] = len(wartosci)

#podusmowanie klasy, ile jest danych wartosci dla danego atrybutu
sumaKlasy = {}
for nrK, kolumna in enumerate(poKolumnach):
    k = {}
    for element in kolumna:
        for u in  unikalne[nrK+1]:
            k[u] = kolumna.count(u)
    sumaKlasy[nrK+1] = k
    
#jakie sa dacyzje dla danych wart w klasach
podsumowanieKlas = { }
for nr in range(len(poKolumnach)):
    dlaKolumny = {}
    for ipk,pk in enumerate(sumaKlasy[nr+1]):
        tab = [decyzja[iel] for iel,el in enumerate(poKolumnach[nr]) if el==pk ]
        dlaKolumny[pk] = {wart : tab.count(wart) for wart in decyzja}
    podsumowanieKlas[nr+1] = dlaKolumny 

Info = {}
Gain = {}
Split = {}
GainRatio = {}

maxA=0

def I(P):
    wynik = (-1)*sum([p*log2(p) for p in P if p!=0])
    return wynik

podsumowanieDecyzji = sumaKlasy[len(poKolumnach)]
zbior = [podsumowanieDecyzji[a]/len(decyzja) for a in podsumowanieDecyzji]

def Informacje(numer):
    info=0
    split=0
    print("\n")
    print("A"+str(numer))
    print(sumaKlasy[numer])
    print(T)
    C = [ podsumowanieKlas[numer][x] for x in podsumowanieKlas[numer] ]
    for w in range(ileWartosciWKolumnie[numer]):
        print("\n")
        print("\t",'Decyzje:')
        print("\t",unikalne[numer][w])
        print("\t",C[w])
        liczebnosc = [C[w][a] for a in C[w]]
        Ti = sum(liczebnosc)
        PP = [C[w][a]/Ti if Ti!=0 else "0" for a in C[w]]
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
    
print("=====")
print(sumaKlasy[len(poKolumnach)])
print(zbior)
print("Entropia:",I(zbior))
print("=====")

for nr in range(len(poKolumnach)-1):  
    Informacje(nr+1)

print("\n")
for nr in range(len(poKolumnach)-1):
    print(f"Info(A{str(nr+1)},T)= {Info[nr+1]}   \t Gain(A{str(nr+1)},T)= {Gain[nr+1]}")

#wyznacza max Gain
for a in Gain:
    if Gain[a]==max(Gain.values()):
        maxA=a
        
#wyznacza max Gain i usuwa wczesniejsze atrybuty        
def maxAtryb(atryb):
    if atryb in Gain:
        del Gain[atryb]
    for a in Gain:
        if Gain[a]==max(Gain.values()):
            maxA=a
            return maxA

print("\nWybrany atrybut A{}, bo w tym przypadku najwyższa jest wartość Gain: {}".format(maxA,max(Gain.values())))

print("\n")
for nr in range(len(poKolumnach)-1): 
    print(f"Split(D{str(nr+1)},T)= {Split[nr+1]}   \t Gain Ratio(D{str(nr+1)},T)= {GainRatio[nr+1]}")

def szukaj(atryb):
    t=1
    C = [ podsumowanieKlas[atryb][x] for x in podsumowanieKlas[atryb] ] 
    for w in range(ileWartosciWKolumnie[atryb]):
        
        tab="\t"*atryb
        
        Ti = sum([C[w][a] for a in C[w]])
        PP = [C[w][a]/Ti for a in C[w] if Ti!=0]
        
#         def dec():
#             for a in C[w]:
#                 k = a
#                 k = a+f"({C[w][a]})"
#             return k

#         if I(PP) == 0:
#             print(f"{tab}A{atryb} =",unikalne[atryb][w],":",dec()) 
#         else:
#             if atryb>=lAtrybutow:
#                 print(f"{tab}A{atryb} =",unikalne[atryb][w],":",dec())
#                 t+=1
#                # print(f"{tab}\t|--->"+a+f"({C[w][a]})")
#             else:
#                 print(f"{tab}A{atryb} =",unikalne[atryb][w],":") 
#                 print(f"{tab}|-------------->")
#                 t+=1

#                 noweA = maxAtryb(atryb) 
#                 szukaj(noweA)


#         for a in C[w]:            
#             if I(PP) == 0 and C[w][a]!=0:
#                 print(f"{tab}\tA{atryb} =",unikalne[atryb][w],":") 
#                 print(f"{tab}\t|--->"+a+f"({C[w][a]})")
#             elif C[w][a]==0:
#                 continue
#             else:
#                 if atryb>=lAtrybutow:
#                     print(f"{tab}\tA{atryb} =",unikalne[atryb][w],":") 
#                     print(f"{tab}\t|--->"+a+f"({C[w][a]})")
#                 else:
#                     print(f"{tab}A{atryb} =",unikalne[atryb][w],":") 
#                     print(f"{tab}|-------------->")
                    
#                     noweA = maxAtryb(atryb) 
#                     if noweA!=atryb:
#                         szukaj(noweA)

        #for a in C[w]:
            
        if I(PP) == 0 and (C[w][a] for a in C[w])!=0:
            print(f"{tab}A{atryb} =",unikalne[atryb][w],":", [a for a in C[w] if C[w][a]!=0]) 
        elif (C[w][a] for a in C[w])==0:
            continue
        else:
            if atryb>=lAtrybutow:
                print(f"{tab}A{atryb} =",unikalne[atryb][w],":", [a for a in C[w] if C[w][a]!=0]) 
            else:
                print(f"{tab}A{atryb} =",unikalne[atryb][w],":") 
                print(f"{tab}|-------------->")

                noweA = maxAtryb(atryb) 
                if noweA!=atryb:
                    szukaj(noweA)
                        
    
def budujDrzewo():
    print("\nDrzwo decyzyjne dla {0} przypadków ({1} atrybutów)".format(T,lAtrybutow))
    szukaj(maxA) 
    
budujDrzewo()
