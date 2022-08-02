# import json
# import requests


# api_url = "https://api-inference.huggingface.co/models/gpt2"
# API_TOKEN = "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"
# headers = {"Authorization": f"Bearer {API_TOKEN}"}
# def query(payload):
#     data = json.dumps(payload)
#     response = requests.request("POST", api_url, headers=headers, data=data)
#     return json.loads(response.content.decode("utf-8"))
# data = query("Can you please let us know more details about your ")
# print(data)

#-----------------------------

# from transformers import GPT2Tokenizer, GPT2LMHeadModel
# tokenizer = GPT2Tokenizer.from_pretrained('gpt2-large',cache_dir="./src/model/gpt2-large-tok")
# model = GPT2LMHeadModel.from_pretrained('gpt2-large', pad_token_id = tokenizer.eos_token_id, cache_dir="./src/model/gpt2-large-mod")
# text = "And so was the story of"
# encoded_input = tokenizer.encode(text, return_tensors='pt')
# output = model.generate(encoded_input, max_length = 10000, num_beams = 5, no_repeat_ngram_size  = 2, early_stopping = True)
# print(tokenizer.decode(output[0],skip_special_tokens=True))

#-----------------------------

# from os.path import exists
# import requests
# from clint.textui import progress



# resp = requests.get("https://the-eye.eu/public/AI/GPT-J-6B/step_383500_slim.tar.zstd",stream=True)
# with open("src/model/step_383500_slim.tar.zstd","wb") as file:
#     total_length = int(resp.headers.get('content-length'))
#     for chunk in progress.bar(resp.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
#         if chunk:
#             file.write(chunk)
#             file.flush()

# import sys
# import requests

# from bs4 import BeautifulSoup as BS

# link = "https://huggingface.co/gpt2/tree/main"
# soup = BS(requests.get(link).text)
# elem = soup.findAll('a',{"download":True,"href":True})
# print()
# for el in elem:
#     print(el['href'])
#     print()


# with open(file_name, "wb") as f:
#     print("Downloading %s" % file_name)
#     response = requests.get(link, stream=True)
#     total_length = response.headers.get('content-length')
#     if total_length is None: # no content length header
#         f.write(response.content)
#     else:
#         dl = 0
#         total_length = int(total_length)
#         for data in response.iter_content(chunk_size=int(total_length/1000)):
#             dl += len(data)
#             f.write(data)
#             done = int(25 * dl / total_length)
#             sys.stdout.write(f"[{'=' * done + ' ' * (25-done)}] " + f"{int(dl/1000)}mo/{int(total_length/1000)}mo" )
#             sys.stdout.flush()

#--------------------------------------

# import transformers
# import torch
# from transformers import AutoModel,AutoTokenizer


# from transformers import GPT2Tokenizer, TFGPT2Model
# tokenizer = GPT2Tokenizer.from_pretrained("src/model/gpt2")
# model = TFGPT2Model.from_pretrained("src/model/gpt2")
# text = "Replace me by any text you'd like."
# encoded_input = tokenizer(text, return_tensors='tf')
# output = model(encoded_input)

# print(tokenizer.decode(output))

from transformers import pipeline, set_seed

generator = pipeline('text-generation', model='src/model/gpt2', tokenizer='src/model/gpt2')

ret = generator("Hello, I'm a language model,", max_length=30, num_return_sequences=5)

for el in ret:
    print(el)