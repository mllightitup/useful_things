import json
import os

from const import header, footer

with open('links.json') as json_file:
    links = json.load(json_file)

path = r"C:\Users\Grishin\Desktop\useful_things-main\mods"


def fill_lines(mods_list):
    lines = []
    # print(f"{mods_list}\n")
    for mod in mods_list:
        mod_path = f"{path}/{mod}/{mod}.json"
        author_path = f"{path}/{mod}/author.json"
        if os.path.exists(mod_path) or os.path.exists(author_path):
            with open(mod_path, "r", encoding='utf-8') as mod_file, \
                    open(author_path, "r", encoding='utf-8') as author_file:
                mod_json = json.load(mod_file)
                author_json = json.load(author_file)
                if mod_json['client_side'] == 'required' and mod_json['server_side'] == 'required' or mod_json[
                    'client_side'] == 'optional' and mod_json['server_side'] == 'optional':
                    environment = 'Both'
                elif mod_json['client_side'] == 'required' and mod_json['server_side'] == 'unsupported' or mod_json[
                    'client_side'] == 'optional' and mod_json['server_side'] == 'unsupported':
                    environment = 'Client'
                elif mod_json['client_side'] == 'unsupported' and mod_json['server_side'] == 'required' or mod_json[
                    'server_side'] == 'optional':
                    environment = 'Server'

                wiki = '' if mod_json["wiki_url"] is None else f"[Wiki]({mod_json['wiki_url']})"
                discord = '' if mod_json["discord_url"] is None else f"[Discord]({mod_json['discord_url']})"

                if author_json['name'] in [None, ""]:
                    author_name = author_json['username']
                else:
                    author_name = author_json['name']

                line = f"| [{mod_json['title'].capitalize()}](https://modrinth.com/mod/{mod}) | {mod_json['description']} | {author_name} | {environment} | {discord} [Github]({mod_json['issues_url']}) {wiki}"
                lines.append(line)
        else:
            cf_file = os.listdir(f"{path}/{mod}")
            cf_file_path = f"{path}/{mod}/{cf_file[0]}"
            with open(cf_file_path, "r", encoding='utf-8') as file:
                cf_mod_json = json.load(file)
                issue = cf_mod_json['data']['links']['issuesUrl'] if 'issuesUrl' in cf_mod_json['data']['links'] else ''
                #print(issue, cf_mod_json['data']['name'])
                if issue is None:
                    print(cf_mod_json['data']['name'])
                    issue = cf_mod_json['data']['links']['sourceUrl']

                if (
                        'wikiUrl' in cf_mod_json['data']['links']
                        and cf_mod_json['data']['links']['wikiUrl'] is None
                        or 'wikiUrl' not in cf_mod_json['data']['links']
                ):
                    wiki = ""
                else:
                    wiki = cf_mod_json['data']['links']['wikiUrl']
                discord = ''
                environment = 'custom_data'
                line = f"| [{cf_mod_json['data']['name']}]({cf_mod_json['data']['links']['websiteUrl']}) | {cf_mod_json['data']['summary']} | {cf_mod_json['data']['authors'][0]['name']} | {environment} | {discord} [Github]({issue}) {wiki}"
                lines.append(line)
    return lines


for key, value in links.items():
    version_loader = key.split(' - ')
    cf_mr = '\n'.join(fill_lines(value))
    md_path = f"./performance/{key}.md"
    os.makedirs(os.path.dirname(md_path), exist_ok=True)
    with open(md_path, "w", encoding='utf8') as out_file:
        header1 = header.replace('{versions}', f'{version_loader[0]}').replace('{loaders}', f'{version_loader[1].capitalize()}')
        out_file.write(header1 + cf_mr + footer)