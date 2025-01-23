def func(*data):
    middle=[] 
    for n in data:
       if len(n) == 2 or len(n) == 3:
           middle.append(n[1])
       elif len(n) == 4:
           middle.append(n[2])
       elif len(n) == 5:
           middle.append(n[2])
  
    uniqueMiddle=[]
    for n in middle:
        if middle.count(n) == 1:
            uniqueMiddle.append(n)

    # 將 uniqueMiddle 比對回 middle 的位置再比對回 data 陣列?
    # 將 uniqueMiddle 比對回 data 中的 n 
    # 如果 len(n)=2 比對 n[1]
    # 如果 len(n)=3 比對 n[1]
    # 如果 len(n)=4 比對 n[2]
    # 如果 len(n)=5 比對 n[2]
    
    uniqueFullName=[]
    for n in data:
        if n[1] in uniqueMiddle or (len(n)>2 and n[2] in uniqueMiddle) :
            uniqueFullName.append(n)
    
    # 如果沒有獨特的中間字，則印出沒有
    if len(uniqueMiddle) == 0 :
        print("沒有")
    # 如果有獨特的中間字，且比對 data 中的 n 有符合的字，則將 n 加入 uniqueFullName 陣列中，並印出陣列
    else :
        print(uniqueFullName)      

    # ["靜", "立", "靜", "立", "花"].indexOf(靜) Expected output: "0"
    # ["靜", "立", "靜", "立", "花"].indexOf(立) Expected output: "1"
    # ["靜", "立", "靜", "立", "花"].indexOf(靜) Expected output: "0"
    # ["靜", "立", "靜", "立", "花"].indexOf(立) Expected output: "1"
    # ["靜", "立", "靜", "立", "花"].indexOf(花) Expected output: "4"

func("彭大牆", "陳王明雅", "吳明") # print 彭大牆 
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花 
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有 
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安