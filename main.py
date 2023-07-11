from fentoboardimage import fenToImage, loadPiecesFolder
from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"Hello": "World"}


@app.get("/board")
async def board(fen: str, flip: bool = False, before: str = None, after: str = None):
    board = fenToImage(
        fen=f"{fen}",
        squarelength=200,
        pieceSet=loadPiecesFolder("pieces"),
        darkColor="#79a65d",
        lightColor="#daf2cb",
        flipped=flip,
        lastMove={
            "before": before,
            "after": after,
            "darkColor": "#bbcb2b",
            "lightColor": "#f7f769",
        }
        if before is not None and after is not None
        else None,
    )

    board.save("board.png")
    return FileResponse("board.png")


uvicorn.run(app, host="0.0.0.0", port=8000)
