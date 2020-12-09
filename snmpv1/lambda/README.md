# Datadog Webhook To Snmp Trap - Serverless Package
The concept behind this was the need to convert the Webhook payload (JSON) from a Datadog alert into an SNMP Trap that can be sent to a Trap Receiver.

## Disclaimer
This Webhook to SNMP python script is property of whomever wants to maintain it. This script was created to help you convert Webhook (JSON via HTTP) to SNMP Trap via UDP.  Datadog will not provide ongoing support for this script but it can be modified and used at your own consent. If you have any questions please reach out to the developers of the python library pysnmp or work with your internal resources to troubleshoot.

If you modify the contents of the webhook payload you will have to ensure that the correct values are being parsed / stored in the `snmpTrap.py`.

## Overview
You will find one file `snmpTrap.py` which requires the pysnmp library and AWS API Gateway.  API Gateway will receive the Webhook (JSON via HTTP POST) and send the `body` to the related Lambda Function (snmpTrap.py) which will parse the fields from the API Gateway `event` payload.

## Prerequisites

Ensure that you have API gateway configured with a public "REST Endpoint" that allows the http method "POST".  

## SNMP Trap
The code will generate the SNMP Trap via the `pysnmp` library and send over to the declared endpoint and port in the lambda function.  




