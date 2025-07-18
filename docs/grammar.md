# Formal Grammar for My Insane Esolang: EmotiLang

## Overview
This document defines the formal grammar for **EmotiLang**, an esoteric programming language that uses only emoticons as tokens. 

## Lexical Grammar (Tokens)

### Basic Structure Tokens
```
HAPPY_CLOSE     := ":)"     // Closing bracket/parentheses
SAD_OPEN        := ":("     // Opening bracket/parentheses  
WINK_SEP        := ";)"     // Statement separator/newline
CURLY_OPEN      := ":{"     // Opening curly brace/block start
CURLY_CLOSE     := ":}"     // Closing curly brace/block end
FIELD_SEP       := ":,D"    // Field separator for structs and function parameters
```

### Data Type Tokens
```
DECLARE        := ":<"     // Variable declaration
TYPE_ARROW     := ":>"     // Type annotation arrow
SURPRISED      := ":0"     // Number type/literal prefix
L_FACE         := ":L"     // String type/literal prefix
DEAD           := "X_X"    // Boolean type
CRYING         := ":'("    // Boolean false
LAUGHING       := ":D"     // Boolean true
```

### Control Flow Tokens
```
IF             := "(╭ರ_•́)"     // If statement
DIZZY          := "(⸝⸝๑﹏๑⸝⸝)"    // While loop
WAVE           := "/o/"     // Return statement
```

### Arithmetic Operations
```
PLUS_HAPPY     := ":+)"    // Addition
MINUS_SAD      := ":-("    // Subtraction
STAR_EYES      := "*_*"    // Multiplication
SLASH_CONFUSED := ":/"     // Division
PERCENT_WEIRD  := ":%"     // Modulo
```

### Comparison Operations
```
EQUAL_TWINS    := "=)"     // Equality check
NOT_EQUAL      := "!("     // Inequality check
GREATER_SMUG   := ">:)"    // Greater than
LESS_DOWN      := "<:("    // Less than
```

### Logical Operations
```
AND_TOGETHER  := "&)"      // Logical AND
OR_CHOICE     := "|)"      // Logical OR
NOT_OPPOSITE  := "!)"      // Logical NOT
```

### Assignment Operations
```
ASSIGN_GIVE   := "<3"      // Assignment operator
```

### Print Operations
```
TONGUE_OUT    := ":P"     // Print/output statement
```

### High level stuff
```
ROBOT       := 🤖 // Function definition
TRY         := 🕷️ // Try
CATCH       := 🕸️ // Catch
THROW       := 💥 // Throw
```

### Special Tokens
```
IDENTIFIER    := [a-zA-Z_][a-zA-Z0-9_]*    // Variable/function names
NUMBER_VALUE  := \d+(?:\.\d+)?             // Numeric literals
STRING_VALUE  := "[^"]*"                   // String literals
```

### Comments
```
Z_Z           := "Z_Z"    // Single-line comment start (followed by any characters until newline)
```

## Syntactic Grammar (EBNF)

### Program Structure
```ebnf
program         = statements

statements      = statements statement
                | statement

statement       = variable_decl
                | assignment_stmt
                | print_stmt
                | function_decl
                | return_stmt
                | if_stmt
                | while_stmt
                | try_stmt
                | throw_stmt

variable_decl   = DECLARE IDENTIFIER TYPE_ARROW type ASSIGN_GIVE expression WINK_SEP

assignment_stmt = IDENTIFIER ASSIGN_GIVE expression WINK_SEP

print_stmt      = TONGUE_OUT expression WINK_SEP

function_decl   = ROBOT IDENTIFIER SAD_OPEN parameters HAPPY_CLOSE TYPE_ARROW type block

return_stmt     = WAVE expression WINK_SEP

if_stmt         = IF expression block

while_stmt      = DIZZY expression block

try_stmt        = TRY block CATCH IDENTIFIER block

throw_stmt      = THROW expression WINK_SEP
```

### Types and Literals
```ebnf
type            = SURPRISED        // Number type (:0)
                | L_FACE           // String type (:L)  
                | DEAD             // Boolean type (X_X)

literal         = SURPRISED NUMBER_VALUE     // Number literal: :0 42
                | L_FACE STRING_VALUE        // String literal: :L "hello"
                | LAUGHING                   // Boolean true: :D
                | CRYING                     // Boolean false: :'(
```

### Parameters and Arguments
```ebnf
parameters      = parameters FIELD_SEP parameter
                | parameter
                | /* empty */

parameter       = IDENTIFIER TYPE_ARROW type

arguments       = arguments FIELD_SEP argument
                | argument  
                | /* empty */

argument        = expression
```

### Lexical Elements
```ebnf
IDENTIFIER      = [a-zA-Z_][a-zA-Z0-9_]*
NUMBER_VALUE    = \d+(?:\.\d+)?
STRING_VALUE    = "[^"]*"
```

### Grammar Design Notes for Parser Implementation

#### Precedence and Associativity
The expression grammar uses the following precedence levels (from lowest to highest):
1. Logical OR (`|)`) - left associative
2. Logical AND (`&)`) - left associative  
3. Logical NOT (`!)`) - right associative
4. Equality (`=)`, `!(`) - left associative
5. Comparison (`>:)`, `<:(`) - left associative
6. Addition/Subtraction (`:+)`, `:-(`) - left associative
7. Multiplication/Division/Modulo (`*_*`, `:/`, `:%`) - left associative

#### Parsing Strategy
- **LR(1) Compatible**: Uses SLY (Python Lex-Yacc) which generates LR parsers
- **Clear Delimiters**: Blocks use `:{ }:` and function calls use `:( )`
- **Statement Terminators**: All statements end with `;)` for clear separation
- **Expression Precedence**: Uses SLY's precedence declarations for operator precedence
- **Unambiguous Keywords**: Each token has a unique lexical representation

#### Error Recovery Points
- Statement boundaries (`;)`) provide natural recovery points
- Block boundaries (`:{ }:`) help with scope-based recovery
- Function declarations are top-level constructs

#### Lexical Considerations
- **Longest Match**: Emoticon tokens are matched greedily using regex patterns
- **Unicode Handling**: Some tokens use Unicode characters (🤖, 🕷️, 🕸️, 💥)
- **Whitespace**: Implicit whitespace handling between tokens
- **Comments**: Single-line comments from `Z_Z` to end of line

### Example Program Structure
```emotilang
Z_Z This is a comment

Z_Z Variable declaration
:< myNumber :> :0 <3 :0 42 ;)

Z_Z Assignment  
myNumber <3 :0 100 ;)

Z_Z Print statement
:P myNumber ;)

Z_Z Function declaration
🤖 factorial :( n :> :0 :) :> :0 :{
    (╭ರ_•́) n =) :0 0 :{
        /o/ :0 1 ;)
    :}
    /o/ n *_* factorial :( n :-( :0 1 :) ;)
:}

Z_Z Function call and print
:P factorial :( :0 5 :) ;)

Z_Z While loop
:< counter :> :0 <3 :0 0 ;)
(⸝⸝๑﹏๑⸝⸝) counter <:( :0 5 :{
    :P counter ;)
    counter <3 counter :+) :0 1 ;)
:}

Z_Z Try-catch
🕷️ :{
    💥 :L "Something went wrong" ;)
:} 🕸️ e :{
    :P :L "Caught error: " ;)
:}
```
