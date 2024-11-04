import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


# Tạo dữ liệu giả lập
def generate_fake_netflow_data(num_data_points):
    timestamps = pd.date_range(start='2024-01-01', periods=num_data_points, freq='min')
    data = {
        "timestamp": timestamps,
        "inbound_traffic": np.random.uniform(0, 10, num_data_points),  # Mbit/s
        "outbound_traffic": np.random.uniform(0, 5, num_data_points),  # Mbit/s
    }
    return pd.DataFrame(data)


# Hàm tạo đồ thị Plotly
def create_traffic_plot(data, title, avg_in, avg_out, max_in, max_out):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=data['timestamp'], y=data['inbound_traffic'], mode='lines', name='Inbound Traffic (Mb/s)',
                   line=dict(color='green')))
    fig.add_trace(
        go.Scatter(x=data['timestamp'], y=data['outbound_traffic'], mode='lines', name='Outbound Traffic (Mb/s)',
                   line=dict(color='blue')))

    # Thêm max và avg
    fig.add_trace(go.Scatter(x=[data['timestamp'].min(), data['timestamp'].max()],
                             y=[avg_in, avg_in], mode='lines', name=f'Avg In ({avg_in} Mb)',
                             line=dict(dash='dash', color='green')))

    fig.add_trace(go.Scatter(x=[data['timestamp'].min(), data['timestamp'].max()],
                             y=[avg_out, avg_out], mode='lines', name=f'Avg Out ({avg_out} Mb)',
                             line=dict(dash='dash', color='blue')))

    fig.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title="Traffic (Mb/s)",
        legend_title="Legend",
    )

    return fig


# Tạo dữ liệu giả lập
num_data_points = 288  # Số lượng điểm dữ liệu (5 phút = 288 điểm trong ngày)
data = generate_fake_netflow_data(num_data_points)

# Tính toán giá trị trung bình và max
avg_in = data['inbound_traffic'].mean()
avg_out = data['outbound_traffic'].mean()
max_in = data['inbound_traffic'].max()
max_out = data['outbound_traffic'].max()

# Streamlit UI
st.title("Network Traffic Monitoring")

# Tạo đồ thị "Daily"
st.subheader("Daily Traffic (5 Minute Average)")
daily_plot = create_traffic_plot(data, "Daily Traffic (5 Minute Average)", avg_in, avg_out, max_in, max_out)
st.plotly_chart(daily_plot)

# Tạo dữ liệu hàng tuần (30 phút trung bình)
weekly_data = generate_fake_netflow_data(48)  # Số lượng điểm dữ liệu cho hàng tuần
avg_in_weekly = weekly_data['inbound_traffic'].mean()
avg_out_weekly = weekly_data['outbound_traffic'].mean()
max_in_weekly = weekly_data['inbound_traffic'].max()
max_out_weekly = weekly_data['outbound_traffic'].max()

st.subheader("Weekly Traffic (30 Minute Average)")
weekly_plot = create_traffic_plot(weekly_data, "Weekly Traffic (30 Minute Average)", avg_in_weekly, avg_out_weekly,
                                  max_in_weekly, max_out_weekly)
st.plotly_chart(weekly_plot)

# Tạo dữ liệu hàng tháng (2 giờ trung bình)
monthly_data = generate_fake_netflow_data(60)  # Số lượng điểm dữ liệu cho hàng tháng
avg_in_monthly = monthly_data['inbound_traffic'].mean()
avg_out_monthly = monthly_data['outbound_traffic'].mean()
max_in_monthly = monthly_data['inbound_traffic'].max()
max_out_monthly = monthly_data['outbound_traffic'].max()

st.subheader("Monthly Traffic (2 Hour Average)")
monthly_plot = create_traffic_plot(monthly_data, "Monthly Traffic (2 Hour Average)", avg_in_monthly, avg_out_monthly,
                                   max_in_monthly, max_out_monthly)
st.plotly_chart(monthly_plot)

# Tạo dữ liệu hàng năm (1 ngày trung bình)
yearly_data = generate_fake_netflow_data(365)  # Số lượng điểm dữ liệu cho hàng năm
avg_in_yearly = yearly_data['inbound_traffic'].mean()
avg_out_yearly = yearly_data['outbound_traffic'].mean()
max_in_yearly = yearly_data['inbound_traffic'].max()
max_out_yearly = yearly_data['outbound_traffic'].max()

st.subheader("Yearly Traffic (1 Day Average)")
yearly_plot = create_traffic_plot(yearly_data, "Yearly Traffic (1 Day Average)", avg_in_yearly, avg_out_yearly,
                                  max_in_yearly, max_out_yearly)
st.plotly_chart(yearly_plot)
