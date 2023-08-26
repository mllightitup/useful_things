# Useful Things

# TODO:
### Done:

1. Update const.py to the newest template and delete unnecessary
2. Async requests
3. Curseforge API
4. Modrinth API v2
5. Version and loader check(everything is prepared)
6. Create all files in md_creator at once for each version and loader
7. md_creator based on checking the general list of mods and their versions, rather than manually filling in the list of mods for each individual version


### Future plans:
2. Custom data(Performance Improvement, wiki, discord for curseforge)(Incompatibility everywhere)
prepare template for maintainer
4. Authors REWORK(replace authors -> teams)

### 🛠️ How to use?:
Download the three files (``get_all_data.py``, ``links_filler.py``, ``md_creator.py``) and extract them to a convenient folder.
Then run them in this order:
1. ``get_all_data.py``
2. ``links_filler.py``
3. ``md_creator.py``

After that in this directory there will be a file ``links.json`` and also a folder ``performane`` containing md files for each specified version and modloader!
