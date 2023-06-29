import requests
from bs4 import BeautifulSoup
import csv

u_link = [['Course Name', 'Link', 'Coupon']]
breaker = False

def bsdk(num):
    global breaker, u_link
    headers = {
        'authority': 'www.udemyfreebies.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,kn;q=0.6',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    rs = requests.get('https://www.udemyfreebies.com/free-udemy-courses/'+str(num), headers=headers)
    soup = BeautifulSoup(rs.text, 'lxml')
    print(rs.text)

    cpns = soup.select('.col-md-4.col-sm-6 .theme-block')
    for i in cpns:
        title = i.select('div.coupon-name h4 a')[0].text
        link = i.select('div.coupon-name h4 a')[0]['href']
        coupon_type = i.select('.fa.fa-money')[0].parent.text
        urx = link.replace('https://www.udemyfreebies.com/free-udemy-course/', '')
        ury = 'https://www.udemyfreebies.com/out/' + urx
        linkx = requests.get(ury, allow_redirects=False).headers['Location'].strip()
        
        print(title)
        print(linkx)
        print(coupon_type)
        
        if '$' in coupon_type:
            coupn = linkx.split('?couponCode=')[1]
            print(coupn)
            u_link.append([title, linkx, coupn])
        else:
            breaker = True
            break
        print("=" * 100)
print(746766)

for il in range(1, 15):
    if breaker == True:
        break
    bsdk(il)

if len(u_link) > 1:
    with open('results.tsv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file, lineterminator='\n', delimiter='\t')
        writer.writerows(u_link)
else:
    print('No coupons')
