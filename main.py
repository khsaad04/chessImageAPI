import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fentoboardimage import fenToImage, loadPiecesFolder
from PIL import Image, ImageDraw, ImageFont, ImageOps


def create(fen, flip, before, after):
    board = fenToImage(
        fen=f"{fen}",
        squarelength=100,
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
        if before and after
        else None,
    )

    board = ImageOps.expand(board, border=40, fill="black")
    font = ImageFont.truetype("font.ttf", 30)

    Im = ImageDraw.Draw(board)

    if flip:
        x = [chr(104 - i) for i in range(8)]
        y = [str(1 + i) for i in range(8)]
    else:
        x = [chr(97 + i) for i in range(8)]
        y = [str(8 - i) for i in range(8)]

    for i in range(8):
        Im.text((85 + i * 100, 840), x[i], (255, 255, 255), font=font)
        Im.text((10, 75 + i * 100), y[i], (255, 255, 255), font=font)

    board.save("board.png")


app = FastAPI()


@app.get("/")
async def root():
    return "Ready"


@app.get("/board")
async def board(fen: str, flip: bool = False, before: str = None, after: str = None):
    create(fen, flip, before, after)
    return FileResponse("board.png")


uvicorn.run(app, host="0.0.0.0", port=8000)
