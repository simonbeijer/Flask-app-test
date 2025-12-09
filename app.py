""" Flask API """

# import
from flask import Flask, request, jsonify, session, render_template, redirect
from game import Game, Player

# Integrate Flask
app = Flask(__name__)
app.secret_key = 'a_secret_key'

# API function
@app.route("/")
def index():
    return redirect("/game")

@app.route("/game")
def game_ui():
    return render_template("index.html")

@app.route('/game/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')

    player = Player()
    name_valid, name_msg = player.validate_name(name)
    if not name_valid:
        return jsonify({'success': False, 'message': name_msg})

    session['player'] = player.__dict__
    return jsonify({'success': True, 'player_name': player.player_name})

@app.route("/game/start")
def start_game():
    if 'player' not in session:
        return jsonify({"error": "Player not registered."}), 400

    game = Game()
    game.initialize_game()
    session['game_state'] = game.__dict__
    return jsonify({
        "message": "Game started! Pick a number.",
        "lucky_list": game.full_lucky_list,
    })

@app.route("/game/guess/<int:number>")
def guess(number):
    if 'game_state' not in session:
        return jsonify({"error": "Game not started. Please go to /game/start"}), 400

    game_state = session['game_state']
    game_state['tries_count'] += 1

    if number == game_state['lucky_number']:
        player_name = session.get('player', {}).get('player_name', 'Player')
        message = f"Congrats {player_name}, you've won! The lucky number was {game_state['lucky_number']} and you got it in {game_state['tries_count']} tries."
        session.pop('game_state', None)
        return jsonify({ "message": message })

    numbers_to_show = []
    if game_state['tries_count'] == 1:
        # This is the first wrong guess, show the shorter list
        numbers_to_show = game_state['shorter_lucky_list']
    else:
        # Subsequent wrong guesses, remove the number and show the list
        if number in game_state['shorter_lucky_list']:
            game_state['shorter_lucky_list'].remove(number)
        numbers_to_show = game_state['shorter_lucky_list']

    game = Game()
    if game.check_length_list(numbers_to_show):
        session.pop('game_state', None)
        return jsonify({ "message": "You lost! No more numbers to guess from." })

    session['game_state'] = game_state
    return jsonify({
        "message": "Wrong guess, try again!",
        "numbers_to_show": numbers_to_show
    })

@app.route("/game/state")
def game_state():
    if 'game_state' not in session:
        return jsonify({"error": "No active game."}), 400
    return jsonify(session['game_state'])

# Start server
if __name__ == "__main__":
    app.run(debug=True)
