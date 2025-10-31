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

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

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

        # Array functions
        self.environment.define('push', self.builtin_push)
        self.environment.define('pop', self.builtin_pop)
        self.environment.define('append', self.builtin_push)  # alias for push
        self.environment.define('join', self.builtin_join)
        self.environment.define('slice', self.builtin_slice)

        # Math functions
        self.environment.define('abs', self.builtin_abs)
        self.environment.define('pow', self.builtin_pow)
        self.environment.define('sqrt', self.builtin_sqrt)
        self.environment.define('floor', self.builtin_floor)
        self.environment.define('ceil', self.builtin_ceil)
        self.environment.define('round', self.builtin_round)
        self.environment.define('min', self.builtin_min)
        self.environment.define('max', self.builtin_max)

        # String functions
        self.environment.define('substring', self.builtin_substring)
        self.environment.define('replace', self.builtin_replace)
        self.environment.define('split', self.builtin_split)
        self.environment.define('tolower', self.builtin_tolower)
        self.environment.define('toupper', self.builtin_toupper)
        self.environment.define('startswith', self.builtin_startswith)
        self.environment.define('endswith', self.builtin_endswith)

        # Utility functions
        self.environment.define('range', self.builtin_range)
        self.environment.define('type', self.builtin_type)

    def interpret(self, program):
        try:
            return self.visit_program(program)
        except ReturnException as e:
            return e.value
        except (BreakException, ContinueException):
            raise RuntimeError("break or continue outside of loop")

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
            except BreakException:
                break
            except ContinueException:
                continue
            except RuntimeError:
                raise  # Re-raise runtime errors

        return None

    def visit_for_statement(self, node):
        # Execute initializer
        if node.initializer:
            node.initializer.accept(self)

        while True:
            # Check condition
            if node.condition:
                if not self.is_truthy(node.condition.accept(self)):
                    break
            else:
                # No condition means infinite loop (condition is always true)
                pass

            try:
                # Execute body
                node.body.accept(self)
            except BreakException:
                break
            except ContinueException:
                # Execute increment and continue
                if node.increment:
                    node.increment.accept(self)
                continue
            except RuntimeError:
                raise  # Re-raise runtime errors

            # Execute increment
            if node.increment:
                node.increment.accept(self)

        return None

    def visit_break_statement(self, node):
        raise BreakException()

    def visit_continue_statement(self, node):
        raise ContinueException()

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

    def visit_array_literal(self, node):
        elements = []
        for element in node.elements:
            elements.append(element.accept(self))
        return elements

    def visit_array_access(self, node):
        array = node.array.accept(self)
        index = node.index.accept(self)

        if not isinstance(array, list):
            raise RuntimeError("Cannot index into non-array value")

        if not isinstance(index, int):
            raise RuntimeError("Array index must be an integer")

        if index < 0 or index >= len(array):
            raise RuntimeError(f"Array index {index} out of bounds")

        return array[index]

    def visit_array_assignment(self, node):
        array = node.array.accept(self)
        index = node.index.accept(self)
        value = node.value.accept(self)

        if not isinstance(array, list):
            raise RuntimeError("Cannot index into non-array value")

        if not isinstance(index, int):
            raise RuntimeError("Array index must be an integer")

        if index < 0 or index >= len(array):
            raise RuntimeError(f"Array index {index} out of bounds")

        array[index] = value

    def visit_prefix_increment(self, node):
        if not isinstance(node.operand, Variable):
            raise RuntimeError("Increment operator requires a variable")
        var_name = node.operand.name
        current_value = self.environment.get(var_name)
        if not isinstance(current_value, (int, float)):
            raise RuntimeError("Increment operator requires a numeric value")
        new_value = current_value + 1
        self.environment.set(var_name, new_value)
        return new_value

    def visit_prefix_decrement(self, node):
        if not isinstance(node.operand, Variable):
            raise RuntimeError("Decrement operator requires a variable")
        var_name = node.operand.name
        current_value = self.environment.get(var_name)
        if not isinstance(current_value, (int, float)):
            raise RuntimeError("Decrement operator requires a numeric value")
        new_value = current_value - 1
        self.environment.set(var_name, new_value)
        return new_value

    def visit_postfix_increment(self, node):
        if not isinstance(node.operand, Variable):
            raise RuntimeError("Increment operator requires a variable")
        var_name = node.operand.name
        current_value = self.environment.get(var_name)
        if not isinstance(current_value, (int, float)):
            raise RuntimeError("Increment operator requires a numeric value")
        self.environment.set(var_name, current_value + 1)
        return current_value

    def visit_postfix_decrement(self, node):
        if not isinstance(node.operand, Variable):
            raise RuntimeError("Decrement operator requires a variable")
        var_name = node.operand.name
        current_value = self.environment.get(var_name)
        if not isinstance(current_value, (int, float)):
            raise RuntimeError("Decrement operator requires a numeric value")
        self.environment.set(var_name, current_value - 1)
        return current_value

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

    # Array built-in functions
    def builtin_push(self, array, value):
        if not isinstance(array, list):
            raise RuntimeError("push() requires an array as first argument")
        array.append(value)
        return array

    def builtin_pop(self, array):
        if not isinstance(array, list):
            raise RuntimeError("pop() requires an array as argument")
        if len(array) == 0:
            raise RuntimeError("Cannot pop from empty array")
        return array.pop()

    def builtin_join(self, array, separator=""):
        if not isinstance(array, list):
            raise RuntimeError("join() requires an array as first argument")
        return separator.join(str(item) for item in array)

    def builtin_slice(self, array, start=0, end=None):
        if not isinstance(array, list):
            raise RuntimeError("slice() requires an array as first argument")
        if end is None:
            end = len(array)
        return array[start:end]

    # Math functions
    def builtin_abs(self, x):
        try:
            return abs(float(x))
        except (ValueError, TypeError):
            raise RuntimeError(f"abs() requires a numeric argument")

    def builtin_pow(self, base, exp):
        try:
            return float(base) ** float(exp)
        except (ValueError, TypeError, OverflowError):
            raise RuntimeError(f"pow() requires numeric arguments")

    def builtin_sqrt(self, x):
        try:
            import math
            return math.sqrt(float(x))
        except (ValueError, TypeError):
            raise RuntimeError(f"sqrt() requires a non-negative numeric argument")

    def builtin_floor(self, x):
        try:
            import math
            return math.floor(float(x))
        except (ValueError, TypeError):
            raise RuntimeError(f"floor() requires a numeric argument")

    def builtin_ceil(self, x):
        try:
            import math
            return math.ceil(float(x))
        except (ValueError, TypeError):
            raise RuntimeError(f"ceil() requires a numeric argument")

    def builtin_round(self, x, ndigits=None):
        try:
            if ndigits is None:
                return round(float(x))
            else:
                return round(float(x), int(ndigits))
        except (ValueError, TypeError):
            raise RuntimeError(f"round() requires numeric arguments")

    def builtin_min(self, *args):
        if len(args) == 0:
            raise RuntimeError("min() requires at least one argument")
        try:
            return min(args)
        except TypeError:
            raise RuntimeError("min() arguments must be comparable")

    def builtin_max(self, *args):
        if len(args) == 0:
            raise RuntimeError("max() requires at least one argument")
        try:
            return max(args)
        except TypeError:
            raise RuntimeError("max() arguments must be comparable")

    # String functions
    def builtin_substring(self, s, start, end=None):
        if not isinstance(s, str):
            raise RuntimeError("substring() requires a string as first argument")
        try:
            if end is None:
                return s[int(start):]
            else:
                return s[int(start):int(end)]
        except (ValueError, TypeError):
            raise RuntimeError("substring() requires integer start and end arguments")

    def builtin_replace(self, s, old, new):
        if not isinstance(s, str):
            raise RuntimeError("replace() requires a string as first argument")
        return str(s).replace(str(old), str(new))

    def builtin_split(self, s, separator=" "):
        if not isinstance(s, str):
            raise RuntimeError("split() requires a string as first argument")
        return str(s).split(str(separator))

    def builtin_tolower(self, s):
        if not isinstance(s, str):
            raise RuntimeError("tolower() requires a string argument")
        return str(s).lower()

    def builtin_toupper(self, s):
        if not isinstance(s, str):
            raise RuntimeError("toupper() requires a string argument")
        return str(s).upper()

    def builtin_startswith(self, s, prefix):
        if not isinstance(s, str):
            raise RuntimeError("startswith() requires a string as first argument")
        return str(s).startswith(str(prefix))

    def builtin_endswith(self, s, suffix):
        if not isinstance(s, str):
            raise RuntimeError("endswith() requires a string as first argument")
        return str(s).endswith(str(suffix))

    # Utility functions
    def builtin_range(self, start, end=None, step=1):
        try:
            if end is None:
                return list(range(int(start)))
            else:
                return list(range(int(start), int(end), int(step)))
        except (ValueError, TypeError):
            raise RuntimeError("range() requires integer arguments")

    def builtin_type(self, obj):
        if obj is None:
            return "null"
        elif isinstance(obj, bool):
            return "boolean"
        elif isinstance(obj, (int, float)):
            return "number"
        elif isinstance(obj, str):
            return "string"
        elif isinstance(obj, list):
            return "array"
        elif isinstance(obj, Function):
            return "function"
        else:
            return "object"

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
