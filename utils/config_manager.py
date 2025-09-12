"""
配置管理器
用于管理应用程序配置
"""
import os
import yaml
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv


class ConfigManager:
    """配置管理器类"""

    def __init__(self, config_file: str = "config/config.yaml"):
        """
        初始化配置管理器

        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config = {}
        self._load_env_file()
        self._load_config_file()

    def _load_env_file(self):
        """加载环境变量文件"""
        env_file = Path(".env")
        if env_file.exists():
            load_dotenv(env_file)

    def _load_config_file(self):
        """加载YAML配置文件"""
        config_path = Path(self.config_file)
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as file:
                self.config = yaml.safe_load(file) or {}
        else:
            raise FileNotFoundError(f"配置文件不存在: {self.config_file}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            key: 配置键，支持点分隔的嵌套键，如 'browser.default'
            default: 默认值

        Returns:
            配置值
        """
        # 首先检查环境变量
        env_key = key.upper().replace('.', '_')
        env_value = os.getenv(env_key)
        if env_value is not None:
            return self._convert_type(env_value)

        # 然后检查配置文件
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def _convert_type(self, value: str) -> Any:
        """
        转换环境变量类型

        Args:
            value: 字符串值

        Returns:
            转换后的值
        """
        # 布尔值转换
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'

        # 数字转换
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            pass

        # 列表转换（逗号分隔）
        if ',' in value:
            return [item.strip() for item in value.split(',')]

        return value

    def set(self, key: str, value: Any):
        """
        设置配置值

        Args:
            key: 配置键
            value: 配置值
        """
        keys = key.split('.')
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def get_all(self) -> Dict[str, Any]:
        """获取所有配置"""
        return self.config.copy()

    def update_from_dict(self, config_dict: Dict[str, Any]):
        """
        从字典更新配置

        Args:
            config_dict: 配置字典
        """
        self._merge_dicts(self.config, config_dict)

    def _merge_dicts(self, dict1: Dict, dict2: Dict):
        """
        合并两个字典

        Args:
            dict1: 目标字典
            dict2: 源字典
        """
        for key, value in dict2.items():
            if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
                self._merge_dicts(dict1[key], value)
            else:
                dict1[key] = value

    def save_config(self, file_path: str = None):
        """
        保存配置到文件

        Args:
            file_path: 文件路径，默认使用原文件
        """
        save_path = file_path or self.config_file
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'w', encoding='utf-8') as file:
            yaml.dump(self.config, file, default_flow_style=False, allow_unicode=True)

    # 便捷方法
    @property
    def base_url(self) -> str:
        """获取基础URL"""
        return self.get("app.base_url", "https://automationexercise.com")

    @property
    def browser(self) -> str:
        """获取默认浏览器"""
        return self.get("browser.default", "chrome")

    @property
    def headless(self) -> bool:
        """获取无头模式设置"""
        return self.get("browser.headless", False)

    @property
    def implicit_wait(self) -> int:
        """获取隐式等待时间"""
        return self.get("browser.implicit_wait", 10)

    @property
    def explicit_wait(self) -> int:
        """获取显式等待时间"""
        return self.get("browser.explicit_wait", 15)

    @property
    def page_load_timeout(self) -> int:
        """获取页面加载超时时间"""
        return self.get("browser.page_load_timeout", 30)
