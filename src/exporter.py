import csv
from pathlib import Path
from typing import List
from .models import LecturaPropiedad
import logging

logger = logging.getLogger(__name__)

class CSVExporter:
    def __init__(self, output_path: Path, delimiter: str = ';'):
        self.output_path = output_path
        self.delimiter = delimiter
        # Definimos el orden de columnas basado en el dataclass
        self.headers = [field for field in LecturaPropiedad.__annotations__.keys()]

    def export(self, data: List[LecturaPropiedad]):
        if not data:
            logger.warning("No hay datos para exportar.")
            return

        try:
            # encoding='utf-8-sig' ayuda a Excel a reconocer caracteres latinos correctamente
            with open(self.output_path, mode='w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=self.delimiter)

                # Escribir cabecera (nombres de campos formateados)
                writer.writerow([h.replace('_', ' ').title() for h in self.headers])

                # Escribir filas
                for item in data:
                    # dataclasses.astuple no se usa directo para mantener control del orden si cambiamos algo
                    row = [getattr(item, field) for field in self.headers]
                    writer.writerow(row)

            logger.info(f"Exportación exitosa: {self.output_path} ({len(data)} registros)")

        except IOError as e:
            logger.error(f"Error escribiendo CSV: {e}")
