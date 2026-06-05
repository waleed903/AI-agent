from flask import Flask, request
import requests
from google import genai

app = Flask(__name__)

# ===== GEMINI SETUP =====
GEMINI_API_KEY = "AQ.Ab8RN6L_Jvy-00MLAto8XhKAxnEMTpiIm5WORjfp9jpbRsia4Q"
client = genai.Client(api_key=GEMINI_API_KEY)

# ===== WHATSAPP SETUP =====
ACCESS_TOKEN = "EAASiVTCewoIBRtCtW35wRrw14bTKZA2nFj7wybtGYe9cs0FZBzxXxu43ZA30mncpXWz2OzPdZAvoGylZBmFXGA6axkbfvtGBMeeAKzqGRyZCsSrnNMauE8LYzoqTE7zWbFjDMgYhiXZBHZAoC3tV6EgObfOlyoA1caSYjvFdK3l4TIKhekxC91h4JrisMwg2LdRs4wvDYj3xXX97g2ZC96KAZCZBNqSY6UUbZBClWzSM9bU9mUJZAuiGwGdqYLNoHxDQazZBNAZCxoXBgnz1rMJLXqqhlYrSgZDZD"
PHONE_NUMBER_ID = "1062308946975306"

def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }

    requests.post(url, headers=headers, json=data)


def ask_gemini(user_text):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_text
    )
    return response.text


# ===== WEBHOOK =====
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        user_text = message["text"]["body"]
        user_number = message["from"]

        reply = ask_gemini(user_text)

        send_whatsapp_message(user_number, reply)

    except:
        pass

    return "OK", 200


if __name__ == "__main__":
    app.run(port=5000)