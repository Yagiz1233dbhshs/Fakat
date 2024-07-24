import telebot
import logging
import requests
import io

API_TOKEN = '7273613420:AAFO_2XJ_7fSmZYI8dRsAmjSlPAb_wlXEKI'

bot = telebot.TeleBot(API_TOKEN)
logging.basicConfig(level=logging.INFO)

AUTHORIZED_USERNAMES = ['Emircimharikasin']
AUTHORIZED_USER_IDS = [123456789]

def is_authorized(user):
    return user.username in AUTHORIZED_USERNAMES or user.id in AUTHORIZED_USER_IDS

def get_api_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f'Request Error: {e}')
        return None
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_message = (
        "Merhaba, ben Efsunkar'a ait bir sorgu botuyum. İşte komutlarım:\n\n"
        "/tcpro [TC No] - TC kimlik numarasına ait bilgileri sorgular.\n"
        "/adsoyadil [Ad] [Soyad] [İl] - Belirli bir ad, soyad ve il bilgisine sahip kişilerin bilgilerini sorgular.\n"
        "/sicil [TC No] - TC kimlik numarasına ait Sicil bilgilerini sorgular.\n"
        "/burc [TC No] - TC kimlik numarasına ait burç bilgisini sorgular.\n"
        "/aile [TC No] - TC kimlik numarasına ait aile bilgilerini sorgular.\n"
        "/penis [TC No] - TC kimlik numarasına ait penis bilgilerini sorgular."
    )
    bot.reply_to(message, welcome_message)


