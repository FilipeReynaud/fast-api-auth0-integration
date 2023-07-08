from fastapi import APIRouter

router = APIRouter()


@router.get("/", status_code=200)
async def healthcheck():
  """ Healthcheck endpoint"""
  return "OK"
