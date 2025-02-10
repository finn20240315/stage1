from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, Response, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
# 引入裝置
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
#
from starlette.routing import Route

app=FastAPI()

templates = Jinja2Templates(directory="templates")

class myMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print(f"被攔截的請求: {request.method} {request.url}")
        # cookie改成session
        logined = request.session.get("already_login")
        if request.url.path.startswith("/member") and logined != "true":
            return RedirectResponse("/",status_code=302)
        
        response = await call_next(request)
        return response
    
app.add_middleware(myMiddleware)
# 印出所有路由
@app.on_event("startup")
async def startup_event():
    print("已經註冊的路由", app.routes)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/signin") # 傳入參數：request: Request
async def signin(request: Request,username: str = Form(...), password: str = Form(...)):
    if username == "test" and password == "test": 
        response = RedirectResponse(url="/member", status_code=302)
        # 將cookie 改成session
        request.session["already_login"] = "true"
        return response
    return RedirectResponse(url="/error?message=登入失敗，請重新輸入", status_code=302)

@app.get("/member")
async def member():
    return HTMLResponse("""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>member</title>
    <link rel="stylesheet" href="/static/style.css" />
  </head>
  <body>
    <h2>歡迎光臨，這是會員頁</h2>
    <h4>恭喜您，成功登入系統</h4>
    <a href="/signout">登出系統</a>
  </body>
</html>""")

@app.get("/signout")
async def signout(request: Request):
    response = RedirectResponse(url="/", status_code=302)
    # 將 cookie 改成 session
    del request.session["already_login"]  
    return response

@app.get("/error")
async def error(message: str):
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>錯誤頁面</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h2>失敗頁面</h2>
        <h4>{message}</h4>
        <a href="/">回到首頁</a>
    </body>
    </html>
    """)


app.mount("/static", StaticFiles(directory="static"), name="static")

# 新增 sessionmiddleware
app.add_middleware(SessionMiddleware, secret_key='my-secret-key', https_only=True, max_age=1800)

