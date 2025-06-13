# 🔍 Data Scanner

A powerful and efficient data scanning tool built with Python for analyzing and extracting insights from various data sources.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Examples](#examples)
- [API Reference](#api-reference)
- [Contributing](#contributing)

## 🎯 Overview

Data Scanner is designed to help developers and data analysts quickly scan, analyze, and extract meaningful information from various data sources. Whether you're working with databases, CSV files, or API endpoints, this tool provides a unified interface for data exploration and analysis.

## ✨ Features

- 🗃️ **Multi-format Support** - Scan CSV, JSON, XML, and database files
- 🔒 **Security Scanning** - Detect sensitive data patterns (PII, credentials)
- 📊 **Data Profiling** - Generate statistical summaries and data quality reports
- 🚀 **High Performance** - Optimized for large datasets with parallel processing
- 🎨 **Rich Output** - Beautiful CLI output with progress bars and colored results
- 📈 **Export Options** - Export results to JSON, CSV, or HTML reports
- 🔧 **Configurable** - Flexible configuration options for different use cases

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install from source

```bash
# Clone the repository
git clone https://github.com/soorajsatheesan/data_scanner.git
cd data_scanner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Install dependencies

```bash
pip install pandas numpy click colorama tqdm
```

## 📖 Usage

### Basic Usage

```bash
# Scan a CSV file
python data_scanner.py --file data.csv

# Scan a directory
python data_scanner.py --directory /path/to/data

# Scan with specific patterns
python data_scanner.py --file data.csv --patterns email,phone,ssn
```

### Advanced Usage

```bash
# Generate detailed report
python data_scanner.py --file data.csv --output report.html --format html

# Scan with custom configuration
python data_scanner.py --config config.yaml --file data.csv

# Scan database
python data_scanner.py --database postgresql://user:pass@localhost/db
```

## ⚙️ Configuration

Create a `config.yaml` file to customize scanning behavior:

```yaml
# Scanner Configuration
scanner:
  chunk_size: 10000
  max_workers: 4
  timeout: 30

# Data patterns to detect
patterns:
  email: true
  phone: true
  ssn: true
  credit_card: false
  custom_patterns:
    - pattern: "\\b[A-Z]{2}\\d{6}\\b"
      name: "custom_id"

# Output settings
output:
  format: "json"  # json, csv, html
  include_samples: true
  max_samples: 5
```

## 💡 Examples

### Example 1: Basic File Scanning

```python
from data_scanner import DataScanner

# Initialize scanner
scanner = DataScanner()

# Scan a file
results = scanner.scan_file('data.csv')

# Print results
for finding in results:
    print(f"Found {finding.pattern} in column {finding.column}")
```

### Example 2: Database Scanning

```python
from data_scanner import DatabaseScanner

# Initialize database scanner
db_scanner = DatabaseScanner(
    connection_string="postgresql://user:pass@localhost/db"
)

# Scan specific tables
results = db_scanner.scan_tables(['users', 'orders'])

# Generate report
db_scanner.generate_report(results, 'database_report.html')
```

### Example 3: Directory Scanning

```python
from data_scanner import DirectoryScanner

# Scan all files in directory
dir_scanner = DirectoryScanner()
results = dir_scanner.scan_directory('/path/to/data', recursive=True)

# Filter results
sensitive_data = [r for r in results if r.sensitivity_level == 'HIGH']
```

## 📊 Sample Output

```
🔍 Data Scanner Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 File: customer_data.csv
┌─────────────────┬──────────────┬───────────┬─────────────┐
│ Pattern         │ Column       │ Matches   │ Sensitivity │
├─────────────────┼──────────────┼───────────┼─────────────┤
│ Email Address   │ email        │ 1,247     │ MEDIUM      │
│ Phone Number    │ phone        │ 1,198     │ MEDIUM      │
│ SSN             │ ssn          │ 1,247     │ HIGH        │
│ Credit Card     │ payment_info │ 23        │ HIGH        │
└─────────────────┴──────────────┴───────────┴─────────────┘

⚠️  High sensitivity data detected!
💡 Consider encrypting columns: ssn, payment_info
```

## 🔧 API Reference

### Core Classes

#### `DataScanner`
Main scanner class for file-based scanning.

```python
scanner = DataScanner(
    patterns=['email', 'phone'],
    chunk_size=10000,
    max_workers=4
)
```

#### `DatabaseScanner`
Scanner for database sources.

```python
db_scanner = DatabaseScanner(
    connection_string="postgresql://user:pass@localhost/db",
    sample_size=1000
)
```

### Methods

- `scan_file(filepath)` - Scan a single file
- `scan_directory(directory, recursive=True)` - Scan directory
- `generate_report(results, output_file)` - Generate HTML/JSON report
- `add_custom_pattern(pattern, name)` - Add custom regex pattern

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/soorajsatheesan/data_scanner.git
cd data_scanner

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linting
flake8 data_scanner/
black data_scanner/
```

## 🙏 Acknowledgments

- Built with ❤️ using Python
- Inspired by the need for better data governance and security
- Special thanks to the open-source community

<div align="center">
  <b>⭐ Star this repository if you find it helpful!</b>
</div>
