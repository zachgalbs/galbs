---
title: The Transport and Application Layers
course: The Bits and Bytes of Computer Networking
module: 3
provider: Coursera (Google)
---

# Module 3: The Transport and Application Layers

Everything we've gone over so far has told us how to get data from one device to another device. The physical layer told us how to transmit data between two devices connected by a wire, the data link layer told us how to transmit data between two devices on the same network, and the network layer told us how to transmit data between two devices on separate networks.

The **transport layer** tells us what program the data goes to once it has arrived at a device. Since hosts can have multiple programs running, it's important to deliver the data to the correct one.

The **application layer** defines how two programs communicate with each other.

# The Transport Layer

At its core, the transport layer's job is to deliver data to programs running on devices. It stores information on which port to find the program, the computer uses that information to locate the program, and then data is transmitted between two programs.

### Multiplexing

Since on any given device there can be multiple programs running on it, there needs to be some way of logically separating the requests by the program requesting them. The transport layer uses **multiplexing** to do this. It takes the multiple output streams from programs on the device and combines them into one stream to be delivered.

**demultiplexing** happens on the receiving end. Devices can get tons of requests intended for their programs at once, so there needs to be a process of separating the traffic by port. Demultiplexing is the process of taking one input stream and separating it into multiple streams, delivered to the corresponding programs on the host.

## The TCP and UDP protocols

As you may have noticed, for the transport layer to work, we need more information, namely what port for the data to be transmitted to, what port it was sent from so that we can send data back, etc. All of this information is stored in the *data* section of the IP datagram.

### TCP

The Transmission Control Protocol is a connection-oriented protocol, and is reliable. It will establish a connection between two programs before sending data, and uses techniques to ensure that every TCP segment sent by one device is received by the other.

#### What information actually needs to be transmitted?

The important things that need to be transmitted include the **source port**, **destination port**, **sequence number**, **acknowledgement number**, **flags**, **checksum**, and the actual **data**.

> The sequence number is used when splitting transport layer requests: 3001 would mean '*this data starts at byte 3001 of the stream*'

> The flags are mostly used for the TCP protocol, to establish a connection using flags like ACK, SYN, and FIN. More on this later.

> The checksum is used to ensure no data was corrupted from the TCP header and the data.

#### Handshakes

To establish a connection between two programs, TCP performs a **three-way handshake**. First, the program that wants to initiate a connection sends a TCP segment with the SYN flag set to 1 (active), and sets the sequence number to a random number, called the Initial Sequence Number. This signifies the starting label for future segments. For example, if the sequence number is set to 4000, that means the next actual data-transmitting segment will be labelled 4001, then 4001 + payload length, etc.

After the SYN segment is sent, the receiving program sends back a TCP segment with both the SYN flag set to 1 and the ACK flag set to 1, signifying that it received the SYN segment and wants to synchronize. It sets the acknowledgement number to the sequence number sent + 1 (4001), and then generates its own ISN and attaches it to the sequence number field. Once this segment is received by the initial sender, a final ACK segment is sent with the ISN + 1. For example, if the recipient's ISN is 9000, the final ACK segment would have the acknowledgement number set to 9001.

After these three segments are sent, a connection is established. Future segments are identified with the source port, destination port, source IP, and destination IP. The sequence number is used to string back together TCP segments, but since the number starts randomized, it adds additional security since attackers can't manufacture a connected state with another program.

In addition to the three-way handshake, two programs need to end a connection with the four-way handshake so that they know to no longer store information about the other program, such as the expected next packet's position, whether it's seen the source port before, etc. To stop a connection, side A sends FIN, side B ACK's, side B sends FIN, and side A ACK's. Importantly, after side A sends FIN, side B can still send data. It's only when side A ACKs side B's FIN that the connection is truly closed.

### UDP

UDP is a connectionless protocol. It's similar to TCP in that it still includes the destination port and the source port, but it doesn't establish a connection between two devices, and isn't reliable. This means that data you send through UDP may not ever get to your destination.

> *Why would anyone use UDP then?*

Because it's **much** faster. Notice how to send one packet of data we have to send a baseline of seven segments back and forth. And beyond that segments sent must be ACK'ed. For certain applications, like video streaming or video games, you don't need every segment to make it to the recipient. If someone skips a frame on a YouTube video or someone has a bit of lag in a video game, that's acceptable.

## Ports

The port is similar to the IP address, just for programs. It's a 16 bit number used to identify a program on a host. Ranges of ports are used for different purposes:

0 - 1023: Reserved for standard services

1024 - 49151: User designated space

49152 - 65535: Ephemeral ports

## Sockets

A socket is just a collection of the device's IP, a program's port, and the status. For example, server sockets will have a status of LISTEN, meaning they're waiting for a SYN request. The status updates with the connection, so if the three-way handshake was completed, the status would be updated to ESTABLISHED. The socket isn't running any listen loop or anything, it's just a data structure used for the operating system to see what's going on at each port, and to deliver demux'ed data.

## Firewalls

A firewall is just a program or device that blocks or allows traffic based on rules. It usually filters by port, so that if you have a device connected to your network you can make it so that outside devices can only access certain open ports.
