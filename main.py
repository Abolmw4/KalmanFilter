import json

import numpy as np
import uvicorn
from dns.rdtypes.ANY.CNAME import CNAME
from fastapi import FastAPI, Query, Path
from typing import Dict, Annotated, List

from watchfiles import awatch

from kalmanfilter.kalman_filter import KalmanFilter
from utils.util import Radar, EstimateInfo, Response, RadarList, send_messege_to_kafka_from_request, read_json_file, recieve_messege_from_kafka, estimate_position

RADAR_INFO: Dict[int, Radar] = {}
RESULT_INFO: Dict[int, EstimateInfo] = {}

CONFIG = read_json_file()

app = FastAPI()

async def is_empty(structure: Dict[int, Radar]) -> bool:
    return True if not structure else False

@app.post("/save")
async def save_info(request: RadarList | Radar):
    if isinstance(request, RadarList):
        for value in request.radars:
            await send_messege_to_kafka_from_request(value, CONFIG.get("raw_track_topic_name"))
        return {"result": "All Request add successfully"}
    elif isinstance(request, Radar):
        await send_messege_to_kafka_from_request(request, CONFIG.get("raw_track_topic_name"))
        return {"result": "request added successfully"}
    else:
        return {"Result": f"request not valid '{request}'"}

@app.get("/{item_id}")
async def get_info(item_id: Annotated[int, Path(ge=1, lt=1000000)]):
    async for mes in recieve_messege_from_kafka(CONFIG.get("raw_track_topic_name")):
        if mes.get('trackID') == item_id:
            await estimate_position(Radar(trackID=mes.get("trackID"), X=mes.get("X"), Y=mes.get("Y"), V_X=mes.get("V_X"), V_Y=mes.get("V_Y")))
            return mes

@app.get("/result/{item_id}")
async def get_result(item_id: Annotated[int, Path(ge=1, lt=1000000)]):
    async for mes in recieve_messege_from_kafka(CONFIG.get("estimate_topic_name")):
        if mes.get("trackID") == item_id:
            return mes

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
