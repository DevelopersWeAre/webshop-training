# Django

Potreban software:
1. Python 3.x
2. Virtualenv ili neki drugi software za virtuelne razvojne sredine: pyenv, conda i sl. (Ovaj vodic je za virtuelnv, za ostale pogledati [pyenv](https://realpython.com/intro-to-pyenv/) i [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/index.html))

Instalacija django biblioteka i pokretanje projekta:
____________________________

1. Kreirati virtual env u folderu koji se nalazi iznad webshop-training foldera (u koji smo klonirali repozitorijum):
- ```virtualenv -p python3.7 env```
- ```source env/bin/activate``` - ako je unix-like sistem ili ```env\Scripts\activate.bat``` za windows sisteme

2. Instalirati potrebne python biblioteke:
- ući u folder *src/backend* i pokrenuti komandu
- ```pip install -r requirements.txt```

3. Ući u folder *webshop* i pokrenuti projekat u dev modu:
- ```./manage.py runserver```
- komanda ce pokrenuti django server i u pretrazivacu ce biti dostupna test stranica na adresi: localhost:8000

4. Ako je prvo pokretanje potrebno je odraditi dodatne korake:
- Za kreiranje lokalne sqlite baze: 
  > ```./manage.py makemigrations``` - za pripremu shema tabela
  > ```./manage.py migrate``` - za kreiranje tabela (ili u lokalnom slucaju i baze i tabela)
  > ```./manage.py createsuperuser``` - za kreiranje administratorskog korisnika sa kojim se prijavljujemo na endpointu: /api/v1/techops


