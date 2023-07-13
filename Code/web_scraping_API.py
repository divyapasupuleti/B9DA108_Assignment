from flask import Flask
import requests
from bs4 import BeautifulSoup
import pandas as pd
from utils import mysql_connector


app = Flask(__name__)


@app.route('/',methods=['POST', 'GET'])
def home_page():
    return("Extraction API : Call /web_extraction/v1.0")

@app.route('/web_extraction/v1.0',methods=['POST', 'GET'])
def extraction():
    books = []
    try:
        for i in range(1,20):
            url = f"https://books.toscrape.com/catalogue/page-{i}.html"
            response = requests.get(url)
            response = response.content
            soup = BeautifulSoup(response, 'html.parser')
            ol = soup.find('ol')
            articles = ol.find_all('article', class_='product_pod')
            idx = 1
            for article in articles:
                print("---------------------------------------")
                print(idx)
                image = article.find('img')
                title = image.attrs['alt']
                starTag = article.find('p')
                star = starTag['class'][1]
                price = article.find('p', class_='price_color').text
                price = float(price[1:])
                mydb, mycursor = mysql_connector()
                sql = "INSERT INTO web_extraction.bookdata (Title, Rating, Price) VALUES (%s, %s, %s)"
                val = (title, star, price)
                mycursor.execute(sql, val)
                mydb.commit()
                idx = idx + 1
                books.append([title, star, price])
        df = pd.DataFrame(books, columns=['Title', 'Star Rating', 'Price'])
        return {
            "APIResponse" : "Web Scraping Successfull and Results Stored in the DB"
            }

    except Exception as e:
        print(e)
        return {
            "APIResponse" : e
            }
    
    
if __name__ == '__main__':
    app.run()