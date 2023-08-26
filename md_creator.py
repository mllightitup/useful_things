import json
import os
from const import header, footer


def get_environment(client_side, server_side):
    if client_side == server_side:
        if client_side in ('required', 'optional'):
            return 'Both'
        elif client_side == 'unsupported':
            return 'Server'
    elif client_side == 'required' and server_side == 'unsupported':
        return 'Client'
    elif client_side == 'unsupported' and server_side == 'required':
        return 'Server'
    return 'custom_data'


def get_links_info(mod_json):
    wiki = f"[Wiki]({mod_json['wiki_url']})" if mod_json["wiki_url"] else ''
    discord = f"[Discord]({mod_json['discord_url']})" if mod_json["discord_url"] else ''
    return wiki, discord


def get_author_name(author_json):
    if author_json['name'] in (None, ""):
        return author_json['username']
    return author_json['name']


def process_mod(mod_path, author_path):
    lines = []

    with open(mod_path, "r", encoding='utf-8') as mod_file, \
            open(author_path, "r", encoding='utf-8') as author_file:

        mod_json = json.load(mod_file)
        author_json = json.load(author_file)

        environment = get_environment(mod_json['client_side'], mod_json['server_side'])

        wiki, discord = get_links_info(mod_json)
        author_name = get_author_name(author_json)

        line = f"| [{mod_json['title'].capitalize()}](https://modrinth.com/mod/{mod_json['slug']}) | {mod_json['description']} | {author_name} | {environment} | {discord} [Github]({mod_json['issues_url']}) {wiki}"
        lines.append(line)

    return lines


def process_curseforge(cf_mod_json):
    lines = []
    discord = ''
    environment = 'custom_data'

    issue = f"[Github]({cf_mod_json['data']['links']['sourceUrl']})"

    if cf_mod_json['data']['links']['sourceUrl'] is None:
        issue = f"[Github]({cf_mod_json['data']['links']['issuesUrl']})"

    wiki = f"[Wiki]({cf_mod_json['data']['links']['wikiUrl']})" if cf_mod_json['data']['links']['wikiUrl'] else ''

    line = f"| [{cf_mod_json['data']['name']}]({cf_mod_json['data']['links']['websiteUrl']}) | {cf_mod_json['data']['summary']} | {cf_mod_json['data']['authors'][0]['name']} | {environment} | {discord} {issue} {wiki}"
    lines.append(line)
    return lines


def fill_lines(mods_list, path):
    lines = []

    for mod in mods_list:
        mod_path = f"{path}/{mod}/{mod}.json"
        author_path = f"{path}/{mod}/author.json"

        if os.path.exists(mod_path) or os.path.exists(author_path):
            lines.extend(process_mod(mod_path, author_path))
        else:
            cf_file = os.listdir(f"{path}/{mod}")
            cf_file_path = f"{path}/{mod}/{cf_file[0]}"

            with open(cf_file_path, "r", encoding='utf-8') as file:
                cf_mod_json = json.load(file)
                lines.extend(process_curseforge(cf_mod_json))

    return lines


with open('links.json') as json_file:
    links = json.load(json_file)

path = r"./mods"

for key, value in links.items():
    version_loader = key.split(' - ')
    cf_mr = '\n'.join(fill_lines(value, path))
    md_path = f"./performance/{key.replace(' ', '')}.md"
    os.makedirs(os.path.dirname(md_path), exist_ok=True)
    with open(md_path, "w", encoding='utf8') as out_file:
        header1 = header.replace('{versions}', f'{version_loader[0]}').replace('{loaders}',
                                                                               f'{version_loader[1].capitalize()}')
        out_file.write(header1 + cf_mr + footer)
