#!/usr/bin/env python3

#
# Tumbed - A simple bot for testing out the limitations of typed interactions with the GitHub API v3.
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org>
#

from datetime import datetime, timedelta
import traceback
import os
import json
import github
import jinja2
import sched
import time

Username = None
Password = None

def manual(gh, repos, target):
    for repo in repos:
        ghRepo = gh.get_repo(repo)
        since = datetime.now() - timedelta(days=1)

        print(" => Scanning {}".format(ghRepo.full_name))

        comments = ghRepo.get_issues_comments(sort = "updated", since = since)
        for comment in comments:
            if comment.user.name == target:
                # Find a way to add a reaction to the comment vote, looks like PyGitHub
                # Looks like PyGithub doesn't support reactions at the moment as it went inactive
                # before reactions were introduced on comments.
                # Regarding: PyGithub/PyGithub#649

                print("  => Comment {} is from {}. Downvoting!".format(page.id, target))

def configure():
    try:
        Username = os.environ["TUMBED_USERNAME"]
        Password = os.environ["TUMBED_PASSWORD"]
    except:
        print(" => An error occured while getting settings for Tumbed.")
        return False

    return True

def periodic(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, periodic,
                    (scheduler, interval, action, actionargs))
    action(*actionargs)

def main():
    if configure() is False:
        return -1

    print("=> Logging into GitHub...")

    gh = github.Github(Username, Password)

    print("=> Logged in as {}.".format(Username))

    repos = [
        "ValveSoftware/portal2",
        "ValveSoftware/Dota-2-Vulkan",
        "ValveSoftware/Dota-2",
        "ValveSoftware/Source-1-Games",
        "ValveSoftware/steam-for-linux",
        "ValveSoftware/SteamOS",
        "ValveSoftware/csgo-osx-linux",
        "ValveSoftware/SteamVR-for-Linux"
    ]
    target = "kisak-valve"

    scheduler = sched.scheduler(time.time, time.sleep)

    print( "=> Starting scheduler.")

    periodic(scheduler, 60, manual, (gh, repos, target))

    print("=> Hello and welcome to Tumbed.")

    return 0

if __name__ == "__main__":
    exit(main())
