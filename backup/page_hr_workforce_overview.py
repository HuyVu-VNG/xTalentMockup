def page_hr_workforce_overview():
    import streamlit as st
    import pandas as pd
    import plotly.graph_objs as go
    import numpy as np

    
    st.title("Tổng quan nhân sự (Workforce Overview)")

    # --- Dummy Data ---
    quarters = ['2023 Q1','2023 Q2','2023 Q3','2023 Q4','2024 Q1']
    business_units = ['BU1', 'BU2', 'BU3', 'BU4']

    # 1. Headcount (pie + value)
    headcount = [300, 220, 190, 140]
    headcount_labels = business_units
    headcount_total = sum(headcount)
    headcount_target = 900
    headcount_pct = headcount_total / headcount_target * 100

    # 2. Annualized Retention (bar by grade)
    grades = ['M1', 'M2', 'M3', 'M4', 'M5']
    retention = [88, 91, 85, 86, 82]
    retention_target = 90

    # 3. Top Talent Retention (heatmap-like table)
    perf_levels = ['Low', 'Medium', 'High']
    potential_levels = ['Low', 'Medium', 'High']
    top_talent_matrix = [
        [67, 78, 84],
        [81, 65, 82],
        [88, 86, 75]
    ]
    # 4. Average Tenure (bar)
    tenure_buckets = ['<1y', '1-2y', '3-5y', '6-10y', '>10y']
    tenure_counts = [60, 120, 300, 200, 100]
    avg_tenure = np.round(np.average([0.5, 1.5, 4, 8, 12], weights=tenure_counts),2)

    # 5. Female Gender Ratio (area/line)
    female_pct = [38, 40, 39, 41, 41]
    female_target = 50

    # 6. Span of Control (bar by BU)
    span_bu = business_units
    span_values = [8, 10, 12, 7]
    avg_span = np.round(np.mean(span_values),2)

    # 7. Compa Ratio (scatter)
    compa_ratio = np.random.normal(0.75, 0.05, 30)
    perf_rating = np.random.randint(1, 5, 30)
    compa_target = 0.80

    # 8. Hires (bar by manager)
    hires_managers = ['Manager A','Manager B','Manager C','Manager D','Manager E']
    hires_values = [120, 98, 110, 80, 79]
    hires_total = sum(hires_values)
    hires_target = 600

    # --- Layout: 2 hàng x 4 chart ---
    col1, col2, col3, col4 = st.columns(4)

    # 1. Headcount Pie + Value
    with col1:
        st.metric("Headcount", f"{headcount_total:,}", f"{headcount_pct:.1f}% of Target")
        fig1 = go.Figure(data=[go.Pie(labels=headcount_labels, values=headcount, hole=.4)])
        fig1.update_traces(textinfo='label+percent', showlegend=False)
        fig1.update_layout(margin=dict(t=5,b=5,l=5,r=5), height=220)
        st.plotly_chart(fig1, use_container_width=True)

    # 2. Annualized Retention (bar by grade)
    with col2:
        st.metric("Annualized Retention", f"{np.mean(retention):.0f}%", f"{int(np.mean(retention)-retention_target)}% vs Target")
        fig2 = go.Figure(data=[go.Bar(x=grades, y=retention, marker_color='teal')])
        fig2.update_layout(margin=dict(t=5,b=5,l=5,r=5), yaxis=dict(range=[0,100]), height=220)
        st.plotly_chart(fig2, use_container_width=True)

    # 3. Top Talent Retention (heatmap-like table)
    with col3:
        st.metric("Top Talent Retention", "75%", "vs Target 83.5%")
        z = top_talent_matrix
        fig3 = go.Figure(data=go.Heatmap(
            z=z, x=potential_levels, y=perf_levels, colorscale='YlGn', showscale=False,
            hovertemplate="Performance: %{y}<br>Potential: %{x}<br>Retention: %{z}%"
        ))
        fig3.update_layout(
            yaxis_title="Performance",
            xaxis_title="Potential",
            margin=dict(t=5,b=5,l=5,r=5), height=220
        )
        st.plotly_chart(fig3, use_container_width=True)

    # 4. Average Tenure (bar)
    with col4:
        st.metric("Average Tenure", f"{avg_tenure:.2f} years")
        fig4 = go.Figure(data=[go.Bar(
            x=tenure_buckets, y=tenure_counts, marker_color='darkslateblue'
        )])
        fig4.update_layout(margin=dict(t=5,b=5,l=5,r=5), height=220)
        st.plotly_chart(fig4, use_container_width=True)

    col5, col6, col7, col8 = st.columns(4)

    # 5. Female Gender Ratio (area)
    with col5:
        st.metric("Female Gender Ratio", f"{female_pct[-1]}%", f"{(female_pct[-1]/female_target*100):.1f}% of Target")
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(
            x=quarters, y=female_pct, fill='tozeroy', mode='lines+markers', line_color='deeppink'
        ))
        fig5.update_layout(margin=dict(t=5,b=5,l=5,r=5), height=220)
        st.plotly_chart(fig5, use_container_width=True)

    # 6. Span of Control (bar by BU)
    with col6:
        st.metric("Span of Control", f"{avg_span}")
        fig6 = go.Figure(data=[go.Bar(
            y=span_bu, x=span_values, orientation='h', marker_color='darkgreen'
        )])
        fig6.update_layout(margin=dict(t=5,b=5,l=5,r=5), height=220, yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig6, use_container_width=True)

    # 7. Compa Ratio (scatter vs rating)
    with col7:
        st.metric("Compa Ratio", f"{np.mean(compa_ratio):.2f}", f"{(np.mean(compa_ratio)/compa_target*100):.1f}% of Target")
        fig7 = go.Figure(data=[go.Scatter(
            x=perf_rating, y=compa_ratio,
            mode='markers',
            marker=dict(size=14, color=perf_rating, colorscale='Viridis', showscale=True),
        )])
        fig7.update_layout(margin=dict(t=5,b=5,l=5,r=5), height=220, xaxis_title="Performance Rating", yaxis_title="Compa Ratio")
        st.plotly_chart(fig7, use_container_width=True)

    # 8. Hires (bar by manager)
    with col8:
        st.metric("Hires", f"{hires_total}", f"{(hires_total/hires_target*100):.1f}% of Target")
        fig8 = go.Figure(data=[go.Bar(
            x=hires_managers, y=hires_values, marker_color='purple'
        )])
        fig8.update_layout(margin=dict(t=5,b=5,l=5,r=5), height=220)
        st.plotly_chart(fig8, use_container_width=True)

    # Gợi ý: Thêm chart nào nữa?
    # - Distribution by Age Group
    # - Department Size
    # - Average Performance
    # - Absence/Ot Trend
    # Nếu cần, bạn chỉ việc thêm col9, col10, ... và block chart tương ứng.
        # ======= DÒNG MỚI: 4 chart tiếp theo =======
    col9, col10, col11, col12 = st.columns(4)

    # 9. Distribution by Age Group
    with col9:
        age_groups = ['<25', '25-30', '31-35', '36-40', '>40']
        age_counts = [45, 110, 185, 80, 40]
        fig9 = go.Figure(data=[go.Bar(
            x=age_groups, y=age_counts, marker_color='skyblue'
        )])
        fig9.update_layout(
            title="Phân bổ theo nhóm tuổi",
            margin=dict(t=30, b=5, l=5, r=5), height=220,
            yaxis_title="Số lượng"
        )
        st.plotly_chart(fig9, use_container_width=True)

    # 10. Department Size
    with col10:
        departments = ['HCNS', 'Tài chính', 'Kinh doanh', 'IT', 'Dự án']
        dept_size = [70, 55, 120, 42, 78]
        fig10 = go.Figure(data=[go.Bar(
            x=departments, y=dept_size, marker_color='coral'
        )])
        fig10.update_layout(
            title="Quy mô phòng ban",
            margin=dict(t=30, b=5, l=5, r=5), height=220,
            yaxis_title="Nhân sự"
        )
        st.plotly_chart(fig10, use_container_width=True)

    # 11. Average Performance by Department
    with col11:
        avg_perf = [86, 84, 78, 90, 80]
        fig11 = go.Figure(data=[go.Bar(
            x=departments, y=avg_perf, marker_color='seagreen'
        )])
        fig11.update_layout(
            title="Hiệu suất TB theo phòng",
            margin=dict(t=30, b=5, l=5, r=5), height=220,
            yaxis_title="Điểm KPI"
        )
        st.plotly_chart(fig11, use_container_width=True)

    # 12. Absence/OT Trend
    with col12:
        months = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']
        absences = [15, 22, 20, 16, 18, 14]
        ot_hours = [34, 45, 42, 38, 51, 40]
        fig12 = go.Figure()
        fig12.add_trace(go.Scatter(x=months, y=absences, mode='lines+markers', name='Absence', line_color='red'))
        fig12.add_trace(go.Scatter(x=months, y=ot_hours, mode='lines+markers', name='OT Hours', line_color='blue'))
        fig12.update_layout(
            title="Xu hướng ngày nghỉ & OT",
            margin=dict(t=30, b=5, l=5, r=5), height=220,
            yaxis_title="Số ngày/Giờ"
        )
        st.plotly_chart(fig12, use_container_width=True)

    st.caption("🟢 Số liệu demo. Khi triển khai thực tế, bạn kết nối dữ liệu HR thực tế hoặc BI query vào block này.")

# -- Để test thử standalone, bạn chỉ cần gọi:
if __name__ == "__main__":
    page_hr_overview()
