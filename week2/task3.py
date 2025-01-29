def func(*data):
    middle=[] 
    for n in data:
       if len(n) == 2 or len(n) == 3:
           middle.append(n[1])
       elif len(n) == 4 or len(n) == 5:
           middle.append(n[2])
       else:
           middle.append("")    
  
    uniqueMiddle=[]
    for m in middle:
        if middle.count(m) == 1 and n != "":
            uniqueMiddle.append(m)

    uniqueFullName=[]
    for c in data:
        if (len(c)>1 and c[1] in uniqueMiddle) or (len(c)>2 and c[2] in uniqueMiddle) :
            uniqueFullName.append(c)
    
    # 如果沒有獨特的中間字，則印出沒有
    if len(uniqueMiddle) == 0 :
        print("沒有")
    # 如果有獨特的中間字，且比對 data 中的 n 有符合的字，則將 n 加入 uniqueFullName 陣列中，並印出陣列
    else :
        print("、".join(uniqueFullName))      

    # ["靜", "立", "靜", "立", "花"].indexOf(靜) Expected output: "0"
    # ["靜", "立", "靜", "立", "花"].indexOf(立) Expected output: "1"
    # ["靜", "立", "靜", "立", "花"].indexOf(靜) Expected output: "0"
    # ["靜", "立", "靜", "立", "花"].indexOf(立) Expected output: "1"
    # ["靜", "立", "靜", "立", "花"].indexOf(花) Expected output: "4"

func("彭大牆", "陳王明雅", "吳明") # print 彭大牆 
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花 
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有 
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安
func("郭宣雅", "夏曼藍波安", "郭宣恆", "林靜花") # print 夏曼藍波安、林靜花
