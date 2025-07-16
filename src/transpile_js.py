"""Sample AST provided by test_parser.py and demo.emoti

AST root type: <class 'ast_nodes.Program'>
Program
  declarations:
    [0]:
      VariableDeclaration: myNumber : type=number 
        initial_value:
          NumberLiteral: 42 
    [1]:
      Assignment: myNumber 
        expression:
          BinaryOp: + 
            left:
              NumberLiteral: 2 
            right:
              BinaryOp: * 
                left:
                  NumberLiteral: 3 
                right:
                  NumberLiteral: 5 
    [2]:
      VariableDeclaration: myInput : type=string 
        initial_value:
          InputExpression
    [3]:
      PrintStatement
        expression:
          Identifier: myInput 
    [4]:
      FunctionDeclaration: factorial : return_type=number : <Block statements=2> 
        parameters:
          [0]:
            Parameter: n : param_type=number 
        block:
          Block
            statements:
              [0]:
                IfStatement
                  condition:
                    BinaryOp: == 
                      left:
                        Identifier: n 
                      right:
                        NumberLiteral: 0 
                  then_block:
                    Block
                      statements:
                        [0]:
                          ReturnStatement
                            expression:
                              NumberLiteral: 1 
              [1]:
                ReturnStatement
                  expression:
                    BinaryOp: * 
                      left:
                        Identifier: n 
                      right:
                        FunctionCall: factorial 
    [5]:
      PrintStatement
        expression:
          FunctionCall: factorial 
    [6]:
      VariableDeclaration: counter : type=number 
        initial_value:
          NumberLiteral: 0 
    [7]:
      WhileLoop
        condition:
          BinaryOp: < 
            left:
              Identifier: counter 
            right:
              NumberLiteral: 5 
        body:
          Block
            statements:
              [0]:
                PrintStatement
                  expression:
                    Identifier: counter 
              [1]:
                Assignment: counter 
                  expression:
                    BinaryOp: + 
                      left:
                        Identifier: counter 
                      right:
                        NumberLiteral: 1 
    [8]:
      TryStatement: catch_var=e 
        try_block:
          Block
            statements:
              [0]:
                ThrowStatement
                  expression:
                    StringLiteral: 'Something went wrong' 
        catch_block:
          Block
            statements:
              [0]:
                PrintStatement
                  expression:
                    StringLiteral: 'Caught error: ' 

"""

from typing import List, Dict, Any
from ast_nodes import *


