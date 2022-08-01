from charset_normalizer import from_path
import transformers
from grongier.pex import BusinessOperation
from msg import HFRequest,HFResponse,MLRequest,MLResponse

from os.path import exists
import json
import requests
#import tensorflow as tf
import transformers
from transformers import TFAutoModel,AutoTokenizer

class HFOperation(BusinessOperation):
    def on_init(self):
        if not hasattr(self, "api_key"):
            setattr(self, "api_key", "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")
        return

    def on_message(self,request):
        self.log_info(str(request))
        return

    def on_hfrequest(self,request:HFRequest):
        response = HFResponse(self.query(request.api_url,request.payload))
        return response
        
    def query(self,api_url,payload):
        data = json.dumps(payload)
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.request("POST", api_url, headers=headers, data=data)
        return json.loads(response.content.decode("utf-8"))

class MLOperation(BusinessOperation):
    def on_init(self):
        # if not hasattr(self,"transf_mod_name"):
        #     self.transf_mod_name = "TFOpenAIGPTLMHeadModel"
        # if not hasattr(self,"transf_tok_name"):
        #     self.transf_tok_name = "OpenAIGPTTokenizer"

        if not hasattr(self,"model_url"):
            self.model_url = "https://s3.amazonaws.com/models.huggingface.co/bert/openai-gpt-tf_model.h5"
        if not hasattr(self,"config_url"):
            self.config_url = "https://s3.amazonaws.com/models.huggingface.co/bert/openai-gpt-config.json"

        self.model_name = self.model_url.split("/")[-1]
        self.config_name = self.config_url.split("/")[-1]

        if not hasattr(self,"path"):
            self.path = "/irisdev/app/src/model/"

        self.download(self.model_name,self.model_url)
        self.download(self.config_name,self.config_url)

        self.log_info("All downloads are completed or cached, loading the model and the config")
        self.model = TFAutoModel.from_pretrained(pretrained_model_name_or_path = self.path + self.config_name, config = self.path + self.model_name,from_pt=True)
        #self.model = TFAutoModel.from_pretrained(self.path)
        self.tokenizer = AutoTokenizer.from_pretrained("openai-gpt")
        return

    def download(self,name,url):
        try:
            if not exists(self.path + name):
                with open(self.path + name, "wb") as f:
                    self.log_info("Downloading %s" % name)
                    response = requests.get(url, stream=True)
                    total_length = response.headers.get('content-length')

                    if total_length is None: # no content length header
                        f.write(response.content)
                    else:
                        dl = 0
                        total_length = int(total_length)
                        for data in response.iter_content(chunk_size=int(total_length/20)):
                            dl += len(data)
                            f.write(data)
                            done = int(20 * dl / total_length)
                            self.log_info(f"[{'=' * done + '-' * (20-done)}] " + f"{round(dl*1E-9,2)}go/{round(total_length*1E-9,2)}go")
                self.log_info("Download complete") 
            else:
                self.log_info("Existing files found for " + name)
        except Exception as e:
            self.log_info(str(e))

    def on_message(self,request):
        return

    def on_ml_request(self,request:MLRequest):
        resp = MLResponse()
        try:   
            inputs = self.tokenizer(request.input, return_tensors="tf")

            outputs = self.model(inputs)
            
            resp.logits = outputs.logits
        except Exception as e:
            self.log_info(str(e))
        return resp
    



