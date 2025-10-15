from ast_nodes import *

class RuntimeError(Exception):
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"RuntimeError at line {line}, column {column}: {message}")

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def get(self, name):
        if name in self.variables:
            return self.variables[name]

        if self.parent:
            return self.parent.get(name)

        raise RuntimeError(f"Undefined variable '{name}'")

    def set(self, name, value):
        if name in self.variables:
            self.variables[name] = value
        elif self.parent:
            self.parent.set(name, value)
        else:
            self.variables[name] = value

    def define(self, name, value):
        self.variables[name] = value

class Interpreter:
    def __init__(self):
        self.environment = Environment()
        self.setup_builtins()

    def setup_builtins(self):
        # Built-in functions
        self.environment.define('print', self.builtin_print)
        self.environment.define('input', self.builtin_input)
        self.environment.define('len', self.builtin_len)
        self.environment.define('str', self.builtin_str)
        self.environment.define('int', self.builtin_int)
        self.environment.define('bool', self.builtin_bool)

    def interpret(self, program):
        try:
            return self.visit_program(program)
        except ReturnException as e:
            return e.value

    def visit_program(self, node):
        result = None
        for statement in node.statements:
            result = statement.accept(self)
        return result

    def visit_variable_declaration(self, node):
        value = node.value.accept(self) if node.value else None
        self.environment.define(node.name, value)

    def visit_assignment(self, node):
        value = node.value.accept(self)
        self.environment.set(node.name, value)

    def visit_if_statement(self, node):
        condition = node.condition.accept(self)

        if self.is_truthy(condition):
            return node.then_block.accept(self)
        elif node.else_block:
            return node.else_block.accept(self)

        return None

    def visit_while_statement(self, node):
        while self.is_truthy(node.condition.accept(self)):
            try:
                node.body.accept(self)
            except RuntimeError:
                raise  # Re-raise runtime errors

        return None

    def visit_function_definition(self, node):
        func = Function(node.name, node.parameters, node.body, self.environment)
        self.environment.define(node.name, func)

    def visit_return_statement(self, node):
        value = None
        if node.value:
            value = node.value.accept(self)
        raise ReturnException(value)

    def visit_block_statement(self, node):
        previous_env = self.environment
        self.environment = Environment(previous_env)

        result = None
        for statement in node.statements:
            result = statement.accept(self)

        self.environment = previous_env
        return result

    def visit_expression_statement(self, node):
        return node.expression.accept(self)

    def visit_binary_expression(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)

        if node.operator == '+':
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif node.operator == '-':
            return left - right
        elif node.operator == '*':
            return left * right
        elif node.operator == '/':
            if right == 0:
                raise RuntimeError("Division by zero")
            return left / right
        elif node.operator == '%':
            return left % right
        elif node.operator == '==':
            return left == right
        elif node.operator == '!=':
            return left != right
        elif node.operator == '<':
            return left < right
        elif node.operator == '>':
            return left > right
        elif node.operator == '<=':
            return left <= right
        elif node.operator == '>=':
            return left >= right
        elif node.operator == '&&':
            return self.is_truthy(left) and self.is_truthy(right)
        elif node.operator == '||':
            return self.is_truthy(left) or self.is_truthy(right)

        raise RuntimeError(f"Unknown operator: {node.operator}")

    def visit_unary_expression(self, node):
        operand = node.operand.accept(self)

        if node.operator == '!':
            return not self.is_truthy(operand)
        elif node.operator == '-':
            return -operand

        raise RuntimeError(f"Unknown unary operator: {node.operator}")

    def visit_literal(self, node):
        return node.value

    def visit_variable(self, node):
        return self.environment.get(node.name)

    def visit_function_call(self, node):
        func = self.environment.get(node.name)

        if not callable(func):
            raise RuntimeError(f"'{node.name}' is not a function")

        arguments = []
        for arg in node.arguments:
            arguments.append(arg.accept(self))

        if isinstance(func, Function):
            return func(self, arguments)
        else:
            # Built-in function
            return func(*arguments)

    def is_truthy(self, value):
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        return True

    # Built-in functions
    def builtin_print(self, *args):
        output = ' '.join(str(arg) for arg in args)
        print(output)
        return None

    def builtin_input(self, prompt=""):
        return input(prompt)

    def builtin_len(self, obj):
        return len(obj)

    def builtin_str(self, obj):
        return str(obj)

    def builtin_int(self, obj):
        try:
            return int(obj)
        except (ValueError, TypeError):
            raise RuntimeError(f"Cannot convert '{obj}' to int")

    def builtin_bool(self, obj):
        return bool(obj)

class Function:
    def __init__(self, name, parameters, body, closure):
        self.name = name
        self.parameters = parameters
        self.body = body
        self.closure = closure

    def __call__(self, interpreter, arguments):
        return self.call(interpreter, arguments)

    def call(self, interpreter, arguments):
        if len(arguments) != len(self.parameters):
            raise RuntimeError(f"Function '{self.name}' expects {len(self.parameters)} arguments, got {len(arguments)}")

        # Create new environment with closure
        previous_env = interpreter.environment
        interpreter.environment = Environment(self.closure)

        # Define parameters
        for param, arg in zip(self.parameters, arguments):
            interpreter.environment.define(param, arg)

        try:
            result = self.body.accept(interpreter)
            return result
        except ReturnException as e:
            return e.value
        finally:
            interpreter.environment = previous_env
