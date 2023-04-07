from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
Comp_list = ['Exotel','Ozonetel','AiSensy_wa','interaksyon','AmeyoCIM']
Comp1_list = []
like_list = []
date_list = []
tweet_list = []
# set up the driver
for Comp_name in Comp_list:
    driver = webdriver.Chrome()
    driver.get(f"https://www.twitter.com/{Comp_name}")
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
            # views = tweet.find_elements(By.XPATH,'//div[@role="group"]/div[4]/a/div/div[2]/span/span/span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"]')
            # extract the text from the tweet body and likes elements
            tweet_text = tweet_body[0].text if tweet_body else None
            likes_count = likes[0].text if likes else None
            time_count = date_time[0].text if date_time else None
            # views_count = views[0].text if views else None
            print("Date-Time:",time_count)
            print("Tweet Body:", tweet_text)
            print("Likes:", likes_count)
            # print("Views:", views_count)
            print()
            Comp1_list.append(Comp_name)
            like_list.append(likes_count)
            date_list.append(time_count)
            tweet_list.append(tweet_text)

        else:
            btn.click()
        finally:
            tweets = driver.find_elements(By.XPATH,"//article[@data-testid='tweet']")
    # close the driver

raw_data = {
    "Company Name": Comp1_list,
    "Dates": date_list,
    "Likes": like_list,
    "Tweet": tweet_list 
}
# df = pd.DataFrame(raw_data, columns = ['Dates', 'Likes', 'Tweet'])
# test code start
# T - 3 : fetch last 10 posts of a company & put in excel 
df = pd.DataFrame(raw_data)
writer = pd.ExcelWriter('Comp5.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', index=False)
writer.close()
# test code end
#df.to_excel('Tweet.xlsx')
print(df)

driver.close()
# pop up window 
# xpath = //div[@class='css-1dbjc4n r-kemksi r-16y2uox r-1dqxon3 r-16wqof']
# cross btn xpath
# //div[@class='css-901oao r-1awozwy r-6koalj r-18u37iz r-16y2uox r-37j5jr r-a023e6 r-b88u0q r-1777fci r-rjixqe r-bcqeeo r-q4m81j r-qvutc0']
# not not button
# xpath //span[@class='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0' and text()="Not now"]
# time xpath = //time