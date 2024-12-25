from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time
# from tqdm import tqdm

retry_times = 10

def article_content(driver, url, title, folder, idx):
    print("*"*50)
    print(f"Extracting: {title}")
    print("*"*50)
    driver.get(url)
    driver.implicitly_wait(20)
    # 去除一些“声明”
    def is_normal(t):
        if "necessarily reflect those of China Daily." in t \
            or "send us your writings" in t:
            print(f"Anouncement in ", url)
            return False
        else:
            return True
    # 习总书记的讲话
    if "Xi" in title:
        try:
            page_block = driver.find_element(By.XPATH, "//*[@id='div_currpage']")
            page_buttons = page_block.find_elements(By.CSS_SELECTOR, "a")
            text = ""
            # 添加标题
            while True:
                # 获取段落，在 content.p 里面
                texts = driver.find_elements("xpath", "//*[@id='Content']/p")
                # 拼接段落并输出
                text += "\n".join([t.text for t in texts])
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
        except Exception as err:
            print("Error: when extracting in a multi-page manner, exception occured:")
            print(err)
            print("Try to solve it in single-page manner.")
            # 获取段落，在 content.p 里面
            texts = driver.find_elements("xpath", "//*[@id='Content']/p")
            # 拼接段落并输出
            text = "\n".join([t.text for t in texts if is_normal(t.text)])
            # 添加标题
            text = "\n".join([f"Title: {title}", text])

    else:
        # 获取段落，在 content.p 里面
        texts = driver.find_elements("xpath", "//*[@id='Content']/p")
        # 拼接段落并输出
        text = "\n".join([t.text for t in texts if is_normal(t.text)])
        # 添加标题
        text = "\n".join([f"Title: {title}", text])
    # 替换冒号为连接号
    title = title.replace(":", "-")
    output_file = os.path.join(folder, str(idx + 1)+ "-" + title + ".txt")
    with open(output_file, mode='w', encoding='utf-8') as txtfile:
        txtfile.write(text)
    return text

def extract_by_year(driver, df, tgt_path, together_path):

    for idx, art in df.iterrows():
        with open(together_path, mode='a', encoding='utf-8') as txtfile:
            for t in range(retry_times):
                try:
                    content = article_content(ff_driver, art["href"], art["title"], tgt_path, idx)
                    break
                except Exception as err:
                    print(err)
                    print(f"Time out, retrying time {t+1}.")
                    time.sleep(1)
    
            txtfile.write(str(idx + 1).center(4, " ").center(40, "#") + "\n" + content + '\n\n')      
        time.sleep(2)


if __name__ == "__main__":
    df_22 = pd.read_csv("results\\2022-23_articles.csv")
    df_23 = pd.read_csv("results\\2023-24_articles.csv")
    tgt_path = "results"
    tgt_22 = os.path.join(tgt_path,"22")
    tgt_23 = os.path.join(tgt_path,"23")
    together_22 = os.path.join(tgt_path, 'together_22.txt')
    together_23 = os.path.join(tgt_path, 'together_23.txt')
    os.makedirs(tgt_22, exist_ok=True)
    os.makedirs(tgt_23, exist_ok=True)

    ff_driver = webdriver.Firefox()
    # extract_by_year(ff_driver, df_22, tgt_22, together_22)
    extract_by_year(ff_driver, df_23, tgt_23, together_23)

    ff_driver.close()
    # extract_by_year(ff_driver, df_23)