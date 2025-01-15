# break, continue 必須寫在迴圈裡面
n=1
while n<5:
    if n==3:
        break
    n+=1
    print(n)
print("done",n)