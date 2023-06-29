import requests
from bs4 import BeautifulSoup
import csv

u_link = [['Course Name', 'Link', 'Coupon']]
breaker = False

def bsdk(num):
    global breaker, u_link
    rs = requests.get('https://www.udemyfreebies.com/free-udemy-courses/'+str(num))
    soup = BeautifulSoup(rs.text, 'lxml')

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


for il in range(1, 15):
    if breaker == True:
        break
    bsdk(il)
print(u_link)
if len(u_link) > 1:
    with open('results.tsv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file, lineterminator='\n', delimiter='\t')
        writer.writerows(u_link)
else:
    print('No coupons')
