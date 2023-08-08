from bs4 import *
import requests
import json
import boto3

# Define env parameters / values
# first hard coded. later move to env parameter in AWS configuration
sqs_arn = "https://sqs.us-east-1.amazonaws.com/578409035468/sqs-matomo-message"
site_list = ["https://www.jamesallen.com/loose-diamonds/oval-cut/"] # Adding any site you want to extract images/data on diamond


# Sending a message to SQS
def sanding_sqs_massage(message):

    data = {}
    data['ref'] = message
    print(data)

    sqs_resource = boto3.resource('sqs')

    response = sqs_resource.send_message(
        QueueUrl=sqs_arn,
        MessageBody=json.dumps(data)
    )
    print(response)


# extract relevant content from HTML
def lambda_handler():

    try:
        for site in site_list:
            # content of URL
            r = requests.get(site)

            # Parse HTML Code
            soup = BeautifulSoup(r.text, 'html.parser')

            # find all href from 'link' and 'a' elemnts
            ref_list = soup.find_all('link')
            ref_list += soup.find_all('a')

            for ref in ref_list:
                if ref.has_attr('href'):  # Check if the tag has an 'href' attribute
                    href = ref['href']
                    if not href.endswith(('.css', '.png', '/')):  # Skip if the link ends with .css or .png or /

                        # Appropriate conditions for specific sites
                        if (site.__contains__('www.jamesallen.com')) & (not href.startswith(('https://www.jamesallen.com'))):
                            href = 'https://www.jamesallen.com/' + href
                            sanding_sqs_massage(href)  # sending url using sqs
                        else:
                            sanding_sqs_massage(href)  # sending url using sqs
    except:
        pass