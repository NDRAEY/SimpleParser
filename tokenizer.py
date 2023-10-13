def tokenize(code: str) -> list[str]:
    tokens = []
    token_buf = ""
    is_tokenizing_string = False

    for i in code:
        if i.isalnum():
            token_buf += i
        elif i == "\"":
            is_tokenizing_string = not is_tokenizing_string
            token_buf += "\""
        elif is_tokenizing_string:
            token_buf += i
        else:
            if token_buf:
                tokens.append(token_buf)
                token_buf = ""
            tokens.append(i)

    tokens.append(token_buf)

    return tokens


if __name__ == "__main__":
    print(tokenize("Hello, world! [abc123] {abc123}"))