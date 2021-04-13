#<==================================================================================================>
#                                          IMPORTS
#<==================================================================================================>
import uuid
from project.apis.models import Game
from flask import request, Blueprint, jsonify
from project.apis.serializer import GameIdSchema, GameStateSchema, GameMovesSchema
from project.apis.schema_validator import validate_game_schema, validate_move_schema
from project.game.logic import get_board, is_valid, get_current_null_position, set_value, winning_move

#<==================================================================================================>
#                                          BLUEPRINTS
#<==================================================================================================>
api_blueprint = Blueprint('apis', __name__, url_prefix="/api/v1/")


#<==================================================================================================>
#                                CREATE A NEW GAME & GET ALL DETAILS
#<==================================================================================================>
@api_blueprint.route("/", methods=["GET", "POST"])
def create_a_game():
    if request.method == "GET":
        all_games_obj = Game.objects.filter(game_in_progress=True).fields(game_id=1)
        ma_schema = GameIdSchema()
        serialised_data = ma_schema.dump(all_games_obj, many=True)
        data = [game.get("game_id") for game in serialised_data]
        return jsonify({
            "result": True,
            "data": data
        }), 200

    elif request.method == "POST":
        inp_data = request.get_json()
        validated_resp = validate_game_schema(inp_data)

        if validated_resp.get("result"):
            game_id = str(uuid.uuid4())
            data = validated_resp.get("data")
            row = data.get("rows")
            col = data.get("columns")
            data_obj = {
                "rows": row,
                "columns": col,
                "game_id": game_id,
                "board": get_board(row, col),
                "players": data.get("players")
            }
            new_game = Game(**data_obj)
            new_game.save()
            return jsonify({
                "result": True,
                "message": "Game Created",
                "gameId": game_id
            }), 200
        else:
            return jsonify({
                    "result": False,
                    "message": validated_resp.get("error").replace("'", "")
            }), 400


#<==================================================================================================>
#                                    GET STATE OF THE GAME
#<==================================================================================================>
@api_blueprint.route("/<token>", methods=["GET"])
def get_state_of_game(token):
    is_token_valid = validate_token(token)
    if is_token_valid:
        game_info = Game.objects.filter(game_id=token).fields(game_id=1, state=1, players=1, winner=1).first()
        if not game_info:
            return jsonify({
                "result": False,
                "message": "game not found"
            }), 404
        else:
            ma_schema = GameStateSchema()
            data = ma_schema.dump(game_info)
            if not data.get("winner"):
                data.pop("winner")

            return jsonify({
                "result": True,
                "data": data
            }), 200
    else:
        return jsonify({
            "result": False,
            "message": "malformed request"
        }), 400


# #<==================================================================================================>
# #                                 LIST OF MOVES PLAYED
# #<==================================================================================================>
@api_blueprint.route("/<game_id>/moves", methods=["GET"])
def get_list_of_palyer_moves(game_id):
    is_token_valid = validate_token(game_id)
    if is_token_valid:
        game_info = Game.objects.filter(game_id=game_id).fields(moves=1).first()
        if not game_info:
            return jsonify({
                "result": False,
                "message": "game not found"
            }), 404
        else:
            ma_schema = GameMovesSchema()
            data = ma_schema.dump(game_info)

            try:
                start = int(request.args.get('start'))
                until = int(request.args.get('until'))
                if start < until:
                    if until < len(data.get("moves")):
                        data = data.get("moves")[start:until]
            except:
                pass

            return jsonify({
                "result": True,
                "data": data
            }), 200
    else:
        return jsonify({
            "result": False,
            "message": "malformed request"
        }), 400


