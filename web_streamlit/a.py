import ipaddress
import netflow
import socket
import time
from datetime import datetime, timedelta

# Tạo dict lưu templates
templates = {}

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
        # Lấy thời gian hiện tại
        current_time = datetime.now()

        # Giải mã gói NetFlow
        packet = netflow.parse_packet(payload, templates=templates)

        if packet.header.version == 9:  # Xử lý NetFlow v9
            print(f"NetFlow Version: {packet.header.version}")
            print(f"Number of Flows: {len(packet.flows)}")

            # Lưu template nếu có
            if packet.header.is_template:
                print(f"Template received: {packet.header.template_id}")
                templates[packet.header.template_id] = packet

            # Lấy thời gian khởi động thiết bị (bằng cách trừ uptime từ thời gian hiện tại)
            uptime_ms = packet.header.uptime  # Uptime tính bằng mili giây
            uptime_delta = timedelta(milliseconds=uptime_ms)
            flow_real_time = current_time - uptime_delta

            print(f"Thời gian thực của gói tin: {flow_real_time.strftime('%Y-%m-%d %H:%M:%S')}")

            # Lặp qua các flows và in ra thông tin
            for flow in packet.flows:
                print(f"Flow:")
                src_ip = ipaddress.ip_address(flow.IPV4_SRC_ADDR)
                dst_ip = ipaddress.ip_address(flow.IPV4_DST_ADDR)
                print(f"  Source IP: {src_ip}")
                print(f"  Destination IP: {dst_ip}")
                print(f"  Source Port: {flow.SRC_PORT}")
                print(f"  Destination Port: {flow.DST_PORT}")
                print(f"  Protocol: {flow.PROTO}")
                print(f"  Packets: {flow.IN_PACKETS}")
                print(f"  Bytes: {flow.IN_OCTETS}")
                print("------------")
        else:
            print(f"Unsupported NetFlow version: {packet.header.version}")

    except Exception as e:
        print(f"Error decoding NetFlow data: {e}")
