from selenium import webdriver
import pandas as pd
import time

# target URLs
url_22 = "https://newssearch.chinadaily.com.cn/en/search?cond=%7B%22publishedDateFrom%22%3A%222022-08-24%22%2C%22publishedDateTo%22%3A%222023-08-23%22%2C%22fullMust%22%3A%22marine+pollution%22%2C%22sort%22%3A%22dp%22%2C%22duplication%22%3A%22on%22%7D&language=en"
url_23 = "https://newssearch.chinadaily.com.cn/en/search?cond=%7B%22publishedDateFrom%22%3A%222023-08-24%22%2C%22publishedDateTo%22%3A%222024-08-23%22%2C%22fullMust%22%3A%22marine+pollution%22%2C%22sort%22%3A%22dp%22%2C%22duplication%22%3A%22on%22%7D&language=en"

# Part 1: Function to get all article URLs
def get_article_urls(driver, url_list):
    """Fetch all article URLs and titles from the page."""
    articles = driver.find_elements("css selector", "span.intro")
    
    for article_element in articles:
        # Find the article link within the span
        article_link = article_element.find_element("css selector", 'a')
        
        # Print the article title and URL
        print(article_link.text)
        print(article_link.get_attribute("href"))
        
        # Append article details to the list
        article = {
            'title': article_link.text,
            'href': article_link.get_attribute('href')
        }
        url_list.append(article)
    
    return url_list

# Part 2: Pagination Handling
def get_current_page(driver):
    """Get the current page's pagination information."""
    try:
        page_block = driver.find_element("css selector", "div.page.rt")
        pages = page_block.find_element("css selector", "span")
        
        # Check if there is a 'NEXT' button for pagination
        if "NEXT" not in pages.text:
            return None
        return pages
    except Exception as e:
        print(f"Error getting current page: {e}")
        return None

def go_to_next_page(driver, pages):
    """Click on the 'NEXT' button to go to the next page."""
    try:
        page_buttons = pages.find_elements("css selector", "a")
        for button in page_buttons:
            if "NEXT" in button.text:
                print("Navigating to the next page.")
                button.click()
                driver.implicitly_wait(10)
                time.sleep(5)
                break
    except Exception as e:
        print(f"Error navigating to the next page: {e}")

def get_articles_from_url(driver, url):
    """Extract articles from a given URL, handling pagination."""
    driver.get(url)
    driver.implicitly_wait(10)
    
    # Initialize list to store article URLs
    article_urls = []
    
    # Get the pagination info and start extracting articles
    pages = get_current_page(driver)
    while True:
        # Extract articles from the current page
        article_urls = get_article_urls(driver, article_urls)
        
        # Exit if no more pages are available
        if not pages:
            break
        
        # Go to the next page
        go_to_next_page(driver, pages)
        
        # Update the pagination information for the next iteration
        pages = get_current_page(driver)
    
    return article_urls

if __name__ == "__main__":
    # Initialize the Firefox driver
    ff_driver = webdriver.Firefox()

    # Fetch articles for 2022-23 and 2023-24
    articles_22 = get_articles_from_url(ff_driver, url_22)
    articles_23 = get_articles_from_url(ff_driver, url_23)
    
    # Save the results to CSV files
    df_22 = pd.DataFrame(articles_22)
    df_23 = pd.DataFrame(articles_23)

    df_22.to_csv("results\\2022-23_articles.csv", index=False)
    df_23.to_csv("results\\2023-24_articles.csv", index=False)

    # Close the browser
    ff_driver.quit()
