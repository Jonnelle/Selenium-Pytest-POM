# AutomationExercise 自动化测试项目

## 📋 项目概述

这是一个基于 **Selenium + Pytest + POM + Allure + CI/CD** 的完整自动化测试框架，专门为 [AutomationExercise](https://automationexercise.com/) 网站设计。

### 🎯 主要特性

- ✅ **多浏览器支持**: Chrome, Firefox, Edge
- ✅ **POM设计模式**: 页面对象模型，提高代码可维护性
- ✅ **数据驱动测试**: 支持JSON、Excel数据源
- ✅ **并行测试执行**: 使用pytest-xdist
- ✅ **详细测试报告**: Allure + HTML报告
- ✅ **CI/CD集成**: GitHub Actions支持
- ✅ **智能等待策略**: 显式等待和重试机制
- ✅ **截图和日志**: 失败自动截图，详细日志记录
- ✅ **配置管理**: 灵活的配置文件系统 

## 🏗️ 项目架构

```
Selenium-Pytest-POM/
├── 📁 .github/workflows/        # CI/CD配置
├── 📁 config/                   # 配置文件
├── 📁 data/                     # 测试数据
├── 📁 pages/                    # 页面对象模型
├── 📁 tests/                    # 测试用例
├── 📁 utils/                    # 工具类
├── 📁 reports/                  # 测试报告
├── 📄 conftest.py               # Pytest配置
├── 📄 pytest.ini               # Pytest设置
├── 📄 requirements.txt          # 依赖包
├── 📄 run_tests.py              # 测试运行脚本
└── 📄 README.md                 # 项目文档
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Chrome/Firefox/Edge 浏览器
- Allure (可选，用于生成报告)

### 安装步骤

1. **克隆项目**
```
git clone <repository-url>
cd Selenium-Pytest-POM
```

2. **安装依赖**
```
pip install -r requirements.txt
```

3. **配置环境变量** (可选)
```
cp .env.example .env
# 编辑 .env 文件，设置个人配置
```

4. **验证安装**
```
python run_tests.py --check-deps
```

### 运行测试

#### 🔥 快速运行

```
# 运行冒烟测试
python run_tests.py --test-type smoke

# 运行回归测试
python run_tests.py --test-type regression

# 运行所有测试
python run_tests.py --test-type all
```

#### ⚙️ 高级选项

```
# 指定浏览器
python run_tests.py --browser firefox --test-type smoke

# 无头模式运行
python run_tests.py --headless --test-type smoke

# 并行执行
python run_tests.py --parallel --workers 4 --test-type regression

# 生成并查看Allure报告
python run_tests.py --test-type smoke --generate-report --serve-report
```

#### 🎯 按功能模块运行

```
# 登录功能测试
python run_tests.py --test-type login

# 产品功能测试
python run_tests.py --test-type product

# 购物车功能测试
python run_tests.py --test-type cart

# 联系我们功能测试
python run_tests.py --test-type contact
```

#### 📊 直接使用Pytest

```
# 基本运行
pytest -m smoke -v

# 指定浏览器和无头模式
pytest --browser=chrome --headless -m smoke

# 并行运行
pytest -n 4 -m regression

# 生成报告
pytest --alluredir=reports/allure-results --html=reports/html/report.html
```

## 🧪 测试用例覆盖

### 🏠 首页功能
- ✅ 页面加载验证
- ✅ 导航链接功能
- ✅ 产品展示
- ✅ 分类筛选
- ✅ 品牌筛选
- ✅ 邮件订阅
- ✅ 响应式布局

### 👤 用户认证
- ✅ 用户注册流程
- ✅ 用户登录功能
- ✅ 表单验证
- ✅ 错误处理
- ✅ 安全测试

### 🛍️ 产品功能
- ✅ 产品列表展示
- ✅ 产品搜索
- ✅ 产品详情查看
- ✅ 分类筛选
- ✅ 品牌筛选

### 🛒 购物车功能
- ✅ 添加商品到购物车
- ✅ 删除购物车商品
- ✅ 更新商品数量
- ✅ 购物车信息验证
- ✅ 结账流程

### 📞 联系我们
- ✅ 联系表单提交
- ✅ 表单验证
- ✅ 文件上传
- ✅ 错误处理

## 📊 测试报告

### Allure报告特性
- 📈 测试执行统计
- 📋 详细的测试步骤
- 📸 失败时自动截图
- 🏷️ 测试分类和标记
- 📝 测试历史趋势
- 🔍 错误分析

### 查看报告

```
# 生成Allure报告
allure generate reports/allure-results -o reports/allure-reports --clean

# 启动报告服务器
allure serve reports/allure-results
```

## ⚙️ 配置说明

### 浏览器配置 (`config/config.yaml`)
```
browser:
  default: "chrome"
  headless: false
  window_size: "1920,1080"
  implicit_wait: 10
  explicit_wait: 15
```

### 环境变量 (`.env`)
```
BASE_URL=https://automationexercise.com
BROWSER=chrome
HEADLESS=false
LOG_LEVEL=INFO
```

### Pytest配置 (`pytest.ini`)
```
[tool:pytest]
markers =
    smoke: 冒烟测试
    regression: 回归测试
    login: 登录相关测试
    product: 产品相关测试
```

## 🔧 开发指南

### 添加新的测试用例

1. **创建页面对象** (如果需要)
```
# pages/new_page.py
from pages.base_page import BasePage

class NewPage(BasePage):
    ELEMENT_LOCATOR = (By.ID, "element-id")

    def perform_action(self):
        self.click_element(self.ELEMENT_LOCATOR)
```

2. **编写测试用例**
```
# tests/test_new_feature.py
import pytest
import allure
from tests.base_test import BaseTest

@allure.feature("新功能")
class TestNewFeature(BaseTest):

    @allure.story("功能测试")
    @pytest.mark.smoke
    def test_new_functionality(self):
        # 测试实现
        pass
```

### 添加测试数据

```
# data/new_data.json
{
  "test_data": {
    "field1": "value1",
    "field2": "value2"
  }
}
```

### 工具类使用

```
# 使用配置管理器
from utils.config_manager import ConfigManager
config = ConfigManager()
base_url = config.base_url

# 使用日志记录器
from utils.logger import log
log.step("测试步骤描述")
log.info("信息日志")

# 使用数据管理器
from utils.data_manager import DataManager
data_manager = DataManager(config)
user_data = data_manager.generate_test_user()
```

## 🎛️ CI/CD集成

### GitHub Actions

项目包含完整的GitHub Actions配置：

- 🔄 **自动触发**: Push、PR、定时任务
- 🌐 **多浏览器**: Chrome、Firefox并行测试
- 📊 **报告发布**: 自动生成并发布Allure报告
- 📢 **通知集成**: Slack通知支持
- 🚀 **部署集成**: GitHub Pages报告发布

### 手动触发

可以通过GitHub Actions界面手动触发测试，选择：
- 测试套件：smoke/regression/all
- 浏览器：chrome/firefox/edge

## 📈 性能监控

### 性能测试
- 页面加载时间监控
- 操作响应时间测试
- 资源使用监控

### 运行性能测试
```bash
pytest -m slow --browser=chrome --headless
```

## 🔒 安全测试

项目包含基础安全测试：
- XSS攻击防护测试
- SQL注入防护测试
- 表单验证安全性

## 🐛 调试指南

### 调试失败的测试

1. **查看截图**: `reports/screenshots/`
2. **查看日志**: `reports/logs/automation.log`
3. **查看HTML报告**: `reports/html/report.html`

### 常见问题

**问题**: 元素找不到
```
# 解决方案：增加等待时间或更新定位器
```

**问题**: 浏览器启动失败
```
# 解决方案：检查浏览器安装和WebDriver版本
```

**问题**: 测试超时
```
# 解决方案：检查网络连接或增加超时时间
```

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request


## 🙏 致谢

感谢以下开源项目：
- [Selenium WebDriver](https://selenium.dev/)
- [Pytest](https://pytest.org/)
- [Allure Framework](https://allure.qatools.ru/)
- [AutomationExercise](https://automationexercise.com/)

---

⭐ 如果这个项目对您有帮助，请给个Star支持一下！
