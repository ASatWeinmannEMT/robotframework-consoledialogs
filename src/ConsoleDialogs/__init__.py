# -*- coding: utf-8 -*-
"""
==============
ConsoleDialogs
==============

A pure console replacement for the Robot Framework Dialogs library.
"""
import pkg_resources
import os

from robot.api import logger

from ConsoleDialogs.keywords import ConsoleKeywords

# PEP 396 style version marker
try:
    __version__ = pkg_resources.get_distribution('robotframework-consoledialogs').version
except Exception:
    logger.warn("Could not get the package version from pkg_resources")
    __version__ = 'unknown'

class ConsoleDialogs(ConsoleKeywords):
    """A test library providing dialogs for interacting with users.

    `ConsoleDialogs` is a replacement for the `Dialogs` Robot Framework's
    standard library that provides means for pausing the test execution and
    getting input from users. The dialogs are slightly different depending on
    are tests run on Python or Jython but they provide the same functionality.
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_DOC_FORMAT = 'ROBOT'
    ROBOT_LIBRARY_VERSION = __version__
