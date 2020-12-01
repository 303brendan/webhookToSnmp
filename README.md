# Datadog Webhook To Snmp
The concept behind this was the need to convert the Webhook payload (JSON) from a Datadog alert into an SNMP Trap that can be sent to a Trap Receiver.

## Disclaimer
This Webhook to SNMP python script is property of whomever wants to maintain it. This script was created to help you convert Webhook (JSON via HTTP) to SNMP Trap via UDP.  Datadog will not provide ongoing support for this script but it can be modified and used at your own consent. If you have any questions please reach out to the developers of the python library pysnmp or work with your internal resources to troubleshoot.

If you modify the contents of the webhook payload you will have to ensure that the correct values are being parsed / stored in the `snmpTrap.py`.

## Overview
You will find one file `snmpTrap.py` which requires a few libraries (pysnmp & flask).  As long as you have these libraries installed on the server (install via `pip install X` command) you should be able to run this web service which will expose the `webhook` endpoint, allow incoming JSON via http POST, and parse the JSON body.

## Prerequisites

Ensure you've permitted inbound traffic to the host running the Flack web service.  Here is the [list of IPs](https://ip-ranges.datadoghq.com/webhooks.json) that are the source of Datadog webhook notifications.  

## To Run Flask
1. Install Flask via `pip3 install Flask`.  Also install pysnmp via `pip3 install pysnmp`
2. Define the flask app `export FLASK_APP=link/to/my/python/snmpTrap.py`
3. Run the Flask App `python3 -m flask run --host=0.0.0.0`
4. Let the Webhook's trigger
5. See the Webhook payload on the command line as it's received
6. Verifiy it's being recieved by your SNMP Trap Receiver

## SNMP Trap
The code will generate the SNMP Trap via the `pysnmp` library and send over to the declared endpoint and port.  You can verify or test with a tool such as [MIB Browser](https://www.ireasoning.com/mibbrowser.shtml) to ensure that the SNMP trap is being recieved.

## Example Curl Request
You can run this curl request via CLI to simulate a Webhook `POST` from Datadog.  The body was captured using [PipeDream's Webhook Endpoints](https://pipedream.com/) to capture the outbound payload.
```
curl --insecure -XPOST -H "Content-type: application/json" -d '{
    "body": "%%%\n\n@slack-brendan-demo CPU is high on GamingPC with a threshold of 70.0 \n@webhook-brendansnmp \n\nTest notification triggered by brendan.roche@datadoghq.com.\n\n[![Metric Graph](https://p.datadoghq.com/snapshot/view/dd-snapshots-prod/org_11287/2020-11-30/aec053705bfb9108b43c3d94c578971d842dd1a0.png)](https://app.datadoghq.com/monitors#2865250?to_ts=1606757679000&group=host%3Arouter-0&from_ts=1606754019000)\n\n**system.cpu.system** over **host:router-0** was **> 70.0** at all times during the **last 5m**.\n\nThe monitor was last triggered at Mon Nov 30 2020 17:33:39 UTC.\n\n- - -\n\n[[Monitor Status](https://app.datadoghq.com/monitors#2865250?group=host%3Arouter-0)] · [[Edit Monitor](https://app.datadoghq.com/monitors#2865250/edit)] · [[View router-0](https://app.datadoghq.com/infrastructure?filter=router-0)] · [[Show Processes](https://app.datadoghq.com/process?sort=cpu%2CDESC&to_ts=1606757739000&tags=host%3Arouter-0&from_ts=1606756719000&live=false&showSummaryGraphs=true)] · [[Related Logs](https://app.datadoghq.com/logs?query=host%3A%22router-0%22&live=false&to_ts=1606757619000&from_ts=1606756719000)]\n%%%",
    "last_updated": "1606757621000",
    "event_type": "metric_alert_monitor",
    "title": "[Triggered] [TEST] CPU is high on GamingPC - BMR",
    "date": "1606757621000",
    "hostname": "router-0",
    "ip": "10.0.0.15",
    "alerttype": "error",
    "alerttransition": "Triggered",
    "link": "https://app.datadoghq.com/event/event?id=5746108497135337488",
    "alertmetric": "system.cpu.system",
    "alertstatus": "system.cpu.system over *** was > 70.0 at all times during the last 5m**.",
    "org": {
      "id": "11287",
      "name": "Datadog Demo (11287)"
    },
    "id": "5746108497135337488"
  }' 'http://localhost:5000/webhook'
```


