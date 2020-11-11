'''
         ____        __        ____
        / __ \____ _/ /_____ _/ __ \____  ____ _
       / / / / __ `/ __/ __ `/ / / / __ \/ __ `/
      / /_/ / /_/ / /_/ /_/ / /_/ / /_/ / /_/ /
     /_____/\__,_/\__/\__,_/_____/\____/\__, /
                                       /____/
'''

from pysnmp.hlapi import *
from pysnmp import debug

##################################################################################
############################## Details from Charter ##############################
##################################################################################
# .1 Node
# .2 NodeAlias
# .3 Summary
# .4 Severity
# .5 Type
# .6 Integration name
# .7 AlertGroup
# .8 AlertKey


##################################################################################
#################### Set Variables for testing ###################################
##################################################################################
node="laptop"
nodeAlias="10.0.0.1"
summary="ITS BROKE!!!"
severity="5"
type="alert"
integration="DATADOG-INTEGRATION"
alertgroup="blah"
alertkey="blah"


##################################################################################
################# Send SNMP Trap #################################################
##################################################################################

errorIndication, errorStatus, errorIndex, varbinds = next(sendNotification(SnmpEngine(),
     CommunityData('not_public'),
     UdpTransportTarget(('localhost', 162)), #define IP or URL and Port to use for trap
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
