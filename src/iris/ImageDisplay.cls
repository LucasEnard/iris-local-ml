/* Copyright (c) 2021 by InterSystems Corporation.
   Cambridge, Massachusetts, U.S.A.  All rights reserved.
   Confidential property of InterSystems Corporation. */

Class PEX.Msg.ImageDisplay Extends (Ens.MessageBody, %CSP.Page, %XML.Adaptor)
{

Property Base64Image As %Stream.GlobalCharacter;

Property BinaryImage As %Stream.GlobalBinary;

/// This method is called by the Management Portal to determine the content type that will be returned by the <method>%ShowContents</method> method.
/// The return value is a string containing an HTTP content type.
Method %GetContentType() As %String
{
	Quit "text/html"
}

/// This method is called by the Management Portal to display a message-specific content viewer.<br>
/// This method displays its content by writing out to the current device.
/// The content should match the type returned by the <method>%GetContentType</method> method.<br>
Method %ShowContents(pZenOutput As %Boolean = 0)
{
	set MaxStringLength = 3640044
	if ..Base64Image.Size > 0 {
		&html<<div>Base64Image<div>>
		&html<<img src="data:image/jpeg;base64,#(..Base64Image.Read(MaxStringLength))#" width="100%">>
	}
	if ..BinaryImage.Size >0 {
		&html<<div>BinaryImage<div>>
		&html<<img src="%25CSP.StreamServer.cls?STREAMOID=#(..Encrypt(..BinaryImage.%Oid()))#" width="100%">>
	}
}

Storage Default
{
<Data name="MessageDefaultData">
<Subscript>"Message"</Subscript>
<Value name="1">
<Value>Base64Image</Value>
</Value>
<Value name="2">
<Value>BinaryImage</Value>
</Value>
</Data>
<DefaultData>MessageDefaultData</DefaultData>
<Type>%Storage.Persistent</Type>
}

}
