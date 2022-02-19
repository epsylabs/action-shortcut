import os
import re

import requests
from actions_toolkit import core

TOKEN = os.getenv('SHORTCUT_TOKEN')


def main():
    story = core.get_input("issue")
    soft_fail = core.get_input("soft_fail")

    s = requests.Session()
    s.headers.update({'Shortcut-Token': TOKEN})

    result = s.get(f"https://api.app.shortcut.com/api/v3/stories/{story}")
    if result.status_code != 200:
        result = s.get(f"https://api.app.shortcut.com/api/v3/epics/{story}")

    if result.status_code != 200:
        if soft_fail == 'true':
            core.warning("Unable to locate given story/epic")
            return
        else:
            core.set_failed("Unable to locate given story/epic")

    result = result.json()

    title = result.get("name")

    slug = re.sub(r"\W+", "-", title.lower())
    pr_title = f"[{story}] {title}"
    if result.get("entity_type") == "bug":
        pr_branch = f"fix/{story}-{slug}"
    else:
        pr_branch = f"feature/{story}-{slug}"

    core.set_output("title", result.get("name"))
    core.set_output("type", result.get("entity_type"))
    core.set_output("subtype", result.get("story_type", "epic"))
    core.set_output("description", result.get("description"))
    core.set_output("slug", slug)
    core.set_output("link", result.get("app_url"))
    core.set_output("pr_branch", pr_branch)
    core.set_output("pr_title", pr_title)


if __name__ == "__main__":
    main()
