#!/usr/bin/env python3
"""
Flask server for EmotiLang Playground
Provides web interface for compiling and running EmotiLang code
"""

import os
import sys
import tempfile
import subprocess
import traceback
from flask import Flask, request, jsonify, render_template_string, send_from_directory
from pathlib import Path

# Add parent directory to path to import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from parser import EmotiLexer, EmotiParser
from transpile_js import transpile_to_javascript
import test_parser

app = Flask(__name__)

# Configure upload folder for temporary files
TEMP_DIR = tempfile.mkdtemp()

def capture_parser_output(code):
    """
    Run the parser on code and capture the debug output
    """
    try:
        # Create a temporary file
        temp_file = os.path.join(TEMP_DIR, 'temp_input.emoti')
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # Run test_parser.py and capture output
        result = subprocess.run([
            sys.executable, 'test_parser.py', temp_file
        ], 
        cwd=os.path.join(os.path.dirname(__file__), '..'),
        capture_output=True, 
        text=True, 
        timeout=10
        )
        
        # Clean up temp file
        try:
            os.remove(temp_file)
        except:
            pass
            
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr or result.stdout
            
    except subprocess.TimeoutExpired:
        return False, "Parser execution timed out"
    except Exception as e:
        return False, f"Parser error: {str(e)}"

def parse_and_transpile(code):
    """
    Parse EmotiLang code and transpile to JavaScript
    """
    try:
        # Create lexer and parser
        lexer = EmotiLexer()
        parser = EmotiParser()
        
        # Parse the code
        ast = parser.parse(lexer.tokenize(code))
        
        if ast is None:
            return False, None, "Failed to parse code"
        
        # Transpile to JavaScript
        js_code = transpile_to_javascript(ast)
        return True, js_code, None
        
    except Exception as e:
        error_msg = f"Transpilation error: {str(e)}\n{traceback.format_exc()}"
        return False, None, error_msg

@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('.', 'index.html')

@app.route('/styles.css')
def styles():
    """Serve CSS file"""
    return send_from_directory('.', 'styles.css')

@app.route('/script.js')
def script():
    """Serve JavaScript file"""
    return send_from_directory('.', 'script.js')

@app.route('/compile', methods=['POST'])
def compile_code():
    """
    Compile EmotiLang code to JavaScript
    """
    try:
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({
                'success': False,
                'error': 'No code provided'
            })
        
        code = data['code'].strip()
        if not code:
            return jsonify({
                'success': False,
                'error': 'Empty code provided'
            })
        
        # Get debug output from parser
        parser_success, debug_output = capture_parser_output(code)
        
        # Parse and transpile
        transpile_success, js_code, transpile_error = parse_and_transpile(code)
        
        if transpile_success:
            return jsonify({
                'success': True,
                'debug_output': debug_output,
                'js_code': js_code
            })
        else:
            return jsonify({
                'success': False,
                'error': transpile_error,
                'debug_output': debug_output
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

if __name__ == '__main__':
    # For development only - use Gunicorn for production
    app.run(host='0.0.0.0', port=8080, debug=True)