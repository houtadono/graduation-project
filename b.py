import ipaddress
import netflow
import socket
import struct

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

print(f"Tên máy: {hostname}")
print(f"Địa chỉ IP: {ip_address}")

# Khởi tạo socket UDP để lắng nghe
UDP_IP = "0.0.0.0"  # Lắng nghe trên mọi địa chỉ IP
UDP_PORT = 2055  # Cổng mặc định của NetFlow

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for NetFlow data on port {UDP_PORT}...")

while True:
    payload, client = sock.recvfrom(4096)  # Nhận dữ liệu NetFlow
    print(f"Received {len(payload)} bytes from {client}")

    try:
        # Giải mã gói NetFlow
        packet = netflow.parse_packet(payload)
        print(f"NetFlow Version: {packet.header.version}")
        print(f"Number of Flows: {len(packet.flows)}")
        print(f"System Uptime: {packet.header.uptime}")

        # Lặp qua các flows và in ra thông tin
        for flow in packet.flows:
            print(f"Flow:")
            # In ra địa chỉ IP nguồn và đích
            src_ip = ipaddress.ip_address(flow.IPV4_SRC_ADDR)
            dst_ip = ipaddress.ip_address(flow.IPV4_DST_ADDR)
            print(f"  Source IP: {src_ip}")
            print(f"  Destination IP: {dst_ip}")
            print(f"  Source Port: {flow.SRC_PORT}")
            print(f"  Destination Port: {flow.DST_PORT}")
            print(f"  Protocol: {flow.PROTO}")
            print(f"  Packets: {flow.IN_PACKETS}")  # Sử dụng IN_PACKETS
            print(f"  Bytes: {flow.IN_OCTETS}")  # Sử dụng IN_OCTETS
            print("------------")
    except Exception as e:
        print(f"Error decoding NetFlow data: {e}")