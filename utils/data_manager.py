"""
数据管理器
用于管理测试数据
"""
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any
from faker import Faker
from utils.config_manager import ConfigManager
from utils.logger import log


class DataManager:
    """数据管理器类"""

    def __init__(self, config: ConfigManager):
        """
        初始化数据管理器

        Args:
            config: 配置管理器实例
        """
        self.config = config
        self.fake = Faker(['zh_CN', 'en_US'])
        self._ensure_data_directories()

    def _ensure_data_directories(self):
        """确保数据目录存在"""
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)

    def load_json_data(self, file_path: str) -> Dict[str, Any]:
        """
        加载JSON数据文件

        Args:
            file_path: 文件路径

        Returns:
            JSON数据字典
        """
        try:
            path = Path(file_path)
            if path.exists():
                with open(path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    log.data_operation(f"Loaded JSON data from {file_path}", "JSON")
                    return data
            else:
                log.warning(f"JSON文件不存在: {file_path}")
                return {}
        except Exception as e:
            log.error(f"加载JSON数据失败: {str(e)}")
            return {}

    def save_json_data(self, data: Dict[str, Any], file_path: str):
        """
        保存数据到JSON文件

        Args:
            data: 要保存的数据
            file_path: 文件路径
        """
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)

            log.data_operation(f"Saved JSON data to {file_path}", "JSON")
        except Exception as e:
            log.error(f"保存JSON数据失败: {str(e)}")

    def load_excel_data(self, file_path: str, sheet_name: str = None) -> pd.DataFrame:
        """
        加载Excel数据文件

        Args:
            file_path: 文件路径
            sheet_name: 工作表名称

        Returns:
            pandas DataFrame
        """
        try:
            path = Path(file_path)
            if path.exists():
                df = pd.read_excel(path, sheet_name=sheet_name)
                log.data_operation(f"Loaded Excel data from {file_path}", "Excel")
                return df
            else:
                log.warning(f"Excel文件不存在: {file_path}")
                return pd.DataFrame()
        except Exception as e:
            log.error(f"加载Excel数据失败: {str(e)}")
            return pd.DataFrame()

    def save_excel_data(self, data: pd.DataFrame, file_path: str, sheet_name: str = "Sheet1"):
        """
        保存数据到Excel文件

        Args:
            data: pandas DataFrame
            file_path: 文件路径
            sheet_name: 工作表名称
        """
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            data.to_excel(path, sheet_name=sheet_name, index=False)
            log.data_operation(f"Saved Excel data to {file_path}", "Excel")
        except Exception as e:
            log.error(f"保存Excel数据失败: {str(e)}")

    def get_user_data(self) -> Dict[str, Any]:
        """获取用户测试数据"""
        users_file = self.config.get("test_data.users_file", "data/users.json")
        return self.load_json_data(users_file)

    def get_product_data(self) -> Dict[str, Any]:
        """获取产品测试数据"""
        products_file = self.config.get("test_data.products_file", "data/products.json")
        return self.load_json_data(products_file)

    def generate_test_user(self, save_to_file: bool = False) -> Dict[str, str]:
        """
        生成测试用户数据

        Args:
            save_to_file: 是否保存到文件

        Returns:
            用户数据字典
        """
        user_data = {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "email": self.fake.email(),
            "password": self.fake.password(length=12),
            "company": self.fake.company(),
            "address": self.fake.address(),
            "address2": self.fake.secondary_address(),
            "country": "India",
            "state": self.fake.state(),
            "city": self.fake.city(),
            "zipcode": self.fake.zipcode(),
            "mobile_number": self.fake.phone_number()
        }

        if save_to_file:
            users_file = self.config.get("test_data.users_file", "data/users.json")
            existing_users = self.load_json_data(users_file)
            if "generated_users" not in existing_users:
                existing_users["generated_users"] = []
            existing_users["generated_users"].append(user_data)
            self.save_json_data(existing_users, users_file)

        log.data_operation("Generated test user data", "User")
        return user_data

    def generate_contact_data(self) -> Dict[str, str]:
        """生成联系我们表单数据"""
        contact_data = {
            "name": self.fake.name(),
            "email": self.fake.email(),
            "subject": self.fake.sentence(nb_words=6),
            "message": self.fake.text(max_nb_chars=500)
        }

        log.data_operation("Generated contact form data", "Contact")
        return contact_data

    def get_test_data_by_scenario(self, scenario: str) -> List[Dict[str, Any]]:
        """
        根据场景获取测试数据

        Args:
            scenario: 测试场景名称

        Returns:
            测试数据列表
        """
        try:
            test_data_file = self.config.get("test_data.test_data_file", "data/test_data.xlsx")
            df = self.load_excel_data(test_data_file, sheet_name=scenario)

            if not df.empty:
                data_list = df.to_dict('records')
                log.data_operation(f"Loaded test data for scenario: {scenario}", "Excel")
                return data_list
            else:
                log.warning(f"没有找到场景 '{scenario}' 的测试数据")
                return []
        except Exception as e:
            log.error(f"获取测试数据失败: {str(e)}")
            return []

    def create_test_data_template(self):
        """创建测试数据模板文件"""
        try:
            # 创建用户数据模板
            user_template = {
                "valid_user": {
                    "first_name": "Test",
                    "last_name": "User",
                    "email": "testuser@example.com",
                    "password": "Test123456",
                    "company": "Test Company",
                    "address": "123 Test Street",
                    "address2": "Apt 4B",
                    "country": "India",
                    "state": "Delhi",
                    "city": "New Delhi",
                    "zipcode": "110001",
                    "mobile_number": "9876543210"
                },
                "invalid_user": {
                    "first_name": "",
                    "last_name": "",
                    "email": "invalid-email",
                    "password": "123",
                    "company": "",
                    "address": "",
                    "address2": "",
                    "country": "",
                    "state": "",
                    "city": "",
                    "zipcode": "",
                    "mobile_number": "invalid"
                }
            }

            # 创建产品数据模板
            product_template = {
                "products": [
                    {
                        "id": 1,
                        "name": "Blue Top",
                        "price": "Rs. 500",
                        "category": "Women > Tops"
                    },
                    {
                        "id": 2,
                        "name": "Men Tshirt",
                        "price": "Rs. 400",
                        "category": "Men > Tshirts"
                    }
                ]
            }

            # 保存模板文件
            self.save_json_data(user_template, "data/users.json")
            self.save_json_data(product_template, "data/products.json")

            # 创建Excel测试数据模板
            login_data = pd.DataFrame([
                {"email": "testuser@example.com", "password": "Test123456", "expected_result": "success"},
                {"email": "invalid@email.com", "password": "wrongpass", "expected_result": "failure"},
                {"email": "", "password": "", "expected_result": "failure"}
            ])

            contact_data = pd.DataFrame([
                {"name": "Test User", "email": "test@example.com", "subject": "Test Subject", "message": "Test Message"},
                {"name": "", "email": "invalid-email", "subject": "", "message": ""}
            ])

            # 保存到Excel文件
            with pd.ExcelWriter("data/test_data.xlsx", engine='openpyxl') as writer:
                login_data.to_excel(writer, sheet_name='login_tests', index=False)
                contact_data.to_excel(writer, sheet_name='contact_tests', index=False)

            log.data_operation("Created test data templates", "Templates")

        except Exception as e:
            log.error(f"创建测试数据模板失败: {str(e)}")

    def get_random_product_name(self) -> str:
        """获取随机产品名称"""
        products = ["Blue Top", "Men Tshirt", "Sleeveless Dress", "Stylish Dress", "Winter Top"]
        return self.fake.random_element(products)

    def get_random_search_term(self) -> str:
        """获取随机搜索词"""
        search_terms = ["top", "dress", "tshirt", "jeans", "saree", "kids", "women", "men"]
        return self.fake.random_element(search_terms)
