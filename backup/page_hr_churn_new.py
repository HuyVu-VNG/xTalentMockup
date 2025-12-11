def page_hr_churn_new():
    import streamlit as st
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    import numpy as np

    st.title("📈 Dashboard Biến Động Nhân Sự")

    # --------------- MOCKUP DATA ---------------
    periods = [f'2023-Q{i}' for i in range(1, 5)] + [f'2024-Q{i}' for i in range(1, 3)]

    # 1. Headcount change
    headcount = [520, 538, 548, 530, 545, 552]
    hire = [30, 28, 25, 35, 32, 30]
    exit = [12, 18, 15, 20, 17, 18]
    net_move = [h-e for h,e in zip(hire, exit)]

    # 2. Attrition/churn trend
    attrition_rate = [2.2, 3.4, 2.7, 3.8, 3.2, 3.1]

    # 3. Hire trend
    hire_type = pd.DataFrame({
        "period": periods,
        "Hiring": hire,
        "Internal Move": [6, 5, 7, 8, 9, 10],
        "Backfill": [10, 13, 10, 15, 10, 12]
    })

    # 4. Turnover voluntary/involuntary
    turnover = pd.DataFrame({
        "period": periods,
        "Voluntary": [7, 11, 8, 12, 11, 12],
        "Involuntary": [5, 7, 7, 8, 6, 6]
    })

    # 5. Tenure distribution of exit
    exit_tenure = pd.DataFrame({
        "Tenure": ["<1y", "1-3y", "3-5y", "5-10y", "10y+"],
        "Exit": [8, 17, 14, 7, 5]
    })

    # 6. Internal Mobility (transfer/promote)
    mobility = pd.DataFrame({
        "Type": ["Promote", "Transfer", "Demote", "Concurrent"],
        "Count": [7, 10, 2, 5]
    })

    # 7. Department Movement
    dept_move = pd.DataFrame({
        "Department": ["HCNS", "IT", "Kinh doanh", "Kế toán", "QA"],
        "Join": [5, 6, 12, 4, 3],
        "Leave": [3, 5, 7, 3, 2]
    })

    # 8. Replacement rate
    replacement_rate = [90, 120, 88, 105, 110, 97]

    # 9. Key Talent Movement
    keytalent_move = pd.DataFrame({
        "period": periods,
        "New": [2, 3, 1, 3, 2, 3],
        "Exit": [1, 1, 0, 2, 1, 0]
    })

    # 10. Backfill vs New position
    backfill_new = pd.DataFrame({
        "period": periods,
        "Backfill": [10, 13, 10, 15, 10, 12],
        "New": [5, 4, 7, 5, 7, 6]
    })

    # 11. Average Time to Fill
    avg_fill = pd.DataFrame({
        "period": periods,
        "Avg days": [32, 28, 34, 30, 26, 27]
    })

    # 12. Resignation Reason Breakdown
    reasons = pd.DataFrame({
        "Reason": ["Tìm cơ hội tốt hơn", "Thu nhập", "Môi trường", "Gia đình", "Khác"],
        "Count": [18, 14, 10, 7, 4]
    })

    # 13. Promotion/Demotion Trend
    promote_demote = pd.DataFrame({
        "period": periods,
        "Promote": [4, 5, 3, 6, 4, 5],
        "Demote": [1, 0, 2, 1, 2, 1]
    })

    # 14. Absence Trend around attrition
    absence = pd.DataFrame({
        "month": ["-3", "-2", "-1", "Exit", "+1"],
        "Absence Days": [2.0, 2.4, 4.8, 5.2, 0.5]
    })

    # 15. Diversity of Movement
    diversity = pd.DataFrame({
        "Group": ["Nam", "Nữ", "Dưới 30", "30-40", "Trên 40"],
        "Join": [16, 14, 10, 12, 8],
        "Leave": [10, 8, 7, 6, 5]
    })

    # 16. Rehire Rate
    rehire = pd.DataFrame({
        "period": periods,
        "Rehire": [1, 2, 0, 1, 1, 2]
    })

    # 17. Exit interview completion
    exit_interview = pd.DataFrame({
        "period": periods,
        "Completion Rate": [70, 75, 90, 95, 92, 93]
    })

    # 18. Waterfall Headcount Change
    waterfall = go.Figure(go.Waterfall(
        x=["Start", "Hires", "Internal Move", "Exit", "Net"],
        y=[520, 30, 8, -17, 541],
        measure=["absolute", "relative", "relative", "relative", "total"]
    ))

    # ============== CHARTS ==============

    row = st.columns(3)
    with row[0]:
        # 1. Headcount Change (Bar)
        fig = px.bar(x=periods, y=headcount, title="Headcount by Period")
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    with row[1]:
        # 2. Attrition Trend
        fig = px.line(x=periods, y=attrition_rate, markers=True, title="Attrition Rate (%)")
        fig.update_traces(line_color='orange')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    with row[2]:
        # 3. Hire Trend
        fig = px.bar(hire_type, x="period", y=["Hiring", "Internal Move", "Backfill"], barmode="group",
                    title="Hiring/Move/Backfill")
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    row = st.columns(3)
    with row[0]:
        # 4. Turnover Voluntary/Involuntary
        fig = px.bar(turnover, x="period", y=["Voluntary", "Involuntary"], barmode="stack", title="Turnover Breakdown")
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    with row[1]:
        # 5. Tenure of Exit
        fig = px.bar(exit_tenure, x="Tenure", y="Exit", title="Tenure Distribution of Exit")
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    with row[2]:
        # 6. Internal Mobility
        fig = px.pie(mobility, values="Count", names="Type", title="Internal Mobility (YTD)", hole=0.4)
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    row = st.columns(3)
    with row[0]:
        # 7. Dept Movement
        fig = go.Figure()
        fig.add_trace(go.Bar(x=dept_move["Department"], y=dept_move["Join"], name="Join"))
        fig.add_trace(go.Bar(x=dept_move["Department"], y=dept_move["Leave"], name="Leave"))
        fig.update_layout(barmode='group', title="Department Movement", height=350)
        st.plotly_chart(fig, use_container_width=True)
    with row[1]:
        # 8. Replacement Rate
        fig = px.line(x=periods, y=replacement_rate, markers=True, title="Replacement Rate (%)")
        fig.update_traces(line_color='green')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    with row[2]:
        # 9. Key Talent Movement
        fig = px.bar(keytalent_move, x="period", y=["New", "Exit"], barmode="group", title="Key Talent Movement")
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    row = st.columns(3)
    
    with row[0]:
        # 10. Backfill vs New Position
        fig = px.bar(backfill_new, x="period", y=["Backfill", "New"], barmode="stack", title="Backfill vs New Position")
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    with row[1]:
        # 11. Avg Time to Fill
        fig = px.bar(avg_fill, x="period", y="Avg days", title="Average Time to Fill (days)", color="Avg days")
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    with row[2]:
        # 12. Resignation Reason
        fig = px.pie(reasons, values="Count", names="Reason", title="Resignation Reasons", hole=0.3)
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    row = st.columns(3)
    with row[0]:
        # 13. Promotion/Demotion
        fig = px.bar(promote_demote, x="period", y=["Promote", "Demote"], barmode="group", title="Promotion/Demotion")
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    with row[1]:
        # 14. Absence before Exit
        fig = px.line(absence, x="month", y="Absence Days", title="Absence Trend Around Attrition", markers=True)
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    with row[2]:
        # 15. Diversity of Movement
        fig = go.Figure()
        fig.add_trace(go.Bar(x=diversity["Group"], y=diversity["Join"], name="Join"))
        fig.add_trace(go.Bar(x=diversity["Group"], y=diversity["Leave"], name="Leave"))
        fig.update_layout(barmode='group', title="Diversity of Movement", height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    row = st.columns(3)
    with row[0]:
        # 16. Rehire Rate
        fig = px.bar(rehire, x="period", y="Rehire", title="Rehire Rate (Headcount)")
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    with row[1]:
        # 17. Exit Interview Completion
        fig = px.line(exit_interview, x="period", y="Completion Rate", markers=True, title="Exit Interview Completion (%)")
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    with row[2]:
        # 18. Waterfall Headcount Change
        waterfall.update_layout(title="Headcount Change (Waterfall)", height=350)
        st.plotly_chart(waterfall, use_container_width=True)
    

    st.caption("Dashboard động, phân tích đầy đủ các biến động nhân sự theo từng góc độ nghiệp vụ HR. (Mock data HR)")
