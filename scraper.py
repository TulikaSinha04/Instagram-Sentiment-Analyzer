from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def scrape_instagram_data(username):
    url = f"https://www.instagram.com/{username}/"
    driver = init_driver()
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    try:
        data = soup.find_all('meta', property='og:description')[0]['content']
        values = data.split(" - ")[0].split(', ')
        posts = int(values[0].replace(',', '').split(' ')[0])
        followers = values[1].split(' ')[0]
        following = values[2].split(' ')[0]
    except:
        posts = followers = following = "Unknown"

    post_links = []
    captions = []
    hashtags = []

    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href and "/p/" in href:
            post_url = "https://www.instagram.com" + href
            if post_url not in post_links:
                post_links.append(post_url)
            if len(post_links) >= 10:
                break

    for post_url in post_links:
        driver.get(post_url)
        time.sleep(3)
        post_soup = BeautifulSoup(driver.page_source, 'html.parser')
        span = post_soup.find('meta', property='og:description')
        if span:
            caption = span['content']
            captions.append(caption)
            hashtags.append([tag for tag in caption.split() if tag.startswith('#')])
        else:
            captions.append("")
            hashtags.append([])

    driver.quit()

    return {
        'username': username,
        'posts': posts,
        'followers': followers,
        'following': following,
        'post_links': post_links,
        'captions': captions,
        'hashtags': hashtags
    }