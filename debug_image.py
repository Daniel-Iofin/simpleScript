#!/usr/bin/env python3

from image_lexer import ImageLexer

def debug_image():
    lexer = ImageLexer("test_script.png")
    tokens = lexer.tokenize()

    print("Decoded tokens:")
    for i, token in enumerate(tokens):
        print(f"{i}: {token}")

if __name__ == "__main__":
    debug_image()