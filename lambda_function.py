import boto3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Define env parameters / values
# first hard coded. later move to env parameter in AWS configuration
sqs_arn = "arn:aws:sqs:us-east-1:682766493838:sqs_invoking_web_scraping_fnc"
site_list = ["https://www.jamesallen.com/loose-diamonds/oval-cut/"] # Adding any site you want to extract images/data on diamond


# Sending a message to SQS
def sanding_sqs_massage(message):

    data = {}
    data['ref'] = message
    print(data)

    # sqs_resource = boto3.resource('sqs')
    #
    # response = sqs_resource.send_message(
    #     QueueUrl=sqs_arn,
    #     MessageBody=json.dumps(data)
    # )
    # print(response)


# extract relevant content from HTML
def lambda_handler(event, context):
    try:

        driver_path = '/usr/local/bin/chromedriver'

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        for site in site_list:

            driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
            driver.get(site)

            ref_list = []  # REF LIST for specific site

            pause = 2  # Increased pause time to allow content to load

            # Explicitly wait for some element to appear (you can adjust this condition based on your use case)
            wait = WebDriverWait(driver, 30)  # Wait up to 30 seconds
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            lastHeight = driver.execute_script("return document.body.scrollHeight")
            # print(lastHeight)

            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(pause)
                newHeight = driver.execute_script("return document.body.scrollHeight")
                if newHeight == lastHeight:
                    break
                lastHeight = newHeight
                print(lastHeight)

            # print(driver.page_source) # print the html with the exist HTML tags before effect on div tags (like click on div to open)

            # # ------------------ # # relevant only for https://www.jamesallen.com/loose-diamonds/oval-cut/ website
            j = 1
            while j <= 20:
                i = 0
                while i <= 22:

                    xpathDiv = f"// *[ @ id = \"_{j}_{i}\"]"
                    xpathSubDiv = f"// *[ @ id = \"_{j}_{i}\"] / div"
                    xpathSubSubDiv = f"// *[ @ id = \"_{j}_{i}\"] / div / div[2]"
                    xpathLink = f"// *[ @ id = \"_{j}_{i}\"] / div / div[2] / a"

                    # print("Href Element: ", f"_{j}_{i}") # Print element number

                    try:
                        # Main div
                        # Wait for the element to be clickable
                        element = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, xpathDiv))
                        )
                        # Scroll to element and click
                        driver.execute_script("arguments[0].scrollIntoView();", element)
                        driver.execute_script("arguments[0].click();", element)

                        # Subdiv
                        subElement = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, xpathSubDiv))
                        )
                        # Scroll to element and click
                        driver.execute_script("arguments[0].scrollIntoView();", subElement)
                        driver.execute_script("arguments[0].click();", subElement)

                        # SubSubdiv
                        subSubElement = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, xpathSubSubDiv))
                        )
                        # Scroll to element and click
                        driver.execute_script("arguments[0].scrollIntoView();", subSubElement)
                        driver.execute_script("arguments[0].click();", subSubElement)

                        # Link
                        linkElement = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, xpathLink))
                        )
                        # Scroll to element and click
                        driver.execute_script("arguments[0].scrollIntoView();", linkElement)

                        # Get the value of the 'href' attribute and print it
                        href_value = linkElement.get_attribute("href")
                        ref_list.append(href_value)
                        # print("Href attribute:", href_value)

                    except Exception as e:
                        # Handle the stale element reference exception if needed
                        print("An error occurred:", str(e))

                    i += 1

                j += 1
            # -------------------
            driver.quit()

            for href in ref_list:
                print(href)
                # sanding_sqs_massage(href)  # sending url using sqs

    except Exception as e:
        print("An error occurred:", str(e))