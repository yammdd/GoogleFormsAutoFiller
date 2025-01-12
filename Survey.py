import random
import time
import threading
from PyQt6.QtWidgets import QApplication
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

class Survey:

    def __init__(self, webdriver_path, form_url, target_response, ui=None):
        self.webdriver_path = webdriver_path
        self.form_url = form_url
        self.target_response = target_response
        self.ui = ui
        self.stop = threading.Event()
        self.complete = 0

        # Initialize the browser
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
        chrome_options.add_argument("--no-sandbox")  # For running in environments like Docker
        chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent resource limits

        service = Service(webdriver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        #self.driver = webdriver.Chrome(service=service)

    @staticmethod
    def random_text():
        """Generate random text for form fields."""
        return random.choice(['Text 1', 'Text 2', 'Text 3', 'Text 4', 'Text 5'])

    def fill_form(self, answers_list, input_text=""):
        """Fill out the form fields automatically based on their type."""
        try:
            # Handle multiple-choice questions.
            radio_groups = self.driver.find_elements(By.XPATH, '//div[@role="radiogroup"]')
            if radio_groups:
                for radiogroup in radio_groups:
                    options = radiogroup.find_elements(By.XPATH, './/div[@role="radio"]')
                    if options:
                        selected_option = None
                        for option in options:
                            if option.get_attribute("aria-checked") == "true":
                                selected_option = option
                                break
                        if not selected_option:
                            valid_answers = {
                                option.get_attribute("aria-label"): 
                                    option for option in options 
                                if option.get_attribute("aria-label") in answers_list
                            }
                            if valid_answers:
                                first_valid_answer = next(iter(valid_answers.values()))
                                first_valid_answer.click()
                            else:
                                valid_options = [option for option in options if option.get_attribute("aria-label") != 'Mục khác:']
                                random.choice(valid_options).click()

            # Handle checkbox questions.
            checkboxes = self.driver.find_elements(By.XPATH, '//div[@role="listitem"]')
            if checkboxes:
                for checkbox_group in checkboxes:
                    checkboxes = checkbox_group.find_elements(By.XPATH, './/div[@role="checkbox"]')
                    if checkboxes:
                        random.choice(checkboxes).click()

            # Handle short text fields.
            short_text_fields = self.driver.find_elements(By.XPATH, '//input[@type="text"]')
            if short_text_fields:
                for short_field in short_text_fields:
                    try:
                        parent = short_field.find_element(By.XPATH, './ancestor::div[@role="radiogroup"]')
                    except:
                        parent = None
                    if parent and len(answers_list) > 0:
                        continue
                    if input_text:
                        short_field.send_keys(input_text)
                    else:
                        short_field.send_keys(self.random_text())

            # Handle long text fields.
            long_text_fields = self.driver.find_elements(By.XPATH, '//textarea')
            if long_text_fields:
                for long_field in long_text_fields:
                    try:
                        parent = long_field.find_element(By.XPATH, './ancestor::div[@role="radiogroup"]')
                    except:
                        parent = None
                    if parent and len(answers_list) > 0:
                        continue
                    if input_text:
                        long_field.send_keys(input_text)
                    else:
                        long_field.send_keys(self.random_text())

            # Handle dropdown questions
            drop_groups = self.driver.find_elements(By.XPATH, '//div[@role="presentation"]')
            if drop_groups:
                for drop_group in drop_groups:
                    try:
                        drop_group.click()
                        time.sleep(0.3)
                        select_options = drop_group.find_elements(By.XPATH, './/div[@role="option"]')
                        if select_options and isinstance(select_options, list):
                            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(select_options))
                            random.choice(select_options).click()
                    except Exception as e:
                        print(f"Error: {e}")

            time.sleep(0.2)  # Delay between processing each question

        except Exception as e:
            print(f"Error while filling form: {e}")

    def click_next(self):
        """Click the 'Next' button if available."""
        try:
            next_button = self.driver.find_element(By.XPATH, '//span[contains(text(), "Tiếp")]')
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(next_button))
            next_button.click()
            self.driver.execute_script("document.body.style.zoom='40%'")
            time.sleep(1)
            return True
        except Exception as e:
            print(f"Error while clicking next: {e}")
            return False

    def submit_form(self):
        """Click the 'Submit' button to submit the form."""
        try:
            submit_button = self.driver.find_element(By.XPATH, '//span[contains(text(), "Gửi")]')
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(submit_button))
            submit_button.click()
            self.driver.execute_script("document.body.style.zoom='40%'")
            self.complete += 1
            time.sleep(1)  # Wait for page reload after submission
        except Exception as e:
            print(f"Error while submitting form: {e}")

    def start(self, answers_list, input_text=""):
        """Start the survey automation."""
        try:
            while self.complete < self.target_response:
                if self.stop.is_set():
                    if self.ui:
                        self.ui.add_item_to_list_widget("Đã dừng chương trình.")
                    break

                self.driver.get(self.form_url)
                self.driver.execute_script("document.body.style.zoom='40%'")
                time.sleep(1)  # Wait for the page to load
                while True:
                    self.fill_form(answers_list, input_text)
                    if self.click_next():
                        time.sleep(1)
                    else:
                        self.submit_form()
                        break
                if self.ui:
                    self.ui.add_item_to_list_widget(f"Đã gửi. Tổng số phản hồi: {self.complete}/{self.target_response}")
                    QApplication.processEvents()
            if self.ui:
                self.ui.add_item_to_list_widget(f"Hoàn thành. Tổng số phản hồi: {self.complete}/{self.target_response}")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            try:
                self.driver.quit()
            except Exception as quit_error:
                print(f"Browser already closed. Clean exit. ({quit_error})")

    def quit_anyway(self):
        """Close the browser."""
        self.stop.set()


# Setup and run the survey automation
def run_survey(url, response_number, answers_list, input_text, ui=None):
    """Run the survey automation."""
    path = "data/chromedriver.exe"  # ChromeDriver path
    survey = Survey(path, url, response_number, ui=ui)
    survey.start(answers_list, input_text)

def quit_browser(url, response_number, ui=None):
    """Close the browser."""
    path = "data/chromedriver.exe"  # ChromeDriver path
    survey = Survey(path, url, response_number, ui=ui)
    survey.quit_anyway()


