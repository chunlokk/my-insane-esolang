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

### Input/Output Operations
```
INPUT         := "O_O"    // Input expression
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

### Expressions  
```ebnf
expression      = expression PLUS_HAPPY expression          // Addition: expr :+) expr
                | expression MINUS_SAD expression           // Subtraction: expr :-( expr
                | expression STAR_EYES expression           // Multiplication: expr *_* expr
                | expression SLASH_CONFUSED expression      // Division: expr :/ expr
                | expression PERCENT_WEIRD expression       // Modulo: expr :% expr
                | expression EQUAL_TWINS expression         // Equality: expr =) expr
                | expression NOT_EQUAL expression           // Not equal: expr !( expr
                | expression GREATER_SMUG expression        // Greater than: expr >:) expr
                | expression LESS_DOWN expression           // Less than: expr <:( expr
                | expression AND_TOGETHER expression        // Logical AND: expr &) expr
                | expression OR_CHOICE expression           // Logical OR: expr |) expr
                | NOT_OPPOSITE expression                   // Logical NOT: !) expr
                | IDENTIFIER SAD_OPEN arguments HAPPY_CLOSE // Function call: func :( args :)
                | IDENTIFIER                                // Variable reference
                | INPUT                                     // Input expression: O_O
                | literal                                   // Literal values
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

### Blocks
```ebnf
block           = CURLY_OPEN statements CURLY_CLOSE    // Block: :{ statements :}
```

### Lexical Elements
```ebnf
IDENTIFIER      = [a-zA-Z_][a-zA-Z0-9_]*
NUMBER_VALUE    = \d+(?:\.\d+)?
STRING_VALUE    = "[^"]*"
```

### Precedence and Associativity
Expression precedence (from lowest to highest):
1. Logical OR (`|)`) - left associative
2. Logical AND (`&)`) - left associative  
3. Logical NOT (`!)`) - right associative
4. Equality (`=)`, `!(`) - left associative
5. Comparison (`>:)`, `<:(`) - left associative
6. Addition/Subtraction (`:+)`, `:-(`) - left associative
7. Multiplication/Division/Modulo (`*_*`, `:/`, `:%`) - left associative

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
