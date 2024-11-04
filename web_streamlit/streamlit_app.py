from collections import namedtuple
import random
import numpy as np
import streamlit as st
from pyvis.network import Network
import pandas as pd
from streamlit_option_menu import option_menu

# st.logo(
#     "python/api-examples-source/tutorials/dynamic-navigation/images/horizontal_blue.png",
#     icon_image="python/api-examples-source/tutorials/dynamic-navigation/images/icon_blue.png",
# )
st.set_page_config(layout="wide")

settings = st.Page("config/settings.py", title="Settings", icon=":material/settings:")
test = st.Page("config/test.py", title="Test", icon=":material/settings:")
ssh = st.Page("config/ssh.py", title="SSH", icon=":material/settings:")


live_data = st.Page("monitor/live_data.py", title="Live Data", icon=":material/ssid_chart:")


about = st.Page("info/about.py", title="About", icon=":material/info:")
support = st.Page("info/support.py", title="Support", icon=":material/assistant:")


pg = st.navigation({"System Configuration": [settings, test, ssh], "Monitoring & Analysis": [live_data],
                    "Alerts & Response": [], "Info & Support": [about, support]})
pg.run()