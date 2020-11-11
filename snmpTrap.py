##################################################################################
################################## Disclaimer ####################################
##################################################################################

'''
This Webhook to SNMP python script is property of whomever wants to maintain it.
Datadog Sales Engineers have help craft the script to convert Webhook (JSON via HTTP)
to SNMP Trap via UDP at the customer request.  Datadog will not provide ongoing
support for this script but it can be modified and used at your own consent. If you
have any questions please reach out to the developers of the python library pysnmp
or work with your internal resources to troubleshoot.
'''


##################################################################################
################################## Packages ####################################
##################################################################################
from pysnmp.hlapi import *
from pysnmp import debug
from flask import Flask, request, Response


app = Flask(__name__)


##################################################################################
############################## Details from Charter ##############################
##################################################################################
# .1 Node - Usually the host or device name of the alarming device.
# .2 NodeAlias - The IP address of the alarming device.
# .3 Summary - Alarm description.
# .4 Severity - Any from 0 to 5; 0=Clear, 1=Info, 2=Warning, 3=Minor, 4=Major, 5=Critical.
# .5 Type - 1=Alarm, 2=Resolution (clear).
# .6 Integration name - DATADOG-INTEGRATION
# .7 AlertGroup - This is the alarmed module of the device; for instance, Network.
# .8 AlertKey - This is the alarmed component of the module; following the above example, it can be Ethernet-Card-01.


##################################################################################
############### Set Static Variables for SNMP Trap Address #######################
##################################################################################

snmpAddress = "localhost" #charter specified 69.134.208.40 as Netcool IP
snmpPort = 162 #What port is open for SNMP Trap over UDP

##################################################################################
################# Send SNMP Trap #################################################
##################################################################################

@app.route('/webhook', methods=['POST'])
def respond():
    webhookPayload = request.json
    #Set Variables from webhook

    node = webhookPayload['body']['hostname']
    nodeAlias="10.0.0.1" #not sure how to get this from webhook
    summary = webhookPayload['body']['title']


    #Check Status of "alerttype" field and map to numberical value
    alerttype = webhookPayload['body']['alerttype']
    if "error" in alerttype: severity = 5
    elif "warning" in alerttype: severity = 2
    elif "success" in alerttype: severity = 0
    else: severity = 0 #catch all should not be hit


    #Check if alert or Resolution
    alerttransition = webhookPayload['body']['alerttransition']
    if "Recovered" in alerttransition: type = 2
    elif "Warn" in alerttransition: type = 2
    elif "Triggered" in alerttransition: type = 1
    else: type = 2 #catch all but should never be seen


    #Hardcode Datadog Integration
    integration="DATADOG-INTEGRATION" #hardcoded to DATADOG
    alertgroup= "Server" #hard coded for now
    alertkey= webhookPayload['body']['hostname']

    #Additional Fields that may be useful
    link = webhookPayload['body']['link']
    alertmetric = webhookPayload['body']['alertmetric']
    body = webhookPayload['body']['body']
    date = webhookPayload['body']['date']
    alertstatus = webhookPayload['body']['alertstatus']



    errorIndication, errorStatus, errorIndex, varbinds = next(sendNotification(SnmpEngine(),
         CommunityData('not_public'),
         UdpTransportTarget(('{}'.format(snmpAddress), snmpPort)), #define IP or URL and Port to use for trap
         ContextData(),
         'trap',
         [ObjectType(ObjectIdentity('.1.3.6.1.4.1.999.1'), OctetString('{}'.format(node))),
          ObjectType(ObjectIdentity('.1.3.6.1.4.1.999.2'), OctetString('{}'.format(nodeAlias))),
          ObjectType(ObjectIdentity('.1.3.6.1.4.1.999.3'), OctetString('{}'.format(summary))),
          ObjectType(ObjectIdentity('.1.3.6.1.4.1.999.4'), OctetString('{}'.format(severity))),
          ObjectType(ObjectIdentity('.1.3.6.1.4.1.999.5'), OctetString('{}'.format(type))),
          ObjectType(ObjectIdentity('.1.3.6.1.4.1.999.6'), OctetString('{}'.format(integration))),
          ObjectType(ObjectIdentity('.1.3.6.1.4.1.999.7'), OctetString('{}'.format(alertgroup))),
          ObjectType(ObjectIdentity('.1.3.6.1.4.1.999.8'), OctetString('{}'.format(alertkey)))

          ])
    )

    if errorIndication:
        print(errorIndication)
    else:
        print("successfully sent trap")

    print(request.json);
    return Response(status=200)
