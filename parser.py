from lexer import TokenType
from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None

    def advance(self):
        self.position += 1
        self.current_token = self.tokens[self.position] if self.position < len(self.tokens) else None

    def peek(self, offset=1):
        peek_pos = self.position + offset
        return self.tokens[peek_pos] if peek_pos < len(self.tokens) else None

    def match(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        return None

    def expect(self, token_type):
        token = self.match(token_type)
        if not token:
            raise ValueError(f"Expected {token_type} at line {self.current_token.line}, column {self.current_token.column}")
        return token

    def parse_program(self):
        statements = []
        while self.current_token and self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)

        return Program(statements, line=1, column=1)

    def parse_statement(self):
        if self.match(TokenType.LET):
            return self.parse_variable_declaration()
        elif self.match(TokenType.IF):
            return self.parse_if_statement()
        elif self.match(TokenType.WHILE):
            return self.parse_while_statement()
        elif self.match(TokenType.DEF):
            return self.parse_function_definition()
        elif self.match(TokenType.RETURN):
            return self.parse_return_statement()
        elif self.current_token.type == TokenType.IDENTIFIER:
            # Could be assignment or function call
            if self.peek() and self.peek().type == TokenType.ASSIGN:
                return self.parse_assignment()
            else:
                # Function call as statement
                expr = self.parse_expression()
                self.expect(TokenType.SEMICOLON)
                return ExpressionStatement(expr)
        else:
            # Try to parse as expression statement
            expr = self.parse_expression()
            if expr:
                self.expect(TokenType.SEMICOLON)
                return ExpressionStatement(expr)
            return None

    def parse_variable_declaration(self):
        name_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return VariableDeclaration(name_token.value, value, name_token.line, name_token.column)

    def parse_assignment(self):
        name_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return Assignment(name_token.value, value, name_token.line, name_token.column)

    def parse_if_statement(self):
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)

        then_block = self.parse_block()

        else_block = None
        if self.match(TokenType.ELSE):
            else_block = self.parse_block()

        return IfStatement(condition, then_block, else_block)

    def parse_while_statement(self):
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return WhileStatement(condition, body)

    def parse_function_definition(self):
        name_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.LPAREN)

        parameters = []
        if self.current_token.type != TokenType.RPAREN:
            param_token = self.expect(TokenType.IDENTIFIER)
            parameters.append(param_token.value)

            while self.match(TokenType.COMMA):
                param_token = self.expect(TokenType.IDENTIFIER)
                parameters.append(param_token.value)

        self.expect(TokenType.RPAREN)
        body = self.parse_block()

        return FunctionDefinition(name_token.value, parameters, body, name_token.line, name_token.column)

    def parse_return_statement(self):
        value = None
        if self.current_token.type != TokenType.SEMICOLON:
            value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return ReturnStatement(value)

    def parse_block(self):
        statements = []

        if self.match(TokenType.LBRACE):
            while self.current_token and self.current_token.type != TokenType.RBRACE:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
            self.expect(TokenType.RBRACE)
        else:
            # Single statement block
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)

        return BlockStatement(statements)

    def parse_expression(self):
        return self.parse_or_expression()

    def parse_or_expression(self):
        expr = self.parse_and_expression()

        while self.match(TokenType.OR):
            operator = "||"
            right = self.parse_and_expression()
            expr = BinaryExpression(expr, operator, right)

        return expr

    def parse_and_expression(self):
        expr = self.parse_equality_expression()

        while self.match(TokenType.AND):
            operator = "&&"
            right = self.parse_equality_expression()
            expr = BinaryExpression(expr, operator, right)

        return expr

    def parse_equality_expression(self):
        expr = self.parse_comparison_expression()

        while True:
            if self.match(TokenType.EQUAL):
                operator = "=="
                right = self.parse_comparison_expression()
                expr = BinaryExpression(expr, operator, right)
            elif self.match(TokenType.NOT_EQUAL):
                operator = "!="
                right = self.parse_comparison_expression()
                expr = BinaryExpression(expr, operator, right)
            else:
                break

        return expr

    def parse_comparison_expression(self):
        expr = self.parse_additive_expression()

        while True:
            if self.match(TokenType.LESS):
                operator = "<"
                right = self.parse_additive_expression()
                expr = BinaryExpression(expr, operator, right)
            elif self.match(TokenType.GREATER):
                operator = ">"
                right = self.parse_additive_expression()
                expr = BinaryExpression(expr, operator, right)
            elif self.match(TokenType.LESS_EQUAL):
                operator = "<="
                right = self.parse_additive_expression()
                expr = BinaryExpression(expr, operator, right)
            elif self.match(TokenType.GREATER_EQUAL):
                operator = ">="
                right = self.parse_additive_expression()
                expr = BinaryExpression(expr, operator, right)
            else:
                break

        return expr

    def parse_additive_expression(self):
        expr = self.parse_multiplicative_expression()

        while True:
            if self.match(TokenType.PLUS):
                operator = "+"
                right = self.parse_multiplicative_expression()
                expr = BinaryExpression(expr, operator, right)
            elif self.match(TokenType.MINUS):
                operator = "-"
                right = self.parse_multiplicative_expression()
                expr = BinaryExpression(expr, operator, right)
            else:
                break

        return expr

    def parse_multiplicative_expression(self):
        expr = self.parse_unary_expression()

        while True:
            if self.match(TokenType.MULTIPLY):
                operator = "*"
                right = self.parse_unary_expression()
                expr = BinaryExpression(expr, operator, right)
            elif self.match(TokenType.DIVIDE):
                operator = "/"
                right = self.parse_unary_expression()
                expr = BinaryExpression(expr, operator, right)
            elif self.match(TokenType.MODULO):
                operator = "%"
                right = self.parse_unary_expression()
                expr = BinaryExpression(expr, operator, right)
            else:
                break

        return expr

    def parse_unary_expression(self):
        if self.match(TokenType.NOT):
            operator = "!"
            operand = self.parse_unary_expression()
            return UnaryExpression(operator, operand)
        elif self.match(TokenType.MINUS):
            operator = "-"
            operand = self.parse_unary_expression()
            return UnaryExpression(operator, operand)

        return self.parse_primary_expression()

    def parse_primary_expression(self):
        token = self.current_token

        if self.match(TokenType.NUMBER):
            return NumberLiteral(token.value, token.line, token.column)
        elif self.match(TokenType.STRING):
            return StringLiteral(token.value, token.line, token.column)
        elif self.match(TokenType.TRUE):
            return BooleanLiteral(True, token.line, token.column)
        elif self.match(TokenType.FALSE):
            return BooleanLiteral(False, token.line, token.column)
        elif self.match(TokenType.IDENTIFIER):
            if self.current_token and self.current_token.type == TokenType.LPAREN:
                # Function call
                return self.parse_function_call(token.value)
            else:
                # Variable reference
                return Variable(token.value, token.line, token.column)
        elif self.match(TokenType.LPAREN):
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr

        return None

    def parse_function_call(self, name):
        self.expect(TokenType.LPAREN)

        arguments = []
        if self.current_token.type != TokenType.RPAREN:
            arguments.append(self.parse_expression())

            while self.match(TokenType.COMMA):
                arguments.append(self.parse_expression())

        self.expect(TokenType.RPAREN)

        return FunctionCall(name, arguments)
