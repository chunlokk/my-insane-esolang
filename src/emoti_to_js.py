#!/usr/bin/env python3
"""
EmotiLang to JavaScript Compiler

This script takes an EmotiLang (.emoti) file, parses it into an AST,
and transpiles it to JavaScript.

Usage:
    python emoti_to_js.py input.emoti [output.js]
    
    If output.js is not specified, it will be generated automatically
    by replacing .emoti extension with .js
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path

# Add the src directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parser import EmotiLexer, EmotiParser
from transpile_js import transpile_to_javascript, save_transpiled_code


def parse_emoti_file(file_path: str):
    """
    Parse an EmotiLang file and return the AST
    
    Args:
        file_path (str): Path to the .emoti file
        
    Returns:
        ASTNode: The parsed AST, or None if parsing failed
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📂 Reading file: {file_path}")
        print(f"📝 File size: {len(content)} characters")
        
        # Create lexer and parser
        lexer = EmotiLexer()
        parser = EmotiParser()
        
        # Tokenize the input
        print("🔍 Tokenizing...")
        tokens = lexer.tokenize(content)
        
        # Parse tokens into AST
        print("🌳 Parsing into AST...")
        ast = parser.parse(tokens)
        
        if ast:
            print("✅ Parsing successful!")
            return ast
        else:
            print("❌ Parsing failed!")
            return None
            
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found")
        return None
    except Exception as e:
        print(f"❌ Error parsing file: {e}")
        return None


def transpile_to_js(ast, output_path: str):
    """
    Transpile AST to JavaScript and save to file
    
    Args:
        ast: The AST to transpile
        output_path (str): Path to save the JavaScript file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print("🔄 Transpiling to JavaScript...")
        
        # Transpile AST to JavaScript
        js_code = transpile_to_javascript(ast)
        
        # Save to file
        save_transpiled_code(ast, output_path)
        
        print(f"✅ JavaScript generated successfully!")
        print(f"📁 Output saved to: {output_path}")
        
        # Show the generated code
        print("\n" + "="*50)
        print("Generated JavaScript Code:")
        print("="*50)
        print(js_code)
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error transpiling to JavaScript: {e}")
        return False


def run_javascript(js_file_path: str):
    """
    Attempt to run the generated JavaScript file using Node.js
    
    Args:
        js_file_path (str): Path to the JavaScript file
    """
    try:
        print(f"\n🚀 Running JavaScript with Node.js...")
        print("="*30)
        result = subprocess.run(['node', js_file_path], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        
        if result.returncode == 0:
            print("✅ Execution successful!")
            if result.stdout:
                print("📤 Output:")
                print(result.stdout)
        else:
            print("❌ Execution failed!")
            if result.stderr:
                print("🚨 Error:")
                print(result.stderr)
                
    except subprocess.TimeoutExpired:
        print("⏱️  Execution timed out (10 seconds)")
    except FileNotFoundError:
        print("⚠️  Node.js not found. Install Node.js to run the generated JavaScript.")
    except Exception as e:
        print(f"❌ Error running JavaScript: {e}")


def get_js_code_only(input_text: str):
    """
    Parse EmotiLang code and return only the JavaScript code
    
    Args:
        input_text (str): EmotiLang source code as string
        
    Returns:
        str: JavaScript code, or None if parsing/transpilation failed
    """
    try:
        # Create lexer and parser
        lexer = EmotiLexer()
        parser = EmotiParser()
        
        # Parse the input
        ast = parser.parse(lexer.tokenize(input_text))
        if not ast:
            return None
        
        # Transpile to JavaScript
        js_code = transpile_to_javascript(ast)
        return js_code
        
    except Exception:
        return None


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Compile EmotiLang (.emoti) files to JavaScript",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python emoti_to_js.py program.emoti
  python emoti_to_js.py program.emoti output.js
  python emoti_to_js.py program.emoti --run
  python emoti_to_js.py program.emoti --output result.js --run
        """
    )
    
    parser.add_argument('input_file', 
                       help='Input EmotiLang file (.emoti)')
    parser.add_argument('output_file', 
                       nargs='?',
                       help='Output JavaScript file (.js). If not specified, '
                            'will use input filename with .js extension')
    parser.add_argument('-o', '--output',
                       help='Output JavaScript file (alternative to positional argument)')
    parser.add_argument('-r', '--run',
                       action='store_true',
                       help='Run the generated JavaScript with Node.js after compilation')
    parser.add_argument('-v', '--verbose',
                       action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Determine input file
    input_file = args.input_file
    if not input_file.endswith('.emoti'):
        print("⚠️  Warning: Input file doesn't have .emoti extension")
    
    # Determine output file
    if args.output:
        output_file = args.output
    elif args.output_file:
        output_file = args.output_file
    else:
        # Generate output filename by replacing .emoti with .js
        input_path = Path(input_file)
        output_file = str(input_path.with_suffix('.js'))
    
    if args.verbose:
        print(f"🎯 Input file: {input_file}")
        print(f"🎯 Output file: {output_file}")
    
    print("🎭 EmotiLang to JavaScript Compiler")
    print("="*40)
    
    # Step 1: Parse the EmotiLang file
    ast = parse_emoti_file(input_file)
    if not ast:
        print("💥 Compilation failed at parsing stage")
        sys.exit(1)
    
    if args.verbose:
        print(f"\n🌳 AST Structure:")
        print(f"   {ast}")
    
    # Step 2: Transpile to JavaScript
    success = transpile_to_js(ast, output_file)
    if not success:
        print("💥 Compilation failed at transpilation stage")
        sys.exit(1)
    
    # Step 3: Optionally run the JavaScript
    if args.run:
        run_javascript(output_file)
    
    print(f"\n🎉 Compilation completed successfully!")
    if not args.run:
        print(f"💡 Run the JavaScript with: node {output_file}")


def demo_mode():
    """Run a demonstration with example files"""
    print("🎭 EmotiLang to JavaScript Compiler - Demo Mode")
    print("="*50)
    
    # Look for example files
    examples_dir = Path("../docs/examples")
    if not examples_dir.exists():
        examples_dir = Path("docs/examples")
    
    if examples_dir.exists():
        emoti_files = list(examples_dir.glob("*.emoti"))
        if emoti_files:
            print(f"Found {len(emoti_files)} example EmotiLang files:")
            for i, file in enumerate(emoti_files, 1):
                print(f"  {i}. {file.name}")
            
            # Process the first example file
            example_file = emoti_files[0]
            print(f"\n🎯 Compiling {example_file.name}...")
            
            ast = parse_emoti_file(str(example_file))
            if ast:
                output_file = f"demo_{example_file.stem}.js"
                transpile_to_js(ast, output_file)
                run_javascript(output_file)
        else:
            print("No .emoti files found in examples directory")
    else:
        print("Examples directory not found")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments provided, show help
        print("🎭 EmotiLang to JavaScript Compiler")
        print("\nUsage:")
        print("  python emoti_to_js.py <input.emoti> [output.js]")
        print("  python emoti_to_js.py --help")
        print("\nFor demo mode with example files:")
        print("  python emoti_to_js.py --demo")
        print("\nExamples:")
        print("  python emoti_to_js.py program.emoti")
        print("  python emoti_to_js.py program.emoti --run")
        print("  python emoti_to_js.py program.emoti output.js --run")
    elif len(sys.argv) == 2 and sys.argv[1] == '--demo':
        demo_mode()
    else:
        main()
