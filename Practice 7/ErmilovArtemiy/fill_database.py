import argparse
from argparse import ArgumentParser
from datetime import timedelta
from typing import List

import psycopg2
from faker import Faker

# Taken from pastebin given: https://pastebin.com/dEqPSAk3
CREATE_DATABASE_STR = """
    create table Countries (
        name char(40),
        country_id char(3) unique,
        area_sqkm integer,
        population integer
    );
     
    create table Olympics (
        olympic_id char(7) unique,
        country_id char(3),
        city char(50),
        year integer,
        startdate date,
        enddate date,
        foreign key (country_id) references Countries(country_id)
    );
     
    create table Players (
        name char(40),
        player_id char(10) unique,
        country_id char(3),
        birthdate date,
        foreign key (country_id) references Countries(country_id)
    );
     
    create table Events (
        event_id char(7) unique,
        name char(40),
        eventtype char(20),
        olympic_id char(7),
        is_team_event integer check (is_team_event in (0, 1)),
        num_players_in_team integer,
        result_noted_in char(100),
        foreign key (olympic_id) references Olympics(olympic_id)
    );
     
    create table Results (
        event_id char(7),
        player_id char(10),
        medal char(7),
        result float,
        foreign key (event_id) references Events(event_id),
        foreign key (player_id) references players(player_id)
    );
"""


def choose_random_option(list: List):
    return fake.random_choices(list, length=1)[0]


def get_db_faker_parser() -> argparse.ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("url", help="Used database URL.")
    parser.add_argument("--seed", help="Random seed for reproducibility.", type=int)
    parser.add_argument("--country_count", help="Number of countries to be generated.", type=int, required=True)
    parser.add_argument("--player_count", help="Number of players to be generated.", type=int, required=True)
    parser.add_argument("--olympics_count", help="Number of olympics to be generated.", type=int, required=True)
    parser.add_argument("--event_count", help="Number of events to be generated.", type=int, required=True)

    return parser


def generate_countries(country_count: int, fake, cursor) -> List[int]:
    country_ids = []
    for _ in range(country_count):
        id = fake.unique.country_code('alpha-3')
        name = fake.country()
        while len(name) > 40:
            name = fake.country()
        area_sqkm = fake.random_int(1, 18_000_000)
        population = fake.random_int(1, 1_500_000_000)

        cursor.execute("INSERT INTO Countries VALUES(%s, %s, %s, %s);",
                       (name, id, area_sqkm, population))
        country_ids.append(id)

    return country_ids


def generate_players(player_count: int, country_ids: List[int], fake, cursor) -> List[int]:
    player_ids = []
    for _ in range(player_count):
        name = fake.name()
        birthdate = fake.date_object()
        country = fake.random_choices(country_ids, length=1)[0]

        names = [e for e in name.split(' ') if e.isalpha()]
        id = fake.unique.numerify(names[-1][:5] + names[0][:3] + '##').upper()

        cursor.execute("INSERT INTO Players VALUES(%s, %s, %s, %s);",
                       (name, id, country, birthdate))
        player_ids.append(id)


def generate_olympics(olympics_count: int, country_ids: List[int], fake, cursor) -> List[int]:
    olympics_ids = []
    for _ in range(olympics_count):
        country = fake.random_choices(country_ids, length=1)[0]
        city = fake.city()
        year = fake.unique.random_int(1900, 2020, 4)
        olympics_id = city[:3].upper() + str(year)

        startdate = fake.date_object().replace(year=year)
        enddate = startdate + timedelta(days=14)

        cursor.execute("INSERT INTO Olympics VALUES(%s, %s, %s, %s, %s, %s);",
                       (olympics_id, country, city, year, startdate, enddate))
        olympics_ids.append(olympics_id)

    return olympics_ids


def generate_events(events_count: int, olympics_ids: List[int], fake, cursor) -> List[str]:
    event_ids = []
    for i in range(events_count):
        event_id = 'ID_' + str(i)
        event_type = choose_random_option(['TYPE1', 'TYPE2'])
        olympics = choose_random_option(olympics_ids)
        result_noted_in = choose_random_option(['m', 's'])
        name = choose_random_option([f"NAME{ii}" for ii in range(100)])

        cursor.execute("INSERT INTO Events VALUES(%s, %s, %s, %s, 0, 0, %s);",
                       (event_id, name, event_type, olympics, result_noted_in))
        event_ids.append(event_id)

    return event_ids


def generate_results(event_ids: List[str], player_ids: List[int], fake, cursor) -> None:
    for event_id in event_ids:
        scores = sorted([fake.pyfloat(positive=True, max_value=100) for _ in range(3)])

        for score, medal in zip(scores, ["GOLD", "SILVER", "BRONZE"]):
            player = choose_random_option(player_ids)
            cursor.execute("INSERT INTO Results VALUES(%s, %s, %s, %s);", (event_id, player, medal, score))


if __name__ == "__main__":
    parser = get_db_faker_parser()
    args = parser.parse_args()

    seed = args.seed
    player_count = args.player_count
    country_count = args.country_count
    olympics_count = args.olympics_count
    event_count = args.event_count

    if seed is not None:
        Faker.seed(seed)
    fake = Faker()

    conn = psycopg2.connect(args.url)
    cursor = conn.cursor()
    cursor.execute(CREATE_DATABASE_STR)

    country_ids = generate_countries(country_count, fake, cursor)

    player_ids = generate_players(player_count, country_ids, fake, cursor)

    olympics_ids = generate_olympics(olympics_count, country_ids, fake, cursor)

    event_ids = generate_events(event_count, olympics_ids, fake, cursor)

    generate_results(event_ids, player_ids, fake, cursor)

    conn.commit()
    cursor.close()
    conn.close()
