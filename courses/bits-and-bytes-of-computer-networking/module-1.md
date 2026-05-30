---
title: Introduction to Networking
course: The Bits and Bytes of Computer Networking
module: 1
provider: Coursera (Google)
---

# Module 1: Introduction to Networking

## Layers

### 1. Physical
How to transport bits with electricity

### 2. Data Link
Structures bits as frames

### 3. Network
Allows networks to talk to each other through routers

### 4. Transport
Gets information to specific programs on servers

### 5. Application
Manipulates and renders data for end user

## Physical Layer

### Cables
Cables are used to transfer electrical signals, and then translated into bits.

The most common cable used is a **twisted pair** copper cable, which has strings of copper twisted together to prevent crosstalk. Modern cables have multiple of these twisted copper cables, which allows **full duplex** communication.

**crosstalk** is when copper cables' signals interfere with each other, corrupting the message.

**full duplex** communication is where you can send and receive data at the same time. This usually means some of the twisted pair cables are used to send signal, and some are used to receive signal.

> In modern networks you use all pairs for both receiving and sending

Before full duplex (multiple twisted pair cables), computers would commonly send signals at the same time, causing collisions. To fix this, **carrier sense multiple access with collision detection**, or CSMA/CD was invented, where computers resend bits with a random time delay when a collision is detected.

**half duplex** is when you can only send or receive at one time.

### Network ports
Once a twisted pair (ethernet cable) ends, it's connected to a network port, which exposes its data.

The most common network port is called the **Registered Jack 45** port, and is the specific name for what people usually call *ethernet ports*.

The ethernet port, or RJ45 port you see on your wall connects directly to a hub or switch through something called a **patch panel**. The patch panel has tons of RJ45 ports which are then wired to the hub or switch.

The RJ45 port has two lights: the **Link Light**, and **Activity Light**. The Link Light proves there's some electrical connection between hardware, and the Activity Light shows data frames are moving across the wire.

A **hub** is where a collection of cables are connected, and allows nodes on a network to communicate with each other. It's the most primitive method of connecting computers, and gives all traffic to all computers, giving the responsibility to the nodes to decide what data to process.

## Data Link Layer

> *How do nodes on a network know what data belongs to them?*

Through **MAC Addresses**. They're globally unique identifiers assigned to each device on a network so that traffic can be routed correctly.

They're **48 bits**, and are **globally unique**, meaning no other device in the world will have the same MAC address as your device. This is possible because 48 bits allows 2^48 possibilities, or around half a quadrillion different combinations.

MAC addresses are typically listed using hexadecimal numbers, which are base-16, meaning each hex digit has 4 bits, and each couple has 8 bits. In other words, each pair is an octet (or byte):

`9A:4B:22:F1:27:E2` is an example MAC address. It has 6 octets, or 48 bits.

The **first three octets** in a MAC address correspond to the manufacturer who made the device. Manufacturers like Apple are given tons of different ranges of MAC addresses to give out to their devices from the IEEE (Institute of Electrical and Electronics Engineers).

Every set of data sent through wires contains the **destination MAC address**, and each device looks at the destination MAC address, checks if it is theirs, and if not rejects the data.

> *But isn't this super inefficient? Why does every device need to do this check?*

A **switch** is an intelligent hub, containing a computer on board that decides which nodes get data. This way, there's way less traffic on the network. The switch keeps a table of MAC addresses and connected cables, and simply sends the data through the cable corresponding to the destination MAC address

> *What if it doesn't yet have an entry for a MAC address?*

The switch sends the data to every device, and when the recipient device sends its response, the switch parses, extracts the Source MAC address, and stores it.

### Different types of requests

#### 1. Unicast
When a device intends for a message to be received by exactly one node. Includes the node's MAC address in its request.

#### 2. Multicast
When a device intends for multiple, but not all, nodes to receive its message. MAC address **group**, that devices subscribe to. You cannot pick multiple devices to send a message to unless they agree.

#### 3. Broadcast
All devices receive message. Uses MAC address `FF:FF:FF:FF:FF:FF`, which tells switch to route to all devices. Devices know to read data with this MAC address.

### Ethernet Frame

> *How is the transmitted data structured?*

The **Ethernet frame**  defines the lowest-level structure of how bits between computers are transferred.

Ethernet frames are structured with the following:

#### 1. Preamble
Syncs up receiver of data. Sometimes, nodes can have varying processing speeds, so they could read from the wire every 5ms instead of every 3ms. The preamble is a 7 byte alternating sequence of 0's and 1's: `01010101...` so that the receiving node can get ready for the rest of the frame.

The Starting Frame Delimiter is one byte marking where the preamble ends, by repeating 1 twice: `10101011`

#### 2. Destination MAC Address

#### 3. Source MAC Address

#### 4. VLAN
4 bytes, indicates if on Virtual LAN

#### 5. Ether-type field
2 bytes, describing protocol of payload:
- IPv4: `0x0800` or `0000 1000 0000 0000`
- IPv6: `0x86DD`, or `1000 0110 1101 1101`
- ARP: `0x0806`, or `0000 1000 0000 0110`


#### 6. Payload
46-1500 bytes

#### 7. Frame Check Sequence
4 bytes, checksum value for frame, calculated using Cyclic Redundancy Check

### Cyclic Redundancy Check
Does polynomial division, sets Frame Check Sequence to result.