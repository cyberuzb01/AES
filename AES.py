from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

tanlov = input("shifrlash && deshifrlash: ")
if tanlov == "shifrlash":

    kalit = input("Kalitni o'zing yaratsanmi? ha/yo'q ").lower()
    if kalit == "ha":
        kalit == input("Kalitni kirit: 16/24/32 bo'lishi kerak ").encode()
        if len(kalit) not in (16, 24, 32):
            raise ValueError("XATO! Kalitni uzunligi faqat 16/24/32 bayt bo'ladi")
        print("Kalit qabul qilindi")
    elif kalit == "yo'q":
        uzunlik = int(input("Kalit uzunligini tanla: 16/24/32 "))
        if uzunlik not in (16,24,32):
            raise ValueError("AES klaiti faqat 16/24/32 bo'ladi")
        kalit = get_random_bytes(uzunlik)
    else:
        print(" ha yoki yo'qni tanla")

    with open("kalit", "wb") as file:
        file.write(kalit)
        print("Kalit yaritildi va faylga yozildi")

    jarayon = input("matn yoki fayl: ")
    if jarayon == "matn":
        matn = input("Matnni kirit: ")

        shifr = AES.new(kalit, AES.MODE_EAX)
        ciphertext, tag = shifr.encrypt_and_digest(matn.encode("utf-8"))

        with open("shifr.bin", "wb") as f:
            # tartib bilan yozamiz: nonce, tag, ciphertext
            [f.write(x) for x in (shifr.nonce, tag, ciphertext)]
        print("Matn shifrlanib 'shifr.bin' fayliga yozildi")

    elif jarayon == "fayl":
        while True:
            fayl_manzili = input("Fayl manzilini kirit: ")
            if os.path.isfile(fayl_manzili):
                print("Fayl topildi:", fayl_manzili)
                with open(fayl_manzili, "rb") as file:
                    data = file.read()
                
                shifrf = AES.new(kalit, AES.MODE_EAX)
                ciphertextf, tagf = shifrf.encrypt_and_digest(data)

                # natijani faylga yozish ham mumkin:
                with open("shifr_fayl.bin", "wb") as f:
                    [f.write(x) for x in (shifrf.nonce, tagf, ciphertextf)]

                print("Fayl shifrlanib 'shifr_fayl.bin' saqlandi")
                break
            else:
                print("Fayl topilmadi, qayta urinib ko'r! ")


    