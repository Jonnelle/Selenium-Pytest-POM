"""
页面对象模型基类
所有页面类的基础类
"""
import time
from typing import List, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from utils.webdriver_utils import WebDriverUtils
from utils.config_manager import ConfigManager
from utils.logger import log


class BasePage:
    """页面对象模型基类"""

    def __init__(self, driver):
        """
        初始化基础页面

        Args:
            driver: WebDriver实例
        """
        self.driver = driver
        self.config = ConfigManager()
        self.utils = WebDriverUtils(driver, self.config.explicit_wait)
        self.base_url = self.config.base_url

    def open_page(self, url: str = None):
        """
        打开页面

        Args:
            url: 页面URL，默认使用基础URL
        """
        page_url = url or self.base_url
        self.driver.get(page_url)
        self.wait_for_page_load()
        log.page_action("Opened page", page_url)

    def wait_for_page_load(self, timeout: int = None):
        """等待页面加载完成"""
        self.utils.wait_for_page_load(timeout)

    def get_current_url(self) -> str:
        """获取当前URL"""
        return self.utils.get_current_url()

    def get_page_title(self) -> str:
        """获取页面标题"""
        return self.utils.get_page_title()

    def refresh_page(self):
        """刷新页面"""
        self.utils.refresh_page()

    def navigate_back(self):
        """后退"""
        self.utils.navigate_back()

    def navigate_forward(self):
        """前进"""
        self.utils.navigate_forward()

    def scroll_to_top(self):
        """滚动到页面顶部"""
        self.utils.execute_javascript("window.scrollTo(0, 0);")

    def scroll_to_bottom(self):
        """滚动到页面底部"""
        self.utils.execute_javascript("window.scrollTo(0, document.body.scrollHeight);")

    def take_screenshot(self, name: str = None) -> str:
        """
        截图

        Args:
            name: 截图文件名

        Returns:
            截图文件路径
        """
        if not name:
            name = f"screenshot_{int(time.time())}"

        file_path = f"reports/screenshots/{name}.png"
        self.utils.take_screenshot(file_path)
        return file_path

    def wait_for_element(self, locator: tuple, timeout: int = None) -> Optional[WebElement]:
        """等待元素出现"""
        return self.utils.find_element(locator, timeout)

    def wait_for_element_visible(self, locator: tuple, timeout: int = None) -> Optional[WebElement]:
        """等待元素可见"""
        return self.utils.wait_for_element_visible(locator, timeout)

    def wait_for_element_clickable(self, locator: tuple, timeout: int = None) -> Optional[WebElement]:
        """等待元素可点击"""
        return self.utils.wait_for_element_clickable(locator, timeout)

    def click_element(self, locator: tuple, timeout: int = None) -> bool:
        """点击元素"""
        return self.utils.click_element(locator, timeout)

    def send_keys(self, locator: tuple, text: str, clear: bool = True, timeout: int = None) -> bool:
        """输入文本"""
        return self.utils.send_keys(locator, text, clear, timeout)

    def get_text(self, locator: tuple, timeout: int = None) -> str:
        """获取元素文本"""
        return self.utils.get_text(locator, timeout)

    def get_attribute(self, locator: tuple, attribute: str, timeout: int = None) -> str:
        """获取元素属性"""
        return self.utils.get_attribute(locator, attribute, timeout)

    def is_element_present(self, locator: tuple) -> bool:
        """检查元素是否存在"""
        return self.utils.is_element_present(locator)

    def is_element_visible(self, locator: tuple, timeout: int = 3) -> bool:
        """检查元素是否可见"""
        return self.utils.is_element_visible(locator, timeout)

    def hover_element(self, locator: tuple, timeout: int = None) -> bool:
        """鼠标悬停"""
        return self.utils.hover_element(locator, timeout)

    def scroll_to_element(self, locator: tuple, timeout: int = None) -> bool:
        """滚动到元素"""
        return self.utils.scroll_to_element(locator, timeout)

    def select_dropdown_by_text(self, locator: tuple, text: str, timeout: int = None) -> bool:
        """通过文本选择下拉框"""
        return self.utils.select_dropdown_by_text(locator, text, timeout)

    def select_dropdown_by_value(self, locator: tuple, value: str, timeout: int = None) -> bool:
        """通过值选择下拉框"""
        return self.utils.select_dropdown_by_value(locator, value, timeout)

    def get_elements(self, locator: tuple, timeout: int = None) -> List[WebElement]:
        """获取元素列表"""
        return self.utils.find_elements(locator, timeout)

    def execute_javascript(self, script: str, *args):
        """执行JavaScript"""
        return self.utils.execute_javascript(script, *args)

    def verify_page_title(self, expected_title: str) -> bool:
        """
        验证页面标题

        Args:
            expected_title: 期望的标题

        Returns:
            是否匹配
        """
        actual_title = self.get_page_title()
        is_match = expected_title in actual_title
        log.assertion("Page title verification", expected_title, actual_title)
        return is_match

    def verify_current_url(self, expected_url: str) -> bool:
        """
        验证当前URL

        Args:
            expected_url: 期望的URL

        Returns:
            是否匹配
        """
        actual_url = self.get_current_url()
        is_match = expected_url in actual_url
        log.assertion("Current URL verification", expected_url, actual_url)
        return is_match

    def verify_element_text(self, locator: tuple, expected_text: str, timeout: int = None) -> bool:
        """
        验证元素文本

        Args:
            locator: 定位器
            expected_text: 期望的文本
            timeout: 等待超时时间

        Returns:
            是否匹配
        """
        actual_text = self.get_text(locator, timeout)
        is_match = expected_text in actual_text
        log.assertion("Element text verification", expected_text, actual_text)
        return is_match

    def verify_element_visible(self, locator: tuple, timeout: int = 3) -> bool:
        """
        验证元素可见

        Args:
            locator: 定位器
            timeout: 等待超时时间

        Returns:
            是否可见
        """
        is_visible = self.is_element_visible(locator, timeout)
        log.assertion("Element visibility", "visible", "visible" if is_visible else "not visible")
        return is_visible

    def verify_element_not_visible(self, locator: tuple, timeout: int = 3) -> bool:
        """
        验证元素不可见

        Args:
            locator: 定位器
            timeout: 等待超时时间

        Returns:
            是否不可见
        """
        is_visible = self.is_element_visible(locator, timeout)
        log.assertion("Element invisibility", "not visible", "not visible" if not is_visible else "visible")
        return not is_visible

    def wait_and_click(self, locator: tuple, timeout: int = None) -> bool:
        """
        等待并点击元素

        Args:
            locator: 定位器
            timeout: 等待超时时间

        Returns:
            是否点击成功
        """
        element = self.wait_for_element_clickable(locator, timeout)
        if element:
            return self.click_element(locator, timeout)
        return False

    def clear_and_send_keys(self, locator: tuple, text: str, timeout: int = None) -> bool:
        """
        清空并输入文本

        Args:
            locator: 定位器
            text: 输入文本
            timeout: 等待超时时间

        Returns:
            是否输入成功
        """
        return self.send_keys(locator, text, clear=True, timeout=timeout)

    def get_page_source(self) -> str:
        """获取页面源码"""
        return self.driver.page_source
