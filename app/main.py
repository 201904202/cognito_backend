from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
from decouple import config

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # S3에서 제공되는 프론트엔드를 허용하기 위해 "*" 대신 S3 도메인을 사용 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 환경 변수 설정
CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")
REDIRECT_URI = config("REDIRECT_URI")
COGNITO_DOMAIN = config("COGNITO_DOMAIN")

@app.post("/api/token")
async def get_token(request: Request):
    data = await request.json()
    code = data.get("code")

    if not code:
        return {"error": "Authorization code is missing"}

    token_url = f"{COGNITO_DOMAIN}/oauth2/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code == 200:
        token_data = response.json()
        return {
            "access_token": token_data.get("access_token"),
            "id_token": token_data.get("id_token")
        }
    else:
        return {"error": "Failed to retrieve token", "details": response.text}