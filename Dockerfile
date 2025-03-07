# Python 기반 이미지 사용
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 프로젝트 파일 복사
COPY . /app

# 필요 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 컨테이너 실행 명령어
CMD ["gunicorn", "-b", "0.0.0.0:5002", "SEEDROUND1:app"]
