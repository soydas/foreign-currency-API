import os
import requests
import time
from termcolor import colored
from tabulate import tabulate
import tabulate


previous_response = {}
previous_response2 = {}

while True:

    try:

        response = requests.get('https://www.hsbcyatirim.com.tr/api/hsbcdata/getForeignCurrencies').json()
        headers = [colored("KUR", attrs=["bold"])]
        for h in ["TCMB Alış", "TCMB Satış", "Piyasa Alış", "Piyasa Satış", "Hsbc Alış", "Hsbc Satış"]:
            headers.append(h)
        table = []
        table.append(headers)

        for data in response:
            kur = data['Symbol']
            tcmb_alis = "{:.4f}".format(float(data['CentralBuy']))
            tcmb_satis = "{:.4f}".format(float(data['CentralSell']))
            piyasa_alis = "{:.4f}".format(float(data['OpenBuy']))
            piyasa_satis = "{:.4f}".format(float(data['OpenSell']))
            hsbc_alis = "{:.4f}".format(float(data['HsbcBuy']))
            hsbc_satis = "{:.4f}".format(float(data['HsbcSell']))

            previous_kur = previous_response.get(kur, [])
            previous_tcmb_alis = previous_kur[0] if previous_kur else tcmb_alis
            previous_tcmb_satis = previous_kur[1] if previous_kur else tcmb_satis
            previous_piyasa_alis = previous_kur[2] if previous_kur else piyasa_alis
            previous_piyasa_satis = previous_kur[3] if previous_kur else piyasa_satis
            previous_hsbc_alis = previous_kur[4] if previous_kur else hsbc_alis
            previous_hsbc_satis = previous_kur[5] if previous_kur else hsbc_satis

            row = [kur, tcmb_alis, tcmb_satis, piyasa_alis, piyasa_satis, hsbc_alis, hsbc_satis]

            # Tablodaki her bir değer için önceki değerle karşılaştırma yaparak renkli yazdırma
            for i, value in enumerate([tcmb_alis, tcmb_satis, piyasa_alis, piyasa_satis, hsbc_alis, hsbc_satis]):
                previous_value = previous_kur[i] if previous_kur else value
                if str(value) < str(previous_value):
                    row[i + 1] = colored(value, 'green')
                elif str(value) > str(previous_value):
                    row[i + 1] = colored(value, 'red')

            table.append(row)

            previous_response[kur] = [tcmb_alis, tcmb_satis, piyasa_alis, piyasa_satis, hsbc_alis, hsbc_satis]

            # Tablo başlıklarını bold ve kırmızı renkli olarak yazdırmak için:
        headers = [colored("KUR", "red", attrs=['bold']),
                   colored("TCMB ALIŞ", "red", attrs=['bold']),
                   colored("TCMB SATIŞ", "red", attrs=['bold']),
                   colored("PIYASA ALIŞ", "blue", attrs=['bold']),
                   colored("PIYASA SATIŞ", "blue", attrs=['bold']),
                   colored("HSBC ALIŞ", "yellow", attrs=['bold']),
                   colored("HSBC SATIŞ", "yellow", attrs=['bold'])]

        os.system('cls')
        print(colored("HSBC DÖVİZ KURLARI", "blue", attrs=['bold']))
        print(tabulate.tabulate(table, tablefmt="grid", floatfmt="s", stralign="left"))

        response2 = requests.get('https://www.hsbcyatirim.com.tr/api/hsbcdata/getGoldData').json()
        table2 = []
        for data in response2:
            kur2 = data['Symbol']
            if kur2 == 'SCUM':
                kur2 = 'SCUM - Serbest Piyasa Cumhuriyet Altını'
            elif kur2 == 'SGLD':
                kur2 = 'SGLD - Altın Gr / TL'
            elif kur2 == 'USD/ONS':
                kur2 = 'USD/ONS - Altın Ons / USD'
            elif kur2 == 'XAUKG':
                kur2 = 'XAUKG - Altın Gr / TL'
            elif kur2 == 'XAG':
                kur2 = 'XAG - Gümüş Gr / TL'
            elif kur2 == 'XPD':
                kur2 = 'XPD - Paladyum Gr / TL'
            elif kur2 == 'XPT':
                kur2 = 'XPT - Platin Gr / TL'

            buy = "{:.2f}".format(float(data['Buy']))
            sell = "{:.2f}".format(float(data['Sell']))
            previous_kur2 = previous_response2.get(kur2, [])
            previous_buy = previous_kur2[0] if previous_kur2 else buy
            previous_sell = previous_kur2[1] if previous_kur2 else sell
            row2 = [kur2, buy, sell]
            for i, value in enumerate([buy, sell]):
                previous_value = previous_kur2[i] if previous_kur2 else value
                if str(value) < str(previous_value):
                    row2[i + 1] = colored(value, 'green')
                elif str(value) > str(previous_value):
                    row2[i + 1] = colored(value, 'red')
            table2.append(row2)
            previous_response2[kur2] = [buy, sell]

        # os.system('cls')
        print(colored("HSBC ALTIN KURLARI", "blue", attrs=['bold']))
        print(tabulate.tabulate(table2, headers=["Symbol", "Alış", "Satış"], tablefmt="pretty", stralign="left"))

        time.sleep(5)


    except requests.exceptions.ReadTimeout:
        print("Timeout hatası! İstek zaman aşımına uğradı.")
        continue

    except requests.exceptions.JSONDecodeError:
        print("Expecting value: line X column Y (char Z)")
        continue

    except requests.exceptions.ConnectTimeout:
        print("ConnectTimeout")
        continue

    except requests.exceptions.ConnectionError:
        print("Varolan bir bağlantı uzaktaki bir ana bilgisayar tarafından zorla kapatıldı")
        continue

    except urllib3.exceptions.ProtocolError:
        print("Connection aborted.")
        continue

    except KeyboardInterrupt:
        print("KeyboardInterrupt : Klavye müdahalesi ile sonlandırıldı.")
        break
