import datetime
from project import db


#<==================================================================================================>
#                                    GAME COLLECTION
#<==================================================================================================>
class Game(db.Document):
    winner = db.StringField()
    game_id = db.StringField()
    rows = db.IntField(default=4)
    columns = db.IntField(default=4)
    board = db.ListField(db.ListField())
    moves = db.ListField(db.DictField())
    move_number = db.IntField(default=0)
    players = db.ListField(db.StringField())
    state = db.StringField(default="IN_PROGRESS")
    game_in_progress = db.BooleanField(default=True)
    current_player_turn = db.StringField(default="player1")
    created = db.DateTimeField(default=datetime.datetime.now)

    meta = dict(indexes=["game_id"])
