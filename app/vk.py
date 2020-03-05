import requests
import csv
import datetime

from datetime import datetime



# обрабатываем ссылки и получаем id паблика или его домен
def public_url(urls, c):
    data_public_url = []
    print(urls)
    i = 0
    count_members = []
    while i < c:

        try:
            if urls[i].find('public') == -1:
                data_public_url.append(['1', urls[i][urls[i].find('vk.com/') + 7:len(urls[i])]])
            else:
                data_public_url.append(['0', ('-' + urls[i][urls[i].find('public') + 6:len(urls[i])])])
        except:
            pass
        i += 1
    return data_public_url


# получаем все посты паблика
def get_all_posts(data_public_url, count_url):
    url = 'https://api.vk.com/method/wall.get'
    ver = '5.103'
    # сервисный ключ вк приложения
    token = 'a92ba8d9a92ba8d9a92ba8d9d8a9444243aa92ba92ba8d9f77eb8bc3a634677be0a63ed'
    # id или домен сообщества
    count = 100
    all_posts = []
    count_members = []
    # костыль
    tmp_m = []
    i = 0

    # перебираем
    while i < count_url:
        # определяем id или домен сообщества в data
        if data_public_url[i][0] == '0':
            param_domain_or_id = 'owner_id'
        else:
            param_domain_or_id = 'domain'
        print('Паблик ' + data_public_url[i][1])

        c = requests.get(url,
                         params={
                             param_domain_or_id: data_public_url[i][1],
                             'access_token': token,
                             'v': ver,
                             'count': 1,
                             'offset': 0
                         }
                         )

        # получаем количество участников в сообществе
        id = str(c.json()['response']['items'][0]['owner_id'])
        tmp = requests.get('https://api.vk.com/method/groups.getById?group_ids=' + id[1:len(
            id)] + '&access_token=a92ba8d9a92ba8d9a92ba8d9d8a9444243aa92ba92ba8d9f77eb8bc3a634677be0a63ed&fields=members_count&v=5.103')
        tmp_m.append(tmp.json())
        count_members.append(tmp_m[i]['response'][0]['members_count'])
        print('кол-во участников ')
        print(count_members)
        print('кол-во участников ')

        # получаем количество постов в сообществе
        count_posts = c.json()['response']['count']
        print('кол-публикаций ')
        print(count_posts)

        # Получаем все посты
        posts = []
        offset = 0
        while offset < count_posts:
            print('берем посты из ' + data_public_url[i][1])
            #print(count_posts)
            #print(offset)
            r = requests.get(url,
                             params={
                                 param_domain_or_id: data_public_url[i][1],
                                 'access_token': token,
                                 'v': ver,
                                 'count': count,
                                 'offset': offset
                             }
                             )
            #print(r.json()['response']['items'])
            data = r.json()['response']['items'];
            posts.extend(data)
            offset += 100

        # добавляем собранные посты по паблику в общий список
        all_posts.append(posts)
        # Переход на следующий паблик
        i += 1

    return all_posts  # , count_members


# записываем данные в csv
def csv_writer(data):
    with open('vk.csv', 'w') as file:
        a_pen = csv.writer(file, delimiter=';')
        a_pen.writerow(('likes', 'comments'))
        for post in data:
            a_pen.writerow((post['likes']['count'], post['comments']['count']))
            # post['likes']['count'], post['comments']['count']), post['reposts']['count'], post['views']['count']
            # like_count += post['likes']['count']


# считаем показатели
def count_param(data):
    count_data = []
    i = 0
    j = 0
    while i < len(data):
        tmp_l = 0
        tmp_c= 0
        tmp_r = 0
        tmp_v = 0
        print('Длина ' + str(len(data[i])))
        while j < len(data[i]):
            #value = datetime.datetime.fromtimestamp(data[i][j]['date'])
            #print(value.strftime('%Y-%m-%d'))
            tmp_l += (int(data[i][j]['likes']['count']))
            tmp_c += (int(data[i][j]['comments']['count']))
            tmp_r += (int(data[i][j]['reposts']['count']))
            try:
                tmp_v += (data[i][j]['views']['count'])
            except:
                pass
            tmp_count_data = [tmp_l, tmp_c, tmp_r, tmp_v]
            j += 1
        count_data.append(tmp_count_data)
        i += 1
        j = 0

    return count_data

