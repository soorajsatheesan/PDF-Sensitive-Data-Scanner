# 🔍 PDF Sensitive Data Scanner

A Flask-based web application that scans PDF documents for sensitive information including PII (Personally Identifiable Information), PHI (Protected Health Information), and PCI (Payment Card Information). The application extracts text from PDFs, identifies sensitive data patterns using regex, and stores results in a PostgreSQL database.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Detected Patterns](#detected-patterns)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Contributing](#contributing)

## 🎯 Overview

PDF Sensitive Data Scanner is a web application designed to help organizations identify and classify sensitive information in PDF documents. It automatically detects various types of sensitive data including government IDs, medical records, financial information, and contact details. This tool is particularly useful for compliance audits, data privacy assessments, and security reviews.

## ✨ Features

- 📄 **PDF Text Extraction** - Extracts text from PDF files using PyPDF2
- 🔒 **Sensitive Data Detection** - Identifies PII, PHI, PCI, and other sensitive information
- 🗄️ **Database Storage** - Stores scan results in PostgreSQL for tracking and auditing
- 🌐 **RESTful API** - Clean API endpoints for file upload, result retrieval, and management
- 🎨 **Web Interface** - Simple HTML frontend for easy file upload and result viewing
- 📊 **Data Classification** - Automatically classifies detected data (PII, PHI, PCI, etc.)
- 🔍 **Multiple Pattern Detection** - Supports detection of PAN, SSN, Passport, Aadhaar, Credit Cards, Medical Records, and more

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database (local or remote)
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
```

### Database Setup

1. Create a PostgreSQL database (or use an existing one)
2. Update the `DATABASE_URL` in `db.py` with your database credentials:

```python
DATABASE_URL = "postgresql://username:password@host:port/database_name"
```

The application will automatically create the required table on first run.

## 📖 Usage

### Running the Application

```bash
# Start the Flask server
python app.py
```

The application will start on `http://0.0.0.0:5000` (or the port specified in the `PORT` environment variable).

### Using the Web Interface

1. Open `index.html` in your browser (or serve it through the Flask app)
2. Click "Choose File" and select a PDF document
3. Click "Upload and Scan"
4. View the detected sensitive data in the results section

### Using the API

#### Upload and Scan a PDF

```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@document.pdf"
```

Response:
```json
{
  "message": "File processed successfully",
  "results": [
    {
      "type": "Email",
      "value": "user@example.com",
      "classification": "Contact Information"
    },
    {
      "type": "SSN",
      "value": "123-45-6789",
      "classification": "PII"
    }
  ]
}
```

#### Get All Scan Results

```bash
curl http://localhost:5000/results
```

#### Get Results for a Specific File

```bash
curl http://localhost:5000/results?file_name=document.pdf
```

#### Delete Scan Results

```bash
curl -X DELETE http://localhost:5000/delete?file_name=document.pdf
```

#### Health Check

```bash
curl http://localhost:5000/health
```

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload` | POST | Upload a PDF file and scan for sensitive data |
| `/results` | GET | Retrieve scan results (all or filtered by filename) |
| `/delete` | DELETE | Delete scan results for a specific file |
| `/health` | GET | Health check endpoint |

## 🔍 Detected Patterns

The scanner detects the following types of sensitive information:

### Government IDs
- **PAN** (Permanent Account Number) - Indian tax ID
- **SSN** (Social Security Number) - US Social Security Number
- **Passport** - Passport numbers (various formats)
- **Aadhaar** - Indian unique identification number

### Medical Information
- **Medical Record Numbers (MRN)**
- **Medical Test Results** - Detects test result keywords
- **Diagnosis** - Common medical conditions
- **Health Insurance Numbers (HIN)**

### Financial Information
- **Credit Card Numbers** - Detects credit card patterns

### Contact Information
- **Email Addresses**

All detected data is automatically classified as:
- **PII** - Personally Identifiable Information
- **PHI** - Protected Health Information
- **PCI** - Payment Card Information
- **Contact Information**
- **Insurance Information**

## 📁 Project Structure

```
data_scanner/
├── app.py              # Flask application and API endpoints
├── utils.py            # Text extraction and scanning logic
├── models.py           # Database operations (CRUD)
├── db.py               # Database connection and initialization
├── index.html          # Web frontend interface
├── requirements.txt    # Python dependencies
├── uploads/            # Directory for uploaded PDF files
└── README.md           # This file
```

## ⚙️ Configuration

### Environment Variables

- `PORT` - Port number for the Flask server (default: 5000)

### Database Configuration

Update the `DATABASE_URL` in `db.py`:

```python
DATABASE_URL = "postgresql://user:password@host:port/database"
```

### Adding Custom Patterns

To add custom detection patterns, edit `utils.py` and add to the `PATTERNS` dictionary:

```python
PATTERNS = {
    "Custom Pattern": r"your_regex_pattern_here",
    # ... existing patterns
}
```

## 🛠️ Technologies Used

- **Flask** - Web framework
- **PyPDF2** - PDF text extraction
- **PostgreSQL** - Database for storing scan results
- **psycopg2** - PostgreSQL adapter for Python
- **Flask-CORS** - Cross-origin resource sharing support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.
