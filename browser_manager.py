"""
Browser setup and management for MathWorks Course Automation
"""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from config import Config

logger = logging.getLogger(__name__)

class BrowserManager:
    """Manages browser setup and configuration"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
    
    def setup_chrome_driver(self):
        """
        Set up Chrome WebDriver with optimized settings
        
        Returns:
            tuple: (driver, wait) instances
        """
        try:
            # Set up Chrome options
            options = Options()
            
            # Anti-detection measures
            if Config.BROWSER_SETTINGS['disable_automation_detection']:
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
            
            # Performance optimizations
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            
            # Window size
            if Config.BROWSER_SETTINGS['window_size']:
                width, height = Config.BROWSER_SETTINGS['window_size']
                options.add_argument(f"--window-size={width},{height}")
            
            # Headless mode (optional)
            if Config.BROWSER_SETTINGS.get('headless', False):
                options.add_argument("--headless")
            
            # Set up service
            service = Service(ChromeDriverManager().install())
            
            # Create driver
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Additional anti-detection
            if Config.BROWSER_SETTINGS['disable_automation_detection']:
                self.driver.execute_script(
                    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
                )
            
            # Set timeouts
            self.driver.set_page_load_timeout(Config.BROWSER_SETTINGS['page_load_timeout'])
            self.driver.implicitly_wait(Config.BROWSER_SETTINGS['implicit_wait'])
            
            # Create wait instance
            self.wait = WebDriverWait(self.driver, Config.BROWSER_SETTINGS['implicit_wait'])
            
            logger.info("Chrome WebDriver successfully initialized")
            return self.driver, self.wait
            
        except Exception as e:
            logger.error(f"Failed to setup Chrome driver: {e}")
            raise
    
    def close_browser(self):
        """Close the browser and clean up resources"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Browser closed successfully")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self.setup_chrome_driver()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close_browser()
        
        if exc_type:
            logger.error(f"Exception in browser context: {exc_type.__name__}: {exc_val}")
        
        return False  # Don't suppress exceptions
