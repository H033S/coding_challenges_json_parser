from json_parser.operators import (
    CollectionExpression,
    ConstantExpression,
    Expression,
    FieldExpression,
    KeyExpression,
    ObjectExpression,
    ValueExpression,
)
from collections import deque
import json_parser.lexer as lexer


class ParseException(Exception):

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

    def __repr__(self) -> str:
        return self.message


class Parser:

    def __init__(self, tokens: list[lexer.Token]) -> None:
        self.stack_expression: list[Expression] = []
        self.tokens = deque(tokens)

    def throw_parse_exception(self, invalid_token):
        raise ParseException("Invalid Token {}".format(invalid_token))

    def parser(self):

        while self.tokens:

            if self.hasStackAnOpenCurlyBracketAtFirst():
                self.consumeObjectFromTokens()

            elif self.hasStackAnOpenSquareBracketAtFirst():
                self.consumeListFromTokens()

            else:
                raise ParseException(
                    "Expected token { or '[' but provided %s" % self.tokens[0]
                )

    def consumeObjectFromTokens(self):

        object = ObjectExpression([])
        fieldsConsumed = 0
        commaWasConsumed = False

        if not self.hasStackAnOpenCurlyBracketAtFirst():
            raise ParseException("Cannot parse object")

        self.tokens.popleft()

        while self.tokens:

            token = self.tokens[0]

            if token.type == lexer.TokenType.CLOSED_CURLY_BRACKET:
                self.tokens.popleft()
                self.stack_expression.append(object)
                return

            if fieldsConsumed > 1 and not commaWasConsumed:
                raise ParseException("Expected comma after field")

            self.consumeFieldFromTokens()
            fieldsConsumed += 1
            commaWasConsumed = False
            if self.nextTokenInTokensIsComma():
                self.consumeCommaFromTokens()
                commaWasConsumed = True

            expression = self.stack_expression.pop()
            assert type(expression) == FieldExpression

            object.value.append(expression)

        else:
            raise ParseException("Expected } ")

    def nextTokenInTokensIsComma(self):
        return self.tokens and self.tokens[0].type == lexer.TokenType.COMMA

    def hasStackAnOpenCurlyBracketAtFirst(self) -> bool:
        return (
            len(self.tokens) > 0
            and self.tokens[0].type == lexer.TokenType.OPEN_CURLY_BRACKET
        )

    def consumeFieldFromTokens(self):

        if not self.isAvailableElementsToParseField():
            raise ParseException("Insufficient Element to parse an element")

        self.consumeKeyFromTokens()
        self.consumeSemiColonFromTokens()
        self.consumeValueFromTokens()

        value = self.stack_expression.pop()
        key = self.stack_expression.pop()

        assert isinstance(key, KeyExpression)
        assert isinstance(value, ValueExpression)

        self.stack_expression.append(FieldExpression(key, value))

    def isAvailableElementsToParseField(self):
        return len(self.tokens) >= 4

    def consumeKeyFromTokens(self):

        token: lexer.Token = self.tokens.popleft()
        if not token.type == lexer.TokenType.TEXT:
            self.throw_parse_exception(token)

        self.stack_expression.append(KeyExpression(token.value))

    def consumeSemiColonFromTokens(self):

        token: lexer.Token = self.tokens.popleft()

        if not token.type == lexer.TokenType.SEMI_COLON:
            self.throw_parse_exception(token)

    def consumeValueFromTokens(self):

        token: lexer.Token = self.tokens[0]

        if not token.type in (
            lexer.TokenType.OPEN_CURLY_BRACKET,
            lexer.TokenType.OPEN_SQUARE_BRACKET,
            lexer.TokenType.TEXT,
            lexer.TokenType.NUMBER,
            lexer.TokenType.BOOL,
        ):
            self.throw_parse_exception(token)

        if token.type == lexer.TokenType.OPEN_CURLY_BRACKET:
            self.consumeObjectFromTokens()

        elif token.type == lexer.TokenType.OPEN_SQUARE_BRACKET:
            self.consumeListFromTokens()

        elif token.type in (
            lexer.TokenType.TEXT,
            lexer.TokenType.NUMBER,
            lexer.TokenType.BOOL,
        ):
            self.tokens.popleft()
            self.stack_expression.append(ConstantExpression(token.value))

    def consumeCommaFromTokens(self):

        token: lexer.Token = self.tokens.popleft()

        if not token.type == lexer.TokenType.COMMA:
            self.throw_parse_exception(token)

    def consumeListFromTokens(self):

        collection = CollectionExpression([])
        fieldsConsumed = 0
        commaWasConsumed = False

        if not self.isPossibleToStartParsingObject():
            raise ParseException("Cannot parse list")

        self.tokens.popleft()

        while self.tokens:

            token = self.tokens[0]

            if token.type == lexer.TokenType.CLOSED_SQUARE_BRACKET:
                self.tokens.popleft()
                self.stack_expression.append(collection)
                return

            if fieldsConsumed > 1 and not commaWasConsumed:
                raise ParseException("Expected comma after field")

            self.consumeValueFromTokens()
            fieldsConsumed += 1
            commaWasConsumed = False
            if self.nextTokenInTokensIsComma():
                self.consumeCommaFromTokens()
                commaWasConsumed = True

            expression = self.stack_expression.pop()
            assert isinstance(expression, ValueExpression)

            collection.value.append(expression)

        else:
            raise ParseException("Expected } ")

    def hasStackAnOpenSquareBracketAtFirst(self) -> bool:
        return (
            len(self.tokens) >= 0
            and self.tokens[0].type == lexer.TokenType.OPEN_SQUARE_BRACKET
        )

    def isPossibleToStartParsingObject(self) -> bool:
        return (
            len(self.tokens) >= 3
            and self.tokens[0].type == lexer.TokenType.OPEN_SQUARE_BRACKET
        )
