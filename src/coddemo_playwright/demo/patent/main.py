import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright


load_dotenv()
username = os.getenv("PATENT_USERNAME")
password = os.getenv("PATENT_PASSWORD")


def main():
    # 输出环境变量
    print(f"Username = {username}, Password = {password}")
    if username is None or password is None:
        print("请在 .env 文件中设置 PATENT_USERNAME 和 PATENT_PASSWORD 环境变量")
        return

    # 开始
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False)

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

        # todo 通过滑动验证码

        # 关闭浏览器
        browser.close()


if __name__ == "__main__":
    main()
