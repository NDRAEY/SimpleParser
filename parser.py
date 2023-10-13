"""
Scyther parser.

Grammar:

NUMBER_TOKEN = [0-9]+
DECIMAL = '-'? + NUMBER_TOKEN

PLUS_MINUS = '+' | '-'
MUL_DIV = '*' | '/'

EXPR_LV1 = DECIMAL + MUL_DIV + DECIMAL
         | DECIMAL

EXPR_LV2 = EXPR_LV1 + PLUS_MINUS + EXPR_LV1
"""


class Parser:
    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        self.position = 0

    def _prev(self) -> str | None:
        self.position -= 1
        reserved = self.tokens[self.position]


        if self.position >= 0:
            return reserved

    def _next(self) -> str | None:
        if self.position > len(self.tokens) - 1:
            return

        reserved = self.tokens[self.position]

        self.position += 1

        return reserved

    def current(self) -> str | None:
        if self.position > len(self.tokens) - 1:
            return

        return self.tokens[self.position]

    def next(self):
        while self.current() and self.current() == ' ':
            self._next()

        return self._next()

    def number_token(self):
        token = self.next()

        print("Number: ", token)

        if token and token.isdigit():
            return token

    def decimal(self):
        minus = self.next()

        if not (minus is None or minus == "-"):  # '-'?
            number = minus
        else:
            number = self.number_token()

        if number is None:
            print("Syntax error: Expected number, got:", self.current())
            print(self.position, len(self.tokens))
            exit(1)

        return (-1 if minus == "-" else 1) * int(number)

    def plus_minus(self):
        token = self.next()

        if token in ('+', '-'):
            return token

    def mul_div(self):
        token = self.next()

        if token in ('*', '/'):
            return token

    def expr_lv1(self):
        left = self.decimal()

        while True:
            sign = self.mul_div()

            if sign is None:
                self._prev()
                return left

            right = self.decimal()

            if sign == "*":
                left = left * right
            elif sign == "/":
                left = left / right

    def expr_lv2(self):
        left = self.expr_lv1()

        while True:
            sign = self.plus_minus()

            if sign is None:
                return left

            right = self.expr_lv1()

            if sign == "+":
                left =  left + right
            elif sign == "-":
                left =  left - right


    def parse(self):
        print(self.expr_lv2())
