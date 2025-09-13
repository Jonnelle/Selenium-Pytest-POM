"""
首页测试用例
测试AutomationExercise网站首页功能
"""
import pytest
import allure
import time
from tests.base_test import BaseTest
from utils.logger import log


@allure.epic("AutomationExercise网站测试")
@allure.feature("首页功能")
class TestHomePage(BaseTest):
    """首页测试类"""

    @allure.story("页面加载验证")
    @allure.title("验证首页加载成功")
    @allure.description("测试首页能够正确加载并显示所有关键元素")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_home_page_loads_successfully(self):
        """测试首页加载成功"""
        with allure.step("打开首页"):
            assert self.navigate_to_home(), "首页加载失败"

        with allure.step("验证页面标题"):
            title = self.home_page.get_page_title()
            self.assert_with_screenshot(
                "Automation Exercise" in title,
                f"页面标题不正确，实际标题: {title}"
            )

        with allure.step("验证Logo可见"):
            assert self.home_page.verify_element_visible(self.home_page.LOGO), "Logo不可见"

        with allure.step("验证特色商品区域"):
            assert self.home_page.verify_element_visible(self.home_page.FEATURES_ITEMS_TITLE), "特色商品区域不可见"

    @allure.story("导航功能")
    @allure.title("验证导航链接功能")
    @allure.description("测试首页导航链接是否正确工作")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.navigation
    def test_navigation_links(self):
        """测试导航链接"""
        assert self.navigate_to_home(), "首页加载失败"

        with allure.step("测试产品链接"):
            self.home_page.click_products_link()
            time.sleep(2)
            current_url = self.home_page.get_current_url()
            self.assert_with_screenshot(
                "/products" in current_url,
                f"产品页面导航失败，当前URL: {current_url}"
            )

        with allure.step("返回首页"):
            self.navigate_to_home()

        with allure.step("测试登录/注册链接"):
            self.home_page.click_signup_login_link()
            time.sleep(2)
            current_url = self.home_page.get_current_url()
            self.assert_with_screenshot(
                "/login" in current_url,
                f"登录页面导航失败，当前URL: {current_url}"
            )

        with allure.step("返回首页"):
            self.navigate_to_home()

        with allure.step("测试联系我们链接"):
            self.home_page.click_contact_us_link()
            time.sleep(2)
            current_url = self.home_page.get_current_url()
            self.assert_with_screenshot(
                "/contact_us" in current_url,
                f"联系我们页面导航失败，当前URL: {current_url}"
            )

    @allure.story("产品展示")
    @allure.title("验证产品展示功能")
    @allure.description("测试首页产品列表显示和基本交互功能")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.product
    def test_products_display(self):
        """测试产品展示"""
        assert self.navigate_to_home(), "首页加载失败"

        with allure.step("验证产品数量"):
            product_count = self.home_page.get_product_count()
            self.assert_with_screenshot(
                product_count > 0,
                f"首页应该显示产品，实际产品数量: {product_count}"
            )

        with allure.step("验证产品名称获取"):
            product_names = self.home_page.get_product_names()
            self.assert_with_screenshot(
                len(product_names) > 0,
                f"应该能获取产品名称，实际获取到: {product_names}"
            )

        with allure.step("验证产品价格获取"):
            product_prices = self.home_page.get_product_prices()
            self.assert_with_screenshot(
                len(product_prices) > 0,
                f"应该能获取产品价格，实际获取到: {product_prices}"
            )

        with allure.step("验证查看产品功能"):
            self.home_page.click_view_product_by_index(0)
            time.sleep(2)
            current_url = self.home_page.get_current_url()
            self.assert_with_screenshot(
                "/product_details/" in current_url,
                f"产品详情页导航失败，当前URL: {current_url}"
            )

    @allure.story("分类功能")
    @allure.title("验证产品分类功能")
    @allure.description("测试首页产品分类侧边栏功能")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.product
    def test_category_functionality(self):
        """测试分类功能"""
        assert self.navigate_to_home(), "首页加载失败"

        with allure.step("验证分类区域可见"):
            assert self.home_page.verify_categories_section(), "分类区域不可见"

        with allure.step("测试女装分类"):
            self.home_page.click_women_dress_category()
            time.sleep(2)
            current_url = self.home_page.get_current_url()
            self.assert_with_screenshot(
                "/category_products/1" in current_url,
                f"女装连衣裙分类导航失败，当前URL: {current_url}"
            )

        with allure.step("返回首页"):
            self.navigate_to_home()

        with allure.step("测试男装分类"):
            self.home_page.click_men_tshirts_category()
            time.sleep(2)
            current_url = self.home_page.get_current_url()
            self.assert_with_screenshot(
                "/category_products/3" in current_url,
                f"男装T恤分类导航失败，当前URL: {current_url}"
            )

    @allure.story("品牌功能")
    @allure.title("验证品牌筛选功能")
    @allure.description("测试首页品牌筛选功能")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.product
    def test_brand_functionality(self):
        """测试品牌功能"""
        assert self.navigate_to_home(), "首页加载失败"

        with allure.step("验证品牌区域可见"):
            assert self.home_page.verify_brands_section(), "品牌区域不可见"

        with allure.step("测试Polo品牌"):
            self.home_page.click_brand("Polo")
            time.sleep(2)
            current_url = self.home_page.get_current_url()
            self.assert_with_screenshot(
                "/brand_products/Polo" in current_url,
                f"Polo品牌页面导航失败，当前URL: {current_url}"
            )

        with allure.step("返回首页"):
            self.navigate_to_home()

        with allure.step("测试H&M品牌"):
            self.home_page.click_brand("H&M")
            time.sleep(2)
            current_url = self.home_page.get_current_url()
            self.assert_with_screenshot(
                "/brand_products/H&M" in current_url,
                f"H&M品牌页面导航失败，当前URL: {current_url}"
            )

    @allure.story("订阅功能")
    @allure.title("验证邮件订阅功能")
    @allure.description("测试首页邮件订阅功能")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.subscription
    def test_email_subscription(self):
        """测试邮件订阅"""
        assert self.navigate_to_home(), "首页加载失败"

        with allure.step("滚动到页脚"):
            self.home_page.scroll_to_bottom_of_page()
            time.sleep(1)

        with allure.step("验证订阅区域可见"):
            assert self.home_page.verify_subscription_section(), "订阅区域不可见"

        with allure.step("测试邮件订阅"):
            test_email = f"test_{int(time.time())}@example.com"
            subscription_success = self.home_page.subscribe_to_newsletter(test_email)
            self.assert_with_screenshot(
                subscription_success,
                "邮件订阅失败"
            )

    @allure.story("推荐商品")
    @allure.title("验证推荐商品区域")
    @allure.description("测试首页推荐商品区域显示")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.product
    def test_recommended_items(self):
        """测试推荐商品"""
        assert self.navigate_to_home(), "首页加载失败"

        with allure.step("滚动到推荐商品区域"):
            self.home_page.scroll_to_element(self.home_page.RECOMMENDED_ITEMS_TITLE)
            time.sleep(1)

        with allure.step("验证推荐商品区域可见"):
            assert self.home_page.verify_recommended_items_section(), "推荐商品区域不可见"

    @allure.story("页面滚动")
    @allure.title("验证页面滚动功能")
    @allure.description("测试首页滚动到顶部和底部功能")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.navigation
    def test_page_scrolling(self):
        """测试页面滚动"""
        assert self.navigate_to_home(), "首页加载失败"

        with allure.step("滚动到页面底部"):
            self.home_page.scroll_to_bottom_of_page()
            time.sleep(1)

            # 验证页脚元素可见
            assert self.home_page.verify_element_visible(
                self.home_page.COPYRIGHT, timeout=5
            ), "滚动到底部后，页脚元素不可见"

        with allure.step("滚动到页面顶部"):
            self.home_page.scroll_to_top_of_page()
            time.sleep(1)

            # 验证顶部元素可见
            assert self.home_page.verify_element_visible(
                self.home_page.LOGO, timeout=5
            ), "滚动到顶部后，Logo不可见"

    @allure.story("响应式测试")
    @allure.title("验证页面响应式布局")
    @allure.description("测试不同窗口大小下的页面布局")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.slow
    def test_responsive_layout(self):
        """测试响应式布局"""
        assert self.navigate_to_home(), "首页加载失败"

        original_size = self.driver.get_window_size()

        try:
            with allure.step("测试移动端尺寸"):
                self.driver.set_window_size(375, 667)  # iPhone 6/7/8
                time.sleep(2)
                assert self.home_page.verify_element_visible(self.home_page.LOGO), "移动端Logo不可见"

            with allure.step("测试平板尺寸"):
                self.driver.set_window_size(768, 1024)  # iPad
                time.sleep(2)
                assert self.home_page.verify_element_visible(self.home_page.LOGO), "平板端Logo不可见"

            with allure.step("测试桌面尺寸"):
                self.driver.set_window_size(1920, 1080)  # Desktop
                time.sleep(2)
                assert self.home_page.verify_element_visible(self.home_page.LOGO), "桌面端Logo不可见"

        finally:
            # 恢复原始窗口大小
            self.driver.set_window_size(original_size['width'], original_size['height'])

    @allure.story("错误处理")
    @allure.title("验证页面错误处理")
    @allure.description("测试页面在异常情况下的表现")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_error_handling(self):
        """测试错误处理"""
        assert self.navigate_to_home(), "首页加载失败"

        with allure.step("测试JavaScript错误处理"):
            # 执行一个可能出错的JavaScript代码
            try:
                self.home_page.execute_javascript("nonExistentFunction();")
            except Exception:
                # 预期会出错，验证页面仍然可用
                assert self.home_page.verify_element_visible(self.home_page.LOGO), "页面在JavaScript错误后不可用"

        with allure.step("测试页面刷新"):
            self.home_page.refresh_page()
            time.sleep(2)
            assert self.home_page.verify_page_loaded(), "页面刷新后加载失败"
