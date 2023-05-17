from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from xlsxwriter import Workbook
import pandas as pd
from elasticsearch import Elasticsearch
import requests
# endpoints
# post_req = 'https://api.sheety.co/f82ee7eb6e161c1b0a429a3a00506100/scrappingTwitterLinkedin/sheet1'

# ****************Time-handler**********************#


def Time_Changer(date_string):
    # ***********************************************#
    iso_date = date_string
    dt = datetime.fromisoformat(iso_date[:-1])
    unix_ts = dt.timestamp()
    ms_since_epoch = int(unix_ts * 1000)
    return ms_since_epoch
    # **********************************************#
    # date, time = date_string.split('T')
    # tame = time.split('.')
    # 2023-04-12T10:21:41.000Z
    # year, month, day = date.split('-')
    # hour, minute, seconds = tame[0].split(':')
    # year = int(year)
    # hour = int(hour)
    # minute = int(minute)
    # epoch = time.mktime((year, 1, 1, hour, minute, 0, 0, 0, 0))
    # milliseconds = int(epoch * 1000)

    # return milliseconds
# *************************************************#


def Twitter():
    Comp_list = ['Exotel', 'Ozonetel', 'AiSensy_wa', 'interaksyon', 'AmeyoCIM', 'yellowdotai',
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
    # set up the driver
    for Comp_name in Comp_list:
        driver = webdriver.Chrome()
        driver.get(f"https://www.twitter.com/{Comp_name}")
        time.sleep(5)
        initialScroll = 0
        finalScroll = 1000
        # scroll down to load more tweets
        for i in range(2):
            driver.execute_script(
                f"window.scrollTo({initialScroll},{finalScroll})")
            initialScroll = finalScroll
            finalScroll += 1000
            time.sleep(5)
        # extract tweet body and number of likes of 10 latest posts
        tweets = driver.find_elements(
            By.XPATH, "//article[@data-testid='tweet']")
        for tweet in tweets[:10]:
            try:
                btn = driver.find_element(
                    By.XPATH, './/span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0" and text()="Not now"]')
            except:
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

                # Get current date
                current_date = datetime.today()

                # Get year, month, and day from the date
                year = current_date.year
                month = current_date.month
                day = current_date.day

                date_string = f"{day}/{month}/{year}:00:00"
                # 09/05/2023:00:00
                # 08/05/2023:00:00
                # 2023-05-02T09:39:41.000Z
                # 3/5/2023:12:00
                datetime_obj = datetime.strptime(date_string, '%d/%m/%Y:%H:%M')

                # Convert the datetime object to epoch time in milliseconds
                epoch_time_ms = int(datetime_obj.timestamp() * 1000)

                # if time_count >= curr_time-86400000:
                # time count = 1683443546000
                # print(
                #     "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                # print('post time:', time_count)
                # print('post date:', date_time[0].get_attribute(
                #     'datetime'))
                # print('starting time:', epoch_time_ms-86400000)
                # print('Ending time:', epoch_time_ms)
                # print(tweet_text)
                if time_count >= epoch_time_ms-86400000 and time_count < epoch_time_ms:
                    Comp1_list.append(Comp_name)
                    like_list.append(likes_count)
                    date_list.append(time_count)
                    tweet_list.append(tweet_text)
                    comment_list.append(comment_count)
                    Tweet_ID_list.append(tweet_ID[1])
                    curr_time_list.append(curr_time)
                    Urls_list.append(URL)
                    Tweet_content_list.append(Tweet_content)

            else:
                btn.click()
            finally:
                tweets = driver.find_elements(
                    By.XPATH, ".//article[@data-testid='tweet']")
        driver.close()

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

    es = Elasticsearch(['http://172.17.4.15:9200/'])

    for i in range(0, len(Comp1_list)):

        doc = {
            "company": Comp1_list[i],
            "platform": 'Twitter',
            "platform_id": Tweet_ID_list[i],
            "Tweet url": Urls_list[i],
            "content": tweet_list,
            "scrapping_time": date_list[i],
            "post_time": curr_time_list[i],
            "likes": like_list[i],
            "comments": comment_list[i],
            "type": Tweet_content_list[i],
        }

        res = es.index(index="social_posts2", id=i+1, document=doc)
        print(res['result'])

        res = es.get(index="social_posts2", id=i+1)
        print(res['_source'])

        es.indices.refresh(index="social_posts2")

    # for i in range(len(Comp1_list)):
    #     sheet_input = {
    #         'sheet1': {
    #             "Company Name": Comp1_list[i],
    #             "Linked/Twitter": 'Twitter',
    #             "Tweet id": Tweet_ID_list[i],
    #             "Tweet Url": Urls_list[i],
    #             "Tweet content": tweet_list[i],
    #             "Date_Time of posting (in millisecond format)": date_list[i],
    #             "Date_Time of scrapping (in millisecond format)": curr_time_list[i],
    #             "no. of likes": like_list[i],
    #             "no. comments": comment_list[i],
    #             "type of post(img/text/video)": Tweet_content_list[i],
    #         }
    #     }

    # response = requests.post(url=post_req, json=sheet_input)
    # print(response.text)
    # print("response.status_code =", response.status_code)
    # print("response.text =", response.text)
    # ************************************************#
    df = pd.DataFrame(raw_data)
    writer = pd.ExcelWriter('test2.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.close()
    # ************************************************#


Twitter()
