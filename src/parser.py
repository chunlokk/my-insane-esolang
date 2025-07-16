#!/usr/bin/env python3
"""
EmotiLang Parser using SLY (Python Lex-Yacc)
Step 1: Basic variable declaration support
"""

import sys
import os

from sly import Lexer, Parser
from ast_nodes import *

class EmotiLexer(Lexer):
    """
    Lexer for EmotiLang - handles tokenization of emoticon-based syntax
    """
    
    # Define tokens
    tokens = {
        # Structure tokens
        'HAPPY_CLOSE', 'SAD_OPEN', 'WINK_SEP', 'CURLY_OPEN', 'CURLY_CLOSE',
        'FIELD_SEP',
        
        # Data type tokens  
        'DECLARE', 'SURPRISED', 'L_FACE', 'DEAD',
        'CRYING', 'LAUGHING',
        
        # Assignment
        'ASSIGN_GIVE', 'TYPE_ARROW',
        
        # Function and control flow
        'ROBOT', 'WAVE', 'IF', 'DIZZY', 'TRY', 'CATCH', 'THROW',
        
        # I/O
        'TONGUE_OUT', 'INPUT',
        
        # Identifiers and literals
        'IDENTIFIER', 'NUMBER_VALUE', 'STRING_VALUE',

        # Arithmetic operations
        'PLUS_HAPPY', 'MINUS_SAD', 'STAR_EYES', 'SLASH_CONFUSED', 'PERCENT_WEIRD',

        # Comparison operations
        'EQUAL_TWINS', 'NOT_EQUAL', 'GREATER_SMUG', 'LESS_DOWN',

        # Logical operations
        'AND_TOGETHER', 'OR_CHOICE', 'NOT_OPPOSITE',
    }
    
    # Ignore whitespace
    ignore = ' \t'
    
    # Token definitions - order matters for precedence
    
    # Comments (handled separately to avoid conflicts)
    @_(r'Z_Z[^\n]*')
    def ignore_comment(self, t):
        pass

    IDENTIFIER['X_X'] = DEAD
    IDENTIFIER['O_O'] = INPUT
    
    # Structure tokens
    HAPPY_CLOSE = r':\)'
    SAD_OPEN = r':\('
    WINK_SEP = r';\)'
    CURLY_OPEN = r':\{'
    CURLY_CLOSE = r':\}'
    FIELD_SEP = r':,D'
    
    # Data type tokens
    DECLARE = r':<'
    TYPE_ARROW = r':>'
    SURPRISED = r':0'
    L_FACE = r':L'
    CRYING = r':\'\('
    LAUGHING = r':D'
    
    # Function and control flow
    ROBOT = r'🤖'
    WAVE = r'/o/'
    IF = r"\(╭ರ_•́\)"
    DIZZY = r"\(⸝⸝๑﹏๑⸝⸝\)"
    TRY = r'🕷️'
    CATCH = r'🕸️'
    THROW = r'💥'

    # Print statement
    TONGUE_OUT = r':P'
    
    # Assignment
    ASSIGN_GIVE = r'<3'

    # Arithmetic operations
    PLUS_HAPPY = r':\+\)'
    MINUS_SAD = r':-\('
    STAR_EYES = r'\*_\*'
    SLASH_CONFUSED = r':/'
    PERCENT_WEIRD = r':%'

    # Comparison operations
    EQUAL_TWINS = r'=\)'
    NOT_EQUAL = r'!\('
    GREATER_SMUG = r'>:\)'
    LESS_DOWN = r'<:\('

    # Logical operations
    AND_TOGETHER = r'&\)'
    OR_CHOICE = r'\|\)'
    NOT_OPPOSITE = r'!\)'
    
    # Numbers - must come before general patterns
    @_(r'\d+(?:\.\d+)?')
    def NUMBER_VALUE(self, t):
        t.value = float(t.value) if '.' in t.value else int(t.value)
        return t
    
    # String literals
    @_(r'"[^"]*"')
    def STRING_VALUE(self, t):
        t.value = t.value[1:-1]  # Remove quotes
        return t
    
    # Identifiers - must come after keywords
    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def IDENTIFIER(self, t):
        return t
    
    # Handle newlines
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')
    
    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1


