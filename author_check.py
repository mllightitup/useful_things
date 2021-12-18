import json
from os import listdir
from os.path import join, isfile
from constants import start_list

import requests

name_list = [link.replace('https://modrinth.com/mod/', '') for link in start_list]

for i in range(len(start_list)):
    mypath = f'./mods/{name_list[i]}/versions/'
    file_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    filename = f'./mods/{name_list[i]}/author.json'
    with open(mypath + file_list[0], "r", encoding='utf-8') as mod_file, open(f'./mods/{name_list[i]}/author.json', "w", encoding='utf-8') as author_file:
        data = json.load(mod_file)
        author_json = requests.get(f"https://api.modrinth.com/api/v1/user/{data['author_id']}").json()
        json.dump(author_json, author_file, ensure_ascii=False, indent=4)
