class Parser:
    def __init__(self, tokens):
        self.tokens = [(ttype, value) for ttype, value, *_ in tokens]
        self.pos = 0

    def match(self, expected_type, expected_value=None):
        if self.pos < len(self.tokens):
            ttype, tval = self.tokens[self.pos]
            if ttype == expected_type and (expected_value is None or tval == expected_value):
                self.pos += 1
                return True
        return False

    def parse(self):
        while self.pos < len(self.tokens):
            if not self.statement():
                print("HATA: Sözdizimi uyumsuz.")
                return False
        return True

    def declaration(self):
        current = self.pos
        if self.match("TYPE"):
            if self.match("IDENTIFIER"):
                if self.match("OPERATOR", "="):
                    if self.expression():
                        if self.match("PUNCTUATION", ";"):
                            return True
        self.pos = current
        return False

    def statement(self):
        if self.declaration():
            return True
        if self.match("KEYWORD", "if"):
            if self.match("PUNCTUATION", "("):
                if self.expression():
                    if self.match("PUNCTUATION", ")"):
                        return self.block()
            return False
        if self.match("KEYWORD", "while"):
            if self.match("PUNCTUATION", "("):
                if self.expression():
                    if self.match("PUNCTUATION", ")"):
                        return self.block()
            return False
        if self.match("KEYWORD", "return"):
            if self.expression():
                return self.match("PUNCTUATION", ";")
            return False
        if self.assignment():
            return True
        return False

    def assignment(self):
        current = self.pos
        if self.match("IDENTIFIER"):
            if self.match("OPERATOR", "="):
                if self.expression():
                    if self.match("PUNCTUATION", ";"):
                        return True
        self.pos = current
        return False

    def block(self):
        if self.match("PUNCTUATION", "{"):
            while self.pos < len(self.tokens) and not self.match("PUNCTUATION", "}"):
                if not self.statement():
                    return False
            return True
        return False

    def expression(self):
        if not self.term():
            return False
        while self.match("OPERATOR") and (self.lookahead_type() in ("IDENTIFIER", "NUMBER", "PUNCTUATION") or self.lookahead_value() == "("):
            if not self.term():
                return False
        return True

    def term(self):
        if self.match("IDENTIFIER") or self.match("NUMBER"):
            return True
        if self.match("PUNCTUATION", "("):
            if self.expression():
                return self.match("PUNCTUATION", ")")
        return False

    def lookahead_type(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos][0]
        return None

    def lookahead_value(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos][1]
        return None
