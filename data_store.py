import requests
import json

from bs4 import BeautifulSoup
from lxml import etree

data_test = {}
start_list = ['https://modrinth.com/mod/alternate-current',
              'https://modrinth.com/mod/sodium',
              'https://modrinth.com/mod/hydrogen',
              'https://modrinth.com/mod/lithium',
              'https://modrinth.com/mod/lazydfu',
              'https://modrinth.com/mod/krypton',
              'https://modrinth.com/mod/starlight',
              'https://modrinth.com/mod/ferrite-core',
              'https://modrinth.com/mod/dashloader',
              'https://modrinth.com/mod/lazy-language-loader',
              'https://modrinth.com/mod/cull-leaves',
              'https://modrinth.com/mod/better-beds',
              'https://modrinth.com/mod/smoke-suppression',
              'https://modrinth.com/mod/c2me-fabric',
              'https://modrinth.com/mod/servercore',
              'https://modrinth.com/mod/vmp-fabric',
              ]

HEADERS = ({
    'User-Agent':
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5 '
})

main = []

for start in start_list:
    URL = start + '/versions'
    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))

    mod_name = dom.xpath('//*[@id="__layout"]/div/main/div[3]/div/div/div[1]/div[2]/h1')[0].text.strip('\n')
    modrinth_link = start
    minecraft_version = dom.xpath('//*[@id="__layout"]/div/main/div[3]/div/section/div[1]/div[3]/div/p')[0].text.strip('\n')
    mod_version = dom.xpath('//*[@id="__layout"]/div/main/div[3]/div/div/div[4]/div/table/tbody/tr[1]/td[3]/a')[0].text.strip('\n')
    last_mod_update = dom.xpath('//*[@id="__layout"]/div/main/div[3]/div/div/div[4]/div/table/tbody/tr[1]/td[8]')[0].text.strip('\n')
    author = dom.xpath('//*[@id="__layout"]/div/main/div[3]/div/section/div[2]/div/div/a/h4')[0].text.strip('\n')
    description = dom.xpath('//*[@id="__layout"]/div/main/div[3]/div/div/div[1]/div[2]/p')[0].text.strip('\n')

    client = dom.xpath('//*[@id="__layout"]/div/main/div[3]/div/section/div[1]/div[5]/div/p')[0].text.strip('\n')
    server = dom.xpath('//*[@id="__layout"]/div/main/div[3]/div/section/div[1]/div[6]/div/p')[0].text.strip('\n')
    if client == 'required' and server == 'required' or client == 'optional' and server == 'optional':
        environment = 'Client / Server'
    elif client == 'required' and server == 'unsupported' or client == 'optional' and server == 'unsupported':
        environment = 'Client'
    elif client == 'unsupported' and server == 'required' or server == 'optional':
        environment = 'Server'
    temp = {
        f'{mod_name}': {
            'modrinth_link': f'{modrinth_link}',
            # 'curseforge_link': f'',
            'minecraft_version': f'{minecraft_version}',
            'mod_version': f'{mod_version}',
            'last_mod_update': f'{last_mod_update}',
            'author': f'{author}',  # static
            'description': f'{description}',
            'environment': f'{environment}'
        },
    }
    data_test.update(temp)
    print(f"{mod_name} - DONE")
    temp2 = f"| [{mod_name}]({modrinth_link}) | Unknown | {description} | {author} | {environment} | none |"
    main.append(temp2)
with open("mod_data.json", "w", encoding='utf8') as out_file:
    json.dump(data_test, out_file, indent=6, ensure_ascii=False)


