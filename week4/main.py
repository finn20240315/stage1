from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, Response, RedirectResponse, FileResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app=FastAPI()

templates = Jinja2Templates(directory="templates")

class myMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print(f"被攔截的請求: {request.method} {request.url}")
        
        logined = request.cookies.get("already_login")
        if request.url.path.startswith("/member") and logined != "true":
            return RedirectResponse("/",status_code=302)
        
        response = await call_next(request)
        return response
    
app.add_middleware(myMiddleware)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/signin")
async def signin(username: str = Form(...), password: str = Form(...)):
    if username == "test" and password == "test": 
        response = RedirectResponse(url="/member", status_code=302)
        response.set_cookie(key="already_login", value="true")  
        return response
    return RedirectResponse(url="/error?message=登入失敗，請重新輸入", status_code=302)

@app.get("/member", response_class=HTMLResponse)
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
async def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("already_login")  
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
