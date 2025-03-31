from sqlalchemy.orm import Session
from main import SessionLocal, Warframe, Ability, Weapon, Mod

def seed_database():
    db = SessionLocal()
    
    # Clear existing data
    db.query(Warframe).delete()
    db.query(Ability).delete()
    db.query(Weapon).delete()
    db.query(Mod).delete()
    
    # Create sample warframes
    excalibur = Warframe(
        name="Excalibur",
        health=100,
        shield=100,
        armor=225,
        energy=100,
        description="Excalibur is a master of blade and gun."
    )
    
    volt = Warframe(
        name="Volt",
        health=100,
        shield=150,
        armor=100,
        energy=100,
        description="Volt can create and harness electrical elements."
    )
    
    rhino = Warframe(
        name="Rhino",
        health=150,
        shield=150,
        armor=275,
        energy=100,
        description="Rhino is a heavily armored Warframe with tremendous strength."
    )
    
    # Create sample abilities
    slash_dash = Ability(
        name="Slash Dash",
        description="Excalibur dashes between enemies while slashing with the Exalted Blade.",
        energy_cost=25
    )
    
    radial_blind = Ability(
        name="Radial Blind",
        description="Excalibur emits a bright flash of light, blinding all enemies in range.",
        energy_cost=50
    )
    
    shock = Ability(
        name="Shock",
        description="Volt emits a shocking bolt of electricity.",
        energy_cost=25
    )
    
    speed = Ability(
        name="Speed",
        description="Volt charges himself and nearby allies with electrical speed.",
        energy_cost=50
    )
    
    rhino_charge = Ability(
        name="Rhino Charge",
        description="Rhino charges forward, damaging enemies in his path.",
        energy_cost=25
    )
    
    iron_skin = Ability(
        name="Iron Skin",
        description="Rhino reinforces his armor, creating a protective metal coating.",
        energy_cost=50
    )
    
    # Create sample weapons
    braton = Weapon(
        name="Braton",
        type="Primary",
        damage=20.0,
        critical_chance=0.12,
        critical_multiplier=1.6,
        status_chance=0.06,
        description="The Braton is a balanced assault rifle."
    )
    
    lex = Weapon(
        name="Lex",
        type="Secondary",
        damage=130.0,
        critical_chance=0.20,
        critical_multiplier=2.0,
        status_chance=0.10,
        description="The Lex is a high-powered pistol."
    )
    
    skana = Weapon(
        name="Skana",
        type="Melee",
        damage=35.0,
        critical_chance=0.10,
        critical_multiplier=1.5,
        status_chance=0.10,
        description="The Skana is a balanced sword."
    )
    
    # Create sample mods
    serration = Mod(
        name="Serration",
        type="Rifle",
        rarity="Common",
        drain=7,
        description="Increases rifle damage.",
        effect="Damage +15%"
    )
    
    vitality = Mod(
        name="Vitality",
        type="Warframe",
        rarity="Common",
        drain=8,
        description="Increases Warframe health.",
        effect="Health +20%"
    )
    
    pressure_point = Mod(
        name="Pressure Point",
        type="Melee",
        rarity="Common",
        drain=6,
        description="Increases melee damage.",
        effect="Damage +20%"
    )
    
    # Add abilities to warframes
    excalibur.abilities.append(slash_dash)
    excalibur.abilities.append(radial_blind)
    volt.abilities.append(shock)
    volt.abilities.append(speed)
    rhino.abilities.append(rhino_charge)
    rhino.abilities.append(iron_skin)
    
    # Add to database
    db.add_all([
        excalibur, volt, rhino,
        slash_dash, radial_blind, shock, speed, rhino_charge, iron_skin,
        braton, lex, skana,
        serration, vitality, pressure_point
    ])
    
    db.commit()
    db.close()
    
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()

