import glob
import json
import os

import author as author

from const import links, header, footer


def curseforge(values):
    lines = []
    path = "./mods/"
    curseforge_values = [x for x in values if not isinstance(x, str)]
    for value in curseforge_values:
        text_files = glob.glob(path + f"/**/{value}.json", recursive=True)
        with open(text_files[0], "r", encoding='utf-8') as file:
            mod_json = json.load(file)
            issue = mod_json['issueTrackerUrl'] if 'issueTrackerUrl' in mod_json else ''
            if (
                    'wikiUrl' in mod_json
                    and mod_json['wikiUrl'] == ""
                    or 'wikiUrl' not in mod_json
            ):
                wiki = ""
            else:
                wiki = mod_json['wikiUrl']
            discord = ''
            environment = 'custom_data'
            line = f"| [{mod_json['name']}]({mod_json['websiteUrl']}) | {mod_json['summary']} | {mod_json['authors'][0]['name']} | {environment} | {discord} [Github]({issue}) {wiki}"
            lines.append(line)
    return lines


def modrinth(values):
    lines = []
    path = "./mods/"
    modrinth_values = [x for x in values if not isinstance(x, int)]
    for link in modrinth_values:
        slug = link.replace('https://modrinth.com/mod/', '')
        mod_path = glob.glob(path + f"/**/{slug}.json", recursive=True)
        author_path = glob.glob(path + f'/{slug}/author.json', recursive=True)
        with open(mod_path[0], "r", encoding='utf-8') as mod_file, \
                open(author_path[0], "r", encoding='utf-8') as author_file:
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

            line = f"| [{mod_json['title']}]({link}) | {mod_json['description']} | {author_name} | {environment} | {discord} [Github]({mod_json['issues_url']}) {wiki}"
            lines.append(line)
    return lines


def md_create(version, loader):
    for keys, values in links.items():
        if version in keys and loader in keys:
            cf_lines = curseforge(values)
            mr_lines = modrinth(values)
            # print(cf_lines)
            # print(mr_lines)
            cf = '\n'.join(cf_lines)
            mr = '\n'.join(mr_lines)
            path = f"./performance/{keys}.md"
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding='utf8') as out_file:
                header1 = header.replace('{versions}', f'{version}').replace('{loaders}', f'{loader.capitalize()}')
                out_file.write(header1 + mr + cf + footer)


if __name__ == '__main__':
    md_create('1.18.x', 'fabric')
    md_create('1.18.x', 'forge')
    md_create('1.17.x', 'fabric')
    md_create('1.17.x', 'forge')


# any(x in keys for x in versions) and any(x in keys for x in loaders):