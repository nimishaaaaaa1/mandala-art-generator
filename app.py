# app.py
import streamlit as st
from openai import OpenAI
import requests
from PIL import Image, ImageOps
import io

# A4 dimensions at 300 DPI
A4_SIZE = (2480, 3508)

st.set_page_config(page_title="Mandala Art Generator", layout="centered")
st.title("🌀 Mandala Art Generator")
st.markdown("Generate beautiful **black-and-white mandala art** from a single word or phrase using DALL·E 3.")

st.markdown("➡️ Enter your **OpenAI API key** and a **one-word or one-line prompt** to begin:")

# 1. Get API key
api_key = st.text_input("🔑 OpenAI API Key", type="password", help="Your API key is never stored or logged.")

# 2. Get user prompt
prompt = st.text_input("🎨 Inspiration Prompt", help="Type one word or a short phrase like 'lotus', 'calm energy', etc.")

# 3. Button click logic
generate_clicked = st.button("Generate Mandala", key="generate_mandala_button")

if generate_clicked:
    if not api_key or not prompt.strip():
        st.error("🚫 Please enter both your API key and a prompt.")
    else:
        st.info("⏳ Generating your mandala—please wait a few seconds...")

        try:
            client = OpenAI(api_key=api_key)
            response = client.images.generate(
                model="dall-e-3",
                prompt=f"black and white symmetrical mandala art, highly detailed, intricate, suitable for printing, inspired by '{prompt.strip()}'",
                size="1024x1024",
                quality="standard",
                n=1
            )

            # 4. Load and process image
            image_url = response.data[0].url
            image_data = requests.get(image_url).content
            img = Image.open(io.BytesIO(image_data)).convert("L")

            # 5. Resize and paste into A4 canvas
            canvas = Image.new("L", A4_SIZE, "white")
            img_resized = img.resize((2048, 2048), Image.Resampling.LANCZOS)
            pos = ((A4_SIZE[0] - img_resized.width) // 2, (A4_SIZE[1] - img_resized.height) // 2)
            canvas.paste(img_resized, pos)

            # 6. Show preview
            st.success("✅ Mandala generated!")
            st.image(canvas, caption="Your Mandala (A4 @300 DPI)", use_container_width=True)

            # 7. Download buttons
            png_buf = io.BytesIO()
            canvas.save(png_buf, format="PNG", dpi=(300, 300))
            png_buf.seek(0)

            jpeg_buf = io.BytesIO()
            canvas.save(jpeg_buf, format="JPEG", dpi=(300, 300), quality=95)
            jpeg_buf.seek(0)

            st.download_button("📥 Download as PNG", png_buf, file_name="mandala.png", mime="image/png")
            st.download_button("📥 Download as JPEG", jpeg_buf, file_name="mandala.jpg", mime="image/jpeg")

        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")
