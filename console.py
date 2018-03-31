"""
The console is a wrapper around the cli.py client, and provides an interactive terminal.
"""
from __future__ import unicode_literals

import sys
import threading

import fire

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from cli import ArsenalClient
from pyclient import Target, Group

class ArsenalCompleter(Completer): # pylint: disable=too-few-public-methods
    """
    A completer specific to the Arsenal API.
    """
    _api_methods = {}
    _api_completers = {}
    _names = []
    def __init__(self):
        """
        Constructor for the completer, used to gather API information.
        """
        self._api_methods = list(filter(lambda x: not x.startswith('_'), dir(ArsenalClient)))

        self._names = [target.name for target in Target.list_targets(include_status=False)]
        self._names += [group.name for group in Group.list_groups()]

        self.api_completer = WordCompleter(self._api_methods)
        self.name_completer = WordCompleter(self._names)

    def get_completions(self, document, complete_event):
        """
        A function for determining auto-complete results.
        """
        words = document.text.split(' ')
        if len(words) > 3:
            return

        if words and words[0] in self._api_methods:
            yield from (Completion(
                completion.text,
                completion.start_position,
                display=completion.display)
                        for completion
                        in self.name_completer.get_completions(document, complete_event))
        else:
            yield from (Completion(
                completion.text,
                completion.start_position,
                display=completion.display)
                        for completion
                        in self.api_completer.get_completions(document, complete_event))

class FireThread(threading.Thread):
    """
    Creates a separate thread and calls the google fire library on the Arsenal client.
    """
    def __init__(self, cmd):
        self._cmd = cmd
        threading.Thread.__init__(self)

    def run(self):
        try:
            fire.Fire(ArsenalClient, '{}'.format(self._cmd))
        except TypeError as exception:
            print(', '.join(exception.args))

def exit_arsenal():
    """
    Exit the console
    """
    print("\nThanks for using Arsenal")
    sys.exit(0)

def main():
    """
    The main entry point of the program.
    """
    history = InMemoryHistory()

    while True:
        try:
            text = prompt(
                'Arsenal >> ',
                completer=ArsenalCompleter(),
                history=history,
                auto_suggest=AutoSuggestFromHistory()
            )
            if text:
                firethread = FireThread(text)
                firethread.start()
                firethread.join()
                print('')

        except EOFError:
            exit_arsenal()
        except KeyboardInterrupt:
            exit_arsenal()
        except Exception as exception: # pylint: disable=broad-except
            print(exception)

if __name__ == '__main__':
    main()