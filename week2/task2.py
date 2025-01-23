def book(consultants, hour, duration, criteria):
    # print("初始資料: ", hour, duration, criteria)
    # 排序顧問依據條件 (price 或 rate)
    if criteria == "price":
        consultants.sort(key=lambda c: c["price"])  # 按 price 從低到高排序
    elif criteria == "rate":
        consultants.sort(key=lambda c: c["rate"], reverse=True)  # 按 rate 從高到低排序

    # 模擬每位顧問的已預約時間表
    for c in consultants:
        if "appointments" not in c:
            c["appointments"]=[0]*24
            # print(c)

        start = hour
        end = hour + duration
        # print("嘗試預約顧問: ", c["name"], "預約時間: ", start, end)

        available = True  # 假設可預約
        for i in range(start,end):
            if c["appointments"][i]==1:
                # print(c["name"], "時間段", start, "-", end, "已被預約")
                available = False  # 無法預約
                break
        if available:
            # 如果這位顧問可預約，標記時間為已預約並跳出外層迴圈
            for i in range(start, end):
                c["appointments"][i] = 1  # 標記時間段為已預約
            # print("----------------------")
            print(c["name"])
            # print("----------------------")
            # print("更新的預約時間表：", c["appointments"])
            return  # 跳出函數，結束處理
    # 如果所有顧問都無法預約，打印無服務
    print("No Service")


consultants = [
    {"name": "John", "rate": 4.5, "price": 1000},
    {"name": "Bob", "rate": 3, "price": 1200},
    {"name": "Jenny", "rate": 3.8, "price": 800}
]


book(consultants, 15, 1, "price") # Jenny 
book(consultants, 11, 2, "price") # Jenny 
book(consultants, 10, 2, "price") # John 
book(consultants, 20, 2, "rate") # John 
book(consultants, 11, 1, "rate") # Bob 
book(consultants, 11, 2, "rate") # No Service 
book(consultants, 14, 3, "price") # John



