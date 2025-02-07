import sympy as sp
from sympy.parsing.latex import parse_latex

def main():
    # Define the LaTeX string representing the integrand
    latex_str = r"""
    \left(v\frac{(\theta*u*(v-1)-\theta*(u-1)(v-1)+1)}
    {(\theta*(u-1)(v-1)-1)^2}\right)^2
    """

    # Parse the LaTeX code into a Sympy expression
    try:
        integrand = parse_latex(latex_str)
    except Exception as e:
        print("Error parsing LaTeX:", e)
        return

    # Extract the free symbols from the expression
    free_syms = integrand.free_symbols

    # Get the specific symbols 'u' and 'v'
    try:
        u = next(sym for sym in free_syms if sym.name == "u")
        v = next(sym for sym in free_syms if sym.name == "v")
    except StopIteration:
        print("Could not find symbols 'u' and 'v' in the expression.")
        return

    # Simplify the integrand for easier integration
    integrand = sp.simplify(integrand)

    # Compute the double integral over u and v from 0 to 1
    integral_result = sp.integrate(integrand, (u, 0, 1), (v, 0, 1))

    # Combine the result as specified: 6 * integral - 2
    final_expr = 6 * integral_result - 2

    # Convert the final expression into LaTeX format
    latex_output = sp.latex(final_expr)
    print("The result in LaTeX format:")
    print(latex_output)

if __name__ == '__main__':
    main()
