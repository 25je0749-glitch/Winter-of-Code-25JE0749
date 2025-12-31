# Import Scapy capabilities
from scapy.all import *

print("Scapy is starting... Waiting for traffic...")

# The sniffing command you learned
# We use iface=None to let Scapy pick the default (since we set it up earlier)
# or you can specifically use the index if needed.
sniff(count=5, prn=lambda x: x.summary())

print("Done! Captured 5 packets.")
