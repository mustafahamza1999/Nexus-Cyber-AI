# Nexus Cyber AI

A web-based multi-agent AI platform designed for Static Application Security Testing (SAST), automated vulnerability detection, performance analysis, and automated forensic PDF reporting.

## Key Features
- **Multi-Agent AI Architecture:** Coordinates specialized agents using LangGraph workflows to inspect code, identify potential vulnerabilities, and analyze performance.
- **Automated Reporting:** Generates structured outputs and forensic PDF reports.
- **Web Interface:** Includes a FastAPI backend and a web frontend under `static/`.

## API Key Requirement
Scanning and analysis require a valid `GROQ_API_KEY`. Copy `.env.example` to `.env` and add your own API key before running the application:

    GROQ_API_KEY=your_actual_api_key_here

## Setup & Usage
1. Clone the repository:

    git clone https://github.com/mustafahamza1999/Nexus-Cyber-AI.git
    cd Nexus-Cyber-AI

2. Install dependencies:

    pip install -r requirements.txt

3. Create a `.env` file with your `GROQ_API_KEY` and start the server.

## Disclaimer
For authorized security analysis, code quality review, and educational use.