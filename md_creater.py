import json

header = """
# Performance Mods
A list of performance-enhancing mods for 1.18.x forge/fabric versions.

Any suggestions/complaints?<br>
Join our [discord](https://discord.gg/8nzHYhVUQS) or use the gist comments.<br><br>

[![Home](https://i.imgur.com/zGuelkW.png)](https://gist.github.com/NordicGamerFE/c89623db94844744b233eac717a71ca5)

## Fabric 1.18.X

| Name | Known Incompatibilities | Description | Author | Environment | [Label](https://gist.github.com/NordicGamerFE/c89623db94844744b233eac717a71ca5#threat-level) |
| --- | :---: | :---: | :---: | :---: | :---: |
"""

main = []

footer = """



[![Home](https://i.imgur.com/zGuelkW.png)](https://gist.github.com/NordicGamerFE/c89623db94844744b233eac717a71ca5)
"""

with open('mod_data.json') as data_file:
    data = json.load(data_file)
    for key, value in data.items():
        template = f"| [{key}]({value['modrinth_link']}) | Unknown | {value['description']} | {value['author']} | {value['environment']} | none |"
        main.append(template)

a = '\n'.join(main)
#print(header + a + footer)

with open("performance18.md", "w", encoding='utf8') as out_file:
    out_file.write(header + a + footer)