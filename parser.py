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
        elif self.match(TokenType.FOR):
            return self.parse_for_statement()
        elif self.match(TokenType.BREAK):
            return self.parse_break_statement()
        elif self.match(TokenType.CONTINUE):
            return self.parse_continue_statement()
        elif self.match(TokenType.DEF):
            return self.parse_function_definition()
        elif self.match(TokenType.RETURN):
            return self.parse_return_statement()
        elif self.current_token.type == TokenType.IDENTIFIER:
            # Could be assignment, array assignment, or function call
            name_token = self.expect(TokenType.IDENTIFIER)

            if self.current_token.type == TokenType.LBRACKET:
                # Array assignment: arr[index] op= value
                self.expect(TokenType.LBRACKET)
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET)

                # Check for compound assignment
                compound_op = None
                if self.match(TokenType.PLUS_ASSIGN):
                    compound_op = '+'
                elif self.match(TokenType.MINUS_ASSIGN):
                    compound_op = '-'
                elif self.match(TokenType.MULTIPLY_ASSIGN):
                    compound_op = '*'
                elif self.match(TokenType.DIVIDE_ASSIGN):
                    compound_op = '/'
                elif self.match(TokenType.MODULO_ASSIGN):
                    compound_op = '%'
                elif self.match(TokenType.ASSIGN):
                    pass  # Regular assignment
                else:
                    raise ValueError(f"Expected assignment operator at line {self.current_token.line}, column {self.current_token.column}")

                value_expr = self.parse_expression()
                self.expect(TokenType.SEMICOLON)

                array_var = Variable(name_token.value)
                array_access = ArrayAccess(array_var, index)

                if compound_op:
                    # Compound assignment: arr[index] op= value becomes arr[index] = arr[index] op value
                    binary_expr = BinaryExpression(array_access, compound_op, value_expr)
                    return ArrayAssignment(array_var, index, binary_expr, name_token.line, name_token.column)
                else:
                    # Regular assignment
                    return ArrayAssignment(array_var, index, value_expr, name_token.line, name_token.column)
            else:
                # Check for compound assignment or regular assignment
                compound_op = None
                if self.match(TokenType.PLUS_ASSIGN):
                    compound_op = '+'
                elif self.match(TokenType.MINUS_ASSIGN):
                    compound_op = '-'
                elif self.match(TokenType.MULTIPLY_ASSIGN):
                    compound_op = '*'
                elif self.match(TokenType.DIVIDE_ASSIGN):
                    compound_op = '/'
                elif self.match(TokenType.MODULO_ASSIGN):
                    compound_op = '%'
                elif self.match(TokenType.ASSIGN):
                    pass  # Regular assignment, compound_op remains None
                else:
                    # Not an assignment, put back the token and parse as expression
                    self.position -= 1
                    self.current_token = name_token
                    expr = self.parse_expression()
                    self.expect(TokenType.SEMICOLON)
                    return ExpressionStatement(expr)

                # This is an assignment (regular or compound)
                value_expr = self.parse_expression()
                self.expect(TokenType.SEMICOLON)

                if compound_op:
                    # Compound assignment: var op= value becomes var = var op value
                    var_expr = Variable(name_token.value, name_token.line, name_token.column)
                    binary_expr = BinaryExpression(var_expr, compound_op, value_expr)
                    return Assignment(name_token.value, binary_expr, name_token.line, name_token.column)
                else:
                    # Regular assignment
                    return Assignment(name_token.value, value_expr, name_token.line, name_token.column)
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

    def parse_assignment_from_name(self, name_token):
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

    def parse_for_statement(self):
        self.expect(TokenType.LPAREN)

        # Parse initializer (variable declaration or assignment or empty)
        initializer = None
        if self.match(TokenType.LET):
            # Parse variable declaration without semicolon
            name_token = self.expect(TokenType.IDENTIFIER)
            self.expect(TokenType.ASSIGN)
            value = self.parse_expression()
            initializer = VariableDeclaration(name_token.value, value, name_token.line, name_token.column)
        elif self.current_token.type == TokenType.IDENTIFIER:
            if self.peek() and self.peek().type == TokenType.ASSIGN:
                # Parse assignment expression without semicolon
                name_token = self.expect(TokenType.IDENTIFIER)
                self.expect(TokenType.ASSIGN)
                value = self.parse_expression()
                initializer = Assignment(name_token.value, value, name_token.line, name_token.column)
            else:
                # Empty initializer
                pass
        # If semicolon, it's empty initializer

        self.expect(TokenType.SEMICOLON)

        # Parse condition
        condition = None
        if self.current_token.type != TokenType.SEMICOLON:
            condition = self.parse_expression()
        self.expect(TokenType.SEMICOLON)

        # Parse increment
        increment = None
        if self.current_token.type != TokenType.RPAREN:
            increment = self.parse_expression()
        self.expect(TokenType.RPAREN)

        body = self.parse_block()
        return ForStatement(initializer, condition, increment, body)

    def parse_break_statement(self):
        self.expect(TokenType.SEMICOLON)
        return BreakStatement()

    def parse_continue_statement(self):
        self.expect(TokenType.SEMICOLON)
        return ContinueStatement()

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
        elif self.match(TokenType.PLUS_PLUS):
            operand = self.parse_unary_expression()
            return PrefixIncrement(operand)
        elif self.match(TokenType.MINUS_MINUS):
            operand = self.parse_unary_expression()
            return PrefixDecrement(operand)

        return self.parse_primary_expression()

    def parse_primary_expression(self):
        token = self.current_token

        if self.match(TokenType.NUMBER):
            return self.parse_postfix_operators(NumberLiteral(token.value, token.line, token.column))
        elif self.match(TokenType.STRING):
            return self.parse_postfix_operators(StringLiteral(token.value, token.line, token.column))
        elif self.match(TokenType.TRUE):
            return self.parse_postfix_operators(BooleanLiteral(True, token.line, token.column))
        elif self.match(TokenType.FALSE):
            return self.parse_postfix_operators(BooleanLiteral(False, token.line, token.column))
        elif self.match(TokenType.LBRACKET):
            return self.parse_array_literal()
        elif self.match(TokenType.IDENTIFIER):
            if self.current_token and self.current_token.type == TokenType.LPAREN:
                # Function call
                return self.parse_postfix_operators(self.parse_function_call(token.value))
            elif self.current_token and self.current_token.type == TokenType.LBRACKET:
                # Array access
                return self.parse_postfix_operators(self.parse_array_access(token.value))
            else:
                # Variable reference
                return self.parse_postfix_operators(Variable(token.value, token.line, token.column))
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

    def parse_postfix_operators(self, expr):
        while True:
            if self.match(TokenType.PLUS_PLUS):
                expr = PostfixIncrement(expr)
            elif self.match(TokenType.MINUS_MINUS):
                expr = PostfixDecrement(expr)
            else:
                break
        return expr

    def parse_array_literal(self):
        elements = []

        if self.current_token.type != TokenType.RBRACKET:
            elements.append(self.parse_expression())

            while self.match(TokenType.COMMA):
                elements.append(self.parse_expression())

        self.expect(TokenType.RBRACKET)
        return ArrayLiteral(elements)

    def parse_array_access(self, array_name):
        self.expect(TokenType.LBRACKET)
        index = self.parse_expression()
        self.expect(TokenType.RBRACKET)

        array_var = Variable(array_name)
        return ArrayAccess(array_var, index)
