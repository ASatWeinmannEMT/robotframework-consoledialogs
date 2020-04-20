# -*- coding: utf-8 -*-
"""
=======================
ConsoleDialogs.keywords
=======================

Provide the keywords
"""
try:
    import curses
    curses_available = True
    from ConsoleDialogs.cursesdialogs import CursesMessageDialog, CursesPassFailDialog, CursesInputDialog
except ImportError:
    logger.warn("Failed to load curses module - falling back to raw input mode")
    curses_available = False

from ConsoleDialogs.rawdialogs import RawMessageDialog, RawPassFailDialog, RawInputDialog, RawSingleSelectionDialog

class ConsoleKeywords(object):

    def pause_execution(self, message="Test execution paused. Press OK to continue."):
        """Pauses test execution until user clicks ``Ok`` button.

        ``message`` is the message shown in the dialog.
        """
        if curses_available:
            CursesMessageDialog(message).show()
        else:
            RawMessageDialog(message).show()

    def execute_manual_step(self, message, default_error=""):
        """Pauses test execution until user sets the keyword status.

        User can press either ``PASS`` or ``FAIL`` button. In the latter case execution
        fails and an additional dialog is opened for defining the error message.

        ``message`` is the instruction shown in the initial dialog and
        ``default_error`` is the default value shown in the possible error message
        dialog.
        """
        if curses_available:
            pf_dialog = CursesPassFailDialog(message)
            pf_dialog.show()
            result = pf_dialog.get_result()
        else:
            result = RawPassFailDialog(message).show()

        if not result:
            if curses_available:
                CursesMessageDialog(default_error).show()
            else:
                RawMessageDialog(default_error).show()
            raise AssertionError("User selected FAIL when executing manual step")

    def get_value_from_user(self, message, default_value="", hidden=False):
        """Pauses test execution and asks user to input a value.

        Value typed by the user, or the possible default value, is returned.
        Returning an empty value is fine, but pressing ``Cancel`` fails the keyword.

        ``message`` is the instruction shown in the dialog and ``default_value`` is
        the possible default value shown in the input field.

        If ``hidden`` is given a true value, the value typed by the user is hidden.
        ``hidden`` is considered true if it is a non-empty string not equal to
        ``false``, ``none`` or ``no``, case-insensitively. If it is not a string,
        its truth value is got directly using same
        [http://docs.python.org/library/stdtypes.html#truth|rules as in Python].

        Example:
        | ${username} = | Get Value From User | Input user name | default    |
        | ${password} = | Get Value From User | Input password  | hidden=yes |

        Considering strings ``false`` and ``no`` to be false is new in RF 2.9
        and considering string ``none`` false is new in RF 3.0.3.
        """
        if curses_available:
            input_dialog = CursesInputDialog(message, default_value, hidden)
            input_dialog.show()
            return input_dialog.get_result()
        else:
            input_dialog = RawInputDialog(message, default_value, hidden)
            return input_dialog.show()

    def get_selection_from_user(self, message, *values):
        """Pauses test execution and asks user to select a value.

        The selected value is returned. Pressing ``Cancel`` fails the keyword.

        ``message`` is the instruction shown in the dialog and ``values`` are
        the options given to the user.

        Example:
        | ${user} = | Get Selection From User | Select user | user1 | user2 | admin |
        """
        # Currently only supported by raw dialog mode
        dialog = RawSingleSelectionDialog(message, *values)
        return dialog.show()

    def get_selections_from_user(self, message, *values):
        """Pauses test execution and asks user to select multiple values.

        The selected values are returned as a list. Selecting no values is OK
        and in that case the returned list is empty. Pressing ``Cancel`` fails
        the keyword.

        ``message`` is the instruction shown in the dialog and ``values`` are
        the options given to the user.

        Example:
        | ${users} = | Get Selections From User | Select users | user1 | user2 | admin |

        New in Robot Framework 3.1.
        """
        # Currently only supported by raw dialog mode
        dialog = RawMultiSelectionDialog(message, *values)
        return dialog.show()
