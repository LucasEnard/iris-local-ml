from grongier.pex import BusinessOperation
import iris

from msg import HFRequest,HFResponse,MLRequest,MLResponse

from os.path import exists
from os import mkdir

from math import ceil
import random

from io import BytesIO
import base64

from PIL import Image,ImageDraw

import json
import requests

from bs4 import BeautifulSoup as BS

from transformers import pipeline

class HFOperation(BusinessOperation):
    def on_init(self):
        return

    def on_message(self,request):
        """
        The function takes a request object, logs it, and returns nothing
        
        :param request: The request object
        :return: The request object is being returned.
        """
        self.log_info(str(request))
        return

    def on_hfrequest(self,request:HFRequest):
        """
        > The function takes a request object, queries the API, and returns a response object
        
        :param request: The request object that is passed to the function
        :type request: HFRequest
        :return: A HFResponse object
        """
        response = HFResponse(self.query(request.api_key,request.api_url,request.payload))
        return response
        
    def query(self,api_key,api_url,payload):
        """
        It takes an API key, an API URL, and a payload (a dictionary of the query parameters) and returns
        the response from the API as a dictionary
        
        :param api_key: Your API key
        :param api_url: The URL of the API endpoint you're querying
        :param payload: The query you want to run
        :return: A JSON object
        """
        data = json.dumps(payload)
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.request("POST", api_url, headers=headers, data=data)
        return json.loads(response.content.decode("utf-8"))

class MLOperation(BusinessOperation):
    def on_init(self):
        """
        It downloads the model and the config from HuggingFace if the model_url is given, otherwise it
        tries to load the model and the config from the folder
        :return: The answer is a list of strings.
        """
        if not hasattr(self,"path"):
            self.path = "/irisdev/app/src/model/"

        if not hasattr(self,"name"):
            self.name = "gpt2"

        if not hasattr(self,'task'):
            self.task = "text-generation"

        if hasattr(self,"model_url"):
            try:
                # Get the elements from the html page of the model page on HuggingFace
                soup = BS(requests.get(self.model_url + "/tree/main").text)
                elem = soup.findAll('a',{"download":True,"href":True})
                # Download every element
                for el in elem:
                    href = el['href']
                    tmp_name = href.split("/")[-1]
                    self.download(tmp_name,"https://huggingface.co" + href)
                self.log_info("All downloads are completed or cached ; loading the model and the config from folder " + self.path + self.name)
            except Exception as e:
                self.log_info(str(e))
                self.log_info("Impossible to request from HuggingFace ; loading the model and the config from existing folder " + self.path + self.name)
        else:
            self.log_info("No given model_url ; trying to load the model and the config from the folder " + self.path + self.name)


        try:
            # Get all the attributes of self to put it into the pipeline
            config_attr = set(dir(self)).difference(set(dir(BusinessOperation))).difference(set(['name','model_url','path','download','on_ml_request','object_detection_segmentation']))
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
                # Open the file and write in it by chunck of size total_lenght/20.
                # For every chunck, write an advancement message in the logs
                with open(self.path + self.name + "/" + name, "wb") as f:
                    self.log_info("Downloading %s" % name)
                    response = requests.get(url, stream=True)
                    total_length = response.headers.get('content-length')

                    if total_length is None or int(total_length) < 0.2E9: # no content length header
                        f.write(response.content)
                    else:
                        try:
                            nb_chunck = min(20,ceil(ceil(total_length)*1E-8))
                        except Exception as e:
                            self.log_info(str(e))
                            nb_chunck = 20
                        dl = 0
                        total_length = int(total_length)
                        for data in response.iter_content(chunk_size=int(total_length/nb_chunck)):
                            dl += len(data)
                            f.write(data)
                            done = ceil(nb_chunck * dl / total_length)
                            self.log_info(f"[{'#' * done + ' -' * (nb_chunck-done)}] " + f"{round(dl*1E-9,2)}go/{round(total_length*1E-9,2)}go")
                self.log_info("Download complete for " + name) 
            else:
                self.log_info("Existing files found for " + name)
        except Exception as e:
            self.log_info(str(e))

    def on_message(self,request):
        return

    def on_ml_request(self,request:MLRequest):
        """
        > The function takes in a request object, puts it's variable into a dictionary, and then calls the
        `generator` function with the dictionary as arguments
        
        :param request: The request object that is passed to the operation
        :type request: MLRequest
        """
        args = dict()
        for key,value in request.__dict__.items():
            if key[0] != "_":
                args[key] = value

        resp = MLResponse()
        try: 

            if self.task == "object-detection" or self.task == "image-segmentation" or self.task == "image-classification":
                resp = self.object_detection_segmentation(request)
            else:
                ret = self.generator(**args)
                resp.output = ret

        except Exception as e:
            self.log_info(str(e))

        return resp
    
    def object_detection_segmentation(self,req):
        """
        The function takes in an image url and returns a response object with the image with the
        bounding boxes and labels drawn on it
        
        :param req: The request message that contains the image url
        :return: The output of the model is being returned.
        """
        # If the url is an url, download the image
        try:
            image = Image.open(requests.get(req.url, stream=True).raw)
        except:
            # Else, fecth the image from the local files
            try:
                image = Image.open(req.url)
            except Exception as e:
                self.log_info(str(e))

        res = self.generator(image)
        resp = MLResponse(res)
        try:
            # Drawing the bounding box and the label on the image for each detected object
            if res[0].__contains__("box"):
                resp = iris.cls('PEX.Msg.ImageDisplay')._New()
                drawimage = ImageDraw.Draw(image)
                # It's drawing the bounding boxes and the labels on the image.
                for object in res:
                    r = random.randint(0,255)
                    g = random.randint(0,255)
                    b = random.randint(0,255)
                    rgb = (r,g,b)
                    xmin,ymin,xmax,ymax = object["box"].values()
                    label = object["label"]
                    drawimage.rectangle(((xmin,ymin),(xmax,ymax)),outline=rgb,width=2)
                    drawimage.text((xmin,ymin),label,rgb)

                # It's converting the image into a binary and then writing it into the response object.
                output = BytesIO()
                image.save(output, format="png")
                n = 3600
                binary = output.getvalue()
                chunks = [binary[i:i+n] for i in range(0, len(binary), n)]
                for chunk in chunks:
                    resp.BinaryImage.Write(chunk)
            # Drawing the masks of each detected object on the image
            elif res[0].__contains__("mask"):
                resp = iris.cls('PEX.Msg.ImageDisplay')._New()
                coloredimage = image.copy()
                # It's drawing the masks of each detected object on the image.
                for object in res:
                    r = random.randint(0,255)
                    g = random.randint(0,255)
                    b = random.randint(0,255)
                    rgb = (r,g,b)
                    try:
                        bNwimage = Image.open(BytesIO(base64.b64decode(object['mask'])))
                    except:
                        bNwimage = object['mask']
                    coloredimage = Image.composite(Image.new('RGBA', image.size, color = rgb),coloredimage,bNwimage)
                
                # Takes the coloredimage and mask it into the base image
                mask = Image.new('RGBA', image.size, color = (255,255,255))
                mask.putalpha(185)
                image = Image.composite(coloredimage,image,mask)

                # It's converting the image into a binary and then writing it into the response object.
                output = BytesIO()
                image.save(output, format="png")
                n = 3600
                binary = output.getvalue()
                chunks = [binary[i:i+n] for i in range(0, len(binary), n)]
                for chunk in chunks:
                    resp.BinaryImage.Write(chunk)
            # The default case where the output is not an image.
            else:
                resp.output = res
        except Exception as e:
            self.log_info(str(e))
        return resp

