import sys
import asyncio
from telegram import Bot

# Configura el token de tu bot de Telegram y el chat_id al que enviarás el mensaje
bot_token = ''
chat_id = ''

async def enviar_mensaje_telegram(mensaje):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=mensaje)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python enviar_telegram.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    mensaje = f'Cambio detectado, visita {url}'

    loop = asyncio.get_event_loop()
    loop.run_until_complete(enviar_mensaje_telegram(mensaje))
