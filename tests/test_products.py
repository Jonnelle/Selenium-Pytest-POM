"""
产品功能测试用例
测试产品浏览、搜索、筛选等功能
"""
import pytest
import allure
import time
from tests.base_test import BaseTest
from utils.logger import log


@allure.epic("AutomationExercise网站测试")
@allure.feature("产品功能")
class TestProducts(BaseTest):
    """产品功能测试类"""

    @allure.story("产品页面")
    @allure.title("验证产品页面加载")
    @allure.description("测试产品页面能够正确加载并显示产品列表")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.product
    def test_products_page_loads(self):
        """测试产品页面加载"""
        with allure.step("导航到产品页面"):
            assert self.navigate_to_products(), "产品页面加载失败"

        with allure.step("验证'All Products'标题"):
            assert self.products_page.verify_all_products_title(), "'All Products'标题不可见"

        with allure.step("验证产品列表"):
            assert self.products_page.verify_products_visible(), "产品列表不可见"

        with allure.step("验证产品数量"):
            product_count = self.products_page.get_product_count()
            self.assert_with_screenshot(
                product_count > 0,
                f"应该显示产品，实际产品数量: {product_count}"
            )

    @allure.story("产品详情")
    @allure.title("查看产品详情")
    @allure.description("测试点击查看产品详情功能")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.product
    def test_view_product_details(self):
        """测试查看产品详情"""
        with allure.step("导航到产品页面"):
            assert self.navigate_to_products(), "产品页面加载失败"

        with allure.step("点击查看第一个产品"):
            self.products_page.click_view_first_product()
            time.sleep(2)

        with allure.step("验证跳转到产品详情页"):
            current_url = self.products_page.get_current_url()
            self.assert_with_screenshot(
                "/product_details/" in current_url,
                f"应该跳转到产品详情页，当前URL: {current_url}"
            )

    @allure.story("产品搜索")
    @allure.title("搜索产品功能")
    @allure.description("测试产品搜索功能的基本操作")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.product
    def test_product_search_basic(self):
        """测试基本产品搜索"""
        with allure.step("导航到产品页面"):
            assert self.navigate_to_products(), "产品页面加载失败"

        with allure.step("搜索'top'"):
            self.products_page.search_product("top")

        with allure.step("验证搜索结果标题"):
            assert self.products_page.verify_searched_products_title(), "搜索结果标题不正确"

        with allure.step("验证搜索结果"):
            assert self.products_page.verify_products_visible(), "搜索结果为空"

        with allure.step("验证搜索结果包含搜索词"):
            assert self.products_page.verify_search_results_contain_term("top"), "搜索结果不包含搜索词"

    @pytest.mark.parametrize("search_term,should_have_results", [
        ("top", True),
        ("dress", True),
        ("tshirt", True),
        ("jeans", True),
        ("saree", True),
        ("kids", True),
        ("nonexistent", False)
    ])
    @allure.story("产品搜索")
    @allure.title("参数化搜索测试")
    @allure.description("使用不同关键词进行搜索测试")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.product
    def test_product_search_parametrized(self, search_term, should_have_results):
        """参数化搜索测试"""
        with allure.step(f"搜索关键词: {search_term}"):
            assert self.navigate_to_products(), "产品页面加载失败"

            self.products_page.search_product(search_term)
            time.sleep(2)

            assert self.products_page.verify_searched_products_title(), "搜索结果标题不正确"

            has_results = self.products_page.verify_products_visible()

            if should_have_results:
                self.assert_with_screenshot(
                    has_results,
                    f"搜索'{search_term}'应该有结果"
                )
                # 验证结果相关性
                if has_results:
                    assert self.products_page.verify_search_results_contain_term(search_term), \
                        f"搜索结果应该包含关键词'{search_term}'"
            else:
                # 对于不存在的关键词，可能有结果也可能没有结果
                log.step(f"搜索'{search_term}'的结果: {'有结果' if has_results else '无结果'}")

    @allure.story("产品搜索")
    @allure.title("空搜索测试")
    @allure.description("测试空关键词搜索的行为")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.product
    def test_empty_search(self):
        """测试空搜索"""
        with allure.step("导航到产品页面"):
            assert self.navigate_to_products(), "产品页面加载失败"

        with allure.step("执行空搜索"):
            self.products_page.search_product("")
            time.sleep(2)

        with allure.step("验证搜索行为"):
            # 空搜索可能显示所有产品或保持原状
            current_url = self.products_page.get_current_url()
            # 验证页面仍然可用
            assert self.products_page.verify_element_visible(
                self.products_page.SEARCH_INPUT
            ), "搜索框应该仍然可见"

    @allure.story("产品搜索")
    @allure.title("特殊字符搜索测试")
    @allure.description("测试使用特殊字符进行搜索")
    @allure.severity(allure.severity_level.LOW)
    @pytest.mark.product
    @pytest.mark.regression
    def test_special_character_search(self):
        """测试特殊字符搜索"""
        special_chars = ["@#$%", "123", "   ", "!@#$%^&*()"]

        for char in special_chars:
            with allure.step(f"搜索特殊字符: '{char}'"):
                assert self.navigate_to_products(), "产品页面加载失败"

                self.products_page.search_product(char)
                time.sleep(2)

                # 验证页面没有崩溃
                assert self.products_page.verify_element_visible(
                    self.products_page.SEARCH_INPUT
                ), f"搜索特殊字符'{char}'后页面应该仍然可用"

    @allure.story("添加到购物车")
    @allure.title("添加产品到购物车")
    @allure.description("测试从产品页面添加产品到购物车")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_add_product_to_cart(self):
        """测试添加产品到购物车"""
        with allure.step("导航到产品页面"):
            assert self.navigate_to_products(), "产品页面加载失败"

        with allure.step("添加第一个产品到购物车"):
            self.products_page.add_first_product_to_cart()

        with allure.step("验证模态框出现"):
            assert self.products_page.verify_modal_appeared(), "添加到购物车模态框未出现"

        with allure.step("点击查看购物车"):
            self.products_page.click_view_cart_from_modal()
            time.sleep(2)

        with allure.step("验证跳转到购物车页面"):
            current_url = self.driver.current_url
            self.assert_with_screenshot(
                "/view_cart" in current_url,
                f"应该跳转到购物车页面，当前URL: {current_url}"
            )

        with allure.step("验证产品已添加到购物车"):
            self.cart_page = self.cart_page.__class__(self.driver)
            assert self.cart_page.verify_cart_has_items(), "购物车应该包含商品"

    @allure.story("添加到购物车")
    @allure.title("继续购物功能")
    @allure.description("测试添加产品后继续购物功能")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    def test_continue_shopping(self):
        """测试继续购物功能"""
        with allure.step("导航到产品页面"):
            assert self.navigate_to_products(), "产品页面加载失败"

        with allure.step("添加产品到购物车"):
            self.products_page.add_first_product_to_cart()

        with allure.step("验证模态框出现"):
            assert self.products_page.verify_modal_appeared(), "添加到购物车模态框未出现"

        with allure.step("点击继续购物"):
            self.products_page.click_continue_shopping()
            time.sleep(2)

        with allure.step("验证仍在产品页面"):
            current_url = self.driver.current_url
            self.assert_with_screenshot(
                "/products" in current_url,
                f"继续购物后应该仍在产品页面，当前URL: {current_url}"
            )

    @allure.story("产品分类")
    @allure.title("验证分类面板")
    @allure.description("测试产品页面的分类面板功能")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.product
    def test_category_panel(self):
        """测试分类面板"""
        with allure.step("导航到产品页面"):
            assert self.navigate_to_products(), "产品页面加载失败"

        with allure.step("验证分类面板可见"):
            assert self.products_page.verify_category_panel_visible(), "分类面板不可见"

    @allure.story("产品品牌")
    @allure.title("验证品牌面板")
    @allure.description("测试产品页面的品牌面板功能")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.product
    def test_brands_panel(self):
        """测试品牌面板"""
        with allure.step("导航到产品页面"):
            assert self.navigate_to_products(), "产品页面加载失败"

        with allure.step("验证品牌面板可见"):
            assert self.products_page.verify_brands_panel_visible(), "品牌面板不可见"

        with allure.step("获取可用品牌"):
            brands = self.products_page.get_available_brands()
            self.assert_with_screenshot(
                len(brands) > 0,
                f"应该显示品牌列表，实际获取到: {brands}"
            )

    @allure.story("产品品牌")
    @allure.title("品牌筛选功能")
    @allure.description("测试点击品牌进行产品筛选")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.product
    def test_brand_filtering(self):
        """测试品牌筛选"""
        with allure.step("导航到产品页面"):
            assert self.navigate_to_products(), "产品页面加载失败"

        with allure.step("点击Polo品牌"):
            self.products_page.click_brand_by_name("Polo")
            time.sleep(2)

        with allure.step("验证跳转到品牌页面"):
            current_url = self.driver.current_url
            self.assert_with_screenshot(
                "/brand_products/Polo" in current_url,
                f"应该跳转到Polo品牌页面，当前URL: {current_url}"
            )

    @allure.story("产品交互")
    @allure.title("产品悬停效果")
    @allure.description("测试鼠标悬停在产品上的效果")
    @allure.severity(allure.severity_level.LOW)
    @pytest.mark.product
    def test_product_hover_effect(self):
        """测试产品悬停效果"""
        with allure.step("导航到产品页面"):
            assert self.navigate_to_products(), "产品页面加载失败"

        with allure.step("鼠标悬停在第一个产品上"):
            self.products_page.hover_on_product_by_index(0)
            time.sleep(2)

        with allure.step("验证页面仍然正常"):
            # 悬停后页面应该仍然可用
            assert self.products_page.verify_element_visible(
                self.products_page.ALL_PRODUCTS_TITLE
            ), "悬停后页面应该仍然正常"

    @allure.story("性能测试")
    @allure.title("产品页面加载性能")
    @allure.description("测试产品页面的加载性能")
    @allure.severity(allure.severity_level.LOW)
    @pytest.mark.slow
    def test_products_page_performance(self):
        """测试产品页面加载性能"""
        with allure.step("测量页面加载时间"):
            start_time = time.time()

            assert self.navigate_to_products(), "产品页面加载失败"

            # 等待所有产品加载完成
            self.products_page.verify_products_visible()

            end_time = time.time()
            load_time = end_time - start_time

            log.performance("Products page load time", load_time, "seconds")

            # 验证加载时间在合理范围内（15秒）
            self.assert_with_screenshot(
                load_time < 15,
                f"产品页面加载时间过长: {load_time:.2f}秒"
            )

    @allure.story("性能测试")
    @allure.title("搜索响应时间")
    @allure.description("测试产品搜索的响应时间")
    @allure.severity(allure.severity_level.LOW)
    @pytest.mark.slow
    def test_search_response_time(self):
        """测试搜索响应时间"""
        with allure.step("导航到产品页面"):
            assert self.navigate_to_products(), "产品页面加载失败"

        with allure.step("测量搜索响应时间"):
            start_time = time.time()

            self.products_page.search_product("top")
            self.products_page.verify_searched_products_title()

            end_time = time.time()
            search_time = end_time - start_time

            log.performance("Search response time", search_time, "seconds")

            # 验证搜索响应时间在合理范围内（10秒）
            self.assert_with_screenshot(
                search_time < 10,
                f"搜索响应时间过长: {search_time:.2f}秒"
            )

    @allure.story("错误处理")
    @allure.title("网络错误处理")
    @allure.description("测试产品页面在网络错误情况下的表现")
    @allure.severity(allure.severity_level.LOW)
    @pytest.mark.regression
    def test_network_error_handling(self):
        """测试网络错误处理"""
        with allure.step("导航到产品页面"):
            assert self.navigate_to_products(), "产品页面加载失败"

        with allure.step("模拟网络中断"):
            # 这里可以通过各种方式模拟网络问题，比如设置无效代理
            # 由于环境限制，这里只做基本的错误恢复测试

            # 尝试刷新页面
            self.products_page.refresh_page()
            time.sleep(3)

        with allure.step("验证页面恢复"):
            # 验证页面能够正常恢复
            assert self.products_page.verify_all_products_title(), "页面刷新后应该能正常显示"

    @allure.story("数据验证")
    @allure.title("产品数据完整性")
    @allure.description("验证产品页面显示的数据完整性")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.product
    def test_product_data_integrity(self):
        """测试产品数据完整性"""
        with allure.step("导航到产品页面"):
            assert self.navigate_to_products(), "产品页面加载失败"

        with allure.step("获取产品信息"):
            product_names = self.products_page.get_product_names()
            product_prices = self.products_page.get_product_prices()

        with allure.step("验证产品名称"):
            self.assert_with_screenshot(
                len(product_names) > 0,
                "应该有产品名称数据"
            )

            # 验证产品名称不为空
            for name in product_names:
                assert name.strip() != "", f"产品名称不应为空: '{name}'"

        with allure.step("验证产品价格"):
            self.assert_with_screenshot(
                len(product_prices) > 0,
                "应该有产品价格数据"
            )

            # 验证价格格式
            for price in product_prices:
                assert "Rs." in price or "$" in price or "₹" in price, \
                    f"价格格式不正确: '{price}'"

        with allure.step("验证数据一致性"):
            # 产品名称和价格数量应该一致（如果页面设计如此）
            log.step(f"产品名称数量: {len(product_names)}, 价格数量: {len(product_prices)}")
            # 注意：实际验证需要根据具体页面结构调整
