import telebot
import re
import os  

# 現在這行就不會報錯了
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# ... 下面原本的程式碼保持不變 ...

# ⚠️ 魔法少女緊急提醒：這個 Token 測試完記得去找 @BotFather 點擊 Revoke Token 換一個新的喔！
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

URL_REPLACEMENTS = {
    # X / Twitter
    r'https?://(?:www\.)?(twitter\.com|x\.com)(/[^\s]*)': r'<a href="https://fxtwitter.com\2">https://\1\2</a>',
    
    # Instagram 
    r'https?://(?:www\.)?instagram\.com(/[^\s]*)': r'<a href="https://vxinstagram.com\1">https://instagram.com\1</a>'
    
    # Threads 暫時拿掉，避免一直轉發失效網址
}

# --- 1. 這是負責轉換網址的「加工機」 ---
def fix_urls(text):
    if not text:
        return text
        
    new_text = text
    for pattern, replacement in URL_REPLACEMENTS.items():
        new_text = re.sub(pattern, replacement, new_text)
        
    # YouTube Shorts 轉換 (轉成 watch 網址大家也看得懂，所以不用隱身披風)
    new_text = re.sub(r'(https?://(?:www\.)?)youtube\.com/shorts/([a-zA-Z0-9_-]+)\S*', r'\1youtube.com/watch?v=\2', new_text)
    
    return new_text


# --- 2. 魔法少女的專屬開場白 (/start 指令) ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # 使用三個雙引號包起來，就可以自由換行排版囉！
    welcome_text = """嗨~我是你們可愛的魔法少女，我可以把以下的網址變出來喔💖
X
IG
YOUTUBE
不過魔法少女還在見習中, 如果變不出來不要生氣喔QQ"""
    
    bot.reply_to(message, welcome_text)


# --- 3. 接收 /magic 指令的區塊 ---
@bot.message_handler(commands=['magic'])
def send_magic_greeting(message):
    bot.reply_to(message, "魔法少女正在為大家施展預覽魔法✨✨！請把網址交給我吧！(⁎⁍̴̛ᴗ⁍̴̛⁎)")


# --- 4. 處理大家平常聊天與傳送網址的區塊 ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    original_text = message.text
    
    if original_text:
        # 新手防護機制：把使用者亂打的 < 或 > 換掉，避免破壞我們的 HTML 隱形披風
        safe_text = original_text.replace('<', '&lt;').replace('>', '&gt;')
        fixed_text = fix_urls(safe_text)
        
        # 判斷網址是否有被轉換
        if fixed_text != safe_text:
            try:
                # 加上 parse_mode='HTML' 讓 Telegram 看懂我們的隱形披風！
                bot.reply_to(message, fixed_text, parse_mode='HTML')
                
                # 刪除使用者的原始訊息
                bot.delete_message(message.chat.id, message.message_id)
            except telebot.apihelper.ApiTelegramException as e:
                print(f"發送失敗，可能是訊息格式有誤: {e}")


# --- 5. 啟動機器人與開發者專屬提示 ---
print("魔法少女已換上隱形披風，正在施展魔法✨✨...")
bot.polling(none_stop=True)
