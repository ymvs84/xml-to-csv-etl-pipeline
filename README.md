# XML to CSV Data Pipeline (Utility Consumption)

## 📋 Overview

This project is a robust **ETL (Extract, Transform, Load)** utility designed to process batch XML files containing real estate utility consumption data. It parses complex ISO-standard XML structures, normalizes hierarchical data into a flat format, and exports it for integration with legacy ERP systems or data analysis tools.

Built with **Python 3.10+**, it emphasizes **Separation of Concerns (SoC)**, strict type hinting, and production-grade error handling.

## 🚀 Key Features

  * [cite_start]**Namespace Aware:** Automatically handles complex XML namespaces (ISO 20022 standards) [cite: 1] without hardcoding fragility.
  * [cite_start]**Data Normalization:** Flattens hierarchical XML structures, merging header data (Community Code/Name) [cite: 1, 2] [cite_start]with individual property records [cite: 3, 4] for relational integrity.
  * [cite_start]**Localization Support:** Handles European number formats (comma decimals like `36,55` [cite: 3]) and generates CSVs compatible with Excel/Spanish locales (semicolon delimiters).
  * **Type Safety:** Uses Python `dataclasses` and type hints to ensure data consistency throughout the pipeline.
  * **Resilience:** Detailed logging system and fault tolerance—one corrupt file does not stop the entire batch process.

## 🏗 Architecture

The project follows a modular architecture to ensure testability and scalability:

1.  **Model Layer (`src/models.py`):** Defines the data contract (DTOs) using immutable `dataclasses`.
2.  **Parser Layer (`src/parser.py`):** Encapsulates the `xml.etree` logic and namespace resolution. Isolate changes in the XML schema here.
3.  **Exporter Layer (`src/exporter.py`):** Handles file I/O, encoding (`utf-8-sig`), and CSV formatting rules.
4.  **Orchestrator (`main.py`):** CLI entry point that manages the workflow and arguments.

## 📂 Project Structure

```text
xml-to-csv-converter/
├── data/
│   ├── input/         # Drop raw XML files here
│   └── output/        # Generated CSV files land here
├── src/
│   ├── __init__.py
│   ├── models.py      # Data Transfer Objects (DTO)
│   ├── parser.py      # XML Parsing Logic & Namespace handling
│   └── exporter.py    # CSV Writing Logic
├── tests/             # Unit tests
├── main.py            # CLI Entry Point
├── requirements.txt   # Dependencies
└── README.md          # Documentation
```

## 🛠️ Installation & Requirements

  * Python 3.10 or higher.
  * Standard library only (no heavy external dependencies required), maximizing portability.

<!-- end list -->

```bash
# Clone the repository
git clone https://github.com/your-username/xml-consumption-parser.git

# Navigate to directory
cd xml-consumption-parser
```

## 💻 Usage

The tool is designed with a CLI interface for easy integration into cron jobs or shell scripts.

**Basic Run (Default directories):**

```bash
python main.py
```

**Custom Input/Output Paths:**

```bash
python main.py --input "/var/data/xml_imports" --output "./report_2024.csv"
```

**Help Command:**

```bash
python main.py --help
```

## 🔍 Technical Details

### 1\. Handling XML Namespaces

[cite_start]The source documents use a specific URN namespace (`urn:iso:std:iso:20022...`)[cite: 1]. The `XMLParser` class isolates this complexity. Instead of stripping namespaces (which can be risky), we map them properly, ensuring the parser validates against the correct schema definitions.

### 2\. Decimal & CSV Delimiters

[cite_start]The input data uses comma-separated decimals (e.g., `<importe_total>36,55</importe_total>` [cite: 3]).

  * **Problem:** Standard CSVs use commas as delimiters, which splits the value `36,55` into two columns.
  * [cite_start]**Solution:** The exporter defaults to a semicolon (`;`) delimiter, standard for European CSV formats, ensuring values like `47,15` [cite: 6] [cite_start]or `19,2` [cite: 5] remain intact.

### 3\. Encoding

Outputs are encoded in `utf-8-sig` (UTF-8 with BOM). [cite_start]This ensures that characters in names like "MASCUNANO" [cite: 5] [cite_start]or "GONZALEZ" [cite: 7] render correctly when opened directly in Microsoft Excel on Windows.

## 🧪 Testing

The project includes unit tests for the parsing logic.

```bash
# Run tests using unittest
python -m unittest discover tests

# OR using pytest (if installed)
pytest
```

## 👤 Author

**[Yago Menéndez de la Vega]**
*Software Engineer*
Specialist in Backend Development & Data Integration.

-----

*Note: This project serves as a demonstration of clean code practices, utilizing Python's standard library for efficient XML processing.*
