from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Arkham 제공 웹훅 토큰
ARKHAM_WEBHOOK_TOKEN = "rzDAPMrKgRjpTi"

# 디스코드 웹훅 URL (네가 설정한 디스코드 웹훅으로 변경!)
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1347635345717465270/2z46mlr1py-Jp5Yak60UCWSHiacLy0iLf3scw27c72x7haqdpgd9218XQRrK9Y5KsAE0"

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # 헤더에서 웹훅 토큰 검증
    received_token = request.headers.get("Arkham-Webhook-Token")
    if received_token != ARKHAM_WEBHOOK_TOKEN:
        return jsonify({"error": "Unauthorized"}), 403

    # JSON 데이터 받기
    data = request.json
    if not data or "transfer" not in data:
        return jsonify({"error": "Invalid data"}), 400

    # 전송된 데이터 추출
    transfer = data["transfer"]
    alert_name = data.get("alertName", "No Alert Name")
    tx_hash = transfer.get("transactionHash", "N/A")
    token_name = transfer.get("tokenName", "Unknown Token")
    token_symbol = transfer.get("tokenSymbol", "???")
    amount = transfer.get("unitValue", 0)
    from_address = transfer.get("fromAddress", {}).get("address", "Unknown")
    to_address = transfer.get("toAddress", {}).get("address", "Unknown")
    block_timestamp = transfer.get("blockTimestamp", "Unknown")

    # 디스코드 메시지 구성
    discord_message = {
        "content": f"🚨 **{alert_name}** 🚨",
        "embeds": [
            {
                "title": "📌 새 트랜잭션 발생!",
                "color": 16753920,  # 오렌지색
                "fields": [
                    {"name": "🆔 거래 해시", "value": f"`{tx_hash}`", "inline": False},
                    {"name": "📦 토큰", "value": f"{token_name} ({token_symbol})", "inline": True},
                    {"name": "💰 전송량", "value": f"{amount:,}", "inline": True},
                    {"name": "📤 보낸 주소", "value": f"`{from_address}`", "inline": False},
                    {"name": "📥 받는 주소", "value": f"`{to_address}`", "inline": False},
                    {"name": "⏰ 시간", "value": block_timestamp, "inline": False},
                ],
                "footer": {"text": "Powered by Arkham Webhook"},
            }
        ],
    }

    # 디스코드 웹훅으로 전송
    response = requests.post(DISCORD_WEBHOOK_URL, json=discord_message)

    if response.status_code == 204:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"error": "Failed to send to Discord"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
