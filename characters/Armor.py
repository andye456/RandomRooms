# The shields can be used to deflect an attack which will cause no hit points to be lost
# Shields don't work against magic
small_shield = {"experience": 1, "uses_per_fight": 1}
medium_shield = {"experience": 5, "uses_per_fight": 2}
medium_shield = {"experience": 7, "uses_per_fight": 3}

# Armour determines the success of an opponents strike
# e.g. AC (armor class) 100 means that the attack will be 100% successful
none = {"AC": 100, "experience": 0}
shield_only = {"AC": 90}
leather_armor = {"AC": 80}
chain_mail = {"AC": 70}
scale_mail = {"AC": 60}
chain_mail_shield = {"AC": 50}
banded_mail = {"AC": 40}
plate_mail = {"AC": 30}
plate_mail_shield = {"AC": 20}
