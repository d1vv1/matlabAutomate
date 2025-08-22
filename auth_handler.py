"""
Authentication handler for MathWorks
"""

import time
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from config import Config
from utils import ElementFinder, ActionHelper

logger = logging.getLogger(__name__)

class AuthenticationHandler:
    """Handles MathWorks login and authentication"""
    
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.element_finder = ElementFinder(driver, wait)
        self.action_helper = ActionHelper(driver, self.element_finder)
    
    def login(self, username, password):
        """
        Login to MathWorks
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            bool: Success status
        """
        logger.info("Attempting to login to MathWorks...")
        
        try:
            # First, check if we need to click the "Sign In" link
            if not self.click_sign_in_link():
                logger.warning("Could not find or click sign-in link, checking if already on login page")
            
            # Look for username field
            username_field = self.element_finder.find_element_by_selectors([
                Config.SELECTORS['login']['username_field'],
                '#email',
                'input[name="username"]',
                'input[type="email"]'
            ])
            
            if not username_field:
                logger.warning("No login form found after clicking sign-in link")
                return False
            
            # Look for password field
            password_field = self.element_finder.find_element_by_selectors([
                Config.SELECTORS['login']['password_field'],
                'input[name="password"]',
                'input[type="password"]'
            ])
            
            if not password_field:
                logger.error("Found username field but no password field")
                return False
            
            # Look for submit button
            submit_button = self.element_finder.find_clickable_element_by_selectors([
                Config.SELECTORS['login']['submit_button'],
                'button[type="submit"]',
                'input[type="submit"]',
                '//button[contains(text(), "Sign In")]',
                '//button[contains(text(), "Login")]'
            ])
            
            if not submit_button:
                logger.error("Could not find login submit button")
                return False
            
            # Fill in credentials
            logger.info("Filling in credentials...")
            
            if not self.action_helper.safe_send_keys(username_field, username):
                logger.error("Failed to enter username")
                return False
            
            if not self.action_helper.safe_send_keys(password_field, password):
                logger.error("Failed to enter password")
                return False
            
            # Submit login form
            if not self.action_helper.safe_click(submit_button):
                logger.error("Failed to click login button")
                return False
            
            # Wait for login to complete
            self.action_helper.wait_for_page_load(timeout=10)
            
            # Check if login was successful by looking for common post-login elements
            success_indicators = [
                '.user-menu',
                '.logout',
                '.dashboard',
                '[data-testid*="user"]',
                '.profile'
            ]
            
            post_login_element = self.element_finder.find_element_by_selectors(
                success_indicators, timeout=5
            )
            
            if post_login_element:
                logger.info("Login successful")
                return True
            else:
                # Check for error messages
                error_selectors = [
                    '.error',
                    '.alert-danger',
                    '[class*="error"]',
                    '[role="alert"]'
                ]
                
                error_element = self.element_finder.find_element_by_selectors(
                    error_selectors, timeout=2
                )
                
                if error_element:
                    error_message = error_element.text
                    logger.error(f"Login failed with error: {error_message}")
                else:
                    logger.warning("Login status unclear - no success or error indicators found")
                
                return False
                
        except Exception as e:
            logger.error(f"Login failed with exception: {e}")
            return False
    
    def is_logged_in(self):
        """
        Check if already logged in
        
        Returns:
            bool: Login status
        """
        try:
            # Look for indicators that user is logged in
            logged_in_indicators = [
                '.user-menu',
                '.logout',
                '.dashboard',
                '[data-testid*="user"]',
                '.profile',
                '//a[contains(text(), "Sign Out")]',
                '//button[contains(text(), "Logout")]'
            ]
            
            element = self.element_finder.find_element_by_selectors(
                logged_in_indicators, timeout=3
            )
            
            if element:
                logger.info("User appears to be already logged in")
                return True
            
            # Look for login form indicators
            login_indicators = [
                '#userId',
                '#email',
                'input[name="username"]',
                'input[type="email"]',
                '//button[contains(text(), "Sign In")]'
            ]
            
            login_element = self.element_finder.find_element_by_selectors(
                login_indicators, timeout=3
            )
            
            if login_element:
                logger.info("Login form detected - user not logged in")
                return False
            
            logger.info("Could not determine login status")
            return False
            
        except Exception as e:
            logger.error(f"Error checking login status: {e}")
            return False
    
    def click_sign_in_link(self):
        """
        Click the sign-in anchor tag to navigate to login page
        
        Returns:
            bool: Success status
        """
        logger.info("Looking for sign-in link...")
        
        try:
            # Use selectors from config first, then fallbacks
            all_selectors = Config.SELECTORS['login']['sign_in_link'] + [
                'a[href*="login"]',
                '.login-link',
                '#login-link',
                '//a[contains(text(), "Login")]',
                '//a[contains(text(), "log in")]'
            ]
            
            sign_in_link = self.element_finder.find_clickable_element_by_selectors(all_selectors)
            
            if sign_in_link:
                success = self.action_helper.safe_click(sign_in_link)
                if success:
                    logger.info("Successfully clicked sign-in link")
                    # Wait for login page to load
                    self.action_helper.wait_for_page_load(timeout=10)
                    return True
                else:
                    logger.warning("Failed to click sign-in link")
                    return False
            else:
                logger.warning("Could not find sign-in link")
                return False
                
        except Exception as e:
            logger.error(f"Error clicking sign-in link: {e}")
            return False
