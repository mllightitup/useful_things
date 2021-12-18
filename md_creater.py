import json
from constants import start_list, header, footer

main = []

name_list = [link.replace('https://modrinth.com/mod/', '') for link in start_list]

for i in range(len(name_list)):
    with open(f'./mods/{name_list[i]}/{name_list[i]}.json') as mod_file, open(f'./mods/{name_list[i]}/author.json') as author_file:
        data = json.load(mod_file)
        author = json.load(author_file)

        if data['client_side'] == 'required' and data['server_side'] == 'required' or data[
            'client_side'] == 'optional' and data['server_side'] == 'optional':
            environment = 'Client Server'
        elif data['client_side'] == 'required' and data['server_side'] == 'unsupported' or data[
            'client_side'] == 'optional' and data['server_side'] == 'unsupported':
            environment = 'Client'
        elif data['client_side'] == 'unsupported' and data['server_side'] == 'required' or data[
            'server_side'] == 'optional':
            environment = 'Server'
        if len(data['donation_urls']) == 0:
            donate = 'None'
        else:
            donate = f"[Donate]({data['donation_urls']})"

        wiki = '' if data["wiki_url"] is None else f"[Wiki]({data['wiki_url']})"
        discord = '' if data["discord_url"] is None else f"[Discord]({data['discord_url']})"
        if author['name'] in [None, ""]:
            author_name = author['username']
        else:
            author_name = author['name']
        temp = f"| [{data['title']}]({start_list[i]}) | Unknown | {data['description']} | {author_name} | {environment} | {', '.join(data['categories'])} | {discord} [Github]({data['issues_url']}) {wiki} | {donate} "
        main.append(temp)

a = '\n'.join(main)

with open("performance18.md", "w", encoding='utf8') as out_file:
    out_file.write(header + a + footer)
