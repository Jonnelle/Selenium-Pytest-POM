# AutomationExercise 测试项目 Makefile

.PHONY: help install clean test smoke regression report serve-report setup check-deps

# 默认目标
help:
	@echo "AutomationExercise 自动化测试项目"
	@echo ""
	@echo "可用命令:"
	@echo "  install       - 安装项目依赖"
	@echo "  setup         - 设置测试环境和数据"
	@echo "  check-deps    - 检查依赖是否正确安装"
	@echo "  clean         - 清理测试报告"
	@echo ""
	@echo "测试执行:"
	@echo "  smoke         - 运行冒烟测试"
	@echo "  regression    - 运行回归测试"
	@echo "  test          - 运行所有测试"
	@echo "  login         - 运行登录功能测试"
	@echo "  product       - 运行产品功能测试"
	@echo "  cart          - 运行购物车功能测试"
	@echo "  contact       - 运行联系我们功能测试"
	@echo ""
	@echo "报告相关:"
	@echo "  report        - 生成Allure报告"
	@echo "  serve-report  - 启动Allure报告服务器"
	@echo ""
	@echo "高级选项:"
	@echo "  test-parallel - 并行运行测试"
	@echo "  test-headless - 无头模式运行测试"
	@echo "  test-firefox  - 使用Firefox运行测试"

# 安装依赖
install:
	@echo "📦 安装项目依赖..."
	pip install -r requirements.txt
	@echo "✅ 依赖安装完成"

# 设置环境
setup: install
	@echo "🔧 设置测试环境..."
	python run_tests.py --setup-data
	@echo "✅ 环境设置完成"

# 检查依赖
check-deps:
	@echo "🔍 检查依赖..."
	python run_tests.py --check-deps

# 清理报告
clean:
	@echo "🧹 清理测试报告..."
	python run_tests.py --clean
	@echo "✅ 清理完成"

# 冒烟测试
smoke:
	@echo "🔥 运行冒烟测试..."
	python run_tests.py --test-type smoke --generate-report

# 回归测试
regression:
	@echo "🔄 运行回归测试..."
	python run_tests.py --test-type regression --generate-report

# 所有测试
test:
	@echo "🚀 运行所有测试..."
	python run_tests.py --test-type all --generate-report

# 登录功能测试
login:
	@echo "👤 运行登录功能测试..."
	python run_tests.py --test-type login --generate-report

# 产品功能测试
product:
	@echo "🛍️ 运行产品功能测试..."
	python run_tests.py --test-type product --generate-report

# 购物车功能测试
cart:
	@echo "🛒 运行购物车功能测试..."
	python run_tests.py --test-type cart --generate-report

# 联系我们功能测试
contact:
	@echo "📞 运行联系我们功能测试..."
	python run_tests.py --test-type contact --generate-report

# 并行测试
test-parallel:
	@echo "⚡ 并行运行测试..."
	python run_tests.py --test-type regression --parallel --workers 4 --generate-report

# 无头模式测试
test-headless:
	@echo "👻 无头模式运行测试..."
	python run_tests.py --test-type smoke --headless --generate-report

# Firefox测试
test-firefox:
	@echo "🦊 使用Firefox运行测试..."
	python run_tests.py --test-type smoke --browser firefox --generate-report

# 生成报告
report:
	@echo "📊 生成Allure报告..."
	python run_tests.py --generate-report

# 启动报告服务器
serve-report:
	@echo "🌐 启动Allure报告服务器..."
	python run_tests.py --serve-report

# 开发模式运行（快速反馈）
dev:
	@echo "🔧 开发模式运行测试..."
	pytest -m smoke -v --tb=short

# 收集测试用例（不执行）
collect:
	@echo "📋 收集测试用例..."
	python run_tests.py --collect-only

# 安装开发依赖
install-dev: install
	@echo "📦 安装开发依赖..."
	pip install pytest-cov black flake8 mypy
	@echo "✅ 开发依赖安装完成"

# 代码格式化
format:
	@echo "🎨 格式化代码..."
	black .
	@echo "✅ 代码格式化完成"

# 代码检查
lint:
	@echo "🔍 代码质量检查..."
	flake8 .
	@echo "✅ 代码检查完成"

# 类型检查
typecheck:
	@echo "🔍 类型检查..."
	mypy .
	@echo "✅ 类型检查完成"

# 测试覆盖率
coverage:
	@echo "📊 运行测试覆盖率..."
	pytest --cov=pages --cov=utils --cov-report=html --cov-report=term
	@echo "✅ 覆盖率报告生成完成"

# Docker构建
docker-build:
	@echo "🐳 构建Docker镜像..."
	docker build -t automation-exercise-tests .
	@echo "✅ Docker镜像构建完成"

# Docker运行
docker-run:
	@echo "🐳 在Docker中运行测试..."
	docker run --rm -v $(PWD)/reports:/app/reports automation-exercise-tests
	@echo "✅ Docker测试完成"

# 性能测试
performance:
	@echo "⚡ 运行性能测试..."
	pytest -m slow --browser chrome --headless -v
	@echo "✅ 性能测试完成"

# 安全测试
security:
	@echo "🔒 运行安全测试..."
	pytest -k "security or xss or sql" -v
	@echo "✅ 安全测试完成"

# 生成测试报告摘要
summary:
	@echo "📋 生成测试摘要..."
	@echo "最新测试结果:"
	@ls -la reports/html/ | grep report.html || echo "没有找到HTML报告"
	@ls -la reports/allure-results/ | wc -l || echo "没有找到Allure结果"
	@echo ""
	@echo "测试用例统计:"
	@pytest --collect-only -q | grep "test session starts" -A 10 || echo "无法收集测试统计"

# 全面检查（CI模式）
ci: clean check-deps test report
	@echo "✅ CI检查完成"

# 快速验证
quick: smoke
	@echo "✅ 快速验证完成"
