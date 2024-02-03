# net7.dev

Site web vitrine de présentation de net7.

## Développement

### Pré-requis

- [Poetry](https://python-poetry.org/docs/)

### Installation

```bash
poetry install
```

### Compilation

```bash
./build.sh
```

## Architecture

Toutes les pages sont statiques, et la page Réalisations (`realisation.html.j2`) est une template [Jinja2](https://jinja.palletsprojects.com/en/3.0.x/) qui génère le contenu à partir des projets du git qui:

- sont publics
- ont le topic "sur net7.dev"
- possède un fichier `.ortfo/description.md` qui décrit brièvement le projet, avec cette syntaxe:

```markdown
---
url: https://lien.vers.le/site
git: groupe/repo # par exemple, net7/website pour ce dépôt
---

# Nom du projet

Quelques phrases pour décrire le projet.

![](./chemin/vers/une/image.png)

![](./chemin/vers/une/autre/image.png)

<!-- on peut rajouter autant d'images que l'on veut, bien sûr. -->
<!-- les chemins sont relatif au dossier .ortfo du projet (donc si on veut l'image qui est à `/logo.png` à la racine du dépôt, par exemple, on met `../logo.png` comme chemin) -->
```

Pour plus d'infos, voir [ortfo/db](https://github.com/ortfo/db).

