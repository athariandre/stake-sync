#!/usr/bin/env python3
"""Simple test to verify code structure without external dependencies."""
import sys
import ast

def check_python_syntax(filepath):
    """Check if Python file has valid syntax."""
    try:
        with open(filepath, 'r') as f:
            code = f.read()
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, str(e)

def main():
    """Test all Python files for syntax errors."""
    python_files = [
        'app/__init__.py',
        'app/config.py',
        'app/main.py',
        'app/database/__init__.py',
        'app/database/database.py',
        'app/database/init_db.py',
        'app/database/models.py',
        'app/services/__init__.py',
        'app/services/gemini_service.py',
        'app/services/sendgrid_service.py',
        'app/services/style_analyzer.py',
        'app/services/memory_service.py',
        'app/services/draft_generator.py',
        'app/routes/__init__.py',
        'app/routes/auth.py',
        'app/routes/updates.py',
        'app/routes/style.py',
        'app/routes/drafts.py',
        'app/routes/review.py',
        'app/routes/send.py',
        'app/routes/dashboard.py',
        'app/routes/audience.py',
    ]
    
    all_passed = True
    for filepath in python_files:
        passed, error = check_python_syntax(filepath)
        if passed:
            print(f"✓ {filepath}")
        else:
            print(f"✗ {filepath}: {error}")
            all_passed = False
    
    if all_passed:
        print("\n✓ All files have valid Python syntax!")
        return 0
    else:
        print("\n✗ Some files have syntax errors!")
        return 1

if __name__ == '__main__':
    sys.exit(main())
