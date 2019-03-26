import os
import shutil
import sys
sys.path.append('/PyWeb/PyWPS-Extension/garin-lowry/')

import interface
from pywps import FORMATS, ComplexInput, ComplexOutput, Format, Process


__author__ = 'Soku'

class Garin_Lowry_T(Process):
    def __init__(self):
        inputs = [ComplexInput(
            'odtime', 
            'Input odtime', 
            supported_formats=[Format('text/plain', extension='.txt')]
            )]

        outputs = [ComplexOutput(
            'result',
            'Output result', 
            supported_formats=[Format('text/plain', extension='.txt')]
            )]

        super(Garin_Lowry_T, self).__init__(
            self._handler,
            identifier='garin-lowry-t',
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

        filepath = request.inputs['odtime'][0].file
        shutil.move(filepath, interface._dir+'odtime.prn')

        command = interface.createCommand()
        os.system(command)

        response.outputs['result'].output_format = FORMATS.TEXT
        response.outputs['result'].file= interface._dir + interface.result    
        return response
