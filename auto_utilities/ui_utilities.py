import json
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from auto_utilities.webdriver_utility import CustomWebDriverManager

DEFAULT_TIMEOUT = 10
IMAGE_FORMATS = {'png', 'jpeg'}
XPATH_PREFIXES = ('/', '(/')


class UIActions(CustomWebDriverManager):

    @classmethod
    def capture_console_browser_errors(cls, level: str, display_err=False):
        driver = cls.get_active_driver()
        logs = driver.get_log("browser")
        error_logs = [log['message'] for log in logs if log['level'] == level]
        if display_err:
            return error_logs
        elif len(error_logs) > 0:
            return True
        return False

    @classmethod
    def clear_input(cls, locator: str, index: int = 0, timeout: int = DEFAULT_TIMEOUT, scroll_options: dict = None):
        UIWaits.wait_until_clickable(locator, timeout, ignore_timeout=True)
        element = cls._find_element(locator, index=index, scroll_options=scroll_options)
        element.clear()

    @classmethod
    def click_element(cls, locator: str, index: int = 0, timeout: int = DEFAULT_TIMEOUT, scroll_options: dict = None):
        UIWaits.wait_until_clickable(locator, timeout, ignore_timeout=True)
        element = cls._find_element(locator, index=index, scroll_options=scroll_options)
        element.click()

    @classmethod
    def click_partial_link(cls, partial_text: str):
        element = cls.active_driver.find_element(By.PARTIAL_LINK_TEXT, partial_text)
        element.click()

    @classmethod
    def perform_mouse_click(cls, click_action: str, locator: str = None, x_offset: float = 0, y_offset: float = 0,
                            reset_position: bool = True, reset_actions: bool = True):
        cls.move_mouse(locator, x_offset, y_offset, reset_actions=False)
        actions = ActionChains(cls.active_driver)

        if click_action == 'click':
            actions.click()
        elif click_action == 'right_click':
            actions.context_click()
        elif click_action == 'double_click':
            actions.double_click()
        else:
            raise ValueError('Invalid click action specified')

        actions.perform()

        if reset_position:
            cls.move_mouse(x_offset=-x_offset, y_offset=-y_offset)

        if reset_actions:
            actions.reset_actions()

    @classmethod
    def delete_input(cls, locator: str, index: int = 0, timeout: int = DEFAULT_TIMEOUT, scroll_options: dict = None):
        UIWaits.wait_until_clickable(locator, timeout, ignore_timeout=True)
        element = cls._find_element(locator, index=index, scroll_options=scroll_options)
        text_content = element.text or element.get_attribute('value')
        for _ in text_content:
            element.send_keys(Keys.BACKSPACE)

    @classmethod
    def capture_element_screenshot(cls, locator: str, index: int = 0, scroll_options: dict = None,
                                   as_base64: bool = True, image_path: str = None):
        element = cls._find_element(locator, index=index, scroll_options=scroll_options)
        if image_path:
            return element.screenshot(image_path)
        elif as_base64:
            return element.screenshot_as_base64
        else:
            return element.screenshot_as_png

    @classmethod
    def enter_text(cls, locator: str, text: str, index: int = 0, click_first: bool = True, clear_first: bool = True,
                   timeout: int = DEFAULT_TIMEOUT, scroll_options: dict = None):
        UIWaits.wait_until_clickable(locator, timeout, ignore_timeout=True)
        element = cls._find_element(locator, index=index, scroll_options=scroll_options)
        if click_first:
            element.click()
        if clear_first:
            element.clear()
        element.send_keys(text)

    @classmethod
    def type_at_offset(cls, text: str, x_offset: float = 0, y_offset: float = 0, reset_actions: bool = True):
        actions = ActionChains(cls.active_driver)
        actions.move_by_offset(x_offset, y_offset)
        actions.send_keys(text)
        actions.perform()
        if reset_actions:
            actions.reset_actions()

    @classmethod
    def run_script(cls, script: str, locator: str = None, timeout: int = DEFAULT_TIMEOUT, index: int = 0,
                   scroll_options: dict = None):
        if locator:
            UIWaits.wait_until_clickable(locator, timeout, ignore_timeout=True)
            element = cls._find_element(locator, index=index, scroll_options=scroll_options)
            return cls.active_driver.execute_script(script, element)
        else:
            return cls.active_driver.execute_script(script)

    @classmethod
    def get_element_attribute(cls, locator: str, attribute: str, all_elements: bool = False, index: int = 0,
                              timeout: int = DEFAULT_TIMEOUT, scroll_options: dict = None):
        UIWaits.wait_until_visible(locator, timeout, ignore_timeout=True)
        elements = cls._find_elements(locator)
        if all_elements:
            return [el.get_attribute(attribute) for el in elements]
        else:
            element = elements[index]
            return element.get_attribute(attribute)

    @classmethod
    def get_element_location(cls, locator: str, scroll_to: bool = True, scroll_options: dict = None):
        element = cls._find_element(locator, scroll_to=scroll_to, scroll_options=scroll_options)
        return element.location

    @classmethod
    def get_css_property(cls, locator: str, property_name: str, all_elements: bool = False, index: int = 0,
                         timeout: int = DEFAULT_TIMEOUT, scroll_options: dict = None):
        UIWaits.wait_until_visible(locator, timeout, ignore_timeout=True)
        elements = cls._find_elements(locator)
        if all_elements:
            return [el.value_of_css_property(property_name) for el in elements]
        else:
            element = elements[index]
            return element.value_of_css_property(property_name)

    @classmethod
    def _find_elements(cls, locator: str):
        by = By.XPATH if locator.startswith(XPATH_PREFIXES) else By.CSS_SELECTOR
        elements = cls.active_driver.find_elements(by, locator)
        return elements

    @classmethod
    def _find_element(cls, locator: str, index: int = 0, scroll_to: bool = True, scroll_options: dict = None):
        elements = cls._find_elements(locator)
        if scroll_to:
            cls.scroll_to_view(locator, index, scroll_options)
        try:
            return elements[index]
        except IndexError:
            raise NoSuchElementException(f"No element found for locator '{locator}' at index {index}")

    @classmethod
    def count_elements(cls, locator: str):
        elements = cls._find_elements(locator)
        return len(elements)

    @classmethod
    def get_selected_option_text(cls, locator: str, all_elements: bool = False, index: int = 0,
                                 timeout: int = DEFAULT_TIMEOUT, scroll_options: dict = None):
        UIWaits.wait_until_visible(locator, timeout, ignore_timeout=True)
        elements = cls._find_elements(locator)
        if all_elements:
            return [Select(el).first_selected_option.text for el in elements]
        else:
            element = elements[index]
            return Select(element).first_selected_option.text

    @classmethod
    def get_element_text(cls, locator: str, all_elements: bool = False, index: int = 0, timeout: int = DEFAULT_TIMEOUT,
                         scroll_options: dict = None):
        UIWaits.wait_until_visible(locator, timeout, ignore_timeout=True)
        elements = cls._find_elements(locator)
        if all_elements:
            return [el.text for el in elements]
        else:
            element = elements[index]
            return element.text

    @classmethod
    def is_element_displayed(cls, locator: str, index: int = 0, scroll_options: dict = None):
        try:
            element = cls._find_element(locator, index=index, scroll_options=scroll_options)
            return element.is_displayed()
        except NoSuchElementException:
            return False

    @classmethod
    def is_partial_link_displayed(cls, partial_text: str):
        try:
            element = cls.active_driver.find_element(By.PARTIAL_LINK_TEXT, partial_text)
            return element.is_displayed()
        except NoSuchElementException:
            print('Partial link text not found')
            return False

    @classmethod
    def is_element_selected(cls, locator: str, index: int = 0, scroll_options: dict = None):
        element = cls._find_element(locator, index=index, scroll_options=scroll_options)
        return element.is_selected()

    @classmethod
    def move_mouse(cls, locator: str = None, x_offset: float = 0, y_offset: float = 0, reset_actions: bool = True):
        actions = ActionChains(cls.active_driver)
        if locator and x_offset:
            element = cls._find_element(locator, scroll_to=False)
            actions.move_to_element_with_offset(element, x_offset, y_offset).perform()
        elif locator:
            element = cls._find_element(locator, scroll_to=False)
            actions.move_to_element(element).perform()
        else:
            actions.move_by_offset(x_offset, y_offset).perform()

        if reset_actions:
            actions.reset_actions()

    @classmethod
    def execute_keyboard_shortcut(cls, key: str, modifier_key: str = None):
        actions = ActionChains(cls.active_driver)
        if modifier_key:
            actions.key_down(getattr(Keys, modifier_key.upper())).send_keys(key).key_up(
                getattr(Keys, modifier_key.upper()))
        else:
            actions.send_keys(getattr(Keys, key.upper()))
        actions.perform()
        actions.reset_actions()

    @classmethod
    def scroll_to_view(cls, locator: str, index: int = 0, scroll_options: dict = None):
        element = cls._find_element(locator, index=index, scroll_to=False)
        script = "arguments[0].scrollIntoView();"
        if scroll_options:
            script = f"arguments[0].scrollIntoView({json.dumps(scroll_options)});"
        cls.active_driver.execute_script(script, element)

    @classmethod
    def select_option_by_text(cls, locator: str, option_text: str, index: int = 0, timeout: int = DEFAULT_TIMEOUT,
                              scroll_options: dict = None):
        UIWaits.wait_until_visible(locator, timeout, ignore_timeout=True)
        element = cls._find_element(locator, index=index, scroll_options=scroll_options)
        Select(element).select_by_visible_text(option_text)

    @classmethod
    def select_option_matching_text(cls, dropdown_locator: str, options_locator: str, text: str, index: int = 0,
                                    click_dropdown: bool = True, timeout: int = DEFAULT_TIMEOUT,
                                    scroll_options: dict = None):
        if click_dropdown:
            UIWaits.wait_until_visible(dropdown_locator, timeout, ignore_timeout=True)
            dropdown_element = cls._find_element(dropdown_locator, index=index, scroll_options=scroll_options)
            dropdown_element.click()

        options = cls._find_elements(f'{dropdown_locator}{options_locator}')
        for option in options:
            if option.text == text:
                option.click()
                return
        raise ValueError(f'Option with text "{text}" not found')

    @classmethod
    def is_element_enabled(cls, locator: str, index: int = 0, scroll_options: dict = None):
        try:
            element = cls._find_element(locator, index=index, scroll_options=scroll_options)
            return element.is_enabled()
        except NoSuchElementException:
            return False

    @classmethod
    def is_element_focused(cls, locator: str, index: int = 0, scroll_options: dict = None):
        try:
            element = cls._find_element(locator, index=index, scroll_options=scroll_options)
            return element == cls.active_driver.switch_to.active_element
        except NoSuchElementException:
            return False


