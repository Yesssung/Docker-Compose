from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 허용할 출처
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메소드
    allow_headers=["*"],  # 허용할 헤더
)

# MongoDB 클라이언트 설정
MONGODB_URL = "mongodb://mongodb:27017"  # docker-compose로 MongoDB가 실행 중일 때
client = AsyncIOMotorClient(MONGODB_URL)
db = client.mydatabase  # 원하는 데이터베이스 이름

# 요청 모델 설정
class CountRequest(BaseModel):
    count: int

# 응답 모델 설정
class CountResponse(BaseModel):
    count: Optional[int] = None

# POST 엔드포인트 - count 값 저장
@app.post("/count", response_model=dict)
async def save_count(request: CountRequest):
    try:
        # MongoDB에 새로운 카운트 값을 저장
        result = await db.counters.insert_one({"count": request.count})
        
        # 데이터 저장 성공 여부 확인
        if result.inserted_id:
            return {"message": "Count saved successfully!", "id": str(result.inserted_id)}
        
        # 예상치 못한 오류 메시지 반환
        raise HTTPException(status_code=500, detail="Failed to save count")
        
    except Exception as e:
        print(f"Error occurred while saving count: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while saving count")

# GET 엔드포인트 - 최근 count 값 가져오기
@app.get("/count", response_model=CountResponse)
async def get_latest_count():
    try:
        latest_count = await db.counters.find().sort("_id", -1).limit(1).to_list(length=1)
        if latest_count:
            return {"count": latest_count[0]["count"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve count")
    return {"count": 0}

@app.post("/increase", response_model=CountResponse)
async def increase_count():
    try:
        latest_count = await db.counters.find().sort("_id", -1).limit(1).to_list(length=1)
        new_count = latest_count[0]["count"] + 1 if latest_count else 1
        await db.counters.insert_one({"count": new_count})
        return {"count": new_count}
    except Exception as e:
        print(f"Error occurred while increasing count: {e}")
        raise HTTPException(status_code=500, detail="Failed to increase count")

# 카운트 감소
@app.post("/decrease", response_model=CountResponse)
async def decrease_count():
    try:
        latest_count = await db.counters.find().sort("_id", -1).limit(1).to_list(length=1)
        new_count = latest_count[0]["count"] - 1 if latest_count and latest_count[0]["count"] > 0 else 0
        await db.counters.insert_one({"count": new_count})
        return {"count": new_count}
    except Exception as e:
        print(f"Error occurred while decreasing count: {e}")
        raise HTTPException(status_code=500, detail="Failed to decrease count")