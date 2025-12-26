from fastapi import FastAPI

app = FastAPI(root_path="api/v1")

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

"""
Campaigns
- campaign_id
- name
- due date
-created_at

"""
@app.get("/api/v1/campaigns")
async def read_campaigns():
    return {"campaigns": "example"}

