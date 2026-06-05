import requests
import time
import json

BASE_URL = "http://210.70.254.110:2237"
USERNAME = "AI_agent"
PASSWORD = "12345678"

emotion_test_data = {
    "1": {
        "name": "快樂 Joy",
        "messages": [
            "我考上理想的大學了！超級開心！",
            "今天朋友給我一個驚喜派對，我好感動",
        ]
    },
    "2": {
        "name": "悲傷 Sadness",
        "messages": [
            "陪了我十年的狗狗昨天走了，我好難過",
            "我失戀了，心好痛，做什麼都提不起勁",
        ]
    },
    "3": {
        "name": "憤怒 Anger",
        "messages": [
            "有人在我的專案上動手腳，我氣炸了！",
            "太不公平了！我無法忍受這種惡劣行為！",
        ]
    },
    "4": {
        "name": "恐懼 Fear",
        "messages": [
            "我每晚都失眠，總覺得有不好的事要發生",
            "我對未來感到非常恐懼，不知道該怎麼辦",
        ]
    },
    "5": {
        "name": "厭惡 Disgust",
        "messages": [
            "看到那種欺騙行為我覺得很噁心",
            "這種自私自利的做法讓我感到非常厭惡",
        ]
    },
    "6": {
        "name": "驚訝 Surprise",
        "messages": [
            "天啊！他居然是我失散多年的親生父親！",
            "完全不敢相信！我中樂透了！",
        ]
    },
}

def show_menu():
    print("\n" + "=" * 50)
    print("          六大情緒測試系統")
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

def analyze_emotion(cs_id, mes_id, content, headers):
    sa_resp = requests.post(
        f"{BASE_URL}/api/sa",
        json={"cs_id": cs_id, "mes_id": mes_id, "content": content},
        headers=headers
    )
    return sa_resp.json()

def print_emotion_result(sa_data, expected_emotion=""):
    if not sa_data.get("success") or not sa_data.get("data"):
        print("  情緒分析失敗")
        return
    emotions = sa_data["data"]
    scores = {
        "joy": emotions.get("joy", 0),
        "sadness": emotions.get("sadness", 0),
        "anger": emotions.get("anger", 0),
        "fear": emotions.get("fear", 0),
        "disgust": emotions.get("disgust", 0),
        "surprise": emotions.get("surprise", 0),
    }
    max_emotion = max(scores, key=scores.get)
    max_score = scores[max_emotion]
    emo_labels = {
        "joy": "Joy", "sadness": "Sadness", "anger": "Anger",
        "fear": "Fear", "disgust": "Disgust", "surprise": "Surprise"
    }
    print(f"  Joy={scores['joy']}  Sadness={scores['sadness']}  Anger={scores['anger']}")
    print(f"  Fear={scores['fear']}  Disgust={scores['disgust']}  Surprise={scores['surprise']}")
    print(f"  摘要: {emotions.get('summary', '')}")

    if expected_emotion:
        expected_key = expected_emotion.lower()
        is_match = max_emotion == expected_key and max_score > 0
        if is_match:
            print(f"  >> 預期情緒: {expected_emotion} | 分析最高: {emo_labels.get(max_emotion, max_emotion)}={max_score}  ✅ 符合")
        else:
            print(f"  >> 預期情緒: {expected_emotion} | 分析最高: {emo_labels.get(max_emotion, max_emotion)}={max_score}  ⚠️ 不符合")

def send_and_analyze(cs_id, msg, headers, expected_emotion=""):
    print(f"\n--- 發送: {msg} ---")
    resp = requests.post(
        f"{BASE_URL}/api/ai/sessions/{cs_id}/messages",
        json={"content": msg},
        headers=headers
    )
    msg_data = resp.json()
    reply = msg_data.get("reply", "")
    mes_id = msg_data.get("mes_id")
    print(f"AI 回覆: {reply[:60]}...")

    if mes_id:
        print("  分析情緒中...")
        sa_data = analyze_emotion(cs_id, mes_id, msg, headers)
        print_emotion_result(sa_data, expected_emotion)
    else:
        print("  無 mes_id，跳過情緒分析")
    time.sleep(2)

def test_emotion(cs_id, headers, choice):
    if choice == "0":
        msg = input("請輸入你要測試的訊息: ").strip()
        if msg:
            send_and_analyze(cs_id, msg, headers)
        return True
    elif choice in emotion_test_data:
        info = emotion_test_data[choice]
        expected = info["name"].split()[-1]
        print(f"\n>>> 測試情緒: {info['name']} <<<")
        for msg in info["messages"]:
            send_and_analyze(cs_id, msg, headers, expected)
        return True
    elif choice == "7":
        for key, info in emotion_test_data.items():
            expected = info["name"].split()[-1]
            print(f"\n{'=' * 40}")
            print(f">>> 測試情緒: {info['name']} <<<")
            print("=" * 40)
            for msg in info["messages"]:
                send_and_analyze(cs_id, msg, headers, expected)
        return True
    else:
        return False

def main():
    print("=== 登入中... ===")
    resp = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": USERNAME,
        "password": PASSWORD
    })
    data = resp.json()
    print(f"登入結果: {data.get('message')}")
    if not data.get("success"):
        print("登入失敗！")
        return

    token = data["token"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("\n=== 建立新對話... ===")
    resp = requests.post(f"{BASE_URL}/api/ai/sessions", json={
        "title": "六大情緒測試"
    }, headers=headers)
    session_data = resp.json()
    cs_id = session_data.get("cs_id")
    if not cs_id:
        print("無法建立對話")
        return
    print(f"對話建立成功，cs_id={cs_id}")

    import sys
    choice = sys.argv[1] if len(sys.argv) > 1 else "7"
    show_menu()
    print(f"選擇: {choice}")
    test_emotion(cs_id, headers, choice)

    # Final: get emotion history
    print("\n=== 取得完整情緒分析歷史 ===")
    et_resp = requests.get(
        f"{BASE_URL}/api/sa/et/{cs_id}",
        headers=headers
    )
    print(json.dumps(et_resp.json(), ensure_ascii=False, indent=2))
    print("\n=== 測試完成！ ===")

if __name__ == "__main__":
    main()
