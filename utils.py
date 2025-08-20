"""
Utility functions for MathWorks Course Automation
"""

import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import Config

# Set up logging
logging.basicConfig(
    level=getattr(logging, Config.LOGGING['level']),
    format=Config.LOGGING['format'],
    handlers=[
        logging.FileHandler(Config.LOGGING['file']),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ElementFinder:
    """Utility class for finding elements with multiple selector strategies"""
    
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
    
    def find_element_by_selectors(self, selectors, timeout=None):
        """
        Try multiple selectors to find an element
        
        Args:
            selectors (list): List of CSS selectors or XPath expressions
            timeout (int): Custom timeout for this search
            
        Returns:
            WebElement or None
        """
        wait_time = timeout or Config.TIMING['element_wait']
        
        for selector in selectors:
            try:
                if selector.startswith('//'):
                    element = WebDriverWait(self.driver, wait_time).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                else:
                    element = WebDriverWait(self.driver, wait_time).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                logger.debug(f"Found element using selector: {selector}")
                return element
            except TimeoutException:
                continue
        
        logger.warning(f"Could not find element using any of the selectors: {selectors}")
        return None
    
    def find_clickable_element_by_selectors(self, selectors, timeout=None):
        """
        Try multiple selectors to find a clickable element
        
        Args:
            selectors (list): List of CSS selectors or XPath expressions
            timeout (int): Custom timeout for this search
            
        Returns:
            WebElement or None
        """
        wait_time = timeout or Config.TIMING['element_wait']
        
        for selector in selectors:
            try:
                if selector.startswith('//'):
                    element = WebDriverWait(self.driver, wait_time).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                else:
                    element = WebDriverWait(self.driver, wait_time).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                logger.debug(f"Found clickable element using selector: {selector}")
                return element
            except TimeoutException:
                continue
        
        logger.warning(f"Could not find clickable element using any of the selectors: {selectors}")
        return None
    
    def find_multiple_elements_by_selectors(self, selectors):
        """
        Try multiple selectors to find multiple elements
        
        Args:
            selectors (list): List of CSS selectors or XPath expressions
            
        Returns:
            List of WebElements
        """
        for selector in selectors:
            try:
                if selector.startswith('//'):
                    elements = self.driver.find_elements(By.XPATH, selector)
                else:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                
                if elements:
                    logger.debug(f"Found {len(elements)} elements using selector: {selector}")
                    return elements
            except Exception:
                continue
        
        logger.warning(f"Could not find elements using any of the selectors: {selectors}")
        return []

class ActionHelper:
    """Helper class for common web automation actions"""
    
    def __init__(self, driver, element_finder):
        self.driver = driver
        self.element_finder = element_finder
    
    def safe_click(self, element, retries=3):
        """
        Safely click an element with retries
        
        Args:
            element: WebElement to click
            retries (int): Number of retry attempts
            
        Returns:
            bool: Success status
        """
        for attempt in range(retries):
            try:
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                time.sleep(0.5)
                element.click()
                logger.debug("Successfully clicked element")
                return True
            except Exception as e:
                logger.warning(f"Click attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(Config.TIMING['action_delay'])
        
        logger.error("Failed to click element after all retries")
        return False
    
    def safe_send_keys(self, element, text, clear_first=True):
        """
        Safely send keys to an element
        
        Args:
            element: WebElement to send keys to
            text (str): Text to send
            clear_first (bool): Whether to clear the element first
            
        Returns:
            bool: Success status
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            time.sleep(0.5)
            
            if clear_first:
                element.clear()
                time.sleep(0.5)
            
            element.send_keys(text)
            logger.debug(f"Successfully sent text to element: {text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Failed to send keys to element: {e}")
            return False
    
    def extract_text_from_elements(self, elements):
        """
        Extract and clean text from multiple elements
        
        Args:
            elements: List of WebElements
            
        Returns:
            str: Combined cleaned text
        """
        text_lines = []
        
        for element in elements:
            try:
                text = element.text.strip()
                if text and text not in text_lines:
                    text_lines.append(text)
            except Exception as e:
                logger.warning(f"Failed to extract text from element: {e}")
        
        combined_text = "\n".join(text_lines)
        logger.debug(f"Extracted text: {combined_text[:100]}...")
        return combined_text
    
    def wait_for_page_load(self, timeout=None):
        """
        Wait for page to be fully loaded
        
        Args:
            timeout (int): Custom timeout
        """
        wait_time = timeout or Config.TIMING['page_load']
        try:
            WebDriverWait(self.driver, wait_time).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            time.sleep(1)  # Additional wait for dynamic content
            logger.debug("Page fully loaded")
        except TimeoutException:
            logger.warning("Page load timeout reached")

def take_screenshot_on_error(driver, error_description):
    """
    Take a screenshot when an error occurs
    
    Args:
        driver: WebDriver instance
        error_description (str): Description of the error
    """
    if Config.ERROR_HANDLING['screenshot_on_error']:
        try:
            timestamp = int(time.time())
            filename = f"error_screenshot_{timestamp}.png"
            driver.save_screenshot(filename)
            logger.info(f"Screenshot saved: {filename} - {error_description}")
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")

def retry_on_failure(func, max_retries=None, delay=None):
    """
    Decorator to retry function calls on failure
    
    Args:
        func: Function to retry
        max_retries (int): Maximum number of retries
        delay (int): Delay between retries
        
    Returns:
        Function result or None if all retries fail
    """
    retries = max_retries or Config.ERROR_HANDLING['max_retries']
    retry_delay = delay or Config.ERROR_HANDLING['retry_delay']
    
    def wrapper(*args, **kwargs):
        for attempt in range(retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt < retries:
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                else:
                    logger.error(f"All {retries + 1} attempts failed for {func.__name__}")
                    raise e
    
    return wrapper
