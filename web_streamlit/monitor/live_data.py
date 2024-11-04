import streamlit as st
import pandas as pd
import numpy as np
import time


# Giả lập dữ liệu mạng
def generate_fake_data(num_packets):
    src_ips = [f"192.168.1.{i}" for i in range(1, 10)]
    dst_ips = [f"192.168.1.{i}" for i in range(10, 20)]
    data = {
        "src_ip": np.random.choice(src_ips, num_packets),
        "dst_ip": np.random.choice(dst_ips, num_packets),
        "src_port": np.random.randint(1024, 65535, num_packets),
        "dst_port": np.random.randint(1024, 65535, num_packets),
        "timestamp": pd.date_range(start='2024-01-01', periods=num_packets, freq='s'),
        "protocol": np.random.choice(['TCP', 'UDP'], num_packets),
        "byte_size": np.random.randint(50, 1500, num_packets)
    }
    return pd.DataFrame(data)


# Tiêu đề trang
st.title("Live Network Data")
num_packets = st.slider("Select number of packets to display", 1, 100, 10)
st.subheader("Network Data Stream")

data_placeholder = st.empty()
while True:
    network_data = generate_fake_data(num_packets)
    with data_placeholder.container():
        st.line_chart(network_data.set_index('timestamp')['byte_size'])
        st.dataframe(network_data)
    time.sleep(2)
