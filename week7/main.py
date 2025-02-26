from fastapi import FastAPI, Form, Request
from typing import Annotated
from fastapi.responses import HTMLResponse, JSONResponse, Response, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.datastructures import URL
import logging
import mysql.connector

logging.basicConfig(level=logging.DEBUG)

con=mysql.connector.connect(
    user="root",
    password="abcd",
    host="localhost",
    database="website"
)
print("database ready")

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

app=FastAPI() 

app.add_middleware(SessionMiddleware, secret_key='my-secret-key', https_only=True, max_age=1800)

class myMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print(f"被攔截的請求: {request.method} {request.url}")
        
        session = request.scope.get("session", {})
        logined = session.get("already_login", "false")

        if request.url.path.startswith("/member") and logined != "true":
            return RedirectResponse("/",status_code=302)
        
        response = await call_next(request)
        return response
    
app.add_middleware(myMiddleware)

@app.get("/error")
async def error(request:Request,message: str):
    return templates.TemplateResponse(request=request,name="error.html",context={"message":message})

@app.post("/signup")
async def signup(request:Request):
    data=await request.json()
    name_1=data.get("name_1")   
    username_1=data.get("username_1")
    password_1=data.get("password_1")
    
    if not name_1 or not username_1 or not password_1:
        return RedirectResponse(url="/error?message=請提供所有欄位", status_code=303)

    cursor=con.cursor()
    cursor.execute("SELECT * FROM member WHERE username = %s",[username_1])
    result=cursor.fetchone()
    print(f"查詢結果 result: {result}")

    if result:
        return RedirectResponse(url="/error?message=使用者名稱重複", status_code=303)
    
    cursor.execute("INSERT INTO member(name,username,password) VALUES(%s,%s,%s)",[name_1,username_1,password_1])
    con.commit()

    return RedirectResponse("/",status_code=302)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/signin") 
async def signin(request:Request):
    data=await request.json()
    username_2=data.get("username_2")
    password_2=data.get("password_2")

    if not username_2 or not password_2:
        logging.debug(f"未提供使用者名稱或密碼: username_2={username_2}, password_2={password_2}")
        return RedirectResponse(url="/error?message=請提供使用者名稱和密碼", status_code=400)

    logging.debug(f"收到登入請求：username={username_2}, password={password_2}")

    try:
        cursor=con.cursor()
        cursor.execute("SELECT id,username,password FROM member WHERE username=%s and password=%s",[username_2,password_2])
        result_2=cursor.fetchone()
        print(f"查詢結果 result_2: {result_2}")
        request.session["user_id"] = result_2[0]
        print(f"查詢結果 result_2[0]: {result_2[0]}")
        
        logging.debug(f"查詢結果: {result_2}")
    
        if result_2 :
            request.session["already_login"]="true"
            request.session["username_2"]=username_2
            request.session["user_id"]=result_2[0] 
            print("Session 已設置：", request.session)  
            logging.debug(f"登入成功，Session 設定: {request.session}")
            print("登入成功，session是：",request.session)
            print(f"Redirecting to /member?username={username_2}")

            return RedirectResponse(url=f"/member?username={username_2}", status_code=302)
        else:
            logging.debug(f"登入失敗，未找到匹配的使用者: username={username_2}")
            return RedirectResponse(url="/error?message=使用者名稱或密碼錯誤", status_code=302)
     
    except Exception as e:
        logging.error(f"發生錯誤: {str(e)}")
        return RedirectResponse(url="/error?message=系統錯誤，請稍後再試", status_code=500)
    
@app.patch("/api/member")
async def update_member_name(request: Request):
    logined = request.session.get("already_login")
    if logined != "true":
        return JSONResponse(content={"error": True}, status_code=401)

    data = await request.json()
    new_name = data.get("name")

    if not new_name:
        return JSONResponse(content={"error": True}, status_code=400)

    member_id = request.session.get("user_id")

    cursor = con.cursor()
    cursor.execute("UPDATE member SET name = %s WHERE id = %s", [new_name, member_id])
    con.commit()

    if cursor.rowcount > 0:
        return {"ok": True}
    else:
        return JSONResponse(content={"error": True}, status_code=500)

@app.get("/api/member")
async def get_member(request: Request, username: str):
    logined = request.session.get("already_login")
    
    if logined != "true":
        return JSONResponse(content={"data": None}, status_code=401)  # 未登入

    cursor = con.cursor()
    cursor.execute("SELECT id, name, username FROM member WHERE username = %s", [username])
    result = cursor.fetchone()

    if result:
        member_data = {
            "id": result[0],
            "name": result[1],
            "username": result[2]
        }
        return JSONResponse(content={"data": member_data}, status_code=200)
    
    return JSONResponse(content={"data": None}, status_code=404)

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
    member_id = request.session.get("user_id")
    print(f"登入狀態: {logined}, 使用者名稱: {username_2}, 使用者ID: {member_id}")

    if logined !="true": 
        return RedirectResponse(url="/",status_code=302)

    member_id = request.session["user_id"]
    print(f"取得的 member_id: {member_id}")
    
    cursor = con.cursor()
    cursor.execute("INSERT INTO message (member_id, content) VALUES (%s, %s)", [member_id, content])
    con.commit()
   
    return RedirectResponse(url="/member",status_code=302)

@app.get("/signout")
def signout(request: Request):
    request.session.clear() 
    return RedirectResponse(url="/", status_code=302)


app.mount("/static", StaticFiles(directory="static"), name="static")

