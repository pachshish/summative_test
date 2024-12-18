import csv
from sqlalchemy.orm import Session

from db.models.csv1_model import Country, TerrorAttack, Region, Attack, TargetSpecific, Target, Location

#
# def load_countries_from_csv(session: Session, csv_file: str):
#     with open(csv_file, 'r', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             country = Country(
#                 country_id=int(row['country']),
#                 country_name=row['country_txt']
#             )
#             session.add(country)
#         session.commit()
#
# def load_region_from_csv(session: Session, csv_file: str):
#     with open(csv_file, 'r', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             region = Region(
#                 region_id=int(row['region']),
#                 region_name=row['region_txt']
#             )
#             session.add(region)
#         session.commit()
#
# def load_attack_from_csv(session: Session, csv_file: str):
#     with open(csv_file, 'r', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             attack = Attack(
#                 attack_type_id=int(row['attacktype1']),
#                 attack_type_name=row['attacktype1_txt']
#             )
#             session.add(attack)
#         session.commit()
#
# def load_target_from_csv(session: Session, csv_file: str):
#     with open(csv_file, 'r', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             target = Target(
#                 target_type_id=int(row['targtype1']),
#                 target_type_name=row['targtype1_txt']
#             )
#             session.add(target)
#         session.commit()
#
# def load_target_specific_from_csv(session: Session, csv_file: str):
#     with open(csv_file, 'r', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             target_specific = TargetSpecific(
#                 target_type_specific_id=int(row['targsubtype1']),
#                 target_type_specific_name=row['targsubtype1_txt']
#             )
#             session.add(target_specific)
#         session.commit()
#
# def load_terror_attacks_from_csv(session: Session, csv_file: str):
#     with open(csv_file, 'r', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             location = session.query(Location).filter_by(
#                 latitude=float(row['latitude']),
#                 longitude=float(row['longitude'])
#             ).first()
#
#             if not location:
#                 location = Location(
#                     latitude=float(row['latitude']),
#                     longitude=float(row['longitude'])
#                 )
#                 session.add(location)
#                 session.flush()
#
#             attack = TerrorAttack(
#                 id=int(row['eventid']),
#                 year=int(row['iyear']),
#                 month=int(row['imonth']),
#                 day=int(row['iday']),
#                 country_id=int(row['country']),
#                 region_id=int(row['region']),
#                 provstate=row['provstate'],
#                 city=row['city'],
#                 location_id=location.id,
#                 attack_type_id=int(row['attacktype1']),
#                 target_type_id=int(row['targtype1']),
#                 target_specific_type_id=int(row['targsubtype1']),
#                 group_name=row['gname'],
#                 num_of_terrorists=int(row['nperps']),
#                 num_of_dead=int(row['nkill'])
#             )
#             session.add(attack)
#         session.commit()


# if __name__ == '__main__':
#     database_uri = "sqlite:///terror_attacks.db"  # לדוגמה
#     session = create_session(database_uri)
#
#     load_countries_from_csv(session, 'countries.csv')
#     load_terror_attacks_from_csv(session, 'terror_attacks.csv')
#
#     session.close()

import csv
from sqlalchemy.orm import Session
from db.models.csv1_model import Country, TerrorAttack, Region, Attack, TargetSpecific, Target, Location

def load_countries_from_csv(session: Session, csv_file: str):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                country = Country(
                    country_id=int(row.get('country', 0)),
                    country_name=row.get('country_txt', 'Unknown')
                )
                session.add(country)
            except Exception as e:
                print(f"Error loading country: {e}")
        session.commit()

def load_region_from_csv(session: Session, csv_file: str):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                region = Region(
                    region_id=int(row.get('region', 0)),
                    region_name=row.get('region_txt', 'Unknown')
                )
                session.add(region)
            except Exception as e:
                print(f"Error loading region: {e}")
        session.commit()

def load_attack_from_csv(session: Session, csv_file: str):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                attack = Attack(
                    attack_type_id=int(row.get('attacktype1', 0)),
                    attack_type_name=row.get('attacktype1_txt', 'Unknown')
                )
                session.add(attack)
            except Exception as e:
                print(f"Error loading attack: {e}")
        session.commit()

def load_target_from_csv(session: Session, csv_file: str):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                target = Target(
                    target_type_id=int(row.get('targtype1', 0)),
                    target_type_name=row.get('targtype1_txt', 'Unknown')
                )
                session.add(target)
            except Exception as e:
                print(f"Error loading target: {e}")
        session.commit()

def load_target_specific_from_csv(session: Session, csv_file: str):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                target_specific = TargetSpecific(
                    target_type_specific_id=int(row.get('targsubtype1', 0)),
                    target_type_specific_name=row.get('targsubtype1_txt', 'Unknown')
                )
                session.add(target_specific)
            except Exception as e:
                print(f"Error loading target specific: {e}")
        session.commit()

def load_terror_attacks_from_csv(session: Session, csv_file: str):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                location = session.query(Location).filter_by(
                    latitude=float(row.get('latitude', 0.0)),
                    longitude=float(row.get('longitude', 0.0))
                ).first()

                if not location:
                    location = Location(
                        latitude=float(row.get('latitude', 0.0)),
                        longitude=float(row.get('longitude', 0.0))
                    )
                    session.add(location)
                    session.flush()

                attack = TerrorAttack(
                    id=int(row.get('eventid', 0)),
                    year=int(row.get('iyear', 0)),
                    month=int(row.get('imonth', 0)),
                    day=int(row.get('iday', 0)),
                    country_id=int(row.get('country', 0)),
                    region_id=int(row.get('region', 0)),
                    provstate=row.get('provstate', 'Unknown'),
                    city=row.get('city', 'Unknown'),
                    location_id=location.id,
                    attack_type_id=int(row.get('attacktype1', 0)),
                    target_type_id=int(row.get('targtype1', 0)),
                    target_specific_type_id=int(row.get('targsubtype1', 0)),
                    group_name=row.get('gname', 'Unknown'),
                    num_of_terrorists=int(row.get('nperps', 0)),
                    num_of_dead=int(row.get('nkill', 0)),
                    num_of_casualties=int(row.get('nwound', 0))
                )
                session.add(attack)
            except Exception as e:
                print(f"Error loading terror attack: {e}")
        session.commit()
