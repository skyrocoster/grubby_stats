from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import time

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///grubby.db"
db = SQLAlchemy(app)
app_context = app.app_context()
app_context.push()
app.secret_key = "1234567A"


class PlayerMatches(db.Model):

    __tablename__ = "player_matches"

    player_id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, primary_key=True)
    player_slot = db.Column(db.Integer)
    radiant_win = db.Column(db.Boolean)
    duration = db.Column(db.Integer)
    game_mode = db.Column(db.Integer)
    lobby_type = db.Column(db.Integer)
    hero_id = db.Column(db.Integer)
    start_time = db.Column(db.Integer)
    version = db.Column(db.Integer)
    kills = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    skill = db.Column(db.String(10))
    average_rank = db.Column(db.Integer)
    leaver_status = db.Column(db.Integer)
    party_size = db.Column(db.Integer)
    start_time_normal = db.Column(db.DateTime)
    session_id = db.Column(db.Integer)
    session_counter = db.Column(db.Integer)
    team = db.Column(db.String(7))
    win = db.Column(db.Boolean)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Heroes(db.Model):

    __tablename__ = "heroes"

    hero_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    localized_name = db.Column(db.String(50))
    primary_attr = db.Column(db.String(3))
    attack_type = db.Column(db.String(10))
    img = db.Column(db.String(500))
    icon = db.Column(db.String(500))
    base_health = db.Column(db.Integer)
    base_health_regen = db.Column(db.Integer)
    base_mana = db.Column(db.Integer)
    base_mana_regen = db.Column(db.Integer)
    base_armor = db.Column(db.Integer)
    base_mr = db.Column(db.Integer)
    base_attack_min = db.Column(db.Integer)
    base_attack_max = db.Column(db.Integer)
    base_str = db.Column(db.Integer)
    base_agi = db.Column(db.Integer)
    base_int = db.Column(db.Integer)
    str_gain = db.Column(db.Float)
    agi_gain = db.Column(db.Float)
    int_gain = db.Column(db.Float)
    attack_range = db.Column(db.Integer)
    projectile_speed = db.Column(db.Integer)
    attack_rate = db.Column(db.Float)
    base_attack_time = db.Column(db.Integer)
    attack_point = db.Column(db.Integer)
    move_speed = db.Column(db.Integer)
    turn_rate = db.Column(db.Float)
    cm_enabled = db.Column(db.Float)
    legs = db.Column(db.Integer)
    day_vision = db.Column(db.Integer)
    night_vision = db.Column(db.Integer)
    initiator = db.Column(db.Boolean, default=0)
    durable = db.Column(db.Boolean, default=0)
    disabler = db.Column(db.Boolean, default=0)
    carry = db.Column(db.Boolean, default=0)
    support = db.Column(db.Boolean, default=0)
    escape = db.Column(db.Boolean, default=0)
    nuker = db.Column(db.Boolean, default=0)
    pusher = db.Column(db.Boolean, default=0)
    jungler = db.Column(db.Boolean, default=0)


class GameModes(db.Model):

    __tablename__ = "game_modes"

    mode_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    localised_name = db.Column(db.String(100))
    balanced = db.Column(db.Boolean, default=0)


class MatchDetails(db.Model):

    __tablename__ = "match_details"

    match_id = db.Column(db.Integer, primary_key=True)
    barracks_status_dire = db.Column(db.Integer)
    barracks_status_radiant = db.Column(db.Integer)
    dire_score = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    first_blood_time = db.Column(db.Integer)
    game_mode = db.Column(db.Integer)
    lobby_type = db.Column(db.Integer)
    negative_votes = db.Column(db.Integer)
    radiant_score = db.Column(db.Integer)
    radiant_win = db.Column(db.Boolean)
    start_time = db.Column(db.Integer)
    patch = db.Column(db.Integer)
    region = db.Column(db.Integer)


class MatchPlayers(db.Model):

    __tablename__ = "match_players"

    match_player_id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer)
    hero_id = db.Column(db.Integer)
    player_id = db.Column(db.Integer)
    player_slot = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    denies = db.Column(db.Integer)
    firstblood_claimed = db.Column(db.Integer)
    gold_per_min = db.Column(db.Integer)
    hero_id = db.Column(db.Integer)
    kills = db.Column(db.Integer)
    last_hits = db.Column(db.Integer)
    level = db.Column(db.Integer)
    net_worth = db.Column(db.Integer)
    xp_per_min = db.Column(db.Integer)
    radiant_win = db.Column(db.Integer)
    start_time = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    lobby_type = db.Column(db.Integer)
    game_mode = db.Column(db.Integer)
    patch = db.Column(db.Integer)
    region = db.Column(db.Integer)
    isRadiant = db.Column(db.Integer)
    personaname = db.Column(db.Integer)
    win = db.Column(db.Boolean)
    team = db.Column(db.String(10))
    lane_role = db.Column(db.Integer)
    lane = db.Column(db.Integer)


class PickBans(db.Model):
    __tablename__ = "pick_bans"

    pick_id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer)
    is_pick = db.Column(db.Boolean)
    hero_id = db.Column(db.Integer)
    team = db.Column(db.String(10))
    order = db.Column(db.Integer)


class NetworthTimings(db.Model):
    __tablename__ = "networth_timings"

    networth_timing_id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer)
    player_id = db.Column(db.Integer)
    minute = db.Column(db.Integer)
    gold = db.Column(db.Integer)
    last_hits = db.Column(db.Integer)


if __name__ == "__main__":
    db.create_all()
