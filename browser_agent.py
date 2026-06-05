import asyncio

USERNAME = "AI_agent"
PASSWORD = "12345678"
LOGIN_URL = "http://210.70.254.110:2237/pages/login.html"

EMOTION_DATA = {
    "1": {"name": "快樂 Joy", "messages": [
        "我考上理想的大學了！超級開心！",
        "今天朋友給我一個驚喜派對，我好感動",
    ]},
    "2": {"name": "悲傷 Sadness", "messages": [
        "陪了我十年的狗狗昨天走了，我好難過",
        "我失戀了，心好痛，做什麼都提不起勁",
    ]},
    "3": {"name": "憤怒 Anger", "messages": [
        "有人在我的專案上動手腳，我氣炸了！",
        "太不公平了！我無法忍受這種惡劣行為！",
    ]},
    "4": {"name": "恐懼 Fear", "messages": [
        "我每晚都失眠，總覺得有不好的事要發生",
        "我對未來感到非常恐懼，不知道該怎麼辦",
    ]},
    "5": {"name": "厭惡 Disgust", "messages": [
        "看到那種欺騙行為我覺得很噁心",
        "這種自私自利的做法讓我感到非常厭惡",
    ]},
    "6": {"name": "驚訝 Surprise", "messages": [
        "天啊！他居然是我失散多年的親生父親！",
        "完全不敢相信！我中樂透了！",
    ]},
}

def show_menu():
    print("\n" + "=" * 50)
    print("          六大情緒瀏覽器測試")
    print("       (瀏覽器會自動開啟操作)")
    print("=" * 50)
    print("  1. 快樂 Joy")
    print("  2. 悲傷 Sadness")
    print("  3. 憤怒 Anger")
    print("  4. 恐懼 Fear")
    print("  5. 厭惡 Disgust")
    print("  6. 驚訝 Surprise")
    print("  7. 全部測試")
    print("  0. 自訂訊息")
    print("  q. 結束")
    print("=" * 50)

async def type_like_human(page, text):
    """逐字輸入，模擬真人打字"""
    for char in text:
        await page.keyboard.type(char, delay=0.05)
        await asyncio.sleep(0.02)

async def wait_for_bot_reply(page, timeout=120):
    """等待 AI 回覆出現"""
    import datetime
    start = datetime.datetime.now()
    bot_count_before = await page.evaluate("""
        () => document.querySelectorAll('.row.bot .bubble:not(.typing-bubble)').length
    """)
    while True:
        elapsed = (datetime.datetime.now() - start).total_seconds()
        if elapsed > timeout:
            print(f"  ⏰ AI 回覆等待超時 ({timeout}s)")
            return False
        typing = await page.query_selector(".typing-bubble")
        bot_count_now = await page.evaluate("""
            () => document.querySelectorAll('.row.bot .bubble:not(.typing-bubble)').length
        """)
        if not typing and bot_count_now > bot_count_before:
            await asyncio.sleep(1)
            return True
        await asyncio.sleep(0.5)

async def run():
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("=" * 50)
        print("❌ 需要安裝 Playwright")
        print()
        print("請依序執行以下指令：")
        print("  pip install playwright")
        print("  playwright install chromium")
        print()
        print("安裝完成後再執行本程式。")
        print("=" * 50)
        return

    choice = input("請選擇: ").strip()
    if choice == "q":
        return

    if choice == "0":
        msg = input("請輸入你要發送的訊息: ").strip()
        custom_msgs = [msg]
    elif choice == "7":
        keys = list(EMOTION_DATA.keys())
    elif choice in EMOTION_DATA:
        keys = [choice]
    else:
        print("❌ 無效選項")
        return

    print("\n🚀 正在啟動瀏覽器...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            locale="zh-TW",
            no_viewport=True
        )
        page = await context.new_page()

        print("1. 前往登入頁面...")
        await page.goto(LOGIN_URL, wait_until="networkidle")
        await asyncio.sleep(2)

        print("2. 登入中...")
        await page.wait_for_selector("input", timeout=15000)
        await page.click("input")
        await page.fill("input", USERNAME)
        await page.fill("input[type='password']", PASSWORD)
        await page.keyboard.press("Enter")
        await asyncio.sleep(2)

        print("3. 等待聊天頁面載入...")
        try:
            await page.wait_for_selector("textarea", timeout=20000)
        except:
            await page.wait_for_timeout(5000)
        print("   ✅ 登入成功！")

        msg_count = 0

        if choice == "0":
            for msg in custom_msgs:
                msg_count += 1
                print(f"\n💬 發送 ({msg_count}): {msg[:30]}...")
                await page.click("textarea")
                await page.fill("textarea", "")
                await type_like_human(page, msg)
                await asyncio.sleep(0.3)
                await page.keyboard.press("Enter")
                await wait_for_bot_reply(page)
                await asyncio.sleep(0.5)
        else:
            for key in keys:
                info = EMOTION_DATA[key]
                print(f"\n>>> 📋 測試: {info['name']} <<<")
                for msg in info["messages"]:
                    msg_count += 1
                    print(f"  💬 發送 ({msg_count}): {msg[:30]}...")
                    await page.click("textarea")
                    await page.fill("textarea", "")
                    await type_like_human(page, msg)
                    await asyncio.sleep(0.3)
                    await page.keyboard.press("Enter")
                    await wait_for_bot_reply(page)
                    await asyncio.sleep(0.5)

        print(f"\n✅ 全部完成！共發送 {msg_count} 則訊息")
        print("瀏覽器保持開啟，關閉視窗即可結束")
        await asyncio.sleep(999999)

if __name__ == "__main__":
    show_menu()
    asyncio.run(run())
