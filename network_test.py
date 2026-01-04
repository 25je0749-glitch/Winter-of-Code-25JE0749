#CODE FOR CONNECTIVITY TESTING

#! /usr/bin/env python3
from scapy.all import IP, ICMP, sr1

# 1. Send the packet and save the answer in 'reply'
# We tell Scapy to wait 2 seconds. If no answer, it moves on.
reply = sr1(IP(dst="10.98.127.179")/ICMP(), timeout=2, verbose=False)

# 2. Check if the 'reply' variable is empty or full
if reply:
    # 3. If it's full, we got a packet!
    print("I got a response!")
    print(reply.summary())
else:
    # 4. If it's None (empty), the timeout was reached
    print("No response from the server.")



