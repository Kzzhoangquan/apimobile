from fastapi import FastAPI, File, UploadFile
import cloudinary
import cloudinary.uploader
from fastapi.responses import JSONResponse

app = FastAPI()

# Cấu hình Cloudinary
cloudinary.config(
    cloud_name="diyonw6md",
    api_key="324758519181249",
    api_secret="GSt3Ttptm9N4Wi4aTmBwodCuc5U",  # đừng để lộ public nếu deploy
    secure=True
)

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Đọc nội dung file
        contents = await file.read()

        # Upload lên Cloudinary
        result = cloudinary.uploader.upload(contents, public_id=file.filename)
        return {"url": result["secure_url"]}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})