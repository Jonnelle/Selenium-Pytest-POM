"""
WebDriver工具类
提供常用的WebDriver操作方法
"""
import time
from typing import List, Optional, Union
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException
)
from utils.logger import log


class WebDriverUtils:
    """WebDriver工具类"""

    def __init__(self, driver, timeout: int = 15):
        """
        初始化WebDriver工具类

        Args:
            driver: WebDriver实例
            timeout: 默认等待时间
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.timeout = timeout

    def find_element(self, locator: tuple, timeout: int = None) -> Optional[WebElement]:
        """
        查找单个元素

        Args:
            locator: 定位器元组 (By.ID, "element_id")
            timeout: 等待超时时间

        Returns:
            WebElement或None
        """
        try:
            wait_time = timeout or self.timeout
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            log.page_action("Found element", f"{locator[0]}='{locator[1]}'")
            return element
        except TimeoutException:
            log.warning(f"Element not found: {locator}")
            return None

    def find_elements(self, locator: tuple, timeout: int = None) -> List[WebElement]:
        """
        查找多个元素

        Args:
            locator: 定位器元组
            timeout: 等待超时时间

        Returns:
            WebElement列表
        """
        try:
            wait_time = timeout or self.timeout
            elements = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_all_elements_located(locator)
            )
            log.page_action("Found elements", f"{locator[0]}='{locator[1]}' (count: {len(elements)})")
            return elements
        except TimeoutException:
            log.warning(f"Elements not found: {locator}")
            return []

    def wait_for_element_visible(self, locator: tuple, timeout: int = None) -> Optional[WebElement]:
        """
        等待元素可见

        Args:
            locator: 定位器元组
            timeout: 等待超时时间

        Returns:
            WebElement或None
        """
        try:
            wait_time = timeout or self.timeout
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            log.page_action("Element visible", f"{locator[0]}='{locator[1]}'")
            return element
        except TimeoutException:
            log.warning(f"Element not visible: {locator}")
            return None

    def wait_for_element_clickable(self, locator: tuple, timeout: int = None) -> Optional[WebElement]:
        """
        等待元素可点击

        Args:
            locator: 定位器元组
            timeout: 等待超时时间

        Returns:
            WebElement或None
        """
        try:
            wait_time = timeout or self.timeout
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            log.page_action("Element clickable", f"{locator[0]}='{locator[1]}'")
            return element
        except TimeoutException:
            log.warning(f"Element not clickable: {locator}")
            return None

    def click_element(self, locator: tuple, timeout: int = None) -> bool:
        """
        点击元素

        Args:
            locator: 定位器元组
            timeout: 等待超时时间

        Returns:
            是否点击成功
        """
        try:
            element = self.wait_for_element_clickable(locator, timeout)
            if element:
                element.click()
                log.page_action("Clicked element", f"{locator[0]}='{locator[1]}'")
                return True
            return False
        except Exception as e:
            log.error(f"Click element failed: {str(e)}")
            return False

    def send_keys(self, locator: tuple, text: str, clear: bool = True, timeout: int = None) -> bool:
        """
        向元素输入文本

        Args:
            locator: 定位器元组
            text: 输入文本
            clear: 是否先清空
            timeout: 等待超时时间

        Returns:
            是否输入成功
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            if element:
                if clear:
                    element.clear()
                element.send_keys(text)
                log.page_action("Sent keys", f"{locator[0]}='{locator[1]}' text='{text}'")
                return True
            return False
        except Exception as e:
            log.error(f"Send keys failed: {str(e)}")
            return False

    def get_text(self, locator: tuple, timeout: int = None) -> str:
        """
        获取元素文本

        Args:
            locator: 定位器元组
            timeout: 等待超时时间

        Returns:
            元素文本
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            if element:
                text = element.text
                log.page_action("Got text", f"{locator[0]}='{locator[1]}' text='{text}'")
                return text
            return ""
        except Exception as e:
            log.error(f"Get text failed: {str(e)}")
            return ""

    def get_attribute(self, locator: tuple, attribute: str, timeout: int = None) -> str:
        """
        获取元素属性

        Args:
            locator: 定位器元组
            attribute: 属性名
            timeout: 等待超时时间

        Returns:
            属性值
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            if element:
                value = element.get_attribute(attribute)
                log.page_action("Got attribute", f"{locator[0]}='{locator[1]}' {attribute}='{value}'")
                return value or ""
            return ""
        except Exception as e:
            log.error(f"Get attribute failed: {str(e)}")
            return ""

    def is_element_present(self, locator: tuple) -> bool:
        """
        检查元素是否存在

        Args:
            locator: 定位器元组

        Returns:
            是否存在
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def is_element_visible(self, locator: tuple, timeout: int = 3) -> bool:
        """
        检查元素是否可见

        Args:
            locator: 定位器元组
            timeout: 等待超时时间

        Returns:
            是否可见
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def select_dropdown_by_text(self, locator: tuple, text: str, timeout: int = None) -> bool:
        """
        通过文本选择下拉框选项

        Args:
            locator: 定位器元组
            text: 选项文本
            timeout: 等待超时时间

        Returns:
            是否选择成功
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            if element:
                select = Select(element)
                select.select_by_visible_text(text)
                log.page_action("Selected dropdown", f"{locator[0]}='{locator[1]}' text='{text}'")
                return True
            return False
        except Exception as e:
            log.error(f"Select dropdown failed: {str(e)}")
            return False

    def select_dropdown_by_value(self, locator: tuple, value: str, timeout: int = None) -> bool:
        """
        通过值选择下拉框选项

        Args:
            locator: 定位器元组
            value: 选项值
            timeout: 等待超时时间

        Returns:
            是否选择成功
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            if element:
                select = Select(element)
                select.select_by_value(value)
                log.page_action("Selected dropdown", f"{locator[0]}='{locator[1]}' value='{value}'")
                return True
            return False
        except Exception as e:
            log.error(f"Select dropdown failed: {str(e)}")
            return False

    def hover_element(self, locator: tuple, timeout: int = None) -> bool:
        """
        鼠标悬停到元素

        Args:
            locator: 定位器元组
            timeout: 等待超时时间

        Returns:
            是否悬停成功
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            if element:
                ActionChains(self.driver).move_to_element(element).perform()
                log.page_action("Hovered element", f"{locator[0]}='{locator[1]}'")
                return True
            return False
        except Exception as e:
            log.error(f"Hover element failed: {str(e)}")
            return False

    def double_click_element(self, locator: tuple, timeout: int = None) -> bool:
        """
        双击元素

        Args:
            locator: 定位器元组
            timeout: 等待超时时间

        Returns:
            是否双击成功
        """
        try:
            element = self.wait_for_element_clickable(locator, timeout)
            if element:
                ActionChains(self.driver).double_click(element).perform()
                log.page_action("Double clicked element", f"{locator[0]}='{locator[1]}'")
                return True
            return False
        except Exception as e:
            log.error(f"Double click element failed: {str(e)}")
            return False

    def scroll_to_element(self, locator: tuple, timeout: int = None) -> bool:
        """
        滚动到元素

        Args:
            locator: 定位器元组
            timeout: 等待超时时间

        Returns:
            是否滚动成功
        """
        try:
            element = self.find_element(locator, timeout)
            if element:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                log.page_action("Scrolled to element", f"{locator[0]}='{locator[1]}'")
                return True
            return False
        except Exception as e:
            log.error(f"Scroll to element failed: {str(e)}")
            return False

    def wait_for_page_load(self, timeout: int = None):
        """
        等待页面加载完成

        Args:
            timeout: 等待超时时间
        """
        wait_time = timeout or self.timeout
        WebDriverWait(self.driver, wait_time).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        log.page_action("Page loaded")

    def switch_to_frame(self, locator: tuple, timeout: int = None) -> bool:
        """
        切换到iframe

        Args:
            locator: 定位器元组
            timeout: 等待超时时间

        Returns:
            是否切换成功
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            if element:
                self.driver.switch_to.frame(element)
                log.page_action("Switched to frame", f"{locator[0]}='{locator[1]}'")
                return True
            return False
        except Exception as e:
            log.error(f"Switch to frame failed: {str(e)}")
            return False

    def switch_to_default_content(self):
        """切换回默认内容"""
        self.driver.switch_to.default_content()
        log.page_action("Switched to default content")

    def get_current_url(self) -> str:
        """获取当前URL"""
        url = self.driver.current_url
        log.page_action("Got current URL", url)
        return url

    def get_page_title(self) -> str:
        """获取页面标题"""
        title = self.driver.title
        log.page_action("Got page title", title)
        return title

    def refresh_page(self):
        """刷新页面"""
        self.driver.refresh()
        log.page_action("Refreshed page")

    def navigate_back(self):
        """后退"""
        self.driver.back()
        log.page_action("Navigated back")

    def navigate_forward(self):
        """前进"""
        self.driver.forward()
        log.page_action("Navigated forward")

    def execute_javascript(self, script: str, *args):
        """
        执行JavaScript代码

        Args:
            script: JavaScript代码
            *args: 参数

        Returns:
            执行结果
        """
        result = self.driver.execute_script(script, *args)
        log.page_action("Executed JavaScript", script[:50] + "..." if len(script) > 50 else script)
        return result

    def take_screenshot(self, file_path: str) -> bool:
        """
        截图

        Args:
            file_path: 保存路径

        Returns:
            是否截图成功
        """
        try:
            self.driver.save_screenshot(file_path)
            log.page_action("Took screenshot", file_path)
            return True
        except Exception as e:
            log.error(f"Take screenshot failed: {str(e)}")
            return False
