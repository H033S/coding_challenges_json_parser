from json_parser.operators import FieldExpression, ObjectExpression
from json_parser.lexer import Token, TokenType
from json_parser.parser import ParseException, Parser
import pytest


def test_field_expression():

    tokens = [
        Token(TokenType.TEXT, "key"),
        Token(TokenType.SEMI_COLON, ":"),
        Token(TokenType.NUMBER, 6),
        Token(TokenType.COMMA, ","),
    ]

    try:
        parse = Parser(tokens)
        parse.consumeFieldFromTokens()

        assert len(parse.stack_expression) == 1
        expression = parse.stack_expression[-1]

        assert type(expression) == FieldExpression
        assert expression.key.value == "key"
        assert expression.value.value == 6

    except Exception as exc:
        pytest.fail(reason="Unexpected Exception {}".format(exc), pytrace=True)


def test_object_expression():

    tokens = [
        Token(TokenType.OPEN_CURLY_BRACKET, "{"),
        Token(TokenType.TEXT, "key"),
        Token(TokenType.SEMI_COLON, ":"),
        Token(TokenType.NUMBER, 6),
        Token(TokenType.COMMA, ","),
        Token(TokenType.CLOSED_CURLY_BRACKET, "}"),
    ]

    try:
        parse = Parser(tokens)
        parse.parser()

        assert len(parse.stack_expression) == 1
        expression = parse.stack_expression[-1]

        assert type(expression) == ObjectExpression

    except Exception as exc:
        pytest.fail(reason="Unexpected Exception {}".format(exc), pytrace=True)


def test_empty_json():

    tokens = [
        Token(TokenType.OPEN_CURLY_BRACKET, "{"),
        Token(TokenType.CLOSED_CURLY_BRACKET, "}"),
    ]

    try:
        parse = Parser(tokens)
        parse.parser()
    except Exception as exc:
        pytest.fail(reason="Unexpected Exception {}".format(exc), pytrace=True)


def test_incorrect_json():

    tokens = [
        Token(TokenType.OPEN_CURLY_BRACKET, "{"),
        Token(TokenType.OPEN_CURLY_BRACKET, "{"),
        Token(TokenType.CLOSED_CURLY_BRACKET, "}"),
    ]

    with pytest.raises(ParseException):
        parse = Parser(tokens)
        parse = parse.parser()


def test_object_with_list():
    tokens = [
        Token(TokenType.OPEN_CURLY_BRACKET, "{"),
        Token(TokenType.TEXT, "key"),
        Token(TokenType.SEMI_COLON, ":"),
        Token(TokenType.OPEN_SQUARE_BRACKET, "["),
        Token(TokenType.OPEN_CURLY_BRACKET, "{"),
        Token(TokenType.TEXT, "key1"),
        Token(TokenType.SEMI_COLON, ":"),
        Token(TokenType.NUMBER, 6),
        Token(TokenType.COMMA, ","),
        Token(TokenType.CLOSED_CURLY_BRACKET, "}"),
        Token(TokenType.COMMA, ","),
        Token(TokenType.CLOSED_SQUARE_BRACKET, "]"),
        Token(TokenType.COMMA, ","),
        Token(TokenType.CLOSED_CURLY_BRACKET, "}"),
    ]

    try:
        parse = Parser(tokens)
        parse.parser()
    except Exception as exc:
        pytest.fail(reason="Unexpected Exception {}".format(exc), pytrace=True)


def test_array_with_elements():

    tokens = [
        Token(TokenType.OPEN_SQUARE_BRACKET, "["),
        Token(TokenType.NUMBER, 5),
        Token(TokenType.COMMA, ","),
        Token(TokenType.NUMBER, 5),
        Token(TokenType.COMMA, ","),
        Token(TokenType.NUMBER, 5),
        Token(TokenType.COMMA, ","),
        Token(TokenType.NUMBER, 5),
        Token(TokenType.COMMA, ","),
        Token(TokenType.NUMBER, 5),
        Token(TokenType.CLOSED_SQUARE_BRACKET, "]"),
    ]

    try:
        parse = Parser(tokens)
        parse.parser()
    except Exception as exc:
        pytest.fail(reason="Unexpected Exception {}".format(exc), pytrace=True)


def test_object_with_one_field_no_comma():

    tokens = [
        Token(TokenType.OPEN_CURLY_BRACKET, "{"),
        Token(TokenType.TEXT, "Key"),
        Token(TokenType.SEMI_COLON, ":"),
        Token(TokenType.NUMBER, 5),
        Token(TokenType.CLOSED_CURLY_BRACKET, "}"),
    ]

    try:
        parse = Parser(tokens)
        parse.parser()
    except Exception as exc:
        pytest.fail(reason="Unexpected Exception {}".format(exc), pytrace=True)
