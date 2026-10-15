class MonitorStore:
    def __init__(self) -> None:
        self.items: dict[int,dict]={}
        self.next_id=1

    def create(self,data:dict) -> dict:
        item={"id": self._next_id,**data}
        self.items[self._next_id]=item
        self._next_id+=1
        return item
    
    def list_all(self,q: str|None=None)-> list[dict]:
        items=list(self.items.values())
        if q:
            items=[m for m in items if q.lower() in m["name"].lower()]
        return items
    def get(self,monitor_id:int)->dict | None:
        return self._items.get(monitor_id)

    def update(self,monitor_id:int,data:dict)->dict | None:
        if monitor_id not in self._items:
            return None
        self._items[monitor_id]={"id": monitor_id,**data}
        return self._tems[monitor_id]
    def delete(self,monitor_id:int)->bool:
        return self._items.pop(monitor_id,None) is not None

_store=MonitorStore()
def get_store()->MonitorStore:
    return _store