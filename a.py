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

# Hàm giải mã header của NetFlow
def decode_netflow_header(data):
    # NetFlow v5 header có độ dài 20 bytes
    header_format = "!HHIIII"  # Định dạng của header NetFlow v5
    if len(data) < 20:
        print("Received data is too short for NetFlow v5 header")
        return

    version, count, sys_uptime, unix_secs, unix_nsecs, flow_sequence = struct.unpack(header_format, data[:20])
    
    print(f"NetFlow Version: {version}")
    print(f"Number of Flows: {count}")
    print(f"System Uptime: {sys_uptime}")
    print(f"Unix Seconds: {unix_secs}")
    print(f"Unix Nanoseconds: {unix_nsecs}")
    print(f"Flow Sequence: {flow_sequence}")

# Lắng nghe và xử lý gói NetFlow
while True:
    data, addr = sock.recvfrom(4096)  # Nhận gói tin từ máy gửi NetFlow
    print(f"Received data from {addr}")
    decode_netflow_header(data)