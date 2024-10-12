import os

import pytest

from json_parser import lexer
from json_parser.parser import ParseException, Parser


FILES_PATH = r"./files/"

PASS = FILES_PATH + "pass"
FAIL = FILES_PATH + "fail"

getFilename = lambda file: os.path.join(FILES_PATH, file)
filepaths = [getFilename(file) for file in os.listdir(FILES_PATH)]


@pytest.mark.parametrize("filename", filepaths)
def test_files(filename: str):

    with open(filename, "r") as json:

        if filename.startswith(PASS):

            print("Should success: {}".format(filename))
            try:
                tokens = lexer.tokenize(json.read())
                parser = Parser(tokens)
                parser.parser()
            except Exception as exc:
                pytest.fail(reason="Unexpected Exception {}".format(exc), pytrace=False)

        elif filename.startswith(FAIL):

            print("Should fail: {}".format(filename))
            with pytest.raises((ParseException, lexer.LexerException)):
                tokens = lexer.tokenize(json.read())
                parser = Parser(tokens)
                parser.parser()
