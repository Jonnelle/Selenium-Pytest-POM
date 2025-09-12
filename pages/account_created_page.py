"""
账户创建成功页面对象
AutomationExercise网站账户创建成功确认页面
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import log


class AccountCreatedPage(BasePage):
    """账户创建成功页面对象"""

    # 页面元素
    PAGE_TITLE = (By.XPATH, "//h2[@data-qa='account-created']")
    SUCCESS_MESSAGE = (By.XPATH, "//h2[@data-qa='account-created']/b[text()='Account Created!']")
    CONTINUE_BUTTON = (By.XPATH, "//a[@data-qa='continue-button']")
    CONGRATULATIONS_MESSAGE = (By.XPATH, "//p[contains(text(), 'Congratulations')]")

    def __init__(self, driver):
        """初始化账户创建成功页面"""
        super().__init__(driver)
        self.page_url = f"{self.base_url}/account_created"

    def verify_page_loaded(self) -> bool:
        """验证页面加载成功"""
        log.step("Verifying account created page loaded")
        return self.verify_element_visible(self.SUCCESS_MESSAGE)

    def verify_success_message(self) -> bool:
        """验证成功消息"""
        log.step("Verifying account creation success message")
        return self.verify_element_visible(self.SUCCESS_MESSAGE)

    def verify_congratulations_message(self) -> bool:
        """验证祝贺消息"""
        log.step("Verifying congratulations message")
        return self.verify_element_visible(self.CONGRATULATIONS_MESSAGE)

    def click_continue_button(self):
        """点击继续按钮"""
        log.step("Clicking continue button")
        self.click_element(self.CONTINUE_BUTTON)
        return self

    def get_success_message_text(self) -> str:
        """获取成功消息文本"""
        log.step("Getting success message text")
        return self.get_text(self.SUCCESS_MESSAGE)

    def verify_continue_button_present(self) -> bool:
        """验证继续按钮存在"""
        log.step("Verifying continue button present")
        return self.verify_element_visible(self.CONTINUE_BUTTON)
