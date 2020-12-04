##################################################################################
################################## Disclaimer ####################################
##################################################################################

'''
This Webhook to SNMP python script is property of whomever wants to maintain it.
This script was created to help you convert Webhook (JSON via HTTP) to SNMP Trap via UDP.
Datadog will not provide ongoing support for this script but it can be modified and used at your own consent.
If you have any questions please reach out to the developers of the python library pysnmp or work with your internal resources to troubleshoot.
If you modify the contents of the webhook payload you will have to ensure that the correct values are being parsed / stored in the snmpTrap.py.
'''


##################################################################################
################################## Packages ####################################
##################################################################################
from pysnmp.hlapi import *
from pysnmp import debug
from flask import Flask, request, Response

app = Flask(__name__)

##################################################################################
############################## Details from Customer ##############################
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

snmpAddress = "localhost" #enter trap IP or URL
snmpPort = 162 #What port is open for SNMP Trap over UDP

##################################################################################
################# Send SNMP Trap #################################################
##################################################################################

@app.route('/webhook', methods=['POST'])
def respond():
    #set webhook JSON payload to variable
    webhookPayload = request.json

    #Set individual variables from webhookPayload

    if webhookPayload:
        node = webhookPayload.get('hostname','NULL')
        nodeAlias=webhookPayload.get('ip','NULL')
        summary = webhookPayload.get('title','NULL')

        #Check Status of "alerttype" field and map to numberical value
        alerttype = webhookPayload.get('alerttype','NULL')
        if "error" in alerttype: severity = 5
        elif "warning" in alerttype: severity = 2
        elif "success" in alerttype: severity = 0
        else: severity = 0 #catch all should not be hit

        #Check if alert or Resolution
        alerttransition = webhookPayload.get('alerttransition','NULL')
        if "Recovered" in alerttransition: type = 2
        elif "Warn" in alerttransition: type = 1
        elif "Triggered" in alerttransition: type = 1
        else: type = 2 #catch all but should never be seen

        #Hardcode Datadog Integration
        integration="DATADOG-INTEGRATION" #hardcoded to DATADOG

        alertgroup= "Server" #hard coded for now

        alertkey= webhookPayload.get('hostname','NULL')

        #Additional Fields that may be useful
        link = webhookPayload.get('link','NULL')
        alertmetric = webhookPayload.get('alertmetric','NULL')
        fullbody = webhookPayload.get('body','NULL')
        epochdate = webhookPayload.get('date','NULL')
        alertstatus = webhookPayload.get('alertstatus','NULL')
        
        iterator = sendNotification(
            SnmpEngine(),
            CommunityData('public', mpModel=0),
            UdpTransportTarget(('{}'.format(snmpAddress), snmpPort)), #define IP or URL and Port to use for trap
            ContextData(),
            'trap',
            NotificationType(
                ObjectIdentity('1.3.6.1.4.1.999')
            ).addVarBinds(
                ('.1.3.6.1.4.1.999.1', OctetString('{}'.format(node))),
                ('.1.3.6.1.4.1.999.2', OctetString('{}'.format(nodeAlias))),
                ('.1.3.6.1.4.1.999.3', OctetString('{}'.format(summary))),
                ('.1.3.6.1.4.1.999.4', OctetString('{}'.format(severity))),
                ('.1.3.6.1.4.1.999.5', OctetString('{}'.format(type))),
                ('.1.3.6.1.4.1.999.6', OctetString('{}'.format(integration))),
                ('.1.3.6.1.4.1.999.7', OctetString('{}'.format(alertgroup))),
                ('.1.3.6.1.4.1.999.8', OctetString('{}'.format(alertkey)))
            ).loadMibs(
                'SNMPv2-MIB'
            )
        )
    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(errorIndication)

    else:
        #Print Entire JSON payload from Webhook for troubleshooting
        print (webhookPayload)
        print ("***************************************************************************************")
        print("Successfully sent trap to {}".format(snmpAddress)+ " on port {}".format(snmpPort))
        print ("")
        return Response(status=200)
