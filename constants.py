# Constants
constants = [
    "game_mode.json",
    "item_colors.json",
    "lobby_type.json",
    "order_types.json",
    "patch.json",
    "permanent_buffs.json",
    "player_colors.json",
    "skillshots.json",
    "xp_level.json",
]

for constant in constants:
    ref = requests.get(f"{dota_constants}/{constant}").json()
    with open(f"{raw_data}/{constant}", "w", encoding="utf-8") as f:
        json.dump(ref, f, ensure_ascii=False, indent=4)

constants_build = [
    "abilities.json",
    "ability_ids.json",
    "aghs_desc.json",
    "ancients.json",
    "chat_wheel.json",
    "cluster.json",
    "countries.json",
    "game_mode.json",
    "hero_abilities.json",
    "hero_lore.json",
    "hero_names.json",
    "heroes.json",
    "item_colors.json",
    "item_ids.json",
    "items.json",
    "lobby_type.json",
    "neutral_abilities.json",
    "order_types.json",
    "patch.json",
    "patchnotes.json",
    "permanent_buffs.json",
    "player_colors.json",
    "region.json",
    "skillshots.json",
    "xp_level.json",
]

for constant in constants_build:
    ref = requests.get(f"{dota_constants_build}/{constant}").json()
    with open(f"{raw_data}/{constant}", "w", encoding="utf-8") as f:
        json.dump(ref, f, ensure_ascii=False, indent=4)
