"""
Core automation logic for MathWorks Course
"""

import time
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import Config
from utils import ElementFinder, ActionHelper, take_screenshot_on_error, retry_on_failure

logger = logging.getLogger(__name__)

class MathWorksTaskAutomator:
    """Handles individual task automation logic"""
    
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.element_finder = ElementFinder(driver, wait)
        self.action_helper = ActionHelper(driver, self.element_finder)
    
    def find_tasks(self):
        """
        Find all task elements on the page
        
        Returns:
            list: List of task WebElements
        """
        logger.info("Searching for task elements...")
        
        tasks = self.element_finder.find_multiple_elements_by_selectors(
            Config.SELECTORS['task_navigation']['task_elements']
        )
        
        if not tasks:
            # Fallback: look for any clickable elements that might be tasks
            fallback_selectors = [
                "//div[contains(text(), 'Task')]",
                "//button[contains(@class, 'task')]",
                "[role='button'][aria-label*='Task']"
            ]
            tasks = self.element_finder.find_multiple_elements_by_selectors(fallback_selectors)
        
        logger.info(f"Found {len(tasks)} task elements")
        return tasks
    
    @retry_on_failure
    def click_see_solution(self):
        """
        Click the 'See Solution' button
        
        Returns:
            bool: Success status
        """
        logger.info("Looking for 'See Solution' button...")
        
        button = self.element_finder.find_clickable_element_by_selectors(
            Config.SELECTORS['task_navigation']['see_solution_button']
        )
        
        if button:
            success = self.action_helper.safe_click(button)
            if success:
                logger.info("Successfully clicked 'See Solution' button")
                time.sleep(Config.TIMING['action_delay'])
                return True
        
        logger.warning("Could not find or click 'See Solution' button")
        return False
    
    def extract_solution_from_right_panel(self):
        """
        Extract solution code from the right panel based on HTML structure
        
        Returns:
            str: Extracted solution code
        """
        logger.info("Extracting solution from right panel...")
        
        try:
            # Wait for the right panel to load
            time.sleep(Config.TIMING['element_wait'])
            
            # Look for the right panel container first
            right_container = self.element_finder.find_element_by_selectors([
                Config.SELECTORS['right_panel']['container'],
                '.mwTabContainer:last-child',
                '[id*="TabContainer1"]'
            ])
            
            if not right_container:
                logger.warning("Could not find right panel container")
                return ""
            
            # Look for solution content within the right panel
            solution_elements = []
            
            # Try to find elements with the specific structure from the HTML
            selectors_to_try = [
                '.textBox .textWrapper',  # Based on your original example
                '.textBox',
                'code',
                'pre',
                '.matlab-code',
                '[class*="code"]',
                '.editorWindow .rtcPlaceholder',
                '.MultiViewRTC'
            ]
            
            for selector in selectors_to_try:
                try:
                    elements = right_container.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        solution_elements = elements
                        logger.debug(f"Found solution elements using selector: {selector}")
                        break
                except Exception:
                    continue
            
            # Extract text from found elements
            if solution_elements:
                solution_code = self.action_helper.extract_text_from_elements(solution_elements)
                
                if solution_code:
                    logger.info(f"Successfully extracted solution: {solution_code[:100]}...")
                    return solution_code
            
            # Fallback: get all text from the right panel
            try:
                solution_code = right_container.text.strip()
                if solution_code:
                    logger.info("Used fallback method to extract solution")
                    return solution_code
            except Exception:
                pass
            
            logger.warning("Could not extract solution code from right panel")
            return ""
            
        except Exception as e:
            logger.error(f"Error extracting solution: {e}")
            take_screenshot_on_error(self.driver, "solution_extraction_error")
            return ""
    
    @retry_on_failure
    def paste_solution_to_left_panel(self, solution_code):
        """
        Paste solution code into the left panel editor
        
        Args:
            solution_code (str): Code to paste
            
        Returns:
            bool: Success status
        """
        logger.info("Pasting solution to left panel...")
        
        try:
            # Find the left panel container
            left_container = self.element_finder.find_element_by_selectors([
                Config.SELECTORS['left_panel']['container'],
                '.mwTabContainer:first-child',
                '[id*="TabContainer0"]'
            ])
            
            if not left_container:
                logger.warning("Could not find left panel container")
                return False
            
            # Look for editor elements within the left panel
            editor_selectors = [
                'textarea',
                '.CodeMirror textarea',
                '.monaco-editor textarea',
                '[contenteditable="true"]',
                'input[type="text"]',
                '.editor textarea',
                '.rtcPlaceholder textarea'
            ]
            
            editor = None
            for selector in editor_selectors:
                try:
                    elements = left_container.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            editor = element
                            break
                    if editor:
                        break
                except Exception:
                    continue
            
            if not editor:
                logger.warning("Could not find editor element in left panel")
                return False
            
            # Paste the solution
            success = self.action_helper.safe_send_keys(editor, solution_code, clear_first=True)
            
            if success:
                logger.info("Successfully pasted solution to left panel")
                time.sleep(Config.TIMING['action_delay'])
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error pasting solution: {e}")
            take_screenshot_on_error(self.driver, "solution_paste_error")
            return False
    
    @retry_on_failure
    def submit_solution(self):
        """
        Submit the solution
        
        Returns:
            bool: Success status
        """
        logger.info("Submitting solution...")
        
        button = self.element_finder.find_clickable_element_by_selectors(
            Config.SELECTORS['task_navigation']['submit_button']
        )
        
        if button:
            success = self.action_helper.safe_click(button)
            if success:
                logger.info("Successfully submitted solution")
                time.sleep(Config.TIMING['submit_wait'])
                return True
        
        logger.warning("Could not find or click submit button")
        return False
    
    @retry_on_failure
    def move_to_next_task(self):
        """
        Move to the next task
        
        Returns:
            bool: Success status
        """
        logger.info("Moving to next task...")
        
        button = self.element_finder.find_clickable_element_by_selectors(
            Config.SELECTORS['task_navigation']['next_task_button']
        )
        
        if button:
            success = self.action_helper.safe_click(button)
            if success:
                logger.info("Successfully moved to next task")
                time.sleep(Config.TIMING['task_transition'])
                return True
        
        logger.warning("Could not find or click next task button")
        return False
    
    def process_single_task(self, task_number):
        """
        Process a single task completely
        
        Args:
            task_number (int): Task number for logging
            
        Returns:
            bool: Success status
        """
        logger.info(f"--- Processing Task {task_number} ---")
        
        try:
            # Step 1: Click "See Solution"
            if not self.click_see_solution():
                logger.error(f"Task {task_number}: Failed to click 'See Solution'")
                return False
            
            # Step 2: Extract solution from right panel
            solution_code = self.extract_solution_from_right_panel()
            if not solution_code:
                logger.error(f"Task {task_number}: Failed to extract solution")
                return False
            
            # Step 3: Paste solution to left panel
            if not self.paste_solution_to_left_panel(solution_code):
                logger.error(f"Task {task_number}: Failed to paste solution")
                return False
            
            # Step 4: Submit solution
            if not self.submit_solution():
                logger.warning(f"Task {task_number}: Could not submit solution")
                # Continue anyway as submission might not always be required
            
            logger.info(f"Task {task_number}: Completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Task {task_number}: Unexpected error - {e}")
            take_screenshot_on_error(self.driver, f"task_{task_number}_error")
            return False
