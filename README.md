# 1. iris-huggingface
Usage of Machine Learning models in IRIS using Python

- [1. iris-huggingface](#1-iris-huggingface)
- [2. Installation](#2-installation)
  - [2.1. Starting the Production](#21-starting-the-production)
  - [2.2. Access the Production](#22-access-the-production)
  - [2.3. Closing the Production](#23-closing-the-production)
- [3. HuggingFace API](#3-huggingface-api)
- [4. Use any model from the web](#4-use-any-model-from-the-web)
  - [4.1. FIRST CASE : YOU HAVE YOUR OWN MODEL](#41-first-case--you-have-your-own-model)
  - [4.2. SECOND CASE : YOU WANT TO DOWNLOAD A MODEL FROM HUGGINGFACE](#42-second-case--you-want-to-download-a-model-from-huggingface)
    - [4.2.1. Settings](#421-settings)
    - [4.2.2. Testing](#422-testing)
- [5. TroubleShooting](#5-troubleshooting)
- [6. Conclusion](#6-conclusion)

# 2. Installation
## 2.1. Starting the Production
While in the iris-local-ml folder, open a terminal and enter :
```
docker-compose up
```

The very first time, it may take a few minutes to build the image correctly and install all the needed modules for Python.

## 2.2. Access the Production
Following this link, access the production :
[Access the Production](http://localhost:52795/csp/irisapp/EnsPortal.ProductionConfig.zen?RODUCTION=INFORMATION.QuickFixProduction)

## 2.3. Closing the Production
```
docker-compose down
```

# 3. HuggingFace API

You must first start the demo, using the green `Start` button or `Stop` and `Start` it again to apply your config changes.

Then, by clicking on the operation `Python.HFOperation` of your choice, and selecting in the right tab `action`, you can `test` the demo.

In this `test` window, select :<br>

Type of request : `Grongier.PEX.Message`<br>

For the `classname` you must enter :
```
msg.HFRequest
```

 And for the `json`, here is an example of a call to GPT2 :
```
{
    "api_url":"https://api-inference.huggingface.co/models/gpt2",
    "payload":"Can you please let us know more details about your ",
    "api_key":"----------------------"
}
```
Now you can click on `Visual Trace` to see in details what happened and see the logs.

**NOTE** that you must have an API key from HuggingFace before using this Operation ( the api-keys are free, you just need to register to HF )

**NOTE** that you can change the url to try any other models from HuggingFace, you may need to change the payload.

See as example:<br>
![sending hf req](https://user-images.githubusercontent.com/77791586/182403526-0f6e97a0-2019-4d86-b1ae-38c56dfc8746.png)
![hf req](https://user-images.githubusercontent.com/77791586/182403522-5e2f962f-2de0-40d3-8120-f2f3fcb74759.png)
![hf resp](https://user-images.githubusercontent.com/77791586/182403515-7c6c2075-bdb6-46cd-9258-ac251844d591.png)



# 4. Use any model from the web
In the section we will teach you how to use almost any model from the internet, HuggingFace or not.

## 4.1. FIRST CASE : YOU HAVE YOUR OWN MODEL
In this case, you must copy paste your model, with the config, the tokenizer.json etc inside a folder inside the model folder.<br>
Path : `src/model/yourmodelname/` 

From here you must go to the parameters of the `Python.MLOperation`.<br>
Click on the `Python.MLOperation` then go to `settings` in the right tab, then in the `Python` part, then in the `%settings` part.
Here, you can enter or modify any parameters ( don't forget to press `apply` once your are done ).<br>
Here's the default configuration for this case :<br>
%settings
```
name=yourmodelname
task=text-generation
```
**NOTE** that any settings that are not `name` or `model_url` will go into the PIPELINE settings.

Now you can double-click on the operation `Python.MLOperation` and `start` it.
You must see in the `Log` part the starting of your model.

From here, we create a `PIPELINE` using transformers that uses your config file find in the folder as seen before.

To call that pipeline, click on the operation `Python.MLOperation` , and select in the right tab `action`, you can `test` the demo.

In this `test` window, select :<br>

Type of request : `Grongier.PEX.Message`<br>

For the `classname` you must enter :
```
msg.MLRequest
```

 And for the `json`, you must enter every arguments needed by your model.<br>
 Here is an example of a call to GPT2 :
```
{
    "text_inputs":"Unfortunately, the outcome",
    "max_length":100,
    "num_return_sequences":3
}
```
Click `Invoke Testing Service` and wait for the model to operate.<br>

See for example:<br>
![sending ml req](https://user-images.githubusercontent.com/77791586/182402707-13ca90d0-ad5a-4934-8923-a58fe821e00e.png)

Now you can click on `Visual Trace` to see in details what happened and see the logs.

See for example :<br>
![ml req](https://user-images.githubusercontent.com/77791586/182402878-e34b64de-351c-49c3-affe-023cd885e04b.png)

![ml resp](https://user-images.githubusercontent.com/77791586/182402932-4afd14fe-5f57-4b03-b0a6-1c6b74474015.png)

## 4.2. SECOND CASE : YOU WANT TO DOWNLOAD A MODEL FROM HUGGINGFACE
In this case, you must find the URL of the model on HuggingFace;
### 4.2.1. Settings
From here you must go to the parameters of the `Python.MLOperation`.<br>
Click on the `Python.MLOperation` then go to `settings` in the right tab, then in the `Python` part, then in the `%settings` part.
Here, you can enter or modify any parameters ( don't forget to press `apply` once your are done ).<br>
Here's some example configuration for some models we found on HuggingFace :<br>
%settings for gpt2
```
model_url=https://huggingface.co/gpt2
name=gpt2
task=text-generation
```

%settings for camembert-ner
```
name=camembert-ner
model_url=https://huggingface.co/Jean-Baptiste/camembert-ner
task=ner
aggregation_strategy=simple
```

%settings for bert-base-uncased
```
name=bert-base-uncased
model_url=https://huggingface.co/bert-base-uncased
task=fill-mask
```

**NOTE** that any settings that are not `name` or `model_url` will go into the PIPELINE settings, so in our second example, the camembert-ner pipeline requirers an `aggregation_strategy` and a `task` that are specified here while the gpt2 requirers only a `task`.

See as example:<br>
![settings ml ope2](https://user-images.githubusercontent.com/77791586/182403258-c24efb77-2696-4462-ae71-9184667ac9e4.png)

Now you can double-click on the operation `Python.MLOperation` and `start` it.<br>
**You must see in the `Log` part the starting of your model and the downloading.**<br>
**NOTE** You can refresh those logs every x seconds to see the advancement with the downloads.
![dl in real time](https://user-images.githubusercontent.com/77791586/182403064-856724b5-876e-460e-a2b4-34eb63f44673.png


From here, we create a `PIPELINE` using transformers that uses your config file find in the folder as seen before.

### 4.2.2. Testing
To call that pipeline, click on the operation `Python.MLOperation` , and select in the right tab `action`, you can `test` the demo.

In this `test` window, select :<br>

Type of request : `Grongier.PEX.Message`<br>

For the `classname` you must enter :
```
msg.MLRequest
```

 And for the `json`, you must enter every arguments needed by your model.<br>
 Here is an example of a call to GPT2 ( `Python.MLOperation` ):
```
{
    "text_inputs":"George Washington lived",
    "max_length":30,
    "num_return_sequences":3
}
```

 Here is an example of a call to Camembert-ner ( `Python.MLOperation2` ) :
```
{
    "inputs":"George Washington lived in washington"
}
```

 Here is an example of a call to bert-base-uncased ( `Python.MLOperation3` ) :
```
{
    "inputs":"George Washington lived in [MASK]."
}
```
Click `Invoke Testing Service` and wait for the model to operate.<br>
Now you can click on `Visual Trace` to see in details what happened and see the logs.

**NOTE** that once the model was downloaded once, the production won't download it again but get the cached files found at `src/model/TheModelName/`.<br>
If some files are missing, the Production will download them again.

See as example:<br>
![sending ml req](https://user-images.githubusercontent.com/77791586/182402707-13ca90d0-ad5a-4934-8923-a58fe821e00e.png)
![ml req](https://user-images.githubusercontent.com/77791586/182402878-e34b64de-351c-49c3-affe-023cd885e04b.png)
![ml resp](https://user-images.githubusercontent.com/77791586/182402932-4afd14fe-5f57-4b03-b0a6-1c6b74474015.png)

# 5. TroubleShooting

If you have issues, reading is the first advice we can give you, most errors are easily understood just by reading the logs as almost all errors will be captured by a try / catch and logged.<br>

If you need to install a new module, or Python dependence, open a terminal inside the container and enter for example : "pip install new-module"<br>
To open a terminal there are many ways, 
- If you use the InterSystems plugins, you can click in the below bar in VSCode, the one looking like `docker:iris:52795[IRISAPP]` and select `Open Shell in Docker`.
- In any local terminal enter : `docker-compose exec -it iris bash`
- From Docker-Desktop find the IRIS container and click on `Open in terminal`

Some models may require some changes for the pipeline or the settings for example, it is your task to add in the settings and in the request the right information.


# 6. Conclusion
From here you should be able to use any model that you need or own on IRIS.<br>
**NOTE** that you can create a `Python.MLOperation` for each of your model and have them on at the same time. 
