#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
LOCAL_FILE = lambda *path: os.path.join(PROJECT_ROOT, *path)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.active")

    from django.core.management import execute_from_command_line

    SETTINGS_ACTIVE_CONTENTS = (
        "\033[1;32mfrom settings.local import *\033[1;33m")

    if not os.path.exists(LOCAL_FILE('settings', 'active.py')):
        print('\033[1;33m')
        print("Apparently you don't have the file "
              "\033[1;37msettings/active.py\033[1;33m yet.")
        print("Create it containing '{}'\033[0m".format(SETTINGS_ACTIVE_CONTENTS))
        print()
        sys.exit(1)

    sys.path.insert(0, LOCAL_FILE('..'))
    sys.path.insert(0, LOCAL_FILE('apps'))

    execute_from_command_line(sys.argv)
