import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List
import logging
from .models import LecturaPropiedad

logger = logging.getLogger(__name__)

class XMLParser:
    def __init__(self):
        # Namespace extraído de tu archivo
        self.namespaces = {'ns': 'urn:iso:std:iso:20022:tech:xsd:pain.008.001.02'}

    def _get_text(self, element: ET.Element, tag: str) -> str:
        """Helper seguro para extraer texto manejando namespaces."""
        node = element.find(f"ns:{tag}", self.namespaces)
        return node.text.strip() if node is not None and node.text else ""

    def parse_file(self, file_path: Path) -> List[LecturaPropiedad]:
        """Procesa un archivo XML y devuelve una lista de objetos LecturaPropiedad."""
        if not file_path.exists():
            logger.error(f"El archivo {file_path} no existe.")
            return []

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Datos de Cabecera
            cabecera = root.find('ns:cabecera', self.namespaces)
            cod_comunidad = self._get_text(cabecera, 'codcomunidad')
            nombre_comunidad = self._get_text(cabecera, 'comunidad')

            resultados = []

            # Iterar Propiedades
            body = root.find('ns:body', self.namespaces)
            if body is None:
                logger.warning(f"No se encontró body en {file_path.name}")
                return []

            for prop in body.findall('ns:propiedad', self.namespaces):
                try:
                    lectura = LecturaPropiedad(
                        archivo_origen=file_path.name,
                        cod_comunidad=cod_comunidad,
                        nombre_comunidad=nombre_comunidad,
                        propiedad_codigo=self._get_text(prop, 'propiedad_codigo'),
                        propiedad_nombre=self._get_text(prop, 'propiedad_nombre'),
                        propietario=self._get_text(prop, 'propietario_nombre'),
                        lectura_ant=int(self._get_text(prop, 'lectura_ant') or 0),
                        lectura_act=int(self._get_text(prop, 'lectura_act') or 0),
                        consumo=int(self._get_text(prop, 'consumo') or 0),
                        importe_total=self._get_text(prop, 'importe_total')
                    )
                    resultados.append(lectura)
                except ValueError as ve:
                    logger.error(f"Error de conversión de datos en {file_path.name}: {ve}")

            return resultados

        except ET.ParseError as e:
            logger.error(f"Error parseando XML {file_path.name}: {e}")
            return []
