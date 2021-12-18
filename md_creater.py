import json

header = """
# Performance Mods
A list of performance-enhancing mods for 1.18.x forge/fabric versions.

Any suggestions/complaints?<br>
Join our [discord](https://discord.gg/8nzHYhVUQS) or use the issues.<br><br>

[![Home](https://i.imgur.com/zGuelkW.png)](https://github.com/NordicGamerFE/usefulmods/tree/main)
## Fabric 1.18.X

| Name | Known Incompatibilities | Description | Author | Enviroment | Categories | Need help? | Support author |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
"""

main = []

footer = """



[![Home](https://i.imgur.com/zGuelkW.png)](https://github.com/NordicGamerFE/usefulmod)
"""

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
        author_name = author['username'] if author['name'] is None else author['name']

        temp = f"| [{data['title']}]({start_list[i]}) | Unknown | {data['description']} | {author_name} | {environment} | {', '.join(data['categories'])} | {discord} [Github]({data['issues_url']}) {wiki} | {donate} "
        main.append(temp)
            # print(data['discord_url'])

a = '\n'.join(main)

with open("performance18.md", "w", encoding='utf8') as out_file:
    out_file.write(header + a + footer)