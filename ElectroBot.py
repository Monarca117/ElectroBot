from config import *
import telebot
from telebot import types
from fuzzywuzzy import process

# Se instancia el bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

#Manejador de comando principal
@bot.message_handler(commands=["Start", "start"])
def cmd_start(message):
    """Da la bienvenida al usuario del bot"""
    user = message.from_user
    bot.send_message(message.chat.id, f"Bienvenido {user.first_name}, este es el bot oficial de Electro Federation. Nosotros protegemos tus datos personales.")

    #Boton de Aviso de privacidad
    markup = types.InlineKeyboardMarkup()
    btn_PrivacyLink = types.InlineKeyboardButton(text="Aviso de privacidad", url="https://www.gob.mx/cms/uploads/attachment/file/179045/proteccion_datos.pdf")
    markup.add(btn_PrivacyLink)

    # Enviamos el mensaje con el botón
    bot.send_message(message.chat.id, "Puedes consultar nuestro aviso de privacidad aquí:", reply_markup=markup)

    print("ID del chat: ", message.chat.id)
    bot.send_message(CHAT_ID, "Aqui tienes una lista de nuestros servicios: \nOpción 1. Consultar un reporte \nOpción 2. Consultar saldo y recibo \nOpción 3. Medios de pago \nOpción 4. Informacion")

# Opciones válidas
opciones_validas = ["opción 1", "opción 2", "opción 3", "opción 4"]

# Función para obtener la opción seleccionada
def obtener_opcion(texto):
    opcion, score = process.extractOne(texto.lower(), opciones_validas)
    if score >= 80:  # Umbral de similitud
        return opcion
    else:
        return None

# Manejador de mensajes de texto para las opciones
@bot.message_handler(func=lambda message: True)
def handle_options(message):
    opcion = obtener_opcion(message.text)

    if opcion is None:
        bot.send_message(message.chat.id, "Opción no válida. Por favor, selecciona una opción de la lista.")
        bot.send_message(message.chat.id, "Aqui tienes una lista de nuestros servicios: \nOpción 1. Consultar un reporte \nOpción 2. Consultar saldo y recibo \nOpción 3. Medios de pago \nOpción 4. Informacion")
        return

    if opcion == "opción 1":
        print("Opción 1 elegida")
        bot.send_message(message.chat.id, "Dame el ID de tu reporte.")
        # Cambiar el estado del usuario para esperar el ID del reporte
        bot.register_next_step_handler(message, handle_report_id)

    elif opcion == "opción 2":
        print("Opción 2 elegida")
        bot.send_message(message.chat.id, "Has seleccionado la opción 2.")

    elif opcion == "opción 3":
        print("Opción 3 elegida")
        bot.send_message(message.chat.id, "Has seleccionado la opción 3.")

    elif opcion == "opción 4":
        print("Opción 4 elegida")
        bot.send_message(message.chat.id, "Has seleccionado la opción 4.")

# Manejador de ID de reporte
def handle_report_id(message):
    id_reporte = message.text.lower()
    if id_reporte == "r01":
        print("Mandando reporte 1")
        bot.send_message(message.chat.id, "Enviando reporte 1...")
    elif id_reporte == "r02":
        print("Mandando reporte 2")
        bot.send_message(message.chat.id, "Enviando reporte 2...")
    else:
        bot.send_message(message.chat.id, "ID de reporte no válido.")

# MAIN
if __name__ == '__main__':
    print("INICIANDO BOT . . .")
    # Iniciamos un bucle
    bot.infinity_polling()
