import unittest
from unittest.mock import patch, MagicMock
import xml.etree.ElementTree as ET
from src.parser import XMLParser

# XML simulado
MOCK_XML_CONTENT = """<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.008.001.02">
    <cabecera>
        <codcomunidad>001</codcomunidad>
        <comunidad>TEST COMUNIDAD</comunidad>
    </cabecera>
    <body>
        <propiedad>
            <propiedad_codigo>01</propiedad_codigo>
            <propiedad_nombre>BAJO DER</propiedad_nombre>
            <propietario_nombre>JUAN TEST</propietario_nombre>
            <lectura_ant>100</lectura_ant>
            <lectura_act>110</lectura_act>
            <consumo>10</consumo>
            <importe_total>20,50</importe_total>
        </propiedad>
    </body>
</Document>
"""

class TestXMLParser(unittest.TestCase):
    def test_parsing_logic(self):
        parser = XMLParser()

        # Mockeamos ET.parse para no necesitar ficheros reales
        with patch('xml.etree.ElementTree.parse') as mock_parse:
            # Corregido: creamos el elemento directamente desde el string
            root = ET.fromstring(MOCK_XML_CONTENT)

            mock_tree = MagicMock()
            mock_tree.getroot.return_value = root
            mock_parse.return_value = mock_tree

            # Ejecutamos con una ruta falsa
            path = MagicMock()
            path.exists.return_value = True
            path.name = "test.xml"

            resultados = parser.parse_file(path)

            self.assertEqual(len(resultados), 1)
            self.assertEqual(resultados[0].cod_comunidad, "001")
            self.assertEqual(resultados[0].consumo, 10)
            self.assertEqual(resultados[0].importe_total, "20,50")

if __name__ == '__main__':
    unittest.main()
