import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()
username = os.getenv("PATENT_USERNAME")
password = os.getenv("PATENT_PASSWORD")


def patent():
    # 输出环境变量
    print(f"Username = {username}, Password = {password}")
    if username is None or password is None:
        print("请在 .env 文件中设置 PATENT_USERNAME 和 PATENT_PASSWORD 环境变量")
        return

    # 开始
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']  # 隐藏自动化特征，让网站以为手动打开的浏览器
        )

        # 当前的浏览器环境
        context = browser.new_context()

        # 创建页面
        page = browser.new_page()

        # 进入页面
        page.goto("https://tysf.cponline.cnipa.gov.cn/am/#/user/login")

        # 选择自然人登陆
        page.get_by_role("radio", name="自然人登录").click()

        # 输入账号与密码
        page.get_by_placeholder("手机号/证件号码").fill(username)
        page.get_by_placeholder("密码").fill(password)

        # 点击登陆
        page.get_by_role("button", name="登录").click()

        # todo 先等待手动滑动验证码
        page.wait_for_timeout(30_000)

        # 等待进入门户首页
        page.wait_for_url("https://tysfjk.cponline.cnipa.gov.cn/portal/#/home/welcome", timeout=30_000)

        # 点击返回系统（右上角）
        page.get_by_text("返回系统").click()

        # 等待进入官网首页
        page.wait_for_url("https://cponline.cnipa.gov.cn/", timeout=30_000)

        # 盘旋专利审查信息查询
        page.get_by_text("专利审查信息查询", exact=True).first.hover(force=True)

        with context.expect_page() as new_page_info:
            # 点击专利检索及分析
            page.get_by_text("专利检索及分析", exact=True).first.click()
        new_page = new_page_info.value

        # 等待进入专利检索及分析的免责声明页面
        new_page.wait_for_load_state("networkidle")
        if "Disclaimer" in new_page.url:
            agree = new_page.locator('button:has-text("同意")').first
            if agree and agree.is_visible():
                agree.click()

                # 等待进入专利检索及分析页面
                new_page.wait_for_url("https://pss-system.cponline.cnipa.gov.cn/conventionalSearch", timeout=30_000)

        # 暂停
        input("...")

        # 关闭浏览器
        browser.close()


if __name__ == "__main__":
    patent()
