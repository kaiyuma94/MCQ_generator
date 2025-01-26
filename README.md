```markdown
# MCQ Question Standardizer

## Overview
A Python application that processes Multiple Choice Questions (MCQ) from Excel files using GPT-4o-mini to improve and standardize question format and clarity. The tool reads Excel files containing MCQs, processes them through a standardized prompt, and outputs improved versions in a new Excel file.

## Features
- Batch processing of Excel files
- Automatic standardization of question format
- Error handling and logging
- Progress tracking
- Configurable processing parameters

## Installation
1. Clone the repository:
```bash
git clone https://github.com/kaiyuma94/MCQ_generator.git
cd MCQ_generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the application:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to `.env`
   - Adjust settings in `config/config.yml` if needed

## Usage
1. Place your Excel files in the `data/input` directory
2. Run the application:
```bash
python main.py
```
3. Find processed files in `data/output` directory with prefix "processed_"

## Input File Format
Excel files should have the following columns:
- Question
- A (Option A)
- B (Option B)
- C (Option C)
- D (Option D)

## Project Structure
```
MCQ_generator/
├── data/
│   ├── input/
│   └── output/
├── modules/
│   ├── input_handler.py
│   ├── question_processor.py
│   ├── output_generator.py
│   ├── logger.py
│   └── config_manager.py
├── config/
│   └── config.yml
├── logs/
├── main.py
└── requirements.txt
```

## Configuration
Edit `config/config.yml` to modify:
- OpenAI API settings
- Processing batch size
- Retry settings
- Logging configuration
- Input/Output paths

## Error Handling
- Logs are stored in `logs/processing.log`
- The application handles:
  - File not found errors
  - API failures
  - Parse errors
  - Invalid input formats

## Requirements
See `requirements.txt` for a complete list of dependencies.
