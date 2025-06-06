KEYWORDS = {"if", "while", "return"}
TYPES = {"int", "float", "string"}
OPERATORS = {'%', '+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>='}
PUNCTUATIONS = {';', '(', ')', '{', '}'}

def is_identifier_start(ch):
    return ch.isalpha() or ch == '_'

def is_identifier_part(ch):
    return ch.isalnum() or ch == '_'

def tokenize(code):
    tokens = []
    i = 0
    while i < len(code):
        ch = code[i]
        if ch.isspace():
            i += 1
            continue
        start_index = i
        if ch.isdigit():
            num = ch
            i += 1
            while i < len(code) and (code[i].isdigit() or code[i] == '.'):
                num += code[i]
                i += 1
            tokens.append(("NUMBER", num, start_index))
            continue
        if is_identifier_start(ch):
            ident = ch
            i += 1
            while i < len(code) and is_identifier_part(code[i]):
                ident += code[i]
                i += 1
            if ident in TYPES:
                token_type = "TYPE"
            elif ident in KEYWORDS:
                token_type = "KEYWORD"
            else:
                token_type = "IDENTIFIER"
            tokens.append((token_type, ident, start_index))
            continue
        if ch in "=!<>":
            op = ch
            i += 1
            if i < len(code) and code[i] == '=':
                op += '='
                i += 1
            tokens.append(("OPERATOR", op, start_index))
            continue
        elif ch in "+-*/%":
            tokens.append(("OPERATOR", ch, start_index))
            i += 1
            continue
        if ch in PUNCTUATIONS:
            tokens.append(("PUNCTUATION", ch, start_index))
            i += 1
            continue
        tokens.append(("UNKNOWN", ch, start_index))
        i += 1
    return tokens
