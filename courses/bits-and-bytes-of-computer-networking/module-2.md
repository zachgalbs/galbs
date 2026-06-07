---
title: The Network Layer
course: The Bits and Bytes of Computer Networking
module: 2
provider: Coursera (Google)
---

# Module 2: The Network Layer

Everything we've gone over so far is about how nodes communicate on the **same network**. The network layer was built so that devices could communicate between networks: so that **internetworks** could be built.

## How can you communicate between networks?

To send information to another device on the same network, you need the receipients MAC address. You attach their MAC address to your Ethernet frame, send it to the switch, and then the switch forwards the frame to the device.

If you wanted to send something to a friend at a different network, you would have to store a table with every one of your friend's MAC addresses, and the next hop on how to get there. Since MAC addresses have no grouping, there's no way to condense this table, and every router would end up storing an obscene number of entries to account for every device you would ever want to communicate with.

## The Internet Protocol
To solve this issue, researchers in the late 1970s came up with the **Internet Protocol**. The idea was to give every device their own **IP Address**, with a common **network id** to group devices.

In the first version, you had four octets, with the first representing a network id, and the last three serving to identify the device on the network:

> 243.104.23.1 *is the device on network 243 with host id 6,821,889.

Since there are 8 bits in an octet, there are 256(2^8) possible networks, and each network has 16,777,216(2^24) possible devices.

256 networks couldn't sustain the demand, though, and it was rare for one network to use all 16 million possiblities. So, a new standard was born:

### Classful IP Addresses

Instead of fighting for the limited number of network IDs, and then leaving 99% of the host IDs vacant, what if you could choose a **class** of IP address to claim for your need?

#### Class A
The first octet is dedicated to network ID, last three are dedicated for host IDs. This IP address is hard to get, but once you have it, you can account for 16 million unique devices. Large companies like Apple, Google, and IBM have their own Class A IP address.

#### Class B
First **two** octets dedicated to network ID, last two for host IDs.

#### Class C
First **three** octets for network ID, last one for host IDs.

#### How can you tell the difference?

The first octet looks a little different for each case:

Class A's first bit starts with a 0. This limits the number of possible network ids to 128.

Class B's first octet starts with `10`, and Class C's starts with `110`.

> Other classes D and E are used for multicast and experiments respectively.

### Subnetting

Often, large organizations with their own IP address would find they had too many host ids for their one network. Assuming you had a class A or B IP address, it was common to have tens of thousands of devices on one local network. This was clunky and slow because every time something like an ARP request is sent a broadcast would flood to every single device on the network.

To fix this, subnetting was devised. You keep your first 1-3 octets as the network ID, but then you dedicate some of the bits that used to be for identifying devices, and use them as network separators. To do this, you define a new field that every device requires to communicate: **subnet masks**.

The subnet mask tells each devices what range of IP addresses are on their local network. You compute a **bitwise AND** on your subnet mask and your IP address, do the same for the intended recepients IP address, compare the results of the bitwise AND (called the **subnet id**), and if they're the same, conclude that they're on the same local network.

This was better because you could limit the number of hosts you have to the number you need. You don't need 65,536 combinations of host IDs, you can choose to have 64.

This way, even if you only have one class B IP address, you can use subnetting to give yourself 16 logically separate networks.

For sending traffic to devices that don't share your subnet id, you simply route the IP datagram to the router, the router sees that the IP address belongs to one of the 16 networks, sends it to another router at the corresponding network it does ARP to find the MAC address, and then sends it along.

### CIDR

At this point there was still an issue: What if you simply didn't need that many networks? What if you didn't need 60,000 devices on your network? You could move to class C, but then you only had 254 slots. As demand for IP addresses increased, the authority handing them out wanted to conserve address space and ended up giving out multiple class C IP addresses to corporations. Since there was an increase in class C addresses, routing tables exploded, increasing strain on routers.

To fix this, the **Classless Inter-Domain Routing** standard was introduced. In addition to your IP address, you include a number representing the number of bits used for the network ID.

`192.168.1.0/26`: 26 bits are used to identify the network, and 6 bits are used for the host id, yielding 64 possible connections on the network.
