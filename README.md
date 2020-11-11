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

## Example Curl Request
curl --insecure -XPOST -H "Content-type: application/json" -d '{
  "method": "POST",
  "path": "/",
  "query": {},
  "headers": {
    "x-forwarded-for": "52.20.96.17",
    "x-forwarded-proto": "https",
    "x-forwarded-port": "443",
    "host": "96b171e044dbe5ce6775d67652bbbdb9.m.pipedream.net",
    "x-amzn-trace-id": "Root=1-5fab6ef7-2fd0906963fbbca7557f218a",
    "content-length": "1931",
    "accept-encoding": "gzip, deflate",
    "accept": "*/*",
    "user-agent": "python-requests/2.24.0",
    "content-type": "application/json; charset=utf-8",
    "x-datadog-trace-id": "14706617228889315125",
    "x-datadog-parent-id": "7625497438789849858",
    "x-datadog-sampling-priority": "1"
  },
  "bodyRaw": "{\n    \"body\": \"%%%\\nCPU is high on nls-jenkins-master with an IP of 10.88.11.35  @webhook-datadogSupportTest\\n\\nTest notification triggered by support-chartercommunications-31.\\n\\n[![Metric Graph](https://p.datadoghq.com/snapshot/view/dd-snapshots-prod/org_475940/2020-11-11/95d50cd6149a071c3569499edc3c5e15e1a8f9cd.png)](https://app.datadoghq.com/monitors#25562336?to_ts=1605070640000&group=host%3Anls-jenkins-master&from_ts=1605066980000)\\n\\n**system.cpu.system** over **host:nls-jenkins-master** was **> 0.1** at least once during the **last 5m**.\\n\\nThe monitor was last triggered at Wed Nov 11 2020 04:56:20 UTC.\\n\\n- - -\\n\\n[[Monitor Status](https://app.datadoghq.com/monitors#25562336?group=host%3Anls-jenkins-master)] \\u00b7 [[Edit Monitor](https://app.datadoghq.com/monitors#25562336/edit)] \\u00b7 [[View nls-jenkins-master](https://app.datadoghq.com/infrastructure?filter=nls-jenkins-master)] \\u00b7 [[Show Processes](https://app.datadoghq.com/process?sort=cpu%2CDESC&to_ts=1605070700000&tags=host%3Anls-jenkins-master&from_ts=1605069680000&live=false&showSummaryGraphs=true)] \\u00b7 [[Related Logs](https://app.datadoghq.com/logs?query=host%3A%22nls-jenkins-master%22&live=false&to_ts=1605070580000&from_ts=1605069680000)]\\n%%%\",\n    \"alertid\": \"25562336\",\n    \"alertstatus\": \"system.cpu.system over *** was > 0.1 at least once during the last 5m**.\",\n    \"alerttype\": \"error\",\n    \"scope\" : \"host:nls-jenkins-master\",\n    \"alertmetric\": \"system.cpu.system\",\n    \"alerttransition\": \"Triggered\",\n    \"hostname\": \"nls-jenkins-master\",\n    \"link\":\"https://app.datadoghq.com/event/event?id=5717804682337238360\",\n    \"last_updated\": \"1605070582000\",\n    \"event_type\": \"metric_alert_monitor\",\n    \"title\": \"[Triggered on {host:nls-jenkins-master}] [TEST] CPU is high on nls-jenkins-master with an IP of 10.88.11.35\",\n    \"date\": \"1605070582000\",\n    \"id\": \"5717804682337238360\",\n    \"tags\": \"host:nls-jenkins-master,monitor\"\n}",
  "body": {
    "body": "%%%\nCPU is high on nls-jenkins-master with an IP of 10.88.11.35  @webhook-datadogSupportTest\n\nTest notification triggered by support-chartercommunications-31.\n\n[![Metric Graph](https://p.datadoghq.com/snapshot/view/dd-snapshots-prod/org_475940/2020-11-11/95d50cd6149a071c3569499edc3c5e15e1a8f9cd.png)](https://app.datadoghq.com/monitors#25562336?to_ts=1605070640000&group=host%3Anls-jenkins-master&from_ts=1605066980000)\n\n**system.cpu.system** over **host:nls-jenkins-master** was **> 0.1** at least once during the **last 5m**.\n\nThe monitor was last triggered at Wed Nov 11 2020 04:56:20 UTC.\n\n- - -\n\n[[Monitor Status](https://app.datadoghq.com/monitors#25562336?group=host%3Anls-jenkins-master)] · [[Edit Monitor](https://app.datadoghq.com/monitors#25562336/edit)] · [[View nls-jenkins-master](https://app.datadoghq.com/infrastructure?filter=nls-jenkins-master)] · [[Show Processes](https://app.datadoghq.com/process?sort=cpu%2CDESC&to_ts=1605070700000&tags=host%3Anls-jenkins-master&from_ts=1605069680000&live=false&showSummaryGraphs=true)] · [[Related Logs](https://app.datadoghq.com/logs?query=host%3A%22nls-jenkins-master%22&live=false&to_ts=1605070580000&from_ts=1605069680000)]\n%%%",
    "alertid": "25562336",
    "alertstatus": "system.cpu.system over *** was > 0.1 at least once during the last 5m**.",
    "alerttype": "error",
    "scope": "host:nls-jenkins-master",
    "alertmetric": "system.cpu.system",
    "alerttransition": "Triggered",
    "hostname": "nls-jenkins-master",
    "link": "https://app.datadoghq.com/event/event?id=5717804682337238360",
    "last_updated": "1605070582000",
    "event_type": "metric_alert_monitor",
    "title": "[Triggered on {host:nls-jenkins-master}] [TEST] CPU is high on nls-jenkins-master with an IP of 10.88.11.35",
    "date": "1605070582000",
    "id": "5717804682337238360",
    "tags": "host:nls-jenkins-master,monitor"
  }
}' 'http://127.0.0.1:5000/webhook'

### Disclaimer
Use at your own risk.  If you modify the contents of the webhook payload you will have to ensure that the correct values are being parsed / stored in the `snmpTrap.py`.
