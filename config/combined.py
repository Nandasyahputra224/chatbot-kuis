from telegram import Update
import requests
from PIL import Image
from io import BytesIO


async def send_combined_image(update: Update, url1: str, url2: str, caption: str):
    response1 = requests.get(url1)
    response2 = requests.get(url2)
    img1 = Image.open(BytesIO(response1.content)).convert("RGB")
    img2 = Image.open(BytesIO(response2.content)).convert("RGB")

    height = max(img1.height, img2.height)
    img1 = img1.resize((int(img1.width * height / img1.height), height))
    img2 = img2.resize((int(img2.width * height / img2.height), height))

    combined = Image.new("RGB", (img1.width + img2.width, height))
    combined.paste(img1, (0, 0))
    combined.paste(img2, (img1.width, 0))

    output = BytesIO()
    output.name = "combined.jpg"
    combined.save(output, format="JPEG")
    output.seek(0)

    await update.message.reply_photo(photo=output, caption=caption, parse_mode="Markdown")