import argparse
import logging
import sys
from pathlib import Path
from src.parser import XMLParser
from src.exporter import CSVExporter

# Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Herramienta profesional de conversión XML a CSV (Modo Batch)")
    parser.add_argument('--input', '-i', type=str, default='./data/input', help='Directorio de archivos XML de entrada')
    # CAMBIO: Ahora output es un directorio, no un archivo
    parser.add_argument('--output', '-o', type=str, default='./data/output', help='Directorio de destino para los archivos CSV')

    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    # Validaciones
    if not input_dir.exists():
        logger.error(f"El directorio de entrada {input_dir} no existe.")
        sys.exit(1)

    # Aseguramos que el directorio de salida exista
    output_dir.mkdir(parents=True, exist_ok=True)

    xml_parser = XMLParser()

    xml_files = list(input_dir.glob('*.xml'))
    if not xml_files:
        logger.warning(f"No se encontraron archivos XML en {input_dir}")
        return

    logger.info(f"Iniciando procesamiento de {len(xml_files)} archivos...")

    # Proceso 1 a 1
    for xml_file in xml_files:
        # 1. Parsear
        data = xml_parser.parse_file(xml_file)

        if not data:
            logger.warning(f"Saltando {xml_file.name} (sin datos o error de lectura)")
            continue

        # 2. Definir nombre de salida (mismo nombre, extensión .csv)
        # xml_file.stem obtiene el nombre sin extensión (ej: "factura_enero")
        output_filename = f"{xml_file.stem}.csv"
        final_output_path = output_dir / output_filename

        # 3. Exportar individualmente
        exporter = CSVExporter(final_output_path)
        exporter.export(data)

    logger.info("Proceso por lotes finalizado.")

if __name__ == "__main__":
    main()
