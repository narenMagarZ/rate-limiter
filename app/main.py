from fastapi import FastAPI, APIRouter, Header
from fastapi.middleware.cors import CORSMiddleware
import time
from app.redis_instance import Redis_App
from app.config import token_capacity, time_interval, app_base_url, environment

print("Rate limiting server running on", environment, "environment")

app = FastAPI(title="Simple http server")
api_router = APIRouter()
redis_app = Redis_App()

app.add_middleware(
  CORSMiddleware, 
  allow_origins=app_base_url, 
  allow_methods=["*"], 
  allow_headers=["*"], 
  allow_credentials=True
)

@api_router.get("/health")
def health_check():
  return {"status": "success"}

@api_router.get("/limited")
def get_users(x_client_id: str = Header(..., alias="X-Client-ID")):
  capacity = token_capacity
  refill_rate = capacity / time_interval
  current_time = int(time.time())
  bucket_key = f"bucket:{x_client_id}"
  try:
    client_bucket = redis_app.hget_all(name=bucket_key)
    print(client_bucket)
    if client_bucket:
      elapsed_time = current_time - int(client_bucket["last_refill_time"])
      tokens_to_add = elapsed_time * refill_rate
      token = min(capacity, float(client_bucket["token"]) + tokens_to_add)
      if token < 1:
        redis_app.hset(name=bucket_key, mapping={
          "id": x_client_id,
          "token": token,
          "last_refill_time": current_time
        })
        return {"success": False}
      token -= 1
      redis_app.hset(name=bucket_key, mapping={
        "id": x_client_id,
        "last_refill_time": current_time,
        "token": token
      })
      return {"success": True}
    else:
      redis_app.hset(name=bucket_key, mapping={
        "id": x_client_id,
        "token": capacity - 1,
        "last_refill_time": current_time 
      })
      return {"success": True}
  except Exception as e:
    print("Error", e)
    return {"success": False}


  
app.include_router(api_router, prefix="/api/public/v1")