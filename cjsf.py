import urllib.request as ur
from bs4 import BeautifulSoup
import re
def geturl(url,headears):
    r=ur.urlopen(url)
    text = r.read()
    html = text.decode('utf-8')
    return html

def chuli(html):
    soup = BeautifulSoup(html,'lxml')
    datas = soup.find_all("li")
    books,bookid,booknm,time,chubans = [],[],[],[],[]
    time = re.findall('<p>出版时间： (.*?)</p>',html)
    author = re.findall('<p>作者：(.*?)</p>',html)
    chubans = re.findall('<p>出版社：(.*?)</p>',html)
    for book in datas:
        bookid.append(re.search('"bookid":"(\d*?)"',book.input['value']).group(1))
        booknm.append(re.search('"title":"(.*?)"',book.input['value']).group(1))
    # books = [bookid,booknm,author,chubans,time]
    books = []
    length = min(len(bookid),len(booknm),len(author),len(chubans),len(time))
    for i in range(0,length):
        p = [bookid[i],booknm[i],author[i],chubans[i],time[i]]
        books.append(p)
    page = re.search(r'selected="selected">1/(\d*?)</option>',html)
    if(page is not None):
        return books,int(page.group(1))
    else:
        return books
    

# def suoyou(booklist,books):
#     for i in range(0,5):
#         for k in books[i]:
#                 booklist[i].append(k)
#     return booklist

def main():
    keyword = "python"
    url="http://mlib.yznu.cn:8089/search/searchList?kw="+keyword
    headears = {"User-Agent":" Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
                "Accept-Encoding":" gzip, deflate","Connection":" keep-alive",
                "Cookie":" JSESSIONID=CA421982C51F9A429FA243EC72491D6A"}
    html = geturl(url,headears)
    booklist,pageint = chuli(html)
    for i in range(2,pageint+1):
        url="http://mlib.yznu.cn:8089/search/searchList?kw="+keyword+"&pageIndex="+str(i)
        html = geturl(url,headears)
        # booklist = suoyou(booklist,chuli(html))
        booklist=booklist+chuli(html)
    booklist2 = sorted(booklist,key=lambda time: time[4],reverse=True)
    for i in range(0,10):
        print(booklist2[i])
        

    
    
if __name__=='__main__':
    main()