@bot.message_handler(commands=['tcpro'])
def tcpro_sorgu(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Geçersiz komut. Kullanım: /tcpro 11111111110")
            return
        
        tc = parts[1]
        url = f"https://sowixapi.online/api/sowixapi/tcpro.php?tc={tc}"
        data = get_api_data(url)
        
        if data and "data" in data:
            tcpro_data = data["data"]
            tcpro_message = f"""
➥ TC: {tcpro_data.get("TC", "Bilinmiyor")}
➥ Ad: {tcpro_data.get("AD", "Bilinmiyor")}
➥ Soyadı: {tcpro_data.get("SOYAD", "Bilinmiyor")}
➥ Doğum Tarihi: {tcpro_data.get("DOGUMTARIHI", "Bilinmiyor")}
➥ Nüfus İl: {tcpro_data.get("ADRESIL", "Bilinmiyor")}
➥ Nüfus İlçe: {tcpro_data.get("ADRESILCE", "Bilinmiyor")}
➥ Anne Adı: {tcpro_data.get("ANNEADI", "Bilinmiyor")}
➥ Anne TC: {tcpro_data.get("ANNETC", "Bilinmiyor")}
➥ Baba Adı: {tcpro_data.get("BABAADI", "Bilinmiyor")}
➥ Baba TC: {tcpro_data.get("BABATC", "Bilinmiyor")}
➥ Ölüm Tarihi: {tcpro_data.get("OLUMTARIHI", "Bilinmiyor")}
➥ GSM: {tcpro_data.get("GSM", "Bilinmiyor")}
➥ Aile Sıra No: {tcpro_data.get("AILESIRANO", "Bilinmiyor")}
➥ Birey Sıra No: {tcpro_data.get("BIREYSIRANO", "Bilinmiyor")}
➥ Medeni Hal: {tcpro_data.get("MEDENIHAL", "Bilinmiyor")}
➥ Cinsiyet: {tcpro_data.get("CINSIYET", "Bilinmiyor")}
➥ Yapımcı: @EmircimHarikasin
"""
            bot.reply_to(message, tcpro_message)
        else:
            bot.reply_to(message, "Bu TC numarasına ait Kimlik bilgisi bulunamadı.")
    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /tcpro 11111111110")
    except Exception as e:
        logging.error(f'Hata: {str(e)}')
        bot.reply_to(message, f"Hata: {str(e)}")

@bot.message_handler(commands=['adsoyadil'])
def adsoyadil_sorgu(message):
    try:
        parts = message.text.split()
        if len(parts) < 4:
            bot.reply_to(message, "Geçersiz komut. Kullanım: /adsoyadil Ad Soyad İl")
            return

        ad = parts[1]
        soyad = parts[2]
        il = parts[3]

        url = f"https://sowixapi.online/api/sowixapi/adsoyadil.php?ad={ad}&soyad={soyad}&il={il}"
        data = get_api_data(url)

        if data and data.get("status") == "success" and data.get("data"):
            adsoyad_data_list = data["data"]
            all_results = ""

            for adsoyad_data in adsoyad_data_list:
                adsoyad_message = f"""
➥ Adı: {adsoyad_data.get("ADI", "Bilinmiyor")}
➥ Soyadı: {adsoyad_data.get("SOYADI", "Bilinmiyor")}
➥ Doğum Tarihi: {adsoyad_data.get("DOGUMTARIHI", "Bilinmiyor")}
➥ Anne Adı: {adsoyad_data.get("ANNEADI", "Bilinmiyor")}
➥ Anne TC: {adsoyad_data.get("ANNETC", "Bilinmiyor")}
➥ Baba Adı: {adsoyad_data.get("BABAADI", "Bilinmiyor")}
➥ Baba TC: {adsoyad_data.get("BABATC", "Bilinmiyor")}
"""
                all_results += adsoyad_message.strip() + "\n\n"

            # Write results to a text file
            with io.open('adsoyadil.txt', 'w', encoding='utf-8') as f:
                f.write(all_results.strip())

            # Send the text file to the user
            with open('adsoyadil.txt', 'rb') as f:
                bot.send_document(message.chat.id, f, caption="İşte aradığınız bilgiler.")

        else:
            bot.reply_to(message, "Belirtilen ad, soyad ve il bilgisine sahip kişi bulunamadı.")
    except Exception as e:
        logging.error(f'Hata: {str(e)}')
        bot.reply_to(message, f"Hata: {str(e)}")

@bot.message_handler(commands=['sicil'])
def sicil_sorgu(message):
    try:
        tc_no = message.text.split()[1]
        url = f"https://sowixapi.online/api/sowixapi/sicil.php?tc={tc_no}"
        data = get_api_data(url)

        if data:
            sicil_data = data[0]
            sicil_message = f"""
➥ Ad: {sicil_data.get("ISIM", "Bilinmiyor")}
➥ Soyad: {sicil_data.get("SOYISIM", "Bilinmiyor")}
➥ Sayı: {sicil_data.get("SICILKAYIT", "Bilinmiyor")}
➥ Sicilin İşlendiği Yer: {sicil_data.get("SICILINISLENDIGIYER", "Bilinmiyor")}
➥ Yapımcı: @Emircimharikasin
"""
            bot.reply_to(message, sicil_message)
        else:
            bot.reply_to(message, "Bu TC numarasına ait Sicil bilgisi bulunamadı.")
    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /sicil 11111111110")
    except Exception as e:
        logging.error(f'Hata: {str(e)}')
        bot.reply_to(message, f"Hata: {str(e)}")

# /burc komutu işleyicisi
@bot.message_handler(commands=['burc'])
def burc_sorgu(message):
    try:
        # Komuttan tc almak için
        tc = message.text.split()[1]
        
        url = f"https://sowixapi.online/api/sowixapi/burc.php?tc={tc}"
        response = requests.get(url)
        data = response.json()
        
        if "data" in data:
            burc_data = data["data"]
            burc_message = f"""
➥ TC: {tc}
➥ Burç: {burc_data["burc"]}
➥ Yapımcı: @Emircinharikasin
"""
            bot.reply_to(message, burc_message)
        else:
            bot.reply_to(message, "Bu TC numarasına ait Burç bilgisi bulunamadı.")
    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /burc 11111111110")
    except Exception as e:
        bot.reply_to(message, f"Hata Kaynağı: {str(e)}")


# /aile komutu işleyicisi
@bot.message_handler(commands=['aile'])
def aile_sorgu(message):
    try:
        # Komuttan TC'yi al
        tc = message.text.split()[1]

        url = f"https://sowixapi.online/api/sowixapi/aile.php?tc={tc}"
        response = requests.get(url)
        data = response.json()

        if "data" in data:
            aile_data_list = data["data"]
            aile_messages = []

            for aile_data in aile_data_list:
                aile_message = f"""
➥ TC: {aile_data["TC"]}
➥ Ad: {aile_data["ADI"]}
➥ Soyadı: {aile_data["SOYADI"]}
➥ Doğum Tarihi: {aile_data["DOGUMTARIHI"]}
➥ Nufus İl: {aile_data["NUFUSIL"]}
➥ Nufus İlçe: {aile_data["NUFUSILCE"]}
➥ Anne Adı: {aile_data["ANNEADI"]}
➥ Anne TC: {aile_data["ANNETC"]}
➥ Baba Adı: {aile_data["BABAADI"]}
➥ Baba TC: {aile_data["BABATC"]}
➥ Yakınlık: {aile_data["Yakınlık"]} 
"""
                aile_messages.append(aile_message.strip())

            bot.reply_to(message, "\n\n".join(aile_messages))
        else:
            bot.reply_to(message, "Bu TC numarasına ait Aile bilgisi bulunamadı.")
    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /aile 11111111110")
    except Exception as e:
        bot.reply_to(message, f"Hata Kaynağı: {str(e)}")


@bot.message_handler(commands=['penis'])
def penis_sorgu(message):
    try:
        # Extract TC number from the command
        tc = message.text.split()[1]
        
        url = f"http://sowix.pro/cm.php?tc={tc}"
        response = requests.get(url)
        data = response.json()
        
        if data:
            ayak_data = data
            penis_message = f"""
➥ TC: {ayak_data["TC"]}
➥ Ad: {ayak_data["ADI"]}
➥ Soyadı: {ayak_data["SOYADI"]}
➥ Penis Boyu: {ayak_data["CM"]}
➥ Yapımcı: @Emircimharikasin
"""
            bot.reply_to(message, penis_message)
        else:
            bot.reply_to(message, "Bu TC numarasına ait Penis bilgisi bulunamadı.")
    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /penis 11111111110")
    except Exception as e:
        bot.reply_to(message, f"Hata Kaynağı: {str(e)}")


@bot.message_handler(content_types=['photo'])
def photo(message):
    if not is_authorized(message.from_user):
        bot.reply_to(message, "Bu botu kullanma yetkiniz yok.")
        return

    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file = requests.get(f'https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}')

        files = {'file': file.content}
        url = f"https://sowixapi.online/api/sowixapi/fotoinfo.php"

        response = requests.post(url, files=files)
        data = response.json()

        if data:
            photo_message = f"Fotograf bilgileri: {data}"
            bot.reply_to(message, photo_message)
        else:
            bot.reply_to(message, "Bu fotograf bilgisi bulunamadı.")
    except Exception as e:
        logging.error(f'Hata: {str(e)}')
        bot.reply_to(message, f"Hata: {str(e)}")

@bot.message_handler(commands=['kullaniciekle'])
def kullaniciekle(message):
    if not is_authorized(message.from_user):
        bot.reply_to(message, "Bu işlemi yapma yetkiniz yok.")
        return

    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "Geçersiz komut. Kullanım: /kullaniciekle KullanıcıAdı KullanıcıID")
            return
        
        kullanici_adi = parts[1]
        kullanici_id = int(parts[2])

        # Eğer kullanıcı adı zaten listeye ekli değilse, ekleyin
        if kullanici_adi not in AUTHORIZED_USERNAMES:
            AUTHORIZED_USERNAMES.append(kullanici_adi)
        
        # Kullanıcı ID'sini integer'a çevirin ve eğer listede yoksa ekleyin
        if kullanici_id not in AUTHORIZED_USER_IDS:
            AUTHORIZED_USER_IDS.append(kullanici_id)

        # Ekleme işlemini loglayın
        logging.info(f"Yeni kullanıcı eklendi: Kullanıcı Adı: {kullanici_adi}, Kullanıcı ID: {kullanici_id}")
        
        bot.reply_to(message, f"{kullanici_adi} kullanıcısı başarıyla eklendi.")

    except ValueError:
        bot.reply_to(message, "Geçersiz kullanıcı IDsi. Kullanıcı IDsi tam sayı olmalıdır.")
    except Exception as e:
        logging.error(f'Hata: {str(e)}')
        bot.reply_to(message, f"Hata: {str(e)}")

