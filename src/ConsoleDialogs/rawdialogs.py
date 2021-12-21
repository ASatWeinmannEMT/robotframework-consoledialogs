# -*- coding: utf-8 -*-
"""
=========================
ConsoleDialogs.rawdialogs
=========================

raw input based dialogs
"""
import functools
import sys
import textwrap

if sys.version_info < (3, 3):
    from backports.shutil_get_terminal_size import get_terminal_size
else:
    from shutil import get_terminal_size
    raw_input = input


class ConsoleIO(object):
    """Context manager and decorator that forces temporarily stdin, stdout and stderr to the console"""
    def __init__(self):
        self.mem_stdin, self.mem_stdout, self.mem_stderr = sys.stdin, sys.stdout, sys.stderr

    def __flush_out_streams(self):
        sys.stdout.flush()
        sys.stderr.flush()

    def __to_console(self):
        """Forces default IO to console"""
        self.__flush_out_streams()
        sys.stdin, sys.stdout, sys.stderr = sys.__stdin__, sys.__stdout__, sys.__stderr__

    def __to_previous(self):
        """Back to previous situation"""
        self.__flush_out_streams()
        sys.stdin, sys.stdout, sys.stderr = self.mem_stdin, self.mem_stdout, self.mem_stderr

    # Context manager
    def __enter__(self):
        self.__to_console()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__to_previous()

    # Decorator
    def __call__(self, callable_):
        @functools.wraps(callable_)
        def wrapper(*args, **kwargs):
            with self:
                return callable_(*args, **kwargs)
        return wrapper


def show_message(text):
    width = get_terminal_size().columns
    width -= 1
    text = textwrap.fill(text, width=width)
    print()
    print('-' * width)
    print(text)
    print('-' * width)


class RawMessageDialog(object):
    def __init__(self, message):
        self.message = message

    @ConsoleIO()
    def show(self):
        show_message(self.message)


class RawPassFailDialog(object):
    def __init__(self, message):
        self.message = message

    @ConsoleIO()
    def show(self):
        possible = {
            'f': False,
            'p': True
        }
        show_message(self.message)
        while True:
            result = input('[P]ass or [f]ail? [P]')
            result = result.strip().lower()
            result = possible.get(result)
            if isinstance(result, bool):
                break
        return result

class RawInputDialog(object):
    def __init__(self, message, default, hidden):
        self.message = message

    @ConsoleIO()
    def show(self):
        show_message(self.message)
        result = input('> ')
        return result

class RawSingleSelectionDialog(object):
    def __init__(self, message, *values):
        self.message = message
        self.values = values

    @ConsoleIO()
    def show(self):
        lines = [self.message]
        for i in range(0, len(self.values)):
            lines.append(str(i+1) + ": " + self.values[i])
        while True:
            message = "Select a single item from the option list by entering its number"
            show_message(message + '\r\n' + '\r\n'.join(lines))
            result = input('> ')
            try:
                intresult = int(result)
                intresult = intresult - 1
                if intresult < 0 or intresult >= len(self.values):
                    raise RuntimeError()
                return intresult
            except Exception:
                print("Invalid selection")

class RawMultiSelectionDialog(object):
    def __init__(self, message, *values):
        self.message = message
        self.values = values

    @ConsoleIO()
    def show(self):
        lines = [self.message]
        for i in range(0, len(self.values)):
            lines.append(str(i+1) + ": " + self.values[i])
        while True:
            message = "Select zero or more items from the option list by entering a comma-separated list of numbers"
            show_message(message + '\r\n' + '\r\n'.join(lines))
            result = input('> ')
            try:
                result_list = [x.strip() for x in result.split(',')]
                int_results = [(int(x)-1) for x in result_list]
                for i in int_results:
                    if i < 0 or i >= len(self.values):
                        raise RuntimeError()
                return [self.values[x] for x in int_results]
            except Exception:
                print("Invalid selection")
