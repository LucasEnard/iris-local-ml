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

# from transformers import AutoTokenizer, AutoModelForCausalLM

# tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")

# model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-j-6B")


# text = "In a hole in the ground there lived"
# input = tokenizer(text)
# output = model(input)
# print(output)

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

# link = "https://the-eye.eu/public/AI/GPT-J-6B/step_383500_slim.tar.zstd"
# file_name = "src/model/step_383500_slim.tar.zstd"
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

# ("\r[%s%s]" % ('x' * done, '-' * (25-done)) )

print(1E-10)