###
# Greg Jewell
# Phase 1.2 Lexp, Tokenizer
###

import re
import sys

# Set pattern objects
IDENTIFIER = re.compile(r"^([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*$")
NUMBER = re.compile(r"^[0-9]+$")
SYMBOL = re.compile(r"^(\+|-|\*|/|\(|\)|:=|;)$")
KEYWORD = re.compile(r"^(if|then|else|endif|while|do|endwhile|skip)$")

token_bank = []


class Tokens:
    def __init__(self, base, t, l, r):
        self.root = base
        self.type = t
        self.left = l
        self.right = r


def output(lines):
    out_file = open(sys.argv[2], 'a')

    for line in lines:
        print(f"Line {line[0]} : {str.join(' ', line[1])}", file=out_file)
        for token in line[1]:
            if re.match(KEYWORD, token):
                Token = Tokens(token, "KEYWORD", None, None)
                print(f"{token} : KEYWORD", file=out_file)
            elif re.match(IDENTIFIER, token):
                Token = Tokens(token, "IDENTIFIER", None, None)
                print(f"{token} : IDENTIFIER", file=out_file)
            elif re.match(NUMBER, token):
                Token = Tokens(token, "NUMBER", None, None)
                print(f"{token} : NUMBER", file=out_file)
            elif re.match(SYMBOL, token):
                Token = Tokens(token, "SYMBOL", None, None)
                print(f"{token} : SYMBOL", file=out_file)
            else:
                Token = Tokens(token, "ERROR", None, None)
                print(f"{token} : ERROR", file=out_file)

            token_bank.append(Token)

    out_file.close()


def atomize(token):
    Run = 0
    tokens = []

    while True:
        Run += 1
        temp = []
        word = ""
        index = 0

        characters = list(token)

        if re.match(IDENTIFIER, characters[0]):
            word.join(characters[0])
            if re.match(IDENTIFIER, token):
                tokens.append(token)
                token = token.strip(token)
            elif re.match(KEYWORD, token):
                tokens.append(token)
                token = token.strip(token)
            else:
                print(f"Checking word: {word} -- Stage 1")
                if re.match(KEYWORD, (word.join(characters[index]))):
                    while re.match(KEYWORD, (word.join(characters[index]))):
                        print(f"Checking word: {word} -- Stage 2")
                        word = word + characters[index]
                        index += 1
                    tokens.append(word)
                    token = token.strip(word)
                elif re.match(IDENTIFIER, (word.join(characters[index]))):
                    while re.match(IDENTIFIER, (word.join(characters[index]))):
                        print(f"Checking word: {word} -- Stage 3")
                        word = word + characters[index]
                        index += 1
                    tokens.append(word)
                    token = token.strip(word)
                else:
                    tokens.append(word)
                    token = token.strip(word)

        elif re.match(NUMBER, characters[0]):
            word = word + characters[0]
            if re.match(NUMBER, token):
                tokens.append(token)
                token = token.strip(token)
            else:
                if re.match(NUMBER, (word.join(characters[index]))):
                    while re.match(NUMBER, (word.join(characters[index]))):
                        index += 1
                    tokens.append(word)
                    token = token.strip(word)
                else:
                    tokens.append(word)
                    token = token.strip(word)

        elif re.match(SYMBOL, characters[0]):
            word.join(characters[0])
            if re.match(SYMBOL, token):
                tokens.append(token)
                token = token.strip(token)
            else:
                if re.match(SYMBOL, (word.join(characters[index]))):
                    while re.match(SYMBOL, (word.join(characters[index]))):
                        word = word + characters[index]
                        index += 1
                    tokens.append(word)
                    token = token.strip(word)
                else:
                    tokens.append(word)
                    token = token.strip(characters[index])

        else:
            error = list(token)
            if len(error) > 1 and re.match(SYMBOL, (error[0] + error[1])):
                error = (error[0] + error[1])
                tokens.append(error)
                token = token.strip(error)
            else:
                tokens.append(token[0])
                token = token.strip(token[0])

        if len(token) == 0 or Run == 10:
            return tokens


def tokenize(file, line):
    # print(f"Current Line: {line}")
    segments = line.split(' ')
    tokens = []  # Make list to hold tokens

    for token in segments:
        if re.match(NUMBER, token):
            tokens.append(token)
        elif re.match(IDENTIFIER, token):
            tokens.append(token)
        elif re.match(SYMBOL, token):
            tokens.append(token)
        elif re.match(KEYWORD, token):
            tokens.append(token)
        else:
            results = atomize(token)
            for result in results:
                if result != "ERROR":
                    tokens.append(result)
                elif result == "ERROR":
                    print(f"{results} : ERROR")

    return tokens


def parse():
    for token in token_bank:
        if token.type is "SYMBOL":
            if token.root is '*':
                print(f"{token.root} : {token.type}")