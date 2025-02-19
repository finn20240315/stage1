
# ✨ Week5 - Python FastAPI ✨ Memo ✒️
### 📍 Static Files 靜態檔案 
### 語法：
```
from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles 

app = FastAPI() 

app.mount("/static", StaticFiles(directory="static"),name="static")
```
- 從 FastAPI 套件中導入 FastAPI 模組
- 從 FastAPI 套件中導入靜態檔案類別
- 建立一個 FastAPI 應用實例 app
- 掛載一個靜態檔案目錄 (mount)，讓使用者能夠透過 URL 存取靜態檔案
  - 路徑前綴 "/static"
### 📍 Jinja2 Templates 神社模板
### 📍 http status
狀態碼（Status Code）：如 
 - 200 OK
 - 404 Not Found
 - 500 Internal Server Error
 - 302 Found（預設）：臨時重定向
   - 作用：告訴瀏覽器：「這個網址暫時變更」，但舊網址仍然有效
   - 瀏覽器行為：不會記住新網址，下次還是請求舊網址
 - 301 Moved Permanently：永久重定向
   - 作用：告訴瀏覽器：「這個網址永久變更」，以後請求新網址
   - 瀏覽器行為：瀏覽器會記住新網址，下次直接訪問新網址
 - 307 Temporary Redirect
 - 308 Permanent Redirect：保留請求方法的重定向

### 📍 From Data 表單數據
### 📍 建立路由
 - 基本路由
   - `@app.get("/")`
 - Query Parameters 要求字串<br>
   - `@app.get("/search?q=abc")`
 - Path Parameters 路徑參數
   - `@app.get("/users/{user_id}")`
### 📍 Custom Response - HTML, Stream, File, others 自訂回應
### 📍 SessionMiddleWare 會話中介軟體
### 📍 CORSMiddleWare CORS中介軟體
### 📍 MiddleWare 中介軟體
### 📍 Advanced Middleware 進階中介軟體
* Adding ASGI middlewares
* Integrated middlewares
* HTTPSRedirectMiddleware
* TrustedHostMiddleware
* GZipMiddleware

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

### **為什麼不直接使用 `SessionMiddleware` 來管理 session 的登入狀態？**  

其實，**`SessionMiddleware` 本來就是用來處理 session 的，它負責讓我們能夠存取 `request.session`**，但是它**不會自動管理登入狀態**，所以我們才需要自己定義一個 Middleware 來做登入驗證。

---

### **`SessionMiddleware` 的主要功能**
- **讓我們能夠使用 `request.session` 來存取 session 資料**
- **自動處理 Cookie**（把 session 存在瀏覽器 Cookie）
- **不會自動檢查使用者是否登入**
- **不會攔截 `/member` 頁面並導向 `/`**

舉個例子，如果我們只使用 `SessionMiddleware`：
```python
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# 加入 SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key="my-secret-key", max_age=1800)

@app.get("/")
async def home(request: Request):
    return {"message": "這是首頁"}

@app.get("/member")
async def member(request: Request):
    logined = request.session.get("already_login")
    return {"message": f"登入狀態: {logined}"}
```
**問題：**
- 這樣的程式碼雖然能讓我們存取 `request.session`，但 `/member` 這個路由**並不會自動檢查是否登入**，也不會幫我們重導向 `/`。
- 也就是說，**即使沒有登入，使用者還是可以直接進入 `/member` 頁面**。

---

### **為什麼我們要自訂 Middleware 來管理登入？**
因為 `SessionMiddleware` **只是提供 session 功能**，它不會幫我們**自動攔截未登入的請求**。  
我們可以自己定義一個 Middleware，來負責登入驗證：
```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

app = FastAPI()

# 加入 SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key="my-secret-key", max_age=1800)

# 自訂 Middleware 來攔截未登入的請求
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logined = request.session.get("already_login")

        # 如果使用者訪問 /member，但 session 中沒有登入資訊，就重導向 /
        if request.url.path.startswith("/member") and logined != "true":
            return RedirectResponse("/", status_code=302)

        response = await call_next(request)
        return response

# 加入我們的自訂 Middleware
app.add_middleware(AuthMiddleware)

@app.get("/")
async def home(request: Request):
    return {"message": "這是首頁"}

@app.get("/signin")
async def signin(request: Request):
    request.session["already_login"] = "true"
    return {"message": "登入成功"}

@app.get("/signout")
async def signout(request: Request):
    request.session.pop("already_login", None)
    return {"message": "登出成功"}

@app.get("/member")
async def member(request: Request):
    return {"message": "歡迎來到會員頁面"}
```

