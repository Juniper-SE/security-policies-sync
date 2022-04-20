from base64 import encode
from jnpr.junos import Device
from lxml import etree
import jcs
import re

log_server = ""

if __name__ == '__main__':
    jdev = Device(host="10.192.16.240", user="lab", passwd="Lablab")

    # Opens a connection
    jdev.open()

    # Sends a CLI request to check the security policies
    # NOTE: cannot use RPC call at the moment as there is an error
    # Should be replaced with RPC call when fixed
    sec_pols_check = jdev.cli("request security policies check")

    # Checks whether "out-of-sync" is in the output OR
    # whether node0 or node1 is missing
    # If it is found, get security policies checksum,
    # get the USP policy checksum for each node, and write
    # those checksums out to a file for logging purposes
    # NOTE: this only works in an HA set-up; remove 'node0' for
    # a non-HA SRX
    matches = re.findall('node\d\.fpc\d.+', sec_pols_check)
    if len(matches) != 2 or "out-of-sync" in sec_pols_check:

        # "show security policies checksum"
        sec_polcs_checksum = jdev.rpc.get_policy_checksum_information({'format':'text'})
        print(etree.tostring(sec_polcs_checksum, encoding="unicode"))

        # request pfe execute target node0.fpc0 command "show usp policy checksum"
        # request pfe execute target node1.fpc0 command "show usp policy checksum"
        # node0_fpc0 = jdev.rpc.request_pfe_execute(target='fpc0', command='show usp policy checksum')
        # node1_fpc0 = jdev.rpc.request_pfe_execute(target='node1.fpc0', command='show usp policy checksum')
        # print(etree.tostring(node0_fpc0, encoding='unicode'))
        # TODO: SCP to log server

        jdev.display_xml_rpc("request security policies resync")

        # Sends a syslog with a custom message
        # For syslog priority levels, see: https://manuals.plus/m/e7f98432136a1bb0ce2b378dc99d4c20765f61b020863ffe97021947651df6a9.pdf
        # jcs.syslog("facility.change.alert", "Security policies are out of sync and need to be fixed")