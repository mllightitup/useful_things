# Useful Things

## Changelog
- 25.11.2023 Updated get_all_data.py to improve readability(docstrings, typehints, refactoring) and got rid of unnecessary code.
- 27.08.2023 Made necessary changes to maintain stable operation in the future and on other PCs!

## TODO:
### Done:

1. Update const.py to the newest template and delete unnecessary
2. Async requests
3. Curseforge API
4. Modrinth API v2
5. Version and loader check(everything is prepared)
6. Create all files in md_creator at once for each version and loader
7. md_creator based on checking the general list of mods and their versions, rather than manually filling in the list of mods for each individual version


### Future plans:
1. ``const.py`` rework
2. Custom data(Performance Improvement, wiki, discord for curseforge)(Incompatibility everywhere)
prepare template for maintainer
4. Authors REWORK(replace authors -> teams)

### 🛠️ How to use?:
Download the files (``get_all_data.py``, ``links_filler.py``, ``md_creator.py``, ``const.py``) and extract them to a convenient folder.
Then run them in this order:
1. ``get_all_data.py``
2. ``links_filler.py``
3. ``md_creator.py``

After that in this directory there will be a file ``links.json`` and also a folder ``performane`` containing md files for each specified version and modloader!
