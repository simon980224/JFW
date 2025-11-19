import os
# import subprocess
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from colorama import init, Fore, Style
from datetime import datetime
import subprocess
import logging

# 设置日志级别为 ERROR，只显示错误信息
logging.basicConfig(level=logging.ERROR)

# 设置环境变量来禁止 TensorFlow 输出
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # '3' 代表仅输出 ERROR 级别日志

# 设置控制台输出编码为 UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# 设置CMD窗口标题
os.system("title " +  "金富翁 - 代理後台管理系統")

# 设置 CMD 窗口大小为 100 列，30 行
os.system("mode con: cols=100 lines=30")

# 执行命令获取 ChromeDriver 版本
result = subprocess.run(["chromedriver", "--version"], capture_output=True, text=True)
# 提取版本号并显示
version = result.stdout.split()[1]  # 获取第二部分，即版本号
print(f"ChromeDriver {version}")

# 确保 colorama 正常工作
init(autoreset=True)  # 初始化 colorama，确保支持 UTF-8 输出

user_account = input(Fore.LIGHTYELLOW_EX + "請輸入使用者帳號: \n" + Style.RESET_ALL)
print("")
user_password = input(Fore.LIGHTYELLOW_EX + "請輸入使用者密碼: \n" + Style.RESET_ALL)
print("")
user_code = input(Fore.LIGHTYELLOW_EX + "請輸入验证码: \n" + Style.RESET_ALL)
print("")


# 设置 Chrome WebDriver 路径
# 获取当前目录
if getattr(sys, 'frozen', False):
    current_dir = os.path.dirname(sys.executable)  # 打包后的 .exe 目录
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))  # 运行 .py 时的目录


CHROMEDRIVER_PATH = os.path.join(current_dir, "chromedriver.exe")
# 确保 ChromeDriver 文件存在
if not os.path.exists(CHROMEDRIVER_PATH):
    print(f"錯誤：找不到 {CHROMEDRIVER_PATH}，請將 chromedriver.exe 放在同目錄！")
    sys.exit(1)

service = Service(CHROMEDRIVER_PATH)
init(autoreset=True)

# 启动浏览器
driver = webdriver.Chrome(service=service)

def click_with_retry(driver, xpath, next_xpath, retries=3, delay=1):
    """
    尝试点击元素，如果下一个元素未出现则重试。
    :param driver: Selenium WebDriver 实例
    :param xpath: 要点击元素的 XPath
    :param next_xpath: 点击后预期出现元素的 XPath
    :param retries: 重试次数
    :param delay: 每次重试前的等待时间
    :return: True 表示点击成功，False 表示点击失败
    """
    for attempt in range(retries):
        try:
            # 等待可点击并点击
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            time.sleep(0.5)
            element.click()

            # 检查下一个元素是否出现
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, next_xpath)))
            return True
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print(f"点击失败：{xpath}，错误信息：{e}")
                return False

def wait_for_scroll_end(driver, timeout=10, interval=0.1):
    """等待滚动结束"""
    end_time = time.time() + timeout
    last_scroll_position = driver.execute_script("return window.pageYOffset;")

    while time.time() < end_time:
        time.sleep(interval)
        new_scroll_position = driver.execute_script("return window.pageYOffset;")
        if new_scroll_position == last_scroll_position:
            return True  # 滚动结束
        last_scroll_position = new_scroll_position
    return False  # 超时未结束

def log_info(message):
    print(Fore.CYAN + f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}" + Style.RESET_ALL)


def log_success(message):
    print(Fore.GREEN + f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}" + Style.RESET_ALL)


def log_warning(message):
    print(Fore.YELLOW + f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}" + Style.RESET_ALL)


def log_error(message):
    print(Fore.RED + f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}" + Style.RESET_ALL)


def log_loading_light(message):
    print(Fore.LIGHTBLUE_EX + f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}" + Style.RESET_ALL)


def log_important(message):
    print(Fore.LIGHTGREEN_EX + f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}" + Style.RESET_ALL)

def wait_for_element(driver, xpath, timeout=20, retries=3):
    """等待元素可见并可点击，支持重试"""
    for i in range(retries):
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            return element  # 找到元素后立即返回
        except Exception as e:
            print(f"尝试 {i+1}/{retries} 失败，错误：{e}")
            time.sleep(2)  # 等待2秒后重试
    raise Exception(f"元素 {xpath} 在 {retries} 次尝试后仍未找到！")

