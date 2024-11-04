import os
import pandas as pd
import streamlit as st
import paramiko

def check_exporter_status(ip, username="root"):
    return 1
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username)

        stdin, stdout, stderr = client.exec_command('pgrep fprobe')
        status = stdout.read().decode().strip()
        client.close()

        if status:
            return "Running"
        else:
            return "Stopped"
    except Exception as e:
        return f"Error: {e}"


st.title("NetFlow Collector & Exporter Configuration")

# Section 1: Configure nfdump (collector)
st.header("Collector Configuration (nfdump)")
collector_port = st.text_input("Collector Port", value="2055")
nfdump_dir = st.text_input("Log Directory for nfdump", value="/var/log/netflow")

if st.button("Apply Collector Configuration"):
    # Command to start nfdump with user inputs
    nfdump_command = f"sudo nfcapd -w -D -p {collector_port} -l {nfdump_dir}"
    os.system(nfdump_command)
    st.success(f"Collector started on port {collector_port} and logs in {nfdump_dir}")

# Section 2: Configure Exporters
st.header("Add Exporter Configuration")
exporter_ip = st.text_input("Exporter IP", value="192.168.1.101")
exporter_interface = st.text_input("Exporter Network Interface", value="eth0")
exporter_port = st.text_input("Exporter Port", value="2055")

# List to store exporter details
if 'exporters' not in st.session_state:
    st.session_state['exporters'] = []

if st.button("Add Exporter"):
    # Store exporter info
    st.session_state['exporters'].append({
        "ip": exporter_ip,
        "interface": exporter_interface,
        "port": exporter_port,
        "status": "Unknown"
    })
    st.success(f"Exporter added: {exporter_ip} ({exporter_interface}) on port {exporter_port}")

# Section 3: View Exporters in Table
st.header("Current Exporters")
if len(st.session_state.get('exporters', [])) > 0:
    # Convert exporters list to pandas DataFrame
    exporters_df = pd.DataFrame(st.session_state['exporters'])

    # Check status of each exporter
    for index, exporter in exporters_df.iterrows():
        status = check_exporter_status(exporter['ip'])
        exporters_df.at[index, 'status'] = status
        # Add unique key for each button
        exporters_df.at[index, 'bt'] = st.button('New', key=f"new_btn_{index}")

    # Display table of exporters
    st.dataframe(exporters_df)

else:
    st.write("No exporters added.")

# Apply exporter configurations
if st.button("Apply Exporter Configurations"):
    for exporter in st.session_state['exporters']:
        # Command to start fprobe on each exporter
        fprobe_command = f"ssh root@{exporter['ip']} sudo fprobe -i {exporter['interface']} {exporter_ip}:{exporter['port']}"
        os.system(fprobe_command)
        st.success(
            f"fprobe started on {exporter['ip']} with interface {exporter['interface']} and port {exporter['port']}")
