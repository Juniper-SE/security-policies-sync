# security-policies-sync

An event script that allows you to check whether security policies are in sync,
or whether a node is not shown in the check.
The output of the commands will be output to a local file that will then be SCP'd
to a remote server.
NOTE: only one destination can be used at a time, make sure you remove one before committing.

Special thanks to Lee Gillespie for providing a base for the event script Junos configuration.

# JunOS Config Notes
time-interval: time in seconds to run the script/commands
traceoptions: used to debug any python runtime issues
python-script-user: "By default, Junos OS executes Python event scripts with the access privileges of the generic, unprivileged user and group nobody. Starting in Junos OS Release 16.1R3, you can specify the user under whose access privileges the Python script will execute" https://www.juniper.net/documentation/us/en/software/junos/automation-scripting/topics/concept/automation-enabling-an-event-script.html
