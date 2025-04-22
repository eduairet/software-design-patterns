from abc import ABC, abstractmethod
from enum import Enum
import re


class Language(Enum):
    RUST = "Rust"
    PYTHON = "Python"


# This is just a sample of translation rules, in real-world applications it's better to use a battle-tested library
TRANSLATION_RULES = {
    (Language.RUST, Language.PYTHON): [
        (r"fn (\w+)\((.*?)\) -> (.*?) {([^}]*)}", r"def \1(\2) -> \3:\4"),
        (r"let (\w+) = (.*?);", r"\1 = \2"),
        (r"return (.*?);", r"return \1"),
        (r"(i32|i64|u32|u64)", "int"),
    ],
    (Language.PYTHON, Language.RUST): [
        (r"def (\w+)\((.*?)\) -> (.*?):([^}]*)", r"fn \1(\2) -> \3 {\4}"),
        (r"(\w+) = ([^\n]+)\n", r"let \1 = \2;\n"),
        (r"return ([^\n]+)\n", r"return \1;\n"),
        (r"(int)", "i32"),
    ],
}


class Context:
    def __init__(self, language_from: Language, language_to: Language):
        self.language_from = language_from
        self.language_to = language_to


class Expression(ABC):
    def __init__(self, context: Context):
        self.context = context

    @abstractmethod
    def interpret(self, code: str) -> str:
        pass


class GeneralInterpreter(Expression):
    def __init__(self, context: Context):
        super().__init__(context)
        self.rules = TRANSLATION_RULES.get(
            (context.language_from, context.language_to), []
        )

    def interpret(self, code: str) -> str:
        if not self.rules:
            raise ValueError(
                f"No translation rules for {self.context.language_from} to {self.context.language_to}"
            )
        for pattern, replacement in self.rules:
            code = re.sub(pattern, replacement, code)
        return code


class RustToPythonInterpreter(GeneralInterpreter):
    def __init__(self):
        context = Context(Language.RUST, Language.PYTHON)
        super().__init__(context)


class PythonToRustInterpreter(GeneralInterpreter):
    def __init__(self):
        context = Context(Language.PYTHON, Language.RUST)
        super().__init__(context)
