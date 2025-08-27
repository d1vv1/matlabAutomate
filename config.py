# Configuration file for MathWorks Course Automation

class Config:
    """Configuration class for MathWorks automation"""
    
    # Browser settings
    BROWSER_SETTINGS = {
        'headless': False,
        'window_size': (1920, 1080),
        'disable_automation_detection': True,
        'page_load_timeout': 30,
        'implicit_wait': 10
    }
    
    # Timing settings (in seconds)
    TIMING = {
        'page_load': 3,
        'element_wait': 2,
        'action_delay': 1,
        'submit_wait': 3,
        'task_transition': 2
    }
    
    # Element selectors based on the provided HTML structure
    SELECTORS = {
        # Main document container
        'document_container': '.documentContainer',
        
        # Left panel (editor tab)
        'left_panel': {
            'container': '#motwDocumentContainerTabContainer0',
            'tab': '.tab.checkedTab.selectedGroup',
            'editor_window': '.editorWindow.liveCode',
            'editor_textarea': 'textarea, .CodeMirror textarea, [contenteditable="true"]',
            'rtc_placeholder': '.rtcPlaceholder'
        },
        
        # Right panel (solution tab)
        'right_panel': {
            'container': '#motwDocumentContainerTabContainer1',
            'tab': '.tab.checkedTab.selectedGroup',
            'editor_window': '.editorWindow.liveCode',
            'solution_content': '.textBox .textWrapper, .textBox, code, pre'
        },
        
        # Task navigation
        'task_navigation': {
            'task_elements': [
                '[data-testid*="task"]',
                '.task',
                '[class*="task"]',
                '.exercise',
                'div[class*="task"]'
            ],
            'see_solution_button': [
                '//button[contains(text(), "See Solution")]',
                '//a[contains(text(), "See Solution")]',
                '//span[contains(text(), "See Solution")]',
                '[data-testid*="solution"]',
                '.see-solution',
                '[aria-label*="solution"]'
            ],
            'submit_button': [
                '//button[contains(text(), "Submit")]',
                '//button[contains(text(), "Run")]',
                '//button[contains(text(), "Execute")]',
                '[data-testid*="submit"]',
                '.submit-button',
                '[type="submit"]'
            ],
            'next_task_button': [
                '//button[contains(text(), "Next")]',
                '//button[contains(text(), "Continue")]',
                '[data-testid*="next"]',
                '.next-button',
                '.continue-button'
            ]
        },
        
        # Login elements
        'login': {
            'sign_in_link': [
                'a.mwa-nav_login',
                'a.headernav_login',
                'a[aria-label*="Sign In"]',
                'a[id*="login"]',
                'a.nav-link[href*="login"]',
                '//a[contains(text(), "Sign In")]',
                '//a[contains(@class, "login")]'
            ],
            'subdomain_selection': [
                '#recommended_domain_button',
                '.btn.btn_color_blue[data-lang]',
                'a[href*="mathworks.com/"][class*="btn"]',
                '.recommended-country',
                '//a[contains(@class, "btn") and contains(@href, "mathworks.com")]',
                '//button[contains(text(), "Continue")]',
                '//a[contains(@class, "recommended")]'
            ],
            'username_field': 'input[name="userId"]',  # Updated for MathWorks email field
            'password_field': '#password',
            'submit_button': 'button[type="submit"]',
            'email_submit_button': [
                'button[type="submit"]',
                '//button[contains(text(), "Next")]',
                '//button[contains(text(), "Continue")]',
                '//button[contains(text(), "Submit")]',
                '.btn[type="submit"]'
            ]
        }
    }
    
    # Error handling
    ERROR_HANDLING = {
        'max_retries': 3,
        'retry_delay': 2,
        'continue_on_error': True,
        'screenshot_on_error': True
    }
    
    # Logging
    LOGGING = {
        'level': 'INFO',
        'format': '%(asctime)s - %(levelname)s - %(message)s',
        'file': 'mathworks_automation.log'
    }
