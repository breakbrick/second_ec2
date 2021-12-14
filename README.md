# EvidenceProtect-datalake

## Description

Datalake VM for Evidence Protect is to securely store the hash values obtained from the Parent EC2 instance (Nitro Enclave instance).

## Installation

1. Launch and SSH into your EC2 instance.

2. Install Samba service on Datalake VM.

## Usage

1. Install all the required python modules provided in `evidenceprotect-datalake/requirements.txt` file.

```
pip3 install -r requirements.txt
```

2. Run the `dirwatch.py` script in `evidenceprotect-datalake/`.

```
python3 dirwatch.py
```