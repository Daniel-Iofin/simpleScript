class ASTNode:
    def __init__(self, line=None, column=None):
        self.line = line
        self.column = column

    def accept(self, visitor):
        raise NotImplementedError

class Program(ASTNode):
    def __init__(self, statements, line=None, column=None):
        super().__init__(line, column)
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_program(self)

class Statement(ASTNode):
    pass

class Expression(ASTNode):
    def __init__(self, line=None, column=None):
        super().__init__(line, column)

class VariableDeclaration(Statement):
    def __init__(self, name, value, line=None, column=None):
        super().__init__(line, column)
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_variable_declaration(self)

class Assignment(Statement):
    def __init__(self, name, value, line=None, column=None):
        super().__init__(line, column)
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assignment(self)

class IfStatement(Statement):
    def __init__(self, condition, then_block, else_block=None, line=None, column=None):
        super().__init__(line, column)
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def accept(self, visitor):
        return visitor.visit_if_statement(self)

class WhileStatement(Statement):
    def __init__(self, condition, body, line=None, column=None):
        super().__init__(line, column)
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_statement(self)

class ForStatement(Statement):
    def __init__(self, initializer, condition, increment, body, line=None, column=None):
        super().__init__(line, column)
        self.initializer = initializer
        self.condition = condition
        self.increment = increment
        self.body = body

    def accept(self, visitor):
        return visitor.visit_for_statement(self)

class BreakStatement(Statement):
    def __init__(self, line=None, column=None):
        super().__init__(line, column)

    def accept(self, visitor):
        return visitor.visit_break_statement(self)

class ContinueStatement(Statement):
    def __init__(self, line=None, column=None):
        super().__init__(line, column)

    def accept(self, visitor):
        return visitor.visit_continue_statement(self)

class FunctionDefinition(Statement):
    def __init__(self, name, parameters, body, line=None, column=None):
        super().__init__(line, column)
        self.name = name
        self.parameters = parameters
        self.body = body

    def accept(self, visitor):
        return visitor.visit_function_definition(self)

class ReturnStatement(Statement):
    def __init__(self, value=None, line=None, column=None):
        super().__init__(line, column)
        self.value = value

    def accept(self, visitor):
        return visitor.visit_return_statement(self)

class BlockStatement(Statement):
    def __init__(self, statements, line=None, column=None):
        super().__init__(line, column)
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_statement(self)

class ExpressionStatement(Statement):
    def __init__(self, expression, line=None, column=None):
        super().__init__(line, column)
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_statement(self)

class BinaryExpression(Expression):
    def __init__(self, left, operator, right, line=None, column=None):
        super().__init__(line, column)
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expression(self)

class UnaryExpression(Expression):
    def __init__(self, operator, operand, line=None, column=None):
        super().__init__(line, column)
        self.operator = operator
        self.operand = operand

    def accept(self, visitor):
        return visitor.visit_unary_expression(self)

class Literal(Expression):
    def __init__(self, value, line=None, column=None):
        super().__init__(line, column)
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal(self)

class Variable(Expression):
    def __init__(self, name, line=None, column=None):
        super().__init__(line, column)
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable(self)

class FunctionCall(Expression):
    def __init__(self, name, arguments, line=None, column=None):
        super().__init__(line, column)
        self.name = name
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_function_call(self)

class BooleanLiteral(Literal):
    def __init__(self, value, line=None, column=None):
        super().__init__(value, line, column)

class NumberLiteral(Literal):
    def __init__(self, value, line=None, column=None):
        super().__init__(float(value) if '.' in str(value) else int(value), line, column)

class StringLiteral(Literal):
    def __init__(self, value, line=None, column=None):
        super().__init__(value, line, column)

class ArrayLiteral(Expression):
    def __init__(self, elements, line=None, column=None):
        super().__init__(line, column)
        self.elements = elements

    def accept(self, visitor):
        return visitor.visit_array_literal(self)

class ArrayAccess(Expression):
    def __init__(self, array, index, line=None, column=None):
        super().__init__(line, column)
        self.array = array
        self.index = index

    def accept(self, visitor):
        return visitor.visit_array_access(self)

class ArrayAssignment(Statement):
    def __init__(self, array, index, value, line=None, column=None):
        super().__init__(line, column)
        self.array = array
        self.index = index
        self.value = value

    def accept(self, visitor):
        return visitor.visit_array_assignment(self)

class PrefixIncrement(Expression):
    def __init__(self, operand, line=None, column=None):
        super().__init__(line, column)
        self.operand = operand

    def accept(self, visitor):
        return visitor.visit_prefix_increment(self)

class PrefixDecrement(Expression):
    def __init__(self, operand, line=None, column=None):
        super().__init__(line, column)
        self.operand = operand

    def accept(self, visitor):
        return visitor.visit_prefix_decrement(self)

class PostfixIncrement(Expression):
    def __init__(self, operand, line=None, column=None):
        super().__init__(line, column)
        self.operand = operand

    def accept(self, visitor):
        return visitor.visit_postfix_increment(self)

class PostfixDecrement(Expression):
    def __init__(self, operand, line=None, column=None):
        super().__init__(line, column)
        self.operand = operand

    def accept(self, visitor):
        return visitor.visit_postfix_decrement(self)