**這樣做的好處：**
1. **確保未登入的使用者無法訪問 `/member` 頁面**，會被重導到 `/`。
2. **讓 `SessionMiddleware` 處理 session，讓 `AuthMiddleware` 處理登入驗證**，分工明確。
3. **靈活性更高**，如果未來要修改驗證邏輯（例如增加 JWT Token 驗證），我們只需要修改 `AuthMiddleware`，不用改整個專案。

---

### **結論**
1. **`SessionMiddleware` 只是提供 session 功能，並不會自動檢查登入狀態。**
2. **我們需要自訂 Middleware (`AuthMiddleware`) 來攔截未登入的請求，確保未登入的使用者無法訪問 `/member`。**
3. **`SessionMiddleware` + `AuthMiddleware` 搭配使用，才是一個完整的登入驗證解決方案。**

這樣應該比較清楚了吧？😃

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

這些問題都很關鍵，牽涉到 **安全性** 和 **系統設計**，我來詳細解釋每個部分！🔥

---

## **1️⃣ 駭客可以偽造 session 嗎？**
🚨 **不能輕易偽造！因為 session 不是隨便一個變數，而是儲存在伺服器的安全機制！**

### **🛡 為什麼 session 安全？**
FastAPI 的 `SessionMiddleware` **會自動加密 session，並存放在瀏覽器的 cookie 裡**，所以：
1. **駭客無法直接修改 session 的內容**  
   - session 存在 cookie，但它是經過加密的，**駭客不能隨便改變 username**。
   - 如果駭客試圖改變 session 的值，例如 `"username": "admin"`，伺服器會發現加密內容不匹配，拒絕請求。

2. **伺服器端驗證 session**  
   - session 的真正內容是存在 **伺服器的記憶體 (RAM) 或資料庫**，不是只在瀏覽器上！
   - 每次請求時，瀏覽器 **只是帶著 session ID**，伺服器會對應 session 內容並檢查使用者身份。

### **🛑 那駭客可以盜取 session 嗎？**
理論上，如果駭客 **成功竊取 session ID**，的確可以冒充該使用者（這叫做 **Session Hijacking**，會話劫持）。但我們可以 **用以下方式防範**：
✅ **設置 `httpOnly=True`**（你的程式碼已經有了）：  
   ```python
   app.add_middleware(SessionMiddleware, secret_key='my-secret-key', https_only=True, max_age=1800)
   ```
   - `httpOnly=True`：讓 **JavaScript 不能存取 session**，避免 XSS 攻擊（跨站腳本攻擊）。
   - `https_only=True`：要求 **HTTPS 傳輸**，防止駭客用「中間人攻擊 (MITM)」來竊取 session。

✅ **設置 `max_age` 限制 session 有效時間**（你已設為 30 分鐘）：  
   ```python
   max_age=1800  # 1800秒 (30分鐘)
   ```
   - 如果駭客真的偷到 session，也只能用 30 分鐘，過期後 session 會失效。

✅ **使用 IP 綁定 session**（更安全）：  
   - 可以在 session 裡存 **使用者的 IP**，每次請求時檢查 IP 是否一致：
   ```python
   user_ip = request.client.host
   request.session["user_ip"] = user_ip
   ```
   - 在 `/member` 檢查：
   ```python
   if request.session.get("user_ip") != request.client.host:
       return RedirectResponse(url="/signout", status_code=302)
   ```

---

## **2️⃣ 如果不用 HTTP 302 重定向，還需要 session 嗎？**
### **🔹 可以不用 302，但還是要 session**
- **`302 RedirectResponse` 只是讓瀏覽器跳轉**，本質上不影響 session 的必要性。
- 你可以讓 `/signin` **直接回傳 HTML 頁面**，但問題是：  
  - **登入後，怎麼知道使用者是誰？**
  - **每次請求都要重新查資料庫？這樣效能會變慢！**

### **🔹 如果完全不用 session，怎麼設計？**
- 你可以 **每次請求都讀取 database**：
  ```python
  @app.get("/member")
  def member(request: Request):
      cursor = con.cursor()
      username = request.query_params.get("username")  # 透過 URL 取得 username
      cursor.execute("SELECT * FROM member WHERE username=%s", [username])
      user = cursor.fetchone()
      if not user:
          return RedirectResponse(url="/", status_code=302)
      return templates.TemplateResponse("member.html", {"request": request, "username": username})
  ```
  **但這很不安全！**
  - **任何人都能在網址列改 username，偽造登入！**
  - 每次請求都要查詢資料庫，**效能降低！**
  - URL 會暴露使用者資訊，**不安全！**

