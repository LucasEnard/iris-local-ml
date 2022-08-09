Class iris.Production Extends Ens.Production
{

XData ProductionDefinition
{
<Production Name="iris.Production" TestingEnabled="true" LogGeneralTraceEvents="false">
  <Description></Description>
  <ActorPoolSize>2</ActorPoolSize>
  <Item Name="HuggingFace API" Category="" ClassName="Python.HFOperation" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="%settings"></Setting>
  </Item>
  <Item Name="HuggingFace gpt2 local" Category="" ClassName="Python.MLOperation" PoolSize="1" Enabled="false" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="%settings">name=gpt2
model_url=https://huggingface.co/gpt2
task=text-generation</Setting>
  </Item>
  <Item Name="HuggingFace ner local" Category="" ClassName="Python.MLOperation" PoolSize="1" Enabled="false" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="%settings">name=camembert-ner
model_url=https://huggingface.co/Jean-Baptiste/camembert-ner
task=ner
aggregation_strategy=simple</Setting>
  </Item>
  <Item Name="HuggingFace bert local" Category="" ClassName="Python.MLOperation" PoolSize="1" Enabled="false" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="%settings">name=bert-base-uncased
model_url=https://huggingface.co/bert-base-uncased
task=fill-mask</Setting>
  </Item>
  <Item Name="HuggingFace Image resnet local" Category="" ClassName="Python.MLOperation" PoolSize="1" Enabled="false" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="%settings">name=detr-resnet-50
model_url=https://huggingface.co/facebook/detr-resnet-50
task=object-detection</Setting>
  </Item>
  <Item Name="HuggingFace Image panoptic local" Category="" ClassName="Python.MLOperation" PoolSize="1" Enabled="false" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="%settings">name=detr-resnet-50-panoptic
model_url=https://huggingface.co/facebook/detr-resnet-50-panoptic
task=image-segmentation</Setting>
  </Item>
</Production>
}

}
