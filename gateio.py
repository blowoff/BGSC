from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

app = Flask(__name__)

# 환경 변수에서 값 불러오기
ARKHAM_WEBHOOK_TOKEN = os.getenv("ARKHAM_WEBHOOK_TOKEN")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.route("/")
def home():
    return "Hello, Gunicorn!"

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    print("[LOG] 웹훅 요청 받음")  # 로그 출력

    # 헤더에서 웹훅 토큰 검증
    received_token = request.headers.get("Arkham-Webhook-Token")
    if received_token != ARKHAM_WEBHOOK_TOKEN:
        print("[ERROR] 웹훅 토큰 불일치")  # 로그 출력
        return jsonify({"error": "Unauthorized"}), 403

    # JSON 데이터 받기
    data = request.json
    if not data or "transfer" not in data:
        print("[ERROR] 웹훅 데이터 형식 오류")  # 로그 출력
        return jsonify({"error": "Invalid data"}), 400

    # 전송된 데이터 추출
    transfer = data["transfer"]
    alert_name = data.get("alertName", "No Alert Name")
    tx_hash = transfer.get("transactionHash", "N/A")
    token_name = transfer.get("tokenName", "Unknown Token")
    token_symbol = transfer.get("tokenSymbol", "???")
    amount = transfer.get("unitValue", 0)
    block_timestamp = transfer.get("blockTimestamp", "Unknown")

    # 보낸 주소 정보
    from_address = transfer.get("fromAddress", {}).get("address", "Unknown")
    from_entity = transfer.get("fromAddress", {}).get("arkhamEntity", {}).get("name", "Unknown")
    from_website = transfer.get("fromAddress", {}).get("arkhamEntity", {}).get("website", "")
    
    # 받는 주소 정보
    to_address = transfer.get("toAddress", {}).get("address", "Unknown")
    to_entity = transfer.get("toAddress", {}).get("arkhamEntity", {}).get("name", "Unknown")
    to_website = transfer.get("toAddress", {}).get("arkhamEntity", {}).get("website", "")
    
    # 디스코드 메시지 구성
    discord_message = {
        "content": f"🚨 **{alert_name}** 🚨",
        "embeds": [
            {
                "title": "📌 새 트랜잭션 발생!",
                "color": 16711680,  # 빨간색
                "fields": [
                    {"name": "🆔 거래 해시", "value": f"[`{tx_hash}`](https://etherscan.io/tx/{tx_hash})", "inline": False},
                    {"name": "📦 토큰", "value": f"{token_name} ({token_symbol})", "inline": True},
                    {"name": "💰 전송량", "value": f"{amount:,}", "inline": True},
                    {"name": "📤 보낸 주소", "value": f"[{from_entity}]({from_website})\n`{from_address}`", "inline": False},
                    {"name": "📥 받는 주소", "value": f"[{to_entity}]({to_website})\n`{to_address}`", "inline": False},
                    {"name": "⏰ 시간", "value": block_timestamp, "inline": False},
                ],
                "footer": {"text": "Powered by Arkham Webhook"},
            }
        ],
    }

    # 디스코드 웹훅으로 전송
    response = requests.post(DISCORD_WEBHOOK_URL, json=discord_message)

    if response.status_code == 204:
        print("[SUCCESS] 디스코드 전송 완료")  # 로그 출력
        return jsonify({"status": "success"}), 200
    else:
        print(f"[ERROR] 디스코드 전송 실패: {response.status_code}, {response.text}")  # 로그 출력
        return jsonify({"error": f"Failed to send to Discord: {response.status_code}, {response.text}"}), 500

if __name__ == "__main__":
    print("Flask 앱이 Gunicorn으로 실행됩니다.")
