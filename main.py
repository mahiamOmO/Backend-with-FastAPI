from datetime import datetime
from fastapi import FastAPI
from typing import Any
from fastapi import FastAPI, HTTPException
from random import randint

app = FastAPI(root_path="/api/v1")

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

data = [
    {
        "campaign_id": 1,
        "name": "Summer Launch",
        "due_date": datetime.now(),
        "created_at": datetime.now()
    },
    {
        "campaign_id": 2,
        "name": "Winter Sale",
        "due_date": datetime.now(),
        "created_at": datetime.now()
    }
    
]

"""
Campaigns
- campaign_id
- name
- due date
-created_at

"""
@app.get("/api/v1/campaigns")
async def read_campaigns():
    return {"campaigns": data}

@app.get("/campaigns/{id}")
async def read_campaign(id: int):
    for campaign in data:
        if campaign.get("campaign_id") == id:
            return {"campaign": campaign}
        
    raise HTTPException(status_code=404, detail="Campaign not found")
@app.post("/campaigns")
async  def create_campaign(request: Request):
    body = await request.json()

    new: Any = {
        "campaign_id": ranint(100,1000),
        "name": body.get("name"),
        "due_date": body.get("due_date"),
        "created_at": datetime.now()
    }

    data.append(new)
    return {"campaign": new}