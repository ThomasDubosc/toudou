# Toudou

The best todo application!

Git : https://github.com/ThomasDubosc/toudou

## Installing

```
 Set-Alias -name python C:\Python\python.exepython
```

### Creation d'un environnement virtuel
```bash
python -m venv venv
```
### Initialisation de l'env. virtuel
```
venv\Scripts\Activate.ps1
python -m pip install -e .
```
OU avec PDM

```bash
python -m pip install pdm 
python -m pip install --upgrade pip
python -m pdm install
python -m pdm run toudou
python -m pdm run toudou init-db
```




## Usage de la vue script

```bash
toudou
toudou init-db
toudou create --task MaTache
toudou get --id 579897719
toudou get-all
```

## Serveur Flask
J'ai choisi de recréer une nouvelle vue pour mon application Flask, nommée flaskviews. Cela permet de continuer à utiliser le cli facilement et de rendre le code plus clair.

Pour lancer notre serveur Flask
```bash
python -m pdm run start
```

Pour se connecter, aller sur la page http://127.0.0.1:5000/

Pour utiliser l'API

```bash
curl http://127.0.0.1:5000/api/toudou
curl -X POST "http://127.0.0.1:5000/api/toudou" --data-raw "task=UnExemple&complete=on&due=2023-03-24"
curl http://127.0.0.1:5000/api/toudou/925753
curl -X DELETE http://127.0.0.1:5000/api/toudou/925753
```