# 访问目标网站并最大化窗口
driver.get("https://ad.jfw-win.com/#/agent-login")
driver.maximize_window()
loading_xpath = "/html/body/div[2]/div/p"
loading_xpath2 = "/html/body/div[2]/div/i"

# 等待用户名、密码、验证码输入框可见且可点击
username = WebDriverWait(driver, 180).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/form/div[2]/div[2]/div/div/input'))
)
username.click()
time.sleep(0.5)  # 稍微等待
username.clear()
username.send_keys(user_account)


password = WebDriverWait(driver, 180).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/form/div[2]/div[4]/div/div[1]/input'))
)
password.click()
time.sleep(0.5)  # 稍微等待
password.clear()
password.send_keys(user_password)

code = WebDriverWait(driver, 180).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/form/div[2]/div[6]/div/div/input'))
)
code.click()
time.sleep(0.5)  # 稍微等待
code.clear()
code.send_keys(user_code)

login = WebDriverWait(driver, 180).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/form/div[2]/button'))
)
login.click()
time.sleep(0.5)  # 稍微等待



# 清空输入框，填写账号、密码、验证码并点击登录
from selenium.common.exceptions import StaleElementReferenceException

wait = WebDriverWait(driver, 10)

def safe_click(by, locator, retries=3):
    """ 封装点击操作，自动重试避免 stale element 错误 """
    for attempt in range(retries):
        try:
            element = wait.until(EC.element_to_be_clickable((by, locator)))
            driver.execute_script("arguments[0].scrollIntoView(true);", element)  # 滚动到元素位置
            element.click()
            return True
        except StaleElementReferenceException:
            print(f"⚠️ 第 {attempt+1} 次尝试点击失败，重新查找元素...")
    print("❌ 无法点击元素，请检查网页状态。")
    return False

# 输入账号密码验证码
log_loading_light("登入中...\n")

# username.send_keys("qaqa50")
# password.send_keys("aaaa1111")
# code.send_keys("b48x2")

# 读取中
time.sleep(5)

# 登入成功，直接跳转到账户管理页面
driver.get("https://ad.jfw-win.com/#/agent/user-manage/agent-user")

# 等待页面加载完成
WebDriverWait(driver, 180).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="app"]'))
)

time.sleep(1)

#读取中
WebDriverWait(driver, 180).until_not(
    EC.presence_of_element_located((By.XPATH, loading_xpath))
)

WebDriverWait(driver, 180).until_not(
    EC.presence_of_element_located((By.XPATH, loading_xpath2))
)

#代理账号
player_list = WebDriverWait(driver, 180).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div[1]/div/div[3]/div[1]/div/ul/div[3]/li/ul/div[1]/a/li'))
)
log_loading_light("點選[代理帳號]")
time.sleep(1)
player_list.click()

time.sleep(1)
#读取中
WebDriverWait(driver, 180).until(
    EC.invisibility_of_element_located((By.XPATH, loading_xpath))
)
WebDriverWait(driver, 180).until(
    EC.invisibility_of_element_located((By.XPATH, loading_xpath2))
)

time.sleep(1)

# 直属玩家  等待元素可见
element = WebDriverWait(driver, 180).until(
    EC.visibility_of_element_located((By.XPATH, '//div[@role="tablist"]//div[@id="tab-gameUser"]'))
)

#直属玩家  再次等待元素可点击
player = WebDriverWait(driver, 180).until(
    EC.element_to_be_clickable((By.XPATH, '//div[@role="tablist"]//div[@id="tab-gameUser"]'))
)
time.sleep(1)
log_loading_light("點選[直屬玩家]\n")
player.click()

# 等待 "数据加载中" 消失
WebDriverWait(driver, 180).until_not(
    EC.presence_of_element_located((By.XPATH, loading_xpath))
)

#确保直属玩家真的读取完毕
#使用 换页三角形为参考标的
WebDriverWait(driver, 180).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="app-main"]/section/footer/div[2]/div/span[2]/div/div/span/span/i'))
            )

time.sleep(1)


num_space = True
while num_space:
    user_input = input(Fore.LIGHTYELLOW_EX + "請輸入目標金額: \n" + Style.RESET_ALL)
    if user_input.isdigit():  # 检查输入是否为数字
        num = int(user_input)  # 转换为整数
        num_space = False  # 如果输入有效，退出循环
    else:
        print("")
        print(Fore.RED + "輸入無效，請確保輸入的是數字！\n" + Style.RESET_ALL)

