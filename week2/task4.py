def get_number(index): 
    # 0, 4, 8, 7, 11, 15, 14, 18, 22, 21, 25,...
    # 0 ,1, 2, 3,  4,  5,  6,  7,  8,  9, 10,...
    # 0 +4 +4 -1  +4  +4  -1  +4  +4  -1  +4...
    sum=1
    for n in range(index+1):
        if n%3==1 or n%3==2 :
            sum+=4
        else:
            sum-=1
    print(sum)

get_number(1) # print 4 
get_number(5) # print 15 
get_number(10) # print 25 
get_number(30) # print 70