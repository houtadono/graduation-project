import streamlit as st
import paramiko


# Hàm để kết nối SSH
def ssh_connect(hostname, username, password, port=22, private_key_path=None):
    try:
        # Khởi tạo SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Kết nối bằng mật khẩu hoặc khóa riêng
        if private_key_path:
            key = paramiko.RSAKey.from_private_key_file(private_key_path)
            client.connect(hostname, port=port, username=username, pkey=key)
        else:
            print(hostname, port, username, password)
            client.connect(hostname, port=port, username=username, password=password)

        return client
    except Exception as e:
        st.error(f"Kết nối thất bại: {e}")
        return None


# Giao diện Streamlit
st.title("Kết Nối SSH với Streamlit")

hostname = st.text_input("Địa chỉ IP hoặc tên miền của máy B:")
username = st.text_input("Tên người dùng:")
password = st.text_input("Mật khẩu:", type="password")
private_key_path = st.text_input("Đường dẫn đến khóa riêng (nếu có):")

if st.button("Kết nối"):
    if hostname and username:
        client = ssh_connect(hostname, username, password, private_key_path=private_key_path)
        if client:
            st.success("Kết nối thành công!")
            client.close()
