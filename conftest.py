"""
pytest配置文件
包含全局fixtures和配置
"""
import os
import pytest
import allure
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from utils.config_manager import ConfigManager
from utils.logger import Logger


def pytest_configure(config):
    """pytest配置钩子"""
    # 创建报告目录
    os.makedirs("reports/allure-results", exist_ok=True)
    os.makedirs("reports/html", exist_ok=True)
    os.makedirs("reports/screenshots", exist_ok=True)
    os.makedirs("reports/logs", exist_ok=True)


def pytest_addoption(parser):
    """添加命令行选项"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="https://automationexercise.com",
        help="Base URL for testing"
    )


@pytest.fixture(scope="session")
def config():
    """配置管理器fixture"""
    return ConfigManager()


@pytest.fixture(scope="session")
def logger():
    """日志记录器fixture"""
    return Logger()


@pytest.fixture(scope="function")
def browser_setup(request, config, logger):
    """浏览器设置fixture"""
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    logger.info(f"启动 {browser_name} 浏览器，headless模式: {headless}")

    driver = None

    try:
        if browser_name.lower() == "chrome":
            driver = _setup_chrome_driver(headless, config)
        elif browser_name.lower() == "firefox":
            driver = _setup_firefox_driver(headless, config)
        elif browser_name.lower() == "edge":
            driver = _setup_edge_driver(headless, config)
        else:
            raise ValueError(f"不支持的浏览器: {browser_name}")

        # 配置浏览器
        window_size = config.get("browser.window_size", "1920,1080")
        width, height = map(int, window_size.split(","))
        driver.set_window_size(width, height)

        driver.implicitly_wait(config.get("browser.implicit_wait", 10))
        driver.set_page_load_timeout(config.get("browser.page_load_timeout", 30))

        yield driver

    except Exception as e:
        logger.error(f"浏览器设置失败: {str(e)}")
        raise
    finally:
        if driver:
            logger.info("关闭浏览器")
            driver.quit()


def _setup_chrome_driver(headless: bool, config: ConfigManager) -> webdriver.Chrome:
    """设置Chrome浏览器"""
    options = webdriver.ChromeOptions()

    # 添加基础选项
    chrome_options = config.get("browsers.chrome.options", [])
    for option in chrome_options:
        options.add_argument(option)

    if headless:
        options.add_argument("--headless")

    # 设置下载目录
    prefs = {
        "download.default_directory": os.path.abspath("downloads"),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)

    # 修复ChromeDriver路径问题
    try:
        # 清理并重新获取ChromeDriver
        driver_path = ChromeDriverManager().install()

        # 确保路径指向正确的chromedriver.exe
        if not driver_path.endswith('.exe'):
            # 如果路径不是.exe文件，尝试找到正确的chromedriver.exe
            driver_dir = os.path.dirname(driver_path)
            for file in os.listdir(driver_dir):
                if file.startswith('chromedriver') and file.endswith('.exe'):
                    driver_path = os.path.join(driver_dir, file)
                    break

        service = ChromeService(driver_path)
        return webdriver.Chrome(service=service, options=options)

    except Exception as e:
        # 如果自动下载失败，尝试使用系统PATH中的chromedriver
        print(f"自动下载ChromeDriver失败，尝试使用系统ChromeDriver: {e}")
        service = ChromeService()  # 使用系统PATH中的chromedriver
        return webdriver.Chrome(service=service, options=options)


def _setup_firefox_driver(headless: bool, config: ConfigManager) -> webdriver.Firefox:
    """设置Firefox浏览器"""
    options = webdriver.FirefoxOptions()

    if headless:
        options.add_argument("--headless")

    firefox_options = config.get("browsers.firefox.options", [])
    for option in firefox_options:
        options.add_argument(option)

    service = FirefoxService(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=options)


def _setup_edge_driver(headless: bool, config: ConfigManager) -> webdriver.Edge:
    """设置Edge浏览器"""
    options = webdriver.EdgeOptions()

    if headless:
        options.add_argument("--headless")

    edge_options = config.get("browsers.edge.options", [])
    for option in edge_options:
        options.add_argument(option)

    service = EdgeService(EdgeChromiumDriverManager().install())
    return webdriver.Edge(service=service, options=options)


@pytest.fixture(scope="function")
def base_url(request):
    """基础URL fixture"""
    return request.config.getoption("--base-url")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试执行结果钩子 - 用于截图"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # 获取浏览器实例
        if "browser_setup" in item.fixturenames:
            driver = item.funcargs["browser_setup"]
            # 截图
            _take_screenshot(driver, item.name)


def _take_screenshot(driver, test_name: str):
    """截图功能"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"{test_name}_{timestamp}.png"
        screenshot_path = os.path.join("reports/screenshots", screenshot_name)

        driver.save_screenshot(screenshot_path)

        # 添加到Allure报告
        allure.attach.file(
            screenshot_path,
            name=f"截图_{test_name}",
            attachment_type=allure.attachment_type.PNG
        )
    except Exception as e:
        print(f"截图失败: {str(e)}")


@pytest.fixture(scope="function")
def test_data(config):
    """测试数据fixture"""
    from utils.data_manager import DataManager
    return DataManager(config)


def pytest_collection_modifyitems(config, items):
    """修改测试收集"""
    for item in items:
        # 为所有测试添加allure标记
        if not any(mark.name == "allure" for mark in item.iter_markers()):
            item.add_marker(pytest.mark.allure)
