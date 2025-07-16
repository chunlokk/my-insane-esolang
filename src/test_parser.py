#!/usr/bin/env python3
"""
Test utility for EmotiLang parser
"""

from parser import EmotiLexer, EmotiParser
from ast_nodes import ASTNode
import sys


def print_ast(node, indent=0):
    """Pretty print the AST"""
    if node is None:
        return
        
    spaces = "  " * indent
    print(f"{spaces}{type(node).__name__}", end="")
    # print(repr(node))
    
    if hasattr(node, 'value'):
        print(f": {repr(node.value)}", end=" ")
    if hasattr(node, 'name'):
        print(f": {node.name}", end=" ")
    if hasattr(node, 'identifier'):
        print(f": {node.identifier}", end=" ")
    if hasattr(node, 'operator'):
        print(f": {node.operator}", end=" ")
    if hasattr(node, 'catch_variable'):
        print(f": catch_var={node.catch_variable}", end=" ")
    if hasattr(node, 'var_type'):
        print(f": type={node.var_type.name}", end=" ")
    if hasattr(node, 'return_type'):
        print(f": return_type={node.return_type.name}", end=" ")
    if hasattr(node, 'param_type'):
        print(f": param_type={node.param_type.name}", end=" ")
    if hasattr(node, 'field_type'):
        print(f": field_type={node.field_type.name}", end=" ")
    # if hasattr(node, 'expression'):
    #     print(f": {node.expression}", end=" ")
    if hasattr(node, 'block'):
        print(f": {node.block}", end=" ")

    print()
    
    # Print children based on known attributes
    attrs_to_check = [
        'declarations', 'statements', 'parameters', 'expression', 'block',
        'left', 'right', 'operand', 'arguments', 'condition', 'then_block', 'else_block',
        'body', 'try_block', 'catch_block', 'fields', 'initial_value'
    ]
    
    for attr_name in attrs_to_check:
        if hasattr(node, attr_name):
            attr = getattr(node, attr_name)
            # Debug: print what we're checking
            # print(f"DEBUG: Checking {attr_name} = {attr} (type: {type(attr)})")
            if attr is None:
                continue
            elif isinstance(attr, list):
                if attr:  # Only print non-empty lists
                    print(f"{spaces}  {attr_name}:")
                    for i, item in enumerate(attr):
                        print(f"{spaces}    [{i}]:")
                        print_ast(item, indent + 3)
            elif isinstance(attr, ASTNode):
                print(f"{spaces}  {attr_name}:")
                print_ast(attr, indent + 2)


def test_lexer(text):
    """Test the lexer with given text"""
    print("=== LEXER TEST ===")
    lexer = EmotiLexer()
    tokens = list(lexer.tokenize(text))
    for token in tokens:
        print(f"{token.type:15} {repr(token.value):20} line:{token.lineno}")
    print()


def test_parser(text):
    """Test the parser with given text"""
    print("=== PARSER TEST ===")
    lexer = EmotiLexer()
    parser = EmotiParser()
    
    try:
        result = parser.parse(lexer.tokenize(text))
        print("Parse successful!")
        if result is None:
            print("Parser returned None - no AST generated")
        else:
            print(f"AST root type: {type(result)}")
            print_ast(result)
    except Exception as e:
        print(f"Parse error: {e}")


def main():
    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        # Read from stdin or interactive
        print("Enter EmotiLang code (Ctrl+D to finish):")
        text = sys.stdin.read()
    
    print(f"Input text:\n{repr(text)}\n")
    
    test_lexer(text)
    test_parser(text)


if __name__ == '__main__':
    main()
