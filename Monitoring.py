import requests
import time
from bs4 import BeautifulSoup

print("\'문재인 대통령 탄핵을 촉구합니다.\' 청원과 \'문재인 대통령님을 응원 합니다!\' 청원에 대한 모니터링을 실시합니다.")
sec = int(input("갱신 간격은 어느정도로 할 까요?: "))
print("")

TanHack = requests.get("https://www1.president.go.kr/petitions/584936") #탄핵 청원 주소
EungWon = requests.get("https://www1.president.go.kr/petitions/585683") #응원 청원 주소

thSoup = BeautifulSoup(TanHack.content, 'html.parser') #탄핵 청원 html
ewSoup = BeautifulSoup(EungWon.content, 'html.parser') #응원 청원 html

thCount = thSoup.find('span', {'class':'counter'}).text #탄핵 인원 숫자(String)
ewCount = ewSoup.find('span', {'class':'counter'}).text #응원 인원 숫자(String)

print("탄핵 청원: " + thCount)
print("응원 청원: " + ewCount)

thB4 = int("".join(thCount.split(',')))
ewB4 = int("".join(ewCount.split(',')))

time.sleep(sec)

while True:
    TanHack = requests.get("https://www1.president.go.kr/petitions/584936")  # 탄핵 청원 주소
    EungWon = requests.get("https://www1.president.go.kr/petitions/585683")  # 응원 청원 주소

    thSoup = BeautifulSoup(TanHack.content, 'html.parser')  # 탄핵 청원 html
    ewSoup = BeautifulSoup(EungWon.content, 'html.parser')  # 응원 청원 html

    thCount = thSoup.find('span', {'class': 'counter'}).text  # 탄핵 인원 숫자(String)
    ewCount = ewSoup.find('span', {'class': 'counter'}).text  # 응원 인원 숫자(String)

    thNow = int("".join(thCount.split(',')))
    ewNow = int("".join(ewCount.split(',')))

    print("--------------------------------------------------")
    print("탄핵 청원: " + thCount + ", 변동량:", thNow - thB4)
    print("응원 청원: " + ewCount + ", 변동량:", ewNow - ewB4)

    now = time.localtime()

    thFile = open('탄핵 청원인구', 'at')
    thFile.write("[+] %04d/%02d/%02d %02d:%02d:%02d 탄핵 청원인구:" % (
            now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec) + str(thNow) + " || ")
    thFile.close()
    ewFile = open('탄핵 청원인구', 'at')
    ewFile.write("%04d/%02d/%02d %02d:%02d:%02d 응원 청원인구:" % (
        now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec) + str(ewNow) + "\n")
    ewFile.close()

    if thNow - thB4 < 0:
        now = time.localtime()
        print("[-] 탄핵 청원의 청원인구가 감소되었습니다.")
        thFile = open('탄핵 청원인구 감소 기록', 'at')
        thFile.write("%04d/%02d/%02d %02d:%02d:%02d 탄핵 청원인구 감소가 감지되었습니다.\n" % (
            now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
        thFile.close()


    if ewNow - ewB4 < 0:
        now = time.localtime()
        print("[-] 응원 청원의 청원인구가 감소되었습니다.")
        ewFile = open('응원 청원인구 감소 기록', 'at')
        ewFile.write("%04d/%02d/%02d %02d:%02d:%02d 탄핵 청원인구 감소가 감지되었습니다.\n" % (
        now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
        ewFile.close()

    thB4 = thNow
    ewB4 = ewNow

    time.sleep(sec)