class UIWaits(CustomWebDriverManager):

    @classmethod
    def wait_until_alert_present(cls, timeout: int = DEFAULT_TIMEOUT, ignore_timeout: bool = False):
        try:
            WebDriverWait(cls.active_driver, timeout).until(EC.alert_is_present())
        except TimeoutException:
            if ignore_timeout:
                print('Alert did not appear within the timeout period')
            else:
                raise

    @classmethod
    def wait_until_visible(cls, locator: str, timeout: int = DEFAULT_TIMEOUT, ignore_timeout: bool = False):
        by = By.XPATH if locator.startswith(XPATH_PREFIXES) else By.CSS_SELECTOR
        try:
            WebDriverWait(cls.active_driver, timeout).until(EC.presence_of_element_located((by, locator)))
            WebDriverWait(cls.active_driver, timeout).until(EC.visibility_of_element_located((by, locator)))
        except TimeoutException:
            if ignore_timeout:
                print(f'Element "{locator}" did not become visible within the timeout period')
            else:
                raise

    @classmethod
    def wait_until_clickable(cls, locator: str, timeout: int = DEFAULT_TIMEOUT, ignore_timeout: bool = False):
        by = By.XPATH if locator.startswith(XPATH_PREFIXES) else By.CSS_SELECTOR
        try:
            WebDriverWait(cls.active_driver, timeout).until(EC.element_to_be_clickable((by, locator)))
        except TimeoutException:
            if ignore_timeout:
                print(f'Element "{locator}" was not clickable within the timeout period')
            else:
                raise

    @classmethod
    def wait_until_stale(cls, locator: str, timeout: int = DEFAULT_TIMEOUT):
        try:
            element = cls.active_driver.find_element(By.XPATH if locator.startswith(XPATH_PREFIXES) else By.CSS_SELECTOR,
                                              locator)
            WebDriverWait(cls.active_driver, timeout).until(EC.staleness_of(element))
        except (NoSuchElementException, AttributeError, TimeoutException):
            print(f'Element "{locator}" did not become stale within the timeout period')

    @classmethod
    def wait_until_invisible(cls, locator: str, timeout: int = DEFAULT_TIMEOUT):
        try:
            element = cls.active_driver.find_element(By.XPATH if locator.startswith(XPATH_PREFIXES) else By.CSS_SELECTOR,
                                              locator)
            WebDriverWait(cls.active_driver, timeout).until(EC.invisibility_of_element(element))
        except (NoSuchElementException, AttributeError, TimeoutException):
            print(f'Element "{locator}" did not become invisible within the timeout period')

    @classmethod
    def wait_until_text_present(cls, locator: str, text: str, timeout: int = DEFAULT_TIMEOUT,
                                ignore_timeout: bool = False):
        by = By.XPATH if locator.startswith(XPATH_PREFIXES) else By.CSS_SELECTOR
        try:
            WebDriverWait(cls.active_driver, timeout).until(EC.text_to_be_present_in_element((by, locator), text))
        except TimeoutException:
            if ignore_timeout:
                print(f'Text "{text}" not present in element "{locator}" within the timeout period')
            else:
                raise

    @classmethod
    def wait_until_value_present(cls, locator: str, value: str, timeout: int = DEFAULT_TIMEOUT,
                                 ignore_timeout: bool = False):
        by = By.XPATH if locator.startswith(XPATH_PREFIXES) else By.CSS_SELECTOR
        try:
            WebDriverWait(cls.active_driver, timeout).until(EC.text_to_be_present_in_element_value((by, locator), value))
        except TimeoutException:
            if ignore_timeout:
                print(f'Value "{value}" not present in element "{locator}" within the timeout period')
            else:
                raise


