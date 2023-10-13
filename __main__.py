import tokenizer
import parser

if __name__ == "__main__":
    code = "3 * 4 - 6 + 2 * 3"  # 12

    tokens = tokenizer.tokenize(code)

    prs = parser.Parser(tokens)

    print(prs.parse())
