import asyncio
import os
import re

from actions_toolkit import core
from clubhouse_api import ClubHouse
import clubhouse_api.exceptions

TOKEN = os.getenv('SHORTCUT_TOKEN')

club_house_session = ClubHouse(TOKEN, 'v3')
club_house = club_house_session.get_api()


async def main():
    story = core.get_input("story")

    core.info("Starting image scan")

    result = None
    try:
        result = await club_house.stories.get(story)
    except clubhouse_api.exceptions.ApiError as e:
        if e.code_error == 401:
            core.set_failed("Invalid Shortcut Token")

        try:
            result = await club_house.epics.get(story)
        except clubhouse_api.exceptions.ApiError:
            pass

    if not result:
        core.set_failed("Unable to locate given story/epic")

    title = result.get("name")

    core.set_output("title", result.get("name"))
    core.set_output("type", result.get("entity_type"))
    core.set_output("description", result.get("description"))
    core.set_output("slug", re.sub(r"\W+", "-", title.lower()))
    core.set_output("link", result.get("app_url"))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
