# ip eye

ip eye is an OSINT-based IP tracking and reconnaissance tool designed for educational and defensive security research.

## Features

- IP geolocation lookup (ipinfo.io)
- Multi-threaded port scanner
- DNS lookup
- Reverse DNS lookup
- WHOIS lookup
- Shodan integration
- Report generation
- Configurable API keys
- CLI interface with ASCII banner

## Requirements

- Python 3.8+

## Installation

Clone the repository:

```bash
git clone https://github.com/n0merc/ip-eye.git
cd ip-eye
Install dependencies:

pip install -r requirements.txt
Usage
Run directly:

python ip_eye.py
If installed via setup.py:

ip-eye
Menu
Track IP

Port Scan

DNS Lookup

Reverse DNS

WHOIS Lookup

Shodan Search

Set API Key

Exit

Configuration
API keys are stored in config.json.

Example:

{
    "shodan": ""
}
Shodan API key can be obtained from:
https://account.shodan.io/

Reports
Reports are saved as:

ip_eye_report_<IP>_<TIMESTAMP>.txt
Disclaimer
This tool is intended for educational, OSINT, and defensive security purposes only.

The author is not responsible for misuse or illegal use of this software.

Author
n0merc

License
MIT License


---

##  `requirements.txt`

```txt
requests
colorama
dnspython
python-whois
shodan
