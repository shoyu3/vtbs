import ddQuery
import requests

from fastapi import FastAPI, File, UploadFile, Response
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/get_pic")
async def get_dd_pic(name = None, mid = None, ban = 1):
    if mid == None and name == None:
        return "error args!"

    dd = ddQuery.ddAccount(name = name, mid = mid)
    if dd.user_info['fans'] > 6000 and ban == 1:
        return "many fans!"
    picPath = ddQuery.Pic(dd)
    file_like = open(picPath.get_path(), mode = "rb")
    return StreamingResponse(file_like, media_type = "image/jpg")
    
ddQuery.start_update()