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
- [5. Conclusion](#5-conclusion)

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
purpose=text-generation
```
Here, `purpose` takes as an argument the `TASK` or the `PURPOSE` of your model.

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
Now you can click on `Visual Trace` to see in details what happened and see the logs.


## 4.2. SECOND CASE : YOU WANT TO DOWNLOAD A MODEL FROM HUGGINGFACE
In this case, you must find the URL of the model on HuggingFace;

From here you must go to the parameters of the `Python.MLOperation`.<br>
Click on the `Python.MLOperation` then go to `settings` in the right tab, then in the `Python` part, then in the `%settings` part.
Here, you can enter or modify any parameters ( don't forget to press `apply` once your are done ).<br>
Here's an example configuration for this case :<br>
%settings
```
model_url=https://huggingface.co/gpt2
name=gpt2
purpose=text-generation
```
Here, `purpose` takes as an argument the `TASK` or the `PURPOSE` of your model.

Now you can double-click on the operation `Python.MLOperation` and `start` it.<br>
**You must see in the `Log` part the starting of your model and the downloading.**<br>
**NOTE** You can refresh those logs every x seconds to see the advancement with the downloads.

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
Now you can click on `Visual Trace` to see in details what happened and see the logs.

**NOTE** that once the model was downloaded once, the production won't download it again but get the cached files found at `src/model/TheModelName/`.<br>
If some files are missing, the Production will download them again.

# 5. Conclusion
From here you should be able to use any model that you need or own on IRIS.<br>
**NOTE** that you can create a `Python.MLOperation` for each of your model and have them on at the same time. 
