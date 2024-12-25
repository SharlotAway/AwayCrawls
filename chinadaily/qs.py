from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

xpath = "//*[@id='div_currpage']"

def main1():
    driver = webdriver.Firefox()
    url = "https://www.chinadaily.com.cn/a/202305/13/WS645f7da6a310b6054fad2cba_1.html"
    url = "https://www.chinadaily.com.cn/a/202308/23/WS64e55928a31035260b81db2f.html"
    driver.get(url)
    driver.implicitly_wait(20)

    # 获取页面块
    

    # 判断页面中是否有分页按钮
    try:
        page_block = driver.find_element(By.XPATH, "//*[@id='div_currpage']")
        page_buttons = page_block.find_elements(By.CSS_SELECTOR, "a")
        
        # 添加标题
        while True:
            # 获取段落，在 content.p 里面
            texts = driver.find_elements("xpath", "//*[@id='Content']/p")
            # 拼接段落并输出
            text = "\n".join([t.text for t in texts])
            print(text)
            # 不是最后一页
            if "next" in page_block.text.lower():
                for b in page_buttons:
                    try:
                        if b.text.lower() == "next":
                            # 点击 Next 按钮
                            b.click()
                            print("Next page clicked")

                            # 等待页面加载并重新获取新的 URL
                            WebDriverWait(driver, 10).until(
                                EC.staleness_of(page_block)  # 等待当前页面的元素不再可用
                            )
                            
                            # 在此时尝试获取新的 URL
                            current_url = driver.current_url
                            print(f"New page URL: {current_url}")

                            # 确保页面已经完全加载，可以在这里使用 driver.get() 强制加载
                            driver.get(current_url)
                            
                            # 等待新页面加载完成
                            WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, "//*[@id='div_currpage']"))
                            )

                            # 重新获取分页块元素
                            page_block = driver.find_element(By.XPATH, "//*[@id='div_currpage']")
                            page_buttons = page_block.find_elements(By.CSS_SELECTOR, "a")
                            break

                    except Exception as err:
                        print(f"Error: {err}")
                        driver.quit()
                        break
            else:
                break
    except:
        print("No page buttons.")
        # 获取段落，在 content.p 里面
        texts = driver.find_elements("xpath", "//*[@id='Content']/p")
        # 拼接段落并输出
        text = "\n".join([t.text for t in texts])
        print(text)
    
    driver.quit()  # Ensure to quit the driver after the script ends

if __name__ == "__main__":
    # driver = webdriver.Firefox()
    # url = "https://www.chinadaily.com.cn/a/202305/13/WS645f7da6a310b6054fad2cba_1.html"
    # url = "https://www.chinadaily.com.cn/a/202308/23/WS64e55928a31035260b81db2f.html"
    # driver.get(url)
    # driver.implicitly_wait(20)

    # xpath1 = "/html/body/div[10]/div[1]/div[4]"
    # xpath2 = "/html/body/div[5]/div[6]"
    file_path = "results\together_22.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    n = content.count("##################")