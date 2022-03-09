import sqlalchemy


class BD_library:
    def __init__(self, information_file):
        self.information_file = information_file

    def creature_table(self):
        sel = connection.execute(""" create table if not exists music_genre (
            id serial primary key,
            genre_name varchar(40) unique not null
        );
        create table if not exists musician (
            id serial primary key,
            musician_name varchar(40)  not null
        );
        create table if not exists musician_genre (
            id serial primary key,
            musician_id integer references musician(id),
            music_genre varchar(40) references music_genre(genre_name)
        );
        create table if not exists album (
            id serial primary key,
            album_name varchar(40) unique not null,
            release_year integer check (release_year > 0)
        );
        create table if not exists album_musician (
            id serial primary key,
            musician_id integer references musician(id),
            album varchar(40) references album(album_name)
        );
        create table if not exists track (
            id serial primary key,
            track_name varchar(40) unique not null,
            duration serial check (duration > 0),
            album_name varchar(40) references album (album_name)
        );
        create table if not exists collection (
            id serial primary key,
            collection_name varchar(40)unique not null,
            release_year integer check (release_year > 0)
        );
        create table if not exists collection_track (
            id serial primary key,
            track_id integer references track(id),
            collection_name varchar(40) references collection(collection_name)
        );
       """)
        return print('Таблицы созданы')

    def BD_music_genre(self):
        for i in self.information_file:
            dict_musician_genre = i["musician"]
            for k in dict_musician_genre:
                musician = dict_musician_genre[k]["music_genre"]
                for genre_name in musician:
                    sel = connection.execute(
                        f"INSERT into music_genre (genre_name) values ('{genre_name}') ON CONFLICT DO NOTHING; ")
        return print('Данные в таблицу music_genre загружены')

    def musician(self):
        for i in self.information_file:
            for name_musician in i["musician"]:
                sel = connection.execute(
                    f"INSERT into musician (musician_name) values ('{name_musician}') ON CONFLICT DO NOTHING; ")

        return print('Данные в таблицу musician загружены')

    def musician_genre(self):
        for i in self.information_file:
            for name_musician in i["musician"]:
                musician = i["musician"][name_musician]["music_genre"]
                for genre_name in musician:
                    sel = connection.execute(
                        f"SELECT id, musician_name FROM musician"
                        f" WHERE musician_name IN('{name_musician}'); ").fetchall()
                    for musician_id in sel:
                        if musician_id[1] == name_musician:
                            sel = connection.execute(
                                f"INSERT into musician_genre (musician_id,music_genre)"
                                f" values ('{musician_id[0]}','{genre_name}') ON CONFLICT DO NOTHING; ")
        return print('Данные в таблицу musician_genre загружены')

    def album(self):
        for i in self.information_file:
            for name_musician in i["musician"]:
                musician = i["musician"][name_musician]["album"]
                for album in musician:
                    release_year = musician[album]['release_year']
                    sel = connection.execute(
                        f"INSERT into album (album_name,release_year)"
                        f" values ('{album}','{release_year}') ON CONFLICT DO NOTHING; ")
        return print('Данные в таблицу album загружены')

    def album_musician(self):
        for i in self.information_file:
            for name_musician in i["musician"]:
                musician = i["musician"][name_musician]["album"]
                for album in musician:
                    sel = connection.execute(f"""
                        SELECT id, musician_name FROM musician
                         WHERE musician_name IN('{name_musician}'); """).fetchall()
                    for musician_id in sel:
                        if musician_id[1] == name_musician:
                            sel = connection.execute(
                                f"""INSERT into album_musician (musician_id, album)
                                 values ('{musician_id[0]}','{album}') ON CONFLICT DO NOTHING; """)
        return print('Данные в таблицу album_musician загружены')

    def track(self):
        for i in self.information_file:
            for name_musician in i["musician"]:
                musician = i["musician"][name_musician]["album"]
                for album in musician:
                    for json_track_name in musician[album]['track']:
                        for track_name in json_track_name:
                            duration = json_track_name[track_name]
                            sel = connection.execute(f"""INSERT into track (track_name, duration, album_name) 
                                 values ('{track_name}','{duration}','{album}')
                                  ON CONFLICT DO NOTHING;""")
        return print('Данные в таблицу track загружены')

    def collection(self):
        for i in self.information_file:
            for name_musician in i["musician"]:
                musician = i["musician"][name_musician]["collection"]
                for collection in musician:
                    release_year = musician[collection]['release_year']
                    sel = connection.execute(
                        f"INSERT into collection (collection_name,release_year)"
                        f" values ('{collection}','{release_year}') ON CONFLICT DO NOTHING; ")
        return print('Данные в таблицу collection загружены')

    def collection_track(self):
        for i in self.information_file:
            for name_musician in i["musician"]:
                musician = i["musician"][name_musician]["collection"]
                for collection in musician:
                    for json_track_name in musician[collection]['track']:
                        for track_name in json_track_name:
                            duration = json_track_name[track_name]
                            sel = connection.execute(
                                f"SELECT id, track_name FROM track WHERE track_name IN('{track_name}'); ").fetchall()
                            for track_id in sel:
                                if track_id[1] == track_name:
                                    sel = connection.execute(
                                        f"INSERT into collection_track (track_id, collection_name )"
                                        f" values ('{track_id[0]}','{collection}') ON CONFLICT DO NOTHING; ")
        return print('Данные в таблицу collection_track загружены')

    def muscician_id(self, data2):
        sel = connection.execute(
            f"SELECT id, musician_name FROM musician WHERE musician_name IN('{data2}'); ").fetchall()
        for musician_id in sel:
            if musician_id[1] == data2:
                return musician_id[0]

    def track_id(self, data1):
        sel1 = connection.execute(
            f"SELECT id, track_name FROM track WHERE track_name IN('{data1}'); ").fetchall()
        for track_id in sel1:
            if track_id[1] == data1:
                return track_id[0]

    def album_down_track(self, i):
        for name_musician in i["musician"]:
            musician = i["musician"][name_musician]["album"]
            for album in musician:
                for json_track_name in musician[album]['track']:
                    for track_name in json_track_name:
                        sel = connection.execute(f"""INSERT into musician_track (id_musician, track_id )  
                                               values ('{self.muscician_id(name_musician)}','{self.track_id(track_name)}')  
                                              ON CONFLICT DO NOTHING; """)
        return 'выгруизил треки из альбомов'

    def collection_down_track(self, i):
        for name_musician in i["musician"]:
            musician = i["musician"][name_musician]["collection"]
            for collection in musician:
                for json_track_name in musician[collection]['track']:
                    for track_name in json_track_name:
                        sel = connection.execute(f"""INSERT into musician_track (id_musician, track_id )  
                        values ('{self.muscician_id(name_musician)}','{self.track_id(track_name)}')  
                        ON CONFLICT DO NOTHING; """)
        return 'выгрузили треки из сборников '

    def musician_track(self):
        for i in self.information_file:
            self.album_down_track(i)
            self.collection_down_track(i)
        return print('Данные в таблицу musician_track загружены')

    def DROP_TABLE(self):
        sel = connection.execute(""" DROP TABLE  album, album_musician ,
           collection_track ,musician ,musician_genre ,track,collection, music_genre CASCADE;""")
        return print(' full table delete')

    def search_album_year(self, data: int):
        sel = connection.execute(
            f"SELECT album_name,release_year FROM album WHERE release_year IN('{data}'); ").fetchall()
        return print(f'Название и год выхода альбомов, вышедших в {data} году: {sel}')

    def search_name_long_track(self):
        sel = connection.execute(
            f"SELECT track_name,duration FROM track ORDER BY duration ; ").fetchall()
        return print(f'Название и продолжительность самого длительного трека: {sel[-1]}')

    def search_name_time_track(self, data: int):
        sel = connection.execute(
            f"SELECT track_name,duration FROM track WHERE duration >= {data} ; ").fetchall()
        return print(f'название треков, продолжительность которых не менее {data} секунд;: {sel}')

    def search_collection_time_period(self, data_start: int, data_end: int):
        sel = connection.execute(
            f"""SELECT collection_name,release_year FROM collection
             WHERE release_year BETWEEN {data_start} AND {data_end}; """).fetchall()
        return print(f'Названия сборников, вышедших в период с {data_start} по {data_end} год включительно: {sel}')

    def search_track_name(self, data: str):
        sel = connection.execute(
            f"""SELECT track_name
             FROM track 
             WHERE track_name LIKE '%%{data}%%'; """).fetchall()
        return print(f'название треков, которые содержат слово {data}: {sel}')

    def search_name_one_musician(self):
        sel = connection.execute(f"""SELECT track_name 
        FROM track 
        WHERE track_name NOT LIKE '%% %%'; """).fetchall()
        return print(f'Треки, название которых состоит из 1 слова: {sel}')

    def count_genre_musician(self):
        text = []
        sel = connection.execute(
            """SELECT count(musician_id) , music_genre 
            FROM  musician_genre 
            GROUP by music_genre ;""").fetchall()
        for data in sel:
            name_ganre = data[1]
            count_musican = data[0]
            text.append(f' В жанре "{name_ganre}" коллическо исполнителей = {count_musican}')
        return print('\n'.join(text))

    def time_interval_collection_track(self, data: int, data1: int):
        sel = connection.execute(f""" select count(t.track_name)
        from track t 
        join album a on t.album_name = a.album_name
        where a.release_year between {data} and {data1} ;""").fetchall()

        return print(f'В Сборники {data}-{data1} вошли {sel[0][0]} треков')

    def albul_track_AVGduration(self):
        text = []
        sel = connection.execute("""select a.album_name , avg(t.duration)
        from album a        
        join track t on a.album_name = t.album_name
        group by a.album_name;""").fetchall()
        for data in sel:
            name_album = data[0]
            avg = data[1]
            text.append(f'{"%.2f" % avg} секунд средняя продолжительность треков в альбоме "{name_album}"  ')

        return print('\n'.join(text))

    def no_albums_released_year(self, data: int):
        text = []
        sel = connection.execute(f""" select distinct m.musician_name
        from musician m
        where m.musician_name NOT in (
          select m.musician_name
          from musician m 
          join album_musician am on m.id = am.musician_id 
          join album a on am.album = a.album_name 
          where a.release_year  in ({data}));""").fetchall()
        for data1 in sel:
            text.append(f'{data1[0]} НЕ выпускал альбом в {data} году   ')

        return print('\n'.join(text))

    def collection_name_specific_performer(self, data: str):
        sel = connection.execute(f"""select distinct ct.collection_name
        from  collection_track ct 
        join track t on ct.track_id = t.id 
        join album a on t.album_name = a.album_name
        join album_musician am  on a.album_name = am.album 
        join musician m on am.musician_id = m.id 
        where m.musician_name  like  '%%{data}%%' ;""").fetchall()
        return print(f'Названия сборников, в которых присутствует {data}: {sel}')

    def album_more_number_of_genres(self, data: int):
        sel = connection.execute(f"""select am.album 
            from album_musician am
            where am.musician_id in (
                select mg.musician_id 
                from musician_genre mg 
                GROUP by mg.musician_id 
                HAVING count(mg.music_genre ) >{data}  );
            """).fetchall()
        return print(f'Название альбомов, в которых присутствуют исполнители более {data} жанра:{sel}')

    def tracks_not_in_collection(self):
        sel = connection.execute(f"""select t.track_name 
        from collection_track ct 
        RIGHT JOIN track t on ct.track_id = t.id 
        where ct.collection_name is null;
                    """).fetchall()
        return print(f'Наименование треков, которые не входят в сборники:{sel}')

    def name_musician_min_duration(self):
        sel = connection.execute("""select distinct m.musician_name, t2.duration 
        from musician m 
        join album_musician am ON m.id =am.musician_id 
        join album a on am.album =a.album_name 
        join track t2 on a.album_name =t2.album_name 
        where t2.duration in (
            select min( t.duration) 
            from track t);""").fetchall()
        return print(f'Исполнителя(-ей), написавшего самый короткий по продолжительности трек: {sel}')

    def min_track_album(self):
        sel = connection.execute("""select album_name
        from (select t.album_name, count(t.track_name) 
        from track t 
        group by t.album_name
        ORDER BY count(t.track_name)) as map(album_name, count_track)
        where count_track in (select min(count_track2)
            from (select t.album_name, count(t.track_name) 
            from track t 
            group by t.album_name
            ORDER BY count(t.track_name)) as map(album_name,count_track2));""").fetchall()
        return print(f'название альбомов, содержащих наименьшее количество треков: {sel}')


