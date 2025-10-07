from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

tanlov = input("shifrlash && deshifrlash: ").lower()

if tanlov == "shifrlash":

    kalit_tanlov = input("Kalitni o'zing yaratsanmi? ha/yo'q ").lower()
    if kalit_tanlov == "ha":
        kalit = input("Kalitni kirit: 16/24/32 bo'lishi kerak ").encode()
        if len(kalit) not in (16, 24, 32):
            raise ValueError("XATO! Kalit uzunligi faqat 16/24/32 bayt bo'ladi")
        print("Kalit qabul qilindi ")

    elif kalit_tanlov == "yo'q":
        uzunlik = int(input("Kalit uzunligini tanla: 16/24/32 "))
        if uzunlik not in (16, 24, 32):
            raise ValueError("AES kaliti faqat 16/24/32 bo'ladi")
        kalit = get_random_bytes(uzunlik)
        print("Tasodifiy kalit yaratildi ")

    else:
        print("faqat 'ha' yoki 'yo'q' deb yozing!")
        exit()

    with open("kalit", "wb") as file:
        file.write(kalit)
    print("Kalit 'kalit' fayliga yozildi ")

    jarayon = input("matn yoki fayl: ").lower()
    if jarayon == "matn":
        matn = input("Matnni kirit: ")

        shifr = AES.new(kalit, AES.MODE_EAX)
        ciphertext, tag = shifr.encrypt_and_digest(matn.encode("utf-8"))

        with open("shifr.bin", "wb") as f:

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

                with open("shifr_fayl.bin", "wb") as f:
                    [f.write(x) for x in (shifrf.nonce, tagf, ciphertextf)]

                print("Fayl shifrlanib 'shifr_fayl.bin' sifatida saqlandi")
                break
            else:
                print("Fayl topilmadi, qayta urinib ko'r!")

elif tanlov == "deshifrlash":
    while True:
        dfayl_manzili = input("Shifrlangan fayl manzilini kirit: ")
        if os.path.isfile(dfayl_manzili):
            print("Fayl topildi:", dfayl_manzili)

            kalit_manzil = input("Kalit fayli manzilini kiriting: ")
            if not os.path.isfile(kalit_manzil):
                print("Kalit fayli topilmadi!")
                continue

            with open(kalit_manzil, "rb") as kf:
                kalit = kf.read()

            with open(dfayl_manzili, "rb") as f:
                nonce, tag, ciphertext = [f.read(x) for x in (16, 16, -1)]

            try:
                deshifr = AES.new(kalit, AES.MODE_EAX, nonce=nonce)
                matn = deshifr.decrypt_and_verify(ciphertext, tag)

                with open("deshifrlangan.txt", "wb") as df:
                    df.write(matn)

                print("Deshifrlash muvaffaqiyatli yakunlandi. 'deshifrlangan.txt' fayl yaratildi.")
                break
            except Exception as e:
                print("Xato: Deshifrlash amalga oshmadi!", e)
                break
        else:
            print("Fayl topilmadi, qayta urinib ko'r!")

else:
    print("XATO! 'shifrlash' yoki 'deshifrlash' deb yoz")
