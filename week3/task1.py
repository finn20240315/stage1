# 讀取第一個檔案
import urllib.request as req
import json
src="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
with req.urlopen(src) as resp:
    data=json.load(resp)
slist=data["data"]["results"]

# 讀取第二個檔案
import urllib.request as req2
import json
src2="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"
with req2.urlopen(src2) as resp2:
    data2=json.load(resp2)
MRTlist=data2["data"]
# for MRT in MRTlist:
#     print(MRT["address"])
#     print(MRT["SERIAL_NO"])
s="SpotTitle,District,Longitude,Latitude,ImageURL\n"
for spot in slist:
    n=spot["filelist"].lower().find("jpg")
    img=spot["filelist"][0:n+3] 
    # if n != -1 :
    #     print(spot["stitle"] ,img)
    # else:
    #     print(spot["stitle"] ,"No jpg file")
    for MRT in MRTlist:
        if spot["SERIAL_NO"] == MRT["SERIAL_NO"]:
            print("SpotTitle,District,Longitude,Latitude,ImageURL")
            print(spot["stitle"] +"," +MRT["address"][5:8]+","+spot["longitude"]+","+spot["latitude"]+","+img)
            s=s+spot["stitle"] +"," +MRT["address"][5:8]+","+spot["longitude"]+","+spot["latitude"]+","+img+"\n"
            
f=open("spot.csv","w",encoding="utf-8-sig")
f.write(s)
f.close()

# 輸出 mrt.csv

# # for(let i=0;i<slist.length;i++){
# #     m="StationName"
# #     m+=AttractionTitle[i]
# #     print(m)

# m="StationName,AttractionTitle1,AttractionTitle2,AttractionTitle3,...data\n"
# mrt_dict={}
# for spot in slist:
#     for MRT in MRTlist:
#         if MRT["MRT"] not in mrt_dict:
#             mrt_dict[MRT["MRT"]]=[]

#             if MRT["MRT"] in spot["info"]:
#                 mrt_dict[MRT["MRT"]].append(spot["stitle"])
#                 print(mrt_dict)
# for station,spot in mrt_dict.items():
#     print(station,",".join(spot))
#     m+=station+","+",".join(spot)+"\n"
# # m=m+MRT["stationName"] +","+spot["stitle"] +","+spot["xbody"] +","+spot["filelist"]+"\n"
# f=open("mrt.csv","w",encoding="utf-8-sig")
# f.write(m)
# f.close()

###################################################

# 初始資料
mrt_dict = {}

# 迭代每個景點和每個捷運站
for spot in slist:
    for MRT in MRTlist:
        # 檢查是否已經在字典中初始化該捷運站
        if MRT["MRT"] not in mrt_dict:
            mrt_dict[MRT["MRT"]] = set()  # 初始化該捷運站的景點清單

        # 檢查景點的 info 是否包含捷運站名稱
        if MRT["MRT"] in spot["info"]:
            mrt_dict[MRT["MRT"]].add(spot["stitle"])

# 動態生成表頭，最大景點數量
max_attractions = max(len(spots) for spots in mrt_dict.values())  # 找到最多景點數量
headers = ["StationName"] + [f"AttractionTitle{i+1}" for i in range(max_attractions)]  # 表頭

# 初始化 CSV 內容
m = ",".join(headers) + "\n"

# 根據每個捷運站及其景點數量填充 CSV 內容
for station, spots in mrt_dict.items():
    spots=sorted(list(spots))
    # 用空白填充，確保每列的景點數量與最大景點數量對齊
    spots = spots + [""] * (max_attractions - len(spots))
    m += station + "," + ",".join(spots) + "\n"

# 寫入 CSV 檔案
with open("mrt.csv", "w", encoding="utf-8-sig") as f:
    f.write(m)
