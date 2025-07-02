import cv2
import numpy as np
import os

secenekler = ['A', 'B', 'C', 'D', 'E']

cevap_anahtari_path = "optik_formlar/cevap_anahtari.png"

def parse_optik_form(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

 
    ogr_no = ""
    for i in range(10):
        column_x = 180 + i * 50 + 10
        digit = None
        for j in range(10):
            y = 70 + j * 20 + 10
            roi = thresh[y-5:y+5, column_x-5:column_x+5]
            if cv2.countNonZero(roi) > 20:
                digit = str(j)
                break
        ogr_no += digit if digit is not None else "?"


    cevaplar = []
    for i in range(10):
        y = 300 + i * 40 + 10
        marked = None
        for j in range(5):
            x = 120 + j * 60 + 10
            roi = thresh[y-5:y+5, x-5:x+5]
            if cv2.countNonZero(roi) > 20:
                marked = secenekler[j]
                break
        cevaplar.append(marked if marked else "")

    return ogr_no, cevaplar

def cevap_anahtari_oku(path):
    _, cevaplar = parse_optik_form(path)
    return cevaplar

def main():
    anahtar = cevap_anahtari_oku(cevap_anahtari_path)
    print("✅ Cevap Anahtarı:", anahtar)

    for i in range(1, 11):  
        dosya = f"optik_formlar/ogrenci_{i:02d}.png"
        if not os.path.exists(dosya):
            print(f"❌ Dosya bulunamadı: {dosya}")
            continue

        ogr_no, cevaplar = parse_optik_form(dosya)

        dogru = sum(1 for k, c in enumerate(cevaplar) if c == anahtar[k])
        bos = sum(1 for c in cevaplar if c == "")
        yanlis = 10 - dogru - bos

        print(f"\n📄 Öğrenci No: {ogr_no}")
        print(f"✅ Doğru: {dogru} ❌ Yanlış: {yanlis} ⭕ Boş: {bos}")
        print("📝 Cevaplar:", cevaplar)

if __name__ == "__main__":
    main()
