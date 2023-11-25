import asyncio
import aiohttp
import json
import os
from typing import List, Callable, Any, Tuple

from const import links


# MAIN ASYNCHRONOUS FUNCTION


async def fetch_data(session: aiohttp.ClientSession, url_list: List[str], url_formatter: Callable[[str], str]) -> tuple[Any]:
    """
    Asynchronously fetch data from a list of URLs using a given session and URL formatter.
    """
    tasks = [asyncio.ensure_future(get_data(session, url_formatter(url))) for url in url_list]
    return await asyncio.gather(*tasks)


async def main() -> None:
    """
    Main function to run the asynchronous data fetching and saving process.
    """
    async with aiohttp.ClientSession() as session:
        modrinth_links = [x for x in unique_links if not isinstance(x, int)]
        mods_data = await fetch_data(
            session,
            modrinth_links,
            lambda url: url.replace('https://modrinth.com/mod/', 'https://api.modrinth.com/v2/project/')
        )
        mod_ids, mod_slugs = save_mods(mods_data)

        versions_data = await fetch_data(
            session,
            mod_ids,
            lambda id: f"https://api.modrinth.com/v2/project/{id}/version"
        )
        author_ids = save_versions(versions_data, mod_slugs)

        author_data = await fetch_data(
            session,
            author_ids,
            lambda id: f"https://api.modrinth.com/v2/user/{id}"
        )
        save_authors(author_data, mod_slugs)

        headers = {
            'Accept': 'application/json',
            'x-api-key': '$2a$10$6qG/T.CNpNk12ZzxOZCwJu4/OQtEfc6e83kPHO4Qrw0AtJIf7u04q'
        }

        session.headers.update(headers)
        curseforge_ids = [x for x in unique_links if not isinstance(x, str)]
        curseforge_data = await fetch_data(
            session,
            curseforge_ids,
            lambda id: f"https://api.curseforge.com/v1/mods/{id}"
        )
        save_curseforge(curseforge_data)


# REQUESTS


async def get_data(session: aiohttp.ClientSession, url: str) -> Any:
    """
    Asynchronously get data from a specified URL using the provided session.
    """
    async with session.get(url) as response:
        return await response.json()


# FILE SAVE

def save_data_to_file(data: Any, filename: str, indent: int = 4) -> None:
    """
    Save the given data to a file with the specified filename.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=indent)


def save_mods(mods_data: tuple[Any]) -> Tuple[List[str], List[str]]:
    """
    Save mod data and return lists of mod IDs and slugs.
    """
    ids = [mod['id'] for mod in mods_data]
    slugs = [mod['slug'] for mod in mods_data]

    for mod in mods_data:
        filename = f"./mods/{mod['slug']}/{mod['slug']}.json"
        save_data_to_file(mod, filename)

    return ids, slugs


def save_versions(versions_data: tuple[Any], mod_slugs: List[str]) -> List[str]:
    """
    Save versions data and return a list of author IDs.
    """
    author_ids = [versions[0]["author_id"] for versions in versions_data]

    for slug, versions in zip(mod_slugs, versions_data):
        filename = f"./mods/{slug}/versions.json"
        save_data_to_file(versions, filename)

    return author_ids


def save_authors(author_data: tuple[Any], mod_slugs: List[str]) -> None:
    """
    Save author data.
    """
    for slug, author in zip(mod_slugs, author_data):
        filename = f"./mods/{slug}/author.json"
        save_data_to_file(author, filename)


def save_curseforge(curseforge_data: tuple[Any]) -> None:
    """
    Save CurseForge data.
    """
    for data in curseforge_data:
        slug = data['data']['slug']
        filename = f"./mods/{slug}/{data['data']['id']}.json"
        save_data_to_file(data, filename)


unique_links = set(sum(links.values(), []))

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
