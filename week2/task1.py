def find_and_print(messages, current_station):
    metro = {
        "Songshan": 0,
        "Nanjing Sanmin": 1,
        "Taipei Arena": 2,
        "Nanjing Fuxing": 3,
        "Songjiang Nanjing": 4,
        "Zhongshan": 5,
        "Beimen": 6,
        "Ximen": 7,
        "Xiaonanmen": 8,
        "Chiang Kai-Shek Memorial Hall": 9,
        "Guting": 10,
        "Taipower Building": 11,
        "Gongguan": 12,
        "Wanlong": 13,
        "Jingmei": 14,
        "Dapinglin": 15,
        "Qizhang": 16,
        "Xiaobitan": 15,
        "Xindian City Hall": 17,
        "Xindian": 18,
    }

   
    current_index = metro[current_station]
    nearest_friend = None
    min_distance = float("inf")

    
    for name, message in messages.items():
        for station in metro:
            
            if station in message:
                
                station_index = metro[station] 
                distance = abs(current_index - station_index)  
                if distance < min_distance:
                    
                    min_distance = distance
                    nearest_friend = name  

    
    if nearest_friend:
        print(nearest_friend)
    else:
        print("No friend found.")



messages = {
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Leslie": "I'm at home near Xiaobitan station.",
    "Vivian": "I'm at Xindian station waiting for you.",
}


find_and_print(messages, "Wanlong") # print Mary 
find_and_print(messages, "Songshan") # print Copper 
find_and_print(messages, "Qizhang") # print Leslie 
find_and_print(messages, "Ximen") # print Bob 
find_and_print(messages, "Xindian City Hall") # print Vivian
