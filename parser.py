"""
Scyther parser.

Grammar:

NUMBER_TOKEN = [0-9]+
DECIMAL = '-'? + NUMBER_TOKEN

PLUS_MINUS = '+' | '-'
MUL_DIV = '*' | '/'

EXPR_LV1 = DECIMAL + (MUL_DIV + DECIMAL)+
         | DECIMAL

EXPR_LV2 = EXPR_LV1 + (PLUS_MINUS + EXPR_LV1)+
"""


class Parser:
    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        self.position = -1

    def prev(self) -> str | None:
        self.position -= 1

        while self.current() == ' ':
            self.prev()

        if self.position < 0:
            return

        return self.tokens[self.position]

    def next(self) -> str | None:
        self.position += 1

        while self.current() == ' ':
            self.next()

        if self.position > len(self.tokens) - 1:
            return

        return self.tokens[self.position]

    def expect(self, token: str):
        if token != self.current():
            print("Syntax error: Expected", token, "found", self.current())
            exit(1)

    def current(self) -> str | None:
        if (self.position > len(self.tokens) - 1) or (self.position < 0):
            return

        return self.tokens[self.position]

    def number_token(self):
        token = self.next()

        if token and token.isdigit():
            return token

    def decimal(self):
        minus = self.next()
        real_minus = minus == "-"

        if minus == "(":
            expr = self.expr_lv2()

            if self.current() != ")":
                print("Syntax error: Unclosed '('")
                exit(1)

            return expr
        elif minus != "-":
            self.prev()

        number = self.number_token()

        if number is None:
            print("Syntax error: Expected number, got:", self.current())
            exit(1)
        elif not number.isdigit():
            print("Syntax error:", number, "is not a digit")
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
                self.prev()
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
                left = left + right
            elif sign == "-":
                left = left - right


    def parse(self):
        print(self.expr_lv2())
        #
        # print(self.next())
        # print(self.next())
        # print(self.next())
        # print(self.next())
        # print(self.next())
        # print(self.next())
        # print(self.next())
        # print(self.next())
