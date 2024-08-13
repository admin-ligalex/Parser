from deep_translator import GoogleTranslator

# Текст на китайском языке
text = "D-MAX 2021款 1.9T手动四驱柴油Global劲动型RZ4E"  # Привет, как дела в переводе на русский

# Переводим текст с китайского на русский
translated = GoogleTranslator(source='zh-TW', target='ru').translate(text)

# Выводим оригинальный и переведенный текст
print(f"Оригинал: {text}")
print(f"Перевод: {translated}")