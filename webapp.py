import requests 
from bs4 import BeautifulSoup
import numpy as np
from flask import Flask,render_template,request,jsonify
import time
from werkzeug.exceptions import HTTPException
import json

app=Flask(__name__)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "error": "Something went wrong, check url again."
    })
    response.content_type = "application/json"
    return response


#-------Currency convert function---------#
def convert():
    url="https://www.google.com/search?q=aed+to+pkr+&sxsrf=ALeKk02To4yhBWpyI9HXCdFIBf4NCDTIXQ%3A1616665927504&ei=R11cYNSdHtOs1fAPidWquAk&oq=aed+to+pkr+&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECcyBAgjECcyBQgAEJECMgUIABCRAjIFCAAQsQMyCAgAEMkDEJECMgUIABCRAjICCAAyAggAMgIIADoHCAAQRxCwAzoGCAAQFhAeUMjTDlj54g5glOcOaAFwAngAgAGlA4gBhhWSAQgyLTEwLjAuMZgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=gws-wiz&ved=0ahUKEwiU3dDylcvvAhVTVhUIHYmqCpcQ4dUDCA0&uact=5"
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}
    r = requests.get(url, headers=headers)
    soup=BeautifulSoup(r.text,"html.parser")
    a=soup.find("div",{"class":"BNeawe iBp4i AP7Wnd"})
    a=a.text
    a=a[:-16]
    a=float(a)
    return a


#-------IKEA website scrap-------------#
@app.route("/info",methods=["POST"])
def data():
    url=request.form.get('url')
    rate=convert()
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}
    r = requests.get(url, headers=headers)
    ab=[]
    soup=BeautifulSoup(r.content,"html.parser")
    
    for i in soup.find_all("div",{"class","range-revamp-product-compact"}):
        image=i.find('img').attrs['src']
        title=i.find('div',{"class","range-revamp-header-section__title--small notranslate"}).text
        seat=i.find('span',{"class","range-revamp-header-section__description-text"}).text
        price=i.find('span',{"class","range-revamp-price__integer"})
        price=[price.text]
        price=([s.replace(',', '') for s in price])
        price = [int(i) for i in price] 
        price = [int(element *rate) for element in price]
        prices1 = [int(element *2.5/100) for element in price]
        arr1 = np.array(price)
        arr2 = np.array(prices1)
        price= int(arr1 + arr2)
        price=str(price)
        INFO={
            'images':image,
            'titles':title,
            'seats':seat,
            'prices':price
        }
        a=INFO['titles'],INFO['seats'],INFO['images'],INFO['prices']
        ab.append(a)
    return jsonify(ab)


if __name__ == "__main__":
    app.run(debug=True)
