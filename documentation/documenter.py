from typing import Callable


class Documenter:
    """A class that keeps track of command docs"""

    def __init__(self) -> None:
        self.commands: dict[str, str] = {}

    def add_docs(self, func: Callable) -> Callable:
        """Adds the function name to the list of commands"""
        self.commands[func.__name__] = func.__doc__
        return func

    def get_keys(self) -> list[str]:
        """Returns a list of command names"""
        return list(self.commands.keys())

    def get_docs(self, command: str) -> str:
        """Returns the docstring of the command"""
        return self.commands[command]
