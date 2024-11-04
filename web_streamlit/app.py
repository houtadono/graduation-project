from collections import namedtuple
import random
import numpy as np
import streamlit as st
from pyvis.network import Network
import pandas as pd
from streamlit_option_menu import option_menu

def create_graph_from_data(df):
    net = Network(width="100%", height="600px", directed=True)
    net.set_options("""
            const options = {
  "nodes": {
    "borderWidth": 2,
    "borderWidthSelected": 4,
    "opacity": 1,
    "physics": true
  },
  "edges": {
    "smooth": {
      "type": "continuous",
      "forceDirection": "none"
    }
  },
    "interaction": {
    "dragNodes": true,
    "dragView": true,
    "hideEdgesOnDrag": false,
    "hideEdgesOnZoom": false,
    "multiselect": true,
    "navigationButtons": true
  },
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -40000,
      "springLength": 200,
      "springConstant": 0.001
    }
  }
}
            """)

    for index, row in df.iterrows():
        src_ip = row['IPV4_SRC_ADDR']
        dst_ip = row['IPV4_DST_ADDR']
        src_port = row['L4_SRC_PORT']
        dst_port = row['L4_DST_PORT']
        protocol = row['PROTOCOL']

        net.add_node(src_ip, label=src_ip, title=f"Source IP: {src_ip}", font={'size': 4})
        net.add_node(dst_ip, label=dst_ip, title=f"Destination IP: {dst_ip}", font={'size': 4})
        net.add_edge(str(src_ip), dst_ip, label=f"src_port: {src_port}, dst_port: {dst_port}, protocol: {protocol}",
                     font={'size': 4})
    return net


# Lưu đồ thị vào file HTML và hiển thị trong Streamlit
def display_graph(net):
    net.save_graph('netflow_graph.html')

    html_with_js = open('netflow_graph.html', 'r').read().replace(
        '</body>', '</body>'
        # f'<script type="text/javascript"> {open("graph_script.js", "r").read()}</script></body>'
    )

    st.components.v1.html(html_with_js, height=600)


@st.cache_data
def load_data():
    data = pd.read_csv('data/NF-UNSW-NB15.csv')
    # print(data.duplicated().sum(), "fully duplicate rows to remove")
    # data.drop_duplicates(inplace=True)
    # data.reset_index(inplace=True, drop=True)
    return data


def main():
    st.set_page_config(layout="wide")
    with st.sidebar:
        selected = option_menu("Main Menu", ["Home", 'Settings'],
                               icons=['house', 'gear'], menu_icon="cast", default_index=1)

    st.title("NetFlow Graph Visualization")
    st.sidebar.header("Selected Information")
    node_info_placeholder = st.sidebar.empty()

    data = load_data()
    num_packets = st.slider("Number of Packets to Visualize", 10, 10000, 50)
    if st.button("Generate and Visualize"):
        net = create_graph_from_data(data.iloc[:num_packets, :])
        display_graph(net)
        node_info_placeholder.markdown('<div id="node_info_placeholder">No node selected yet</div>', unsafe_allow_html=True)




if __name__ == "__main__":
    main()
