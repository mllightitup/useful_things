import asyncio
import json
import os

import aiohttp

from constants import links

unique_links = []
for value in links.values():
    unique_links.extend(value)
unique_links = set(unique_links)


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for unique_link in unique_links:
            task = asyncio.ensure_future(get_mod_data(session, unique_link))
            tasks.append(task)
        mods_data = await asyncio.gather(*tasks)

    print(f'Number of mods: {len(mods_data)}')
    for mod in mods_data:
        if isinstance(mod['id'], int):
            filename = f"./mods/{mod['id']}/{mod['id']}.json"  # TODO: normalize structure
        else:
            filename = f"./mods/{mod['slug']}/{mod['slug']}.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding='utf-8') as mod_file:
            json.dump(mod, mod_file, ensure_ascii=False, indent=4)

    async with aiohttp.ClientSession() as session:
        tasks.clear()
        unique_links_modrinth = [x for x in unique_links if not isinstance(x, int)]
        for item in unique_links_modrinth:
            slug = item.replace('https://modrinth.com/mod/', '')
            filepath = f"./mods/{slug}/{slug}.json"
            with open(filepath, "r", encoding='utf-8') as mod_file:
                mod_json = json.load(mod_file)
                for i in range(len(mod_json['versions'])):
                    version_link = f"https://api.modrinth.com/api/v1/version/{mod_json['versions'][i]}"
                    task = asyncio.ensure_future(get_version_data(session, version_link))
                    tasks.append(task)
                version_data = await asyncio.gather(*tasks)
                for version in version_data:
                    version_path = f"./mods/{slug}/versions/{version['id']}.json"
                    os.makedirs(os.path.dirname(version_path), exist_ok=True)
                    with open(version_path, "w", encoding='utf-8') as version_file:
                        json.dump(version, version_file, ensure_ascii=False, indent=4)


async def get_mod_data(session, link):
    try:
        url = link.replace('https://modrinth.com/mod/', 'https://api.modrinth.com/api/v1/mod/')
    except (TypeError, AttributeError):
        url = f"https://addons-ecs.forgesvc.net/api/v2/addon/{link}"
    async with session.get(url) as response:
        mod_data = await response.json()
        return mod_data


async def get_version_data(session, link):
    async with session.get(link) as response:
        version_data = await response.json()
        return version_data


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
