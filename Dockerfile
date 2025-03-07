# Python 3.9 기반 이미지 사용
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 먼저 requirements.txt를 복사
COPY requirements.txt .

# 가상환경 생성 후 패키지 설치
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# 앱 소스 코드 복사
COPY . .

# 가상환경 활성화 후 실행
CMD ["/opt/venv/bin/python", "SEEDROUND1.py"]
