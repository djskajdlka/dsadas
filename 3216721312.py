import requests
import random
import os 
from telegram import Update, 
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

# BIN Checker Fonksiyonu
def check_bin(bin_code):
    try:
        url = f"https://lookup.binlist.net/{bin_code}"
        headers = {"Accept-Version": "3"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            bank = data.get("bank", {}).get("name", "Bilinmiyor")
            country = data.get("country", {}).get("name", "Bilinmiyor")
            scheme = data.get("scheme", "Bilinmiyor")
            card_type = data.get("type", "Bilinmiyor")
            brand = data.get("brand", "Bilinmiyor")

            return f"""
💳 BIN: {bin_code}
🏦 Banka: {bank}
🌍 Ülke: {country}
💼 Kart Türü: {card_type}
🏷️ Marka: {brand}
🔗 Şema: {scheme}
            """
        else:
            return "❌ Geçersiz veya bulunamayan BIN kodu."
    except Exception as e:
        return f"Hata: {e}"

# Random kart üretici (Luhn uyumlu değil)
def random_card():
    bin_start = "457173"  # Visa için örnek BIN
    card = bin_start + "".join([str(random.randint(0, 9)) for _ in range(10)])
    month = str(random.randint(1, 12)).zfill(2)
    year = str(random.randint(25, 30))
    cvv = str(random.randint(100, 999))
    return f"{card}|{month}|{year}|{cvv}"

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hoş geldin! 6 haneli BIN gönder veya /gen ile random kart üret!")

# BIN Kontrol mesajı
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip()
    if msg.isdigit() and len(msg) == 6:
        result = check_bin(msg)
        await update.message.reply_text(result)
    else:
        await update.message.reply_text("Lütfen 6 haneli geçerli bir BIN gönder!")

# /gen komutu
async def gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    card = random_card()
    await update.message.reply_text(f"🎲 Kart: {card}")

# Botu çalıştır
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gen", gen))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot çalışıyor...")
    app.run_polling()

if name == "__main__":
    main()