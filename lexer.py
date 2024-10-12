from enum import Enum


class TokenType(Enum):
    OPEN_CURLY_BRACKET = 1
    CLOSED_CURLY_BRACKET = 2
    OPEN_SQUARE_BRACKET = 3
    CLOSED_SQUARE_BRACKET = 4
    SEMI_COLON = 5
    DOUBLE_QUOTE = 11
    NUMBER = 6
    BOOL = 7
    TEXT = 8
    SKIP = 9
    COMMA = 10


class LexerException(Exception):

    def __init__(self, message:str) -> None:
        super().__init__(message)


class Token:

    def __init__(self, token_type: TokenType, value) -> None:
        assert type(value) in [int, float, str, bool], "Error value {}".format(value)

        self.type: TokenType = token_type
        self.value = value

    def __str__(self) -> str:
        return f"Token<{self.value} : {self.type}>"

    def __repr__(self) -> str:
        return f"Token<{self.value} : {self.type}>"


def tokenize(source: str) -> list[Token]:

    tokens: list[Token] = []
    addToken = tokens.append

    while len(source):

        print(source)

        result, source = check_source_for_str(source)
        if result is not None:
            addToken(result)
            continue

        result, source = check_source_for_number(source)
        if result is not None:
            addToken(result)
            continue

        result, source = check_source_for_bool(source)
        if result is not None:
            addToken(result)
            continue

        result, source = check_source_for_skip(source)
        if result is not None:
            addToken(result)
            continue

        result, source = check_source_for_brackets(source)
        if result is not None:
            addToken(result)
            continue

        raise LexerException("Unexpected Character {}".format(source[0]))

    return tokens


def check_source_for_str(source: str):

    DOUBLE_QUOTE = '"'

    if source[0] != DOUBLE_QUOTE:
        return None, source

    source = source[1:]

    result = ""
    for c in source:
        if c == DOUBLE_QUOTE:
            result_offset = len(result) + 1
            return Token(TokenType.TEXT, result), source[result_offset:]
        else:
            result += c

    raise LexerException("Not closing quotes")


def check_source_for_number(source: str):

    NUMBER_CHAR = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "e", "."]

    if not source[0].isdigit():
        return None, source

    result = ""
    for c in source:
        if c in NUMBER_CHAR:
            result += c
        else:
            break

    try:
        result_offset = len(result)
        source = source[result_offset:]

        if "." in result:
            result = Token(TokenType.NUMBER, float(result))
        else:
            result = Token(TokenType.NUMBER, int(result))

        return result, source

    except Exception as e:
        raise LexerException("Incorrect number format") from e


def check_source_for_bool(source: str):

    result = None

    if source.startswith("true"):
        result_offset = len("true")
        source = source[result_offset:]
        result = Token(TokenType.BOOL, True)

    elif source.startswith("false"):
        result_offset = len("false")
        source = source[result_offset:]
        result = Token(TokenType.BOOL, False)

    return result, source


def check_source_for_skip(source: str):

    SKIP_VALUE = (" ", "\t", "\n")
    result = None

    if source.startswith(SKIP_VALUE):
        result_offset = 1
        result = Token(TokenType.SKIP, source[0])
        source = source[result_offset:]

    return result, source


def check_source_for_brackets(source: str):

    SEPARATORS = ("{", "}", "[", "]", ":")
    result = None

    if source.startswith("{"):
        result = Token(TokenType.OPEN_CURLY_BRACKET, source[0])
    elif source.startswith("}"):
        result = Token(TokenType.CLOSED_CURLY_BRACKET, source[0])

    elif source.startswith("["):
        result = Token(TokenType.OPEN_SQUARE_BRACKET, source[0])
    elif source.startswith("]"):
        result = Token(TokenType.CLOSED_SQUARE_BRACKET, source[0])

    elif source.startswith(":"):
        result = Token(TokenType.SEMI_COLON, source[0])

    if source.startswith(SEPARATORS):
        result_offset = 1
        source = source[result_offset:]

    return result, source
