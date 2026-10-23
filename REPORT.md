# TP2 — Git et DVC

> **À noter :** le dossier TP1 original n'était pas disponible dans le workspace.
> Les trois CSV de ce projet sont donc des données de démonstration créées pour
> suivre le TP et reproduire ses totaux annoncés; ils ne sont pas les données
> originales du TP1. Le fichier `orders_day1.csv` a 30 lignes en v1, dont 25
> conservées après nettoyage, puis 35 lignes en v2, dont 30 conservées.

## Q1 — Travail sur une branche

La branche `feature/country-rule` a été créée et fusionnée dans `main` avec
`--no-ff`. Le squelette de démonstration contenait déjà la règle pays dans son
commit initial; la branche a ajouté les tests qui vérifient son comportement.
Dans le projet TP1 original, la règle devrait être développée et testée sur
cette branche avant sa fusion.

## Q2 — Pull request

Une pull request permet de demander une revue de code, de discuter des
modifications et d'effectuer des vérifications avant la fusion.

## Q3 — Empreinte MD5

L'empreinte identifie le contenu suivi par DVC. Une modification des données
entraîne normalement une nouvelle empreinte, comme le montrent `data-v1` et
`data-v2` dans `data/raw.dvc`.

## Q4 — Fichier .gitignore

Le fichier `data/.gitignore`, créé par DVC, ignore le dossier `raw/` afin que
Git versionne le pointeur `data/raw.dvc` plutôt que les fichiers CSV eux-mêmes.

## Q5 — Stockage DVC

Le remote local `storage` se trouve dans `..\dvc-storage`, à côté du projet.
DVC stocke les objets par contenu, ce qui permet de réutiliser les données
identiques et de récupérer une version depuis le remote.

## Q6 — Pointeur DVC

Git versionne `data/raw.dvc`, qui contient l'empreinte et les métadonnées des
données. Les commits et les tags permettent de retrouver ces références dans
l'historique.

## Q7 — Comparaison des versions

Le code reste identique pendant la comparaison des jeux de données.

- `data-v1` : total `7655.90`, 30 lignes brutes et 25 conservées.
- `data-v2` : total `8835.40`, 35 lignes brutes et 30 conservées.

## Q8 — Git checkout et DVC checkout

`git checkout` restaure le pointeur DVC de la version choisie. `dvc checkout`
restaure les fichiers de données correspondant à ce pointeur.

## Q9 — Oubli de dvc checkout

Les données présentes sur le disque peuvent ne pas correspondre à la version
indiquée par Git. Le rapport risque alors d'être incorrect ou non reproductible.

## Q10 — Git clone et DVC pull

`git clone` récupère le dépôt Git et son historique. `dvc pull` récupère les
données versionnées sur le remote. Le clone `teammate` a récupéré les trois CSV
et reproduit le total `8835.40`.

## Q11 — Oubli de dvc push

Si les objets de `data-v2` n'ont pas été poussés, le collègue ne pourra pas les
récupérer avec `dvc pull`. Le total `8835.40` ne pourra pas être reproduit à
partir du remote. L'ancienne version reste disponible uniquement si ses objets
sont encore accessibles.

## Historique Git

Sortie réelle de `git log --oneline --graph --decorate` avant le commit de ce
rapport :

```text
* ab22d49 (HEAD -> main) Verify latest DVC data in pipeline tests
* f429881 Describe the report as a DVC stage
* 500716d (tag: data-v2) Data v2: late orders for 2026-10-05
* 64a3f3a Add the DVC remote
* d852091 (tag: data-v1) Track raw data with DVC
*   f575ddf Merge the country rule
|\
| * 15a775d (feature/country-rule) Reject orders from countries the shop does not sell to
|/
* f31b049 Create TP2 demonstration pipeline
```
