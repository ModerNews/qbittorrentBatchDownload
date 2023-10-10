from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse

import qbitWrapper
from utils import get_nyaa_entries

app = FastAPI(templates_dir="./templates")
templates = Jinja2Templates(directory="templates")
qbit = qbitWrapper.Client('192.168.0.20', '8080', 'admin', 'adminadmin')


@app.get("/")
async def root(request: Request, src: str = ""):
    return templates.TemplateResponse("index.html", {"request": request, 'src': src})


@app.get("/list")
async def say_hello(request: Request, team: str = "", q: str = ""):
    return templates.TemplateResponse("list.html", {"request": request, "nyaa": get_nyaa_entries(q, team)})


@app.post("/list")
async def schedule_downloads(request: Request):
    data = await request.form()
    data = jsonable_encoder(data)
    print(data)
    qbit.add_torrent("\n".join(data.values()), '/media/' + data['savepath'])
    return RedirectResponse("/?src=list_success", status_code=302)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)