if __name__ == '__main__':
    info_json = [{"musician": {"Михаил Круг": {"music_genre": ["русский шансон"],
                                               "album": {'Жиган-лимон': {
                                                   "track": [{"А сечку жрите сами": '120'}],
                                                   'release_year': '1994'},
                                                   'Мадам': {
                                                       "track": [{'Всё сбудется': '115',
                                                                  'Дороги': '119', 'давай поговорим': '110'}],
                                                       'release_year': '1998'}},
                                               "collection": {
                                                   'MP3 Коллекция': {'track': [{"А сечку жрите сами": '120',
                                                                                'Дороги': '119',
                                                                                'давай поговорим': '110'}],
                                                                     'release_year': '1994'}}},
                               "Nevermind": {"music_genre": ["альтернативный рок", "панк-рок"],
                                             "album": {
                                                 'Nevermind': {"track": [{"Breed": '183',
                                                                          'Polly': '176', 'Stain': '181'}],
                                                               'release_year': '1991'}},
                                             "collection": {'Incesticide': {"track": [{"Breed": '183', 'Stain': '181'}],
                                                                            'release_year': '1992'}}},

                               "Eminem": {"music_genre": ["хип-хоп", "хардкор-рэп", "рэп-рок"],
                                          "album": {'Relapse': {"track": [{"Insane": '181', 'Hello': '248'}],
                                                                'release_year': '2009'}},
                                          "collection": {
                                              'Eminem Presents': {"track": [{"Insane": '181'}],
                                                                  'release_year': '2006'},
                                              'На двоих': {
                                                  "track": [{'Hello': '248'}],
                                                  'release_year': '2023'}
                                          }},

                               "Григорий Лепс": {
                                   "music_genre": ['поп-рок', 'альтернативный рок', 'блюз-рок', 'эстрада'],
                                   "album": {'Лабиринт': {"track": [{"Лабиринт": '300',
                                                                     'Рок-н-ролл': '215', 'Снега': '244'}],
                                                          'release_year': '2019'}},
                                   "collection": {'Лучшие Песни (2022)': {
                                       "track": [{"Лабиринт": '300', 'Снега': '244'}],
                                       'release_year': '2022'},
                                       'На двоих': {
                                           "track": [{'Рок-н-ролл': '215'}],
                                           'release_year': '2023'}
                                   }},

                               "неологизмы 2021": {
                                   "music_genre": ["русский шансон", 'поп-рок', "хардкор-рэп", "авторская песня"],
                                   "album": {
                                       'Инфоцыгане': {
                                           "track": [{"Не в ресурсе": '125', 'На чиле, на расслабоне': '119'}],
                                           'release_year': '2018'},
                                       'Альбом 2020': {
                                           "track": [{"Ресурс": '125'}],
                                           'release_year': '2020'}},
                                   "collection": {'Лучшие Песни (2022)': {'track':
                                                                              [{"Не в ресурсе": '125',
                                                                                'На чиле, на расслабоне': '119',
                                                                                "Ресурс": '125'}],
                                                                          'release_year': '2022'}}}}}]

    engine = sqlalchemy.create_engine('postgresql://user1:1@localhost:5432/user1ecom')
    connection = engine.connect()
    music_library = BD_library(info_json)
    # music_library.DROP_TABLE()

    music_library.creature_table()
    music_library.BD_music_genre()
    music_library.musician()
    music_library.musician_genre()
    music_library.album()
    music_library.album_musician()
    music_library.collection()
    music_library.track()
    music_library.collection_track()
    print()
    print('ВНИМАНИЕ:данные в таблицах считаются не соответствующими действительности сведения! ')
    print()

    # music_library.search_album_year(2018)
    # print()
    # music_library.search_name_long_track()
    # print()
    # music_library.search_name_time_track(210)
    # print()
    # music_library.search_collection_time_period(2017, 2022)
    # print()
    # music_library.search_name_one_musician()
    # print()
    # music_library.search_track_name('Всё')

    music_library.count_genre_musician()
    print()
    music_library.time_interval_collection_track(1994, 2017)
    print()
    music_library.albul_track_AVGduration()
    print()
    music_library.no_albums_released_year(1991)
    print()
    music_library.collection_name_specific_performer('Григорий Лепс')
    print()
    music_library.album_more_number_of_genres(1)
    print()
    music_library.tracks_not_in_collection()
    print()
    music_library.name_musician_min_duration()
    print()
    music_library.min_track_album()
