import random
import requests
from fp.fp import FreeProxy
from common.is_timeout import is_timeout


class ProxyError(Exception):
    pass


class ProxyTimeout(Exception):
    pass


def get_random_proxy_from_file(file_str):
    """find good proxy from proxies.txt file"""

    # s = requests.session()
    proxy_set = set()

    with open(file_str, "r") as file_obj:
        file_lines = file_obj.readlines()
        for line in file_lines:
            proxy_set.add(line.strip())

    while len(proxy_set) != 0:
        try:
            random_proxy = random.choice(list(proxy_set))
            proxy = {"https": "http://" + random.choice(list(proxy_set))}
            url = "https://ok.ru"
            resp = requests.get(url, proxies=proxy, timeout=2)

            print(resp)
            if resp.status_code == 200:
                break
        except requests.exceptions.RequestException:
            print("Try next proxy...")

        proxy_set.remove(random_proxy)
        print("proxy_set len:", len(proxy_set))

    if len(proxy_set) == 0:
        print("good proxies not found in list")
        raise ProxyError("Good proxy not found")

    print("finish, good proxy: " + random_proxy)
    return random_proxy


def get_free_proxy(args):
    """get anonym RU proxy from https://www.sslproxies.org/"""
    proxy = None
    while proxy is None:
        if is_timeout(args['start_time'], args['timeout']):
            raise ProxyTimeout()
        print("Searching free proxy, please wait...")
        proxy = FreeProxy(country_id=["RU"], anonym=True).get()
        if proxy == "There are no working proxies at this time.":
            proxy = None
    return proxy