class JavaScriptTranspiler:
    """Transpiles EmotiLang AST nodes to JavaScript code"""
    
    def __init__(self):
        self.indent_level = 0
        self.operator_map = {
            # Arithmetic operators
            ':+)': '+',
            ':-(': '-',
            '*_*': '*',
            ':/': '/',
            ':%': '%',
            
            # Comparison operators
            '=)': '===',
            '!(': '!==',
            '>:)': '>',
            '<:(': '<',
            '>=)': '>=',
            '<=': '<=',
            
            # Logical operators
            '&)': '&&',
            '|)': '||',
            '!)': '!',
        }
    
    def get_indent(self) -> str:
        """Get current indentation string"""
        return "  " * self.indent_level
    
    def transpile(self, node: ASTNode) -> str:
        """Main transpilation method that dispatches to specific node handlers"""
        method_name = f"transpile_{type(node).__name__}"
        method = getattr(self, method_name, None)
        if method:
            return method(node)
        else:
            raise NotImplementedError(f"Transpilation not implemented for {type(node).__name__}")
    
    def transpile_Program(self, node: Program) -> str:
        """Transpile a program (top-level)"""
        lines = []
        lines.append("// Transpiled from EmotiLang")
        lines.append("")
        
        for declaration in node.declarations:
            transpiled = self.transpile(declaration)
            if transpiled.strip():
                lines.append(transpiled)
        
        return "\n".join(lines)
    
    def transpile_NumberLiteral(self, node: NumberLiteral) -> str:
        """Transpile number literals"""
        return str(node.value)
    
    def transpile_StringLiteral(self, node: StringLiteral) -> str:
        """Transpile string literals"""
        # Ensure proper escaping
        escaped = node.value.replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t')
        return f'"{escaped}"'
    
    def transpile_BooleanLiteral(self, node: BooleanLiteral) -> str:
        """Transpile boolean literals"""
        return "true" if node.value else "false"
    
    def transpile_Identifier(self, node: Identifier) -> str:
        """Transpile identifiers (variable names)"""
        return node.name
    
    def transpile_Type(self, node: Type) -> str:
        """Transpile type annotations (for comments only in JS)"""
        type_map = {
            ':0': 'number',
            ':L': 'string', 
            'X_X': 'boolean'
        }
        return type_map.get(node.name, node.name)
    
    def transpile_BinaryOp(self, node: BinaryOp) -> str:
        """Transpile binary operations"""
        left = self.transpile(node.left)
        right = self.transpile(node.right)
        operator = self.operator_map.get(node.operator, node.operator)
        return f"({left} {operator} {right})"
    
    def transpile_UnaryOp(self, node: UnaryOp) -> str:
        """Transpile unary operations"""
        operand = self.transpile(node.operand)
        operator = self.operator_map.get(node.operator, node.operator)
        return f"({operator}{operand})"
    
    def transpile_FunctionCall(self, node: FunctionCall) -> str:
        """Transpile function calls"""
        args = [self.transpile(arg) for arg in node.arguments]
        return f"{node.name}({', '.join(args)})"
    
    def transpile_InputExpression(self, node: InputExpression) -> str:
        """Transpile input expressions (using prompt in browser or readline in Node.js)"""
        return 'prompt("Enter input:")'
    
    def transpile_Assignment(self, node: Assignment) -> str:
        """Transpile assignment statements"""
        expr = self.transpile(node.expression)
        return f"{self.get_indent()}{node.identifier} = {expr};"
    
    def transpile_VariableDeclaration(self, node: VariableDeclaration) -> str:
        """Transpile variable declarations"""
        type_comment = f" // {self.transpile_Type(node.var_type)}" if node.var_type else ""
        
        if node.initial_value:
            value = self.transpile(node.initial_value)
            return f"{self.get_indent()}let {node.identifier} = {value};{type_comment}"
        else:
            return f"{self.get_indent()}let {node.identifier};{type_comment}"
    
    def transpile_PrintStatement(self, node: PrintStatement) -> str:
        """Transpile print statements to console.log"""
        expr = self.transpile(node.expression)
        return f"{self.get_indent()}console.log({expr});"
    
    def transpile_ReturnStatement(self, node: ReturnStatement) -> str:
        """Transpile return statements"""
        if node.expression:
            expr = self.transpile(node.expression)
            return f"{self.get_indent()}return {expr};"
        else:
            return f"{self.get_indent()}return;"
    
    def transpile_ThrowStatement(self, node: ThrowStatement) -> str:
        """Transpile throw statements"""
        expr = self.transpile(node.expression)
        return f"{self.get_indent()}throw new Error({expr});"
    
    def transpile_ExpressionStatement(self, node: ExpressionStatement) -> str:
        """Transpile expression statements"""
        expr = self.transpile(node.expression)
        return f"{self.get_indent()}{expr};"
    
    def transpile_Block(self, node: Block) -> str:
        """Transpile code blocks"""
        lines = []
        lines.append(f"{self.get_indent()}{{")
        
        self.indent_level += 1
        for stmt in node.statements:
            transpiled = self.transpile(stmt)
            if transpiled.strip():
                lines.append(transpiled)
        self.indent_level -= 1
        
        lines.append(f"{self.get_indent()}}}")
        return "\n".join(lines)
    
    def transpile_IfStatement(self, node: IfStatement) -> str:
        """Transpile if statements"""
        condition = self.transpile(node.condition)
        lines = []
        
        lines.append(f"{self.get_indent()}if ({condition}) {{")
        
        self.indent_level += 1
        for stmt in node.then_block.statements:
            transpiled = self.transpile(stmt)
            if transpiled.strip():
                lines.append(transpiled)
        self.indent_level -= 1
        
        if node.else_block:
            lines.append(f"{self.get_indent()}}} else {{")
            self.indent_level += 1
            for stmt in node.else_block.statements:
                transpiled = self.transpile(stmt)
                if transpiled.strip():
                    lines.append(transpiled)
            self.indent_level -= 1
        
        lines.append(f"{self.get_indent()}}}")
        return "\n".join(lines)
    
    def transpile_WhileLoop(self, node: WhileLoop) -> str:
        """Transpile while loops"""
        condition = self.transpile(node.condition)
        lines = []
        
        lines.append(f"{self.get_indent()}while ({condition}) {{")
        
        self.indent_level += 1
        for stmt in node.body.statements:
            transpiled = self.transpile(stmt)
            if transpiled.strip():
                lines.append(transpiled)
        self.indent_level -= 1
        
        lines.append(f"{self.get_indent()}}}")
        return "\n".join(lines)
    
    def transpile_TryStatement(self, node: TryStatement) -> str:
        """Transpile try-catch statements"""
        lines = []
        
        lines.append(f"{self.get_indent()}try {{")
        
        self.indent_level += 1
        for stmt in node.try_block.statements:
            transpiled = self.transpile(stmt)
            if transpiled.strip():
                lines.append(transpiled)
        self.indent_level -= 1
        
        lines.append(f"{self.get_indent()}}} catch ({node.catch_variable}) {{")
        
        self.indent_level += 1
        for stmt in node.catch_block.statements:
            transpiled = self.transpile(stmt)
            if transpiled.strip():
                lines.append(transpiled)
        self.indent_level -= 1
        
        lines.append(f"{self.get_indent()}}}")
        return "\n".join(lines)
    
    def transpile_Parameter(self, node: Parameter) -> str:
        """Transpile function parameters"""
        type_comment = f" /* {self.transpile_Type(node.param_type)} */" if node.param_type else ""
        return f"{node.name}{type_comment}"
    
    def transpile_FunctionDeclaration(self, node: FunctionDeclaration) -> str:
        """Transpile function declarations"""
        params = [self.transpile(param) for param in node.parameters]
        return_type_comment = f" /* -> {self.transpile_Type(node.return_type)} */" if node.return_type else ""
        
        lines = []
        lines.append(f"{self.get_indent()}function {node.name}({', '.join(params)}){return_type_comment} {{")
        
        self.indent_level += 1
        for stmt in node.block.statements:
            transpiled = self.transpile(stmt)
            if transpiled.strip():
                lines.append(transpiled)
        self.indent_level -= 1
        
        lines.append(f"{self.get_indent()}}}")
        return "\n".join(lines)


