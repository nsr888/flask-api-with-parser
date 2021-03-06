import os
import time
import pickle
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    InvalidCookieDomainException,
    WebDriverException,
    TimeoutException,
)
from common.get_proxy import get_free_proxy, ProxyTimeout
from common.is_timeout import is_timeout

load_dotenv()  # take environment variables from .env.


def get_ok_session(driver):
    """Read session from file or login to http://ok.ru"""
    session_file = "/tmp/session.pkl"
    if os.path.exists(session_file):
        print("Cookies file found.")
        driver.get("https://ok.ru")
        with open(session_file, "rb") as file_obj:
            cookies = pickle.load(file_obj)
            for cookie in cookies:
                if "expiry" in cookie:
                    del cookie["expiry"]
                driver.add_cookie(cookie)
        print("Cookies loaded.")
    else:
        print("Cookies file not found, will try login, please wait...")
        driver.get("https://ok.ru")

        # if os.environ["FLASK_ENV"] == "prod":
        #     with open("before_login.html", "w") as file_obj:
        #         file_obj.write(driver.page_source)

        # assert "Одноклассники" in driver.title
        elem = driver.find_element_by_name("st.email")
        elem.clear()
        elem.send_keys(os.environ["LOGIN"])
        elem = driver.find_element_by_name("st.password")
        elem.clear()
        elem.send_keys(os.environ["PASSWORD"])
        elem.send_keys(Keys.RETURN)
        with open(session_file, "wb") as file_obj:
            pickle.dump(driver.get_cookies(), file_obj)
        print("Logged in, cookies saved.")

        # if os.environ["FLASK_ENV"] == "prod":
        #     with open("after_login.html", "w") as file_obj:
        #         file_obj.write(driver.page_source)
        # if os.environ["FLASK_ENV"] == "development":
        #     time.sleep(30)


def get_ok_friends_html2(settings):
    """Get html with friends from ok.ru"""
    if settings["limit"] == 0 or settings["timeout"] == 0:
        return ""
    scroll_pause_time = 3
    page_open_pause_time = 1
    print("Proxy:", settings["proxy_str"])
    webdriver.DesiredCapabilities.CHROME["proxy"] = {
        "httpProxy": settings["proxy_str"],
        "ftpProxy": settings["proxy_str"],
        "sslProxy": settings["proxy_str"],
        "proxyType": "MANUAL",
    }
    chrome_options = Options()
    if os.environ["FLASK_ENV"] == "prod":
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1200x800")
        path_to_driver = "/usr/bin/chromedriver"
    else:
        path_to_driver = os.environ["CHROMEDRIVER"]
    with webdriver.Chrome(
        executable_path=path_to_driver, options=chrome_options
    ) as driver:
        driver.set_page_load_timeout(settings["timeout"])
        try:
            get_ok_session(driver)
        except InvalidCookieDomainException:
            print(
                "Adding cookies from file failed, remove cookies file and try again..."
            )
            os.remove("/vol-data/session.pkl")
            get_ok_session(driver)
        time.sleep(page_open_pause_time)
        print("Loading ok.ru friends page...")
        driver.get("https://ok.ru/profile/" + str(settings["id"]) + "/friends")
        print("Page loaded.")
        # assert "Татьяна Недомеркова" in driver.title
        last_elem = ""
        while True:
            element = driver.find_element_by_class_name("ugrid_cnt")
            friends_count = len(element.find_elements_by_class_name("ugrid_i"))
            print("Friends count in raw html:", friends_count)
            if friends_count > settings["limit"] or is_timeout(
                settings["start_time"], settings["timeout"]
            ):
                friends_html = element.get_attribute("innerHTML")
                break
            current_last_elem = ".ugrid_cnt > div:last-child"
            scroll = (
                "document.querySelector('" + current_last_elem + "').scrollIntoView();"
            )
            driver.execute_script(scroll)
            time.sleep(scroll_pause_time)
            if last_elem == current_last_elem:
                friends_html = driver.find_element_by_class_name(
                    "ugrid_cnt"
                ).get_attribute("innerHTML")
                break
            last_elem = current_last_elem
        # assert "No results found." not in driver.page_source
        driver.close()
    return friends_html.encode("utf-8")


def get_ok_friends_html(settings):
    if (
        os.environ["LOGIN"] == "defined in Dockerfile ARG"
        or os.environ["PASSWORD"] == "defined in Dockerfile ARG"
    ):
        print("Please provide login to http://ok.ru in ENV")
        return "Please provide login to http://ok.ru in ENV"
    while True:
        try:
            if "PROXY" in os.environ:
                settings["proxy_str"] = os.environ["PROXY"]
            else:
                settings["proxy_str"] = get_free_proxy(settings)
            # proxy_str = "52.205.44.116:8888"
            return get_ok_friends_html2(settings)
        except WebDriverException as err:
            print("Error:", err)
        except ProxyTimeout:
            return "".encode("utf-8")
        except TimeoutException:
            return "".encode("utf-8")


if __name__ == "__main__":
    args = {}
    args["id"] = 550419762162
    args["timeout"] = 120
    args["limit"] = 5
    args["proxy_string"] = get_free_proxy(args)
    html = get_ok_friends_html(args)
    with open("selenium.html", "wb") as f:
        f.write(html)
