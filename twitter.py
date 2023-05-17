from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time
import pandas as pd
from xlsxwriter import Workbook


def Time_Changer(date_string):
    # ***********************************************#
    iso_date = date_string
    dt = datetime.fromisoformat(iso_date[:-1])
    unix_ts = dt.timestamp()
    ms_since_epoch = int(unix_ts * 1000)
    return ms_since_epoch


profiles = ['Exotel', 'Ozonetel', 'AiSensy_wa', 'interaksyon', 'AmeyoCIM', 'yellowdotai',
            'haptik', 'heyinterakt', 'gallabox', 'gupshup', 'koredotai', 'boost_ai_', 'otpless',
            'uniphore', 'RingCentral']

Comp1_list = []
like_list = []
date_list = []
tweet_list = []
comment_list = []
curr_time_list = []
Urls_list = []
Tweet_ID_list = []
Tweet_content_list = []
# Set the profile name and date range for the tweets
for profile_name in profiles:
    yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    today_date = datetime.now().strftime('%Y-%m-%d')

    # Start the WebDriver and navigate to the Twitter profile
    driver = webdriver.Chrome()
    driver.get(f"https://www.twitter.com/{profile_name}")
    # try:
    #     btn = driver.find_element(
    #         By.XPATH, './/span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0" and text()="Not now"]')
    # except:
    # Scroll down to load more tweets
    initialScroll = 0
    finalScroll = 1000
    for i in range(5):
        driver.execute_script(
            f"window.scrollTo({initialScroll},{finalScroll})")
        initialScroll = finalScroll
        finalScroll += 1000
        time.sleep(5)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, ".//div[@aria-label='Timeline: " + yesterday_date + "']")))

    # Fetch the tweets posted yesterday
    tweets = driver.find_elements(
        By.XPATH, ".//div[@aria-label='Timeline: " + yesterday_date + "']//div[@data-testid='tweet']")

    # Print the text content of each tweet
    for tweet in tweets:
        tweet_body = tweet.find_elements(
            By.XPATH, ".//div[@lang='en']")

        likes = tweet.find_elements(
            By.XPATH, ".//div[@data-testid='like']//span[@class='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0']")

        date_time = tweet.find_elements(By.XPATH, ".//time")

        reply_body = tweet.find_elements(
            By.XPATH, ".//div[@data-testid='reply']/div/div[2]/span/span/span[@class='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0']")

        tweet_URL = tweet.find_elements(
            By.XPATH, ".//a[@class='css-4rbku5 css-18t94o4 css-901oao r-1bwzh9t r-1loqt21 r-xoduu5 r-1q142lx r-1w6e6rj r-37j5jr r-a023e6 r-16dba41 r-9aw3ui r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0']")

        tweet_text = tweet_body[0].text if tweet_body else None
        likes_count = likes[0].text if likes else None
        time_count = date_time[0].get_attribute(
            'datetime') if date_time else None
        time_count = Time_Changer(time_count)
        curr_time = round(time.time()*1000)
        comment_count = reply_body[0].text if reply_body else None
        URL = tweet_URL[0].get_attribute('href') if tweet_URL else None
        tweet_ID = URL.split('/status/')
        try:
            image = tweet.find_element(
                By.XPATH, ".//img[@alt='Image']")
            Tweet_content = "image"
        except:
            try:
                video = tweet.find_element(
                    By.XPATH, ".//div[@data-testid='videoPlayer']")
                Tweet_content = "video"
            except:
                Tweet_content = "only text"
            Comp1_list.append(profile_name)
            like_list.append(likes_count)
            date_list.append(time_count)
            tweet_list.append(tweet_text)
            comment_list.append(comment_count)
            Tweet_ID_list.append(tweet_ID[1])
            curr_time_list.append(curr_time)
            Urls_list.append(URL)
            Tweet_content_list.append(Tweet_content)

            raw_data = {
                "Company Name": Comp1_list,
                "Linked/Twitter": 'Twitter',
                "Tweet id": Tweet_ID_list,
                "Tweet url": Urls_list,
                "Tweet content": tweet_list,
                "Date_Time of posting (in millisecond format)": date_list,
                "Date_Time of scrapping (in millisecond format)": curr_time_list,
                "no. of likes": like_list,
                "no. comments": comment_list,
                "type of post(img/text/video)": Tweet_content_list,

            }
        # Close the browser
        driver.quit()
    # else:
    #     btn.click()
df = pd.DataFrame(raw_data)
writer = pd.ExcelWriter('test1.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', index=False)
writer.close()
