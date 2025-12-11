def page_hr_dashboard():
    import streamlit as st
    import pandas as pd
    import numpy as np
    import plotly.express as px
    import plotly.graph_objects as go

    
    st.title("📊 HR Dashboard (Demo)")

    # 1. Dữ liệu mẫu cho 8 chart
    np.random.seed(42)

    months = pd.date_range("2023-01-01", periods=12, freq="M").strftime("%Y-%m")
    departments = ["Sales", "IT", "HR", "Operation"]
    products = ["Product A", "Product B", "Product C"]

    # 1. Số lượng nhân viên theo thời gian
    df_headcount = pd.DataFrame({
        "Month": np.tile(months, len(departments)),
        "Dept": np.repeat(departments, len(months)),
        "Headcount": np.random.randint(12, 55, size=len(departments)*len(months))
    })

    # 2. Tỷ lệ nghỉ việc (attrition rate)
    df_attrition = pd.DataFrame({
        "Month": months,
        "AttritionRate": np.random.uniform(5, 12, size=len(months)).round(2)
    })

    # 3. Tổng lương & phụ cấp từng tháng
    df_pay = pd.DataFrame({
        "Month": months,
        "Salary": np.random.uniform(180, 260, size=len(months)).round(1),      # triệu VND
        "Allowance": np.random.uniform(30, 55, size=len(months)).round(1)
    })

    # 4. Tổng OT & Ngày phép đã dùng
    df_ot_leave = pd.DataFrame({
        "Month": months,
        "OT Hours": np.random.randint(100, 210, size=len(months)),
        "Leave Days": np.random.randint(30, 70, size=len(months))
    })

    # 5. Retention rate & Top talent retention
    df_retention = pd.DataFrame({
        "Month": months,
        "RetentionRate": np.random.uniform(85, 95, size=len(months)).round(1),
        "KeyTalentRetention": np.random.uniform(90, 99, size=len(months)).round(1),
    })

    # 6. Năng suất bình quân (Revenue/Employee)
    df_productivity = pd.DataFrame({
        "Dept": departments,
        "RevenuePerEmp": np.random.randint(220, 370, size=len(departments))
    })

    # 7. So sánh lương thực tế vs. Benchmark
    df_salary_cmp = pd.DataFrame({
        "Dept": departments,
        "Actual": np.random.randint(17, 25, size=len(departments)),
        "Benchmark": np.random.randint(20, 23, size=len(departments))
    })

    # 8. Tuyển mới theo kỳ (Hires)
    df_hire = pd.DataFrame({
        "Month": months,
        "Hires": np.random.randint(3, 14, size=len(months))
    })

    # Layout lưới: 2 hàng × 4 cột
    row1 = st.columns(4)
    row2 = st.columns(4)

    # ---- Row 1 ----

    with row1[0]:
        st.subheader("Nhân viên theo thời gian")
        fig1 = px.bar(df_headcount, x="Month", y="Headcount", color="Dept", barmode="group", height=330)
        fig1.update_layout(legend_title_text="Phòng ban", hovermode="x unified")
        st.plotly_chart(fig1, use_container_width=True)

    with row1[1]:
        st.subheader("Tỷ lệ nghỉ việc (%)")
        fig2 = px.line(df_attrition, x="Month", y="AttritionRate", markers=True, height=330)
        fig2.update_traces(mode="lines+markers", line=dict(width=3), marker=dict(size=10, color="#d62728"))
        fig2.update_yaxes(range=[0, 15])
        st.plotly_chart(fig2, use_container_width=True)

    with row1[2]:
        st.subheader("Tổng lương & phụ cấp (triệu)")
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=df_pay["Month"], y=df_pay["Salary"], name="Lương cơ bản"))
        fig3.add_trace(go.Bar(x=df_pay["Month"], y=df_pay["Allowance"], name="Phụ cấp"))
        fig3.update_layout(barmode="stack", hovermode="x unified", height=330)
        st.plotly_chart(fig3, use_container_width=True)

    with row1[3]:
        st.subheader("Tổng OT & Ngày phép đã dùng")
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(x=df_ot_leave["Month"], y=df_ot_leave["OT Hours"], name="OT (giờ)", marker_color="#636EFA"))
        fig4.add_trace(go.Bar(x=df_ot_leave["Month"], y=df_ot_leave["Leave Days"], name="Ngày phép", marker_color="#FECB52"))
        fig4.update_layout(barmode="group", hovermode="x unified", height=330)
        st.plotly_chart(fig4, use_container_width=True)

    # ---- Row 2 ----

    with row2[0]:
        st.subheader("Retention/Key Talent (%)")
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(x=df_retention["Month"], y=df_retention["RetentionRate"], mode='lines+markers', name="Tổng thể", line=dict(width=3)))
        fig5.add_trace(go.Scatter(x=df_retention["Month"], y=df_retention["KeyTalentRetention"], mode='lines+markers', name="Key Talent", line=dict(width=3, dash="dot")))
        fig5.update_yaxes(range=[80, 100])
        fig5.update_layout(hovermode="x unified", height=330)
        st.plotly_chart(fig5, use_container_width=True)

    with row2[1]:
        st.subheader("Năng suất bình quân (tr/phòng)")
        fig6 = px.bar(df_productivity, x="Dept", y="RevenuePerEmp", text_auto=True, color="Dept", height=330)
        fig6.update_traces(marker_line_width=2)
        fig6.update_layout(showlegend=False, yaxis_title="Triệu VND/người")
        st.plotly_chart(fig6, use_container_width=True)

    with row2[2]:
        st.subheader("So sánh lương thực tế vs. Benchmark")
        fig7 = go.Figure()
        fig7.add_trace(go.Bar(x=df_salary_cmp["Dept"], y=df_salary_cmp["Actual"], name="Thực tế", marker_color="#00b894"))
        fig7.add_trace(go.Bar(x=df_salary_cmp["Dept"], y=df_salary_cmp["Benchmark"], name="Benchmark", marker_color="#636EFA"))
        fig7.update_layout(barmode="group", hovermode="x", height=330)
        st.plotly_chart(fig7, use_container_width=True)

    with row2[3]:
        st.subheader("Số lượng tuyển mới theo tháng")
        fig8 = px.bar(df_hire, x="Month", y="Hires", color="Hires", height=330, color_continuous_scale="Purp")
        fig8.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig8, use_container_width=True)

    # --- Footer ---
    st.caption("Demo dashboard HR | Số liệu mô phỏng, mọi chart động, hover đẹp mắt, native Plotly + Streamlit. Bạn hoàn toàn có thể thay dữ liệu thực tế.")
