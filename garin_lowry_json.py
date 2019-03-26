import sys
sys.path.append('/PyWeb/PyWPS-Extension/garin-lowry/')
import interface
import os
import json
from lxml import etree
from pywps import Process, ComplexInput, \
    ComplexOutput, Format, FORMATS

__author__ = 'Soku'

class Garin_Lowry_J(Process):
    def __init__(self):
        inputs = [ComplexInput(
            'odtime', 
            'Input odtime', 
            supported_formats=[Format('application/json', extension='.json')]
            )]

        outputs = [ComplexOutput(
            'result',
            'Output result', 
            supported_formats=[Format('text/plain', extension='.txt')]
            )]

        super(Garin_Lowry_J, self).__init__(
            self._handler,
            identifier='garin-lowry-j',
            title='Garin-Lowry Model',
            abstract='''Use the Json data format to upload data. 
            The data format is like 
            {
                "line 1": 
                {
                    "StartPoint": "1", 
                    "EndPoint": "1", 
                    "Distance": "0.31415"
                }
            }''',
            version='1.0',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        interface.removeFile(interface.status, 1)
        interface.removeFile(interface.result, 1)
        interface.removeFile(interface.data, 1)

        filepath = request.inputs['odtime'][0].file
        with open(filepath, 'r') as file:
            odtime = json.load(file)

        lines = ''
        index = 1
        while index <= len(odtime):
            content = odtime['line {}'.format(str(index))]
            lines += content['StartPoint'] + '  ' \
                    + content['EndPoint'] + '  ' \
                    + content['Distance'] + '  ' + '\n'
            index += 1
        
        file = open(interface._dir+'odtime.prn', 'w', encoding='utf-8')
        file.write(lines)
        file.close()

        command = interface.createCommand()
        os.system(command)

        response.outputs['result'].output_format = FORMATS.TEXT
        response.outputs['result'].file= interface._dir + interface.result
        return response
