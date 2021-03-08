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
    def __init__(self, i, base=None, t="ERROR", p=None, l=None, r=None):
        self.line = i
        self.root = base
        self.type = t
        self.parent = p
        self.left = l
        self.right = r

    def print(self):
        print(f"root: {self.root}")
        print(f"type: {self.type}")
        print(f"parent: {self.parent}")
        print(f"left: {self.left}")
        print(f"right: {self.right}")
        print("------------------")


def output(lines):
    out_file = open(sys.argv[2], 'a')

    for line in lines:
        print(f"Line {line[0]} : {str.join(' ', line[1])}", file=out_file)
        for token in line[1]:
            if re.match(KEYWORD, token):
                Token = Tokens(line[0], token, "KEYWORD")
                print(f"{token} : KEYWORD", file=out_file)
            elif re.match(IDENTIFIER, token):
                Token = Tokens(line[0], token, "IDENTIFIER")
                print(f"{token} : IDENTIFIER", file=out_file)
            elif re.match(NUMBER, token):
                Token = Tokens(line[0], token, "NUMBER")
                print(f"{token} : NUMBER", file=out_file)
            elif re.match(SYMBOL, token):
                Token = Tokens(line[0], token, "SYMBOL")
                print(f"{token} : SYMBOL", file=out_file)
            else:
                Token = Tokens(line[0], token, "ERROR")
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
                if re.match(KEYWORD, (word.join(characters[index]))):
                    while re.match(KEYWORD, (word.join(characters[index]))):
                        word = word + characters[index]
                        index += 1
                    tokens.append(word)
                    token = token.strip(word)
                elif re.match(IDENTIFIER, (word.join(characters[index]))):
                    while re.match(IDENTIFIER, (word.join(characters[index]))):
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
    segments = line.split(' ')
    tokens = []  # Make list to hold tokens

    for token in segments:
        if re.match(NUMBER, token):
            tokens.append(token)
        elif re.match(KEYWORD, token):
            tokens.append(token)
        elif re.match(IDENTIFIER, token):
            tokens.append(token)
        elif re.match(SYMBOL, token):
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
    index = -1
    for token in token_bank:
        index += 1
        if token.type is "SYMBOL":
            if token.root is '(' or token.root is ')':
                continue  # Just to skip '()'
            elif token.root is '*':
                if (index - 1) > 0 and (token_bank[index-1].type is "NUMBER" or token_bank[index-1].type is "IDENTIFIER"):
                    token_bank[index-1].parent = token
                    token.left = token_bank[index-1]
                if (index + 1) <= len(token_bank) and token_bank[index+1].type is "SYMBOL":
                    token_bank[index+1].parent = token
                    token.right = token_bank[index+1]
            elif token.root is '/':
                if (index - 1) > 0 and (token_bank[index-1].type is "NUMBER" or token_bank[index-1].type is "IDENTIFIER"):
                    token_bank[index-1].parent = token
                    token.left = token_bank[index-1]
                if (index + 1) <= len(token_bank) and token_bank[index+1].type is "SYMBOL":
                    token_bank[index+1].parent = token
                    token.right = token_bank[index+1]
            elif token.root is '-':
                if (index - 1) > 0 and (token_bank[index-1].type is "NUMBER" or token_bank[index-1].type is "IDENTIFIER"):
                    token_bank[index-1].parent = token
                    token.left = token_bank[index-1]
                if (index + 1) <= len(token_bank) and token_bank[index+1].type is "SYMBOL":
                    token_bank[index+1].parent = token
                    token.right = token_bank[index+1]
            elif token.root is '+':
                if (index - 1) > 0 and (token_bank[index-1].type is "NUMBER" or token_bank[index-1].type is "IDENTIFIER"):
                    token_bank[index-1].parent = token
                    token.left = token_bank[index-1]
                if (index + 1) <= len(token_bank) and token_bank[index+1].type is "SYMBOL":
                    token_bank[index+1].parent = token
                    token.right = token_bank[index+1]
            else:
                print(f"An error has occurred at line {token.line} for token {token.root}, AST can not be made, exiting.")
                exit(1)

    print("------------------")
    for token in token_bank:
        token.print()
