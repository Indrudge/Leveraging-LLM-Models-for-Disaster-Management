# Leveraging LLM Models for Disaster Management: Predicting Risks and Locating Help Centers

## Project Overview

This project aims to develop an intelligent disaster management system that utilizes Large Language Models (LLMs) to predict disaster risks and locate help centers in real-time. By collecting and analyzing data from various online sources, such as news websites and social media platforms, the system provides timely alerts, safety advice, and maps of affected areas, helping both the public and emergency responders during disaster situations.

## Features

- **Web Scraping**: Automatically collects data from news sites and social media for disaster-related keywords.
- **LLM-Based Analysis**: Analyzes the collected data to predict potential disasters and assess their severity.
- **Real-Time Alerts**: Provides safety advice and notifications to relevant authorities and the public.
- **Geospatial Mapping**: Maps affected areas, identifying nearby hospitals, safe zones, and escape routes.
- **Automated Reporting**: Generates reports for authorities, detailing the predicted disaster, affected areas, and recommended actions.

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Required Libraries
Install the required Python libraries using the following command:
```bash
pip install -r requirements.txt
```
### Directory Map
Make sure the files are in this perticular order 
```bash
disaster-management-LLM/
│
├── data/                   # Directory for collected raw data
├── models/                 # Trained LLM models
├── reports/                # Generated disaster reports
├── scripts/                # Web scraping, prediction, and mapping scripts
│   ├── scrape_data.py
│   ├── predict_disaster.py
│   └── generate_report.py
├── app.py                  # Main application script
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```
MIT License

Copyright (c) 2024 University of Petroleum and Energy Studies

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Acknowledgments

We would like to express our deepest gratitude to our mentor, Surender Varma Gadhiraju, whose guidance and support were instrumental in the successful completion of this project.

We also thank the University of Petroleum and Energy Studies for providing the necessary resources and an environment conducive to research and development.

Special thanks to the open-source community and the developers of the libraries and frameworks used in this project, including TensorFlow, PyTorch, Flask, and others.

Finally, we appreciate the efforts of all team members who contributed their time and expertise to make this project a reality. Your dedication and collaboration were key to the project's success.
