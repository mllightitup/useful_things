import contextlib
import json
import os

path = r"C:\Users\Grishin\Desktop\useful_things-main\mods"
modrinth = []
curseforge = []
versions = {
    '1.19': '1.19',
    '1.18': '1.18',
    '1.17': '1.17',
    '1.16': '1.16',
    '1.15': '1.15',
    '1.12': '1.12',
}

loaders = {
    1: 'forge',
    4: 'fabric',
    'fabric': 'fabric',
    'forge': 'forge',
    'quilt': 'quilt'
}

links = {
    '1.19 - quilt': [],
    '1.18 - quilt': [],
    '1.19 - fabric': [],
    '1.18 - fabric': [],
    '1.17 - fabric': [],
    '1.16 - fabric': [],
    '1.15 - fabric': [],
    '1.12 - fabric': [],
    '1.19 - forge': [],
    '1.18 - forge': [],
    '1.17 - forge': [],
    '1.16 - forge': [],
    '1.15 - forge': [],
    '1.12 - forge': [],
}
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
            if any("1.19" in s for s in version):
                links[f'1.19 - {loader[0]}'] += [path[49:-14]]
            if any("1.18" in s for s in version):
                links[f'1.18 - {loader[0]}'] += [path[49:-14]]
            if any("1.17" in s for s in version):
                links[f'1.17 - {loader[0]}'] += [path[49:-14]]
            if any("1.16" in s for s in version):
                links[f'1.16 - {loader[0]}'] += [path[49:-14]]
            if any("1.15" in s for s in version):
                links[f'1.15 - {loader[0]}'] += [path[49:-14]]
            if any("1.12" in s for s in version):
                links[f'1.12 - {loader[0]}'] += [path[49:-14]]

for path in curseforge:
    with open(path, "r", encoding='utf-8') as mod_file:
        versions = json.load(mod_file)['data']['latestFilesIndexes']
        for k in range(len(versions)):
            version = versions[k]['gameVersion']
            with contextlib.suppress(KeyError):
                loader = versions[k]['modLoader']
                if '1.19' in version:
                    links[f'1.19 - {loaders[loader]}'] += [path[49:-12]]
                if '1.18' in version:
                    links[f'1.18 - {loaders[loader]}'] += [path[49:-12]]
                if '1.17' in version:
                    links[f'1.17 - {loaders[loader]}'] += [path[49:-12]]
                if '1.16' in version:
                    links[f'1.16 - {loaders[loader]}'] += [path[49:-12]]
                if '1.15' in version:
                    links[f'1.15 - {loaders[loader]}'] += [path[49:-12]]
                if '1.12' in version:
                    links[f'1.12 - {loaders[loader]}'] += [path[49:-12]]
for key in links:
    links[key] = sorted(set(links[key]))

with open('links.json', "w", encoding='utf-8') as mod_links:
    json.dump(links, mod_links, indent=4)
