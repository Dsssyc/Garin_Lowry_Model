import os
import sys
sys.path.append('/PyWeb/PyWPS-Extension/garin-lowry/')

import interface
from pywps import FORMATS, ComplexOutput, Format, LiteralInput, Process


__author__ = 'Soku'

class Garin_Lowry_L(Process):
    def __init__(self):
        inputs = [LiteralInput(
            'odtime', 
            'Input odtime', 
            data_type='string'
            )]
        outputs = [ComplexOutput(
            'result',
            'Output result', 
            supported_formats=[Format('text/plain', extension='.txt')]
            )]

        super(Garin_Lowry_L, self).__init__(
            self._handler,
            identifier='garin-lowry-l',
            title='Garin-Lowry Model',
            abstract='''Embed the data as LiteralData into the XML. 
            Each line needs to input the starting number, 
            the ending number and the distance 
            between the two points in order. 
            Two spaces are required after each value.''',
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

        content = request.inputs['odtime'][0].data
        file = open(interface._dir+'odtime.prn', 'w', encoding='utf-8')
        file.write(content)
        file.close()

        command = interface.createCommand()
        os.system(command)

        response.outputs['result'].output_format = FORMATS.TEXT
        response.outputs['result'].file= interface._dir + interface.result
        return response
