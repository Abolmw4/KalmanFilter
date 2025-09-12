import numpy as np
import uvicorn
from fastapi import FastAPI, Query, Path
from typing import Dict, Annotated
from kalmanfilter.kalman_filter import KalmanFilter
from utils.util import Radar, RadarInfo, EstimateInfo, Response

RADAR_INFO: Dict[int, Radar] = {}
RESULT_INFO: Dict[int, EstimateInfo] = {}
__KALMAN = KalmanFilter(dt=4, u_x=0, u_y=0, std_acc=25, x_std_meas=50, y_std_meas=50)

app = FastAPI()

async def is_empty(structure: Dict[int, Radar]) -> bool:
    return True if not structure else False

@app.post("/save")
async def save_info(request: RadarInfo):
    if request.Id > 0:
        RADAR_INFO[request.Id] = request.radar_info
        z = np.matrix([[request.radar_info.X], [request.radar_info.Y]], dtype=np.float64)
        __KALMAN.predict()
        result = __KALMAN.updata(z)
        EstimateInfo.Id = request.Id
        EstimateInfo.X = result[0]
        EstimateInfo.Y = result[1]
        RESULT_INFO[request.Id] = EstimateInfo
        return {"result": request}
    else:
        raise ValueError("request is not statndard please check Request")
        return

@app.get("/dbinfo")
async def check_db_info():
    result = await is_empty(RADAR_INFO)
    if not result:
        return RADAR_INFO
    else:
        return {"result": "Empty"}

@app.get("/estimate/{item_id}")
async def estimate(item_id: Annotated[int, Path(gt=0, lt=100)]) -> Response:
    Response.Id = RESULT_INFO.get(item_id).Id
    Response.X = RESULT_INFO.get(item_id).X
    Response.Y = RESULT_INFO.get(item_id).Y
    return Response

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
