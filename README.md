# Datadog Webhook To Snmp
The concept behind this was the need to convert the Webhook payload (JSON) from a Datadog alert into an SNMP Trap that can be sent to a Trap Receiver.

## Overview
You will find one file `snmpTrap.py` which requires a few libraries (pysnmp & flask).  As long as you have these libraries installed on the server (install via `pip install X` command) you should be able to run this webservice which will expose the `webhook` endpoint, allow incoming JSON via http POST, and parse the JSON body.

## To Run Flask
1. Install Flask via `pip3 install Flask` 
2. Define the flask app `export FLASK_APP=link/to/my/python/snmpTrap.py`
3. Run the Flask App `python3 -m flask run`
4. Let the Webhook's trigger
5. See the Webhook payload on the command line as it's received
6. Verifiy it's being recieved by your SNMP Trap Receiver

## SNMP Trap
The code will generate the SNMP Trap via the `pysnmp` library and send over to the declared endpoint and port.  You can verify or test with a tool such as [MIB Browser](https://www.ireasoning.com/mibbrowser.shtml) to ensure that the SNMP trap is being recieved.

### Disclaimer
Use at your own risk.  If you modify the contents of the webhook payload you will have to ensure that the correct values are being parsed / stored in the `snmpTrap.py`.
