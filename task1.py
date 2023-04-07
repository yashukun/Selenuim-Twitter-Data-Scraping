from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://www.twitter.com/Exotel")
time.sleep(5)
initialScroll = 0
finalScroll = 1000

# scroll down to load more tweets
for i in range(4):
    driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
    initialScroll = finalScroll
    finalScroll += 1000
    time.sleep(5)

# extract tweet body and number of likes of 10 latest posts
tweets = driver.find_elements(By.XPATH,"//article[@data-testid='tweet']")
for tweet in tweets[:10]:
    try:
        btn = driver.find_element(By.XPATH,'//span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0" and text()="Not now"]')
    except:
        tweet_body = tweet.find_elements(By.XPATH,".//div[@lang='en']")
        likes = tweet.find_elements(By.XPATH,".//div[@data-testid='like']//span[@class='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0']")
        date_time = tweet.find_elements(By.XPATH,".//time")

        # extract the text from the tweet body and likes elements
        tweet_text = tweet_body[0].text if tweet_body else None
        likes_count = likes[0].text if likes else None
        time_count = date_time[0].text if date_time else None
        print("Date-Time:",time_count)
        print("Tweet Body:", tweet_text)
        print("Likes:", likes_count)
        print()
        print()

driver.quit()