import csv

from db.config.sql_config import create_session
from db.config.sql_ditails import database_uri
from db.models.csv1_model import Country, TerrorAttack, Region, Attack, TargetSpecific, Target, Location
from services.read_csv_service import  safe_date, safe_lat_end_lan, process_terrorists


def load_countries_from_csv(session, csv_file: str):
    with open(csv_file, 'r', errors='ignore') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                country = session.query(Country).filter_by(
                    country_id=int(row.get('country') or 0),
                ).first()
                if not country:
                    country = Country(
                        country_id=int(row.get('country') or 0),
                        country_name=row.get('country_txt', 'Unknown')
                    )
                    session.add(country)
                    session.commit()
            except Exception as e:
                session.rollback()
                print(f"Error loading country: {e}")
        # session.commit()

def load_region_from_csv(session, csv_file: str):
    with open(csv_file, 'r', errors='ignore') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                region = session.query(Region).filter_by(
                    region_id=int(row.get('region') or 0),
                ).first()
                if not region:
                    region = Region(
                        region_id=int(row.get('region') or 0),
                        region_name=row.get('region_txt', 'Unknown')
                    )
                    session.add(region)
                    session.commit()
            except Exception as e:
                session.rollback()
                print(f"Error loading region: {e}")

def load_attack_from_csv(session, csv_file: str):
    with open(csv_file, 'r', errors='ignore') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                attack = session.query(Attack).filter_by(
                    attack_type_id=int(row.get('attacktype1') or 0),
                ).first()

                if not attack:
                    attack = Attack(
                    attack_type_id=int(row.get('attacktype1') or 0),
                    attack_type_name=row.get('attacktype1_txt', 'Unknown')
                )
                session.add(attack)
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Error loading attack: {e}")

def load_target_from_csv(session, csv_file: str):
    with open(csv_file, 'r', errors='ignore') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                target = session.query(Target).filter_by(
                    target_type_id=int(row.get('targtype1') or 0)
                ).first()

                if not target:
                    target = Target(
                    target_type_id=int(row.get('targtype1') or 0),
                    target_type_name=row.get('targtype1_txt', 'Unknown')
                )
                    session.add(target)
                    session.commit()
            except Exception as e:
                session.rollback()
                print(f"Error loading target: {e}")

def load_target_specific_from_csv(session, csv_file: str):
    with open(csv_file, 'r', errors='ignore') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                target_specific = session.query(TargetSpecific).filter_by(
                    target_type_specific_id=int(row.get('targsubtype1') or 0)
                ).first()

                if not target_specific:
                    target_specific = TargetSpecific(
                        target_type_specific_id=int(row.get('targsubtype1') or 0),
                    target_type_specific_name=row.get('targsubtype1_txt', 'Unknown')
                    )
                    session.add(target_specific)
                    session.commit()
            except Exception as e:
                session.rollback()
                print(f"Error loading target specific: {e}")


def load_terror_attacks_from_csv(session, csv_file: str):
    with open(csv_file, 'r', errors='ignore') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                year = int(row.get('iyear') or 1970)
                month = int(row.get('imonth') or 1)
                day = int(row.get('iday') or 1)
                date_value = safe_date(year, month, day)

                latitude = safe_lat_end_lan(row.get('latitude'))
                longitude = safe_lat_end_lan(row.get('longitude'))

                location = session.query(Location).filter_by(
                    latitude=latitude, longitude=longitude
                ).first()

                if not location:
                    location = Location(
                        latitude=latitude, longitude=longitude
                    )
                    session.add(location)
                    session.flush()

                attack = TerrorAttack(
                    # id=row.get('eventid'),
                    date=date_value,
                    country_id=int(row.get('country') or -1),
                    region_id=int(row.get('region') or -1),
                    provstate=row.get('provstate', 'Unknown'),
                    city=row.get('city', 'Unknown'),
                    location_id=location.id,
                    attack_type_id=int(row.get('attacktype1') or -1),
                    target_type_id=int(row.get('targtype1') or -1),
                    target_specific_type_id=int(row.get('targsubtype1') or 0),
                    group_name=row.get('gname', 'Unknown'),
                    num_of_terrorists = process_terrorists(row.get('nperps')),
                    num_of_dead=int(row.get('nkill') or 0),
                    num_of_casualties=int(row.get('nwound') or 0)
                )
                session.add(attack)
                session.commit()

            except Exception as e:
                session.rollback()
                print(f"Unexpected error: {e}")



def add_csv1_to_db():
    db_uri = database_uri
    session = create_session(db_uri)
    csv_path = 'csv_data1/data1_big.csv'

    load_countries_from_csv(session, csv_path)
    load_region_from_csv(session, csv_path)
    load_attack_from_csv(session, csv_path)
    load_target_from_csv(session, csv_path)
    load_target_specific_from_csv(session, csv_path)
    load_terror_attacks_from_csv(session, csv_path)

    session.close()

