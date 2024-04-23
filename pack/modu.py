import sqlite3
import json
import csv
import os


sql='library.db'
users_csv='users.csv'
books_json='books.json'


def 創建():
    '''
    創建db
    '''
    if not os.path.exists(users_csv):
        raise FileNotFoundError("users.csv不存在,無法進行初始化")
    if not os.path.exists(books_json):
        raise FileNotFoundError("books.json不存在,無法進行初始化")
    conn = sqlite3.connect(sql)#建立資料庫

    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
             )''')#創建users表
    
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                publisher TEXT NOT NULL,
                year INTEGER NOT NULL
             )''')#創建books表
    
    with open(users_csv, newline='', encoding='utf-8') as csv_file:
        # 建立 CSV 讀取器
        csv_reader = csv.reader(csv_file)
        
        # 讀取 CSV 檔案內容
        for row in csv_reader:
            if not (row[0]=='username' and row[1]=='password'):
                c.execute(f'INSERT INTO users (username, password) VALUES ("{row[0]}", "{row[1]}")')
                #print(row[0])# 做你需要的處理，這裡我只是印出每一列的資料
        conn.commit()

    with open(books_json, encoding='utf-8') as json_file:
        books_data = json.load(json_file)
        for books in books_data:
            title=books["title"]
            author=books["author"]
            publisher=books["publisher"]
            year=books["year"]
            c.execute(f"INSERT INTO books (title, author, publisher, year) VALUES ('{title}','{author}','{publisher}','{year}')")
        conn.commit()
    conn.close()


def 偵測():
    '''
    偵測db存不存在
    '''
    if not os.path.exists('library.db'):
        創建()


def 登入()->bool:
    '''
    登入錯誤->false,登入成功->true
    '''
    conn=sqlite3.connect(sql)
    c = conn.cursor()
    username=input('請輸入帳號：')
    password=input('請輸入密碼：')
    c.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
    if len(c.fetchall()) == 1:
        return True
    else:
        return False
    

def 選單():
    '''
    顯示功能選單
    '''
    print()
    print("-"*20)
    print("    資料表 CRUD")
    print("-"*20)
    print("    1. 增加記錄")
    print("    2. 刪除記錄")
    print("    3. 修改記錄")
    print("    4. 查詢記錄")
    print("    5. 資料清單")
    print("-"*20)


def 對齊(目標字串,對齊數字):
    '''
    為了讓中文字能正常對齊
    '''
    count = 0
    for char in 目標字串:
        # 中文 
        if '\u4e00' <= char <= '\u9fa5':
            count += 2
        #全形標點符號
        elif '\u3000' <= char <= '\u303F':
            count += 2
        else:
            count += 1
    return 目標字串+' '*((對齊數字-count)%2)+'　'*((對齊數字-count)//2)


def 顯示書籍(SELECT=None,printmod=True):
    '''
    搜尋(預設全部),顯示(預設是開)
    '''
    conn=sqlite3.connect(sql)
    c = conn.cursor()
    if SELECT is None:
        c.execute("SELECT title,author,publisher,year FROM books")
    else:
        c.execute(f"SELECT title,author,publisher,year FROM books WHERE title like '%{SELECT}%' or author like '%{SELECT}%'")
    if printmod:
        print("|　　　　書名　　　　|　　　　作者　　　　|　　　出版社　　　　| 年份 |")    
        for book in c.fetchall():
            title= 對齊(book[0],20)
            author=對齊(book[1],20)
            publisher=對齊(book[2],20)
            year=對齊(str(book[3]),6)
            print(f"|{title}|{author}|{publisher}|{year}|")
    return len(c.fetchall())



def 增加記錄():
    '''
    增加記錄
    '''
    title=input("請輸入要新增的標題：")
    author=input("請輸入要新增的作者：")
    publisher=input("請輸入要新增的出版社：")
    year=input("請輸入要新增的年份：")
    if title=='' or author=='' or publisher=='' or year=='':
        raise ValueError("=>給定的條件不足，無法進行新增作業")
    if year.isdigit() ==False:
        raise ValueError("=>年份應是數字")
    if 顯示書籍(title,False)>0:
        raise ValueError("=>已有書籍")
    conn=sqlite3.connect(sql)
    c = conn.cursor()
    c.execute(f"INSERT INTO books (title, author, publisher, year) VALUES ('{title}','{author}','{publisher}','{year}')")
    conn.commit()
    conn.close()
    print("異動 1 記錄")
    顯示書籍()


def 刪除紀錄():
    '''
    刪除紀錄
    '''
    顯示書籍()
    book=input("請問要刪除哪一本書？：")
    conn=sqlite3.connect(sql)
    c = conn.cursor()
    c.execute(f"SELECT title FROM books WHERE title='{book}'")
    if book=='':
        raise ValueError("=>給定的條件不足，無法進行刪除作業")
    if len(c.fetchall())==0:
        raise ValueError("=>沒有這本書")
    c.execute(f"DELETE FROM books WHERE title='{book}'")
    conn.commit()
    conn.close()
    print("異動 1 記錄")
    顯示書籍()


def 查詢():
    '''
    查詢
    '''
    book=input("請輸入想查詢的關鍵字：")
    顯示書籍(book)
    

def 修改紀錄():
    '''
    修改紀錄
    '''
    顯示書籍()
    book=input("請問要修改哪一本書的標題？：")
    title=input("請輸入要更改的標題：")
    author=input("請輸入要更改的作者：")
    publisher=input("請輸入要更改的出版社：")
    year=input("請輸入要更改的年份：")
    conn=sqlite3.connect(sql)
    c = conn.cursor()
    c.execute(f"SELECT title FROM books WHERE title='{book}'")
    if book=='' or title=='' or author=='' or publisher=='' or year=='':
        raise ValueError("=>給定的條件不足，無法進行刪除作業")
    if year.isdigit() ==False:
        raise ValueError("=>年份應是數字")
    if len(c.fetchall())==0:
        raise ValueError("=>沒有這本書")
    if 顯示書籍(title,False)>0 and book != title:
        raise ValueError("=>已有書籍")
    c.execute(f"UPDATE books SET title='{title}', author='{author}', publisher='{publisher}', year='{year}' WHERE title='{book}'")
    conn.commit()
    conn.close()
    print("異動 1 記錄")
    顯示書籍()
