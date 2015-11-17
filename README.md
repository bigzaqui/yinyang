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
 2. Find a probe in each AS
 3. Perform traceroutes
 4. Resolve hops
 5. Draw the paths
### Requirements


## Usage