✅ **最好的方法還是用 session！**  
   - session **只存已登入的使用者資訊**，不影響資料庫效能。  
   - session **不能被用戶修改**，確保安全。

---

## **3️⃣ 既然有資料庫，為什麼還要 session？**
雖然我們可以直接從 **資料庫檢查使用者身份**，但 **session 有以下優勢**：

### **🛠 用 session 可以減少資料庫負擔**
1. **如果沒用 session，每次請求都要查資料庫！**
   ```python
   cursor.execute("SELECT * FROM member WHERE username=%s", [username])
   ```
   這樣伺服器的 **CPU 和資料庫負擔很大**，使用者多時，系統會變慢。

2. **session 讓已登入的用戶不用一直查資料庫**
   - 只在「登入時」查詢一次，之後的請求直接從 **session** 取得資訊，效能更好！
   - 例如：
   ```python
   request.session["username"] = username_2
   ```

### **🛠 session 讓登入狀態持續**
- **session 讓使用者「關閉網頁再回來」時仍然登入**
- 如果只靠資料庫，每次重新打開網站都要重新登入，很麻煩！

### **🛠 session 可以儲存更多資訊**
- 你可以在 session **存會員等級、購物車、偏好設定**：
  ```python
  request.session["user_level"] = "VIP"
  request.session["cart"] = ["item1", "item2"]
  ```

---

## **🔥 總結**
1. **駭客不能輕易偽造 session**，因為：
   - session **被加密**，不能隨便修改。
   - `httpOnly`、`https_only` 限制 session 存取方式。
   - 可以 **綁定 IP** 來避免 session 被盜用。

2. **不用 302 也可以登入，但還是需要 session**
   - `302 RedirectResponse` 只是跳轉方式，跟 session 不是強制關聯。
   - 但如果不用 session，就 **每次請求都要查資料庫，效能會變差**。

3. **有了資料庫，為什麼還要 session？**
   - session 讓使用者登入後，不用每次請求都重新查資料庫，**效能更高**。
   - session 可以讓使用者 **保持登入狀態**，不需要重新輸入密碼。
   - session 可以存放 **額外資訊**（例如會員等級、購物車），提供更好的使用者體驗。

---

### **🔹 簡單說：**
🚀 **資料庫用來存「長期」的會員資料，session 用來存「短期」的登入狀態！**  
🚀 **用 session 讓網站更安全、更快速！** 🔥

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

這些都是很棒的問題！讓我們一個一個來解釋 🚀  

---

## **1️⃣ `request.session.clear()` 跟 `del request.session["already_login"]` 的差別是什麼？**
| 方法 | 功能 | 影響範圍 |
|------|------|------|
| `request.session.clear()` | 清除 **所有** session 資料 | **會刪除 session 裡的全部資訊**，包括 `already_login`、`username` 等 |
| `del request.session["already_login"]` | 只刪除 `already_login` | 只會刪除 **特定的 session 鍵值**，其他的 session（例如 `username`）還會保留 |

**🔹 使用情境**
- **登出時**，一般用 `request.session.clear()`，因為要刪掉所有登入資訊。  
- **如果只是單純刪除某個 session 資料**，可以用 `del request.session["already_login"]`。  

✅ **最佳作法**：建議 **登出時直接用 `clear()`，這樣比較乾淨！**

---

## **2️⃣ `if logined != "true"`, `if logined != True`, `if logined is not True`, `if logined is not None` 的差別？**

### **🚀 這些條件語法的差異**
```python
logined = request.session.get("already_login")  # 假設 logined 可能是 "true"、True 或 None
```
| 條件語法 | 作用 | 可能會有的問題 |
|---------|------|----------------|
| `if logined != "true":` | 檢查 `logined` 是否 **不是** 字串 `"true"` | 但如果 `logined` 存的是 `True`（布林值），這條件不會成立 ❌ |
| `if logined != True:` | 檢查 `logined` 是否 **不是** 布林值 `True` | 但如果 `logined` 存的是 `"true"`（字串），這條件不會成立 ❌ |
| `if logined is not True:` | 檢查 `logined` 是否不是 `True`（布林值） | 但 `logined = None` 或 `logined = "true"` 時，這條件都成立 |
| `if logined is not None:` | **檢查 session 是否有存東西（不管是 "true" 還是 True）** | **這是最通用的寫法** ✅ |

**✅ 最好的寫法**
```python
if logined is not None:
```
因為這樣不管 `logined` 是 `"true"` 還是 `True`，只要有值都會被當成「登入狀態存在」。

