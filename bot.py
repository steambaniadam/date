import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, \
    CallbackQueryHandler, CallbackContext

# Daftar status conversasi
GENDER, AGE, HOBBY, LOCATION, MATCHING = range(5)

# Fungsi untuk menangani perintah /start
def start(update, context):
    reply_keyboard = [[KeyboardButton('Pria'), KeyboardButton('Wanita')]]
    update.message.reply_text(
        'Halo! Selamat datang di bot dating. Silakan pilih jenis kelamin Anda.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return GENDER

# Fungsi untuk menangani input jenis kelamin
def gender(update, context):
    user = update.message.from_user
    context.user_data['gender'] = update.message.text
    update.message.reply_text('Berapa usia Anda?')
    return AGE

# Fungsi untuk menangani input usia
def age(update, context):
    user = update.message.from_user
    context.user_data['age'] = update.message.text
    update.message.reply_text('Apa hobi Anda?')
    return HOBBY

# Fungsi untuk menangani input hobi
def hobby(update, context):
    user = update.message.from_user
    context.user_data['hobby'] = update.message.text
    update.message.reply_text('Dimana lokasi Anda? Kirimkan lokasi Anda saat ini, silakan.')
    return LOCATION

# Fungsi untuk menangani input lokasi
def location(update, context):
    user = update.message.from_user
    location = update.message.location
    context.user_data['location'] = (location.latitude, location.longitude)
    update.message.reply_text('Terima kasih! Profil Anda telah disimpan.')
    update.message.reply_text('Mulai mencari pasangan?', reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Ya'), KeyboardButton('Tidak')]], one_time_keyboard=True))
    return MATCHING

# Fungsi untuk memulai proses pencarian pasangan
def start_matching(update, context):
    user = update.message.from_user
    reply_keyboard = [[KeyboardButton('Suka'), KeyboardButton('Tidak Suka')]]
    update.message.reply_text(
        'Saya telah menemukan pasangan potensial untuk Anda. Apakah Anda tertarik?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return MATCHING

# Fungsi untuk menangani pemilihan pasangan
def choose_matching(update, context):
    user = update.message.from_user
    choice = update.message.text
    
    if choice == 'Suka':
        update.message.reply_text('Anda menyukai pasangan ini! Selamat!')
    else:
        update.message.reply_text('Anda tidak tertarik dengan pasangan ini. Coba yang lain ya!')
    
    update.message.reply_text('Apakah Anda ingin mencari pasangan lain?', reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Ya'), KeyboardButton('Tidak')]], one_time_keyboard=True))
    return MATCHING

# Fungsi untuk menghentikan pencarian pasangan
def stop_matching(update, context):
    update.message.reply_text('Terima kasih! Pencarian pasangan dihentikan.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Fungsi untuk membatalkan proses dan keluar
def cancel(update, context):
    user = update.message.from_user
    update.message.reply_text('Proses dibatalkan. Sampai jumpa!')
    return ConversationHandler.END

def main():
    # Konfigurasi logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    # Inisialisasi bot dan token
    updater = Updater(token='TOKEN_BOT_ANDA', use_context=True)
    dispatcher = updater.dispatcher
    
    # Daftar command handler
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    # Daftar message handler
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GENDER: [MessageHandler(Filters.text & ~Filters.command, gender)],
            AGE: [MessageHandler(Filters.text & ~Filters.command, age)],
            HOBBY: [MessageHandler(Filters.text & ~Filters.command, hobby)],
            LOCATION: [MessageHandler(Filters.location, location)],
            MATCHING: [
                MessageHandler(Filters.text & ~Filters.command, start_matching),
                MessageHandler(Filters.text & ~Filters.command, choose_matching)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(conversation_handler)
    
    # Jalankan bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
