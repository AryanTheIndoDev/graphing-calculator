from sympy import (solve, Eq, symbols, lambdify)
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application
)

transformations = standard_transformations + (implicit_multiplication_application,)

def parseEquation(equation: str, var1: str, var2: str):
    LHS, RHS = equation.split("=")
    x, y = symbols(f"{var1} {var2}")

    leftExpr = parse_expr(LHS, transformations = transformations)
    rightExpr = parse_expr(RHS, transformations = transformations)
    
    parsed = Eq(leftExpr, rightExpr)
    print(f"Parsed: {parsed}")

    expr = solve(parsed, y)
    f = lambdify(x, expr)
    print(f"Lambdified: {f}")

    return f

# f = parseEquation(eq, x, y)

# for i in range(-5, 6):
#     x_val: float = i
#     y_val: float = f(i)[0]

#     print(Vector2(x_val, y_val))

