from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Control Canecas</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <h1>Control de Canecas de Reciclaje</h1>
    <div class="buttons">
        <button onclick="abrirCaneca(1)">Abrir Caneca 1</button>
        <button onclick="abrirCaneca(2)">Abrir Caneca 2</button>
        <button onclick="abrirCaneca(3)">Abrir Caneca 3</button>
    </div>
    <script src="/static/script.js"></script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get():
    return html

active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Mensaje recibido del ESP32: {data}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)

@app.get("/send/{caneca_id}")
async def send_command(caneca_id: int):
    for connection in active_connections:
        await connection.send_text(f"abrir:{caneca_id}")
    return {"status": "mensaje enviado", "caneca": caneca_id}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
