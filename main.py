"""
MathWorks Course Automation - Main Entry Point
Enhanced with modular architecture and improved HTML structure handling
"""

import logging
import time
from browser_manager import BrowserManager
from auth_handler import AuthenticationHandler
from task_automator import MathWorksTaskAutomator
from utils import take_screenshot_on_error
from config import Config

logger = logging.getLogger(__name__)

class MathWorksAutomator:
    """Main automation orchestrator class"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.browser_manager = None
        self.auth_handler = None
        self.task_automator = None
    
    def initialize(self):
        """Initialize all components"""
        try:
            # Set up browser
            self.browser_manager = BrowserManager()
            self.driver, self.wait = self.browser_manager.setup_chrome_driver()
            
            # Initialize handlers
            self.auth_handler = AuthenticationHandler(self.driver, self.wait)
            self.task_automator = MathWorksTaskAutomator(self.driver, self.wait)
            
            logger.info("MathWorks Automator initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize automator: {e}")
            return False
    
    def navigate_to_course(self, course_url):
        """Navigate to the course page"""
        try:
            logger.info(f"Navigating to course: {course_url}")
            self.driver.get(course_url)
            time.sleep(Config.TIMING['page_load'])
            
            # Wait for page to be fully loaded
            self.task_automator.action_helper.wait_for_page_load()
            
            logger.info("Successfully navigated to course page")
            return True
            
        except Exception as e:
            logger.error(f"Failed to navigate to course: {e}")
            take_screenshot_on_error(self.driver, "navigation_error")
            return False
    
    def automate_course(self, course_url, username=None, password=None, num_tasks=None):
        """
        Main method to automate the entire course
        
        Args:
            course_url (str): URL of the course
            username (str): Username for login (optional)
            password (str): Password for login (optional)
            num_tasks (int): Limit number of tasks to process (optional)
            
        Returns:
            bool: Success status
        """
        logger.info("Starting MathWorks course automation...")
        
        try:
            # Step 1: Navigate to course
            if not self.navigate_to_course(course_url):
                logger.error("Failed to navigate to course")
                return False
            
            # Step 2: Always attempt authentication
            if not self.auth_handler.login(username, password):
                logger.error("Login failed")
                return False
            
            # Step 3: Find all tasks
            tasks = self.task_automator.find_tasks()
            if not tasks:
                logger.error("No tasks found on the page")
                return False
            
            # Step 4: Limit number of tasks if specified
            if num_tasks and num_tasks > 0:
                tasks = tasks[:num_tasks]
                logger.info(f"Limited to first {num_tasks} tasks")
            
            logger.info(f"Starting automation for {len(tasks)} tasks")
            
            # Step 5: Process each task
            successful_tasks = 0
            for i, task in enumerate(tasks, 1):
                logger.info(f"\n{'='*50}")
                logger.info(f"Processing Task {i} of {len(tasks)}")
                logger.info(f"{'='*50}")
                
                try:
                    # Click on the task if needed
                    if task.is_displayed() and task.is_enabled():
                        try:
                            self.task_automator.action_helper.safe_click(task)
                            time.sleep(Config.TIMING['action_delay'])
                        except Exception:
                            logger.warning(f"Could not click task {i}, proceeding anyway")
                    
                    # Process the task
                    if self.task_automator.process_single_task(i):
                        successful_tasks += 1
                        logger.info(f"✅ Task {i} completed successfully")
                    else:
                        logger.error(f"❌ Task {i} failed")
                        
                        if not Config.ERROR_HANDLING['continue_on_error']:
                            logger.error("Stopping automation due to task failure")
                            break
                    
                    # Move to next task (except for the last one)
                    if i < len(tasks):
                        if not self.task_automator.move_to_next_task():
                            logger.warning("Could not move to next task automatically")
                            # Continue anyway as the next iteration might work
                
                except Exception as e:
                    logger.error(f"Unexpected error in task {i}: {e}")
                    take_screenshot_on_error(self.driver, f"task_{i}_unexpected_error")
                    
                    if not Config.ERROR_HANDLING['continue_on_error']:
                        break
                
                # Brief pause between tasks
                time.sleep(Config.TIMING['action_delay'])
            
            # Step 6: Summary
            logger.info(f"\n{'='*50}")
            logger.info("AUTOMATION SUMMARY")
            logger.info(f"{'='*50}")
            logger.info(f"Total tasks found: {len(tasks)}")
            logger.info(f"Successfully completed: {successful_tasks}")
            logger.info(f"Failed: {len(tasks) - successful_tasks}")
            logger.info(f"Success rate: {(successful_tasks/len(tasks)*100):.1f}%")
            
            if successful_tasks == len(tasks):
                logger.info("🎉 All tasks completed successfully!")
                return True
            elif successful_tasks > 0:
                logger.info("⚠️ Course partially completed")
                return True
            else:
                logger.error("❌ No tasks were completed successfully")
                return False
                
        except Exception as e:
            logger.error(f"Fatal error during course automation: {e}")
            take_screenshot_on_error(self.driver, "fatal_automation_error")
            return False
    
    def cleanup(self):
        """Clean up resources"""
        if self.browser_manager:
            self.browser_manager.close_browser()
        logger.info("Cleanup completed")
    
    def __enter__(self):
        """Context manager entry"""
        if self.initialize():
            return self
        else:
            raise RuntimeError("Failed to initialize MathWorks Automator")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()
        
        if exc_type:
            logger.error(f"Exception in automator context: {exc_type.__name__}: {exc_val}")
        
        return False  # Don't suppress exceptions

def get_user_input():
    """Get configuration from user input"""
    print("\n" + "="*60)
    print("🤖 MathWorks Course Automation Tool")
    print("="*60)
    
    config = {}
    
    # Course URL
    config['course_url'] = input("\n📚 Enter the course URL: ").strip()
    if not config['course_url']:
        print("❌ Course URL is required!")
        return None
    
    # Login credentials - always required now
    print("\n🔐 Login credentials required for MathWorks automation")
    config['username'] = input("👤 Enter username: ").strip()
    config['password'] = input("🔑 Enter password: ").strip()
    
    if not config['username'] or not config['password']:
        print("❌ Both username and password are required!")
        return None
    
    # Task limit
    limit_tasks = input("\n🎯 Limit number of tasks? (y/n): ").strip().lower() == 'y'
    if limit_tasks:
        try:
            config['num_tasks'] = int(input("🔢 Enter number of tasks to complete: "))
            if config['num_tasks'] <= 0:
                print("❌ Number of tasks must be positive!")
                return None
        except ValueError:
            print("❌ Invalid number! Processing all tasks.")
            config['num_tasks'] = None
    else:
        config['num_tasks'] = None
    
    # Confirmation
    print(f"\n📋 Configuration Summary:")
    print(f"   Course URL: {config['course_url']}")
    print(f"   Username: {config['username']}")
    print(f"   Task limit: {config['num_tasks'] if config['num_tasks'] else 'None (all tasks)'}")
    
    confirm = input(f"\n✅ Proceed with automation? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Automation cancelled by user.")
        return None
    
    return config

def main():
    """Main entry point"""
    try:
        # Get user configuration
        config = get_user_input()
        if not config:
            return
        
        print(f"\n🚀 Starting automation...")
        print(f"⏰ Estimated time: {(config['num_tasks'] or 5) * 30} seconds")
        print(f"📊 Check the log file for detailed progress: {Config.LOGGING['file']}")
        
        # Run automation using context manager
        with MathWorksAutomator() as automator:
            success = automator.automate_course(
                course_url=config['course_url'],
                username=config['username'],
                password=config['password'],
                num_tasks=config['num_tasks']
            )
            
            if success:
                print(f"\n🎉 Automation completed successfully!")
            else:
                print(f"\n⚠️ Automation completed with issues. Check the logs for details.")
            
            # Keep browser open for inspection
            print(f"\n🔍 Browser will remain open for inspection.")
            input("Press Enter to close the browser and exit...")
            
    except KeyboardInterrupt:
        print(f"\n⏹️ Automation stopped by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        print(f"\n❌ An unexpected error occurred: {e}")
        print(f"📄 Check the log file for details: {Config.LOGGING['file']}")
    finally:
        print(f"\n👋 Goodbye!")

if __name__ == "__main__":
    main()