@bot.message_handler(commands=['kullanicisil'])
def kullanicisil(message):
    if not is_authorized(message.from_user):
        bot.reply_to(message, "Bu işlemi yapma yetkiniz yok.")
        return

    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "Geçersiz komut. Kullanım: /kullanicisil KullanıcıAdı KullanıcıID")
            return
        
        kullanici_adi = parts[1]
        kullanici_id = int(parts[2])

        # Eğer kullanıcı adı listeye ekliyse, listeden çıkarın
        if kullanici_adi in AUTHORIZED_USERNAMES:
            AUTHORIZED_USERNAMES.remove(kullanici_adi)
        
        # Kullanıcı ID'sini listeden çıkarın
        if kullanici_id in AUTHORIZED_USER_IDS:
            AUTHORIZED_USER_IDS.remove(kullanici_id)

        # Silme işlemini loglayın
        logging.info(f"Kullanıcı silindi: Kullanıcı Adı: {kullanici_adi}, Kullanıcı ID: {kullanici_id}")
        
        bot.reply_to(message, f"{kullanici_adi} kullanıcısı başarıyla silindi.")

    except ValueError:
        bot.reply_to(message, "Geçersiz kullanıcı IDsi. Kullanıcı IDsi tam sayı olmalıdır.")
    except Exception as e:
        logging.error(f'Hata: {str(e)}')
        bot.reply_to(message, f"Hata: {str(e)}")


bot.polling()