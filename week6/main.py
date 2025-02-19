# 引入 FastAPI 的核心功能
from fastapi import FastAPI, Form, Request
# FastAPI：建立 Web 應用的核心類別
# Form：用於處理 HTML 表單提交的數據（application/x-www-form-urlencoded）
# Request：表示 HTTP 請求，允許存取請求的標頭、Cookies、Session 等資訊

# 引入 FastAPI 的回應類別
from typing import Annotated
from fastapi.responses import HTMLResponse, Response, RedirectResponse, FileResponse
# HTMLResponse：回傳 HTML 內容的 Response
# Response：最基本的 HTTP 回應類別，可自訂 headers、status code 等
# RedirectResponse：用於 重新導向（HTTP 302/303），例如登入成功後導向 /member
# FileResponse：用來回傳靜態檔案，例如圖片、PDF 等

from fastapi.staticfiles import StaticFiles
# StaticFiles：用來掛載靜態檔案（CSS、JS、圖片）

from fastapi.templating import Jinja2Templates
# Jinja2Templates：使用 Jinja2 模板引擎來渲染 HTML 頁面

# 引入 Middleware（中介軟體）
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
# BaseHTTPMiddleware：用來攔截並處理請求，例如 檢查使用者是否登入，若未登入則導回 /。
# Middleware：定義一個中介軟體列表，但這裡沒有用到
# SessionMiddleware：提供 Session 功能，用來 存儲登入狀態

import mysql.connector
con=mysql.connector.connect(
    user="root",
    password="abcd",
    host="localhost",
    database="website"
)
print("database ready")

app=FastAPI() # 等於 app = Flask(__name__)

@app.post("/signup")
def signup(name_1:Annotated[str,Form(...)],username_1:Annotated[str,Form(...)],password_1:Annotated[str,Form(...)]):
    cursor=con.cursor()
    cursor.execute("SELECT * FROM member WHERE username = %s",[username_1])
    result=cursor.fetchone()

    if result is not None:
        return RedirectResponse(url="/error?message=使用者名稱重複", status_code=302)

    cursor.execute("INSERT INTO member(name,username,password) VALUES(%s,%s,%s)",[name_1,username_1,password_1])
    con.commit()
    return RedirectResponse("/",status_code=302)

templates = Jinja2Templates(directory="templates")
# 這行程式碼 指定 templates/ 資料夾作為模板目錄
# 所以 modelues=jinja2templates(directory="templates" 是指定modeules資料夾嗎?

class myMiddleware(BaseHTTPMiddleware):
# 定義 middleware 類別，並且繼承 BaseHTTPMiddleware，讓這個類別擁有攔截請求的功能
    async def dispatch(self, request, call_next):
    # dispatch 是 BaseHTTPMiddleware 的 內建方法，攔截每個請求，語法：async def dispatch(self, request, call_next):
    # self：代表這個類別（myMiddleware）的實例，self 代表目前的 myMiddleware 物件
    # request：是請求物件，表示請求以下資訊：URL、方法（GET、POST）、cookie、session
    # call_next(request)：代表將請求傳遞給下一個 Middleware 或路由處理函式
        print(f"被攔截的請求: {request.method} {request.url}")
        # request.method：GET, request.url：http://127.0.0.1:8000/member

        # cookie改成session
        logined = request.session.get("already_login")
        # request 是 請求物件，包含使用者的請求資訊
        # 如果 already_login 存在，回傳 true；如果沒有，回傳 None
        if request.url.path.startswith("/member") and logined != "true":
        # 如果使用者未想要訪問 "/member" 頁面，但是登入不等於 true
        # request.url.path 代表請求的路徑...
        # starswith：表示網址若是 "/member" 開頭...
            return RedirectResponse("/",status_code=302)
            # 被重新導回 "/"
            # 這是 HTTP 302 Found 狀態碼，表示 "暫時重新導向"
            # 302跟301的差別是啥？
        
        response = await call_next(request)
        # 如果使用者已登入，就讓請求繼續進行，交給下一個 Middleware 或 FastAPI 路由處理函式
        return response
    
