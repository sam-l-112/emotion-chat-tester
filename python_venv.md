## 建立與啟用虛擬環境步驟

### 1. 切換到專案目錄

首先，打開終端機（Terminal）或命令提示字元（CMD），切換到你想放置專案的資料夾：

```bash
cd /path/to/your/project

```

### 2. 建立虛擬環境

執行以下指令來建立虛擬環境。指令最後的 `.venv` 是虛擬環境的資料夾名稱，你可以自己取名（常見的命名有 `.venv` 或 `env`）：

```bash
python -m venv .venv

```

*(注意：在某些 Linux 系統上，你可能需要先安裝套件，例如 Ubuntu 需執行 `sudo apt install python3-venv`)*

### 3. 啟用虛擬環境（依作業系統而定）

建立完成後，你必須「啟用（Activate）」它，終端機才會切換到該獨立環境：

* **Windows (Command Prompt / CMD):**
```cmd
.venv\Scripts\activate.bat

```


* **Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1

```


*(如果遇到權限錯誤，需先執行 `Set-ExecutionPolicy RemoteSigned -Scope Process`)*
* **macOS / Linux:**
```bash
source .venv/bin/activate

```



> 💡 **如何確認啟用成功？**
> 啟用成功後，你的終端機提示字元前方會出現 `(.venv)` 的字樣，代表接下來所有安裝的套件都會鎖在這個環境裡。

---

## 常用操作指令

當你在虛擬環境中工作時，會常用到以下指令：

| 功能 | 指令 | 說明 |
| --- | --- | --- |
| **安裝套件** | `pip install 套件名稱` | 例如 `pip install requests`，只會安裝在當前環境。 |
| **查看已安裝套件** | `pip list` | 顯示目前環境中安裝的所有套件與版本。 |
| **匯出套件清單** | `pip freeze > requirements.txt` | 將當前環境的套件紀錄下來，方便他人複製環境。 |
| **依清單安裝套件** | `pip install -r requirements.txt` | 在新環境中快速還原所有需要的套件。 |
| **離開虛擬環境** | `deactivate` | 結束工作時輸入此指令，即可切換回系統全域的 Python。 |
