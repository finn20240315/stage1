def find_and_print(messages, current_station): 
    for person,says in messages.items():
    # 巡迴 messages 裡面的鍵值對
        m_index=0
        c_index=0
        distance_list=[]
        for station,number in metro.items():
            if station in says:
            # 如果 metro 的 station 在 messages 的值裡面 (一定在裡面的阿???)
                m_index=number
                # 將 metro 的值 number
                print("訊息中的",station ,"索引是： ",m_index)
            # number 是 messages 的車站索引
            # 後續進行其他計算
            if current_station in station:
            # 如果參數(Xiaobitan)在訊息Leslie(Xiaobitan)中
            # 如果參數(Xiaobitan)在訊息Bob(Ximen)中
            # 如果參數(Xiaobitan)在訊息Bob(Ximen)中
            # 如果參數(Xiaobitan)在訊息Bob(Ximen)中
                c_index=number
                print("參數中的",station,"索引是： ",c_index)
            distance=abs(m_index-c_index)
            #print("距離是: ",distance)
            distance_list.append(distance)
            #print("距離的列表是: ",distance_list)
    
# 巡迴字典的資料，
# {}字典dict、[]列表list、()元祖tuple
messages={ 
    "Leslie":"I'm at home near Xiaobitan station.", 
    "Bob":"I'm at Ximen MRT station.", 
    "Mary":"I have a drink near Jingmei MRT station.", 
    "Copper":"I just saw a concert at Taipei Arena.", 
    "Vivian":"I'm at Xindian station waiting for you." 
    } 

metro={
    "Songshan": 0,
    "Nanjing Sanmin": 1,
    "Taipei Arena": 2,
    "Zhongxiao Fuxing": 3,
    "Ximen": 4,
    "Chiang Kai-Shek Memorial Hall": 5,
    "Wanlong": 6,
    "Jingmei": 7,
    "Qizhang": 8,
    "Xiaobitan": 9,
    "Xindian City Hall": 10,
    "Xindian": 11
}
        

find_and_print(messages, "Xiaobitan") # print Mary 
# find_and_print(messages, "Songshan") # print Copper 
# find_and_print(messages, "Qizhang") # print Leslie 
# find_and_print(messages, "Ximen") # print Bob 
# find_and_print(messages, "Xindian City Hall") # print Vivian