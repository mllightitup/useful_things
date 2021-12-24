import asyncio
import json
import os

import aiohttp

from constants import start_list as links


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for link in links:
            task = asyncio.ensure_future(get_mod_data(session, link))
            tasks.append(task)
        mods_data = await asyncio.gather(*tasks)

    print(f'Number of mods: {len(mods_data)}')
    for mod in mods_data:
        filename = f"./mods/{mod['slug']}/{mod['slug']}.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding='utf-8') as mod_file:
            json.dump(mod, mod_file, ensure_ascii=False, indent=4)


async def get_mod_data(session, link):
    url = link.replace('https://modrinth.com/mod/', 'https://api.modrinth.com/api/v1/mod/')
    async with session.get(url) as response:
        result_data = await response.json()
        return result_data


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
