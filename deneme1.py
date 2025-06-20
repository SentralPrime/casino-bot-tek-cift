from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import random
import os
import sys
from datetime import datetime

# Railway ortamı için logging
def log_with_timestamp(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}"
    print(formatted_message)
    sys.stdout.flush()  # Railway için immediate output

random_max = 6
random_min = 1
class BahisButtonClicker:
    def __init__(self):
        self.driver = None
        self.url = "https://mighty.hub.xpressgaming.net/Launcher?token=WqhFpcrRBEGSVXhCn0hNvax15BprwBJe&game=10159&backurl=https%3A%2F%2Fkingroyal619.com&mode=1&language=tr&group=master&clientPlatform=desktop&cashierurl=https%3A%2F%2Fkingroyal619.com&h=9bb45cf2e93b6ce9e1d6573eb1a11eeb"
        
        # 503 numaralı buton bilgileri (TEK butonu)
        self.tek_button = {
            'numara': 503,
            'context': 'Frame 1',
            'tag': 'DIV',
            'text': 'TEK',
            'class': 'spin2win-box__market-display grid grid-middle grid-center',
            'konum_x': 805,
            'konum_y': 424,
            'tur': 'Bahis Seçeneği'
        }
        
        # 500 numaralı buton bilgileri (ÇİFT butonu)
        self.cift_button = {
            'numara': 500,
            'context': 'Frame 1',
            'tag': 'DIV',
            'text': 'ÇİFT',
            'class': 'spin2win-box__market-display grid grid-middle grid-center',
            'konum_x': 604,
            'konum_y': 424,
            'tur': 'Bahis Seçeneği'
        }
        
        # 504 numaralı buton bilgileri (OYNA butonu)
        self.play_button = {
            'numara': 504,
            'context': 'Frame 1',
            'tag': 'DIV',
            'text': 'Boş',
            'class': 'grid grid-middle grid-center casino-game-play-button icon-play-minimal',
            'id': 'game-play-button',
            'konum_x': 1130,
            'konum_y': 556,
            'tur': 'Oyun Butonu'
        }
        
    def setup_driver(self):
        """Chrome WebDriver'ı kurulum - Headless mode ile"""
        chrome_options = Options()
        
        # Her durumda headless mode
        chrome_options.add_argument("--headless")
        log_with_timestamp("🔧 Chrome Headless mode aktif")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        
        # Stability için ek ayarlar
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        
        # Railway ortamı için ek ayarlar
        if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('PORT'):
            chrome_options.add_argument("--disable-javascript")
            chrome_options.add_argument("--single-process")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-software-rasterizer")
            chrome_options.add_argument("--remote-debugging-port=9222")
            log_with_timestamp("🚂 Railway ortamı tespit edildi - Optimize edilmiş ayarlar kullanılıyor")
        
        try:
            # webdriver-manager ile otomatik ChromeDriver yönetimi
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_window_size(1920, 1080)
            log_with_timestamp("✅ Chrome WebDriver başlatıldı (Headless Mode)")
        except Exception as e:
            log_with_timestamp(f"❌ Chrome WebDriver başlatılırken hata: {str(e)}")
            raise
        
    def load_page(self):
        """Sayfayı yükle"""
        log_with_timestamp("🌐 Casino sitesine gidiliyor...")
        try:
            self.driver.get(self.url)
            
            log_with_timestamp("⏳ Sayfa yükleniyor (15 saniye bekleniyor)...")
            time.sleep(15)
            
            WebDriverWait(self.driver, 30).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            log_with_timestamp("✅ Sayfa tamamen yüklendi")
        except Exception as e:
            log_with_timestamp(f"❌ Sayfa yüklenirken hata: {str(e)}")
            raise
        
    def switch_to_game_frame(self):
        """Oyun frame'ine geç"""
        log_with_timestamp("🖼️ Oyun frame'ine geçiliyor...")
        
        try:
            # Ana sayfaya dön
            self.driver.switch_to.default_content()
            
            # İlk iframe'i bul ve geç
            frames = self.driver.find_elements(By.TAG_NAME, "iframe")
            if len(frames) > 0:
                self.driver.switch_to.frame(frames[0])
                log_with_timestamp("✅ Frame 1'e geçildi")
                time.sleep(3)
            else:
                log_with_timestamp("❌ Frame bulunamadı!")
        except Exception as e:
            log_with_timestamp(f"❌ Frame geçişinde hata: {str(e)}")
            
    def find_and_click_tek_button(self):
        """TEK butonunu bul ve rastgele sayıda tıkla"""
        click_count = random.randint(1, random_max)
        log_with_timestamp(f"🎯 {self.tek_button['numara']} numaralı '{self.tek_button['text']}' butonu aranıyor...")
        log_with_timestamp(f"🎲 Rastgele tıklama sayısı: {click_count}")
        
        # Farklı selector'lar ile dene
        selectors_to_try = [
            f"div.spin2win-box__market-display:contains('{self.tek_button['text']}')",
            f"div[class*='spin2win-box__market-display']",
            f"*:contains('{self.tek_button['text']}')",
            "div.spin2win-box__market-display"
        ]
        
        button_found = False
        
        for selector in selectors_to_try:
            try:
                log_with_timestamp(f"   🔍 Selector deneniyor: {selector}")
                
                if ":contains" in selector:
                    # JavaScript ile contains kullan
                    elements = self.driver.execute_script(f"""
                        return Array.from(document.querySelectorAll('div.spin2win-box__market-display')).filter(
                            el => el.textContent.trim() === '{self.tek_button['text']}'
                        );
                    """)
                    
                    if elements and len(elements) > 0:
                        element = elements[0]
                        log_with_timestamp(f"   ✅ JavaScript ile '{self.tek_button['text']}' butonu bulundu!")
                        
                        # Element bilgilerini göster
                        text = self.driver.execute_script("return arguments[0].textContent.trim();", element)
                        class_name = self.driver.execute_script("return arguments[0].className;", element)
                        location = self.driver.execute_script("return {x: arguments[0].getBoundingClientRect().left, y: arguments[0].getBoundingClientRect().top};", element)
                        
                        log_with_timestamp(f"   📊 Buton Bilgileri:")
                        log_with_timestamp(f"      Text: {text}")
                        log_with_timestamp(f"      Class: {class_name}")
                        log_with_timestamp(f"      Konum: x={int(location['x'])}, y={int(location['y'])}")
                        
                        # Çoklu tıklama işlemi
                        log_with_timestamp(f"   🖱️ '{self.tek_button['text']}' butonuna {click_count} kez tıklanıyor...")
                        
                        try:
                            # JavaScript ile çoklu tıkla
                            for i in range(click_count):
                                self.driver.execute_script("arguments[0].click();", element)
                                log_with_timestamp(f"      ✅ Tıklama {i+1}/{click_count} başarılı!")
                                time.sleep(0.1)  # Tıklamalar arası kısa bekleme
                            log_with_timestamp(f"   ✅ Toplam {click_count} JavaScript tıklaması başarılı!")
                            button_found = True
                            break
                            
                        except Exception as click_error:
                            log_with_timestamp(f"   ❌ Tıklama hatası: {str(click_error)}")
                            
                else:
                    # Normal CSS selector
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        try:
                            if element.is_displayed():
                                text = element.text.strip()
                                if text == self.tek_button['text']:
                                    log_with_timestamp(f"   ✅ '{self.tek_button['text']}' butonu bulundu!")
                                    
                                    # Element bilgilerini göster
                                    class_name = element.get_attribute('class')
                                    location = element.location
                                    
                                    log_with_timestamp(f"   📊 Buton Bilgileri:")
                                    log_with_timestamp(f"      Text: {text}")
                                    log_with_timestamp(f"      Class: {class_name}")
                                    log_with_timestamp(f"      Konum: x={location['x']}, y={location['y']}")
                                    
                                    # Çoklu tıklama işlemi
                                    log_with_timestamp(f"   🖱️ '{self.tek_button['text']}' butonuna {click_count} kez tıklanıyor...")
                                    
                                    try:
                                        for i in range(click_count):
                                            element.click()
                                            log_with_timestamp(f"      ✅ Tıklama {i+1}/{click_count} başarılı!")
                                            time.sleep(0.1)  # Tıklamalar arası kısa bekleme
                                        log_with_timestamp(f"   ✅ Toplam {click_count} normal tıklama başarılı!")
                                        button_found = True
                                        break
                                        
                                    except:
                                        # JavaScript ile çoklu tıkla
                                        for i in range(click_count):
                                            self.driver.execute_script("arguments[0].click();", element)
                                            log_with_timestamp(f"      ✅ JS Tıklama {i+1}/{click_count} başarılı!")
                                            time.sleep(0.1)  # Tıklamalar arası kısa bekleme
                                        log_with_timestamp(f"   ✅ Toplam {click_count} JavaScript tıklaması başarılı!")
                                        button_found = True
                                        break
                                        
                        except Exception as e:
                            continue
                            
                if button_found:
                    break
                    
            except Exception as e:
                log_with_timestamp(f"   ❌ Selector hatası: {str(e)}")
                continue
                
        if not button_found:
            log_with_timestamp(f"   ❌ TEK butonu bulunamadı!")
            
        return button_found
        
    def find_and_click_cift_button(self):
        """ÇİFT butonunu bul ve rastgele sayıda tıkla"""
        click_count = random.randint(random_min, random_max)
        log_with_timestamp(f"🎯 {self.cift_button['numara']} numaralı '{self.cift_button['text']}' butonu aranıyor...")
        log_with_timestamp(f"🎲 Rastgele tıklama sayısı: {click_count}")
        
        # Farklı selector'lar ile dene
        selectors_to_try = [
            f"div.spin2win-box__market-display:contains('{self.cift_button['text']}')",
            f"div[class*='spin2win-box__market-display']",
            f"*:contains('{self.cift_button['text']}')",
            "div.spin2win-box__market-display"
        ]
        
        button_found = False
        
        for selector in selectors_to_try:
            try:
                log_with_timestamp(f"   🔍 Selector deneniyor: {selector}")
                
                if ":contains" in selector:
                    # JavaScript ile contains kullan
                    elements = self.driver.execute_script(f"""
                        return Array.from(document.querySelectorAll('div.spin2win-box__market-display')).filter(
                            el => el.textContent.trim() === '{self.cift_button['text']}'
                        );
                    """)
                    
                    if elements and len(elements) > 0:
                        element = elements[0]
                        log_with_timestamp(f"   ✅ JavaScript ile '{self.cift_button['text']}' butonu bulundu!")
                        
                        # Element bilgilerini göster
                        text = self.driver.execute_script("return arguments[0].textContent.trim();", element)
                        class_name = self.driver.execute_script("return arguments[0].className;", element)
                        location = self.driver.execute_script("return {x: arguments[0].getBoundingClientRect().left, y: arguments[0].getBoundingClientRect().top};", element)
                        
                        log_with_timestamp(f"   📊 Buton Bilgileri:")
                        log_with_timestamp(f"      Text: {text}")
                        log_with_timestamp(f"      Class: {class_name}")
                        log_with_timestamp(f"      Konum: x={int(location['x'])}, y={int(location['y'])}")
                        
                        # Çoklu tıklama işlemi
                        log_with_timestamp(f"   🖱️ '{self.cift_button['text']}' butonuna {click_count} kez tıklanıyor...")
                        
                        try:
                            # JavaScript ile çoklu tıkla
                            for i in range(click_count):
                                self.driver.execute_script("arguments[0].click();", element)
                                log_with_timestamp(f"      ✅ Tıklama {i+1}/{click_count} başarılı!")
                                time.sleep(0.1)  # Tıklamalar arası kısa bekleme
                            log_with_timestamp(f"   ✅ Toplam {click_count} JavaScript tıklaması başarılı!")
                            button_found = True
                            break
                            
                        except Exception as click_error:
                            log_with_timestamp(f"   ❌ Tıklama hatası: {str(click_error)}")
                            
                else:
                    # Normal CSS selector
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        try:
                            if element.is_displayed():
                                text = element.text.strip()
                                if text == self.cift_button['text']:
                                    log_with_timestamp(f"   ✅ '{self.cift_button['text']}' butonu bulundu!")
                                    
                                    # Element bilgilerini göster
                                    class_name = element.get_attribute('class')
                                    location = element.location
                                    
                                    log_with_timestamp(f"   📊 Buton Bilgileri:")
                                    log_with_timestamp(f"      Text: {text}")
                                    log_with_timestamp(f"      Class: {class_name}")
                                    log_with_timestamp(f"      Konum: x={location['x']}, y={location['y']}")
                                    
                                    # Çoklu tıklama işlemi
                                    log_with_timestamp(f"   🖱️ '{self.cift_button['text']}' butonuna {click_count} kez tıklanıyor...")
                                    
                                    try:
                                        for i in range(click_count):
                                            element.click()
                                            log_with_timestamp(f"      ✅ Tıklama {i+1}/{click_count} başarılı!")
                                            time.sleep(0.1)  # Tıklamalar arası kısa bekleme
                                        log_with_timestamp(f"   ✅ Toplam {click_count} normal tıklama başarılı!")
                                        button_found = True
                                        break
                                        
                                    except:
                                        # JavaScript ile çoklu tıkla
                                        for i in range(click_count):
                                            self.driver.execute_script("arguments[0].click();", element)
                                            log_with_timestamp(f"      ✅ JS Tıklama {i+1}/{click_count} başarılı!")
                                            time.sleep(0.1)  # Tıklamalar arası kısa bekleme
                                        log_with_timestamp(f"   ✅ Toplam {click_count} JavaScript tıklaması başarılı!")
                                        button_found = True
                                        break
                                        
                        except Exception as e:
                            continue
                            
                if button_found:
                    break
                    
            except Exception as e:
                log_with_timestamp(f"   ❌ Selector hatası: {str(e)}")
                continue
                
        if not button_found:
            log_with_timestamp(f"   ❌ '{self.cift_button['text']}' butonu bulunamadı!")
            
        return button_found
        
    def find_and_click_play_button(self):
        """OYNA butonunu bul ve tıkla"""
        log_with_timestamp(f"\n🎯 {self.play_button['numara']} numaralı 'OYNA' butonu aranıyor...")
        
        # Farklı selector'lar ile dene
        selectors_to_try = [
            f"#{self.play_button['id']}",  # ID ile
            f"div[id='{self.play_button['id']}']",
            "div.casino-game-play-button",
            "*[class*='casino-game-play-button']",
            "*[class*='play-button']",
            "*[class*='icon-play']"
        ]
        
        button_found = False
        
        for selector in selectors_to_try:
            try:
                log_with_timestamp(f"   🔍 Selector deneniyor: {selector}")
                
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                
                for element in elements:
                    try:
                        if element.is_displayed():
                            log_with_timestamp(f"   ✅ OYNA butonu bulundu!")
                            
                            # Element bilgilerini göster
                            class_name = element.get_attribute('class')
                            id_attr = element.get_attribute('id')
                            location = element.location
                            text = element.text.strip() if element.text else 'Boş'
                            
                            log_with_timestamp(f"   📊 Buton Bilgileri:")
                            log_with_timestamp(f"      Text: {text}")
                            log_with_timestamp(f"      Class: {class_name}")
                            log_with_timestamp(f"      ID: {id_attr}")
                            log_with_timestamp(f"      Konum: x={location['x']}, y={location['y']}")
                            
                            # Tıklama işlemi
                            log_with_timestamp(f"   🖱️ OYNA butonuna tıklanıyor...")
                            
                            try:
                                element.click()
                                log_with_timestamp(f"   ✅ Normal tıklama başarılı!")
                                button_found = True
                                break
                                
                            except:
                                # JavaScript ile tıkla
                                self.driver.execute_script("arguments[0].click();", element)
                                log_with_timestamp(f"   ✅ JavaScript tıklaması başarılı!")
                                button_found = True
                                break
                                
                    except Exception as e:
                        continue
                        
                if button_found:
                    break
                    
            except Exception as e:
                log_with_timestamp(f"   ❌ Selector hatası: {str(e)}")
                continue
                
        if not button_found:
            log_with_timestamp(f"   ❌ OYNA butonu bulunamadı!")
            
        return button_found
        
    def wait_for_game_completion(self):
        """Oyun tamamlanana kadar bekle (iframe'in kaybolması)"""
        log_with_timestamp("\n⏳ Oyun tamamlanması bekleniyor...")
        log_with_timestamp("   🔍 İframe kontrolü yapılıyor...")
        
        max_wait_time = 27  # Maksimum 60 saniye bekle
        wait_count = 0
        
        while wait_count < max_wait_time:
            try:
                # Ana sayfaya dön
                self.driver.switch_to.default_content()
                
                # İframe'leri kontrol et
                frames = self.driver.find_elements(By.TAG_NAME, "iframe")
                
                if len(frames) == 0:
                    log_with_timestamp("   ✅ İframe kayboldu - Oyun tamamlandı!")
                    return True
                else:
                    log_with_timestamp(f"   ⏳İşlemler devam ediyor... ({wait_count + 1}/27)")
                    time.sleep(1)
                    wait_count += 1
                    
            except Exception as e:
                log_with_timestamp(f"   ❌ İframe kontrol hatası: {str(e)}")
                time.sleep(1)
                wait_count += 1
                
        return False
        
    def infinite_betting_loop(self):
        """Sonsuz TEK+ÇİFT döngüsü"""
        log_with_timestamp("\n🔄 SONSUZ BAHIS DÖNGÜSÜ BAŞLATILIYOR")
        log_with_timestamp("="*50)
        log_with_timestamp("💡 Döngü: TEK + ÇİFT → PLAY → Bekle → TEK + ÇİFT → PLAY → Bekle → ...")
        log_with_timestamp("🛑 Durdurmak için Ctrl+C basın")
        
        round_count = 1
        
        try:
            while True:
                log_with_timestamp(f"\n🎯 ROUND {round_count} - TEK + ÇİFT BAHSI")
                log_with_timestamp("-" * 50)
                
                # Frame'e geç
                self.switch_to_game_frame()
                
                # 1. TEK butonuna tıkla
                log_with_timestamp("\n🎯 1. ADIM: TEK BUTONUNA TIKLAMA")
                tek_success = self.find_and_click_tek_button()
                
                if tek_success:
                    log_with_timestamp("✅ TEK butonuna tıklama başarılı!")
                    time.sleep(1)
                    
                    # 2. ÇİFT butonuna tıkla
                    log_with_timestamp("\n🎯 2. ADIM: ÇİFT BUTONUNA TIKLAMA")
                    cift_success = self.find_and_click_cift_button()
                    
                    if cift_success:
                        log_with_timestamp("✅ ÇİFT butonuna tıklama başarılı!")
                        time.sleep(1)
                        
                        # 3. PLAY butonuna tıkla
                        log_with_timestamp("\n🎯 3. ADIM: PLAY BUTONUNA TIKLAMA")
                        play_success = self.find_and_click_play_button()
                        
                        if play_success:
                            log_with_timestamp("✅ PLAY butonuna tıklama başarılı!")
                            log_with_timestamp(f"\n🎉 ROUND {round_count} BAŞARILI!")
                            log_with_timestamp("   ✅ TEK butonuna tıklandı")
                            log_with_timestamp("   ✅ ÇİFT butonuna tıklandı")
                            log_with_timestamp("   ✅ PLAY butonuna tıklandı")
                            
                            # Oyun tamamlanana kadar bekle
                            self.wait_for_game_completion()
                            
                            round_count += 1
                            log_with_timestamp(f"🔄 Sonraki round hazırlanıyor...")
                            time.sleep(2)  # Sonraki round için kısa bekleme
                            
                        else:
                            log_with_timestamp(f"❌ PLAY butonuna tıklanamadı! 5 saniye bekleyip tekrar denenecek...")
                            time.sleep(5)
                            
                    else:
                        log_with_timestamp(f"❌ ÇİFT butonuna tıklanamadı! 5 saniye bekleyip tekrar denenecek...")
                        time.sleep(5)
                        
                else:
                    log_with_timestamp(f"❌ TEK butonuna tıklanamadı! 5 saniye bekleyip tekrar denenecek...")
                    time.sleep(5)
                    
        except KeyboardInterrupt:
            log_with_timestamp("\n\n🛑 KULLANICI TARAFINDAN DURDURULDU")
            log_with_timestamp(f"📊 Toplam {round_count - 1} round tamamlandı")
            
        except Exception as e:
            log_with_timestamp(f"\n❌ Döngü hatası: {str(e)}")
            log_with_timestamp("5 saniye bekleyip tekrar denenecek...")
            time.sleep(5)
    
    def run(self):
        """Ana çalıştırma fonksiyonu"""
        try:
            log_with_timestamp("🎰 SONSUZ TEK+ÇİFT BAHIS SİSTEMİ")
            log_with_timestamp("="*50)
            
            # WebDriver'ı başlat
            self.setup_driver()
            
            # Sayfayı yükle
            self.load_page()
            
            # Sonsuz döngüyü başlat
            self.infinite_betting_loop()
                
        except Exception as e:
            log_with_timestamp(f"❌ Hata oluştu: {str(e)}")
            
        finally:
            if self.driver:
                log_with_timestamp("\n🔒 Tarayıcı kapatılıyor...")
                time.sleep(2)
                self.driver.quit()
                log_with_timestamp("✅ İşlem tamamlandı!")

def main():
    clicker = BahisButtonClicker()
    clicker.run()

if __name__ == "__main__":
    main()
