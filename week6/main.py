from fastapi import FastAPI, Form, Request
from typing import Annotated
from fastapi.responses import HTMLResponse, Response, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

import mysql.connector
con=mysql.connector.connect(
    user="root",
    password="abcd",
    host="localhost",
    database="website"
)
print("database ready")

app=FastAPI() 

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

class myMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print(f"被攔截的請求: {request.method} {request.url}")
        
        logined = request.session.get("already_login")
        
        if request.url.path.startswith("/member") and logined != "true":
            return RedirectResponse("/",status_code=302)
        
        response = await call_next(request)
        return response
    
app.add_middleware(myMiddleware)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/signin")
def redirect_signin():
    return RedirectResponse(url="/",status_code=302)
       
@app.post("/signin") 
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
    cursor.execute("SELECT member.username, message.content FROM member JOIN message ON member.id = message.member_id")
    all_content = cursor.fetchall()
    print("在'/member'裡的所有留言：",all_content)

    return templates.TemplateResponse("member.html", {
        "request": request,
        "username": username_2,
        "all_content": all_content  
    })
    
@app.get("/createMessage")
def redirect_createMessage():
    return RedirectResponse(url="/",status_code=302)
  
@app.post("/createMessage")
def createMessage(request: Request,content:Annotated[str,Form(...)]):
    logined = request.session.get("already_login")
    username_2 = request.session.get("username_2")
    print(f"登入狀態: {logined}, 使用者名稱: {username_2}")

    if logined !="true": 
        return RedirectResponse(url="/",status_code=302)

    cursor=con.cursor() # 建立 cursor 物件
    cursor.execute("SELECT id FROM member WHERE username=%s",[username_2])
    member_id=cursor.fetchone()[0]
    print("使用者id：",member_id)

    cursor.execute("INSERT INTO message(member_id,content) VALUES(%s,%s)",[member_id,content])
    con.commit()
   
    return RedirectResponse(url="/member",status_code=302)

@app.get("/signout")
def signout(request: Request):
    request.session.clear() # 會刪除 session 裡的全部資訊，包括 already_login、username 等
    return RedirectResponse(url="/", status_code=302)

@app.get("/error")
async def error(request:Request,message: str):
    return templates.TemplateResponse(request=request,name="error.html",context={"message":message})

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(SessionMiddleware, secret_key='my-secret-key', https_only=True, max_age=1800)
