from grongier.pex import BusinessOperation

from msg import HFRequest,HFResponse,MLRequest,MLResponse

from os.path import exists
from os import mkdir

import json
import requests

from bs4 import BeautifulSoup as BS

from transformers import pipeline

class HFOperation(BusinessOperation):
    def on_init(self):
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
        if not hasattr(self,"path"):
            self.path = "/irisdev/app/src/model/"

        if not hasattr(self,"name"):
            self.name = "gpt2"

        if not hasattr(self,'task'):
            self.task = "text-generation"

        if hasattr(self,"model_url"):
            try:
                soup = BS(requests.get(self.model_url + "/tree/main").text)
                elem = soup.findAll('a',{"download":True,"href":True})
                for el in elem:
                    href = el['href']
                    tmp_name = href.split("/")[-1]
                    # Check if .gitignore or LICENSE file or readme file
                    # if tmp_name[0] != "." and tmp_name.lower() != "license" and tmp_name.split(".")[-1] != "md":
                    #     self.download(tmp_name,"https://huggingface.co" + href)
                    self.download(tmp_name,"https://huggingface.co" + href)
                self.log_info("All downloads are completed or cached ; loading the model and the config from folder " + self.path + self.name)
            except Exception as e:
                self.log_info(str(e))
                self.log_info("Impossible to request from HuggingFace ; loading the model and the config from existing folder " + self.path + self.name)
        else:
            self.log_info("No given model_url ; trying to load the model and the config from the folder " + self.path + self.name)


        try:
            config_attr = set(dir(self)).difference(set(dir(BusinessOperation))).difference(set(['name','model_url','path','download','on_ml_request']))
            config_dict = dict()
            for attr in config_attr:
                config_dict[attr] = getattr(self,attr)
            self.generator = pipeline(model=self.path + self.name, tokenizer=self.path + self.name, **config_dict)
            self.log_info("Model and config loaded")
        except Exception as e:
            self.log_info(str(e))
            self.log_info("Error while loading the model and the config")
        return

    def download(self,name,url):
        try:
            if not exists(self.path + self.name):
                mkdir(self.path + self.name)
            if not exists(self.path + self.name + "/" + name):
                with open(self.path + self.name + "/" + name, "wb") as f:
                    self.log_info("Downloading %s" % name)
                    response = requests.get(url, stream=True)
                    total_length = response.headers.get('content-length')

                    if total_length is None or int(total_length) < 0.2E9: # no content length header
                        f.write(response.content)
                    else:
                        try:
                            nb_chunck = min(20,int(int(total_length)*1E-8))
                        except Exception as e:
                            self.log_info(str(e))
                            nb_chunck = 20
                        dl = 0
                        total_length = int(total_length)
                        for data in response.iter_content(chunk_size=int(total_length/nb_chunck)):
                            dl += len(data)
                            f.write(data)
                            done = int(nb_chunck * dl / total_length)
                            self.log_info(f"[{'#' * done + ' -' * (nb_chunck-done)}] " + f"{round(dl*1E-9,2)}go/{round(total_length*1E-9,2)}go")
                self.log_info("Download complete for " + name) 
            else:
                self.log_info("Existing files found for " + name)
        except Exception as e:
            self.log_info(str(e))

    def on_message(self,request):
        return

    def on_ml_request(self,request:MLRequest):
        args = dict()
        for key,value in request.__dict__.items():
            if key[0] != "_":
                args[key] = value

        resp = MLResponse()

        try:   
            ret = self.generator(**args)
            resp.output = ret

        except Exception as e:
            self.log_info(str(e))
        return resp
    



