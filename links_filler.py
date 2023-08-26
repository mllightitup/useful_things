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

# you can choose other versions, but for testing I chose only modern ones
versions_to_check = ["1.20", "1.19", "1.18", "1.17", "1.16"]

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

# Search and delete keys with empty arrays and keys with the word "quilt"
keys_to_remove = [key for key, value in links.items() if value == [] or "quilt" in key]
for key in keys_to_remove:
    del links[key]

with open('links.json', "w", encoding='utf-8') as mod_links:
    json.dump(links, mod_links, indent=4)
