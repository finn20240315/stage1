# 抓取第一頁標題
import urllib.request as req
import bs4
url="https://www.ptt.cc/bbs/Lottery/index.html"
request=req.Request(url,headers={
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
})
with req.urlopen(request) as response:
    data=response.read().decode("utf-8")

root=bs4.BeautifulSoup(data,"html.parser")
titles=root.find_all("div", class_="title")
# 將"標題"資料定義為列表
titles_collected=[]
likes_collected = [] 
time_collected = [] 

for title in titles:
   if title.a is not None:
        print(title.a.string)
        # 在寫表中加入每個抓到的標題的字串
        titles_collected.append(title.a.string)
        title_href="https://www.ptt.cc"+title.a["href"]
        print(title_href)

        # 抓取每個標題內頁的時間
        inner_request=req.Request(title_href,headers={
            "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
        })
        with req.urlopen(inner_request) as inner_response:
            inner_data=inner_response.read().decode("utf-8")
        
        inner_root=bs4.BeautifulSoup(inner_data,"html.parser")
        time=inner_root.find_all("span", class_="article-meta-value")
        if len(time) > 3:
            print(time[3].string)
            time_collected.append(time[3].string)
        else:
            print("無法抓取時間")
            time_collected.append("無法抓取時間")
   else:
        print(title.string)
        titles_collected.append("無法抓取標題")
        time_collected.append("無法抓取時間")
print("=====================================")

# 抓取按讚數
likes=root.find_all("div", class_="nrec")
for like in likes:
    if like.span is not None:
        print(like.span.string)
        likes_collected.append(like.span.string)
        print(likes_collected)
    else:
        print("0")
        likes_collected.append("0")
# <div class="nrec"></div> #沒有按讚數
# <div class="nrec"><span class="hl f2">8</span></div> #按讚數為8

# 抓取下一頁的網址
href2=root.find_all("a",class_="btn wide")
if len(href2) > 1:
    next_page2="https://www.ptt.cc"+href2[1]["href"]
    print(next_page2)
else:
    print("未找到下一頁按鈕")
    next_page2=None
print("=====================================")

# 抓取第二頁標題(動態的)
if next_page2:
    request=req.Request(next_page2,headers={
        "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
})
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    root=bs4.BeautifulSoup(data,"html.parser")
else:
    print("無法抓取第二頁內容")

titles2=root.find_all("div", class_="title")
for title2 in titles2:
   if title2.a is not None:
        print(title2.a.string)
        # 在寫表中加入每個抓到的標題的字串
        titles_collected.append(title2.a.string)
        title_href2="https://www.ptt.cc"+title2.a["href"]
        print(title_href2)

        # 抓取每個標題內頁的時間
        inner_request2=req.Request(title_href2,headers={
            "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
        })
        with req.urlopen(inner_request2) as inner_response2:
            inner_data2=inner_response2.read().decode("utf-8")
        
        inner_root2=bs4.BeautifulSoup(inner_data2,"html.parser")
        time2=inner_root2.find_all("span", class_="article-meta-value")
        if len(time2) > 3:
            print(time2[3].string)
            time_collected.append(time2[3].string)
        else:
            print("無法抓取時間")
            time_collected.append("無法抓取時間")
   else:
        print(title2.string)
        titles_collected.append("無法抓取標題")
        time_collected.append("無法抓取時間")
print("=====================================")

# 抓取按讚數
likes2=root.find_all("div", class_="nrec")
for like2 in likes2:
    if like2.span is not None:
        print(like2.span.string)
        likes_collected.append(like2.span.string)
        print(likes_collected)
    else:
        print("0")
        likes_collected.append("0")
# <div class="nrec"></div> #沒有按讚數
# <div class="nrec"><span class="hl f2">8</span></div> #按讚數為8



# 抓取下一頁的網址
href3=root.find_all("a",class_="btn wide")
if len(href3) > 1:
    next_page3="https://www.ptt.cc"+href3[1]["href"]
    print(next_page3)
else:
    print("未找到下一頁按鈕")
    next_page3=None
print("=====================================")

# 抓取第三頁標題(動態的)
if next_page3:
    request=req.Request(next_page3,headers={
        "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
})
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    root=bs4.BeautifulSoup(data,"html.parser")
else:
    print("無法抓取第三頁內容") 

titles3=root.find_all("div", class_="title")
for title3 in titles3:
   if title3.a is not None:
        print(title3.a.string)
        # 在寫表中加入每個抓到的標題的字串
        titles_collected.append(title3.a.string)
        title_href3="https://www.ptt.cc"+title3.a["href"]
        print(title_href3)

        # 抓取每個標題內頁的時間
        inner_request3=req.Request(title_href3,headers={
            "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
        })
        with req.urlopen(inner_request3) as inner_response3:
            inner_data3=inner_response3.read().decode("utf-8")
        
        inner_root3=bs4.BeautifulSoup(inner_data3,"html.parser")
        time3=inner_root3.find_all("span", class_="article-meta-value")
        if len(time3) > 3:
            print(time3[3].string)
            time_collected.append(time3[3].string)
        else:
            print("無法抓取時間")
            time_collected.append("無法抓取時間")
   else:
        print(title3.string)
        titles_collected.append("無法抓取標題")
        time_collected.append("無法抓取時間")
print("=====================================")

# 抓取按讚數
likes3=root.find_all("div", class_="nrec")
for like3 in likes3:
    if like3.span is not None:
        print(like3.span.string)
        likes_collected.append(like3.span.string)
        print(likes_collected)
    else:
        print("0")
        likes_collected.append("0")

# 輸出 artical.csv
a="ArticleTitle,Like/DislikeCount,PublishTime\n"
for title, like, time in zip(titles_collected, likes_collected, time_collected):
    a +=  f"{title},{like},{time}\n"
# for t in titles_collected:
    # a+=t+",0,"
# a+=title.a.string +title2.a.string +title3.a.string +",0,0\n"
# s=s+spot["stitle"] +"," +MRT["address"][5:8]+","+spot["longitude"]+","+spot["latitude"]+","+img+"\n"

try:
    with open("artical.csv","w",encoding="utf-8-sig") as f:
        f.write(a)
    print("檔案輸出成功")
except Exception as e:
    print("檔案輸出失敗" + str(e))   
