from http.client import HTTPException
from typing import List
from fastapi import HTTPException
from backend.datemysql import get_db
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
app = FastAPI()


class Heartbeat(BaseModel):
    id: int
    time: datetime
    machine: str
    power: int

class HeartbeatCreate(BaseModel):
    time: datetime
    machine: str
    power: int

class HeartbeatUpdate(BaseModel):
    power: int



@app.get("/hearbeats",response_model=List[Heartbeat])
def list_hearbeats():
    with get_db() as con:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM machinepower ORDER BY time DESC ")
            return cur.fetchall()


@app.get("/heartbeat/{id}",response_model=Heartbeat)
def get_heartbeat(id: int):
    with get_db() as con:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM machinepower WHERE id=%s", (id,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Heartbeat not found")
            return row

@app.post("/heartbeat",response_model=HeartbeatCreate)
def create_heartbeat(heartbeat: HeartbeatCreate):
    with get_db() as con:
        with con.cursor() as cur:
            cur.execute("INSERT INTO machinepower(time,machine,power) VALUES(%s,%s,%s)",(heartbeat.time,heartbeat.machine,heartbeat.power))
            last_id = cur.lastrowid
            cur.execute("SELECT * FROM machinepower WHERE id=%s", (last_id,))
            return cur.fetchone()

@app.put("/heartbeat/{id}",response_model=Heartbeat)
def update_heartbeat(id:int,heartbeat: HeartbeatUpdate):
    with get_db() as con:
        with con.cursor() as cur:
            cur.execute("UPDATE machinepower SET POWER = %s WHERE id = %s", (heartbeat.power, id))
            cur.execute("SELECT * FROM machinepower WHERE id = %s", (id,))
            return cur.fetchone()

@app.delete("/heartbeat/{id}",response_model=Heartbeat)
def delete_heartbeat(id:int):
    with get_db() as con:
        with con.cursor() as cur:
            cur.execute("SElECT * FROM machinepower WHERE id = %s", (id,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="暂无记录，无法删除")
            cur.execute("DELETE  FROM machinepower WHERE id = %s", (id,))
            return row