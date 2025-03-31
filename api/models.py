from typing import List
from pydantic import BaseModel
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Define association tables for many-to-many relationships
warframe_ability = Table(
    "warframe_ability",
    Base.metadata,
    Column("warframe_id", Integer, ForeignKey("warframes.id")),
    Column("ability_id", Integer, ForeignKey("abilities.id")),
)


# Database Models
class Warframe(Base):
    __tablename__ = "warframes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    health = Column(Integer)
    shield = Column(Integer)
    armor = Column(Integer)
    energy = Column(Integer)
    description = Column(String)

    abilities = relationship(
        "Ability", secondary=warframe_ability, back_populates="warframes"
    )


class Ability(Base):
    __tablename__ = "abilities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    energy_cost = Column(Integer)

    warframes = relationship(
        "Warframe", secondary=warframe_ability, back_populates="abilities"
    )


class Weapon(Base):
    __tablename__ = "weapons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(String)  # Primary, Secondary, Melee
    damage = Column(Float)
    critical_chance = Column(Float)
    critical_multiplier = Column(Float)
    status_chance = Column(Float)
    description = Column(String)


class Mod(Base):
    __tablename__ = "mods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(String)  # Warframe, Weapon, Companion, etc.
    rarity = Column(String)  # Common, Uncommon, Rare, Legendary
    drain = Column(Integer)
    description = Column(String)
    effect = Column(String)


# Pydantic models for request/response
class AbilityBase(BaseModel):
    name: str
    description: str
    energy_cost: int


class AbilityCreate(AbilityBase):
    pass

class WarframeBase(BaseModel):
    name: str
    health: int
    shield: int
    armor: int
    energy: int
    description: str


class WarframeCreate(WarframeBase):
    pass


class WeaponBase(BaseModel):
    name: str
    type: str
    damage: float
    critical_chance: float
    critical_multiplier: float
    status_chance: float
    description: str


class WeaponCreate(WeaponBase):
    pass




class ModBase(BaseModel):
    name: str
    type: str
    rarity: str
    drain: int
    description: str
    effect: str


class ModCreate(ModBase):
    pass