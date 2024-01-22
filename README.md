# web-scraping-href-extraction
This repository contains code for web scraping using Selenium to extract a list of Href (hyperlinks). The technology stack includes AWS Lambda Function, AWS CodeBuild, and the Selenium library for web scraping.

## Technology

- AWS Lambda Function
- AWS CodeBuild
- Selenium library for Web Scraping

### AWS Lambda Function

The provided Lambda Function utilizes the Selenium library to extract a list of Href from a web page. This list is then prepared for the next step, where each Href will be inserted into and the data will be scraped.

### AWS CodeBuild

AWS CodeBuild is employed to upload the Lambda Function to the AWS platform. It is an AWS service that facilitates the building and deployment of code. CodeBuild handles the uploading of the Lambda Function code to AWS and installs the necessary libraries specified in the `requirements.txt` file, including the Selenium library for web scraping.

## Usage

1. Ensure you have the required AWS services set up, including Lambda and CodeBuild.
2. Configure the Lambda Function to use the Selenium library for web scraping.
3. Utilize CodeBuild to upload the Lambda Function code to the AWS platform and install the required libraries from the `requirements.txt` file.
