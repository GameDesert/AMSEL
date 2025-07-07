# What is AMSEL?

`Automatic Mathematical Script Execution Language`

A scripting language that is as close as possible to natural mathematical writing, with a few extra features to make calculations as easy as possible.

# Why is AMSEL?

I was messing around with some drag-free projectile equations, and wanted to write a script that would automatically solve a naturally-written equation, no matter where the variable lies (i.e. AMSEL automatically rearranges equations).

# Docs, sorta...

## What we need:
- Tokeniser
  - Line-by-line

- Rearranger
  - When an equation with one or more variables is detected, it caches several forms of the equation rearranged for every possible variable.
  - These rearranged equations can be executed like functions.
  - What about when it sees a polynomial?
    - Figure out when to gather like terms and shit.

- Evaluator

Rules:
- Equations must contain one equals sign with a valid term on each side
  - These can fail to evaluate if each side resolves to a different constant
- Valid expressions must contain at least one term, and may include a valid operation, or many valid operations
- A valid operation must have a valid term on each side
- An output must contain a valid expression on the left and a blank space on the right of a "==" operator
- A term can either be a constant, variable, or expression in brackets
  - A term can have a sign and a power
  - Coefficients were a stupid idea because it requires a lot of nesting. Instead, multiplication is evaluated right-to-left

- There is no such thing as subtraction, there is only summing with a term that has a negative sign
  - i.e. The operator a - b exists, but this is then converted by the tokeniser into a + -b
- A function is defined by a specific symbol or name that is either preceeded by or followed by a term
  - For instance, a factorial (!) is proceeded by a term
  - Some function, such as a summation, have special parameters that must be defined
    - For instance, a summation could take the format `Σ{n = 99}{r = 1}` where the first parameter is the limit and the second is the index

