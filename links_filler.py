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

versions = {
    '1.20': '1.20',
    '1.19': '1.19',
    '1.18': '1.18',
    '1.17': '1.17',
    '1.16': '1.16',
    '1.15': '1.15',
    '1.12': '1.12',
}

links = {f'{v} - {l}': [] for v in versions.values() for l in loaders.values()}


def process_modrinth_file(path):
    with open(path, "r", encoding='utf-8') as mod_file:
        data = json.load(mod_file)
        for entry in data:
            version = entry['game_versions']
            loader = entry['loaders'][0]
            for v, v_alias in versions.items():
                if v in version:
                    links[f'{v_alias} - {loader}'].append(path[7:-14])


def process_curseforge_file(path):
    with open(path, "r", encoding='utf-8') as mod_file:
        data = json.load(mod_file)
        versions_data = data['data']['latestFilesIndexes']
        for entry in versions_data:
            version = entry['gameVersion']
            with contextlib.suppress(KeyError):
                loader = loaders[entry['modLoader']]
                for v, v_alias in versions.items():
                    if v in version:
                        links[f'{v_alias} - {loader}'].append(path[7:-12])


for root, dirs, files in os.walk(path):
    for file in files:
        if file == 'versions.json':
            modrinth.append(os.path.join(root, file))
        elif not any(char.isalpha() for char in file[:-5]):
            curseforge.append(os.path.join(root, file))

for mod_path in modrinth:
    process_modrinth_file(mod_path)

for curse_path in curseforge:
    process_curseforge_file(curse_path)

for key in links:
    links[key] = sorted(set(links[key]))

with open('links.json', "w", encoding='utf-8') as mod_links:
    json.dump(links, mod_links, indent=4)