#<==================================================================================================>
#                                    POST A MOVE AND DELETE
#<==================================================================================================>
@api_blueprint.route("/<game_id>/<player_id>", methods=["POST", "DELETE"])
def post_a_move(game_id, player_id):
    if request.method == "POST":
        inp_data = request.get_json()
        validated_resp = validate_move_schema(inp_data)
        is_token_valid = validate_token(game_id)
        if is_token_valid and validated_resp.get("result"):
            game_info = Game.objects.filter(game_id=game_id).first()
            if not game_info:
                return jsonify({
                    "result": False,
                    "message": "game not found"
                }), 404
            elif game_info.state == "DONE":
                return jsonify({
                    "result": False,
                    "message": "Game is already completed"
                }), 410
            else:
                if not player_id in game_info.players:
                    return jsonify({
                        "result": False,
                        "message": "player not found"
                    }), 404

                if game_info.current_player_turn != player_id:
                    return jsonify({
                        "result": False,
                        "message": "not your turn"
                    }), 409

                if game_info.state == "DONE":
                    return jsonify({
                        "result": False,
                        "message": "Game already finished"
                    }), 409

                # check whether the move is valid
                board = game_info.board
                column = validated_resp.get("data", {}).get("column")
                if is_valid(board, column):
                    row = get_current_null_position(board, column)
                    board = set_value(board, row, column, player_id)
                    game_info.board = board
                    move_number = game_info.move_number
                    game_info.move_number += 1
                    current_player_turn = list(game_info.players)
                    current_player_turn.remove(player_id)
                    game_info.current_player_turn = current_player_turn[0]
                    game_info.moves += [
                        {
                            "type": "MOVE",
                            "column": column,
                            "player": player_id
                        }
                    ]

                    if winning_move(board, player_id):
                        game_info.winner = player_id
                        game_info.state = "DONE"
                        game_info.game_in_progress = False
                        game_info.save()
                        return jsonify({
                            "result": True,
                            "data": f"{game_id}/moves/{move_number}",
                            "message": "You Win"
                        }), 202
                    else:
                        game_info.save()
                        return jsonify({
                            "result": True,
                            "data": f"{game_id}/moves/{move_number}"
                        }), 202
                else:
                    # Game over and no one won
                    game_info.winner = None
                    game_info.state = "DONE"
                    game_info.game_in_progress = False
                    game_info.save()
                    return jsonify({
                        "result": True,
                        "message": "No one Won"
                    }), 202
        else:
            return jsonify({
                "result": False,
                "message": "malformed request"
            }), 400

    elif request.method == "DELETE":
        is_token_valid = validate_token(game_id)
        if is_token_valid:
            game_info = Game.objects.filter(game_id=game_id).first()
            if not game_info:
                return jsonify({
                    "result": False,
                    "message": "game not found"
                }), 404
            elif game_info.state == "DONE":
                return jsonify({
                    "result": False,
                    "message": "Game is already completed"
                }), 410
            else:
                if not player_id in game_info.players:
                    return jsonify({
                        "result": False,
                        "message": "player not found"
                    }), 404
                game_info.moves += [{
                    "type": "QUIT",
                    "player": player_id
                }]
                winner = list(game_info.players)
                winner.remove(player_id)
                game_info.winner = winner[0]
                game_info.state = "DONE"
                game_info.game_in_progress = False
                game_info.save()
                return jsonify({
                    "result": True,
                    "message": "Game Over"
                }), 202
        else:
            return jsonify({
                "result": False,
                "message": "malformed request"
            }), 400


#<==================================================================================================>
#                                RETURN THE MOVE
#<==================================================================================================>
@api_blueprint.route("/<game_id>/moves/<move_number>", methods=["GET"])
def get_a_move(game_id, move_number):
    is_token_valid = validate_token(game_id)
    if not move_number.isdigit():
        return jsonify({
            "result": False,
            "message": "malformed request"
        }), 400
    move_number = int(move_number)

    if is_token_valid:
        game_info = Game.objects.filter(game_id=game_id).fields(moves=1).first()
        if not game_info:
            return jsonify({
                "result": False,
                "message": "game not found"
            }), 404
        else:
            ma_schema = GameMovesSchema()
            data = ma_schema.dump(game_info).get("moves")
            if move_number < len(data):
                return jsonify({
                    "result": True,
                    "data": data[move_number]
                }), 200
            else:
                return jsonify({
                    "result": False,
                    "message": "move not found"
                }), 404
    else:
        return jsonify({
            "result": False,
            "message": "malformed request"
        }), 400


#<==================================================================================================>
#                                      VALIDATE TOKEN FUNCTION
#<==================================================================================================>
def validate_token(token):
    is_token_valid = True
    try:
        uuid.UUID(token, version=4)
    except:
        is_token_valid = False
    return is_token_valid
