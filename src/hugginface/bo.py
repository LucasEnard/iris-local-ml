from grongier.pex import BusinessOperation
import iris

from msg import HFRequest,HFResponse,MLRequest,MLResponse
from dataclasses import asdict

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

# > This class is a business operation that receives a request from the client, sends it to the HF (Hunggin Face)
# API, and returns the response to the client.
class HFOperation(BusinessOperation):

    def on_hfrequest(self,request:HFRequest):
        """
        > The function takes a request object, queries the API, and returns a response object
        
        :param request: The request object that is passed to the function
        :type request: HFRequest
        :return: A HFResponse object
        """
        return HFResponse(self.query(request.api_key,request.api_url,request.payload))
        
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

    generator = None

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

        # Downloading the model and the config from HuggingFace 
        if hasattr(self,"model_url"):
            try:
                soup = BS(requests.get(self.model_url + "/tree/main").text,features="html.parser")
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
                self.log_warning(str(e))
                self.log_info("Impossible to request from HuggingFace ; loading the model and the config from existing folder " + self.path + self.name)
        else:
            self.log_info("No given model_url ; trying to load the model and the config from the folder " + self.path + self.name)


        # Get all the attributes of self to put it into the pipeline
        config_attr = set(dir(self)).difference(set(dir(BusinessOperation))).difference(set(['name','model_url','path','download','on_ml_request','object_detection_segmentation','generator','to_dict']))
        config_dict = dict()
        for attr in config_attr:
            config_dict[attr] = getattr(self,attr)
        # Loading the model and the config from the folder.
        self.generator = pipeline(model=self.path + self.name, tokenizer=self.path + self.name, **config_dict)
        self.log_info("Model and config loaded")

    def download(self,name,url):
        """
        It downloads a file from a url and displays a progress bar
        
        :param name: the name of the file to download
        :param url: The URL of the file you want to download
        """
        if not exists(self.path + self.name):
            mkdir(self.path + self.name)
        if not exists(self.path + self.name + "/" + name):
            with open(self.path + self.name + "/" + name, "wb") as f:
                self.log_info("Downloading %s" % name)
                response = requests.get(url, stream=True)
                total_length = response.headers.get('content-length')

                if total_length is None or int(total_length) < 0.1E9: # no content length header
                    f.write(response.content)
                else:
                    try:
                        nb_chunck = min(20,ceil(ceil(int(total_length))*1E-8))
                    except Exception as e:
                        self.log_warning(str(e))
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

    def to_dict(self,request):
        """
        It takes a request object and returns a dictionary of all the attributes of the request object that
        don't start with an underscore
        
        :param request: The request object
        :return: A dictionary of the request object.
        """
        args = dict()
        for key,value in request.__dict__.items():
            if key[0] != "_":
                args[key] = value
        return args

    def on_ml_request(self,request:MLRequest):
        """
        > The function takes in a request object, converts it into a dictionary, and then calls the
        `generator` function with the dictionary as arguments
        
        :param request: The request object that is passed to the service
        :type request: MLRequest
        """

        resp = MLResponse()

        # Checking if the task is object detection or image segmentation or image classification. If it is, it
        # calls the object_detection_segmentation function.
        if self.task == "object-detection" or self.task == "image-segmentation" or self.task == "image-classification":
            resp = self.object_detection_segmentation(request)
        # Calling the `generator` function with the dictionary `args` as arguments.
        else:
            ret = self.generator(**self.to_dict(MLRequest))
            resp.output = ret

        return resp
    
    def object_detection_segmentation(self,req):
        """
        It takes in an image and returns the detected objects in the image
        
        :param req: The request message
        :return: The response is a list of dictionaries. Each dictionary contains the label, the confidence
        score, the bounding box coordinates and the mask of the detected object.
        """

        # Trying to open the image from the url. 
        # If it fails, it tries to open the image from a path.
        try:
            image = Image.open(requests.get(req.url, stream=True).raw)
        except IOError:
            image = Image.open(req.url)

        # Calling the `generator` function with the image as an argument.
        res = self.generator(image)
        resp = MLResponse(res)

        # Drawing the bounding box and the label on the image for each detected object
        if "box" in res[0]:
            resp = iris.cls('PEX.Msg.ImageDisplay')._New()
            drawimage = ImageDraw.Draw(image)
            for object in res:
                r = random.randint(0,255)
                g = random.randint(0,255)
                b = random.randint(0,255)
                rgb = (r,g,b)
                xmin,ymin,xmax,ymax = object["box"].values()
                label = object["label"]
                drawimage.rectangle(((xmin,ymin),(xmax,ymax)),outline=rgb,width=2)
                drawimage.text((xmin,ymin),label,rgb)

            # Converting the image into a binary format and then writing it into the 
            # BinaryImage field of the response.
            output = BytesIO()
            image.save(output, format="png")
            buffer = 3600
            binary = output.getvalue()
            chunks = [binary[i:i+buffer] for i in range(0, len(binary), buffer)]
            for chunk in chunks:
                resp.BinaryImage.Write(chunk)
        # Drawing the masks of each detected object on the image
        elif "mask" in res[0]:
            resp = iris.cls('PEX.Msg.ImageDisplay')._New()
            coloredimage = image.copy()
            for object in res:
                r = random.randint(0,255)
                g = random.randint(0,255)
                b = random.randint(0,255)
                rgb = (r,g,b)
                try:
                    bnw_image = Image.open(BytesIO(base64.b64decode(object['mask'])))
                except:
                    bnw_image = object['mask']
                coloredimage = Image.composite(Image.new('RGBA', image.size, color = rgb),coloredimage,bnw_image)
            
            # Creating a mask with a transparency of 185 and then compositing the colored image with the original
            # image.
            mask = Image.new('RGBA', image.size, color = (255,255,255))
            mask.putalpha(185)
            image = Image.composite(coloredimage,image,mask)

            # Converting the image into a binary format and then writing it into the 
            # BinaryImage field of the response.
            output = BytesIO()
            image.save(output, format="png")
            buffer = 3600
            binary = output.getvalue()
            chunks = [binary[i:i+buffer] for i in range(0, len(binary), buffer)]
            for chunk in chunks:
                resp.BinaryImage.Write(chunk)
        # The default case where the output is not an image.
        else:
            resp.output = res

        return resp