---

## **3️⃣ 為什麼在 `/member` 不需要傳入 `username: str = None`？**
這裡的 **`username` 可以直接從 session 取得**，所以 **不需要當作參數傳入**！

### **🔹 錯誤做法（不必要的 `username` 參數）**
```python
@app.get("/member")
def member(request: Request, username: str = None):  # ❌ username 其實不用傳入
    logined = request.session.get("already_login")
    if logined != "true":
        return RedirectResponse(url="/", status_code=302)

    return templates.TemplateResponse("member.html", {"request": request, "username": username})
```
這樣的問題是：
1. **`username` 參數其實不需要從網址傳入**，因為我們可以從 session 取得。
2. **如果 `username` 來自網址參數，駭客可以竄改網址，偽裝成別人！**

### **✅ 正確做法**
```python
@app.get("/member")
def member(request: Request):
    logined = request.session.get("already_login")
    username = request.session.get("username")  # 直接從 session 取得使用者名稱

    if logined != "true":
        return RedirectResponse(url="/", status_code=302)

    return templates.TemplateResponse("member.html", {"request": request, "username": username})
```
這樣就確保 **`username` 一定來自 session，而不是網址**，更安全！

---

## **4️⃣ 不能在 `/member` 再次進入資料庫查詢嗎？**
當然可以！但 **不一定有必要**。

### **🔹 直接使用 session（通常夠用）**
```python
@app.get("/member")
def member(request: Request):
    logined = request.session.get("already_login")
    username = request.session.get("username")

    if logined != "true":
        return RedirectResponse(url="/", status_code=302)

    return templates.TemplateResponse("member.html", {"request": request, "username": username})
```
這樣的好處是：
1. **速度快**：session 存在記憶體中，不需要每次都查資料庫。
2. **減少資料庫負擔**。

### **🔹 但如果要確保使用者帳戶還有效，的確可以查詢資料庫**
```python
@app.get("/member")
def member(request: Request):
    logined = request.session.get("already_login")
    username = request.session.get("username")

    if logined != "true":
        return RedirectResponse(url="/", status_code=302)

    # 檢查資料庫，確認這個帳號仍然存在
    cursor = con.cursor()
    cursor.execute("SELECT * FROM member WHERE username = %s", [username])
    user = cursor.fetchone()
    
    if not user:  # 如果找不到該帳號，登出並回到首頁
        request.session.clear()
        return RedirectResponse(url="/", status_code=302)

    return templates.TemplateResponse("member.html", {"request": request, "username": username})
```
這樣的好處是：
1. 如果使用者帳戶被刪除，他就 **無法再用舊的 session 存取會員頁面**。
2. 更安全，但 **會增加一點資料庫負擔**。

✅ **如果使用者帳號可能會被刪除，建議加上資料庫查詢**！

---

## **5️⃣ 設定 `/member` 路由的原因是怕使用者直接輸入網址嗎？**
是的！這是為了 **防止未登入的使用者直接輸入 `/member` 來繞過登入**。

### **❌ 錯誤作法（未檢查 session，可能被繞過）**
```python
@app.get("/member")
def member(request: Request):
    return templates.TemplateResponse("member.html", {"request": request})
```
這樣的問題是：
1. **任何人都能直接輸入 `/member` 並進入會員頁面！** 🚨
2. **沒有驗證登入狀態，導致安全漏洞！**

### **✅ 正確作法（檢查 session，確保使用者已登入）**
```python
@app.get("/member")
def member(request: Request):
    logined = request.session.get("already_login")
    username = request.session.get("username")

    if logined != "true":  # 確保只有登入的人才能進入
        return RedirectResponse(url="/", status_code=302)

    return templates.TemplateResponse("member.html", {"request": request, "username": username})
```
這樣就可以 **確保未登入的使用者無法訪問 `/member` 頁面**！💪

---

## **🎯 總結**
1. `request.session.clear()` **刪除所有 session**，`del request.session["already_login"]` **只刪除單個 session**。
2. `if logined is not None` 是最穩定的寫法，不管 session 是 `True` 還是 `"true"` 都能判斷。
3. `/member` 不需要 `username` 參數，因為可以 **直接從 session 取得**。
4. `/member` **可以查詢資料庫**，但大多數情況下 **session 就足夠**。
5. 設定 `/member` **是為了防止未登入使用者直接輸入網址進入**。

這樣的設計可以讓你的網站更 **安全**、**高效**，不容易被攻擊！🚀🔥