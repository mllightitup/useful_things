import asyncio
import aiohttp
import json
import os

from const import links


# MAIN ASYNCHRONOUS FUNCTION


async def main():
    async with aiohttp.ClientSession() as session:
        unique_links_modrinth = [x for x in unique_links if not isinstance(x, int)]
        tasks = [asyncio.ensure_future(get_mod_data(session, unique_link)) for unique_link in unique_links_modrinth]
        mods_data = await asyncio.gather(*tasks)

    mod_ids, mod_slugs = save_mod(mods_data)

    async with aiohttp.ClientSession() as session:
        tasks.clear()
        tasks = [asyncio.ensure_future(get_versions_data(session, mod_id)) for mod_id in mod_ids]
        versions_data = await asyncio.gather(*tasks)

    author_ids = save_version(versions_data, mod_slugs)

    async with aiohttp.ClientSession() as session:
        tasks.clear()
        tasks = [asyncio.ensure_future(get_author_data(session, author_id)) for author_id in author_ids]
        author_data = await asyncio.gather(*tasks)

    save_author(author_data, mod_slugs)


# REQUESTS


async def get_mod_data(session, link):
    url = link.replace('https://modrinth.com/mod/', 'https://api.modrinth.com/api/v1/mod/')
    async with session.get(url) as response:
        mod_data = await response.json()
        return mod_data


async def get_versions_data(session, mod_id):
    url = f"https://api.modrinth.com/api/v1/mod/{mod_id}/version"
    async with session.get(url) as response:
        versions_data = await response.json()
        return versions_data


async def get_author_data(session, author_id):
    url = f"https://api.modrinth.com/api/v1/user/{author_id}"
    async with session.get(url) as response:
        author_data = await response.json()
        return author_data


# FILE SAVE

def save_mod(mods_data):
    slugs = []
    ids = []
    for mod in mods_data:
        filename = f"./mods/{mod['slug']}/{mod['slug']}.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding='utf-8') as mod_file:
            json.dump(mod, mod_file, ensure_ascii=False, indent=4)
            ids.append(mod['id'])
            slugs.append(mod['slug'])
    return ids, slugs


def save_version(versions_data, mod_slugs):
    author_ids = []
    for i in range(len(versions_data)):
        filename = f"./mods/{mod_slugs[i]}/versions.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding='utf-8') as versions_file:
            json.dump(versions_data[i], versions_file, ensure_ascii=False, indent=4)
            author_ids.append(versions_data[i][0]["author_id"])
    return author_ids


def save_author(author_data, mod_slugs):
    for i in range(len(author_data)):
        filename = f"./mods/{mod_slugs[i]}/author.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding='utf-8') as author_file:
            json.dump(author_data[i], author_file, ensure_ascii=False, indent=4)


unique_links = set(sum(links.values(), []))

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
