"""
联系我们功能测试用例
测试联系表单提交功能
"""
import pytest
import allure
import time
import os
from tests.base_test import BaseTest
from utils.logger import log


@allure.epic("AutomationExercise网站测试")
@allure.feature("联系我们功能")
class TestContactUs(BaseTest):
    """联系我们功能测试类"""

    @allure.story("页面加载")
    @allure.title("验证联系我们页面加载")
    @allure.description("测试联系我们页面能够正确加载")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.contact
    def test_contact_us_page_loads(self):
        """测试联系我们页面加载"""
        with allure.step("导航到联系我们页面"):
            assert self.navigate_to_contact_us(), "联系我们页面加载失败"

        with allure.step("验证'Get In Touch'标题"):
            assert self.contact_us_page.verify_get_in_touch_title(), "'Get In Touch'标题不可见"

        with allure.step("验证表单字段"):
            assert self.contact_us_page.verify_form_fields_visible(), "联系表单字段不完整"

    @allure.story("表单提交")
    @allure.title("成功提交联系表单")
    @allure.description("测试填写并成功提交联系表单")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.contact
    def test_submit_contact_form_success(self):
        """测试成功提交联系表单"""
        contact_data = self.test_data.generate_contact_data()

        with allure.step("导航到联系我们页面"):
            assert self.navigate_to_contact_us(), "联系我们页面加载失败"

        with allure.step("填写联系表单"):
            self.contact_us_page.fill_contact_form(
                name=contact_data["name"],
                email=contact_data["email"],
                subject=contact_data["subject"],
                message=contact_data["message"]
            )

        with allure.step("提交表单"):
            self.contact_us_page.click_submit_button()

            # 处理可能的JavaScript警告框
            self.contact_us_page.handle_alert()
            time.sleep(3)

        with allure.step("验证成功消息"):
            success = self.contact_us_page.verify_success_message()
            self.assert_with_screenshot(
                success,
                "应该显示成功提交消息"
            )

    @allure.story("表单提交")
    @allure.title("使用完整方法提交表单")
    @allure.description("使用封装的提交方法测试表单提交")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.contact
    def test_submit_contact_form_complete(self):
        """测试使用完整方法提交表单"""
        contact_data = self.test_data.generate_contact_data()

        with allure.step("使用完整方法提交联系表单"):
            success = self.submit_contact_form(contact_data)
            self.assert_with_screenshot(
                success,
                "联系表单提交应该成功"
            )

    @allure.story("表单验证")
    @allure.title("空表单提交验证")
    @allure.description("测试提交空表单时的验证行为")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.contact
    def test_empty_form_submission(self):
        """测试空表单提交验证"""
        with allure.step("导航到联系我们页面"):
            assert self.navigate_to_contact_us(), "联系我们页面加载失败"

        with allure.step("直接提交空表单"):
            self.contact_us_page.click_submit_button()
            time.sleep(2)

        with allure.step("验证表单验证"):
            # 检查HTML5表单验证或仍在当前页面
            current_url = self.driver.current_url
            assert "/contact_us" in current_url, "空表单提交后应该仍在联系页面"

    @allure.story("表单验证")
    @allure.title("无效邮箱格式验证")
    @allure.description("测试输入无效邮箱格式的验证")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.contact
    def test_invalid_email_validation(self):
        """测试无效邮箱验证"""
        with allure.step("导航到联系我们页面"):
            assert self.navigate_to_contact_us(), "联系我们页面加载失败"

        with allure.step("填写包含无效邮箱的表单"):
            self.contact_us_page.fill_contact_form(
                name="Test User",
                email="invalid-email",  # 无效邮箱格式
                subject="Test Subject",
                message="Test Message"
            )

        with allure.step("提交表单"):
            self.contact_us_page.click_submit_button()
            time.sleep(2)

        with allure.step("验证邮箱验证"):
            # 验证HTML5邮箱验证或仍在当前页面
            current_url = self.driver.current_url
            assert "/contact_us" in current_url, "无效邮箱提交后应该仍在联系页面"

    @pytest.mark.parametrize("name,email,subject,message,should_succeed", [
        ("John Doe", "john@example.com", "Test Subject", "Test Message", True),
        ("", "test@example.com", "Subject", "Message", False),  # 空姓名
        ("Test User", "", "Subject", "Message", False),  # 空邮箱
        ("Test User", "invalid-email", "Subject", "Message", False),  # 无效邮箱
        ("Test User", "test@example.com", "", "Message", False),  # 空主题
        ("Test User", "test@example.com", "Subject", "", False),  # 空消息
        ("A" * 100, "test@example.com", "Subject", "Message", True),  # 长姓名
        ("Test User", "test@example.com", "A" * 200, "Message", True),  # 长主题
        ("Test User", "test@example.com", "Subject", "A" * 1000, True),  # 长消息
    ])
    @allure.story("表单验证")
    @allure.title("参数化表单验证测试")
    @allure.description("使用不同的表单数据进行验证测试")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.contact
    def test_form_validation_parametrized(self, name, email, subject, message, should_succeed):
        """参数化表单验证测试"""
        with allure.step(f"测试表单数据: name='{name[:20]}...', email='{email}'"):
            assert self.navigate_to_contact_us(), "联系我们页面加载失败"

            self.contact_us_page.fill_contact_form(name, email, subject, message)

            self.contact_us_page.click_submit_button()
            self.contact_us_page.handle_alert()
            time.sleep(3)

            if should_succeed:
                # 应该成功提交
                success = self.contact_us_page.verify_success_message()
                self.assert_with_screenshot(
                    success,
                    f"有效数据应该提交成功: name='{name[:20]}...'"
                )
            else:
                # 应该仍在联系页面（验证失败）
                current_url = self.driver.current_url
                self.assert_with_screenshot(
                    "/contact_us" in current_url,
                    f"无效数据应该提交失败: name='{name[:20]}...', email='{email}'"
                )

    @allure.story("文件上传")
    @allure.title("联系表单文件上传")
    @allure.description("测试联系表单的文件上传功能")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.contact
    def test_contact_form_file_upload(self):
        """测试文件上传功能"""
        # 创建临时测试文件
        test_file_path = "test_upload.txt"

        try:
            with allure.step("创建测试文件"):
                with open(test_file_path, 'w') as f:
                    f.write("This is a test file for contact form upload.")

                # 获取绝对路径
                absolute_path = os.path.abspath(test_file_path)

            with allure.step("导航到联系我们页面"):
                assert self.navigate_to_contact_us(), "联系我们页面加载失败"

            contact_data = self.test_data.generate_contact_data()

            with allure.step("提交包含文件的表单"):
                self.contact_us_page.submit_contact_form(contact_data, absolute_path)
                time.sleep(3)

            with allure.step("验证提交成功"):
                success = self.contact_us_page.verify_success_message()
                self.assert_with_screenshot(
                    success,
                    "包含文件的表单应该提交成功"
                )

        finally:
            # 清理测试文件
            if os.path.exists(test_file_path):
                os.remove(test_file_path)

    @allure.story("导航")
    @allure.title("返回首页功能")
    @allure.description("测试提交成功后返回首页功能")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.contact
    @pytest.mark.navigation
    def test_return_to_home(self):
        """测试返回首页功能"""
        contact_data = self.test_data.generate_contact_data()

        with allure.step("提交联系表单"):
            assert self.submit_contact_form(contact_data), "联系表单提交失败"

        with allure.step("点击返回首页按钮"):
            # 注意：需要确认网站是否有返回首页按钮
            if self.contact_us_page.verify_element_visible(self.contact_us_page.HOME_BUTTON):
                self.contact_us_page.click_home_button()
                time.sleep(2)

                current_url = self.driver.current_url
                self.assert_with_screenshot(
                    current_url == self.config.base_url or current_url == f"{self.config.base_url}/",
                    f"应该返回首页，当前URL: {current_url}"
                )
            else:
                log.step("网站没有返回首页按钮，跳过此测试步骤")

    @allure.story("用户体验")
    @allure.title("表单字段清空功能")
    @allure.description("测试表单字段的清空功能")
    @allure.severity(allure.severity_level.LOW)
    @pytest.mark.contact
    def test_form_clear_functionality(self):
        """测试表单清空功能"""
        with allure.step("导航到联系我们页面"):
            assert self.navigate_to_contact_us(), "联系我们页面加载失败"

        with allure.step("填写表单"):
            self.contact_us_page.fill_contact_form(
                name="Test User",
                email="test@example.com",
                subject="Test Subject",
                message="Test Message"
            )

        with allure.step("验证表单已填写"):
            form_values = self.contact_us_page.get_form_field_values()
            assert form_values["name"] == "Test User", "姓名字段应该已填写"
            assert form_values["email"] == "test@example.com", "邮箱字段应该已填写"

        with allure.step("清空表单"):
            self.contact_us_page.clear_form()

        with allure.step("验证表单已清空"):
            form_values = self.contact_us_page.get_form_field_values()
            assert form_values["name"] == "", "姓名字段应该已清空"
            assert form_values["email"] == "", "邮箱字段应该已清空"

    @allure.story("性能测试")
    @allure.title("表单提交响应时间")
    @allure.description("测试联系表单提交的响应时间")
    @allure.severity(allure.severity_level.LOW)
    @pytest.mark.slow
    def test_form_submission_response_time(self):
        """测试表单提交响应时间"""
        contact_data = self.test_data.generate_contact_data()

        with allure.step("导航到联系我们页面"):
            assert self.navigate_to_contact_us(), "联系我们页面加载失败"

        with allure.step("测量表单提交响应时间"):
            start_time = time.time()

            self.contact_us_page.submit_contact_form(contact_data)
            self.contact_us_page.verify_success_message()

            end_time = time.time()
            response_time = end_time - start_time

            log.performance("Contact form submission time", response_time, "seconds")

            # 验证响应时间在合理范围内（15秒）
            self.assert_with_screenshot(
                response_time < 15,
                f"表单提交响应时间过长: {response_time:.2f}秒"
            )

    @allure.story("安全测试")
    @allure.title("XSS攻击防护测试")
    @allure.description("测试联系表单是否防护XSS攻击")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_xss_protection(self):
        """测试XSS攻击防护"""
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "';alert('XSS');//"
        ]

        for payload in xss_payloads:
            with allure.step(f"测试XSS payload: {payload}"):
                assert self.navigate_to_contact_us(), "联系我们页面加载失败"

                self.contact_us_page.fill_contact_form(
                    name=payload,
                    email="test@example.com",
                    subject=payload,
                    message=payload
                )

                self.contact_us_page.click_submit_button()
                self.contact_us_page.handle_alert()
                time.sleep(3)

                # 验证页面没有执行恶意脚本
                page_source = self.driver.page_source
                self.assert_with_screenshot(
                    payload not in page_source or "alert" not in page_source,
                    f"XSS payload应该被过滤: {payload}"
                )

    @allure.story("错误处理")
    @allure.title("网络错误处理")
    @allure.description("测试联系表单在网络错误情况下的表现")
    @allure.severity(allure.severity_level.LOW)
    @pytest.mark.regression
    def test_network_error_handling(self):
        """测试网络错误处理"""
        with allure.step("导航到联系我们页面"):
            assert self.navigate_to_contact_us(), "联系我们页面加载失败"

        with allure.step("填写表单"):
            contact_data = self.test_data.generate_contact_data()
            self.contact_us_page.fill_contact_form(
                name=contact_data["name"],
                email=contact_data["email"],
                subject=contact_data["subject"],
                message=contact_data["message"]
            )

        with allure.step("模拟网络中断后恢复"):
            # 刷新页面来模拟网络问题恢复
            self.contact_us_page.refresh_page()
            time.sleep(3)

        with allure.step("验证页面恢复"):
            assert self.contact_us_page.verify_page_loaded(), "页面应该能够恢复正常"
            assert self.contact_us_page.verify_form_fields_visible(), "表单字段应该重新可见"

    @allure.story("可访问性")
    @allure.title("表单可访问性测试")
    @allure.description("测试联系表单的基本可访问性")
    @allure.severity(allure.severity_level.LOW)
    @pytest.mark.contact
    def test_form_accessibility(self):
        """测试表单可访问性"""
        with allure.step("导航到联系我们页面"):
            assert self.navigate_to_contact_us(), "联系我们页面加载失败"

        with allure.step("验证表单标签"):
            # 检查表单字段是否有适当的标签或占位符
            name_field = self.contact_us_page.wait_for_element_visible(
                self.contact_us_page.NAME_INPUT
            )

            if name_field:
                # 检查是否有placeholder或相关的label
                placeholder = name_field.get_attribute("placeholder")
                data_qa = name_field.get_attribute("data-qa")

                self.assert_with_screenshot(
                    placeholder or data_qa,
                    "表单字段应该有适当的标识符以提供可访问性"
                )

        with allure.step("验证键盘导航"):
            # 简单的Tab键导航测试
            name_field = self.contact_us_page.wait_for_element_visible(
                self.contact_us_page.NAME_INPUT
            )

            if name_field:
                name_field.click()
                # 验证字段能够获得焦点
                active_element = self.driver.switch_to.active_element
                assert active_element == name_field, "表单字段应该能够获得键盘焦点"
