#!/usr/bin/env python3
"""
测试运行脚本
提供便捷的测试执行接口
"""
import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path


class TestRunner:
    """测试运行器"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.reports_dir = self.project_root / "reports"

    def setup_environment(self):
        """设置测试环境"""
        print("📋 设置测试环境...")

        # 创建报告目录
        directories = [
            "reports/allure-results",
            "reports/allure-reports",
            "reports/html",
            "reports/screenshots",
            "reports/logs"
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ 创建目录: {directory}")

    def clean_reports(self):
        """清理旧的报告"""
        print("🧹 清理旧报告...")

        if self.reports_dir.exists():
            shutil.rmtree(self.reports_dir)
            print("✅ 已清理旧报告")

        self.setup_environment()

    def run_tests(self, test_type="smoke", browser="chrome", headless=True,
                  parallel=False, workers=2, markers=None, collect_only=False):
        """
        运行测试

        Args:
            test_type: 测试类型 (smoke, regression, all)
            browser: 浏览器类型
            headless: 是否无头模式
            parallel: 是否并行运行
            workers: 并行工作进程数
            markers: 自定义标记
            collect_only: 只收集测试，不执行
        """
        print(f"🚀 开始运行{test_type}测试...")

        # 构建pytest命令 - 使用当前Python解释器
        cmd = [sys.executable, "-m", "pytest"]

        # 测试标记
        if test_type == "smoke":
            cmd.extend(["-m", "smoke"])
        elif test_type == "regression":
            cmd.extend(["-m", "regression"])
        elif test_type == "login":
            cmd.extend(["-m", "login"])
        elif test_type == "product":
            cmd.extend(["-m", "product"])
        elif test_type == "cart":
            cmd.extend(["-m", "cart"])
        elif test_type == "contact":
            cmd.extend(["-m", "contact"])
        elif markers:
            cmd.extend(["-m", markers])

        # 浏览器配置
        cmd.extend([f"--browser={browser}"])

        if headless:
            cmd.append("--headless")

        # 并行执行
        if parallel:
            cmd.extend(["-n", str(workers)])

        # 报告配置
        cmd.extend([
            "--alluredir=reports/allure-results",
            "--html=reports/html/report.html",
            "--self-contained-html",
            "-v"
        ])

        # 其他选项
        if collect_only:
            cmd.append("--collect-only")

        # 添加重试
        cmd.extend(["--reruns", "2", "--reruns-delay", "3"])

        print(f"执行命令: {' '.join(cmd)}")

        # 执行测试
        try:
            result = subprocess.run(cmd, cwd=self.project_root, check=False)
            return result.returncode == 0
        except Exception as e:
            print(f"❌ 测试执行失败: {str(e)}")
            return False

    def generate_allure_report(self, serve=False):
        """生成Allure报告"""
        print("📊 生成Allure报告...")

        allure_results = self.project_root / "reports" / "allure-results"
        allure_reports = self.project_root / "reports" / "allure-reports"

        if not allure_results.exists() or not any(allure_results.iterdir()):
            print("❌ 没有找到测试结果文件")
            return False

        try:
            # 生成报告
            cmd = ["allure", "generate", str(allure_results), "-o", str(allure_reports), "--clean"]
            subprocess.run(cmd, check=True)
            print("✅ Allure报告生成成功")

            if serve:
                # 启动报告服务器
                print("🌐 启动Allure报告服务器...")
                subprocess.run(["allure", "serve", str(allure_results)])

            return True

        except subprocess.CalledProcessError:
            print("❌ Allure报告生成失败，请确保已安装Allure")
            return False
        except Exception as e:
            print(f"❌ 报告生成出错: {str(e)}")
            return False

    def check_dependencies(self):
        """检查依赖"""
        print("🔍 检查依赖...")

        # 检查Python包
        try:
            import pytest
            import selenium
            import allure
            print("✅ Python依赖检查通过")
        except ImportError as e:
            print(f"❌ 缺少Python依赖: {e}")
            print("请运行: pip install -r requirements.txt")
            return False

        # 检查Allure
        try:
            subprocess.run(["allure", "--version"], capture_output=True, check=True)
            print("✅ Allure已安装")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  Allure未安装，报告生成功能不可用")

        return True

    def run_data_setup(self):
        """设置测试数据"""
        print("📋 设置测试数据...")

        try:
            from utils.data_manager import DataManager
            from utils.config_manager import ConfigManager

            config = ConfigManager()
            data_manager = DataManager(config)
            data_manager.create_test_data_template()

            print("✅ 测试数据设置完成")
            return True

        except Exception as e:
            print(f"❌ 测试数据设置失败: {str(e)}")
            return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="AutomationExercise 自动化测试运行器")

    # 基本参数
    parser.add_argument("--test-type", "-t",
                       choices=["smoke", "regression", "all", "login", "product", "cart", "contact"],
                       default="smoke",
                       help="测试类型")

    parser.add_argument("--browser", "-b",
                       choices=["chrome", "firefox", "edge"],
                       default="chrome",
                       help="浏览器类型")

    parser.add_argument("--headless",
                       action="store_true",
                       help="无头模式运行")

    parser.add_argument("--parallel", "-p",
                       action="store_true",
                       help="并行运行测试")

    parser.add_argument("--workers", "-w",
                       type=int,
                       default=2,
                       help="并行工作进程数")

    parser.add_argument("--markers", "-m",
                       help="自定义pytest标记")

    # 报告参数
    parser.add_argument("--generate-report", "-r",
                       action="store_true",
                       help="生成Allure报告")

    parser.add_argument("--serve-report", "-s",
                       action="store_true",
                       help="启动Allure报告服务器")

    # 工具参数
    parser.add_argument("--clean",
                       action="store_true",
                       help="清理旧报告")

    parser.add_argument("--setup-data",
                       action="store_true",
                       help="设置测试数据")

    parser.add_argument("--check-deps",
                       action="store_true",
                       help="检查依赖")

    parser.add_argument("--collect-only",
                       action="store_true",
                       help="只收集测试，不执行")

    args = parser.parse_args()

    runner = TestRunner()

    # 检查依赖
    if args.check_deps or not runner.check_dependencies():
        if args.check_deps:
            return
        else:
            sys.exit(1)

    # 清理报告
    if args.clean:
        runner.clean_reports()
        return

    # 设置测试数据
    if args.setup_data:
        if not runner.run_data_setup():
            sys.exit(1)
        return

    # 设置环境
    runner.setup_environment()

    # 运行测试
    success = runner.run_tests(
        test_type=args.test_type,
        browser=args.browser,
        headless=args.headless,
        parallel=args.parallel,
        workers=args.workers,
        markers=args.markers,
        collect_only=args.collect_only
    )

    # 生成报告
    if args.generate_report or args.serve_report:
        runner.generate_allure_report(serve=args.serve_report)

    # 显示结果
    if success:
        print("\n✅ 测试执行成功!")
        print(f"📊 HTML报告: {runner.project_root}/reports/html/report.html")
        if (runner.project_root / "reports" / "allure-reports").exists():
            print(f"📋 Allure报告: {runner.project_root}/reports/allure-reports/index.html")
    else:
        print("\n❌ 测试执行失败!")
        sys.exit(1)


if __name__ == "__main__":
    main()
