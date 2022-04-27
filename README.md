# security-policies-sync

An event script that allows you to check whether security policies are in sync,
or whether a node is not shown in the check.
The output of the commands will be output to a local file that can be pulled off the SRX.

Special thanks to Lee Gillespie for providing a base for the event script Junos configuration.

# JunOS Config Notes
time-interval: time in seconds to run the script/commands
traceoptions: used to debug any python runtime issues
python-script-user: "By default, Junos OS executes Python event scripts with the access privileges of the generic, unprivileged user and group nobody. Starting in Junos OS Release 16.1R3, you can specify the user under whose access privileges the Python script will execute" https://www.juniper.net/documentation/us/en/software/junos/automation-scripting/topics/concept/automation-enabling-an-event-script.html

# To use/install:
1. Load or set SRX configs using the JSON formatted file (srx-config-json) or the set commands (srx-config-set)
    - make sure you set the time-interval to what you actually need and not 60 seconds!!
2. Copy the python file over to the devices into `/var/db/scripts/event`
3. Wait for your time-interval to pass and view the log
