from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import threading
import time
import json
from datetime import datetime
import sys
import os
import random
from selenium.webdriver.common.by import By
from deneme1 import BahisButtonClicker

app = Flask(__name__)
app.config['SECRET_KEY'] = 'casino_bot_secret'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global değişkenler
bot_instance = None
bot_thread = None
bot_running = False
round_count = 0
terminal_output = []
account_owner = "Ömer Gezer"

def emit_terminal_output(timestamp, message):
    """Terminal çıktısını WebSocket ile gönder"""
    try:
        socketio.emit('terminal_output', {
            'timestamp': timestamp,
            'message': message
        })
    except Exception as e:
        print(f"WebSocket emit hatası: {e}")

def emit_round_update(round_num):
    """Round güncellemesini WebSocket ile gönder"""
    try:
        socketio.emit('round_update', {'round': round_num})
    except Exception as e:
        print(f"Round update emit hatası: {e}")

def custom_log_with_timestamp(message):
    """Custom log function that captures output"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}"
    
    # Terminal çıktısını kaydet
    terminal_output.append({
        'timestamp': timestamp,
        'message': message
    })
    
    # Son 100 çıktıyı tut
    if len(terminal_output) > 100:
        terminal_output.pop(0)
    
    # Console'a da yazdır
    print(formatted_message)
    sys.stdout.flush()
    
    # WebSocket ile gönder
    emit_terminal_output(timestamp, message)

def run_bot():
    """Bot çalıştırma fonksiyonu"""
    global bot_instance, bot_running, round_count
    
    try:
        custom_log_with_timestamp("🎰 Bot başlatılıyor...")
        bot_instance = BahisButtonClicker()
        
        # WebDriver'ı başlat
        bot_instance.setup_driver()
        
        # Sayfayı yükle
        custom_log_with_timestamp("⏳ 15 saniye bekleme süresi başladı...")
        bot_instance.load_page()
        custom_log_with_timestamp("✅ Sayfa yüklendi, bot hazır!")
        
        round_count = 1
        
        while bot_running:
            try:
                custom_log_with_timestamp(f"🎯 ROUND {round_count} başlıyor...")
                
                # Frame'e geç
                bot_instance.switch_to_game_frame()
                
                # TEK butonuna tıkla
                tek_click_count = random.randint(1, 6)
                tek_success = custom_click_tek_button(bot_instance, tek_click_count)
                
                if tek_success and bot_running:
                    custom_log_with_timestamp(f"✅ TEK butonuna ({tek_click_count}) defa basıldı")
                    time.sleep(1)
                    
                    # ÇİFT butonuna tıkla
                    cift_click_count = random.randint(1, 6)
                    cift_success = custom_click_cift_button(bot_instance, cift_click_count)
                    
                    if cift_success and bot_running:
                        custom_log_with_timestamp(f"✅ ÇİFT butonuna ({cift_click_count}) defa basıldı")
                        time.sleep(1)
                        
                        # PLAY butonuna tıkla
                        play_success = custom_click_play_button(bot_instance)
                        
                        if play_success and bot_running:
                            custom_log_with_timestamp("✅ PLAY butonuna basıldı, işlemlerin bitmesi bekleniyor (27 saniye)...")
                            
                            # Round sayısını güncelle
                            try:
                                emit_round_update(round_count)
                            except:
                                pass
                            
                            # 27 saniye bekle
                            custom_wait_for_completion()
                            
                            round_count += 1
                            custom_log_with_timestamp(f"🎉 ROUND {round_count-1} tamamlandı! Sonraki round hazırlanıyor...")
                            time.sleep(3)
                            
                        else:
                            custom_log_with_timestamp("❌ PLAY butonuna basılamadı! Tekrar deneniyor...")
                            time.sleep(5)
                            
                    else:
                        custom_log_with_timestamp("❌ ÇİFT butonuna basılamadı! Tekrar deneniyor...")
                        time.sleep(5)
                        
                else:
                    custom_log_with_timestamp("❌ TEK butonuna basılamadı! Tekrar deneniyor...")
                    time.sleep(5)
                    
            except Exception as e:
                custom_log_with_timestamp(f"❌ Hata oluştu: {str(e)}")
                time.sleep(5)
                
    except Exception as e:
        custom_log_with_timestamp(f"❌ Bot hatası: {str(e)}")
        
    finally:
        if bot_instance and bot_instance.driver:
            custom_log_with_timestamp("🔒 Tarayıcı kapatılıyor...")
            bot_instance.driver.quit()
            custom_log_with_timestamp("✅ Bot durduruldu!")

def custom_click_tek_button(bot_instance, click_count):
    """TEK butonuna basma"""
    try:
        bot_instance.switch_to_game_frame()
        elements = bot_instance.driver.execute_script("""
            return Array.from(document.querySelectorAll('div.spin2win-box__market-display')).filter(
                el => el.textContent.trim() === 'TEK'
            );
        """)
        
        if elements and len(elements) > 0:
            element = elements[0]
            for i in range(click_count):
                bot_instance.driver.execute_script("arguments[0].click();", element)
                time.sleep(0.1)
            return True
    except:
        pass
    return False

def custom_click_cift_button(bot_instance, click_count):
    """ÇİFT butonuna basma"""
    try:
        bot_instance.switch_to_game_frame()
        elements = bot_instance.driver.execute_script("""
            return Array.from(document.querySelectorAll('div.spin2win-box__market-display')).filter(
                el => el.textContent.trim() === 'ÇİFT'
            );
        """)
        
        if elements and len(elements) > 0:
            element = elements[0]
            for i in range(click_count):
                bot_instance.driver.execute_script("arguments[0].click();", element)
                time.sleep(0.1)
            return True
    except:
        pass
    return False

def custom_click_play_button(bot_instance):
    """PLAY butonuna basma"""
    try:
        bot_instance.switch_to_game_frame()
        element = bot_instance.driver.find_element(By.ID, "game-play-button")
        if element.is_displayed():
            bot_instance.driver.execute_script("arguments[0].click();", element)
            return True
    except:
        pass
    return False

def custom_wait_for_completion():
    """27 saniye bekleme"""
    for i in range(27):
        if not bot_running:
            break
        time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html', account_owner=account_owner)

@app.route('/start_bot', methods=['POST'])
def start_bot():
    global bot_thread, bot_running
    
    if not bot_running:
        bot_running = True
        # SocketIO background task olarak çalıştır
        socketio.start_background_task(run_bot)
        
        return jsonify({
            'status': 'success',
            'message': 'Bot başlatıldı!',
            'running': True
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Bot zaten çalışıyor!',
            'running': True
        })

@app.route('/stop_bot', methods=['POST'])
def stop_bot():
    global bot_running
    
    if bot_running:
        bot_running = False
        custom_log_with_timestamp("🛑 Bot durdurma komutu verildi...")
        
        return jsonify({
            'status': 'success',
            'message': 'Bot durduruldu!',
            'running': False
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Bot zaten durmuş!',
            'running': False
        })

@app.route('/status')
def status():
    return jsonify({
        'running': bot_running,
        'round': round_count,
        'account_owner': account_owner
    })

@app.route('/logs')
def logs():
    return jsonify(terminal_output)

@socketio.on('connect')
def handle_connect():
    emit('connected', {'data': 'Bağlantı başarılı!'})
    emit('round_update', {'round': round_count})
    # Son çıktıları gönder
    for output in terminal_output[-10:]:  # Son 10 çıktıyı gönder
        emit('terminal_output', output)

if __name__ == '__main__':
    # Railway için PORT environment variable kullan
    port = int(os.environ.get('PORT', 5001))
    debug_mode = not os.environ.get('RAILWAY_ENVIRONMENT', False)
    
    socketio.run(app, 
                debug=debug_mode, 
                host='0.0.0.0', 
                port=port,
                allow_unsafe_werkzeug=True) 