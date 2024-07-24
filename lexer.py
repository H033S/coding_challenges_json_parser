from enum import Enum
from functools import partial


class TokenType(Enum):
    OPEN_CURLY_BRACKET = 1
    CLOSED_CURLY_BRACKET = 2
    OPEN_SQUARE_BRACKET = 3
    CLOSED_SQUARE_BRACKET = 4
    SEMI_COLON = 5
    NUMBER = 6
    BOOL = 7
    TEXT = 8
    SKIP = 9
    DOUBLE_QUOTE = 10


class Token:

    def __init__(self, type: TokenType, value: str) -> None:
        self.type: TokenType = type
        self.value: str = value

    def __str__(self) -> str:
        return f"Token<{self.value} : {self.type}>"

    def __repr__(self) -> str:
        return f"Token<{self.value} : {self.type}>"


def getTokenForMultiChar(multi_char_value: str) -> Token:
    if multi_char_value in ["true", "false"]:
        return Token(TokenType.BOOL, multi_char_value)
    elif multi_char_value.replace(".", "").isdecimal():
        return Token(TokenType.NUMBER, multi_char_value)
    else:
        return Token(TokenType.TEXT, multi_char_value)


def tokenize(source: str) -> list[Token]:

    tokens: list[Token] = []
    addToken = tokens.append
    multi_char_value: str = ""

    def addMultiCharTokenIfExist():
        nonlocal multi_char_value
        if multi_char_value:
            addToken(getTokenForMultiChar(multi_char_value))
            multi_char_value = ""

    for current_char in source:
        newToken = partial(Token, value=current_char)

        if current_char == "{":
            addMultiCharTokenIfExist()
            addToken(newToken(TokenType.OPEN_CURLY_BRACKET))
        elif current_char == "}":
            addMultiCharTokenIfExist()
            addToken(newToken(TokenType.CLOSED_CURLY_BRACKET))
        elif current_char == "[":
            addMultiCharTokenIfExist()
            addToken(newToken(TokenType.OPEN_SQUARE_BRACKET))
        elif current_char == "]":
            addMultiCharTokenIfExist()
            addToken(newToken(TokenType.CLOSED_SQUARE_BRACKET))
        elif current_char == ":":
            addMultiCharTokenIfExist()
            addToken(newToken(TokenType.SEMI_COLON))
        elif current_char == '"':
            addMultiCharTokenIfExist()
            addToken(newToken(TokenType.DOUBLE_QUOTE))
        elif current_char in [" ", "\t", "\n"]:
            addMultiCharTokenIfExist()
            addToken(newToken(TokenType.SKIP))
        else:
            if current_char.isalpha():
                multi_char_value += current_char
            elif current_char.isdecimal() or current_char == ".":
                multi_char_value += current_char
            else:
                raise Exception("Not Supported Character")
            continue
    else:
        addMultiCharTokenIfExist()

    return tokens
