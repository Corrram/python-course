#!/usr/bin/env python3
import sympy as sp
from sympy import (
    symbols, init_printing, pprint, expand, factor, solve, diff, integrate, oo,
    limit, Sum, Product, Matrix, simplify, sin, cos, exp
)

# Try importing LaTeX parsing functionality; if not installed, we warn the user.
try:
    from sympy.parsing.latex import parse_latex
except ImportError:
    print("Warning: LaTeX parsing not available. Install with 'pip install antlr4-python3-runtime==4.11'.")
    parse_latex = None

def main():
    # Initialize pretty printing for better display in interactive sessions.
    init_printing()

    #-----------------------------------------------------------------------
    # Generating Symbols
    print("=== Generating Symbols ===")
    x, y = symbols('x y')
    print("Symbols x, y:")
    pprint([x, y])

    # Indexed symbols (x0, x1, x2):
    x_indexed = symbols('x:3')
    print("\nIndexed symbols (x0, x1, x2):")
    pprint(x_indexed)

    # Symbols with assumptions:
    a = symbols('a', real=True, positive=True)
    print("\nSymbol a with assumptions (real, positive):")
    pprint(a)

    #-----------------------------------------------------------------------
    # Basic Expression Manipulation
    print("\n=== Basic Expression Manipulation ===")
    expr = x**2 + 2*x + 1
    print("Expression: x^2 + 2*x + 1:")
    pprint(expr)

    result = expr.subs(x, 2)
    print("\nSubstitute x=2 gives:")
    pprint(result)

    num_val = expr.evalf(subs={x: 1.5})
    print("\nNumeric evaluation for x=1.5:")
    pprint(num_val)

    #-----------------------------------------------------------------------
    # Algebra and Calculus Examples
    print("\n=== Algebra and Calculus Examples ===")
    expr1 = (x + y)**3
    expanded_expr = expand(expr1)
    print("Expanded (x+y)^3:")
    pprint(expanded_expr)

    factored_expr = factor(expanded_expr)
    print("\nFactored back to (x+y)^3:")
    pprint(factored_expr)

    solutions = solve(x**2 - 2, x)
    print("\nSolutions for x^2 - 2 = 0:")
    pprint(solutions)

    derivative = diff(sin(x)*exp(x), x)
    print("\nDerivative of sin(x)*exp(x):")
    pprint(derivative)

    integral_expr = integrate(exp(-x**2/2), (x, -oo, oo))
    print("\nIntegral of exp(-x^2/2) from -oo to oo:")
    pprint(integral_expr)

    #-----------------------------------------------------------------------
    # Limits, Series, and Matrix Operations
    print("\n=== Limits, Series, and Matrix Operations ===")
    lim_expr = limit(sin(x)/x, x, 0)
    print("Limit of sin(x)/x as x -> 0:")
    pprint(lim_expr)

    sum_expr = Sum(1/x**2, (x, 1, oo)).doit()
    print("\nSum of 1/x^2 for x from 1 to infinity:")
    pprint(sum_expr)

    prod_expr = Product(x, (x, 1, 7)).doit()
    print("\nProduct of x for x from 1 to 7:")
    pprint(prod_expr)

    # Matrix Operations
    M = Matrix([[1, 2], [3, 4]])
    print("\nMatrix M:")
    pprint(M)

    M_squared = M**2
    print("\nM squared:")
    pprint(M_squared)

    M_inv = M.inv()
    print("\nInverse of M:")
    pprint(M_inv)

    #-----------------------------------------------------------------------
    # Simplification Examples
    print("\n=== Simplification Examples ===")
    expr_simplify = (x + x*y) / x
    simplified_expr = simplify(expr_simplify)
    print("Simplify (x + x*y)/x:")
    pprint(simplified_expr)

    trig_expr = sin(x)**2 + cos(x)**2
    simplified_trig = simplify(trig_expr)
    print("\nSimplify sin(x)^2 + cos(x)^2:")
    pprint(simplified_trig)

    #-----------------------------------------------------------------------
    # Parsing LaTeX Code to SymPy Expressions
    if parse_latex:
        print("\n=== Parsing LaTeX to SymPy ===")
        latex_expr = r'\frac{x*(y-1)}{y+1}'
        parsed_expr = parse_latex(latex_expr)
        print("Parsed LaTeX expression for \\frac{x*(y-1)}{y+1}:")
        pprint(parsed_expr)
    else:
        print("\nSkipping LaTeX parsing examples.")


if __name__ == '__main__':
    main()
