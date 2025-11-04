
from flask import Flask, request, jsonify
import laa_core

app = Flask(__name__)

@app.route('/decide', methods=['POST'])
def decide():
    data = request.get_json()
    algorithm = data['algorithm']
    problem_instance = data['problem_instance']
    prediction = data['prediction']

    if algorithm == 'ski_rental':
        ski_rental = laa_core.SkiRental(problem_instance['buy_cost'])
        decision = ski_rental.decide(problem_instance['day'], prediction['days'], prediction['trust'])
        return jsonify({'decision': decision})
    elif algorithm == 'caching':
        predictions = {int(k): v for k, v in problem_instance['predictions'].items()}
        caching = laa_core.Caching(problem_instance['cache_size'], predictions)
        decision, new_cache = caching.decide(problem_instance['item'], problem_instance['cache'])
        return jsonify({'decision': decision, 'new_cache': new_cache})
    elif algorithm == 'oneway_trading':
        oneway_trading = laa_core.OnewayTrading(problem_instance['buy_price'])
        decision = oneway_trading.decide(problem_instance['current_price'], prediction['price'], prediction['trust'])
        return jsonify({'decision': decision})
    elif algorithm == 'scheduling':
        scheduling = laa_core.Scheduling(problem_instance['num_machines'])
        assignments = scheduling.decide(problem_instance['job_lengths'], prediction['job_lengths'])
        return jsonify({'assignments': assignments})
    elif algorithm == 'search':
        search = laa_core.Search(problem_instance['max_value'])
        best_index = search.decide(problem_instance['values'], prediction['value'])
        return jsonify({'best_index': best_index})
    else:
        return jsonify({'error': 'Unknown algorithm'}), 400

if __name__ == '__main__':
    app.run(debug=True)