class EmotiParser(Parser):
    """
    Parser for EmotiLang - builds AST from tokens
    """
    
    tokens = EmotiLexer.tokens
    
    # Operator precedence and associativity
    precedence = (
        ('left', 'OR_CHOICE'),
        ('left', 'AND_TOGETHER'),
        ('right', 'NOT_OPPOSITE'),
        ('left', 'EQUAL_TWINS', 'NOT_EQUAL'),
        ('left', 'GREATER_SMUG', 'LESS_DOWN'),
        ('left', 'PLUS_HAPPY', 'MINUS_SAD'),
        ('left', 'STAR_EYES', 'SLASH_CONFUSED', 'PERCENT_WEIRD'),
    )
    
    def __init__(self):
        self.variables = {}  # Symbol table for variables
    
    # Grammar rules
    
    @_('statements')
    def program(self, p):
        """Program consists of multiple statements"""
        return Program(p.statements)
    
    @_('statements statement')
    def statements(self, p):
        """Multiple statements - add statement to existing list"""
        return p.statements + [p.statement]
    
    @_('statement')
    def statements(self, p):
        """Single statement - create new list"""
        return [p.statement]

    @_('DECLARE IDENTIFIER TYPE_ARROW type ASSIGN_GIVE expression WINK_SEP')
    def statement(self, p):
        """Variable declaration: :< myNumber :> :0 <3 :0 42 ;)"""
        # Store variable type in symbol table
        self.variables[p.IDENTIFIER] = p.type
        return VariableDeclaration(p.IDENTIFIER, p.type, p.expression)
    
    @_('IDENTIFIER ASSIGN_GIVE expression WINK_SEP')
    def statement(self, p):
        """Assignment statement: myVar <3 :0 42 ;)"""
        return Assignment(p.IDENTIFIER, p.expression)

    @_('TONGUE_OUT expression WINK_SEP')
    def statement(self, p):
        """Print statement: :P myNumber ;)"""
        return PrintStatement(p.expression)
    
    @_('ROBOT IDENTIFIER SAD_OPEN parameters HAPPY_CLOSE TYPE_ARROW type block')
    def statement(self, p):
        """Function declaration with parameters: 🤖 factorial :( n :> :0 :) :> :0 :{ ... :}"""
        return FunctionDeclaration(p.IDENTIFIER, p.parameters, p.type, p.block)
    
    @_('WAVE expression WINK_SEP')
    def statement(self, p):
        """Return statement: /o/ :0 0 ;)"""
        return ReturnStatement(p.expression)
    
    @_('IDENTIFIER SAD_OPEN arguments HAPPY_CLOSE')
    def expression(self, p):
        """Function call: sayHello :( :)"""
        return FunctionCall(p.IDENTIFIER, p.arguments) 
        
    @_('IF expression block')
    def statement(self, p):
        """If statement: (╭ರ_•́) expression :{ statements :}"""
        return IfStatement(p.expression, p.block)
    
    @_('DIZZY expression block')
    def statement(self, p):
        """While loop: (⸝⸝๑﹏๑⸝⸝) expression :{ statements :}"""
        return WhileLoop(p.expression, p.block)

    @_('TRY block CATCH IDENTIFIER block')
    def statement(self, p):
        """Try-catch block: 🕷️ :{ statements :} 🕸️ identifier :{ statements :}"""
        return TryStatement(p.block0, p.IDENTIFIER, p.block1)
    
    @_('THROW expression WINK_SEP')
    def statement(self, p):
        """Throw statement: 💥 expression ;)"""
        return ThrowStatement(p.expression)
    
    @_('INPUT')
    def expression(self, p):
        """Input statement: O_O"""
        return InputExpression()
    

    # Parameter rules
    @_('parameters FIELD_SEP parameter')
    def parameters(self, p):
        """Multiple parameters: existing_params :,D param"""
        return p.parameters + [p.parameter]

    @_('parameter')
    def parameters(self, p):
        """Single parameter"""
        return [p.parameter]
    
    @_('')
    def parameters(self, p):
        """Empty parameters"""
        return []

    @_('IDENTIFIER TYPE_ARROW type')
    def parameter(self, p):
        """Single parameter: param_name :> type"""
        return Parameter(p.IDENTIFIER, p.type)
    
    # Argument rules
    @_('arguments FIELD_SEP argument')
    def arguments(self, p):
        """Multiple arguments: existing_args :,D args"""
        return p.arguments + [p.argument]

    @_('argument')
    def arguments(self, p):
        """Single argument"""
        return [p.argument]
    
    @_('')
    def arguments(self, p):
        """Empty arguments"""
        return []

    @_('expression')
    def argument(self, p):
        """Single argument: arg_name"""
        return p.expression

    # Type rules
    @_('SURPRISED')
    def type(self, p):
        """Number type: :0"""
        return Type("number")
    
    @_('L_FACE')  
    def type(self, p):
        """String type: :L"""
        return Type("string")
    
    @_('DEAD')
    def type(self, p):
        """Boolean type: X_X"""
        return Type("boolean")
    
    @_('SURPRISED NUMBER_VALUE')
    def literal(self, p):
        """Number literal: :0 42"""
        return NumberLiteral(p.NUMBER_VALUE)
    
    @_('L_FACE STRING_VALUE')
    def literal(self, p):
        """String literal: :L "hello" """ 
        return StringLiteral(p.STRING_VALUE)
    
    @_('LAUGHING')
    def literal(self, p):
        """Boolean true: :D"""
        return BooleanLiteral(True)
    
    @_('CRYING')
    def literal(self, p):
        """Boolean false: :'("""
        return BooleanLiteral(False)
    
    @_('literal')
    def expression(self, p):
        """Literal can be an expression"""
        return p.literal
    
    @_('expression PLUS_HAPPY expression')
    def expression(self, p):
        """Addition: expr :+) expr"""
        return BinaryOp(p.expression0, '+', p.expression1)
    
    @_('expression MINUS_SAD expression')
    def expression(self, p):
        """Subtraction: expr :-( expr"""
        return BinaryOp(p.expression0, '-', p.expression1)
    
    @_('expression STAR_EYES expression')
    def expression(self, p):
        """Multiplication: expr *_* expr"""
        return BinaryOp(p.expression0, '*', p.expression1)
    
    @_('expression SLASH_CONFUSED expression')
    def expression(self, p):
        """Division: expr :/ expr"""
        return BinaryOp(p.expression0, '/', p.expression1)
    
    @_('expression PERCENT_WEIRD expression')
    def expression(self, p):
        """Modulo: expr :% expr"""
        return BinaryOp(p.expression0, '%', p.expression1)
    
    @_('expression EQUAL_TWINS expression')
    def expression(self, p):
        """Equality: expr =) expr"""
        return BinaryOp(p.expression0, '==', p.expression1)
    
    @_('expression NOT_EQUAL expression')
    def expression(self, p):
        """Not equal: expr !( expr"""
        return BinaryOp(p.expression0, '!=', p.expression1)
    
    @_('expression GREATER_SMUG expression')
    def expression(self, p):
        """Greater than: expr >:) expr"""
        return BinaryOp(p.expression0, '>', p.expression1)
    
    @_('expression LESS_DOWN expression')
    def expression(self, p):
        """Less than: expr <:( expr"""
        return BinaryOp(p.expression0, '<', p.expression1)
    
    @_('expression AND_TOGETHER expression')
    def expression(self, p):
        """Logical AND: expr &) expr"""
        return BinaryOp(p.expression0, '&&', p.expression1)
    
    @_('expression OR_CHOICE expression')
    def expression(self, p):
        """Logical OR: expr |) expr"""
        return BinaryOp(p.expression0, '||', p.expression1)
    
    @_('NOT_OPPOSITE expression')
    def expression(self, p):
        """Logical NOT: !) expr"""
        return UnaryOp('!', p.expression)
    
    @_('IDENTIFIER')
    def expression(self, p):
        """Expression can be an identifier"""
        return Identifier(p.IDENTIFIER)

    
    @_('CURLY_OPEN statements CURLY_CLOSE')
    def block(self, p):
        """Block: :{ statements :}"""
        return Block(p.statements)
    
    def error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}: unexpected '{p.value}'")
        else:
            print("Syntax error: unexpected end of input")


def main():
    """Main function to test the parser"""
    
    if len(sys.argv) > 1:
        # Parse file
        filename = sys.argv[1]
        try:
            with open(filename, 'r') as f:
                text = f.read()
            
            print(f"Parsing file: {filename}")
            print(f"Input: {text.strip()}")
            print()
            
            lexer = EmotiLexer()
            parser = EmotiParser()
            
            # Tokenize and parse
            tokens = lexer.tokenize(text)
            result = parser.parse(tokens)
            
            if result:
                print("Parse successful!")
                print(f"AST: {result}")
            else:
                print("Parse failed!")
                
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
        except Exception as e:
            print(f"Error: {e}")
    else:
        # Interactive mode
        print("EmotiLang Parser - Interactive Mode")
        print("Enter EmotiLang code (Ctrl+C to exit):")
        
        lexer = EmotiLexer()
        parser = EmotiParser()
        
        while True:
            try:
                text = input("emoti> ")
                if text.strip():
                    tokens = lexer.tokenize(text)
                    result = parser.parse(tokens)
                    if result:
                        print(f"AST: {result}")
                    else:
                        print("Parse error")
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")


if __name__ == '__main__':
    main()
