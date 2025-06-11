from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)



# Map person name to portrait image path
portraits = {
    "Rabindranath Tagore": "static/tagore_portrait.png",
    "William Shakespeare": "static/shakespeare_portrait.png"
}



def fetch_works_with_gpt(person_name):
    try:
        prompt = f"List 5 popular poems, songs, or quotes by {person_name}."
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )

        works_text = response.choices[0].message.content.strip()
        works_list = [line.strip("-* \n") for line in works_text.split("\n") if line.strip()]
        return works_list

    except Exception as e:
        print("OpenAI error:", e)
        return None



def create_collage_with_portrait(works, portrait_path):
    # Create white background
    width, height = 800, 600
    bg_color = (255, 255, 255)
    image = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    # Load font
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()

    # Draw each work as text
    y_text = 10
    for line in works:
        draw.text((10, y_text), line, font=font, fill=(0, 0, 0))
        y_text += 40

    if os.path.exists(portrait_path):
        # Load and resize portrait
        portrait = Image.open(portrait_path).convert("RGBA")
        portrait = portrait.resize((300, 400))

    # Apply transparency to portrait
    alpha = portrait.split()[3]
    alpha = alpha.point(lambda p: p * 0.5)
    portrait.putalpha(alpha)

    # Paste portrait onto background
    position = (width - portrait.width - 20, (height - portrait.height) // 2)
    image.paste(portrait, position, portrait)

    # Convert image to BytesIO
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        person = request.form.get("person")
        # Validate input
        if not person:
            return render_template("index.html", error="Please enter a name.")

        works = fetch_works_with_gpt(person)
        # Check if works were fetched successfully        
        if not works:
            return render_template("index.html", error="No works found using GPT. Try a more well-known name.")
        
        portrait_path = portraits.get(person)
        # Check if portrait exists
        if not portrait_path:
            return render_template("index.html", error="No portrait available for this person.")
        
        if not os.path.exists(portrait_path):
            return render_template("index.html", error=f"Portrait image not found at {portrait_path}.")



        img_io = create_collage_with_portrait(works, portrait_path)
        return send_file(img_io, mimetype='image/png')

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
