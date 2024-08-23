from splinter import Browser
from selenium.webdriver.firefox.options import Options
import socket
import datetime
import subprocess
import argparse
import time

start = datetime.datetime.now()

parse = argparse.ArgumentParser(description='arguments to help each itteration')

parse.add_argument("-sock", type=int, help="define sock port")
parse.add_argument("-itter", type=int, help="to know which itteration")

args = parse.parse_args()

tor_process = subprocess.Popen(["tor", "-f", f"insts/torrc_{args.itter}"])

firefox_options = Options()

# Configure the proxy settings
firefox_options.set_preference("network.proxy.type", 1)
firefox_options.set_preference("network.proxy.socks", "127.0.0.1")
firefox_options.set_preference("network.proxy.socks_port", args.sock)
firefox_options.set_preference("network.proxy.socks_remote_dns", True)

def is_tor_running(host='127.0.0.1', port=args.sock):
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except (ConnectionRefusedError, socket.timeout, OSError):
        return False

while not is_tor_running():
    print("tor not running")
    time.sleep(1)
print("Tor is running.")
with Browser('firefox', options=firefox_options) as browser:
    browser.visit('http://adfoc.us/8627851')
    if browser.is_element_present_by_xpath("/html/body/div[2]/div[1]/a/img", wait_time=10):
        pass
    print("visited website")
    tor_process.kill()
end = datetime.datetime.now()

print(f"Done in {end - start} !")
