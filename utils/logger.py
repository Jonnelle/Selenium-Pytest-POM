"""
日志管理器
基于loguru的日志记录功能
"""
import os
import sys
from pathlib import Path
from loguru import logger
from utils.config_manager import ConfigManager


class Logger:
    """日志管理器类"""

    def __init__(self):
        """初始化日志管理器"""
        self.config = ConfigManager()
        self._setup_logger()

    def _setup_logger(self):
        """设置日志配置"""
        # 移除默认处理器
        logger.remove()

        # 获取配置
        log_level = self.config.get("logging.level", "INFO")
        log_format = self.config.get("logging.format",
                                   "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}")
        log_file = self.config.get("logging.file", "reports/logs/automation.log")
        rotation = self.config.get("logging.rotation", "10 MB")
        retention = self.config.get("logging.retention", "30 days")

        # 确保日志目录存在
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)

        # 添加控制台输出
        logger.add(
            sys.stdout,
            format=log_format,
            level=log_level,
            colorize=True,
            enqueue=True
        )

        # 添加文件输出
        logger.add(
            log_file,
            format=log_format,
            level=log_level,
            rotation=rotation,
            retention=retention,
            encoding="utf-8",
            enqueue=True
        )

        # 绑定到实例
        self.logger = logger.bind(name="AutomationTest")

    def info(self, message: str, **kwargs):
        """记录信息日志"""
        self.logger.info(message, **kwargs)

    def debug(self, message: str, **kwargs):
        """记录调试日志"""
        self.logger.debug(message, **kwargs)

    def warning(self, message: str, **kwargs):
        """记录警告日志"""
        self.logger.warning(message, **kwargs)

    def error(self, message: str, **kwargs):
        """记录错误日志"""
        self.logger.error(message, **kwargs)

    def critical(self, message: str, **kwargs):
        """记录严重错误日志"""
        self.logger.critical(message, **kwargs)

    def exception(self, message: str, **kwargs):
        """记录异常日志"""
        self.logger.exception(message, **kwargs)

    def step(self, message: str, **kwargs):
        """记录测试步骤"""
        self.logger.info(f"🔸 STEP: {message}", **kwargs)

    def result(self, message: str, success: bool = True, **kwargs):
        """记录测试结果"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.logger.info(f"{status}: {message}", **kwargs)

    def api_request(self, method: str, url: str, **kwargs):
        """记录API请求"""
        self.logger.info(f"📤 API Request: {method} {url}", **kwargs)

    def api_response(self, status_code: int, response_time: float = None, **kwargs):
        """记录API响应"""
        time_info = f" ({response_time:.2f}s)" if response_time else ""
        self.logger.info(f"📥 API Response: {status_code}{time_info}", **kwargs)

    def page_action(self, action: str, element: str = None, **kwargs):
        """记录页面操作"""
        element_info = f" on '{element}'" if element else ""
        self.logger.info(f"🔄 Page Action: {action}{element_info}", **kwargs)

    def assertion(self, message: str, expected: str, actual: str, **kwargs):
        """记录断言信息"""
        self.logger.info(f"🔍 Assertion: {message} | Expected: '{expected}' | Actual: '{actual}'", **kwargs)

    def test_start(self, test_name: str, **kwargs):
        """记录测试开始"""
        self.logger.info(f"🚀 Test Started: {test_name}", **kwargs)

    def test_end(self, test_name: str, status: str, duration: float = None, **kwargs):
        """记录测试结束"""
        duration_info = f" ({duration:.2f}s)" if duration else ""
        emoji = "✅" if status.upper() == "PASSED" else "❌" if status.upper() == "FAILED" else "⏭️"
        self.logger.info(f"{emoji} Test Finished: {test_name} - {status.upper()}{duration_info}", **kwargs)

    def browser_action(self, action: str, details: str = None, **kwargs):
        """记录浏览器操作"""
        details_info = f" - {details}" if details else ""
        self.logger.info(f"🌐 Browser: {action}{details_info}", **kwargs)

    def data_operation(self, operation: str, data_type: str = None, **kwargs):
        """记录数据操作"""
        data_info = f" ({data_type})" if data_type else ""
        self.logger.info(f"📊 Data Operation: {operation}{data_info}", **kwargs)

    def performance(self, metric: str, value: float, unit: str = "ms", **kwargs):
        """记录性能指标"""
        self.logger.info(f"⚡ Performance: {metric} = {value}{unit}", **kwargs)

    @staticmethod
    def get_logger() -> 'Logger':
        """获取日志实例（单例模式）"""
        if not hasattr(Logger, '_instance'):
            Logger._instance = Logger()
        return Logger._instance


# 便捷的全局日志实例
log = Logger.get_logger()
