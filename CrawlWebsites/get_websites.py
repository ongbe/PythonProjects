import requests
from bs4 import BeautifulSoup
import csv


headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}


def get_html(url):
    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        html = r.text
        return html
    except BaseException:
        return


def get_category_list(url, clist):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    categories = soup.find(
        id='main_container').find_all(
        'div', class_='category-header')
    for category in categories:
        url = 'https://theporndude.com' + category.h2.a.get('href')
        name = category.h2.a.text
        clist.append(
            {
                '类别名': name,
                '链接': url
            }
        )


def get_website_url_list(clist):
    set_csv_header()
    for each in clist:
        category_url = each['链接']
        category_name = each['类别名']
        html = get_html(category_url)
        soup = BeautifulSoup(html, 'lxml')
        contents = soup.find('div', class_='url_links_wrapper url_links_hover').find_all('div', class_='url_link_container')
        count = 0
        for content in contents:
            count = count + 1
            website_name = content.find('div', class_='url_link_title').a.text.split()[0]
            website_url = content.find('div', class_='url_link_title').a.get('data-site-link')
            save_to_csv([[category_name, str(count), website_name, website_url]])
            print('\r当前正在爬取<%s>类别链接\t爬取进度：%.1f%%' % (category_name, count * 100 / 100), end='')


def save_to_csv(rlist):
    with open('results.csv', 'a+', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows(rlist)


def set_csv_header():
    with open('results.csv', 'a+', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows([['类别名', '序号', '网站名', '链接']])


def main():
    start_url = 'https://theporndude.com/zh'
    category_list = []
    get_category_list(start_url, category_list)
    get_website_url_list(category_list)


if __name__ == '__main__':
    main()
