#!/usr/bin/env python3

from PIL import Image
import math

def create_color_mapping():
    """Create the same color mapping as ImageLexer"""
    token_to_color = {}

    # Keywords
    keywords = [
        ('let', 'LET'),
        ('if', 'IF'),
        ('else', 'ELSE'),
        ('while', 'WHILE'),
        ('for', 'FOR'),
        ('def', 'DEF'),
        ('return', 'RETURN'),
        ('break', 'BREAK'),
        ('continue', 'CONTINUE'),
        ('true', 'TRUE'),
        ('false', 'FALSE'),
    ]

    # Single character tokens
    single_chars = [
        ('+', 'PLUS'),
        ('-', 'MINUS'),
        ('*', 'MULTIPLY'),
        ('/', 'DIVIDE'),
        ('%', 'MODULO'),
        ('=', 'ASSIGN'),
        ('<', 'LESS'),
        ('>', 'GREATER'),
        ('(', 'LPAREN'),
        (')', 'RPAREN'),
        ('{', 'LBRACE'),
        ('}', 'RBRACE'),
        ('[', 'LBRACKET'),
        (']', 'RBRACKET'),
        (';', 'SEMICOLON'),
        (',', 'COMMA'),
    ]

    # Two character operators
    two_chars = [
        ('==', 'EQUAL'),
        ('!=', 'NOT_EQUAL'),
        ('<=', 'LESS_EQUAL'),
        ('>=', 'GREATER_EQUAL'),
        ('++', 'PLUS_PLUS'),
        ('--', 'MINUS_MINUS'),
        ('&&', 'AND'),
        ('||', 'OR'),
        ('+=', 'PLUS_ASSIGN'),
        ('-=', 'MINUS_ASSIGN'),
        ('*=', 'MULTIPLY_ASSIGN'),
        ('/=', 'DIVIDE_ASSIGN'),
        ('%=', 'MODULO_ASSIGN'),
    ]

    # Generate colors systematically - same as ImageLexer
    color_index = 0

    # Keywords
    for keyword, token_type in keywords:
        r = (color_index // (256 * 256)) % 256
        g = (color_index // 256) % 256
        b = (color_index % 128) * 2  # Ensure even blue and distinct
        token_to_color[keyword] = (r, g, b)
        color_index += 1

    # Single characters
    for char, token_type in single_chars:
        r = (color_index // (256 * 256)) % 256
        g = (color_index // 256) % 256
        b = (color_index % 128) * 2  # Ensure even blue and distinct
        token_to_color[char] = (r, g, b)
        color_index += 1

    # Two character operators
    for op, token_type in two_chars:
        r = (color_index // (256 * 256)) % 256
        g = (color_index // 256) % 256
        b = (color_index % 128) * 2  # Ensure even blue and distinct
        token_to_color[op] = (r, g, b)
        color_index += 1

    # Add string and identifier colors (we'll need these)
    r = (color_index // (256 * 256)) % 256
    g = (color_index // 256) % 256
    b = (color_index % 128) * 2
    token_to_color['IDENTIFIER'] = (r, g, b)
    color_index += 1

    r = (color_index // (256 * 256)) % 256
    g = (color_index // 256) % 256
    b = (color_index % 128) * 2
    token_to_color['STRING'] = (r, g, b)
    color_index += 1

    r = (color_index // (256 * 256)) % 256
    g = (color_index // 256) % 256
    b = (color_index % 128) * 2
    token_to_color['NUMBER'] = (r, g, b)

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
    """Create a test image with embedded SimpleScript code"""
    width, height = 100, 100

    # Create a white image
    img = Image.new('RGB', (width, height), color='white')
    pixels = img.load()

    # Get color mapping
    token_to_color = create_color_mapping()

    # SimpleScript program tokens: print(42);
    tokens = [
        ('IDENTIFIER', 'print'), ('LPAREN', '('), ('NUMBER', '42'), ('RPAREN', ')'), ('SEMICOLON', ';')
    ]

    # Create a simple curve (diagonal line) - consecutive pixels
    curve_points = []
    for i in range(min(width, height) - 20):
        x, y = 10 + i, 10 + i
        if x < width and y < height:
            curve_points.append((x, y))

    # Set ONLY curve pixels to have odd red LSB (make them slightly different from white)
    for x, y in curve_points:
        # Make sure red channel has odd LSB
        r, g, b = pixels[x, y]
        pixels[x, y] = (r, g, b | 1)  # Ensure blue has odd LSB

    # Place tokens adjacent to curve points
    for i, (x, y) in enumerate(curve_points):
        if i < len(tokens):
            token_type, token_value = tokens[i]

            # Place token directly adjacent to curve pixel
            adj_x, adj_y = x + 1, y  # Directly to the right of curve pixel
            if adj_x < width and adj_y < height:
                if token_type == 'IDENTIFIER':
                    # For identifiers, use a specific identifier color
                    # Use the IDENTIFIER color from the mapping
                    color = (0, 0, 80)  # Hardcoded for demo
                    pixels[adj_x, adj_y] = (color[0], color[1], color[2] | 1)
                elif token_type == 'NUMBER':
                    # For numbers, use NUMBER color
                    color = token_to_color.get('NUMBER')
                    pixels[adj_x, adj_y] = (color[0], color[1], color[2] | 1)
                else:
                    # Use the token value directly as key
                    color = token_to_color.get(token_value)
                    if color:
                        pixels[adj_x, adj_y] = (color[0], color[1], color[2] | 1)

    return img

if __name__ == "__main__":
    img = create_test_image()
    img.save("test_script.png")
    print("Test image saved as test_script.png")
