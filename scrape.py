
#git config  --global user.name "prajita kc"
#git config  --global user.email "ksheaprazeeta@gmail.com"


#git init 
#git status => if you want to check what are teh status of the file 
#git add .
#git commit -m "your message"
#create  repository  in github
#copy paste git code from github


###############
#1.change the code
#2. git add .
#3. gitr commit -m "your message"
#4.git push
###############


import csv
import requests
import json
import sqlite3
from bs4 import BeautifulSoup

#--url of the website to scrape--
url ="http://books.toscrape.com/"


def scrape_books(url):
    response= requests.get(url)  # ---get =>read the data from the website ---
    if response.status_code !=200:  #status code should be 200  to run
        print("failed to fetch the page.status code:{response.status_code}")   #beautifulsoup =>library
        return
  
  #set encoding to handle special character correctly
    response.encoding = response.apparent_encoding    #special character jhiknu paryo vane 


    soup = BeautifulSoup(response.text,"html.parser")       
    books= soup.find_all("article", class_="product_pod")
  
    all_books=[]
    for  book in books:
        title = book.h3.a['title']   #[] =>attribute  (dot) is tag
        price_text = book.find("p",class_= "price_color").text
        currency =price_text[0]
        price= float(price_text [1:])
        book_data ={
        "title":title,
        "currency":currency,
        "price":price,
        
        }
        all_books.append(book_data)
    
    return all_books






def save_to_json(books):
    with open("books.json", "w",encoding="utf-8") as file:
      
        json.dump(books,file,ensure_ascii=False,indent=4)



#into csv
def save_to_csv(books):
    

    with open("books.csv", "w", newline="", encoding="utf-8") as file:
        import csv
        writer = csv.DictWriter(file, fieldnames=["title","currency","price"])
        writer.writeheader()  # write the header row
        writer.writerows(books)

def create_table():
    import sqlite3
    con = sqlite3.connect("books.sqlite3")
    cursor = con.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        currency TEXT,
        price REAL
    )
    """)


    con.commit()
    con.close()

print("database and table are created successfully")

def insert_book(title, currency, price):
   
    con = sqlite3.connect("books.sqlite3")
    cursor = con.cursor()
    cursor.execute(
    "INSERT INTO books (title, currency, price)VALUES (?, ?, ?)",
    (title, currency, price))
    

    con.commit()
    con.close() 

print("Database and table successfully created ")
books = scrape_books(url)
def main():

    save_to_csv(books) 
    save_to_json(books)
    create_table()


    for book in books:
        
        insert_book(book["title"], book["currency"], book["price"]) 

main()