app.add_middleware(myMiddleware)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    # 載入 index.html 檔案，並傳入 request 物件
    # 傳入什麼東西給 request? request物件是啥?

@app.post("/signin") # 傳入參數：request: Request
def signin(request:Request,username_2: str = Form(...), password_2: str = Form(...)):
    cursor=con.cursor()
    cursor.execute("SELECT username,password FROM member WHERE username=%s and password=%s",[username_2,password_2])
    result_2=cursor.fetchone()

    if result_2 :
        request.session["already_login"]="true"
        request.session["username_2"]=username_2
        print("這是session",request.session)
        return RedirectResponse(url=f"/member?username={username_2}",status_code=302)
    
    return RedirectResponse(url="/error?message=使用者名稱或密碼錯誤", status_code=302)

@app.get("/member")
def member(request: Request):
    logined=request.session.get("already_login")
    username_2=request.session.get("username_2")
    
    if logined != "true":
        return RedirectResponse(url="/",status_code=302)
    
    cursor=con.cursor()
    cursor.execute("SELECT id FROM member WHERE username=%s",[username_2])
    member_id=cursor.fetchone()

    if not member_id:
        return RedirectResponse(url="/error?message=使用者不存在", status_code=302)

    # 這裡要在進入 /member 頁面時即查詢留言資料
    cursor.execute("SELECT member.username, message.content FROM member JOIN message ON member.id = message.member_id")
    all_content = cursor.fetchall()
    print("在'/member'裡的所有留言：",all_content)

    return templates.TemplateResponse("member.html", {
        "request": request,
        "username": username_2,
        "all_content": all_content  # 傳遞留言資料
    })

@app.post("/createMessage")
def createMessage(request: Request,content:Annotated[str,Form(...)]):
    logined = request.session.get("already_login")
    username_2 = request.session.get("username_2")
    print(f"登入狀態: {logined}, 使用者名稱: {username_2}")

    if logined !="true":
        return RedirectResponse(url="/",status_code=302)

    cursor=con.cursor()
    cursor.execute("SELECT id FROM member WHERE username=%s",[username_2])
    member_id=cursor.fetchone()
    print("使用者id：",member_id)

    if not member_id:
        return RedirectResponse(url="/error?message=使用者不存在", status_code=302)

    cursor.execute("INSERT INTO message(member_id,content) VALUES(%s,%s)",[member_id[0],content])
    con.commit()
    cursor.execute("SELECT member.username,message.content FROM member JOIN message ON member.id=message.member_id")
    all_content=cursor.fetchall()

    print("所有留言：",all_content)

    return templates.TemplateResponse("member.html", {
        "request": request,
        "username": username_2,
        "all_content": all_content  # 傳遞所有留言
    })

@app.get("/signout")
def signout(request: Request):
    # 將 cookie 改成 session
    request.session.clear() # 會刪除 session 裡的全部資訊，包括 already_login、username 等
    return RedirectResponse(url="/", status_code=302)

@app.get("/error")
async def error(request:Request,message: str):
    return templates.TemplateResponse(request=request,name="error.html",context={"message":message})

app.mount("/static", StaticFiles(directory="static"), name="static")

# 新增 sessionmiddleware
app.add_middleware(SessionMiddleware, secret_key='my-secret-key', https_only=True, max_age=1800)
# 使用 SessionMiddleWare 來管理登入狀態(取代cookie)
# secret_key='my-secret-key' 用於加密 Session 資料
# max_age=1800（30 分鐘）表示 Session 1800 秒後失效，單位是什麼?
# https_only=True 這是甚麼?

# 在 cdm 中止 uvicorn 作業
# taskkill /F /IM python.exe
