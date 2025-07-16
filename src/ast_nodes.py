from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict


class ASTNode(ABC):
    """Base class for all AST nodes"""
    
    def __init__(self):
        pass
        
    def __repr__(self) -> str:
        return f"<{type(self).__name__}>"


# Literals
class NumberLiteral(ASTNode):
    def __init__(self, value: float):
        super().__init__()
        self.value = value
        
    def __repr__(self) -> str:
        return f"<NumberLiteral value={self.value}>"


class StringLiteral(ASTNode):
    def __init__(self, value: str):
        super().__init__()
        self.value = value
        
    def __repr__(self) -> str:
        return f"<StringLiteral value={repr(self.value)}>"


class BooleanLiteral(ASTNode):
    def __init__(self, value: bool):
        super().__init__()
        self.value = value
        
    def __repr__(self) -> str:
        return f"<BooleanLiteral value={self.value}>"


# Identifiers
class Identifier(ASTNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        
    def __repr__(self) -> str:
        return f"<Identifier name={self.name}>"


# Types
class Type(ASTNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        
    def __repr__(self) -> str:
        return f"<Type name={self.name}>"


# Expressions
class BinaryOp(ASTNode):
    def __init__(self, left: ASTNode, operator: str, right: ASTNode):
        super().__init__()
        self.left = left
        self.operator = operator
        self.right = right
        
    def __repr__(self) -> str:
        return f"<BinaryOp left={self.left} op={self.operator} right={self.right}>"


class UnaryOp(ASTNode):
    def __init__(self, operator: str, operand: ASTNode):
        super().__init__()
        self.operator = operator
        self.operand = operand
        
    def __repr__(self) -> str:
        return f"<UnaryOp op={self.operator} operand={self.operand}>"


class FunctionCall(ASTNode):
    def __init__(self, name: str, arguments: List[ASTNode]):
        super().__init__()
        self.name = name
        self.arguments = arguments
        
    def __repr__(self) -> str:
        return f"<FunctionCall name={self.name} args={self.arguments}>"


class InputExpression(ASTNode):
    def __init__(self):
        super().__init__()
        
    def __repr__(self) -> str:
        return "<InputExpression>"


# Statements
class Assignment(ASTNode):
    def __init__(self, identifier: str, expression: ASTNode):
        super().__init__()
        self.identifier = identifier
        self.expression = expression
        
    def __repr__(self) -> str:
        return f"<Assignment id={self.identifier} expr={self.expression}>"


class VariableDeclaration(ASTNode):
    def __init__(self, identifier: str, var_type: Type, initial_value: Optional[ASTNode] = None):
        super().__init__()
        self.identifier = identifier
        self.var_type = var_type
        self.initial_value = initial_value
        
    def __repr__(self) -> str:
        return f"<VariableDeclaration id={self.identifier} type={self.var_type} init={self.initial_value}>"


class PrintStatement(ASTNode):
    def __init__(self, expression: ASTNode):
        super().__init__()
        self.expression = expression
        
    def __repr__(self) -> str:
        return f"<PrintStatement expr={self.expression}>"


class ReturnStatement(ASTNode):
    def __init__(self, expression: Optional[ASTNode] = None):
        super().__init__()
        self.expression = expression
        
    def __repr__(self) -> str:
        return f"<ReturnStatement expr={self.expression}>"


class ThrowStatement(ASTNode):
    def __init__(self, expression: ASTNode):
        super().__init__()
        self.expression = expression
        
    def __repr__(self) -> str:
        return f"<ThrowStatement expr={self.expression}>"


class ExpressionStatement(ASTNode):
    def __init__(self, expression: ASTNode):
        super().__init__()
        self.expression = expression
        
    def __repr__(self) -> str:
        return f"<ExpressionStatement expr={self.expression}>"


# Control Flow
class Block(ASTNode):
    def __init__(self, statements: List[ASTNode]):
        super().__init__()
        self.statements = statements
        
    def __repr__(self) -> str:
        return f"<Block statements={len(self.statements)}>"


class IfStatement(ASTNode):
    def __init__(self, condition: ASTNode, then_block: Block, else_block: Optional[Block] = None):
        super().__init__()
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block
        
    def __repr__(self) -> str:
        return f"<IfStatement condition={self.condition} then={self.then_block} else={self.else_block}>"


class WhileLoop(ASTNode):
    def __init__(self, condition: ASTNode, body: Block):
        super().__init__()
        self.condition = condition
        self.body = body
        
    def __repr__(self) -> str:
        return f"<WhileLoop condition={self.condition} body={self.body}>"


class TryStatement(ASTNode):
    def __init__(self, try_block: Block, catch_variable: str, catch_block: Block):
        super().__init__()
        self.try_block = try_block
        self.catch_variable = catch_variable
        self.catch_block = catch_block
        
    def __repr__(self) -> str:
        return f"<TryStatement try={self.try_block} catch_var={self.catch_variable} catch={self.catch_block}>"


# Function and Struct Definitions
class Parameter(ASTNode):
    def __init__(self, name: str, param_type: Type):
        super().__init__()
        self.name = name
        self.param_type = param_type
        
    def __repr__(self) -> str:
        return f"<Parameter name={self.name} type={self.param_type}>"


class FunctionDeclaration(ASTNode):
    def __init__(self, name: str, parameters: List[Parameter], return_type: Type, block: Block):
        super().__init__()
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.block = block
        
    def __repr__(self) -> str:
        return f"<FunctionDeclaration name={self.name} params={len(self.parameters)} statements={len(self.block.statements)} return_type={self.return_type}>"


# Program
class Program(ASTNode):
    def __init__(self, declarations: List[ASTNode]):
        super().__init__()
        self.declarations = declarations
        
    def __repr__(self) -> str:
        return f"<Program declarations={len(self.declarations)}>"
