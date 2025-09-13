#!/usr/bin/env python3
"""
ChromeDriver修复脚本
用于解决ChromeDriver下载和安装问题
"""
import os
import shutil
from pathlib import Path
from webdriver_manager.chrome import ChromeDriverManager


def clear_webdriver_cache():
    """清理webdriver-manager缓存"""
    cache_dirs = [
        os.path.expanduser("~/.wdm"),
        os.path.expanduser("~/.cache/selenium"),
        Path.home() / ".wdm"
    ]

    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            try:
                shutil.rmtree(cache_dir)
                print(f"✅ 已清理缓存目录: {cache_dir}")
            except Exception as e:
                print(f"❌ 清理缓存失败 {cache_dir}: {e}")


def reinstall_chromedriver():
    """重新安装ChromeDriver"""
    try:
        print("🔄 重新下载ChromeDriver...")
        manager = ChromeDriverManager()
        driver_path = manager.install()
        print(f"✅ ChromeDriver安装成功: {driver_path}")

        # 验证文件存在且可执行
        if os.path.exists(driver_path):
            file_size = os.path.getsize(driver_path)
            print(f"📁 文件大小: {file_size} bytes")

            if driver_path.endswith('.exe') and file_size > 1000:
                print("✅ ChromeDriver验证通过")
                return True
            else:
                print("❌ ChromeDriver文件异常")
                return False
        else:
            print("❌ ChromeDriver文件不存在")
            return False

    except Exception as e:
        print(f"❌ ChromeDriver安装失败: {e}")
        return False


def check_chrome_browser():
    """检查Chrome浏览器是否安装"""
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]

    for chrome_path in chrome_paths:
        if os.path.exists(chrome_path):
            print(f"✅ 找到Chrome浏览器: {chrome_path}")
            return True

    print("❌ 未找到Chrome浏览器，请先安装Chrome")
    return False


def main():
    """主函数"""
    print("🔧 ChromeDriver修复工具")
    print("=" * 50)

    # 检查Chrome浏览器
    if not check_chrome_browser():
        print("\n请先安装Chrome浏览器:")
        print("https://www.google.com/chrome/")
        return

    # 清理缓存
    print("\n🧹 清理webdriver-manager缓存...")
    clear_webdriver_cache()

    # 重新安装ChromeDriver
    print("\n📥 重新安装ChromeDriver...")
    if reinstall_chromedriver():
        print("\n✅ 修复完成！现在可以重新运行测试:")
        print("python run_tests.py --test-type smoke")
    else:
        print("\n❌ 修复失败，请尝试手动解决:")
        print("1. 确保Chrome浏览器已安装")
        print("2. 检查网络连接")
        print("3. 尝试使用代理或VPN")


if __name__ == "__main__":
    main()
