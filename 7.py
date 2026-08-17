import re

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


def tokenize(text):
    token_spec = [
        ("NUMBER",   r'\d+\.\d+|\d+'),
        ("IDENT",    r'[a-zA-Z_]\w*'),
        ("OP",       r'[+\-*/^()=]'),
        ("SKIP",     r'[ \t]+'),
    ]
    regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_spec)
    tokens = []
    for match in re.finditer(regex, text):
        kind = match.lastgroup
        value = match.group()
        if kind == "SKIP":
            continue
        if kind == "NUMBER":
            value = float(value) if '.' in value else int(value)
        tokens.append(Token(kind, value))
    tokens.append(Token("EOF", None))
    return tokens


class Parser:
    """
    Grammar (lowest to highest precedence):
        assign  := IDENT '=' expr | expr
        expr    := term (('+' | '-') term)*
        term    := power (('*' | '/') power)*
        power   := unary ('^' power)?      # right-associative
        unary   := ('-' unary) | atom
        atom    := NUMBER | IDENT | '(' expr ')'
    """
    def __init__(self, tokens, variables):
        self.tokens = tokens
        self.pos = 0
        self.vars = variables

    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, type_, value=None):
        tok = self.advance()
        if tok.type != type_ or (value is not None and tok.value != value):
            raise SyntaxError(f"Expected {type_} {value}, got {tok}")
        return tok

    def parse(self):
        if self.peek().type == "IDENT" and self.tokens[self.pos + 1].value == "=":
            name = self.advance().value
            self.expect("OP", "=")
            value = self.expr()
            self.vars[name] = value
            return value
        return self.expr()

    def expr(self):
        result = self.term()
        while self.peek().type == "OP" and self.peek().value in ("+", "-"):
            op = self.advance().value
            rhs = self.term()
            result = result + rhs if op == "+" else result - rhs
        return result

    def term(self):
        result = self.power()
        while self.peek().type == "OP" and self.peek().value in ("*", "/"):
            op = self.advance().value
            rhs = self.power()
            if op == "/" and rhs == 0:
                raise ZeroDivisionError("Division by zero")
            result = result * rhs if op == "*" else result / rhs
        return result

    def power(self):
        base = self.unary()
        if self.peek().type == "OP" and self.peek().value == "^":
            self.advance()
            exponent = self.power()  # right-associative recursion
            return base ** exponent
        return base

    def unary(self):
        if self.peek().type == "OP" and self.peek().value == "-":
            self.advance()
            return -self.unary()
        return self.atom()

    def atom(self):
        tok = self.advance()
        if tok.type == "NUMBER":
            return tok.value
        if tok.type == "IDENT":
            if tok.value not in self.vars:
                raise NameError(f"Undefined variable '{tok.value}'")
            return self.vars[tok.value]
        if tok.type == "OP" and tok.value == "(":
            result = self.expr()
            self.expect("OP", ")")
            return result
        raise SyntaxError(f"Unexpected token {tok}")


def evaluate(text, variables):
    tokens = tokenize(text)
    return Parser(tokens, variables).parse()


if __name__ == "__main__":
    variables = {}
    tests = [
        "3 + 4 * 2",
        "(3 + 4) * 2",
        "2 ^ 3 ^ 2",      # should be 512 (right-associative: 2^(3^2))
        "-5 + 3",
        "x = 10",
        "y = x * 2 + 1",
        "y / (x - 5)",
    ]
    for t in tests:
        result = evaluate(t, variables)
        print(f"{t!r:20} => {result}")