import lexer


def test_checking_punctuation_tokens():
    source = "{}[]:"
    tokens = lexer.tokenize(source)

    assert tokens[0].type == lexer.TokenType.OPEN_CURLY_BRACKET
    assert tokens[0].value == "{"
    assert tokens[1].type == lexer.TokenType.CLOSED_CURLY_BRACKET
    assert tokens[1].value == "}"
    assert tokens[2].type == lexer.TokenType.OPEN_SQUARE_BRACKET
    assert tokens[2].value == "["
    assert tokens[3].type == lexer.TokenType.CLOSED_SQUARE_BRACKET
    assert tokens[3].value == "]"
    assert tokens[4].type == lexer.TokenType.SEMI_COLON
    assert tokens[4].value == ":"


def test_checking_word_tokenization():
    source = '"word"'
    tokens = lexer.tokenize(source)

    assert len(tokens) == 1, "Invalid Size on Tokens"
    assert tokens[0].type == lexer.TokenType.TEXT, "Invalid Type for Token"
    assert tokens[0].value == "word"


def test_checking_number_tokenization():
    source = "2.5"
    tokens = lexer.tokenize(source)

    assert len(tokens) == 1, "Invalid Size on Tokens"
    assert tokens[0].type == lexer.TokenType.NUMBER, "Invalid Type for Token"
    assert tokens[0].value == 2.5


def test_checking_bool_tokenization():
    source = "true false"
    tokens = lexer.tokenize(source)

    assert len(tokens) == 3, "Invalid Size on Tokens"
    assert tokens[0].type == lexer.TokenType.BOOL, "Invalid Type for Token"
    assert tokens[0].value == True
    assert tokens[1].type == lexer.TokenType.SKIP, "Invalid Type for Token"
    assert tokens[1].value == " "
    assert tokens[2].type == lexer.TokenType.BOOL, "Invalid Type for Token"
    assert tokens[2].value == False


def test_simple_object():
    source = '{\n"a":3.5\n}'
    tokens = lexer.tokenize(source)

    assert len(tokens) == 7
    assert tokens[0].type == lexer.TokenType.OPEN_CURLY_BRACKET
    assert tokens[1].type == lexer.TokenType.SKIP
    assert tokens[2].type == lexer.TokenType.TEXT
    assert tokens[3].type == lexer.TokenType.SEMI_COLON
    assert tokens[4].type == lexer.TokenType.NUMBER
    assert tokens[5].type == lexer.TokenType.SKIP
    assert tokens[6].type == lexer.TokenType.CLOSED_CURLY_BRACKET
