import streamlit as st
import os

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
if 'exporters' not in st.session_state:
    st.session_state['exporters'] = []
    # st.session_state['exporters'].expand(exporters)

cols = st.columns(6)
headers = ["IP Address", "Interface", "Port", "Status"]
for col, header in zip(cols, headers):
    col.write(header)

@st.dialog("Update exporter")
def update_exporter(index: int):
    ip = st.text_input("IP Address", value=st.session_state['exporters'][index]["ip"])
    interface = st.text_input("Interface", value=st.session_state['exporters'][index]["net_interface"])
    port = st.text_input("Port", value=st.session_state['exporters'][index]["port"])

    if st.button("Submit"):
        st.session_state['exporters'][index] = dict({"ip": ip, "net_interface": interface, "port": port, "status": "Inactive"})
        st.rerun()

for i, exporter in enumerate(st.session_state['exporters']):
    cols = st.columns(6)
    cols[0].write(exporter["ip"])
    cols[1].write(exporter["net_interface"])
    cols[2].write(exporter["port"])
    cols[3].write(exporter["status"])

    if cols[4].button("Edit", key=f"edit_{i}", icon=":material/edit:"):
        update_exporter(i)

    if cols[5].button("Refresh", key=f"refresh_{i}", icon=":material/cached:"):
        st.toast('Your edited image was saved!', icon='😍')
        st.write(f"Refreshing status for {exporter['ip']}")

if st.button("Add Exporter", icon=":material/add_circle:"):
    @st.dialog("Add exporter")
    def add_exporter(item):
        new_ip = st.text_input("New Exporter IP")
        new_interface = st.text_input("New Interface")
        new_port = st.text_input("New Port")
        if st.button("Submit"):
            st.session_state['exporters'].append(
                {"ip": new_ip, "net_interface": new_interface, "port": new_port, "status": "Inactive"})
            st.rerun()
    add_exporter(1)