- Order of operations:
  - B/F/IDMAS
    - Brackets (terms are evaluated on their own first)
    - Functions (functions are evaluated only after the child is evaluated, after which they act similar to a constant)
    - Indices (powers of terms are evaluated after the child of the term and do not affect the sign of the term)
    - Division/multiplication (evaluated right-to-left)
    - Addition/subtraction (it's all addition anyway, with some negative terms sprinkled in)

- Spaces _should_ be inserted between terms if implicit multiplication is desired. A space _must_ be inserted after a power to delimit it from the next implicitly multiplied term.

- In AMSEL, the division operator (/) is taken to represent division by means of an algebraic fraction. As such, the entire LHS and the entire RHS will be evaluated first, before the division is evaluated.

# Storage:
Operations kept in RPN

The first value of a block is its type:


## Constants
When you have a positive or negative number that is either whole or a decimal. A constant cannot be negative, it must be evaluated as a term instead.

### Format
`("constant", <absolutevalue>)`

### Examples
`3 -> ("constant", 3)`

`69.0123 -> ("constant", 69.0123)`

`55,000,123 -> ("constant", 55000123)` | In the event of comma-delimited place values, allow the user to set how often values are delimited and throw a warning if an input constant does not match this format.

## Variables
Designated by one or more characters from a-z, A-Z, α-ω, and Α-Ω. This excludes certain characters that may already be defined functions and operations, such as Σ or Π.

Immutable variables are usually those representing imported constants such as π or e.

However, an immutable variable can be set by appending an _ to its name when defined.

### Format
`("variable", <immutable [1 for true and 0 for false]>, <name [for Greek characters, converted to Latin]>)`

### Examples
`A -> ("variable", 0, "A")`

`alan -> ("variable", 0, "alan")`

`Bee_ -> ("variable", 1, "Bee_")`

`A -> ("variable", 0, "ALPHA")`

`Andrew -> ("variable", 0, "Andrew")`

`Andrew_ -> ("variable", 1, "ALPHAndrew_")`

## Terms
Contains a function, constant, variable, or expression. Can either be delimited with brackets (must be, in the case of an expression) or is inferred.

Can possess a power.

Do I turn sign into a separate element that can be multiplied? YES

The power is evaluated before the sign. Thus, `-2²` is `-4`, not `4`.

Removed the idea of coefficients. Instead, implied multiplication takes place instead.

These can get pretty big, is there any way of cutting this down?

### Format
`("term", <power [either a term, constant, variable, or 1]>, <child>)`

### Examples

`-2^2 -> ("term", 1, ("operation", ("sign", 0), ("constant", 2), "multiply"), ("constant", 2))`

`y^x -> ("term", 0, ("variable", 0, "x"), ("variable", 0, "y"))`

`f^-2 -> ("term", 0, ("term", 1, ("operation", ("sign", 0), ("constant", 2), "multiply")), ("variable", "0", "f"))`

## Sign
Because it's easier to convert any negative sign into an implied `× -1` whilst evaluating. Lack of this object implies positive.

### Format
`("sign", <1 for positive, 0 for negative>)`

### Examples
`-a^8 -> ("term", ("constant", 8), ("operation", ("sign", 0), ("variable", 0, "a"), "multiply"))`


## Operations
Applies only to when you have *, /, +, or - with a term on each side.

Reverse Polish notation.

Division is evaluated as if it were an algebraic fraction with the numerator on the left and denominator on the right. For instance `a * b / c * d` would be evaluated in the same way as `(ab / cd)` and `(a * b) / (c * d)`. That is to say, `a * b` would be evaluated, then `c * d`, and finally the result of the former would be divided by the latter.

Multiplications are nested from left-to-right.

### Format
`("operation", <term/constant/variable/operation>, <term/constant/variable/operation>, <operator>)`

### Examples
`a + b -> ("operation", ("variable", 0, "a"), ("variable", 0, "b"), "add")`

`1 - a -> ("operation", ("constant", 1), ("term", 1, 1, ("variable", 0, "a")), "add")` | Upon evaluation, anything to the right of the operator would be made into a term with a negative power. i.e. If the RHS is a constant, it becomes a negative term; if the RHS is a negative term, it becomes a positive term.


`99a^2 / 3(-x)^ka b ->`
```
("operation",
    ("operation",
        ("constant", 99),
        ("term",
            0,
            ("constant", 2),
            ("variable", 0, "a")
        ),
        "multiplication"
    ),
    (
        ("operation",
            ("operation",
                ("constant", 3),
                ("term",
                    0,
                    ("operation",
                        ("variable", 0, "k"),
                        ("variable", 0, "a"),
                        "multiplication"
                    ),
                    ("term",
                        1,
                        1,
                        ("variable", 0, "x")
                    )
                )
                "multiplication"
            ),
            ("variable", 0, "b"),
            "multiplication"
        )
    ),
    "division"
)
```

## Unary Operations and Functions
Unary operators and functions, though slightly different, share the same format here.

The following is a list of unary operators and functions that AMSEL supports:
- ! (Factorial)
- abs (Absolute value)
- sin (Sine)
- cos (Cosine)
- tan (Tangent)
- arcsin (Arcsine)
- arccos (Arccosine)
- arctan (Arctangent)
- csc (Cosecant)
- sec (Secant)
- cot (Cotangent)
- arccsc (Arccosecant)
- arcsec (Arcsecant)
- arccot (Arccotangent)
- Σ or sum (Sum)
- Π or pi (Product of a Sequence)
- √ or root (nth root of a Number)

### Format
`("function", <parameters [reserved for specific functions, otherwise 0]>, <constant/variable/term>, <operation>)`

### Examples
`sum{n = 9}{r = 1} (3n) ->`
```
("function",
    (
        "parameters"
        ("limit", ("variable", 1, n), ("constant", 9)),
        ("initial", ("variable", 1, r), ("constant", 1))
    ),
    ("term", 0, 1,
        ("operation",
            ("constant", 3),
            ("variable", 0, "n"),
            "multiplication"
        )
    ),
"sum")
```
`9! -> ("function", 0, ("constant", 9), "factorial")`

## Equations
Equations must have exactly one equals sign ("=") within them. There must be a term, function, constant, or variable on each side of the sign. A term encompassing the entirety of each side is inferred if the sides are not made up of exclusively a constant or a variable.

Equations represent a relationship between several objects, and are only evaluated when part of an output (see below).

### Format
`("equation", <LHS>, <RHS>)`

### Examples
`a + b = b + 3 -> ("equation", ("operation", ("variable", 0, a), ("variable", 0, b), "add"), ("operation", ("variable", 0, b), ("constant", 3), "add"))`

## Output
An output is usually what prompts AMSEL to evaluate a series of equations.

It is designated by the double-equals sign ("==").

It must have an expression, variable, constant, or term on the LHS and _nothing_ on the RHS.

An output will usually print the value of the evaluated expressions &c. to the stdout.

### Format
`("output", <expression/variable/constant/term>)`

`a + b == -> ("output", ("operation", ("variable", 0, "a"), ("variable", 0, "b"), "add"))`



# The Tokeniser
The tokeniser goes line-by-line.

It has a short buffer in order to account for implicit multiplication.
- If it encounters a negative sign, it will begin recording a new term.
- If it encounters a number, it will begin recording a new constant and it will expect the next character to be either a number or a decimal point (.).
  - If the next character is a space, it stops evaluating and saves the constant.
  - If a second decimal point is encountered, a breaking error is flagged.
  - If a function with a unique symbol is encountered (e.g. !), it stops evaluating, saves the constant and the function.
  - If a letter is encountered, it begins recording a variable.

- Effectively, for implicit tokenising:
  - If presently recording letters and encounter a number, stop. Check string against list of functions. If not a function, save as a variable.
  - If presently recording numbers and encounter a letter, stop.
  - If presently recording anything and encounter a caret (^), save child and create term, begin evaluating power.
  - If presently recording anything and encounter a space, stop.
  - If presently recording anything and encounter a binary operator, flag a breaking error.
  - If presently recording anything and encounter an open bracket '(', stop and begin recording a term.
  - If presently recording a term from an open bracket, and encounter a matching closing one, check next character for a caret (^) and save a term with/without a power depending.
  - If presently recording a space/just started and encounter a minus (-), check if next character is a space. If so, create new addition operation and group next object into a negative term. If there is no space, group next object into a negative term.