deep = True
while deep:
    print("")
    print(Fore.MAGENTA + "腳本開始執行!\n" + Style.RESET_ALL)
    log_loading_light("重新整理页面\n")


    def set_page_size_to_500(driver):
        """切换到 500 条/页"""
        try:
            log_info("目前頁面會員均已符合條件")
            log_info("切換至 500條/頁 檢查")
            page_dropdown = WebDriverWait(driver, 180).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="app-main"]/section/footer/div[2]/div/span[2]/div/div/span/span/i'))
            )
            time.sleep(1)
            page_dropdown.click()

            page_option_500 = WebDriverWait(driver, 180).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[1]/div[1]/ul/li[5]/span'))
            )
            time.sleep(1)
            page_option_500.click()
            time.sleep(2)  # 等待页面刷新
            log_info("已切换至 500 条/页")

        except Exception as e:
            log_error(f"切换至 500 条/页失败: {e}")


    page_size_50_checked = False  # 是否已检查 50 条/页
    switching_to_500 = False  # 是否已经切换到 500 条/页
    all_members_checked = False  # 标记是否所有会员已检查

    # **第一次进入直属玩家**
    player = WebDriverWait(driver, 180).until(
        EC.element_to_be_clickable((By.XPATH, '//div[@role="tablist"]//div[@id="tab-gameUser"]'))
    )
    time.sleep(1)
    player.click()

    while not all_members_checked:
        try:
            # **等待 "数据加载中" 消失**
            WebDriverWait(driver, 180).until_not(
                EC.presence_of_element_located((By.XPATH, loading_xpath))
            )

            log_loading_light("正在取得會員帳號\n")
            time.sleep(1)

            # **获取所有会员账号和按钮**
            accounts = WebDriverWait(driver, 180).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//*[@id="app-main"]/section/main/div[4]/div[2]/div/div/div[1]/div[1]/div[2]/div[2]'))
            )

            # **获取所有详情按钮**
            buttons = WebDriverWait(driver, 180).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//*[@id='agent-bbox-id']/div[2]/div/div/div[1]/div[3]"))
            )


            # **如果没有会员，结束循环**
            if not accounts or not buttons:
                log_success("所有會員上分任務完成！\n")
                break

            processed = False  # 确保循环至少遍历一次
            skipped_accounts = set()

            for idx, (account, button) in enumerate(zip(accounts, buttons), start=1):
                try:
                    account_name = account.text.strip()

                    # **获取代理类型**
                    agent_type_xpath = f'//*[@id="agent-bbox-id"]/div[2]/div/div[{idx}]/div[1]/div[2]/div[1]/div[2]'
                    agent_type_element = WebDriverWait(driver, 180).until(
                        EC.presence_of_element_located((By.XPATH, agent_type_xpath))
                    )
                    agent_type = agent_type_element.text.strip()

                    # **如果是"信用代理"，跳过该账号**

                    if agent_type == "信用代理":
                        if account_name not in skipped_accounts:

                            #不告知跳過:帳號: （類型：『信用代理』）
                            # log_error(f"跳過帳號:{account_name} （類型：『信用代理』）\n")

                            skipped_accounts.add(account_name)
                        continue

                    balance_xpath = f'//*[@id="agent-bbox-id"]/div[2]/div/div[{idx}]/div[1]/div[2]/div[5]/div[2]'
                    balance_element = WebDriverWait(driver, 180).until(
                        EC.presence_of_element_located((By.XPATH, balance_xpath))
                    )
                    member_balance = int(float(balance_element.text.replace(",", "")))

                    # **如果余额符合目标，不打印日志**
                    if member_balance == num:
                        skipped_accounts.add(account_name)  # 用 add() 代替 append()
                        continue

                    # **只有需要处理的会员才打印日志**
                    log_info(f"{account_name}，類型：『現金代理』，餘額: {member_balance}，開始處理")

                    # **处理上分**
                    if member_balance < num:
                        log_info(f"餘額：{member_balance} ，低於目標金額： {num} ，準備上分...")

                        # **滚动到按钮**
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                        if wait_for_scroll_end(driver):
                            time.sleep(2)  # 可选的小延迟，确保元素稳定
                            button.click()
                            log_info("準備上分")
                        else:
                            log_info("滾動超時未結束")
                        time.sleep(3)

                        # 使用 click_with_retry 函数进行点击
                        if click_with_retry(driver,
                                            '//*[@id="app-main"]/section/main/div[2]/div[1]/div[2]/div[6]/div[5]/div/button[3]',
                                            '/html/body/div[2]/div/div[2]/div[1]/div/div[3]/div[2]'):
                            log_info("点击额度设定成功")
                        else:
                            log_warning("点击额度设定失败，已尝试多次")

                        if click_with_retry(driver, '/html/body/div[2]/div/div[2]/div[1]/div/div[3]/div[2]',
                                            '//*[@id="app-main"]/section/main/div[2]/div[2]/div[1]/div/div[2]/div[3]/div[3]/div[2]/input'):
                            log_info("点击点数分配成功")
                        else:
                            log_warning("点击点数分配失败，已尝试多次")

                        # **调整余额**
                        try:
                            adjust = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH,
                                                            '//*[@id="app-main"]/section/main/div[2]/div[2]/div[1]/div/div[2]/div[3]/div[3]/div[2]/input'))
                            )
                            time.sleep(0.2)
                            adjust.clear()
                            time.sleep(0.2)
                            adjust.send_keys(str(num - member_balance))
                            time.sleep(0.2)
                        except Exception as e:
                            log_warning(f"调整余额失败：{e}")

                        # **确认补分**
                        if click_with_retry(driver,
                                            '//*[@id="app-main"]/section/main/div[2]/div[2]/div[1]/div/div[2]/div[3]/div[5]/div[2]',
                                            '//*[@id="app-main"]/section/main/div[2]/div[1]/div[2]'):
                            log_warning(f"{account_name} ，上分成功\n")
                        else:
                            log_warning(f"{account_name} ，上分失败，已尝试多次")







                        # **等待 "数据加载中" 消失**
                        WebDriverWait(driver, 180).until_not(
                            EC.presence_of_element_located((By.XPATH, loading_xpath))
                        )
                        time.sleep(2)

                        # **返回会员列表**
                        log_important("返回代理帳號")
                        driver.get("https://ad.jfw-win.com/#/agent/user-manage/agent-user")

                        time.sleep(2.5)

                        # **点击 "直属玩家" 重新加载页面**
                        log_important("跳轉[直屬玩家]頁面\n")

                        # 设定点击尝试的次数
                        max_attempts = 3
                        attempt = 0
                        clicked = False

                        while attempt < max_attempts and not clicked:
                            try:
                                player = WebDriverWait(driver, 180).until(
                                    EC.element_to_be_clickable(
                                        (By.XPATH, '//div[@role="tablist"]//div[@id="tab-gameUser"]'))
                                )
                                time.sleep(1)
                                player.click()
                                clicked = True  # 如果点击成功，则设置为True，跳出循环
                            except Exception as e:
                                attempt += 1
                                log_important(f"点击直属玩家失败，尝试 {attempt} 次")
                                if attempt < max_attempts:
                                    time.sleep(2)  # 等待2秒后再尝试
                                else:
                                    log_important("点击直属玩家失败，已达最大重试次数。")

                        # 确保直属玩家真的读取完毕
                        # 使用换页三角形为参考标的
                        WebDriverWait(driver, 180).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, '//*[@id="app-main"]/section/footer/div[2]/div/span[2]/div/div/span/span/i'))
                        )
                        time.sleep(1)

                        # **返回会员列表后，重新切换到 500 条/页**
                        if switching_to_500:
                            set_page_size_to_500(driver)

                        processed = True
                        break



                    #**处理扣分**
                    if member_balance > num:
                        log_info(f"{account_name} 餘額 {member_balance} 大於 {num}，準備扣分")

                        # **滚动到按钮**
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                        if wait_for_scroll_end(driver):
                            time.sleep(2)  # 可选的小延迟，确保元素稳定
                            button.click()
                            log_info("準備扣除")
                        else:
                            log_info("滾動超時未結束")

                        time.sleep(3)

                        # **点击额度设定**
                        if click_with_retry(driver,
                                            '//*[@id="app-main"]/section/main/div[2]/div[1]/div[2]/div[6]/div[5]/div/button[3]',
                                            '/html/body/div[2]/div/div[2]/div[1]/div/div[3]/div[2]'):
                            log_info("点击额度设定成功")
                        else:
                            log_warning("点击额度设定失败")

                        time.sleep(1)

                        # **点击点数分配**
                        if click_with_retry(driver, '/html/body/div[2]/div/div[2]/div[1]/div/div[3]/div[2]',
                                            '//*[@id="app-main"]/section/main/div[2]/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[2]/label[2]/span[1]/span'):
                            log_info("点击点数分配成功")
                        else:
                            log_warning("点击点数分配失败")

                        time.sleep(1)

                        # **点击减少余额**
                        if click_with_retry(driver,
                                            '//*[@id="app-main"]/section/main/div[2]/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[2]/label[2]/span[1]/span',
                                            '//*[@id="app-main"]/section/main/div[2]/div[2]/div[1]/div/div[2]/div[3]/div[3]/div[2]/input'):
                            log_info("点击减少余额成功")
                        else:
                            log_warning("点击减少余额失败")

                        time.sleep(1)

                        # **调整余额**
                        try:
                            adjust = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH,
                                                            '//*[@id="app-main"]/section/main/div[2]/div[2]/div[1]/div/div[2]/div[3]/div[3]/div[2]/input'))
                            )
                            time.sleep(0.2)
                            adjust.clear()
                            time.sleep(0.2)
                            adjust.send_keys(str(member_balance - num))
                            log_info("调整余额成功")
                        except Exception as e:
                            log_warning(f"调整余额失败: {e}")

                        time.sleep(0.2)

                        # **确认补分**
                        if click_with_retry(driver,
                                            '//*[@id="app-main"]/section/main/div[2]/div[2]/div[1]/div/div[2]/div[3]/div[5]/div[2]',
                                            '//*[@id="app-main"]/section/main/div[2]/div[1]/div[2]'):
                            log_warning(f"{account_name} 扣分成功\n")
                        else:
                            log_warning(f"{account_name} 扣分失败")

                        # **等待 "数据加载中" 消失**
                        WebDriverWait(driver, 180).until_not(
                            EC.presence_of_element_located((By.XPATH, loading_xpath))
                        )
                        time.sleep(2)

                        # **返回会员列表**
                        log_important("返回代理帳號")
                        driver.get("https://ad.jfw-win.com/#/agent/user-manage/agent-user")

                        time.sleep(2.5)

                        # **点击 "直属玩家" 重新加载页面**
                        log_important("跳轉[直屬玩家]頁面\n")

                        # 设定点击尝试的次数
                        max_attempts = 3
                        attempt = 0
                        clicked = False

                        while attempt < max_attempts and not clicked:
                            try:
                                player = WebDriverWait(driver, 180).until(
                                    EC.element_to_be_clickable(
                                        (By.XPATH, '//div[@role="tablist"]//div[@id="tab-gameUser"]'))
                                )
                                time.sleep(1)
                                player.click()
                                clicked = True  # 如果点击成功，则设置为True，跳出循环
                            except Exception as e:
                                attempt += 1
                                log_important(f"点击直属玩家失败，尝试 {attempt} 次")
                                if attempt < max_attempts:
                                    time.sleep(2)  # 等待2秒后再尝试
                                else:
                                    log_important("点击直属玩家失败，已达最大重试次数。")

                        # 确保直属玩家真的读取完毕
                        # 使用换页三角形为参考标的
                        WebDriverWait(driver, 180).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, '//*[@id="app-main"]/section/footer/div[2]/div/span[2]/div/div/span/span/i'))
                        )
                        time.sleep(1)

                        # **返回会员列表后，重新切换到 500 条/页**
                        if switching_to_500:
                            set_page_size_to_500(driver)

                        processed = True
                        break

                except Exception as e:
                    log_error(f"{account_name} 處理失敗: {e}")
                    continue

            if not processed:
                if not page_size_50_checked:
                    set_page_size_to_500(driver)
                    page_size_50_checked = True
                    switching_to_500 = True
                    continue
                elif switching_to_500:
                    log_success("所有直屬會員已檢查完畢，無需繼續補/扣分。\n")
                    all_members_checked = True
                else:
                    log_success("所有直屬會員餘額均符合要求，無需補/扣分。\n")
                    all_members_checked = True

        except Exception as e:
            log_error(f"發生錯誤: {e}")
            break

    print("\033[1;33m所有會員任務完成！\033[0m")
    print("\033[1;33m輸入任意鍵退出\033[0m")
    req = input("\033[1;33m或按下 ENTER 鍵 繼續使用\033[0m\n")
    if req == "":
        deep = True
        # 设置目标金额

        num_space = True
        while num_space:
            user_input = input(Fore.LIGHTYELLOW_EX + "請輸入目標金額: \n" + Style.RESET_ALL)
            if user_input.isdigit():  # 检查输入是否为数字
                num = int(user_input)  # 转换为整数
                num_space = False  # 如果输入有效，退出循环
            else:
                print("")
                print(Fore.RED + "輸入無效，請確保輸入的是數字！\n" + Style.RESET_ALL)

    else:
        deep = False
        print("\033[1;33m準備退出腳本\033[0m")
        time.sleep(2)
        sys.exit() #终止程序
