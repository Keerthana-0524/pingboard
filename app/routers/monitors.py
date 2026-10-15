from fastapi import APIRouter,Depends,HTTPException
from ..schemas.monitor import MonitorCreate,MonitorOut
from ..services.monitor_store import MonitorStore,get_store

router=APIRouter(prefix="/monitors",tags=["monitors"])

def not_found() -> HTTPException:
    return HTTPException(status_code=404,detail="Monitor not found")

@router.post("",response_model=MonitorOut,status_code=201)
def create_monitor(data: MonitorCreate,store:MonitorStore=Depends(get_store)):
    return store.create(data.model_dump(mode="json"))

@router.get("",response_model=list[MonitorOut])
def list_monitors(q:str | None=None, store:MonitorStore=Depends(get_store)):
    return store.list_all(q)

@router.get("/{monitor_id}",response_model=MonitorOut)
def get_monitor(monitor_id:int,store:MonitorStore=Depends(get_store)):
    monitor=store.get(monitor_id)
    if monitor is None:
        raise not_found()
    return monitor

@router.put("/{monitor_id}",response_model=MonitorOut)
def update_monitor(monitor_id:int,data:MonitorCreate,store:MonitorStore=Depends(get_store)):
    monitor=store.update(monitor_id,data.model_dump(mode="json"))
    if monitor is None:
        raise not_found()
    return monitor

@router.delete("/{monitor_id}",status_code=204)
def delete_monitor(monitor_id:int,store:MonitorStore=Depends(get_store)):
    if not store.delete(monitor_id):
        raise not_found()
    
