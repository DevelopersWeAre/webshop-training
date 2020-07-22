# Uputstvo za kloniranje

```git clone https://github.com/DevelopersWeAre/webshop-training.git```

## Povlačenje poslednje develop grane:
-------------------------------------
```git pull develop```

## Kreiranje grane:
-------------------
1. Povući poslednji develop:

```git pull develop```
```git checkout develop```

2. Napraviti novu granu iz develop-a:
```git checkout -b <ime-grane>``` 
  u tački 4 je opisano kako se daju imena granama (mada je podložno promenama u zavisnosti od dogovora)

3. Posle završetka rada na ticket-u potrebno je napraviti PR (tzv. Pull Request) i odrediti review-ere, odnoso kolege i saradnike koji će pregledati rad i dati konstruktivne kritike gde je neophodno. Kritike koda i rada nikada ne treba shvatati kao nešto negativno, već kao pozitivni podsticaj i savet.
Proces pravljenja PR je sledeći:

    * ```git status``` da proverimo da samo naše izmene idu u granu
    * ```git add <ime_promenjenog fajla>``` ili ```git add .``` ako smo menjali više od jednog
    * ```git commit -m "kratka poruka za commit"``` koja bi trebala da bude vise u fazonu: "Dodaje novi dropdown za izbornik datuma"
    * ```git push origin <ime-grane>```
    * ako koristite visual studio code, onda na link koji se pojavi je potrebno kliknuti i onda se otvara tab u pretraživaču za kreiranje PR-a

4. Imenovanje grana bi trebalo da bude na sledeci način:
```<backend ili frontend>-<ime_zadatka na kome se radi>```
