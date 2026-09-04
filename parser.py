from sympy import (solve, Eq, symbols, lambdify)
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)
from tokenize import TokenError
from sympy.core.sympify import SympifyError

transformations = standard_transformations + (implicit_multiplication_application, convert_xor,)

def parseEquation(equation: str, var1: str, var2: str) -> tuple:
    x, y = symbols(f"{var1} {var2}")

    try:
        # split and parse each side
        LHS, RHS = equation.split("=")
        leftExpr = parse_expr(LHS, transformations = transformations)
        rightExpr = parse_expr(RHS, transformations = transformations)

        # equate and solve for y
        parsed = Eq(leftExpr, rightExpr)
        expr = solve(parsed, y)

        # turn to python math function
        f = lambdify(x, expr, 'numpy')

        # testing
        f(0)

    except (ValueError, SyntaxError, NameError, TypeError, TokenError, IndexError, SympifyError, NotImplementedError):
        return ((), lambda x: None)

    except ZeroDivisionError:
        return (tuple(expr), f)
    else:
        return (tuple(expr), f)

# f = parseEquation(eq, x, y)

# for i in range(-5, 6):
#     x_val: float = i
#     y_val: float = f(i)[0]

#     print(Vector2(x_val, y_val))

