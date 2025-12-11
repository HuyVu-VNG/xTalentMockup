def page_employee_360_manager_view(employee=None):
    import streamlit as st
    from streamlit_elements import elements, mui, nivo
    from streamlit_timeline import st_timeline
    import plotly.express as px
    import pandas as pd
    import datetime

    # --- Dummy data chuẩn hoá cho 360 Manager/HRBP view ---
    if employee is None:
        employee = {
            "emp_code": "EMP001",
            "name": "Lê Văn B",
            "avatar": "https://randomuser.me/api/portraits/men/66.jpg",
            "job_title": "Phó phòng HCNS",
            "department": "Phòng HCNS",
            "legal_entity": "Công ty ABC",
            "status": "Active",
            "joined_date": "2021-06-01",
            # Chi phí/Đầu tư (cost/investment)
            "total_cost": [
                {"year": 2021, "salary": 120000000, "allowance": 20000000, "training": 3000000, "insurance": 7000000, "bonus": 2000000, "contribution": 220000000},
                {"year": 2022, "salary": 160000000, "allowance": 30000000, "training": 6000000, "insurance": 12000000, "bonus": 7000000, "contribution": 260000000},
                {"year": 2023, "salary": 220000000, "allowance": 50000000, "training": 5000000, "insurance": 15000000, "bonus": 15000000, "contribution": 310000000},
            ],
            # Hiệu quả/Đóng góp (performance/contribution)
            "performance": [
                {"period": "2021", "kpi": 75, "grade": "B", "projects": 2, "highlight": "Đạt mục tiêu nhóm"},
                {"period": "2022", "kpi": 82, "grade": "B+", "projects": 4, "highlight": "Hỗ trợ vận hành ERP"},
                {"period": "2023", "kpi": 92, "grade": "A", "projects": 3, "highlight": "Lead dự án HRIS"},
            ],
            # Kỹ năng (skills group)
            "skills": [
                {"group": "Quản lý dự án", "score": 7},
                {"group": "Phân tích dữ liệu", "score": 9},
                {"group": "Quản trị nhân sự", "score": 8},
                {"group": "Kỹ năng giao tiếp", "score": 8},
                {"group": "Lãnh đạo", "score": 7}
            ],
            # Nguy cơ nghỉ việc & rủi ro
            "risk": {
                "churn_risk": "High",  # Normal, High, Critical
                "reason": "Lương thấp hơn thị trường, workload tăng",
                "engagement": "Medium"
            },
            # Tiềm năng phát triển
            "potential": {
                "manager_score": "High",
                "suggested_career_path": "Trưởng phòng HCNS",
                "training_needed": ["Kỹ năng lãnh đạo", "Quản trị chiến lược"],
                "succession_ready": False
            },
            # Dữ liệu hành chính
            "contract": {"number": "HD2021-001", "type": "Không xác định thời hạn", "signed_date": "2021-06-01"},
            "current_assignment": {"job_title": "Phó phòng HCNS", "department": "Phòng HCNS", "status": "Active"},
            # Nhật ký/thời gian
            "timeline_salary": [
                {"from": "2021-06-01", "to": "2022-05-31", "base": 10000000, "bonus": 2000000},
                {"from": "2022-06-01", "to": "2023-06-30", "base": 13000000, "bonus": 3000000},
                {"from": "2023-07-01", "to": None, "base": 18000000, "bonus": 5000000},
            ],
            "timeline_rewards": [
                {"date": "2022-11-01", "type": "Thưởng KPI", "amount": 5000000, "note": "KPI cao"},
                {"date": "2023-03-08", "type": "Thưởng dự án", "amount": 8000000, "note": "Hoàn thành dự án HRIS"},
            ],
            "timeline_kpi": [
                {"year": 2021, "kpi": 75},
                {"year": 2022, "kpi": 82},
                {"year": 2023, "kpi": 92},
            ]
        }

    st.subheader(f"📘 Hồ sơ Nhân viên 360 (Emp Code: {employee['emp_code']} – {employee['name']})")
    

    tabs = st.tabs([
        "Tổng quan", "Chi phí & Đầu tư", "Hiệu quả & Đóng góp",
        "Nguy cơ & Rủi ro", "Tiềm năng phát triển", "Dữ liệu hành chính", "Nhật ký & Thời gian"
    ])

    # --- Tổng quan: mini dashboard, cảnh báo, chỉ số, hành động nhanh ---
    with tabs[0]:
        st.markdown("### Mini Dashboard")
        # Cảnh báo nếu rủi ro nghỉ việc cao
        if employee["risk"]["churn_risk"] == "Critical":
            st.error("⚠️ Nhân sự có **rủi ro nghỉ việc cực cao**! Lý do: " + employee["risk"]["reason"])
        elif employee["risk"]["churn_risk"] == "High":
            st.warning("⚠️ Nhân sự có **rủi ro nghỉ việc cao**! Lý do: " + employee["risk"]["reason"])
        elif employee["risk"]["churn_risk"] == "Normal":
            st.info("Nhân sự có nguy cơ nghỉ việc ở mức bình thường.")

        cols = st.columns(4)
        cols[0].metric("Tổng chi phí năm qua", f"{employee['total_cost'][-1]['salary']+employee['total_cost'][-1]['allowance']+employee['total_cost'][-1]['training']+employee['total_cost'][-1]['insurance']:,}đ")
        cols[1].metric("Điểm KPI mới nhất", f"{employee['performance'][-1]['kpi']}", delta=None)
        cols[2].metric("Thành tích nổi bật", employee['performance'][-1]['highlight'])
        cols[3].metric("Tiềm năng phát triển", employee['potential']['manager_score'])

        st.divider()
        st.markdown("### Hành động nhanh")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("💸 Đề xuất tăng lương"):
                st.success("Đã gửi đề xuất tăng lương!")
        with c2:
            if st.button("📚 Đề xuất đào tạo"):
                st.success("Đã gửi đề xuất đào tạo!")
        with c3:
            if st.button("🤝 Đề xuất giữ chân"):
                st.success("Đã gửi đề xuất giữ chân!")

    # --- Chi phí & Đầu tư ---
    with tabs[1]:
        st.markdown("### Biểu đồ tổng chi phí vs đóng góp (ROI)")
        df_cost = pd.DataFrame(employee["total_cost"])
        df_cost["total_spent"] = df_cost["salary"] + df_cost["allowance"] + df_cost["training"] + df_cost["insurance"] + df_cost["bonus"]
        fig = px.bar(df_cost, x="year", y=["total_spent", "contribution"],
                     barmode="group", labels={"value":"VND", "year":"Năm", "variable":"Khoản"})
        fig.update_layout(yaxis_tickformat=',.0f', legend_title_text='')
        st.plotly_chart(fig, use_container_width=True)
        st.info("So sánh tổng chi phí (lương, thưởng, training, bảo hiểm,...) với tổng đóng góp do HR/Manager đánh giá.")

    # --- Hiệu quả & Đóng góp ---
    with tabs[2]:
        st.markdown("### Thành tích & Hiệu quả")
        # Table projects, highlights
        st.table([
            {
                "Kỳ": perf["period"],
                "KPI": perf["kpi"],
                "Xếp loại": perf["grade"],
                "Dự án": perf["projects"],
                "Thành tích nổi bật": perf["highlight"]
            } for perf in employee["performance"]
        ])
        # Radar chart kỹ năng
        st.markdown("### Đánh giá kỹ năng (Radar Chart)")
        
        # Đặt block này trong tab hoặc dưới tab, chỉ cần có employee["skills"]

        with elements("radar-skill-nivo"):
            from streamlit_elements import mui, nivo

            # Dữ liệu mẫu: điểm nhân viên, điểm min, avg, max (demo khác nhau từng skill)
            skill_list = [
                "Quản lý dự án",
                "Phân tích dữ liệu",
                "Quản trị nhân sự",
                "Kỹ năng giao tiếp",
                "Lãnh đạo"
            ]

            employee_name = employee["name"]
            employee_scores = [s["score"] for s in employee["skills"]]

            # Data giả lập (ở thực tế nên lấy từ nhiều nhân viên để thống kê)
            min_scores = [4, 6, 5, 5, 4]
            avg_scores = [7, 7.5, 6.8, 7, 6.5]
            max_scores = [9, 10, 9, 9, 8]

            # Đưa về pivot dạng radar-data, mỗi item là một skill
            radar_data = []
            for i, skill in enumerate(skill_list):
                radar_data.append({
                    "Kỹ năng": skill,
                    employee_name: employee_scores[i],
                    "Min": min_scores[i],
                    "Avg": avg_scores[i],
                    "Max": max_scores[i],
                })

            keys = [employee_name, "Min", "Avg", "Max"]

            # Render radar chart
            with mui.Box(sx={"height": 420}):
                nivo.Radar(
                    data=radar_data,
                    keys=keys,
                    indexBy="Kỹ năng",
                    valueFormat=">-.1f",
                    maxValue=10,
                    margin={ "top": 70, "right": 80, "bottom": 40, "left": 80 },
                    borderColor={ "from": "color" },
                    gridLabelOffset=36,
                    dotSize=10,
                    dotColor={ "theme": "background" },
                    dotBorderWidth=2,
                    motionConfig="wobbly",
                    legends=[
                        {
                            "anchor": "top-left",
                            "direction": "column",
                            "translateX": -50,
                            "translateY": -40,
                            "itemWidth": 90,
                            "itemHeight": 20,
                            "itemTextColor": "#999",
                            "symbolSize": 12,
                            "symbolShape": "circle",
                            "effects": [
                                {
                                    "on": "hover",
                                    "style": {
                                        "itemTextColor": "#000"
                                    }
                                }
                            ]
                        }
                    ],
                    theme={
                        "background": "#FFFFFF",
                        "textColor": "#31333F",
                        "tooltip": {
                            "container": {
                                "background": "#FFFFFF",
                                "color": "#31333F",
                            }
                        }
                    }
                )


        st.info("Đánh giá kỹ năng dựa trên điểm tự đánh giá hoặc manager chấm.")

    # --- Nguy cơ & Rủi ro ---
    with tabs[3]:
        st.markdown("### Cảnh báo nguy cơ & rủi ro nhân sự")
        st.write("**Churn Risk:**", employee["risk"]["churn_risk"])
        st.write("**Nguyên nhân:**", employee["risk"]["reason"])
        st.write("**Engagement:**", employee["risk"]["engagement"])
        if employee["risk"]["churn_risk"] == "Critical":
            st.error("⚠️ HR cần xây dựng kế hoạch giữ chân, cảnh báo tới line manager!")
        elif employee["risk"]["churn_risk"] == "High":
            st.warning("⚠️ Nên kiểm tra tình trạng đãi ngộ, workload, lộ trình phát triển.")
        else:
            st.success("Không có nguy cơ bất thường.")

    # --- Tiềm năng phát triển ---
    with tabs[4]:
        st.markdown("### Đánh giá tiềm năng & phát triển")
        st.write("**Manager đánh giá:**", employee["potential"]["manager_score"])
        st.write("**Lộ trình nghề nghiệp đề xuất:**", employee["potential"]["suggested_career_path"])
        st.write("**Cần đào tạo:**", ", ".join(employee["potential"]["training_needed"]))
        st.write("**Kế thừa sẵn sàng:**", "Đã sẵn sàng" if employee["potential"]["succession_ready"] else "Chưa sẵn sàng")
        st.info("Dữ liệu này giúp quyết định đầu tư phát triển nhân sự, xây dựng kế hoạch kế thừa (succession plan).")

    # --- Dữ liệu hành chính ---
    with tabs[5]:
        st.markdown("### Dữ liệu hành chính & hợp đồng")
        st.write("**Số hợp đồng:**", employee["contract"]["number"])
        st.write("**Loại hợp đồng:**", employee["contract"]["type"])
        st.write("**Ngày ký:**", employee["contract"]["signed_date"])
        st.write("**Assignment hiện tại:**", f"{employee['current_assignment']['job_title']} – {employee['current_assignment']['department']} ({employee['current_assignment']['status']})")

    # --- Nhật ký & thời gian (timeline lương, thưởng, KPI) ---
    with tabs[6]:
        st.markdown("### Timeline Lương/Thưởng/KPI")
        # Timeline salary bonus
        # df_sal = pd.DataFrame([
        #     {
        #         "from": sal["from"],
        #         "to": sal["to"] or datetime.datetime.now().strftime("%Y-%m-%d"),
        #         "base": sal["base"],
        #         "bonus": sal["bonus"]
        #     } for sal in employee["timeline_salary"]
        # ])
        # fig_sal = px.timeline(df_sal, x_start="from", x_end="to", y=["base", "bonus"], color_discrete_sequence=["#2ca02c", "#e377c2"])
        # fig_sal.update_yaxes(title=None, tickvals=[0,1], ticktext=["Lương cơ bản", "Thưởng"])
        # fig_sal.update_layout(title_text="Timeline lương & thưởng", height=250)
        # st.plotly_chart(fig_sal, use_container_width=True)
        # Timeline salary + bonus (hiển thị từng dòng cho lương/thưởng)
        df_sal = pd.DataFrame([
            {
                "from": sal["from"],
                "to": sal["to"] or datetime.datetime.now().strftime("%Y-%m-%d"),
                "type": "Lương cơ bản",
                "value": sal["base"]
            }
            for sal in employee["timeline_salary"]
        ] + [
            {
                "from": sal["from"],
                "to": sal["to"] or datetime.datetime.now().strftime("%Y-%m-%d"),
                "type": "Thưởng",
                "value": sal["bonus"]
            }
            for sal in employee["timeline_salary"]
        ])
        fig_sal = px.timeline(
            df_sal, x_start="from", x_end="to", y="type", color="type",
            hover_data=["value"], title="Timeline lương & thưởng"
        )
        fig_sal.update_layout(height=250)
        st.plotly_chart(fig_sal, use_container_width=True)

        # Timeline KPI
        df_kpi = pd.DataFrame(employee["timeline_kpi"])
        fig_kpi = px.line(df_kpi, x="year", y="kpi", markers=True, title="KPI theo thời gian")
        fig_kpi.update_traces(line=dict(width=3), marker=dict(size=10))
        st.plotly_chart(fig_kpi, use_container_width=True)

        # Timeline rewards
        df_rewards = pd.DataFrame(employee["timeline_rewards"])
        st.markdown("#### Nhật ký khen thưởng")
        st.table(df_rewards)

    st.divider()
    st.caption("UX xTalent 360 Strategic – HR/Manager View: Đầu tư, hiệu quả, rủi ro, tiềm năng, hành động nhanh, timeline trực quan.")


# -- Chạy thử độc lập:
if __name__ == "__main__":
    page_employee_360_manager_view()
