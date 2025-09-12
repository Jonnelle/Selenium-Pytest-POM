"""
用户认证测试用例
测试用户注册、登录、登出功能
"""
import pytest
import allure
import time
from tests.base_test import BaseTest
from utils.logger import log


@allure.epic("AutomationExercise网站测试")
@allure.feature("用户认证功能")
class TestUserAuthentication(BaseTest):
    """用户认证测试类"""

    @allure.story("用户注册")
    @allure.title("新用户注册成功")
    @allure.description("测试新用户完整的注册流程")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_user_registration_success(self):
        """测试用户注册成功"""
        # 生成测试用户数据
        user_data = self.test_data.generate_test_user()

        with allure.step("导航到登录页面"):
            assert self.navigate_to_login(), "登录页面加载失败"

        with allure.step("验证注册表单可见"):
            assert self.login_page.verify_signup_section_visible(), "注册区域不可见"

        with allure.step("填写注册信息"):
            self.login_page.signup_new_user(
                name=f"{user_data['first_name']} {user_data['last_name']}",
                email=user_data['email']
            )

        with allure.step("验证注册详情页面加载"):
            assert self.verify_page_loaded(self.signup_page, "注册详情页面")

        with allure.step("验证姓名和邮箱预填充"):
            expected_name = f"{user_data['first_name']} {user_data['last_name']}"
            assert self.signup_page.verify_name_and_email_prefilled(
                expected_name, user_data['email']
            ), "姓名和邮箱预填充不正确"

        with allure.step("完成注册信息"):
            self.signup_page.complete_registration(user_data)

        with allure.step("验证账户创建成功"):
            assert self.verify_page_loaded(self.account_created_page, "账户创建成功页面")
            assert self.account_created_page.verify_success_message(), "账户创建成功消息不可见"

        with allure.step("点击继续按钮"):
            self.account_created_page.click_continue_button()
            time.sleep(2)

        with allure.step("验证登录成功"):
            current_url = self.driver.current_url
            # 应该跳转到首页或其他已登录页面
            self.assert_with_screenshot(
                "/login" not in current_url,
                f"注册完成后应该自动登录，但仍在登录页面: {current_url}"
            )

    @allure.story("用户注册")
    @allure.title("已存在邮箱注册失败")
    @allure.description("测试使用已存在的邮箱注册应该失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.regression
    def test_registration_with_existing_email(self):
        """测试已存在邮箱注册失败"""
        with allure.step("导航到登录页面"):
            assert self.navigate_to_login(), "登录页面加载失败"

        with allure.step("尝试使用已存在的邮箱注册"):
            # 使用已知存在的邮箱
            existing_email = "existing@example.com"
            self.login_page.signup_new_user("Test User", existing_email)

        with allure.step("验证错误消息"):
            time.sleep(2)
            error_visible = self.login_page.verify_email_already_exists_error()
            self.assert_with_screenshot(
                error_visible,
                "应该显示邮箱已存在的错误消息"
            )

    @allure.story("用户注册")
    @allure.title("注册表单验证")
    @allure.description("测试注册表单的字段验证")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    def test_registration_form_validation(self):
        """测试注册表单验证"""
        with allure.step("导航到登录页面"):
            assert self.navigate_to_login(), "登录页面加载失败"

        with allure.step("验证注册表单字段"):
            assert self.login_page.verify_signup_form_fields(), "注册表单字段不完整"

        with allure.step("测试空表单提交"):
            self.login_page.signup_new_user("", "")
            time.sleep(1)

            # 验证仍在登录页面（表单验证阻止了提交）
            current_url = self.driver.current_url
            assert "/login" in current_url, "空表单不应该能提交成功"

        with allure.step("测试无效邮箱格式"):
            self.login_page.clear_signup_form()
            self.login_page.signup_new_user("Test User", "invalid-email")
            time.sleep(1)

            # 验证仍在登录页面
            current_url = self.driver.current_url
            assert "/login" in current_url, "无效邮箱格式不应该能提交成功"

    @allure.story("用户登录")
    @allure.title("有效用户登录成功")
    @allure.description("测试有效用户能够成功登录")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_valid_user_login(self):
        """测试有效用户登录"""
        user_data = self.test_data.get_user_data()
        valid_user = user_data.get("valid_user", {})

        with allure.step("导航到登录页面"):
            assert self.navigate_to_login(), "登录页面加载失败"

        with allure.step("验证登录表单可见"):
            assert self.login_page.verify_login_section_visible(), "登录区域不可见"

        with allure.step("输入登录凭据"):
            email = valid_user.get("email", "testuser@example.com")
            password = valid_user.get("password", "Test123456")
            self.login_page.login_user(email, password)

        with allure.step("验证登录成功"):
            time.sleep(3)
            current_url = self.driver.current_url
            self.assert_with_screenshot(
                "/login" not in current_url,
                f"登录应该成功并跳转，但仍在登录页面: {current_url}"
            )

    @allure.story("用户登录")
    @allure.title("无效用户登录失败")
    @allure.description("测试无效凭据登录应该失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.regression
    def test_invalid_user_login(self):
        """测试无效用户登录失败"""
        with allure.step("导航到登录页面"):
            assert self.navigate_to_login(), "登录页面加载失败"

        with allure.step("尝试使用无效凭据登录"):
            self.login_page.login_user("invalid@email.com", "wrongpassword")

        with allure.step("验证错误消息"):
            time.sleep(2)
            error_visible = self.login_page.verify_incorrect_login_error()
            self.assert_with_screenshot(
                error_visible,
                "应该显示登录错误消息"
            )

        with allure.step("验证仍在登录页面"):
            current_url = self.driver.current_url
            assert "/login" in current_url, "无效登录后应该仍在登录页面"

    @allure.story("用户登录")
    @allure.title("空凭据登录失败")
    @allure.description("测试空用户名密码登录应该失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    def test_empty_credentials_login(self):
        """测试空凭据登录失败"""
        with allure.step("导航到登录页面"):
            assert self.navigate_to_login(), "登录页面加载失败"

        with allure.step("尝试使用空凭据登录"):
            self.login_page.login_user("", "")

        with allure.step("验证仍在登录页面"):
            time.sleep(2)
            current_url = self.driver.current_url
            assert "/login" in current_url, "空凭据登录不应该成功"

    @allure.story("用户登录")
    @allure.title("登录表单验证")
    @allure.description("测试登录表单字段验证")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    def test_login_form_validation(self):
        """测试登录表单验证"""
        with allure.step("导航到登录页面"):
            assert self.navigate_to_login(), "登录页面加载失败"

        with allure.step("验证登录表单字段"):
            assert self.login_page.verify_login_form_fields(), "登录表单字段不完整"

        with allure.step("验证按钮状态"):
            assert self.login_page.is_login_button_enabled(), "登录按钮应该可用"
            assert self.login_page.is_signup_button_enabled(), "注册按钮应该可用"

        with allure.step("测试表单字段值获取"):
            self.login_page.fill_login_form("test@example.com", "testpass")

            email_value = self.login_page.get_login_email_value()
            assert email_value == "test@example.com", f"邮箱字段值不正确: {email_value}"

    @pytest.mark.parametrize("email,password,expected", [
        ("testuser@example.com", "Test123456", "success"),
        ("invalid@email.com", "wrongpass", "failure"),
        ("", "", "failure"),
        ("user@test.com", "invalidpass", "failure")
    ])
    @allure.story("用户登录")
    @allure.title("参数化登录测试")
    @allure.description("使用不同的登录凭据进行参数化测试")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    def test_login_parametrized(self, email, password, expected):
        """参数化登录测试"""
        with allure.step(f"测试登录: {email}"):
            assert self.navigate_to_login(), "登录页面加载失败"

            self.login_page.login_user(email, password)
            time.sleep(3)

            current_url = self.driver.current_url

            if expected == "success":
                self.assert_with_screenshot(
                    "/login" not in current_url,
                    f"有效凭据登录应该成功，当前URL: {current_url}"
                )
            else:
                self.assert_with_screenshot(
                    "/login" in current_url,
                    f"无效凭据登录应该失败，当前URL: {current_url}"
                )

    @allure.story("完整流程")
    @allure.title("注册后立即登录")
    @allure.description("测试注册新用户后立即登录的完整流程")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_registration_and_login_flow(self):
        """测试注册和登录完整流程"""
        user_data = self.test_data.generate_test_user()

        with allure.step("执行用户注册"):
            assert self.register_new_user(user_data), "用户注册失败"

        with allure.step("注册完成后继续"):
            self.account_created_page.click_continue_button()
            time.sleep(2)

        with allure.step("验证自动登录"):
            current_url = self.driver.current_url
            self.assert_with_screenshot(
                "/login" not in current_url,
                f"注册完成后应该自动登录，当前URL: {current_url}"
            )

        # 注意：实际网站可能有登出功能，这里简化处理
        with allure.step("模拟登出（清除会话）"):
            # 可以通过删除cookies或访问登出URL来模拟登出
            self.driver.delete_all_cookies()
            self.navigate_to_login()

        with allure.step("使用注册的凭据重新登录"):
            email = user_data['email']
            password = user_data['password']

            self.login_page.login_user(email, password)
            time.sleep(3)

            current_url = self.driver.current_url
            self.assert_with_screenshot(
                "/login" not in current_url,
                f"使用注册凭据登录应该成功，当前URL: {current_url}"
            )

    @allure.story("安全测试")
    @allure.title("SQL注入测试")
    @allure.description("测试登录表单是否存在SQL注入漏洞")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_sql_injection_protection(self):
        """测试SQL注入防护"""
        with allure.step("导航到登录页面"):
            assert self.navigate_to_login(), "登录页面加载失败"

        sql_injection_payloads = [
            "' OR '1'='1",
            "admin'--",
            "' UNION SELECT * FROM users--",
            "'; DROP TABLE users; --"
        ]

        for payload in sql_injection_payloads:
            with allure.step(f"测试SQL注入payload: {payload}"):
                self.login_page.clear_login_form()
                self.login_page.login_user(payload, payload)
                time.sleep(2)

                # 验证仍在登录页面（SQL注入被阻止）
                current_url = self.driver.current_url
                self.assert_with_screenshot(
                    "/login" in current_url,
                    f"SQL注入payload应该被阻止: {payload}"
                )

    @allure.story("性能测试")
    @allure.title("登录响应时间测试")
    @allure.description("测试登录操作的响应时间")
    @allure.severity(allure.severity_level.LOW)
    @pytest.mark.slow
    def test_login_response_time(self):
        """测试登录响应时间"""
        user_data = self.test_data.get_user_data()
        valid_user = user_data.get("valid_user", {})

        with allure.step("导航到登录页面"):
            assert self.navigate_to_login(), "登录页面加载失败"

        with allure.step("测量登录响应时间"):
            start_time = time.time()

            email = valid_user.get("email", "testuser@example.com")
            password = valid_user.get("password", "Test123456")
            self.login_page.login_user(email, password)

            # 等待页面跳转
            time.sleep(3)
            end_time = time.time()

            response_time = end_time - start_time
            log.performance("Login response time", response_time, "seconds")

            # 验证响应时间在合理范围内（10秒）
            self.assert_with_screenshot(
                response_time < 10,
                f"登录响应时间过长: {response_time:.2f}秒"
            )
