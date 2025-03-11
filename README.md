# Web3 Security Scanner

An AI-powered security analysis platform for detecting vulnerabilities in blockchain applications and smart contracts.

## Features (Planned)

- AI-powered vulnerability detection for smart contracts
- Integration with GitHub repositories
- Detailed security reports with remediation suggestions
- Support for Solidity, Vyper, and other blockchain languages
- CLI tool for local scanning

## Development Status

This project is in early development. Current focus:

- Building the core LLM-based analysis pipeline
- Implementing basic vulnerability detection for common issues
- Creating initial GitHub integration
- Developing prototype dashboard

## Getting Started

### Prerequisites

- Python 3.10+
- Docker and Docker Compose (optional)

### Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env`
4. Run the development server: `uvicorn src.api.main:app --reload`

## License

[MIT/Apache 2.0] - See LICENSE file for details