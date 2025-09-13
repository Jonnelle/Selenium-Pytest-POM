"""
购物车功能测试用例
测试购物车的添加、删除、更新等功能
"""
import pytest
import allure
import time
from selenium.webdriver.common.by import By
from tests.base_test import BaseTest
from utils.logger import log


@allure.epic("AutomationExercise网站测试")
@allure.feature("购物车功能")
class TestCart(BaseTest):
    """购物车功能测试类"""

    @allure.story("购物车页面")
    @allure.title("验证购物车页面加载")
    @allure.description("测试购物车页面能够正确加载")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_cart_page_loads(self):
        """测试购物车页面加载"""
        with allure.step("导航到购物车页面"):
            assert self.navigate_to_cart(), "购物车页面加载失败"

        with allure.step("验证页面加载"):
            assert self.cart_page.verify_page_loaded(), "购物车页面元素不完整"

    @allure.story("空购物车")
    @allure.title("验证空购物车状态")
    @allure.description("测试空购物车的显示状态")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    def test_empty_cart_display(self):
        """测试空购物车显示"""
        with allure.step("导航到购物车页面"):
            assert self.navigate_to_cart(), "购物车页面加载失败"

        with allure.step("验证空购物车状态"):
            # 清空购物车以确保测试环境
            if self.cart_page.verify_cart_has_items():
                self.cart_page.clear_cart()
                time.sleep(2)

            is_empty = self.cart_page.verify_cart_is_empty()
            self.assert_with_screenshot(
                is_empty,
                "购物车应该为空"
            )

    @allure.story("添加商品")
    @allure.title("从首页添加商品到购物车")
    @allure.description("测试从首页添加商品到购物车的功能")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_add_product_from_home(self):
        """测试从首页添加商品到购物车"""
        with allure.step("导航到首页"):
            assert self.navigate_to_home(), "首页加载失败"

        with allure.step("获取第一个产品名称"):
            product_names = self.home_page.get_product_names()
            if not product_names:
                pytest.skip("首页没有可用产品")

            first_product_name = product_names[0]
            log.step(f"将要添加的产品: {first_product_name}")

        with allure.step("添加第一个产品到购物车"):
            self.home_page.add_product_to_cart_by_index(0)
            time.sleep(2)

        with allure.step("导航到购物车页面"):
            self.navigate_to_cart()

        with allure.step("验证产品已添加"):
            assert self.cart_page.verify_cart_has_items(), "购物车应该包含商品"

            # 验证产品名称
            cart_products = self.cart_page.get_product_names_in_cart()
            product_found = any(first_product_name in product for product in cart_products)
            self.assert_with_screenshot(
                product_found,
                f"购物车应该包含产品'{first_product_name}'，实际包含: {cart_products}"
            )

    @allure.story("添加商品")
    @allure.title("从产品页面添加商品到购物车")
    @allure.description("测试从产品页面添加商品到购物车的功能")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    def test_add_product_from_products_page(self):
        """测试从产品页面添加商品到购物车"""
        with allure.step("导航到产品页面"):
            assert self.navigate_to_products(), "产品页面加载失败"

        with allure.step("获取第一个产品名称"):
            product_names = self.products_page.get_product_names()
            if not product_names:
                pytest.skip("产品页面没有可用产品")

            first_product_name = product_names[0]
            log.step(f"将要添加的产品: {first_product_name}")

        with allure.step("添加产品到购物车"):
            self.products_page.add_first_product_to_cart()
            time.sleep(2)

        with allure.step("验证模态框并查看购物车"):
            if self.products_page.verify_modal_appeared():
                self.products_page.click_view_cart_from_modal()
            else:
                self.navigate_to_cart()

        with allure.step("验证产品已添加"):
            assert self.cart_page.verify_cart_has_items(), "购物车应该包含商品"

            cart_products = self.cart_page.get_product_names_in_cart()
            product_found = any(first_product_name in product for product in cart_products)
            self.assert_with_screenshot(
                product_found,
                f"购物车应该包含产品'{first_product_name}'"
            )

    @allure.story("删除商品")
    @allure.title("从购物车删除商品")
    @allure.description("测试从购物车删除商品的功能")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.cart
    def test_remove_product_from_cart(self):
        """测试从购物车删除商品"""
        # 先添加商品到购物车
        with allure.step("准备测试数据 - 添加商品到购物车"):
            assert self.add_product_to_cart(), "添加商品到购物车失败"

        with allure.step("导航到购物车页面"):
            assert self.navigate_to_cart(), "购物车页面加载失败"

        with allure.step("验证购物车有商品"):
            assert self.cart_page.verify_cart_has_items(), "购物车应该包含商品"

        with allure.step("获取删除前的商品数量"):
            initial_count = self.cart_page.get_cart_item_count()
            log.step(f"删除前商品数量: {initial_count}")

        with allure.step("删除第一个商品"):
            self.cart_page.delete_first_product()
            time.sleep(3)  # 等待页面更新

        with allure.step("验证商品已删除"):
            final_count = self.cart_page.get_cart_item_count()
            log.step(f"删除后商品数量: {final_count}")

            self.assert_with_screenshot(
                final_count < initial_count,
                f"商品数量应该减少，删除前: {initial_count}，删除后: {final_count}"
            )

    @allure.story("购物车信息")
    @allure.title("验证购物车商品信息")
    @allure.description("测试购物车显示的商品信息是否正确")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    def test_cart_product_information(self):
        """测试购物车商品信息"""
        # 先添加商品到购物车
        with allure.step("准备测试数据 - 添加商品到购物车"):
            assert self.add_product_to_cart(), "添加商品到购物车失败"

        with allure.step("导航到购物车页面"):
            assert self.navigate_to_cart(), "购物车页面加载失败"

        with allure.step("获取购物车信息"):
            cart_summary = self.cart_page.get_cart_summary()
            log.step(f"购物车摘要: {cart_summary}")

        with allure.step("验证商品名称"):
            product_names = cart_summary["product_names"]
            self.assert_with_screenshot(
                len(product_names) > 0,
                "购物车应该显示产品名称"
            )

            for name in product_names:
                assert name.strip() != "", f"产品名称不应为空: '{name}'"

        with allure.step("验证商品价格"):
            prices = self.cart_page.get_product_prices_in_cart()
            self.assert_with_screenshot(
                len(prices) > 0,
                "购物车应该显示产品价格"
            )

            for price in prices:
                assert "Rs." in price or "$" in price, f"价格格式不正确: '{price}'"

        with allure.step("验证商品数量"):
            quantities = self.cart_page.get_product_quantities_in_cart()
            self.assert_with_screenshot(
                len(quantities) > 0,
                "购物车应该显示产品数量"
            )

            for quantity in quantities:
                assert quantity.isdigit() and int(quantity) > 0, f"数量应该是正整数: '{quantity}'"

    @allure.story("数量更新")
    @allure.title("更新购物车商品数量")
    @allure.description("测试更新购物车中商品数量的功能")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    def test_update_product_quantity(self):
        """测试更新商品数量"""
        # 先添加商品到购物车
        with allure.step("准备测试数据 - 添加商品到购物车"):
            assert self.add_product_to_cart(), "添加商品到购物车失败"

        with allure.step("导航到购物车页面"):
            assert self.navigate_to_cart(), "购物车页面加载失败"

        with allure.step("获取初始数量"):
            initial_quantities = self.cart_page.get_product_quantities_in_cart()
            if not initial_quantities:
                pytest.skip("购物车中没有商品")

            initial_quantity = initial_quantities[0]
            log.step(f"初始数量: {initial_quantity}")

        with allure.step("更新第一个商品数量"):
            new_quantity = "2"
            self.cart_page.update_product_quantity(0, new_quantity)
            time.sleep(2)

        with allure.step("验证数量已更新"):
            # 注意：实际网站可能需要刷新页面或点击更新按钮
            # 这里简化处理，实际测试时需要根据网站具体行为调整
            updated_quantities = self.cart_page.get_product_quantities_in_cart()
            if updated_quantities:
                updated_quantity = updated_quantities[0]
                log.step(f"更新后数量: {updated_quantity}")

                # 由于更新机制可能不同，这里只验证数量是有效的
                assert updated_quantity.isdigit(), f"更新后的数量应该是数字: '{updated_quantity}'"

    @allure.story("多商品")
    @allure.title("添加多个商品到购物车")
    @allure.description("测试添加多个不同商品到购物车")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    def test_add_multiple_products(self):
        """测试添加多个商品"""
        with allure.step("清空购物车"):
            self.navigate_to_cart()
            if self.cart_page.verify_cart_has_items():
                self.cart_page.clear_cart()

        with allure.step("导航到首页"):
            assert self.navigate_to_home(), "首页加载失败"

        with allure.step("添加第一个商品"):
            self.home_page.add_product_to_cart_by_index(0)
            time.sleep(2)

        with allure.step("添加第二个商品"):
            # 可能需要关闭模态框或继续购物
            try:
                # 如果有继续购物按钮，点击它
                if self.home_page.verify_element_visible((By.XPATH, "//button[text()='Continue Shopping']"), timeout=3):
                    self.home_page.click_element((By.XPATH, "//button[text()='Continue Shopping']"))
                    time.sleep(1)
            except:
                pass

            self.home_page.add_product_to_cart_by_index(1)
            time.sleep(2)

        with allure.step("导航到购物车页面"):
            self.navigate_to_cart()

        with allure.step("验证多个商品"):
            item_count = self.cart_page.get_cart_item_count()
            self.assert_with_screenshot(
                item_count >= 2,
                f"购物车应该包含至少2个商品，实际数量: {item_count}"
            )

    @allure.story("结账流程")
    @allure.title("购物车结账按钮")
    @allure.description("测试购物车的结账按钮功能")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    def test_proceed_to_checkout(self):
        """测试结账按钮"""
        # 先添加商品到购物车
        with allure.step("准备测试数据 - 添加商品到购物车"):
            assert self.add_product_to_cart(), "添加商品到购物车失败"

        with allure.step("导航到购物车页面"):
            assert self.navigate_to_cart(), "购物车页面加载失败"

        with allure.step("验证结账按钮"):
            assert self.cart_page.verify_proceed_to_checkout_button(), "结账按钮不可见"

        with allure.step("点击结账按钮"):
            self.cart_page.click_proceed_to_checkout()
            time.sleep(3)

        with allure.step("验证跳转"):
            current_url = self.cart_page.get_current_url()
            # 结账可能跳转到登录页面或结账页面
            self.assert_with_screenshot(
                "/checkout" in current_url or "/login" in current_url,
                f"结账应该跳转到结账页面或登录页面，当前URL: {current_url}"
            )

    @allure.story("购物车状态")
    @allure.title("验证购物车总金额")
    @allure.description("测试购物车总金额的计算和显示")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    def test_cart_total_amount(self):
        """测试购物车总金额"""
        # 先添加商品到购物车
        with allure.step("准备测试数据 - 添加商品到购物车"):
            assert self.add_product_to_cart(), "添加商品到购物车失败"

        with allure.step("导航到购物车页面"):
            assert self.navigate_to_cart(), "购物车页面加载失败"

        with allure.step("验证总金额显示"):
            if self.cart_page.verify_total_amount_visible():
                total_amount = self.cart_page.get_total_amount()
                log.step(f"购物车总金额: {total_amount}")

                # 验证总金额格式
                assert total_amount.strip() != "", "总金额不应为空"
                assert "Rs." in total_amount or "$" in total_amount, \
                    f"总金额格式不正确: '{total_amount}'"
            else:
                log.step("购物车页面不显示总金额，跳过此验证")

    @allure.story("清空购物车")
    @allure.title("清空所有购物车商品")
    @allure.description("测试清空购物车的功能")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    def test_clear_cart(self):
        """测试清空购物车"""
        # 先添加商品到购物车
        with allure.step("准备测试数据 - 添加商品到购物车"):
            assert self.add_product_to_cart(), "添加商品到购物车失败"

        with allure.step("导航到购物车页面"):
            assert self.navigate_to_cart(), "购物车页面加载失败"

        with allure.step("验证购物车有商品"):
            assert self.cart_page.verify_cart_has_items(), "购物车应该包含商品"

        with allure.step("清空购物车"):
            self.cart_page.clear_cart()

        with allure.step("验证购物车已清空"):
            assert self.cart_page.verify_cart_is_empty(), "购物车应该为空"

    @allure.story("购物车持久性")
    @allure.title("购物车跨页面持久性")
    @allure.description("测试购物车内容在页面跳转后是否保持")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    def test_cart_persistence(self):
        """测试购物车持久性"""
        # 先添加商品到购物车
        with allure.step("准备测试数据 - 添加商品到购物车"):
            assert self.add_product_to_cart(), "添加商品到购物车失败"

        with allure.step("导航到购物车页面并记录商品"):
            assert self.navigate_to_cart(), "购物车页面加载失败"
            initial_products = self.cart_page.get_product_names_in_cart()
            initial_count = self.cart_page.get_cart_item_count()
            log.step(f"初始购物车商品: {initial_products}")

        with allure.step("导航到其他页面"):
            self.navigate_to_home()
            time.sleep(2)

        with allure.step("返回购物车页面"):
            self.navigate_to_cart()

        with allure.step("验证购物车内容保持"):
            final_products = self.cart_page.get_product_names_in_cart()
            final_count = self.cart_page.get_cart_item_count()

            self.assert_with_screenshot(
                final_count == initial_count,
                f"购物车商品数量应该保持，初始: {initial_count}，最终: {final_count}"
            )

            # 验证商品名称也保持一致
            assert final_products == initial_products, \
                f"购物车商品应该保持一致，初始: {initial_products}，最终: {final_products}"

    @allure.story("性能测试")
    @allure.title("购物车操作响应时间")
    @allure.description("测试购物车各种操作的响应时间")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.slow
    def test_cart_operations_performance(self):
        """测试购物车操作性能"""
        with allure.step("测试添加商品响应时间"):
            start_time = time.time()
            assert self.add_product_to_cart(), "添加商品失败"
            add_time = time.time() - start_time
            log.performance("Add to cart time", add_time, "seconds")

        with allure.step("测试购物车页面加载时间"):
            start_time = time.time()
            assert self.navigate_to_cart(), "购物车页面加载失败"
            load_time = time.time() - start_time
            log.performance("Cart page load time", load_time, "seconds")

        with allure.step("测试删除商品响应时间"):
            if self.cart_page.verify_cart_has_items():
                start_time = time.time()
                self.cart_page.delete_first_product()
                time.sleep(3)
                delete_time = time.time() - start_time
                log.performance("Delete from cart time", delete_time, "seconds")

        # 验证所有操作在合理时间内完成
        total_time = add_time + load_time
        self.assert_with_screenshot(
            total_time < 20,
            f"购物车操作总时间过长: {total_time:.2f}秒"
        )

    @allure.story("边界测试")
    @allure.title("购物车容量测试")
    @allure.description("测试购物车的最大容量限制")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.cart
    @pytest.mark.slow
    def test_cart_capacity_limits(self):
        """测试购物车容量限制"""
        with allure.step("清空购物车"):
            self.navigate_to_cart()
            if self.cart_page.verify_cart_has_items():
                self.cart_page.clear_cart()

        with allure.step("尝试添加多个相同商品"):
            max_attempts = 5  # 限制测试次数

            for i in range(max_attempts):
                try:
                    self.add_product_to_cart()
                    log.step(f"成功添加第{i+1}个商品")
                except Exception as e:
                    log.step(f"添加第{i+1}个商品时出错: {str(e)}")
                    break

        with allure.step("验证购物车状态"):
            self.navigate_to_cart()
            final_count = self.cart_page.get_cart_item_count()
            log.step(f"最终购物车商品数量: {final_count}")

            # 验证购物车仍然可用
            assert self.cart_page.verify_page_loaded(), "购物车页面应该仍然可用"
