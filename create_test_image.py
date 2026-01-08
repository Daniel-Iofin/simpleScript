#!/usr/bin/env python3

from PIL import Image
import math
import sys
import os

# Add the current directory to the path so we can import from lexer
sys.path.insert(0, os.path.dirname(__file__))
from lexer import TokenType

def encode_string(s):
    """Encode a string into a sequence of RGB values"""
    colors = []
    for char in s:
        ascii_val = ord(char)
        # Use R channel for ASCII value, G and B for future extensions
        colors.append((ascii_val, 0, 0))
    # Add null terminator
    colors.append((0, 0, 0))
    return colors

def encode_number(num_str):
    """Encode a number string into RGB values"""
    return encode_string(num_str)

def encode_identifier(ident):
    """Encode an identifier into RGB values"""
    return encode_string(ident)

def create_color_mapping():
    """Create the same color mapping as ImageLexer"""
    token_to_color = {}

    # Keywords
    keywords = [
        ('let', TokenType.LET),
        ('if', TokenType.IF),
        ('else', TokenType.ELSE),
        ('while', TokenType.WHILE),
        ('for', TokenType.FOR),
        ('def', TokenType.DEF),
        ('return', TokenType.RETURN),
        ('break', TokenType.BREAK),
        ('continue', TokenType.CONTINUE),
        ('true', TokenType.TRUE),
        ('false', TokenType.FALSE),
    ]

    # Single character tokens
    single_chars = [
        ('+', TokenType.PLUS),
        ('-', TokenType.MINUS),
        ('*', TokenType.MULTIPLY),
        ('/', TokenType.DIVIDE),
        ('%', TokenType.MODULO),
        ('=', TokenType.ASSIGN),
        ('<', TokenType.LESS),
        ('>', TokenType.GREATER),
        ('(', TokenType.LPAREN),
        (')', TokenType.RPAREN),
        ('{', TokenType.LBRACE),
        ('}', TokenType.RBRACE),
        ('[', TokenType.LBRACKET),
        (']', TokenType.RBRACKET),
        (';', TokenType.SEMICOLON),
        (',', TokenType.COMMA),
    ]

    # Two character operators
    two_chars = [
        ('==', TokenType.EQUAL),
        ('!=', TokenType.NOT_EQUAL),
        ('<=', TokenType.LESS_EQUAL),
        ('>=', TokenType.GREATER_EQUAL),
        ('++', TokenType.PLUS_PLUS),
        ('--', TokenType.MINUS_MINUS),
        ('&&', TokenType.AND),
        ('||', TokenType.OR),
        ('+=', TokenType.PLUS_ASSIGN),
        ('-=', TokenType.MINUS_ASSIGN),
        ('*=', TokenType.MULTIPLY_ASSIGN),
        ('/=', TokenType.DIVIDE_ASSIGN),
        ('%=', TokenType.MODULO_ASSIGN),
    ]

    # Single character operators
    single_operators = [
        ('!', TokenType.NOT),
    ]

    # Generate colors systematically - same as ImageLexer
    color_index = 0

    # Keywords
    for keyword, token_type in keywords:
        r = (color_index // (256 * 256)) % 256
        g = (color_index // 256) % 256
        b = (color_index % 128) * 2  # Ensure even blue and distinct
        token_to_color[(token_type, keyword)] = (r, g, b)
        color_index += 1

    # Single characters
    for char, token_type in single_chars:
        r = (color_index // (256 * 256)) % 256
        g = (color_index // 256) % 256
        b = (color_index % 128) * 2  # Ensure even blue and distinct
        token_to_color[(token_type, char)] = (r, g, b)
        color_index += 1

    # Two character operators
    for op, token_type in two_chars:
        r = (color_index // (256 * 256)) % 256
        g = (color_index // 256) % 256
        b = (color_index % 128) * 2  # Ensure even blue and distinct
        token_to_color[(token_type, op)] = (r, g, b)
        color_index += 1

    # Single character operators
    for op, token_type in single_operators:
        r = (color_index // (256 * 256)) % 256
        g = (color_index // 256) % 256
        b = (color_index % 128) * 2  # Ensure even blue and distinct
        token_to_color[(token_type, op)] = (r, g, b)
        color_index += 1

    # Literal token types (base colors for encoding values)
    r = (color_index // (256 * 256)) % 256
    g = (color_index // 256) % 256
    b = (color_index % 128) * 2
    token_to_color[(TokenType.STRING, 'STRING_BASE')] = (r, g, b)
    color_index += 1

    r = (color_index // (256 * 256)) % 256
    g = (color_index // 256) % 256
    b = (color_index % 128) * 2
    token_to_color[(TokenType.IDENTIFIER, 'IDENTIFIER_BASE')] = (r, g, b)
    color_index += 1

    r = (color_index // (256 * 256)) % 256
    g = (color_index // 256) % 256
    b = (color_index % 128) * 2
    token_to_color[(TokenType.NUMBER, 'NUMBER_BASE')] = (r, g, b)
    color_index += 1

    # Special tokens - EOF
    r = (color_index // (256 * 256)) % 256
    g = (color_index // 256) % 256
    b = (color_index % 128) * 2
    token_to_color[(TokenType.EOF, '')] = (r, g, b)
    color_index += 1

    # Comments
    r = (color_index // (256 * 256)) % 256
    g = (color_index // 256) % 256
    b = (color_index % 128) * 2
    token_to_color[(TokenType.COMMENT, 'COMMENT_BASE')] = (r, g, b)

    return token_to_color

def encode_string_as_colors(s):
    """Encode a string as a sequence of colors (simplified - each char gets a color)"""
    colors = []
    for char in s:
        # Simple encoding: use ASCII value as base color
        ascii_val = ord(char)
        r = ascii_val % 256
        g = (ascii_val // 256) % 256
        b = (ascii_val // (256 * 256)) % 256
        colors.append((r, g, b))
    return colors

def create_test_image():
    """Create a test image with embedded Picasso code"""
    width, height = 1200, 400  # Wider image to fit all tokens

    # Create a white image
    img = Image.new('RGB', (width, height), color='white')
    pixels = img.load()

    # Get color mapping
    token_to_color = create_color_mapping()

    # Test program: let msg = "Hello"; let n = 42; print(msg + " " + str(n));
    tokens = [
        (TokenType.LET, 'let'),
        (TokenType.IDENTIFIER, 'msg'),
        (TokenType.ASSIGN, '='),
        (TokenType.STRING, 'Hello'),
        (TokenType.SEMICOLON, ';'),
        (TokenType.LET, 'let'),
        (TokenType.IDENTIFIER, 'n'),
        (TokenType.ASSIGN, '='),
        (TokenType.NUMBER, '42'),
        (TokenType.SEMICOLON, ';'),
        (TokenType.IDENTIFIER, 'print'),
        (TokenType.LPAREN, '('),
        (TokenType.IDENTIFIER, 'msg'),
        (TokenType.PLUS, '+'),
        (TokenType.STRING, ' '),
        (TokenType.PLUS, '+'),
        (TokenType.IDENTIFIER, 'str'),
        (TokenType.LPAREN, '('),
        (TokenType.IDENTIFIER, 'n'),
        (TokenType.RPAREN, ')'),
        (TokenType.RPAREN, ')'),
        (TokenType.SEMICOLON, ';'),
    ]

    # Create a simple horizontal backbone
    backbone_y = 50
    backbone_start_x = 20
    backbone_spacing = 40  # Space between backbone pixels

    backbone_points = []
    for i in range(len(tokens)):
        bx = backbone_start_x + i * backbone_spacing
        if bx >= width - 20:
            break
        backbone_points.append((bx, backbone_y))


    # Set backbone pixels (curve pixels with odd LSB in blue)
    for bx, by in backbone_points:
        r, g, b = pixels[bx, by]
        pixels[bx, by] = (r, g, b | 1)  # Set odd LSB in blue

    # Place tokens adjacent to backbone points (below the backbone)
    for i, (token_type, token_value) in enumerate(tokens):
        if i >= len(backbone_points):
            break

        # Get backbone position
        bx, by = backbone_points[i]

        # Place token below the backbone
        tx, ty = bx, by + 1

        # Get the base color for this token
        color_key = (token_type, token_value)
        if color_key not in token_to_color:
            # For literal tokens, use the base type
            if token_type in [TokenType.IDENTIFIER, TokenType.NUMBER, TokenType.STRING]:
                color_key = (token_type, f"{token_type.split('_')[0]}_BASE")
            else:
                continue

        base_color = token_to_color[color_key]

        # Set the token pixel
        pixels[tx, ty] = base_color

        # For literal tokens, encode the actual value in subsequent pixels (to the right)
        if token_type in [TokenType.IDENTIFIER, TokenType.NUMBER, TokenType.STRING]:
            literal_colors = []
            if token_type == TokenType.IDENTIFIER:
                literal_colors = encode_identifier(token_value)
            elif token_type == TokenType.NUMBER:
                literal_colors = encode_number(token_value)
            elif token_type == TokenType.STRING:
                literal_colors = encode_string(token_value)

            # Place literal encoding pixels to the right of the token
            literal_x, literal_y = tx + 1, ty
            for r, g, b in literal_colors:
                if literal_x >= width:
                    break
                # For literal pixels, set green channel to 1 to mark as literal data
                pixels[literal_x, literal_y] = (r, 1, b)
                literal_x += 1

    return img

if __name__ == "__main__":
    img = create_test_image()
    img.save("test_script.png")
    print("Test image saved as test_script.png")
