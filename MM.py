import requests
import json

# 디스코드 웹훅 URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1347635345717465270/2z46mlr1py-Jp5Yak60UCWSHiacLy0iLf3scw27c72x7haqdpgd9218XQRrK9Y5KsAE0/github"

# Arkham 웹훅 토큰 추가
ARKHAM_WEBHOOK_TOKEN = "Mmda5FmsFuCBdZ"

# 데이터 구성
data = {
    "username": "Arkham Alerts",
    "embeds": [
        {
            "title": "🔔 Top Market Makers Transactions",
            "description": "**🚀 새로운 토큰 트랜잭션이 감지되었습니다!**",
            "color": 16776960,
            "fields": [
                {
                    "name": "💰 전송 금액",
                    "value": "1,500.003 ABCD (약 $4,299.1 USD)",
                    "inline": False
                },
                {
                    "name": "📍 전송자",
                    "value": "[BlockBank Fund 1](https://block.bank) (`0x333`)",
                    "inline": True
                },
                {
                    "name": "📍 수신자",
                    "value": "[Chainance Primary](https://chainance.org) (`0x444`)",
                    "inline": True
                },
                {
                    "name": "🔗 블록 정보",
                    "value": "[Ethereum 블록 16980384](https://etherscan.io/block/16980384)",
                    "inline": False
                },
                {
                    "name": "📝 트랜잭션 해시",
                    "value": "[0x222](https://etherscan.io/tx/0x222)",
                    "inline": False
                }
            ],
            "footer": {
                "text": "⏰ 2023-08-23 22:26:35 UTC",
                "icon_url": "https://etherscan.io/images/brandassets/etherscan-logo-light-circle.png"
            }
        }
    ]
}

# 헤더에 Arkham 웹훅 토큰 추가
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ARKHAM_WEBHOOK_TOKEN}"
}

# 디스코드 웹훅으로 데이터 전송
response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(data), headers=headers)

if response.status_code == 204:
    print("✅ 웹훅 전송 성공!")
else:
    print(f"❌ 오류 발생: {response.status_code}, {response.text}")
