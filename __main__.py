import tokenizer
import parser

if __name__ == "__main__":
    while True:
        code = input("> ")

        tokens = tokenizer.tokenize(code)
        # print(tokens)

        prs = parser.Parser(tokens)
        print(prs.parse())
