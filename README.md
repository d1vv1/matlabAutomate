# MathWorks Course Automation Tool 🤖

---
**Disclaimer:**
This tool is developed strictly for my personal educational purposes to learn about browser automation and Python. It is NOT intended for cheating, bypassing academic integrity, or violating MathWorks' or any institution's terms of service. I do not condone or support cheating in any form. Please use this tool responsibly and ethically, and only for legitimate learning and research.
---

An advanced, modular automation tool for completing MathWorks courses using Selenium WebDriver. The tool intelligently navigates through course tasks, extracts solutions, and automates the completion process.

## 🌟 Features

- **Intelligent Element Detection**: Uses multiple fallback selectors for robust element finding
- **Modular Architecture**: Clean, maintainable code with separated concerns
- **Error Handling**: Comprehensive error handling with retry mechanisms
- **Logging**: Detailed logging for debugging and monitoring
- **HTML Structure Analysis**: Specifically designed to handle MathWorks' dual-panel layout
- **Anti-Detection**: Browser settings to avoid detection as an automated script
- **Context Managers**: Safe resource management with automatic cleanup

## 📁 Project Structure

```
├── main.py              # Main entry point and orchestration
├── config.py            # Configuration settings and selectors
├── browser_manager.py   # Browser setup and management
├── auth_handler.py      # Authentication and login logic
├── task_automator.py    # Core task automation logic
├── utils.py             # Utility functions and helpers
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── sample.html         # Reference HTML structure
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Chrome browser installed
- Internet connection

### Installation

1. **Clone or download the project:**
   ```bash
   cd /Users/divyanshu/Projects/solveTSforMe
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. **Run the automation tool:**
   ```bash
   python main.py
   ```

2. **Follow the interactive prompts:**
   - Enter your MathWorks course URL
   - Provide login credentials (if required)
   - Set task limits (optional)
   - Confirm and start automation

3. **Monitor progress:**
   - Watch the console output for real-time progress
   - Check `mathworks_automation.log` for detailed logs
   - Screenshots are taken automatically on errors

## 🔧 Configuration

### Customizing Selectors

Edit `config.py` to modify element selectors for different course layouts:

```python
SELECTORS = {
    'left_panel': {
        'container': '#motwDocumentContainerTabContainer0',
        'editor_textarea': 'textarea, .CodeMirror textarea'
    },
    'right_panel': {
        'container': '#motwDocumentContainerTabContainer1',
        'solution_content': '.textBox .textWrapper'
    }
}
```

### Timing Adjustments

Modify timing settings in `config.py`:

```python
TIMING = {
    'page_load': 3,
    'element_wait': 2,
    'action_delay': 1,
    'submit_wait': 3
}
```

### Browser Settings

Customize browser behavior:

```python
BROWSER_SETTINGS = {
    'headless': False,          # Set to True for headless mode
    'window_size': (1920, 1080),
    'disable_automation_detection': True
}
```

## 🏗️ Architecture

### Core Components

1. **MathWorksAutomator** (`main.py`): Main orchestrator
2. **BrowserManager** (`browser_manager.py`): Chrome setup and configuration
3. **AuthenticationHandler** (`auth_handler.py`): Login management
4. **MathWorksTaskAutomator** (`task_automator.py`): Task processing logic
5. **ElementFinder** (`utils.py`): Robust element location
6. **ActionHelper** (`utils.py`): Safe browser interactions

### HTML Structure Handling

The tool is specifically designed to handle MathWorks' dual-panel interface:

- **Left Panel**: Contains the editable workspace (`#motwDocumentContainerTabContainer0`)
- **Right Panel**: Contains the solution reference (`#motwDocumentContainerTabContainer1`)
- **Code Elements**: Extracts from `.textBox .textWrapper` structures

## 🛠️ Advanced Usage

### Custom Element Selectors

If default selectors don't work, inspect the page and update `config.py`:

```python
# Example: Adding new selectors for a different course layout
'custom_task_selector': '.new-task-class',
'custom_solution_btn': '//button[@data-action="show-solution"]'
```

### Error Handling Configuration

Customize error handling behavior:

```python
ERROR_HANDLING = {
    'max_retries': 3,           # Retry attempts
    'retry_delay': 2,           # Delay between retries
    'continue_on_error': True,  # Continue if task fails
    'screenshot_on_error': True # Take screenshots on errors
}
```

### Logging Levels

Adjust logging verbosity:

```python
LOGGING = {
    'level': 'DEBUG',  # DEBUG, INFO, WARNING, ERROR
    'file': 'mathworks_automation.log'
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Elements Not Found**
   - Check browser console for JavaScript errors
   - Verify selectors using Chrome DevTools
   - Increase timing delays in `config.py`

2. **Login Failures**
   - Ensure correct credentials
   - Check for CAPTCHA requirements
   - Verify login page structure hasn't changed

3. **Task Processing Errors**
   - Check `mathworks_automation.log` for details
   - Look at error screenshots in project directory
   - Verify course page has fully loaded

### Debug Mode

Enable detailed logging by setting:

```python
LOGGING = {'level': 'DEBUG'}
```

### Manual Inspection

The browser remains open after completion for manual inspection. Use this to:
- Verify final state
- Check for any missed elements
- Understand page structure changes

## 📊 Monitoring

### Log Files

- **Console Output**: Real-time progress and summaries
- **mathworks_automation.log**: Detailed operation logs
- **Error Screenshots**: Automatic screenshots on failures

### Success Metrics

The tool provides comprehensive reporting:
- Total tasks found and processed
- Success/failure counts
- Overall completion percentage
- Detailed per-task status

## ⚖️ Legal and Ethical Considerations

- **Terms of Service**: Ensure compliance with MathWorks' ToS
- **Educational Use**: Intended for legitimate educational purposes
- **Rate Limiting**: Built-in delays to avoid overwhelming servers
- **Respectful Automation**: Does not bypass security measures

## 🔄 Version History

### v2.0 (Current)
- Modular architecture with separated concerns
- Enhanced HTML structure handling
- Improved error handling and retry mechanisms
- Comprehensive logging and monitoring
- Context manager support for safe resource management

### v1.0
- Basic automation functionality
- Single-file implementation
- Basic element detection

## 🤝 Contributing

To improve the tool:

1. Fork the repository
2. Create feature branches
3. Add comprehensive tests
4. Update documentation
5. Submit pull requests

## 📝 License

This project is for educational purposes. Please respect MathWorks' terms of service and use responsibly.

## 🆘 Support

For issues and questions:

1. Check the troubleshooting section
2. Review log files for detailed error information
3. Inspect browser state when automation pauses
4. Verify element selectors using Chrome DevTools

---

**Note**: This tool is designed specifically for MathWorks' course interface as of 2025. Interface changes may require selector updates in `config.py`.