# считаем показатели
def isnsert_data_by_date(data):
    count_data = []

    i = 0
    j = 0
    date_search = int('2019')

    # Сразу проверяются все условия.
    # Если год не делится на 4 или делится на 100, но не на 400,
    # то он обычный. Во всех остальных случаях - високосный.
    if date_search % 4 != 0 or (date_search % 100 == 0 and date_search % 400 != 0):
        day_vis = 28
    else:
        day_vis = 29

    date_list = [
        ['%s-01-01 00:00:00'  % (date_search), '%s-01-31 00:00:00'  % (date_search), 'Январь'],
        ['%s-02-01 00:00:00'  % (date_search), '%s-02-%s 00:00:00'  % (date_search, day_vis), 'Февраль'],
        ['%s-03-01 00:00:00'  % (date_search), '%s-03-30 00:00:00'  % (date_search), 'Март'],
        ['%s-04-01 00:00:00'  % (date_search), '%s-04-31 00:00:00'  % (date_search), 'Апрель'],
        ['%s-05-01 00:00:00'  % (date_search), '%s-05-30 00:00:00'  % (date_search), 'Май'],
        ['%s-06-01 00:00:00'  % (date_search), '%s-06-30 00:00:00'  % (date_search), 'Июнь'],
        ['%s-07-01 00:00:00'  % (date_search), '%s-07-31 00:00:00'  % (date_search), 'Июль'],
        ['%s-08-01 00:00:00'  % (date_search), '%s-08-31 00:00:00'  % (date_search), 'Август'],
        ['%s-09-01 00:00:00'  % (date_search), '%s-09-31 00:00:00'  % (date_search), 'Сентябрь'],
        ['%s-10-01 00:00:00'  % (date_search), '%s-10-31 00:00:00'  % (date_search), 'Октябрь'],
        ['%s-11-01 00:00:00'  % (date_search), '%s-11-31 00:00:00'  % (date_search), 'Ноябрь'],
        ['%s-12-01 00:00:00'  % (date_search), '%s-12-31 00:00:00'  % (date_search), 'Декабрь']
    ]

    #d1 = datetime.strptime('2019-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    #d3 = datetime.strptime('2019-12-31 00:00:00', '%Y-%m-%d %H:%M:%S')

    #d2 = value.strftime('%Y-%m-%d %H:%M:%S')
    #d2 = datetime.strptime(, '%Y-%m-%d')

    while i < len(data):
        while j < len(data[i]):
            # value = datetime.datetime.fromtimestamp(data[i][j]['date'])
            # print(value.strftime('%Y-%m-%d'))
            p = 12
            while p >= 1:
                print('id сообщества %s, месяц: %s' % (i, date_list[p-1][2]))
                print('i %s, j %s p %s date is data %s' % (i, j, p, datetime.fromtimestamp(data[i][j]['date'])))
                try:
                    if (datetime.strptime((date_list[p - 1][0]), '%Y-%m-%d %H:%M:%S') <= datetime.fromtimestamp(
                            data[i][j]['date']) <= datetime.strptime((date_list[p - 1][1]), '%Y-%m-%d %H:%M:%S')):
                        print(datetime.fromtimestamp(data[i][j]['date']))
                    else:
                        print('не найдено')
                except:
                    print('чет не вышло')
                p -= 1
            j += 1
        i += 1
        j = 0



    return count_data

def main():
    # адрес(а) сообщества
    #urls = ['https://vk.com/kddz2018', 'https://vk.com/minimaks_company', 'https://vk.com/flowerpoint', 'https://vk.com/mcopanacea']
    urls = ['https://vk.com/kddz2018', 'https://vk.com/mcopanacea']
    # подсчитываем кол-во ссылок
    count_url = len(urls)
    # обрабатываем ссылки
    # получаем инфу о постах
    posts = get_all_posts(public_url(urls, count_url), count_url)
    # считаем общие количество параметров по группам
    isnsert_data_by_date(posts)
    count_all_time = count_param(posts)
    print(count_all_time)
    print(count_param)

    # csv_writer(posts)
    # подсчитываем показатели
    # count_param(posts)


if __name__ == '__main__':
    main()
