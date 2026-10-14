from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field,HttpUrl
app=FastAPI(title="PingBoard",version="0.1.0")

class MonitorIn(BaseModel):
    name:str = Field(min_length=1,max_length=100)
    url:HttpUrl
    interval_seconds:int = Field(default=300,ge=30,le=86400)
    expected_status:int=Field(default=200 , ge=100,le=599)

class MonitorOut(MonitorIn):
    id:int

monitors:dict[int,dict]={}
next_id=1

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/monitors",response_model=MonitorOut,status_code=201)
def create_monitor(data:MonitorIn):
    global next_id
    monitor={"id":next_id,**data.model_dump(mode="json")}
    monitors[next_id]=monitor
    next_id+=1
    return monitor

@app.get("/monitors",response_model=list[MonitorOut])
def list_monitors(q:str | None=None):
    items=list(monitors.values())
    if q:
        items=[m for m in items if q.lower() in m["name"].lower()]
    return items

@app.get("/monitors/{monitor_id}", response_model=MonitorOut)
def get_monitor(monitor_id:int):
    if monitor_id not in monitors:
        raise HTTPException(status_code=404, detail="Monitor not Found")
    return monitors[monitor_id]

@app.put("/monitors/{monitor_id}",response_model=MonitorOut)
def update_monitor(monitor_id:int,data:MonitorIn):
    if monitor_id not in monitors:
        raise HTTPException(status_code=404,detail="Monitor not found")
    monitors[monitor_id]={"id":monitor_id,**data.model_dump(mode="json")}
    return monitors[monitor_id]

@app.delete("/monitors/{moniter_id}",status_code=204)
def delete_monitor(monitor_id:int):
    if monitor_id not in monitors:
        raise HTTPException(status_code=404 , detail="Monitor not found")
    del monitors[monitor_id]