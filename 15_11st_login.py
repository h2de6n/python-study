import time
import random
import sys
import pyautogui
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# 1. 브라우저 설정 및 드라이버 초기화 함수
def init_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging", "enable-automation"]
    )
    chrome_options.add_experimental_option("useAutomationExtension", False)

    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 매크로 감지 우회 스크립트
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        },
    )
    driver.implicitly_wait(5)
    return driver


# 2. 네이버 계정 정보 입력 함수
def input_naver_credentials(driver, user_id, user_pw):
    # 아이디 입력
    el_id = driver.find_element(By.CSS_SELECTOR, "#id")
    el_id.click()
    time.sleep(random.uniform(1, 2))
    pyperclip.copy(user_id)
    pyautogui.hotkey("command", "v")

    # 비밀번호 입력
    el_pw = driver.find_element(By.CSS_SELECTOR, "#pw")
    el_pw.click()
    time.sleep(random.uniform(1, 2))
    pyperclip.copy(user_pw)
    pyautogui.hotkey("command", "v")

    # 로그인 버튼 클릭
    driver.find_element(By.CSS_SELECTOR, r"#log\.login").click()
    time.sleep(2)


# 3. 로그인 결과 확인 및 사후 처리 함수
def handle_login_process(driver):
    # 실패 메시지 체크
    error_elements = driver.find_elements(By.CSS_SELECTOR, "#err_common > div")
    if error_elements and error_elements[0].is_displayed():
        print(f"로그인 실패: {error_elements[0].text}")
        driver.quit()
        sys.exit()

    print("스마트폰으로 2단계 인증 완료해주세요.")
    wait = WebDriverWait(driver, 60)

    try:
        # 상태 유지 팝업 처리
        try:
            later_btn = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "#arModalLoginNudge > div > div > div.c-buttons > a",
                    )
                )
            )
            later_btn.click()
            print("팝업창을 닫았습니다.")
        except:
            print("상태 유지 팝업이 뜨지 않았습니다.")

        # 최종 성공 확인
        success_el = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.login_info strong"))
        )
        print(f"반갑습니다! [{success_el.text}] 확인되었습니다.")

    except Exception as e:
        print(f"인증 과정 오류: {e}")
        driver.quit()
        sys.exit()


# --- 메인 실행 로직 ---
if __name__ == "__main__":
    LOGIN_URL = "https://login.11st.co.kr/auth/v2/login?isPopup=false&adultLoginRequired=N&isNonMemberBuy=false&_ds=rdflt1767354189660&returnURL=https%3A%2F%2Fwww.11st.co.kr%2F"  # 기존 URL 넣으세요
    USER_ID = "아이디"
    USER_PW = "비밀번호"

    browser = init_driver()
    browser.get(LOGIN_URL)

    # 네이버 로그인 버튼 클릭
    browser.find_element(By.CSS_SELECTOR, "img[alt='네이버']").click()

    # 로그인 절차 진행
    input_naver_credentials(browser, USER_ID, USER_PW)
    handle_login_process(browser)

    print("모든 로그인 절차가 끝났습니다. 브라우저를 조작하세요.")
