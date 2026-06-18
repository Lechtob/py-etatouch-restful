# py-etatouch-restful

Async Python client fuer die ETA Touch RESTful Webservices.

Die ETA-Dokumentation beschreibt die Webservices unter `http://<eta-ip>:8080`:

- `GET /user/api`: API-Version lesen.
- `GET /user/menu`: Menuebaum lesen.
- `GET /user/var/<uri>`: einzelne Variable lesen.
- `POST /user/var/<uri>`: schreibbare Variable setzen.
- `GET/PUT/DELETE /user/vars`: temporaere Variablensets verwalten.
- `GET /user/errors`: aktive Fehler lesen.
- `GET /user/varinfo/<uri>`: Metadaten und gueltige Werte lesen.

## Beispiel

```python
from etatouch_restful import EtaTouchClient

async with EtaTouchClient("192.168.1.50") as client:
    api_version = await client.get_api_version()
    value = await client.get_variable("112/10021/0/0/12112")
```

## Hinweis

Variablen-URIs sind geraetespezifisch. Fuer einen ETA PU15 koennen sie aus `/user/menu`
und `/user/varinfo/...` abgeleitet werden.

## Repository Setup

Empfohlene GitHub-Repo-Einstellungen:

- Repository-Name: `py-etatouch-restful`
- Default Branch: `main`
- Develop Branch: `develop`
- PyPI-Paketname: `py-etatouch-restful`

Initialer Push in ein leeres Repo:

```powershell
git init
git add .
git commit -m "Initial py-etatouch-restful scaffold"
git branch -M main
git remote add origin https://github.com/<user>/py-etatouch-restful.git
git push -u origin main
git switch -c develop
git push -u origin develop
```

## Release Notes

Vor dem ersten HACS/Core-nahen Einsatz sollte dieses Paket auf PyPI veroeffentlicht
werden, damit Home Assistant es ueber `requirements` installieren kann.
