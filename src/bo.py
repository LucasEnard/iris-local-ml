from grongier.pex import BusinessOperation
from msg import HFRequest,HFResponse

from os.path import exists
import json
import requests
from clint.textui import progress

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

        if not hasattr(self,"model_name"):
            self.model_name = "step_383500_slim.tar.zstd"
        if not hasattr(self,"model_url"):
            self.model_url = "https://the-eye.eu/public/AI/GPT-J-6B/step_383500_slim.tar.zstd"
        try:
            if not exists(f"/irisdev/app/src/model/{self.model_name}"):
                with open(f"/irisdev/app/src/model/{self.model_name}", "wb") as f:
                    self.log_info("Downloading %s" % self.model_name)
                    response = requests.get(self.model_url, stream=True)
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
                self.log_info("Existing files for model found")
        except Exception as e:
            self.log_info(str(e))
        return

    def on_message(self,request):
        return
    



