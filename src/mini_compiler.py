import re

TOKEN_SPEC = [
    ("NUMBER", r"\d+(\.\d+)?"),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("MUL", r"\*"),
    ("DIV", r"/"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("SKIP", r"[ \t]+"),
]


def tokenize(text):
    regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)
    tokens = []
    for match in re.finditer(regex, text):
        kind = match.lastgroup
        value = match.group()
        if kind != "SKIP":
            tokens.append((kind, value))
    tokens.append(("EOF", ""))
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        return self.tokens[self.position]

    def eat(self, expected):
        kind, value = self.current()
        if kind != expected:
            raise SyntaxError(f"Expected {expected}, got {kind}")
        self.position += 1
        return value

    def parse(self):
        result = self.expression()
        self.eat("EOF")
        return result

    def expression(self):
        result = self.term()
        while self.current()[0] in ("PLUS", "MINUS"):
            operator = self.current()[0]
            self.eat(operator)
            if operator == "PLUS":
                result += self.term()
            else:
                result -= self.term()
        return result

    def term(self):
        result = self.factor()
        while self.current()[0] in ("MUL", "DIV"):
            operator = self.current()[0]
            self.eat(operator)
            if operator == "MUL":
                result *= self.factor()
            else:
                result /= self.factor()
        return result

    def factor(self):
        kind, value = self.current()
        if kind == "NUMBER":
            self.eat("NUMBER")
            return float(value)
        if kind == "LPAREN":
            self.eat("LPAREN")
            result = self.expression()
            self.eat("RPAREN")
            return result
        raise SyntaxError(f"Unexpected token: {kind}")


if __name__ == "__main__":
    examples = ["2 + 3 * 4", "(10 + 5) / 3", "8 * (2 + 6) - 5"]
    for expr in examples:
        tokens = tokenize(expr)
        result = Parser(tokens).parse()
        print(f"{expr} = {result}")
