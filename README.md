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

```




## Usage de la vue script

```bash
python -m pdm run toudou
python -m pdm run toudou init-db

toudou create --task MaTache
toudou get --id 579897719
toudou get-all
```

## Serveur Flask IHM
J'ai choisi de recréer une nouvelle vue, via un blueprint, pour mon application Flask, nommée ihm_view. Cela permet de continuer à utiliser le cli facilement et de rendre le code plus clair.

Pour lancer notre serveur Flask
```bash
python -m pdm run start
```

Pour se connecter, aller sur la page http://127.0.0.1:5000/ et renseigner john:hello (admin) ou susan:bye (user, cad uniquement la vue principale)

## API

Pour utiliser l'API

```bash
curl -H "Authorization: Bearer secret-token-1" http://127.0.0.1:5000/api/todos
curl -H "Authorization: Bearer secret-token-1" http://127.0.0.1:5000/api/todos?complete=true
curl -d '{"task" : "myTask", "complete": "true", "due": "2023-05-04"}' -H "Authorization: Bearer secret-token-1" -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/todos
curl -d '{"task" : "myTaskUpdated", "complete": "false", "due": "2023-09-04"}' -H "Authorization: Bearer secret-token-1" -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/api/todos/77223332
curl -H "Authorization: Bearer secret-token-1" -X DELETE http://127.0.0.1:5000/api/todos/1814177
```

## Serveur d’application
```bash
python -m pdm run gunicorn --bind=0.0.0.0 toudou.wsgi:app
```

Aller sur http://127.0.0.1:8000

Remarque : ne fonctionne pas sous Windows (on peut suivre https://stackoverflow.com/questions/62788628/modulenotfounderror-no-module-named-fcntl )

## Packaging

J'ai du rajouter le fichier MANIFEST.in pour inclure les fichiers statiques dans le package généré par pdm build

```bash
python -m pdm build
docker build . -t toudou 
docker run -dp 8000:8000 --env-file ./docker.env --bind=0.0.0.0 toudou.wsgi:app
```

Aller sur http://127.0.0.1:8000
