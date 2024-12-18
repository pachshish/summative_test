from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.config.init_db import Base

class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    terror_attacks = relationship('TerrorAttack', back_populates='location')


class TerrorAttack(Base):
    __tablename__ = 'terror_attack'

    id = Column(Integer(), primary_key=True)
    year = Column(Integer(), nullable=False)
    month = Column(Integer(), nullable=False)
    day = Column(Integer(), nullable=False)
    country_id = Column(Integer(), ForeignKey('countries.id'), nullable=False)
    region_id = Column(Integer(), nullable=False)
    provstate = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)

    attack_type_id = Column(Integer(), ForeignKey('attack_types.id'), nullable=False)
    target_type_id = Column(Integer(), ForeignKey('target_types.id'), nullable=False)
    target_specific_type_id = Column(Integer(), ForeignKey('target_specific_types.id'), nullable=False)
    group_name = Column(String(255), nullable=False)
    num_of_terrorists = Column(Integer())
    num_of_dead = Column(Integer())
    num_of_casualties = Column(Integer())

    # Relationships
    country = relationship('Country', back_populates='terror_attacks')
    attack_type = relationship('Attack', back_populates='terror_attacks')
    target_type = relationship('Target', back_populates='terror_attacks')
    target_specific_type = relationship('TargetSpecific', back_populates='terror_attacks')
    region = relationship('Region', back_populates='terror_attacks')
    location = relationship('Location', back_populates='terror_attacks')


class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer(), primary_key=True)
    country_id = Column(Integer(), unique=True, nullable=False)
    country_name = Column(String(255), nullable=False)

    # Back reference
    terror_attacks = relationship('TerrorAttack', back_populates='country')

class Region(Base):
    __tablename__ = 'regions'
    id = Column(Integer(), primary_key=True)
    region_id = Column(Integer(), unique=True, nullable=False)
    region_name = Column(String(255), nullable=False)

    # Back reference
    terror_attacks = relationship('TerrorAttack', back_populates='country')


class Attack(Base):
    __tablename__ = 'attack_types'
    id = Column(Integer(), primary_key=True)
    attack_type_id = Column(Integer(), unique=True, nullable=False)
    attack_type_name = Column(String(255), nullable=False)

    # Back reference
    terror_attacks = relationship('TerrorAttack', back_populates='attack_type')


class Target(Base):
    __tablename__ = 'target_types'
    id = Column(Integer(), primary_key=True)
    target_type_id = Column(Integer(), unique=True, nullable=False)
    target_type_name = Column(String(255), nullable=False)

    # Back reference
    terror_attacks = relationship('TerrorAttack', back_populates='target_type')


class TargetSpecific(Base):
    __tablename__ = 'target_specific_types'
    id = Column(Integer(), primary_key=True)
    target_type_specific_id = Column(Integer(), unique=True, nullable=False)
    target_type_specific_name = Column(String(255), nullable=False)

    # Back reference
    terror_attacks = relationship('TerrorAttack', back_populates='target_specific_type')
