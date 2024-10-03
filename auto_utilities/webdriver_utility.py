from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class CustomWebDriverManager:
    """Handles the configuration and initialization of WebDriver for different browsers, starting with Chrome."""

    available_browsers = {'chrome', 'firefox'}
    driver_options = None
    capabilities = None
    active_driver = None

    @classmethod
    def configure_driver(cls, browser_type: str = 'chrome', download_path: str = None):
        """
        Configures browser options and capabilities based on the browser type.
        """
        if browser_type not in cls.available_browsers:
            raise ValueError(f"Unsupported browser: {browser_type}. Available options are: {cls.available_browsers}")

        if browser_type == 'chrome':
            cls.driver_options = webdriver.ChromeOptions()
            cls.capabilities = {'browserName': 'chrome'}
            cls.driver_options.capabilities.update(cls.capabilities)
            cls.driver_options.add_argument("--disable-popup-blocking")
            cls.driver_options.add_argument("--disable-infobars")
            cls.driver_options.add_experimental_option('excludeSwitches', ['enable-automation'])

            if download_path:
                prefs = {"download.default_directory": download_path}
                cls.driver_options.add_experimental_option('prefs', prefs)
        else:
            raise ValueError("Configuration for this browser is not yet implemented.")

    @classmethod
    def launch_driver(cls, browser_type: str = 'chrome', remote_host: str = None, download_path: str = None):
        """
        Launches the WebDriver for either a remote or local instance.
        """
        cls.configure_driver(browser_type, download_path)

        try:
            if remote_host:
                cls.active_driver = webdriver.Remote(
                    command_executor=f'http://{remote_host}/wd/hub',
                    options=cls.driver_options
                )
            else:
                cls.active_driver = webdriver.Chrome(service=Service('/Users/dvpx/qa-auto_utilities/chromedriver'),
                                                     options=cls.driver_options)
        except Exception as e:
            raise Exception(f"Failed to initialize WebDriver for {browser_type}: {e}")

    @classmethod
    def get_active_driver(cls):
        """
        Provides the current WebDriver instance.
        """
        if cls.active_driver:
            return cls.active_driver
        raise Exception("No active WebDriver instance. Please initialize the driver first.")

    @classmethod
    def terminate_driver(cls):
        """
        Shuts down the active WebDriver instance and clears the driver reference.
        """
        if cls.active_driver:
            cls.active_driver.quit()
            cls.active_driver = None

    @classmethod
    def update_download_directory(cls, new_download_path: str):
        """
        Updates the download directory for the active browser session.
        """
        if cls.active_driver and cls.driver_options:
            prefs = {"download.default_directory": new_download_path}
            cls.driver_options.add_experimental_option('prefs', prefs)
        else:
            raise Exception("No active driver to update download preferences.")

# Example usage:
# CustomWebDriverManager.launch_driver(browser_type='chrome', download_path='/new/download/path')
# driver = CustomWebDriverManager.get_active_driver()
# CustomWebDriverManager.terminate_driver()
