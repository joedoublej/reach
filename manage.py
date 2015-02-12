#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys


if __name__ == "__main__":

    try:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reach.settings")
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    except Exception as exc:
        sys.stderr.write("Error: Can't find the file 'settings.py' or a valid settings directory or there is an error in your settings file")
        sys.exit(1)

