Class iris.Production Extends Ens.Production
{

XData ProductionDefinition
{
<Production Name="iris.Production" TestingEnabled="true" LogGeneralTraceEvents="false">
  <Description></Description>
  <ActorPoolSize>2</ActorPoolSize>
  <Item Name="Python.HFOperation" Category="" ClassName="Python.HFOperation" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="%settings"></Setting>
  </Item>
  <Item Name="Python.MLOperation" Category="" ClassName="Python.MLOperation" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="%settings">name=gpt2
model_url=https://huggingface.co/gpt2
task=text-generation</Setting>
  </Item>
  <Item Name="Python.MLOperation2" Category="" ClassName="Python.MLOperation" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="%settings">name=camembert-ner
model_url=https://huggingface.co/Jean-Baptiste/camembert-ner
task=ner</Setting>
  </Item>
  <Item Name="Python.MLOperation3" Category="" ClassName="Python.MLOperation" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="%settings">name=bert-base-uncased
model_url=https://huggingface.co/bert-base-uncased
task=fill-mask</Setting>
  </Item>
</Production>
}

}
