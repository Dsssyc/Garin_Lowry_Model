Garin_Lowry_Model
==
This repository is used to store codes about different ways to implement Garin-Lowry-Model-WPS, which is based on PyWPS. 

## Caution
All code files contain information about Soku's server, please modify them if you want to use it yourself.

## interface.py
[interface.py](https://github.com/Dsssyc/Garin_Lowry_Model/blob/master/interface.py) is a module containing functions which may be similar in files named garin_lowry_x。<br>
You can also use this script to create XML request files.<br>
<b>Do not upload interface.py into the `processes` folder</b><br>

## garin_Lory_x.py
These files include different means to implement Garin-Lowry Model, which must have support from interface.py.<br>
>Means contain:
>>LiteralData
>>>[String](https://github.com/Dsssyc/Garin_Lowry_Model/blob/master/garin_lowry_literal.py)

>>ComplexData
>>>[Text/Plain](https://github.com/Dsssyc/Garin_Lowry_Model/blob/master/garin_lowry_text.py)<br>
>>>[Json](https://github.com/Dsssyc/Garin_Lowry_Model/blob/master/garin_lowry_json.py)
            
&
==
Thanks for `PyWPS`: https://pywps.org/<br>


My `Blog`: https://www.dsssyc.xin
