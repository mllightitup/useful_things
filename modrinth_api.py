import requests
import json
import os


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

start_list = [link.replace('https://modrinth.com/mod/', 'https://api.modrinth.com/api/v1/mod/') for link in start_list]

for start in start_list:
    mod_json = requests.get(start).json()
    filename = f"./mods/{mod_json['slug']}/{mod_json['slug']}.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding='utf-8') as mod_file:
        json.dump(mod_json, mod_file, ensure_ascii=False, indent=4)
        for version_id in mod_json['versions']:
            version_path = f"./mods/{mod_json['slug']}/versions/{version_id}.json"
            os.makedirs(os.path.dirname(version_path), exist_ok=True)
            version_json = requests.get(start.replace(f"mod/{mod_json['slug']}", f'version/{version_id}')).json()
            with open(version_path, "w", encoding='utf-8') as version_file:
                json.dump(version_json, version_file, ensure_ascii=False, indent=4)
