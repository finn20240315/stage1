# your code here, maybe 
def book(consultants, hour, duration, criteria): 
    # your code here 
    print("true")
    # hours={1,2,3,4,...,23,24}
    # 用集合的概念，取差集
    # 一天24小時減去已經被預約的時段
    # 巡迴 hours 集合，找出是否有 "參數提供的時段"
    # 時間1小時，取n
    # 時間2小時，取n, n+1
    # 時間3小時，取n, n+1, n+2
    # 若有，印出顧問給使用者，並將 hours 集合畫叉叉

consultants=[ # 他是一個list列表[]不是集合
    {"name":"John", "rate":4.5, "price":1000}, 
    {"name":"Bob", "rate":3, "price":1200}, 
    {"name":"Jenny", "rate":3.8, "price":800} 
    ] 
print(consultants["name"]) # 所以印不出來
# 用in判斷是否在資料裡面

book(consultants, 15, 1, "price") # Jenny 
book(consultants, 11, 2, "price") # Jenny 
book(consultants, 10, 2, "price") # John 
book(consultants, 20, 2, "rate") # John 
book(consultants, 11, 1, "rate") # Bob 
book(consultants, 11, 2, "rate") # No Service 
book(consultants, 14, 3, "price") # John