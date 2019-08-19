
# Matthieu Brucher
# Last Change : 2007-12-12 09:29


"""
Module containing the line searchers

Line Searches :
  - SimpleLineSearch
    - takes a simple step
  - HyperbolicLineSearch
    - takes a step of length 1/(1+iterations)
  - DampedLineSearch
    - searches for a candidate by dividing the step by 2 each time
  - BacktrackingSearch
    - finds a candidate according to the Armijo rule

  - WolfePowellRule
    - finds a candidate according to the standard Wolfe-Powell rules
  - StrongWolfePowellRule
    - finds a candidate according to the strong Wolfe-Powell rules
  - GoldsteinRule
    - finds a candidate according to the Goldstein rules

  - GoldenSectionSearch
    - uses the golden section method for exact line search
  - FibonacciSectionSearch
    - uses the Fibonacci section method for exact line search
  - QuadraticInterpolationSearch
    - uses the quadratic interpolation method with computation of the gradient at the origin for exact line search

  - AdaptiveLastStepModifier
    - modifies the last step length depending on the last direction and gradient and current gradient and direction
  - FixedLastStepModifier
    - modified the last step length with a fixed factor
"""

from .simple_line_search import *           # noqa: F401
from .hyperbolic_line_search import *       # noqa: F401
from .damped_line_search import *           # noqa: F401
from .backtracking_search import *          # noqa: F401

from .wolfe_powell_rule import *            # noqa: F401
from .strong_wolfe_powell_rule import *     # noqa: F401
from .goldstein_rule import *               # noqa: F401

from .golden_section import *               # noqa: F401
from .fibonacci_section import *            # noqa: F401
from .quadratic_interpolation import *      # noqa: F401
from .cubic_interpolation import *          # noqa: F401

from .adaptive_last_step_modifier import *  # noqa: F401
from .fixed_last_step_modifier import *     # noqa: F401

from .scaled_line_search import *           # noqa: F401

line_search__all__ = ['SimpleLineSearch', 'HyperbolicLineSearch', 'DampedLineSearch', 'BacktrackingSearch',
                      'WolfePowellRule', 'StrongWolfePowellRule', 'GoldsteinRule',
                      'GoldenSectionSearch', 'FibonacciSectionSearch', 'QuadraticInterpolationSearch', 'CubicInterpolationSearch',
                      'AdaptiveLastStepModifier', 'FixedLastStepModifier', 'ScaledLineSearch']
__all__ = line_search__all__

