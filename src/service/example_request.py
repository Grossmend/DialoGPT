
import time
import requests


PREDICT_SERVICE_URL = 'http://localhost:8010/gpt/'


def main():

    params = {
        'max_length': 256,
        'no_repeat_ngram_size': 3,
        'do_sample': True,
        'top_k': 100,
        'top_p': 0.9,
        'temperature': 0.6,
        'num_return_sequences': 5,
        'device': 0,
        'is_always_use_length': True,
        'length_generate': '1',
    }

    inputs = [
        {'speaker': 0, 'text': 'Привет, как день прошел?'},
        {'speaker': 1, 'text': 'Хорошо, а у тебя как?'},
        {'speaker': 0, 'text': 'Нормально, посоветуй фильм посмотреть'},
    ]

    s0 = time.time()

    res = requests.post(PREDICT_SERVICE_URL, json={'inputs': inputs, 'params': params})
    res = res.json()

    print()
    print(f"Status is: {res['status']}")
    print(f"Message is: {res['msg']}\n")
    for response in res['outputs']:
        print(f"{'-' * 25}")
        print(f"{response}")

    print(f"{'-' * 25}")
    print(f"\nDone! Time is: {(time.time() - s0):.4f}")


if __name__ == '__main__':
    main()
