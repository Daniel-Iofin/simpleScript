from PIL import Image
import math
from lexer import Token, TokenType

class ImageLexer:
    def __init__(self, image_path):
        self.image = Image.open(image_path)
        self.width, self.height = self.image.size
        self.pixels = self.image.load()
        self.color_to_token = self._create_color_mapping()
        self.visited = set()

    def _is_token_start(self, pixel):
        """Check if this pixel marks the start of a token (odd LSB in blue)"""
        r, g, b = pixel[:3]  # Handle RGBA by taking first 3 channels
        return (b & 1) == 1

    def _is_literal_continuation(self, pixel):
        """Check if this pixel is part of a literal value (green channel = 1)"""
        r, g, b = pixel[:3]  # Handle RGBA by taking first 3 channels
        return g == 1 and (b & 1) == 0  # Green = 1, blue LSB clear

    def _encode_string(self, s):
        """Encode a string into a sequence of RGB values"""
        colors = []
        for char in s:
            ascii_val = ord(char)
            # Use R channel for ASCII value, G and B for future extensions
            colors.append((ascii_val, 0, 0))
        # Add null terminator
        colors.append((0, 0, 0))
        return colors

    def _decode_string(self, colors):
        """Decode a sequence of RGB values back to a string"""
        result = ""
        for r, g, b in colors:
            if r == 0:  # End marker
                break
            result += chr(r)
        return result

    def _encode_number(self, num_str):
        """Encode a number string into RGB values"""
        # Convert the string representation to a sequence of ASCII values
        return self._encode_string(num_str)

    def _decode_number(self, colors):
        """Decode RGB values back to a number string"""
        return self._decode_string(colors)

    def _encode_identifier(self, ident):
        """Encode an identifier into RGB values"""
        return self._encode_string(ident)

    def _decode_identifier(self, colors):
        """Decode RGB values back to an identifier"""
        return self._decode_string(colors)

    def _decode_literal_value(self, start_x, start_y, token_type):
        """Decode a literal value starting from the given position"""
        colors = []
        x, y = start_x, start_y

        # Move to the next pixel (right, then down if at edge)
        x += 1
        if x >= self.width:
            x = 0
            y += 1
            if y >= self.height:
                return ""  # No more space

        # Read pixels until we find a pixel that is not a literal continuation (end of literal)
        while y < self.height and self._is_literal_continuation(self.pixels[x, y]):
            pixel_color = self.pixels[x, y][:3]
            # For literal encoding, use the raw RGB values (red channel contains the data)
            colors.append(pixel_color)

            # Move to next pixel
            x += 1
            if x >= self.width:
                x = 0
                y += 1
                if y >= self.height:
                    break

        # Decode based on token type
        if token_type == TokenType.STRING:
            return self._decode_string(colors)
        elif token_type == TokenType.IDENTIFIER:
            return self._decode_identifier(colors)
        elif token_type == TokenType.NUMBER:
            return self._decode_number(colors)
        elif token_type == TokenType.COMMENT:
            return self._decode_string(colors)  # Comments are just strings
        else:
            return ""

    def _create_color_mapping(self):
        """Create a mapping from RGB colors to tokens - must match image generator"""
        mapping = {}

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

        # Single character operators (NOT)
        single_operators = [
            ('!', TokenType.NOT),
        ]

        # Generate colors systematically - same as image generator
        color_index = 0

        # Keywords
        for keyword, token_type in keywords:
            r = (color_index // (256 * 256)) % 256
            g = (color_index // 256) % 256
            b = (color_index % 128) * 2  # Ensure even blue and distinct
            mapping[(r, g, b)] = (token_type, keyword)
            color_index += 1

        # Single characters
        for char, token_type in single_chars:
            r = (color_index // (256 * 256)) % 256
            g = (color_index // 256) % 256
            b = (color_index % 128) * 2  # Ensure even blue and distinct
            mapping[(r, g, b)] = (token_type, char)
            color_index += 1

        # Two character operators
        for op, token_type in two_chars:
            r = (color_index // (256 * 256)) % 256
            g = (color_index // 256) % 256
            b = (color_index % 128) * 2  # Ensure even blue and distinct
            mapping[(r, g, b)] = (token_type, op)
            color_index += 1

        # Single character operators
        for op, token_type in single_operators:
            r = (color_index // (256 * 256)) % 256
            g = (color_index // 256) % 256
            b = (color_index % 128) * 2  # Ensure even blue and distinct
            mapping[(r, g, b)] = (token_type, op)
            color_index += 1

        # Literal token types (base colors for encoding values)
        r = (color_index // (256 * 256)) % 256
        g = (color_index // 256) % 256
        b = (color_index % 128) * 2
        mapping[(r, g, b)] = (TokenType.STRING, 'STRING_BASE')
        color_index += 1

        r = (color_index // (256 * 256)) % 256
        g = (color_index // 256) % 256
        b = (color_index % 128) * 2
        mapping[(r, g, b)] = (TokenType.IDENTIFIER, 'IDENTIFIER_BASE')
        color_index += 1

        r = (color_index // (256 * 256)) % 256
        g = (color_index // 256) % 256
        b = (color_index % 128) * 2
        mapping[(r, g, b)] = (TokenType.NUMBER, 'NUMBER_BASE')
        color_index += 1

        # Special tokens - EOF
        r = (color_index // (256 * 256)) % 256
        g = (color_index // 256) % 256
        b = (color_index % 128) * 2
        mapping[(r, g, b)] = (TokenType.EOF, '')
        color_index += 1

        # Comments (we'll handle these specially)
        r = (color_index // (256 * 256)) % 256
        g = (color_index // 256) % 256
        b = (color_index % 128) * 2
        mapping[(r, g, b)] = (TokenType.COMMENT, 'COMMENT_BASE')
        color_index += 1


        return mapping

    def _get_adjacent_pixels(self, x, y):
        """Get adjacent pixels (4-way connectivity)"""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        adjacent = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                adjacent.append((nx, ny))

        return adjacent

    def _find_curve_start(self):
        """Find the starting point of the backbone curve"""
        # Start from the known backbone start position (20, 20)
        start_x, start_y = 20, 20
        if (start_x < self.width and start_y < self.height and
            self._is_token_start(self.pixels[start_x, start_y]) and
            (start_x, start_y) not in self.visited):
            return (start_x, start_y)

        # Fallback: find any backbone pixel
        for x in range(self.width):
            for y in range(self.height):
                if self._is_token_start(self.pixels[x, y]) and (x, y) not in self.visited:
                    return (x, y)
        return None

    def _follow_curve(self, start_x, start_y):
        """Follow the backbone curve and collect tokens from adjacent pixels"""
        tokens = []
        current_pos = (start_x, start_y)
        self.visited.add(current_pos)

        # Continue following until we can't find the next backbone pixel
        while True:
            x, y = current_pos

            # Check adjacent pixels for token data - only check BELOW adjacent pixel
            # This ensures each token is associated with exactly one backbone pixel
            adj_x, adj_y = x, y + 1  # Only check pixel below
            if adj_x < self.width and adj_y < self.height:
                pixel_color = self.pixels[adj_x, adj_y][:3]
                base_color = pixel_color  # Token pixels use base colors directly

                if base_color in self.color_to_token:
                    token_type, base_value = self.color_to_token[base_color]

                    # Handle literal tokens that need additional decoding
                    if token_type in [TokenType.STRING, TokenType.IDENTIFIER, TokenType.NUMBER]:
                        value = self._decode_literal_value(adj_x, adj_y, token_type)
                    elif token_type == TokenType.COMMENT:
                        value = self._decode_literal_value(adj_x, adj_y, token_type)
                    else:
                        value = base_value

                    tokens.append(Token(token_type, value, adj_y, adj_x))

            # Find next backbone pixel
            next_pos = None
            min_distance = float('inf')

            for adj_x, adj_y in self._get_adjacent_pixels(x, y):
                if (adj_x < self.width and adj_y < self.height and
                    self._is_token_start(self.pixels[adj_x, adj_y]) and
                    (adj_x, adj_y) not in self.visited):
                    # Prefer continuing in a consistent direction (right/down)
                    distance = (adj_x - x) * 10 + (adj_y - y)  # Weight x direction more
                    if distance < min_distance:
                        min_distance = distance
                        next_pos = (adj_x, adj_y)

            if next_pos is None:
                break

            current_pos = next_pos
            self.visited.add(current_pos)

        return tokens

    def tokenize(self):
        """Main tokenization method"""
        tokens = []

        # Find and follow all curves (backbones)
        while True:
            start = self._find_curve_start()
            if start is None:
                break

            curve_tokens = self._follow_curve(*start)
            tokens.extend(curve_tokens)

        # Add EOF token at the end
        tokens.append(Token(TokenType.EOF, '', self.height, self.width))

        return tokens
