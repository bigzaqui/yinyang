# YIN-YANG ninjaX tracerouting
A [RIPE Atlas][1] [Tools hackathon][2] project

[1]: https://atlas.ripe.net/ "atlas.ripe.net"
[2]: https://atlas.ripe.net/hackathon/tools-2015/ "atlas.ripe.net/hackathon/tools-2015"


## Introduction
### Problem
Troubleshooting a high latency path can be difficult. Standard tracerouting will give you only the path from source to destination. However, the return path from destination to source can significantly differ in terms of both path and time. The roundtrip time (RTT) actually measures the time of forward plus return path, so it would be good if the corresponding path is found.
Getting the reverse path from a particular network can be achieved by either having a person there who can trace for us, or having access to a device or a looking glass in the network. These are not fast and easily achievable and for sure not automatic ways of getting the roundtrip path.
### Solution
The *YIN-YANG ninjaX tracerouting* project takes advantage of RIPE Atlas probes being [present][3] (one day) in every single AS out there. Instead of tracing between two addresses, we input two AS numbers into the script. It will then find two RIPE probes in these autonomous systems (one probe in each AS) and perform two traceroutes - from the source probe to the destination probe and then from the destination probe to the source probe. This way *YIN-YANG* will have the forward and reverse paths of the roundtrip.
*YIN-YANG* is interested in the AS path, so it aggregates IP route into an AS path.
### Bonuses
 * *YIN-YANG* identifies IXP networks along the route and displays them in the AS path.
 * *YIN-YANG* can find another source probe geographically close to the first one, but in another autonomous system, and repeat the traceroute from the second probe. This can show you an alternative provider with possibly better path and RTT who lives next door and is easily reachable. 

[3]: https://atlas.ripe.net/results/maps/network-coverage/ "atlas.ripe.net/results/maps/network-coverage"

## Implementation
### Design
Here is an overview diagram of the implemented workflow:
![Workflow diagram](https://github.com/bigzaqui/yinyang/blob/master/README.resource/workflow.png)

Step by step, the workflow looks like this:
 1. Input source and destination AS
 	The script takes these as command-line parameters.
 2. Find a probe in each AS
 	The script uses [RIPE Atlas Cousteau][4] to connect to RIPE Atlas and ask for a list of public online probes in an autonomous system. Then just takes one of these probes.
 	If the *--another* option is used, it also searches for another probe georgraphically close to the source probe.
 3. Perform traceroutes
 	The script again uses [RIPE Atlas Cousteau][4] to schedule a traceroute measurement in RIPE Atlas and then wait for the traceroute result. This is done once for forward and once for reverse directions and if the *--another* option is used - two more traceroutes from and to the second source probe.
 4. Resolve hops
 	The script then takes every IP in the traceroutes and:
 		- checks if this IP is part of an IXP network. The information about IXP networks is taken from [PeeringDB][6] API, but is currently offline downloaded in a file.
 		- uses the [RIPE Stat][5] API to get the API autonomous system. Then consequent AS numbers in the trace are aggregated to form single steps in the AS path.
 5. Draw the paths
 	The script then takes the AS paths and draws them in a single graph exported to a png image. It uses the [NetworkX][7] library and [PathDrawer][8] example code.

[4]: https://github.com/RIPE-NCC/ripe-atlas-cousteau "github.com/RIPE-NCC/ripe-atlas-cousteau"
[5]: https://stat.ripe.net/ "stat.ripe.net"
[6]: http://docs.peeringdb.com/#peeringdb-20 "http://docs.peeringdb.com/#peeringdb-20"
[7]: https://github.com/networkx/ "github.com/networkx"
[8]: https://networkx.lanl.gov/trac/attachment/ticket/199/PathDrawer.py

### Requirements
Requirements are listed in the [requirements.txt](https://raw.githubusercontent.com/bigzaqui/yinyang/master/requirements.txt).

To get started with this project just install all the requirements

```
pip install -r /requirements.txt
```

## Usage
The tool can be executed via a simple CLI call:

```
python cli.py --verbose asn run --src_asn 12322 --dst_asn 8473 --draw 
```

This will visualize a path from ASN 12322 to ASN 8473 and the reverse direction. 

For more examples have look at [samples.txt](https://raw.githubusercontent.com/bigzaqui/yinyang/master/samples.txt)


