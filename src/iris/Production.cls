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
  <Item Name="en-HealthSea SpaCy" Category="" ClassName="Python.SpacyOperation" PoolSize="1" Enabled="false" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="%settings">name=en_healthsea
model_url=https://huggingface.co/explosion/en_healthsea</Setting>
  </Item>
  <Item Name="Python.FlaskService" Category="" ClassName="Python.FlaskService" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
  </Item>
  <Item Name="Python.CrudPerson" Category="" ClassName="Python.CrudPerson" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
  </Item>
</Production>
}

}