def transpile_to_javascript(ast: ASTNode) -> str:
    """
    Convenience function to transpile an AST to JavaScript
    
    Args:
        ast: The root AST node (typically a Program node)
        
    Returns:
        str: The transpiled JavaScript code
    """
    transpiler = JavaScriptTranspiler()
    return transpiler.transpile(ast)


def save_transpiled_code(ast: ASTNode, output_file: str) -> None:
    """
    Transpile AST to JavaScript and save to file
    
    Args:
        ast: The root AST node
        output_file: Path to save the JavaScript file
    """
    js_code = transpile_to_javascript(ast)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_code)


if __name__ == "__main__":
    # Example usage
    print("JavaScript Transpiler for EmotiLang")
    print("Import this module and use transpile_to_javascript(ast) function")
    print("or save_transpiled_code(ast, 'output.js') to save to file")
    print("\nFor usage examples, see test_transpiler.py and demo_transpiler.py")
    print("\nOperator mappings:")
    print("  :+) -> +   (addition/concatenation)")
    print("  :-( -> -   (subtraction)")
    print("  *_* -> *   (multiplication)")
    print("  :/  -> /   (division)")
    print("  =)  -> === (equality)")
    print("  >:) -> >   (greater than)")
    print("  <:( -> <   (less than)")
    print("  &)  -> &&  (logical AND)")
    print("  |)  -> ||  (logical OR)")
    print("  !)  -> !   (logical NOT)")

