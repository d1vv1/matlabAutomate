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
            # First, check for subdomain selection (region/country selection)
            # This must happen BEFORE clicking sign-in link
            if not self.handle_subdomain_selection():
                logger.warning("Subdomain selection handling failed or not required")
            
            # After subdomain selection, check if we need to click the "Sign In" link
            if not self.click_sign_in_link():
                logger.warning("Could not find or click sign-in link, checking if already on login page")
            
            # Give extra time for login form to load
            logger.info("Waiting for login form to load...")
            time.sleep(3)  # Extra wait for form to appear
            
            # Look for username/email field (first step of login)
            # Add more comprehensive selectors including class-based ones
            username_selectors = [
                'input[name="userId"]',
                '#userId', 
                'input[type="email"][name="userId"]',
                '.form-control[name="userId"]',
                'input.form-control[name="userId"]',
                'input[id="userId"]',
                'input[class*="form-control"][name="userId"]',
                # Additional fallback selectors
                'input[type="email"]',
                'input[name="email"]',
                'input[placeholder*="email"]',
                'input[placeholder*="Email"]',
                '.form-control[type="email"]',
                Config.SELECTORS['login']['username_field'],
                '#email',
                'input[name="username"]'
            ]
            
            username_field = self.element_finder.find_element_by_selectors(username_selectors)
            
            if not username_field:
                # Debug: Let's see what input fields are actually available
                logger.warning("Email field not found. Debugging available input fields...")
                try:
                    # Check if we're in an iframe
                    iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                    if iframes:
                        logger.info(f"Found {len(iframes)} iframes on page")
                        # Try switching to the first iframe
                        try:
                            self.driver.switch_to.frame(iframes[0])
                            logger.info("Switched to first iframe")
                            # Try finding the field again in the iframe
                            username_field = self.element_finder.find_element_by_selectors(username_selectors)
                            if username_field:
                                logger.info("Found email field in iframe!")
                        except Exception as e:
                            logger.warning(f"Could not switch to iframe: {e}")
                            self.driver.switch_to.default_content()
                    
                    if not username_field:
                        all_inputs = self.driver.find_elements(By.TAG_NAME, "input")
                        logger.info(f"Found {len(all_inputs)} input elements on page")
                        for i, inp in enumerate(all_inputs[:10]):  # Log first 10 inputs
                            try:
                                inp_type = inp.get_attribute('type') or 'text'
                                inp_name = inp.get_attribute('name') or 'no-name'
                                inp_id = inp.get_attribute('id') or 'no-id'
                                inp_class = inp.get_attribute('class') or 'no-class'
                                inp_placeholder = inp.get_attribute('placeholder') or 'no-placeholder'
                                logger.info(f"Input {i+1}: type='{inp_type}', name='{inp_name}', id='{inp_id}', class='{inp_class}', placeholder='{inp_placeholder}'")
                            except Exception:
                                logger.info(f"Input {i+1}: Could not get attributes")
                except Exception as e:
                    logger.warning(f"Could not debug input fields: {e}")
                
                if not username_field:
                    logger.warning("No email/username field found after subdomain selection and sign-in")
                    return False
            
            # Fill in email/username (first step)
            logger.info("Filling in email/username (first step)...")
            if not self.action_helper.safe_send_keys(username_field, username):
                logger.error("Failed to enter email/username")
                return False
            
            # Look for and click the "Next" or "Continue" button for email step
            email_submit_button = self.element_finder.find_clickable_element_by_selectors([
                'button[type="submit"]',
                '//button[contains(text(), "Next")]',
                '//button[contains(text(), "Continue")]',
                '//button[contains(text(), "Submit")]',
                '.btn[type="submit"]',
                Config.SELECTORS['login']['submit_button']
            ])
            
            if email_submit_button:
                logger.info("Clicking email submit button...")
                if not self.action_helper.safe_click(email_submit_button):
                    logger.error("Failed to click email submit button")
                    return False
                
                # Wait for password page to load
                self.action_helper.wait_for_page_load(timeout=10)
            else:
                logger.warning("No email submit button found, attempting to continue...")
            
            # Now look for password field (second step)
            password_field = self.element_finder.find_element_by_selectors([
                Config.SELECTORS['login']['password_field'],
                'input[name="password"]',
                'input[type="password"]',
                '#password'
            ])
            
            if not password_field:
                logger.error("No password field found after email submission")
                return False
            
            # Fill in password (second step)
            logger.info("Filling in password (second step)...")
            if not self.action_helper.safe_send_keys(password_field, password):
                logger.error("Failed to enter password")
                return False
            
            # Look for final submit button for password step
            final_submit_button = self.element_finder.find_clickable_element_by_selectors([
                'button[type="submit"]',
                'input[type="submit"]',
                '//button[contains(text(), "Sign In")]',
                '//button[contains(text(), "Login")]',
                '//button[contains(text(), "Submit")]',
                Config.SELECTORS['login']['submit_button']
            ])
            
            if not final_submit_button:
                logger.error("Could not find final login submit button")
                return False
            
            # Submit final login form
            logger.info("Submitting login form...")
            if not self.action_helper.safe_click(final_submit_button):
                logger.error("Failed to click final login button")
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
    
    def handle_subdomain_selection(self):
        """
        Handle MathWorks subdomain/region selection if it appears
        This should be called BEFORE clicking the sign-in link
        
        Returns:
            bool: Success status (True if handled or not needed)
        """
        logger.info("Checking for subdomain selection page (before sign-in)...")
        
        try:
            # Look for subdomain selection elements using config selectors
            subdomain_button = self.element_finder.find_clickable_element_by_selectors(
                Config.SELECTORS['login']['subdomain_selection'], timeout=5
            )
            
            if subdomain_button:
                # Get the country/region name for logging
                try:
                    country_text = subdomain_button.text or subdomain_button.get_attribute('aria-label') or "Unknown region"
                    logger.info(f"Found subdomain selection for: {country_text}")
                except:
                    logger.info("Found subdomain selection button")
                
                success = self.action_helper.safe_click(subdomain_button)
                
                if success:
                    logger.info("Successfully clicked subdomain selection button")
                    # Wait for page to load after subdomain selection
                    self.action_helper.wait_for_page_load(timeout=10)
                    return True
                else:
                    logger.warning("Failed to click subdomain selection button")
                    return False
            else:
                logger.info("No subdomain selection found - proceeding to sign-in")
                return True
                
        except Exception as e:
            logger.warning(f"Error handling subdomain selection: {e}")
            # Don't fail the entire login process for subdomain selection issues
            return True
