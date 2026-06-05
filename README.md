# Emotion Chat Tester - 情緒對話測試工具

自動登入情緒對話系統，發送六大情緒測試訊息，並在瀏覽器上模擬真人操作。

## 📋 專案簡介

本工具可以自動登入 `http://210.70.254.110:2237` 的情緒對話系統，
針對 **六大情緒（Joy / Sadness / Anger / Fear / Disgust / Surprise）**
發送測試訊息，並觀察 AI 的情緒分析結果。

## 🗂️ 檔案說明

| 檔案 | 用途 | 在哪執行 |
|------|------|---------|
| **`browser_agent.py`** | **🔥 主要檔案** — 開啟瀏覽器，自動登入 + 模擬真人對話 | Windows |
| `web_app.py` | Flask 網頁伺服器，可從瀏覽器觀看對話記錄與情緒分析 | 伺服器 |
| `templates/index.html` | Flask 前端頁面，仿原網站聊天風格 | （隨 web_app.py） |
| `emotion_chat_cli.py` | 命令列模式，不開瀏覽器，直接透過 API 測試 | 任何環境 |

## ⚙️ Windows 安裝步驟

### 步驟 1：安裝 Python

1. 前往 https://www.python.org/downloads/
2. 下載 Python **3.10 或以上**版本
3. 安裝時 **務必勾選** "Add Python to PATH"

確認安裝成功：
```
python --version
```

### 步驟 2：下載專案

下載本專案的所有檔案到你的電腦，放到一個資料夾（例如 `C:\emotion-chat-tester`）。

### 步驟 3：安裝 Playwright

打開「命令提示字元 (cmd)」或「PowerShell」：

在那之前要先建立虛擬環境

請先看文件

[python_venv.md](./python_venv.md)

```cmd
cd C:\emotion-chat-tester
pip install playwright
playwright install chromium
```

> 第一次安裝 Playwright 會自動下載 Chromium 瀏覽器（約 150MB），請耐心等待。

## 🚀 執行瀏覽器自動化 (Windows)

```cmd
python browser_agent.py
```

執行後你會看到選單：

```
==================================================
          六大情緒瀏覽器測試
       (瀏覽器會自動開啟操作)
==================================================
  1. 快樂 Joy
  2. 悲傷 Sadness
  3. 憤怒 Anger
  4. 恐懼 Fear
  5. 厭惡 Disgust
  6. 驚訝 Surprise
  7. 全部測試
  0. 自訂訊息
  q. 結束
==================================================
請選擇:
```

選擇後，瀏覽器會自動執行以下動作：

| 步驟 | 畫面 |
|------|------|
| 1 | Chrome 自動開啟 |
| 2 | 自動導航到登入頁面 |
| 3 | 自動填入帳號 AI_agent / 密碼 |
| 4 | 自動點擊登入 |
| 5 | 聊天頁面載入 |
| 6 | 逐字輸入測試訊息（像真人打字） |
| 7 | 自動發送 |
| 8 | 等待 AI 回覆 |
| 9 | 繼續下一則訊息 |

### 選項說明

| 選項 | 說明 |
|------|------|
| **1 ~ 6** | 測試單一情緒，每種發送 2 則訊息 |
| **7** | 依序測試全部 6 種情緒，共 12 則訊息 |
| **0** | 自行輸入訊息內容 |
| **q** | 結束程式 |

## 🎯 支援六大情緒

| 編號 | 情緒 | 英文 | 測試訊息範例 |
|------|------|------|-------------|
| 1 | 快樂 | Joy | 「我考上理想的大學了！超級開心！」 |
| 2 | 悲傷 | Sadness | 「陪了我十年的狗狗昨天走了，我好難過」 |
| 3 | 憤怒 | Anger | 「有人在我的專案上動手腳，我氣炸了！」 |
| 4 | 恐懼 | Fear | 「我每晚都失眠，總覺得有不好的事要發生」 |
| 5 | 厭惡 | Disgust | 「看到那種欺騙行為我覺得很噁心」 |
| 6 | 驚訝 | Surprise | 「天啊！他居然是我失散多年的親生父親！」 |

## 🌐 Flask 網頁（選用）

如果你在伺服器上執行 `web_app.py`，可以在瀏覽器開啟：

```
http://<伺服器IP>:5001
```

檢視對話記錄與情緒分析圖表。

## 💻 CLI 命令列（選用）

不開瀏覽器，直接透過 API 測試：

```cmd
cd C:\emotion-chat-tester
pip install requests
python emotion_chat_cli.py [選項]
```

選項：`1`~`6`（單種情緒）、`7`（全部測試）

## 📝 注意事項

- `browser_agent.py` 需要 Windows 系統且有 Chrome 瀏覽器
- 首次執行會自動下載 Chromium（Playwright 專用）
- 帳號固定為 `AI_agent` / 密碼 `12345678`
- 請確保電腦可以連線到 `http://210.70.254.110:2237`
# emotion-chat-tester
