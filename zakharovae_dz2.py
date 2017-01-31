from lxml import etree
from lxml import html
import requests


class Prof:
    def __init__(self, f='', i=''):
        self.f = f  # фамилия - строка
        self.i = i  # имя - строка
        self.o = '-'  # отчество - строка
        self.phone = []  # телефон - массив со строками, мб пустым
        self.mail = []  # почта  - массив со строками, мб пустым
        self.pos = {}  # должность - словарь со строками должность-ключ, место-значение, мб пустым
        self.tags = []  # теги  - массив со строками, мб пустым

mypage = requests.get('https://www.hse.ru/org/persons/?ltr=%D0%9B;udept=22726')


def teachers_with_etree(page):
    root = etree.HTML(page.content)
    # /html/body/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[2]/div[1]
    persons = root[1][1][3][2][1][0][2][1]
    teachers = []
    for p in persons:
        new = Prof()
        if 'person' in p.attrib['class']:
            # если нет ни почты, ни телефона
            if p[0][0].attrib['class'] == 'main content small':
                fio = p[0][0][0][0][0].attrib['title'].split()
                new.f = fio[0]
                new.i = fio[1]
                # если есть отчество
                if len(fio) == 3:
                    new.o = fio[2]
                positions = p[0][0][0][1]  # внутри этой штуки массив с тегами должностей
                for pos in positions:
                    pos2 = pos.text
                    if pos2 is not None:
                        pos2 = pos2.strip('\t\n:')
                        string = []
                        for place in pos:
                            string.append(place.text)
                        new.pos[pos2] = '/'.join(string)

                # если есть теги
                try:
                    tags = p[0][0][0][2]
                    for t in tags:
                        new.tags.append(t.text)
                except:
                    pass
            # если есть почта или телефон
            else:
                for i in p[0][0]:
                    if i.tag == 'span':
                        new.phone.append(i.text)
                    # собираем емейл
                    if i.tag == 'a':
                        mail = i.attrib['data-at']
                        mail = mail.replace('"', '')
                        mail = mail.replace('[', '')
                        mail = mail.replace(']', '')
                        mail = mail.replace(',', '')
                        mail = mail.replace('-at-', '@')
                        new.mail.append(mail)
                fio = p[0][1][0][0][0].attrib['title'].split()
                new.f = fio[0]
                new.i = fio[1]
                # если есть отчество
                if len(fio) == 3:
                    new.o = fio[2]
                positions = p[0][1][0][1]  # внутри этой штуки массив с тегами должностей
                for pos in positions:
                    pos2 = pos.text
                    if pos2 is not None:
                        pos2 = pos2.strip('\t\n:')
                        string = []
                        for place in pos:
                            string.append(place.text)
                        new.pos[pos2] = '/'.join(string)
                # если есть теги
                try:
                    tags = p[0][1][0][2]
                    for t in tags:
                        new.tags.append(t.text)
                except:
                    pass
        print(new.f, new.i, new.o, new.phone, new.mail, new.pos, new.tags)
        teachers.append(new)

    return teachers


def teachers_with_xpath(page):
    teachers = []
    tree = html.fromstring(page.content)
    persons = tree.xpath('//div[@class="post person"]')
    for person in persons:
        fio = person.xpath('.//a[@class="link link_dark large b"]/text()')[1].strip().split()
        new = Prof()
        new.f = fio[0]
        new.i = fio[1]
        # если есть отчество
        if len(fio) == 3:
            new.o = fio[2]

        new.tags = person.xpath('.//a[@class="tag"]/text()')
        new.phone = person.xpath('.//div[@class="l-extra small"]/span/text()')

        mails = person.xpath('.//div[@class="l-extra small"]/a/@data-at')
        # собираем емейл
        for mail in mails:
            mail = mail.replace('"', '')
            mail = mail.replace('[', '')
            mail = mail.replace(']', '')
            mail = mail.replace(',', '')
            mail = mail.replace('-at-', '@')
            new.mail.append(mail)

        position = person.xpath('.//p[@class="with-indent7"]/span')
        for pos in position:
            pos2 = pos.xpath('./text()')[0].strip('\t\n:')
            places = pos.xpath('./a/text()')
            string = []
            for place in places:
                string.append(place)
            new.pos[pos2] = '/'.join(string)

        print(new.f, new.i, new.o, new.phone, new.mail, new.pos, new.tags)
        teachers.append(new)
    return teachers

# teachers_with_etree(mypage)
teachers_with_xpath(mypage)
