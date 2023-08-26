import contextlib
import json
import os

path = r"./mods"
modrinth = []
curseforge = []

loaders = {
    1: 'forge',
    4: 'fabric',
    'fabric': 'fabric',
    'forge': 'forge',
    'quilt': 'quilt'
}

versions_to_check = ["1.20", "1.19", "1.18", "1.17", "1.16", "1.15", "1.14", "1.13", "1.12", "1.11", "1.10", "1.9", "1.8" ,"1.7"]

links = {f'{ver} - {loader}': [] for ver in versions_to_check for loader in loaders.values()}

for root, dirs, files in os.walk(path):
    for file in files:
        if file == 'versions.json':
            modrinth.append(os.path.join(root, file))
        elif not any(char.isalpha() for char in file[:-5]):
            curseforge.append(os.path.join(root, file))

for path in modrinth:
    with open(path, "r", encoding='utf-8') as mod_file:
        x = json.load(mod_file)
        for j in range(len(x)):
            version = x[j]['game_versions']
            loader = x[j]['loaders']
            for ver in versions_to_check:
                if any(ver in s for s in version):
                    links[f'{ver} - {loader[0]}'] += [path[7:-14]]

for path in curseforge:
    with open(path, "r", encoding='utf-8') as mod_file:
        versions = json.load(mod_file)['data']['latestFilesIndexes']
        for k in range(len(versions)):
            version = versions[k]['gameVersion']
            with contextlib.suppress(KeyError):
                loader = versions[k]['modLoader']
                for ver in versions_to_check:
                    if ver in version:
                        links[f'{ver} - {loaders[loader]}'] += [path[7:-12]]

for key in links:
    links[key] = sorted(set(links[key]))

keys_to_remove = [key for key, value in links.items() if value == []]
for key in keys_to_remove:
    del links[key]

with open('links.json', "w", encoding='utf-8') as mod_links:
    print(links)
    json.dump(links, mod_links, indent=4)
