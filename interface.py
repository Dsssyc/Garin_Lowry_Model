import json
import os
import sys

from lxml import etree

_dir = sys.path[0] + '/EXE/'
data = 'odtime.prn'
status = 'status.log'
result = 'Basic.TXT'

# _dir = '/PyWeb/PyWPS-Extension/garin-lowry/EXE/'

NSMAP = {
    None: 'http://www.opengis.net/wps/1.0.0',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'wfs': 'http://www.opengis.net/wfs',
    'wps': 'http://www.opengis.net/wps/1.0.0',
    'ows': 'http://www.opengis.net/ows/1.1',
    'gml': 'http://www.opengis.net/gml',
    'ogc': 'http://www.opengis.net/ogc',
    'wcs': 'http://www.opengis.net/wcs/1.1.1',
    'xlink': 'http://www.w3.org/1999/xlink',
    'json': 'https://www.json.org/',
    'text': 'https://www.w3.org/Protocols/rfc1341/7_1_Text.html'
}

def removeFile(filename, _bool=1):
    filepath = _dir + filename
    if os.path.exists(filepath) and _bool:
        os.remove(filepath)

def createCommand():
    command = 'cd ' + _dir + '&&wine simucity.exe'
    return command

def readFile(filename, _format='read'):
    filepath = _dir + filename
    file = open(filepath, 'r', encoding='utf-8')
    if _format == 'read':
        content = file.read()
    
    if _format == 'readlines':
        content = file.readlines()
    
    file.close()
    return content

def createLiteralData(filename, parent_element):
    content = readFile(filename, 'read')
    parent_element.text = content
    
def createComplexData(filename, parent_element, _format='text'):
    if _format == 'text':
        content = readFile(filename, 'read')
        parent_element.text = content

    if _format == 'json':
        lines = readFile(filename, 'readlines')
        index = 1
        _dict = {}
        for line in lines:
            elements = line.split('  ')
            info = {
                'StartPoint': elements[0],
                'EndPoint': elements[1],
                'Distance': elements[2]
            }
            del elements[3]

            _dict['line {}'.format(str(index))] = info
            index += 1
        parent_element.text = json.dumps(_dict)

def createXML(filename, means='Text'):
    execute = etree.Element(
        etree.QName(NSMAP['wps'], 'Execute'), 
        nsmap=NSMAP,
        attrib={
            'version': '1.0.0',
            'service': 'WPS'
        }
    )

    identifier = etree.SubElement(
        execute,
        etree.QName(NSMAP['ows'], 'Identifier')
    )
    if means == 'LiteralData':
        identifier.text = 'garin-lowry-l'
    if means == 'Json':
        identifier.text = 'garin-lowry-j'
    if means == 'Text':
        identifier.text = 'garin-lowry-t'
        

    dataInputs = etree.SubElement(
        execute,
        etree.QName(NSMAP['wps'], 'DataInputs')
    )

    _input = etree.SubElement(
        dataInputs,
        etree.QName(NSMAP['wps'], 'Input')
    )

    var_identifier = etree.SubElement(
        _input,
        etree.QName(NSMAP['ows'], 'Identifier')
    )
    var_identifier.text = 'odtime'

    data = etree.SubElement(
        _input,
        etree.QName(NSMAP['wps'], 'Data')
    )

    if means == 'LiteralData':
        literalData = etree.SubElement(
            data,
            etree.QName(NSMAP['wps'], 'LiteralData')
        )
        createLiteralData(filename, literalData)

    if means == 'Json':
        complexData = etree.SubElement(
            data,
            etree.QName(NSMAP['wps'], 'ComplexData')
        )
        createComplexData(filename, complexData, 'json')
    
    if means == 'Text':
        complexData = etree.SubElement(
            data,
            etree.QName(NSMAP['wps'], 'ComplexData')
        )
        createComplexData(filename, complexData, 'text')
    
    responseForm = etree.SubElement(
        execute,
        etree.QName(NSMAP['wps'], 'ResponseForm')
    )

    rawDataOutput = etree.SubElement(
        responseForm,
        etree.QName(NSMAP['wps'], 'RawDataOutput'),
        attrib={
            'mimeType': 'text/xml',
            'subtype': 'gml/3.1.1'
        }
    )

    out_identifier = etree.SubElement(
        rawDataOutput,
        etree.QName(NSMAP['ows'], 'Identifier')
    )
    out_identifier.text = 'result'

    tree = etree.ElementTree(execute)
    tree.write('Request/GL_{}.xml'.format(means), pretty_print=True, xml_declaration=True, encoding='utf-8')

if __name__ == '__main__':
    means = ['LiteralData', 'Json', 'Text']
    for mean in means:
        createXML('odtime.prn', mean)
    
    print('____OK!____')