class BrowserActions(CustomWebDriverManager):

    @classmethod
    def accept_browser_alert(cls):
        cls.active_driver.switch_to.alert.accept()

    @classmethod
    def get_alert_message(cls):
        return cls.active_driver.switch_to.alert.text

    @classmethod
    def close_window(cls):
        cls.active_driver.close()

    @classmethod
    def dismiss_browser_alert(cls):
        cls.active_driver.switch_to.alert.dismiss()

    @classmethod
    def switch_to_frame(cls, locator: str):
        element = cls.active_driver.find_element(By.XPATH if locator.startswith(XPATH_PREFIXES) else By.CSS_SELECTOR, locator)
        cls.active_driver.switch_to.frame(element)

    @classmethod
    def switch_to_default_content(cls):
        cls.active_driver.switch_to.default_content()

    @classmethod
    def retrieve_all_cookies(cls):
        return cls.active_driver.get_cookies()

    @classmethod
    def retrieve_cookie(cls, name: str):
        cookie = cls.active_driver.get_cookie(name)
        if cookie:
            return cookie
        else:
            raise ValueError(f'Cookie named "{name}" not found')

    @classmethod
    def get_current_url(cls):
        return cls.active_driver.current_url

    @classmethod
    def get_all_window_handles(cls):
        return cls.active_driver.window_handles

    @classmethod
    def navigate_to_url(cls, url: str):
        cls.active_driver.get(url)

    @classmethod
    def is_alert_present(cls, timeout: int = DEFAULT_TIMEOUT):
        try:
            WebDriverWait(cls.active_driver, timeout).until(EC.alert_is_present())
            return True
        except TimeoutException:
            return False

    @classmethod
    def refresh_page(cls):
        cls.active_driver.refresh()

    @classmethod
    def set_window_size(cls, width: int, height: int):
        cls.active_driver.set_window_size(width, height)

    @classmethod
    def save_screenshot(cls, file_path: str, format: str = 'png'):
        if format not in IMAGE_FORMATS:
            raise ValueError(f"Unsupported image format. Supported formats: {IMAGE_FORMATS}")
        cls.active_driver.save_screenshot(f'{file_path}.{format}')

    @classmethod
    def switch_to_window_by_index(cls, index: int):
        try:
            cls.active_driver.switch_to.window(cls.active_driver.window_handles[index])
        except IndexError:
            raise ValueError(f'No window found at index {index}')

    @classmethod
    def navigate_back(cls):
        cls.active_driver.execute_script("window.history.go(-1)")

    @classmethod
    def navigate_forward(cls):
        cls.active_driver.execute_script("window.history.go(1)")
