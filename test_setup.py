#!/usr/bin/env python3
"""
Test script to verify MathWorks automation setup
"""

import sys
import traceback
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import selenium
        print(f"✅ Selenium: {selenium.__version__}")
    except ImportError as e:
        print(f"❌ Selenium import failed: {e}")
        return False
    
    try:
        import webdriver_manager
        print(f"✅ WebDriver Manager available")
    except ImportError as e:
        print(f"❌ WebDriver Manager import failed: {e}")
        return False
    
    try:
        import pyperclip
        print(f"✅ Pyperclip available")
    except ImportError as e:
        print(f"❌ Pyperclip import failed: {e}")
        return False
    
    return True

def test_modules():
    """Test that our custom modules can be imported"""
    print("\n🧪 Testing custom modules...")
    
    modules = [
        'config',
        'utils', 
        'browser_manager',
        'auth_handler',
        'task_automator'
    ]
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            return False
    
    return True

def test_configuration():
    """Test configuration loading"""
    print("\n🧪 Testing configuration...")
    
    try:
        from config import Config
        
        # Test key configuration sections
        assert hasattr(Config, 'SELECTORS'), "Missing SELECTORS"
        assert hasattr(Config, 'TIMING'), "Missing TIMING"
        assert hasattr(Config, 'BROWSER_SETTINGS'), "Missing BROWSER_SETTINGS"
        
        print("✅ Configuration structure valid")
        
        # Test selector structure
        selectors = Config.SELECTORS
        required_sections = ['left_panel', 'right_panel', 'task_navigation']
        
        for section in required_sections:
            assert section in selectors, f"Missing selector section: {section}"
        
        print("✅ Selector configuration valid")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_browser_setup():
    """Test browser manager without actually opening browser"""
    print("\n🧪 Testing browser manager...")
    
    try:
        from browser_manager import BrowserManager
        
        # Test that we can create an instance
        manager = BrowserManager()
        print("✅ BrowserManager instantiation")
        
        # Test Chrome driver path resolution (without starting)
        from webdriver_manager.chrome import ChromeDriverManager
        driver_path = ChromeDriverManager().install()
        print(f"✅ Chrome driver available at: {driver_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Browser setup test failed: {e}")
        traceback.print_exc()
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("\n🧪 Testing file structure...")
    
    required_files = [
        'main.py',
        'config.py',
        'utils.py',
        'browser_manager.py',
        'auth_handler.py',
        'task_automator.py',
        'requirements.txt',
        'README.md'
    ]
    
    missing_files = []
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - Missing")
            missing_files.append(file)
    
    return len(missing_files) == 0

def main():
    """Run all tests"""
    print("🚀 MathWorks Automation Setup Test")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Package Imports", test_imports),
        ("Custom Modules", test_modules),
        ("Configuration", test_configuration),
        ("Browser Setup", test_browser_setup)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}: Unexpected error - {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal: {len(results)} | Passed: {passed} | Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! Your setup is ready to go.")
        print("Run 'python main.py' to start the automation.")
    else:
        print(f"\n⚠️ {failed} test(s) failed. Please fix the issues before running the automation.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
