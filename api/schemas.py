from typing import List
from models import WarframeBase, AbilityBase, WeaponBase, ModBase


class ModResponse(ModBase):
    id: int

    class Config:
        orm_mode = True


class WeaponResponse(WeaponBase):
    id: int

    class Config:
        orm_mode = True


class AbilityResponse(AbilityBase):
    id: int

    class Config:
        orm_mode = True


class WarframeResponse(WarframeBase):
    id: int
    abilities: List[AbilityResponse] = []

    class Config:
        orm_mode = True
