import scrapy
import smtplib
import os
from email.message import EmailMessage

# Environment Variables that hold Email Address and Password
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
PASSWORD = os.environ.get('EMAIL_PASSWORD')


# Function which sends the email once conditions are satisfied
def send_mail():
    msg = EmailMessage()
    msg['Subject'] = 'Price Tracker'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'Enter the email address where you want to send the mail to'
    msg.set_content("""The Price of the item is now the desired price.
    Check out the link below:
    [Enter the link below which you've crawled]
    """)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, PASSWORD)
        smtp.send_message(msg)


# PRICE TRACKER FOR AMAZON
class AmazonSpider(scrapy.Spider):
    name = 'Amazon_spider'
    start_urls = [
        'Enter the URL of the item here'
    ]

    def parse(self, response):
        product_name = response.xpath('//*[@id="productTitle"]/text()').get()
        price = response.xpath('//*[@id="priceblock_ourprice"]/text()').get()

        if price is None:
            print('Sorry the item is out of stock!')
        else:
            # Convert the price string to float. The string contains " , " and " \n " so we have to remove it first
            price = price.strip()
            price = price.replace(",", "")
            final_price = float(price)

            if final_price <= "Enter the desired price of the item":
                send_mail()


# For now the function doesn't do anything when the item is out of stock. It just prints the message to console.

# PRICE TRACKER FOR FLIPKART
class FlipkartSpider(scrapy.Spider):
    name = 'Flipkart_spider'
    start_urls = [
        'Enter the URL of the item here'
    ]

    def parse(self, response):
        product_name = response.xpath(
            '//*[@id="container"]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div/div[1]/h1/span/text()').get()
        price = response.xpath(
            '//*[@id="container"]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div/div[4]/div[1]/div/div[1]/text()').get()

        if price is None:
            print('Sorry the item is out of stock!')
        # Converting the Price string to float. Flipkart returns string containing " , " and " ₹ " so we have to remove it
        # to convert it to float
        else:
            price = price.replace(",", "")
            price = price.replace("₹", "")
            final_price = float(price)

            if (final_price <= "Enter the desired price of the item"):
                send_mail()
