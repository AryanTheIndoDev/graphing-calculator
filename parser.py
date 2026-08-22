from sympy import (solve, Eq, symbols, lambdify)
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)
from tokenize import TokenError

from typing import Callable

transformations = standard_transformations + (implicit_multiplication_application,)

def parseEquation(equation: str, var1: str, var2: str) -> Callable:
    x, y = symbols(f"{var1} {var2}")

    try:
        LHS, RHS = equation.split("=")
        leftExpr = parse_expr(LHS, transformations = transformations)
        rightExpr = parse_expr(RHS, transformations = transformations)
    
    except (ValueError, SyntaxError, TokenError):
        LHS, RHS = ("y", "x")
        leftExpr = parse_expr(LHS, transformations = transformations)
        rightExpr = parse_expr(RHS, transformations = transformations)

    parsed = Eq(leftExpr, rightExpr)

    expr = solve(parsed, y)
    f = lambdify(x, expr)

    return f

# f = parseEquation(eq, x, y)

# for i in range(-5, 6):
#     x_val: float = i
#     y_val: float = f(i)[0]

#     print(Vector2(x_val, y_val))

