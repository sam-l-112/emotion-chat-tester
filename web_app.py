from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import requests
import time
import threading

BASE_URL = "http://210.70.254.110:2237"
USERNAME = "AI_agent"
PASSWORD = "12345678"

app = Flask(__name__)
CORS(app)

app.state = {
    "token": None,
    "headers": None,
    "cs_id": None,
    "messages": [],
    "emotion_history": [],
    "status": "idle",
}

emotion_test_data = {
    "joy": {
        "name": "快樂 Joy",
        "messages": [
            "我考上理想的大學了！超級開心！",
            "今天朋友給我一個驚喜派對，我好感動",
        ]
    },
    "sadness": {
        "name": "悲傷 Sadness",
        "messages": [
            "陪了我十年的狗狗昨天走了，我好難過",
            "我失戀了，心好痛，做什麼都提不起勁",
        ]
    },
    "anger": {
        "name": "憤怒 Anger",
        "messages": [
            "有人在我的專案上動手腳，我氣炸了！",
            "太不公平了！我無法忍受這種惡劣行為！",
        ]
    },
    "fear": {
        "name": "恐懼 Fear",
        "messages": [
            "我每晚都失眠，總覺得有不好的事要發生",
            "我對未來感到非常恐懼，不知道該怎麼辦",
        ]
    },
    "disgust": {
        "name": "厭惡 Disgust",
        "messages": [
            "看到那種欺騙行為我覺得很噁心",
            "這種自私自利的做法讓我感到非常厭惡",
        ]
    },
    "surprise": {
        "name": "驚訝 Surprise",
        "messages": [
            "天啊！他居然是我失散多年的親生父親！",
            "完全不敢相信！我中樂透了！",
        ]
    },
}

def login():
    try:
        resp = requests.post(f"{BASE_URL}/api/auth/login", json={
            "username": USERNAME,
            "password": PASSWORD
        }, timeout=10)
        data = resp.json()
        if data.get("success"):
            app.state["token"] = data["token"]
            app.state["headers"] = {
                "Authorization": f"Bearer {data['token']}",
                "Content-Type": "application/json"
            }
            return True
        return False
    except Exception as e:
        print(f"[SA] login error: {e}", file=__import__('sys').stderr)
        return False

def create_session():
    try:
        resp = requests.post(f"{BASE_URL}/api/ai/sessions", json={
            "title": "六大情緒測試"
        }, headers=app.state["headers"], timeout=10)
        data = resp.json()
        if data.get("success"):
            app.state["cs_id"] = data["cs_id"]
            return True
        return False
    except Exception as e:
        print(f"[SA] create_session error: {e}", file=__import__('sys').stderr)
        return False

def send_message(msg):
    try:
        resp = requests.post(
            f"{BASE_URL}/api/ai/sessions/{app.state['cs_id']}/messages",
            json={"content": msg},
            headers=app.state["headers"],
            timeout=60
        )
        data = resp.json()
        mes_id = data.get("mes_id")
        reply = data.get("reply", "")
        elapsed = data.get("reply_elapsed", 0)
        app.state["messages"].append({"role": "user", "content": msg})
        app.state["messages"].append({"role": "bot", "content": reply, "elapsed": elapsed})
        return data
    except Exception as e:
        print(f"[SA] send_message error: {e}", file=__import__('sys').stderr)
        return {"mes_id": None}

def fetch_emotion_history():
    try:
        resp = requests.get(
            f"{BASE_URL}/api/sa/et/{app.state['cs_id']}",
            headers=app.state["headers"],
            timeout=10
        )
        data = resp.json()
        if data.get("success"):
            app.state["emotion_history"] = data.get("history", [])
        return app.state["emotion_history"]
    except Exception as e:
        print(f"[SA] fetch error: {e}", file=__import__('sys').stderr)
        return []

def analyze_sa(mes_id, content):
    try:
        resp = requests.post(
            f"{BASE_URL}/api/sa",
            json={"cs_id": app.state["cs_id"], "mes_id": mes_id, "content": content},
            headers=app.state["headers"],
            timeout=90
        )
        data = resp.json()
        if data.get("success") and data.get("data"):
            emo = data["data"]
            app.state["emotion_history"].append(emo)
        return data
    except Exception as e:
        print(f"[SA] analyze_sa error: {e}", file=__import__('sys').stderr)
        return None

def run_emotion_test(emotion_key):
    import sys
    if emotion_key not in emotion_test_data:
        if emotion_key != "all":
            return
    app.state["status"] = "running"
    app.state["messages"] = []
    app.state["emotion_history"] = []

    print("[SA] login...", flush=True, file=sys.stderr)
    if not login():
        print("[SA] login failed", flush=True, file=sys.stderr)
        app.state["status"] = "error"
        return
    print("[SA] create session...", flush=True, file=sys.stderr)
    if not create_session():
        print("[SA] create session failed", flush=True, file=sys.stderr)
        app.state["status"] = "error"
        return
    print(f"[SA] session={app.state['cs_id']}", flush=True, file=sys.stderr)

    keys = list(emotion_test_data.keys()) if emotion_key == "all" else [emotion_key]
    try:
        for key in keys:
            info = emotion_test_data[key]
            for msg in info["messages"]:
                if app.state.get("stop"):
                    app.state["stop"] = False
                    app.state["status"] = "idle"
                    return
                print(f"[SA] send: {msg[:20]}...", flush=True, file=sys.stderr)
                app.state["typing"] = False
                msg_data = send_message(msg)
                app.state["typing"] = True
                mes_id = msg_data.get("mes_id")
                if mes_id:
                    analyze_sa(mes_id, msg)
                time.sleep(1)
    except Exception as e:
        print(f"[SA] error: {e}", flush=True, file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        app.state["status"] = "error"
        app.state["typing"] = False
        return

    fetch_emotion_history()
    app.state["status"] = "done"
    app.state["typing"] = False
    print("[SA] done", flush=True, file=sys.stderr)


@app.route("/")
def index():
    return render_template("index.html", emotions=emotion_test_data)

@app.route("/api/start", methods=["POST"])
def start():
    emotion = request.json.get("emotion", "all")
    app.state["stop"] = False
    thread = threading.Thread(target=run_emotion_test, args=(emotion,))
    thread.daemon = True
    thread.start()
    return jsonify({"status": "started"})

@app.route("/api/stop", methods=["POST"])
def stop():
    app.state["stop"] = True
    app.state["status"] = "idle"
    return jsonify({"status": "stopped"})

@app.route("/api/status")
def get_status():
    return jsonify({
        "status": app.state["status"],
        "cs_id": app.state["cs_id"],
        "messages": app.state["messages"],
        "emotion_history": app.state["emotion_history"],
        "typing": app.state.get("typing", False),
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
