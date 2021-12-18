import json
from os import listdir
from os.path import join, isfile

import requests




start_list = [
    'https://modrinth.com/mod/starlight',
    'https://modrinth.com/mod/lazydfu',
    'https://modrinth.com/mod/smoothboot-fabric',
    'https://modrinth.com/mod/ferrite-core',
    'https://modrinth.com/mod/sodium',
    'https://modrinth.com/mod/lazy-language-loader',
    'https://modrinth.com/mod/canvas',
    'https://modrinth.com/mod/cull-leaves',
    'https://modrinth.com/mod/better-beds',
    'https://modrinth.com/mod/smoke-suppression',
    'https://modrinth.com/mod/lithium',
    'https://modrinth.com/mod/krypton',
    'https://modrinth.com/mod/c2me-fabric',
    'https://modrinth.com/mod/alternate-current',
    'https://modrinth.com/mod/servercore',
    'https://modrinth.com/mod/vmp-fabric',
    'https://modrinth.com/mod/ebe',
    'https://modrinth.com/mod/phosphor',
    'https://modrinth.com/mod/entity-distance',
    'https://modrinth.com/mod/hydrogen',
    'https://modrinth.com/mod/starlight-forge',
]
name_list = [link.replace('https://modrinth.com/mod/', '') for link in start_list]


for i in range(len(start_list)):
    mypath = f'./mods/{name_list[i]}/versions/'
    file_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    filename = f'./mods/{name_list[i]}/author.json'
    with open(mypath + file_list[0], "r", encoding='utf-8') as mod_file:
        data = json.load(mod_file)
        author_json = requests.get(f"https://api.modrinth.com/api/v1/user/{data['author_id']}").json()
        with open(f'./mods/{name_list[i]}/author.json', "w", encoding='utf-8') as author_file:
            json.dump(author_json, author_file, ensure_ascii=False, indent=4)