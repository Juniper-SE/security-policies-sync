from base64 import encode
from jnpr.junos import Device
from lxml import etree
import re
import logging
syslog = logging.getLogger("syslog")

# Logging levels are DEBUG, INFO, WARNING, and ERROR
# Debug prints ALL logs to file
# INFO only print INFO and above
# ^ same for warning and ERROR is only errors
log_server = ""
logging.basicConfig(
    filename='/var/db/scripts/event/policy_sync.log',
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    # Leave empty if running directly on device;
    # otherwise put in SSH info
    jdev = Device()

    # Opens a connection
    jdev.open()

    # Sends a CLI request to check the security policies
    # NOTE: cannot use RPC call at the moment as there is an error
    # Should be replaced with RPC call when fixed
    sec_pols_check = jdev.cli("request security policies check")
    logging.info("INFO: Security policies check: " + sec_pols_check)

    # Checks whether "out-of-sync" is in the output OR
    # whether node0 or node1 is missing
    # If it is found, get security policies checksum,
    # get the USP policy checksum for each node, and write
    # those checksums out to a file for logging purposes
    # NOTE: this only works in an HA set-up;
    # remove 'node0' for a non-HA SRX
    matches = re.findall('node\d\.fpc\d.+', sec_pols_check)
    if len(matches) != 2 or "out-of-sync" in sec_pols_check:
        logging.warning("WARNING: Policies are out-of-sync OR a node is missing.")
        logging.info("INFO: Gathering checksums...")

        # "show security policies checksum"
        sec_polcs_checksum = jdev.rpc.get_policy_checksum_information({'format':'text'})
        logging.info("INFO: security policies checksums: " + etree.tostring(sec_polcs_checksum, encoding="unicode"))

        # request pfe execute target node0.fpc0 command "show usp policy checksum"
        # request pfe execute target node1.fpc0 command "show usp policy checksum"
        # Gets the checksums of each node for logging
        node0_fpc0 = jdev.rpc.request_pfe_execute(target='node0.fpc0', command='show usp policy checksum')
        node1_fpc0 = jdev.rpc.request_pfe_execute(target='node1.fpc0', command='show usp policy checksum')
        logging.info("INFO: node0 checksum: " + etree.tostring(node0_fpc0, encoding='unicode'))
        logging.info("INFO: node1 checksum: " + etree.tostring(node1_fpc0, encoding='unicode'))

        # "request security policies resync"
        #sec_pols_resync = jdev.rpc.recover_security_policy({'format':'text'})
        sec_pols_resync = jdev.cli("request security policies resync")      # currently the rpc gives an "unrecognized command" error
        logging.info("INFO: resync output: " + sec_pols_resync)

        # TODO: SCP to log server
        # Sends a syslog with a custom message
        # For syslog priority levels, see: https://manuals.plus/m/e7f98432136a1bb0ce2b378dc99d4c20765f61b020863ffe97021947651df6a9.pdf
        syslog.warning("Security policies are out of sync, resync was attempted.")