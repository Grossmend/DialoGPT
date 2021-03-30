
import os
import uvicorn
from fastapi import FastAPI, Body
from typing import Dict

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)


app = FastAPI()


params_default = {
    'max_length': 256,
    'no_repeat_ngram_size': 3,
    'do_sample': True,
    'top_k': 100,
    'top_p': 0.9,
    'temperature': 0.6,
    'num_return_sequences': 3,
    'device': 'cpu',
    'is_always_use_length': True,
    'length_generate': '1',
}


huggingface_models = [
    'Grossmend/rudialogpt3_medium_based_on_gpt2',
]


class GPT:

    def __init__(self, path_model: str):
        self.path_model = path_model
        self.tokenizer = None
        self.model = None
        self._check_is_enough()
        self._load_model()

    def _load_model(self):
        print(f"===> Load model: {self.path_model} ...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.path_model)
        self.model = AutoModelForCausalLM.from_pretrained(self.path_model)

    def _check_is_enough(self):

        if self.path_model in huggingface_models:
            return

        if not os.path.isdir(self.path_model):
            raise Exception(f"Path '{self.path_model}' not found!")

        if not os.path.isfile(os.path.join(self.path_model, 'config.json')):
            raise Exception(f"On path '{self.path_model}' file 'config.json' not found!")

        if not os.path.isfile(os.path.join(self.path_model, 'pytorch_model.bin')):
            raise Exception(f"On path '{self.path_model}' file 'pytorch_model.bin' not found!")

        if not os.path.isfile(os.path.join(self.path_model, 'vocab.json')):
            raise Exception(f"On path '{self.path_model}' file 'vocab.json' not found!")

        if not os.path.isfile(os.path.join(self.path_model, 'tokenizer_config.json')):
            raise Exception(f"On path '{self.path_model}' file 'tokenizer_config.json' not found!")

        if not os.path.isfile(os.path.join(self.path_model, 'special_tokens_map.json')):
            raise Exception(f"On path '{self.path_model}' file 'special_tokens_map.json' not found!")

        if not os.path.isfile(os.path.join(self.path_model, 'merges.txt')):
            raise Exception(f"On path '{self.path_model}' file 'merges.txt' not found!")

    async def get_responses(self, inputs: Dict, params: Dict) -> Dict:

        params_ = {
            'max_length': params.get('max_length', params_default['max_length']),
            'no_repeat_ngram_size': params.get('no_repeat_ngram_size', params_default['no_repeat_ngram_size']),
            'do_sample': params.get('do_sample', params_default['do_sample']),
            'top_k': params.get('top_k', params_default['top_k']),
            'top_p': params.get('top_p', params_default['top_p']),
            'temperature': params.get('temperature', params_default['temperature']),
            'num_return_sequences': params.get('num_return_sequences', params_default['num_return_sequences']),
            'device': params.get('device', params_default['device']),
            "is_always_use_length": params.get('is_always_use_length', params_default['is_always_use_length']),
            "length_generate": params.get('length_generate', params_default['length_generate']),
        }

        inputs_text = ''
        for input_ in inputs:
            if params_['is_always_use_length']:
                length_rep = len(self.tokenizer.encode(input_['text']))
                if length_rep <= 15:
                    length_param = '1'
                elif length_rep <= 50:
                    length_param = '2'
                elif length_rep <= 256:
                    length_param = '3'
                else:
                    length_param = '-'
            else:
                length_param = '-'
            inputs_text += f"|{input_['speaker']}|{length_param}|{input_['text']}"
        inputs_text += f"|1|{params_['length_generate']}|"

        print(f"\n===> Params generate: {params_}")
        print(f"===> Text input: {inputs_text}")

        inputs_token_ids = self.tokenizer.encode(inputs_text, return_tensors='pt')

        try:
            # ToDo make this asynchronous
            outputs_token_ids = self.model.generate(
                inputs_token_ids,
                max_length=params_['max_length'],
                no_repeat_ngram_size=params_['no_repeat_ngram_size'],
                do_sample=params_['do_sample'],
                top_k=params_['top_k'],
                top_p=params_['top_p'],
                temperature=params_['temperature'],
                num_return_sequences=params_['num_return_sequences'],
                device=params_['device'],
                mask_token_id=self.tokenizer.mask_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                unk_token_id=self.tokenizer.unk_token_id,
                pad_token_id=self.tokenizer.pad_token_id,
            )
        except Exception as e:
            print(f"===> Error generate: {str(e)}")
            return {'inputs': '', 'outputs': '', 'status': False, 'msg': f"{str(e)}"}

        outputs = [self.tokenizer.decode(x, skip_special_tokens=True) for x in outputs_token_ids]
        outputs = [x.split('|')[-1] for x in outputs]

        return {'inputs': inputs, 'outputs': outputs, 'status': True, 'msg': ''}


@app.post("/")
def about():
    return "RuDialoGPT Service"


@app.post("/gpt/")
async def get_responses(payload: dict = Body(...)):
    inputs = payload.get('inputs', '')
    params = payload.get('params', {})
    responses = await gpt.get_responses(inputs=inputs, params=params)
    return responses


if __name__ == '__main__':
    # gpt = GPT(path_model='../../../Models/RuDialoGPT')
    gpt = GPT(path_model='Grossmend/rudialogpt3_medium_based_on_gpt2')
    uvicorn.run(app, host='127.0.0.1', port=8010)
