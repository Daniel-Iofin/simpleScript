import re

class TokenType:
    # Keywords
    LET = "LET"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    DEF = "DEF"
    RETURN = "RETURN"
    TRUE = "TRUE"
    FALSE = "FALSE"

    # Literals
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"

    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULO = "MODULO"
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS = "LESS"
    GREATER = "GREATER"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER_EQUAL = "GREATER_EQUAL"
    ASSIGN = "ASSIGN"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"

    # Delimiters
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"

    # Special
    EOF = "EOF"
    COMMENT = "COMMENT"

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', line={self.line}, col={self.column})"

class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source[0] if self.source else None

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.position += 1
        self.current_char = self.source[self.position] if self.position < len(self.source) else None

    def peek(self):
        peek_pos = self.position + 1
        return self.source[peek_pos] if peek_pos < len(self.source) else None

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        if self.current_char == '/' and self.peek() == '/':
            # Single line comment
            while self.current_char and self.current_char != '\n':
                self.advance()
            return True
        elif self.current_char == '/' and self.peek() == '*':
            # Multi-line comment
            self.advance()  # skip /
            self.advance()  # skip *
            while self.current_char:
                if self.current_char == '*' and self.peek() == '/':
                    self.advance()  # skip *
                    self.advance()  # skip /
                    break
                self.advance()
            return True
        return False

    def read_number(self):
        start_col = self.column
        num_str = ''
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            num_str += self.current_char
            self.advance()

        if num_str.count('.') > 1:
            raise ValueError(f"Invalid number format at line {self.line}, column {start_col}")

        return Token(TokenType.NUMBER, num_str, self.line, start_col)

    def read_string(self):
        start_col = self.column
        self.advance()  # skip opening quote
        string_val = ''

        while self.current_char and self.current_char != '"':
            if self.current_char == '\\':
                self.advance()
                if self.current_char == 'n':
                    string_val += '\n'
                elif self.current_char == 't':
                    string_val += '\t'
                elif self.current_char == '"':
                    string_val += '"'
                elif self.current_char == '\\':
                    string_val += '\\'
                else:
                    string_val += self.current_char
            else:
                string_val += self.current_char
            self.advance()

        if not self.current_char:
            raise ValueError(f"Unterminated string at line {self.line}, column {start_col}")

        self.advance()  # skip closing quote
        return Token(TokenType.STRING, string_val, self.line, start_col)

    def read_identifier(self):
        start_col = self.column
        ident_str = ''

        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            ident_str += self.current_char
            self.advance()

        # Check if it's a keyword
        keywords = {
            'let': TokenType.LET,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'def': TokenType.DEF,
            'return': TokenType.RETURN,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
        }

        token_type = keywords.get(ident_str, TokenType.IDENTIFIER)
        return Token(token_type, ident_str, self.line, start_col)

    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.skip_comment():
                continue

            if self.current_char.isdigit():
                return self.read_number()

            if self.current_char == '"':
                return self.read_string()

            if self.current_char.isalpha() or self.current_char == '_':
                return self.read_identifier()

            # Two-character operators
            if self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.EQUAL, '==', self.line, self.column - 1)

            if self.current_char == '!' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.NOT_EQUAL, '!=', self.line, self.column - 1)

            if self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.LESS_EQUAL, '<=', self.line, self.column - 1)

            if self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.GREATER_EQUAL, '>=', self.line, self.column - 1)

            if self.current_char == '&' and self.peek() == '&':
                self.advance()
                self.advance()
                return Token(TokenType.AND, '&&', self.line, self.column - 1)

            if self.current_char == '|' and self.peek() == '|':
                self.advance()
                self.advance()
                return Token(TokenType.OR, '||', self.line, self.column - 1)

            # Single-character operators and delimiters
            char_to_token = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '%': TokenType.MODULO,
                '=': TokenType.ASSIGN,
                '<': TokenType.LESS,
                '>': TokenType.GREATER,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                ';': TokenType.SEMICOLON,
                ',': TokenType.COMMA,
            }

            if self.current_char in char_to_token:
                token = Token(char_to_token[self.current_char], self.current_char, self.line, self.column)
                self.advance()
                return token

            raise ValueError(f"Unexpected character '{self.current_char}' at line {self.line}, column {self.column}")

        return Token(TokenType.EOF, '', self.line, self.column)

    def tokenize(self):
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens
