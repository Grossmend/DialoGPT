import requests

from typing import Dict
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)


PREDICT_SERVICE_URL = 'http://localhost:8010/gpt/'


def get_response(data: Dict) -> Dict:

    try:
        length = int(data['params']['length'])
        if length not in [0, 1, 2, 3]:
            return {'response': '',
                    'success': False,
                    'msg': f"Поле 'Length generate' должно принимать одно из следующих значений: [0, 1, 2, 3]. Текущее значение: {data['params']['length']}"}
    except Exception as e:
        return {'response': '',
                'success': False,
                'msg': f"Поле 'Length generate' должно принимать одно из следующих значений: [0, 1, 2, 3]. Текущее значение: {data['params']['length']}"}

    try:
        max_length = int(data['params']['max_length'])
        if max_length < 8 or max_length > 256:
            return {'response': '',
                    'success': False,
                    'msg': f"Поле 'Max length tokens generate' должно быть больше 8, но меньше 256. Текущее значение: {data['params']['max_length']}"}
    except Exception as e:
        return {'response': '',
                'success': False,
                'msg': f"Поле 'Max length tokens generate' должно быть больше или равно 8, но меньше или равно 256. Текущее значение: {data['params']['max_length']}"}

    try:
        no_repeat_ngram_size = int(data['params']['no_repeat_ngram_size'])
        if no_repeat_ngram_size < 1 or no_repeat_ngram_size > 10:
            return {'response': '',
                    'success': False,
                    'msg': f"Поле 'No repeat ngram size' должно быть больше или равно 1, но меньше или равно 10. Текущее значение: {data['params']['no_repeat_ngram_size']}"}
    except Exception as e:
        return {'response': '',
                'success': False,
                'msg': f"Поле 'Max length tokens generate' должно быть больше или равно 1, но меньше или равно 10. Текущее значение: {data['params']['no_repeat_ngram_size']}"}

    try:
        top_k = int(data['params']['top_k'])
        if top_k < 1 or top_k > 500:
            return {'response': '',
                    'success': False,
                    'msg': f"Поле 'Top K' должно быть больше или равно 1, но меньше или равно 500. Текущее значение: {data['params']['top_k']}"}
    except Exception as e:
        return {'response': '',
                'success': False,
                'msg': f"Поле 'Top K' должно быть больше или равно 1, но меньше или равно 500. Текущее значение: {data['params']['top_k']}"}

    try:
        top_p = float(data['params']['top_p'])
        if top_p < 0.01 or top_p > 1.0:
            return {'response': '',
                    'success': False,
                    'msg': f"Поле 'Top P' должно быть больше или равно 0.01, но меньше или равно 1.0. Текущее значение: {data['params']['top_p']}"}
    except Exception as e:
        return {'response': '',
                'success': False,
                'msg': f"Поле 'Top P' должно быть больше или равно 0.01, но меньше или равно 1.0. Текущее значение: {data['params']['top_p']}"}

    try:
        temperature = float(data['params']['temperature'])
        if temperature < 0.01 or temperature > 1.0:
            return {'response': '',
                    'success': False,
                    'msg': f"Поле 'Temperature' должно быть больше или равно 0.01, но меньше или равно 1.0. Текущее значение: {data['params']['temperature']}"}
    except Exception as e:
        return {'response': '',
                'success': False,
                'msg': f"Поле 'Temperature' должно быть больше или равно 0.01, но меньше или равно 1.0. Текущее значение: {data['params']['temperature']}"}

    try:
        num_return = int(data['params']['num_return'])
        if num_return < 1 or num_return > 10:
            return {'response': '',
                    'success': False,
                    'msg': f"Поле 'Num responses return' должно быть больше или равно 1, но меньше или равно 10. Текущее значение: {data['params']['no_repeat_ngram_size']}"}
    except Exception as e:
        return {'response': '',
                'success': False,
                'msg': f"Поле 'Num responses return' должно быть больше или равно 1, но меньше или равно 10. Текущее значение: {data['params']['no_repeat_ngram_size']}"}

    params = {
        "max_length": max_length,
        "no_repeat_ngram_size": no_repeat_ngram_size,
        "top_k": top_k,
        "top_p": top_p,
        "temperature": temperature,
        "num_return_sequences": num_return,
        "do_sample": data['params']['do_sample'],
        "device": 0 if data['params']['use_gpu'] else 'cpu',
        "is_always_use_len": True,
        "length_generate": length,
    }

    inputs = data['dialog_history_array']

    try:
        response = requests.post(PREDICT_SERVICE_URL, json={'inputs': inputs, 'params': params})
    except Exception as e:
        return {'response': '',
                'success': False,
                'msg': f"Connection predict service error."}

    if response.status_code == 200:

        response_data = response.json()

        if not response_data['status']:
            return {'response': '',
                    'success': False,
                    'msg': response_data['msg']}

        return {'response': response_data['outputs'][0],
                'variants_responses': response.json()['outputs'],
                'success': True,
                'msg': f""}
    else:
        return {'response': '',
                'success': False,
                'msg': f"Status code response from service: {response.status_code}"}


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/information")
def information():
    return render_template("information.html")


@app.route("/support")
def support():
    return render_template("support.html")


@app.route("/dialog", methods=['POST'])
def message():
    if request.method == "POST":
        data = request.get_json()
        response = get_response(data=data)
        return jsonify(response)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8020, debug=False)
