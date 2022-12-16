import pyautogui as pyautogui
from selenium.webdriver.chrome import service as fs
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup



def create_proxyauth_extension(proxy_host, proxy_port,
                               proxy_username, proxy_password,
                               scheme='http', plugin_path=None):
    """Proxy Auth Extension
       args:
           proxy_host (str): domain or ip address, ie proxy.domain.com
           proxy_port (int): port
           proxy_username (str): auth username
           proxy_password (str): auth password
       kwargs:
           scheme (str): proxy scheme, default http
           plugin_path (str): absolute path of the extension
       return str -> plugin_path
       """


    import string
    import zipfile

    if plugin_path is None:
        plugin_path = 'vimm_chrome_proxyauth_plugin.zip'

    manifest_json = """
            {
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Chrome Proxy",
                "permissions": [
                    "proxy",
                    "tabs",
                    "unlimitedStorage",
                    "storage",
                    "<all_urls>",
                    "webRequest",
                    "webRequestBlocking"
                ],
                "background": {
                    "scripts": ["background.js"]
                },
                "minimum_chrome_version":"22.0.0"
            }
            """

    background_js = string.Template(
        """
               var config = {
                       mode: "fixed_servers",
                       rules: {
                         singleProxy: {
                           scheme: "${scheme}",
                           host: "${host}",
                           port: parseInt(${port})
                         },
                         bypassList: ["foobar.com"]
                       }
                     };
               chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
               function callbackFn(details) {
                   return {
                       authCredentials: {
                           username: "${username}",
                           password: "${password}"
                       }
                   };
               }
               chrome.webRequest.onAuthRequired.addListener(
                           callbackFn,
                           {urls: ["<all_urls>"]},
                           ['blocking']
               );
               """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path




# -------------------selenium-----------------------

drive_path = r"C:\Users\Systena\development\chromedriver.exe"
chrome_service = fs.Service(executable_path=drive_path)

chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument('--ignore-certificate-errors')


proxyauth_plugin_path = create_proxyauth_extension("proxy")
chrome_options.add_extension(proxyauth_plugin_path)

drive = webdriver.Chrome(options=chrome_options,service=chrome_service)

drive.get("https://mail.google.com/chat/u/0/#chat/space/AAAAMJIhp8c")
email = drive.find_element(By.NAME, "identifier")
email.send_keys("useremail")
email.send_keys(Keys.ENTER)

time.sleep(4)
password = drive.find_element(By.NAME, "Passwd")
password.send_keys("useremail")
password.send_keys(Keys.ENTER)

time.sleep(7)
chat = drive.find_element(By.XPATH, '//*[@id="gs_lc50"]/input[1]')
chat.send_keys("41")
time.sleep(2)
chat.send_keys(Keys.DOWN)
time.sleep(1)
chat.send_keys(Keys.ENTER)

time.sleep(2)

drive.switch_to.frame("hostFrame1")
textbox = drive.find_element(By.XPATH, "//div[@id='T2Ybvb0']")
drive.execute_script("arguments[0].innerText = 'Python test'", textbox)
drive.execute_script("arguments[0].click()", textbox)
time.sleep(1)

pyautogui.press("enter")



drive.switch_to.default_content()
drive.quit()



# --------------------------------------method storage--------------------------------------
# button = drive.find_elements(By.XPATH, "//div[@aria-label='メッセージを送信']")
# mapObject = drive.execute_script('return document.querySelector(arguments[0])', "body c-wiz div div div div div div c-wiz div div div c-wiz div div div span span span svg")

# print(button[1].get_attribute("tabindex"))
# for i in range(len(button)):
#     actions.click(button[i]).perform()
#     # drive.execute_script("arguments[0].setAttribute('class','U26fgb mUbCce fKz7Od zFe2Ef m7Rhac M9Bg4d')", button[i])
#     # print(button[i].get_attribute("tabindex"))
#     #
#     #
#     # drive.execute_script("arguments[0].click()", button[i])
#     drive.execute_script("arguments[0].click()", textbox)
#     drive.execute_script(
#         "arguments[0].dispatchEvent(new MouseEvent('click', {view: window, bubbles:true, cancelable: true}))",
#         button[i])

