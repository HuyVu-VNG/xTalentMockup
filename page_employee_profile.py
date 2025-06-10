def page_employee_profile(employee=None):
    import streamlit as st
    from streamlit_elements import elements, mui, nivo
    import plotly.express as px
    import pandas as pd
    import datetime

    # --- Dummy employee/assignment-level data làm giàu (song song, promote, transfer) ---
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
            "contract": {
                "number": "HD2021-001",
                "type": "Không xác định thời hạn",
                "signed_date": "2021-06-01",
                "expiry_date": None,
                "status": "Hiệu lực",
                "appendices": [
                    {"number": "PL-001", "desc": "Điều chỉnh lương", "date": "2022-01-01"},
                ]
            },
            "assignment_history": [
                {
                    "from": "2021-06-01", "to": "2022-05-31",
                    "job_title": "Nhân viên Văn phòng", "department": "Phòng HCNS", "status": "Fulltime"
                },
                {
                    "from": "2021-11-01", "to": "2022-03-31",
                    "job_title": "Trợ lý Dự án", "department": "Phòng Dự án", "status": "Parttime"
                },
                {
                    "from": "2022-06-01", "to": "2023-06-30",
                    "job_title": "Chuyên viên Văn phòng", "department": "Phòng HCNS", "status": "Promoted"
                },
                {
                    "from": "2023-07-01", "to": None,
                    "job_title": "Phó phòng HCNS", "department": "Phòng HCNS", "status": "Active"
                },
                {
                    "from": "2023-01-01", "to": "2023-06-30",
                    "job_title": "Chuyên viên IT (Kiêm nhiệm)", "department": "Phòng CNTT", "status": "Concurrent"
                }
            ],
            "position_code": "POS-101",
            "jd": "Phối hợp quản trị nhân sự, điều phối dự án HR, quản lý team.",
            "salary": [
                {"from": "2021-06-01", "to": "2022-05-31", "base": 12000000, "allowance": 1500000},
                {"from": "2022-06-01", "to": "2023-06-30", "base": 16000000, "allowance": 2500000},
                {"from": "2023-07-01", "to": None, "base": 22000000, "allowance": 5000000},
            ],
            "attendance": {
                "working_days": 22, "late": 1, "leave": 2, "ot": 4, "annual_leave_left": 6,
            },
            "performance": [
                {"period": "2021", "kpi": 75, "grade": "B"},
                {"period": "2022", "kpi": 82, "grade": "B+"},
                {"period": "2023", "kpi": 92, "grade": "A"},
            ],
            "rewards_discipline": [
                {"date": "2022-11-01", "type": "Khen thưởng", "title": "Nhân viên xuất sắc", "note": "Đạt KPI cao nhất phòng HCNS"},
                {"date": "2023-03-10", "type": "Kỷ luật", "title": "Khiển trách", "note": "Quên báo cáo tiến độ tuần"},
            ],
            "assets": [
                {"asset": "Laptop", "serial": "ABC123", "date_assigned": "2021-06-01", "status": "Đang sử dụng"},
                {"asset": "SIM điện thoại", "serial": "0909111222", "date_assigned": "2021-06-05", "status": "Thu hồi"},
            ],
            "requests": [
                {"date": "2024-02-01", "type": "Tăng lương", "status": "Đã duyệt"},
                {"date": "2023-12-10", "type": "Nghỉ phép", "status": "Đã duyệt"},
            ],
            "documents": [
                {"type": "Hợp đồng lao động", "file": "HD2021-001.pdf", "date": "2021-06-01"},
                {"type": "Phụ lục", "file": "PL-001.pdf", "date": "2022-01-01"},
            ],
            "current_plan": {
                "engagement": "Medium", "risk": "Normal", "retention": "Tiềm năng giữ chân"
            }
        }

    st.subheader(f"👨‍💼 Hồ sơ Nhân viên 360 – {employee['name']} (Emp Code: {employee['emp_code']})")

    # ---- Mini-dashboard, avatar...
    with elements("employee-overview"):
        with mui.Paper(sx={"p":3, "display":"flex", "alignItems":"center", "gap":3, "mb":2, "boxShadow":3, "borderRadius":2}):
            mui.Avatar(src=employee["avatar"], sx={"width":80, "height":80, "mr":3})
            with mui.Box():
                mui.Typography(employee["name"], variant="h5", sx={"fontWeight":600})
                mui.Typography(f"Emp Code: {employee['emp_code']} | {employee['job_title']} | {employee['department']}", variant="body2")
                mui.Typography(f"Pháp nhân: {employee['legal_entity']} | Vào làm: {employee['joined_date']}", variant="body2")
                status_map = {
                    "Active": "#388e3c", "Probation": "#1976d2", "Suspended": "#ffa000", "Terminated": "#d32f2f"
                }
                mui.Chip(label=employee["status"], color="success" if employee["status"]=="Active" else "warning", sx={"bgcolor":status_map.get(employee["status"], "#9e9e9e"), "color":"white", "fontWeight":600, "mt":1})

    kpis = [
        {"label": "Tổng lương hiện tại", "value": f"{employee['salary'][-1]['base'] + employee['salary'][-1]['allowance']:,}đ", "color": "#388e3c"},
        {"label": "Phép còn lại", "value": f"{employee['attendance']['annual_leave_left']}", "color": "#1976d2"},
        {"label": "Điểm KPI mới nhất", "value": f"{employee['performance'][-1]['kpi']}", "color": "#ffa000"},
        {"label": "Tài sản đang dùng", "value": f"{sum(1 for a in employee['assets'] if a['status']=='Đang sử dụng')}", "color": "#7b1fa2"},
    ]
    cols = st.columns(len(kpis))
    for i, col in enumerate(cols):
        with col:
            st.markdown(
                f"""
                <div style="background:{kpis[i]['color']};padding:12px 10px;border-radius:10px;color:white;">
                    <b>{kpis[i]['label']}</b><div style="font-size:1.7em">{kpis[i]['value']}</div>
                </div>
                """, unsafe_allow_html=True
            )
    st.divider()

    tabs = st.tabs([
        "Tổng quan", "Hợp đồng & phụ lục", "Lịch sử công việc", "Vị trí & mô tả", "Lương & đãi ngộ", 
        "Chấm công & nghỉ phép", "Hiệu suất", "Khen thưởng/Kỷ luật", "Tài sản", "Lịch sử đề xuất", 
        "Hồ sơ tài liệu", "Tình trạng & kế hoạch"
    ])

    # Tab 1: Tổng quan - Timeline công việc dùng plotly.timeline (group by phòng ban)
    with tabs[0]:
        st.markdown("#### Timeline lịch sử Assignment (song song – promote – transfer)")
        # Convert to dataframe for Plotly
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        df_assign = pd.DataFrame([
            {
                "Phòng ban": his["department"],
                "Vị trí": his["job_title"],
                "Bắt đầu": his["from"],
                "Kết thúc": his["to"] or now,
                "Trạng thái": his["status"],
            }
            for his in employee["assignment_history"]
        ])
        # Plotly timeline (multi-row, color by department)
        fig = px.timeline(
            df_assign,
            x_start="Bắt đầu",
            x_end="Kết thúc",
            y="Phòng ban",  # Group theo phòng ban (department)
            color="Vị trí",
            hover_data=["Vị trí", "Trạng thái", "Bắt đầu", "Kết thúc"],
            title="Timeline lịch sử công việc (song song, promote, chuyển phòng)"
        )
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(
            height=330,
            margin=dict(l=40, r=40, t=60, b=30),
            xaxis_title="Thời gian",
            yaxis_title="Phòng ban",
            legend_title="Vị trí"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Các tab khác giữ nguyên (như code cũ) ...

    # Tab 2: Hợp đồng & phụ lục
    with tabs[1]:
        st.markdown("#### Thông tin hợp đồng lao động")
        st.write(f"Số hợp đồng: {employee['contract']['number']}")
        st.write(f"Loại hợp đồng: {employee['contract']['type']}")
        st.write(f"Ký ngày: {employee['contract']['signed_date']}")
        st.write(f"Ngày hết hạn: {employee['contract']['expiry_date'] or 'Không xác định'}")
        st.write(f"Trạng thái: {employee['contract']['status']}")
        st.markdown("##### Phụ lục hợp đồng")
        st.table(employee['contract']['appendices'])

    # Tab 3: Lịch sử công việc (promote, chuyển phòng)
    with tabs[2]:
        st.markdown("#### Timeline lịch sử vị trí làm việc")
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        df_assign = pd.DataFrame([
            {
                "Phòng ban": his["department"],
                "Vị trí": his["job_title"],
                "Bắt đầu": his["from"],
                "Kết thúc": his["to"] or now,
                "Trạng thái": his["status"],
            }
            for his in employee["assignment_history"]
        ])
        fig2 = px.timeline(
            df_assign,
            x_start="Bắt đầu",
            x_end="Kết thúc",
            y="Vị trí",     # hoặc "Phòng ban" tuỳ mục đích
            color="Trạng thái",
            hover_data=["Phòng ban", "Bắt đầu", "Kết thúc"],
            title="Timeline lịch sử vị trí"
        )
        fig2.update_yaxes(autorange="reversed")
        fig2.update_layout(
            height=300,
            margin=dict(l=40, r=40, t=50, b=30),
        )
        st.plotly_chart(fig2, use_container_width=True)


    # Tab 4–12 (giữ nguyên, như ở code trước...)

    with tabs[3]:
        st.write(f"**Vị trí hiện tại:** {employee['job_title']}")
        st.write(f"**Phòng ban:** {employee['department']}")
        st.write(f"**Mã vị trí:** {employee['position_code']}")
        st.markdown(f"**Mô tả công việc:** {employee['jd']}")

    with tabs[4]:
        st.markdown("#### Lịch sử lương & phụ cấp")
        st.table([
            {
                "Từ": sal["from"],
                "Đến": sal["to"] or "Hiện tại",
                "Lương cơ bản": f"{sal['base']:,}đ",
                "Phụ cấp": f"{sal['allowance']:,}đ",
                "Tổng": f"{sal['base']+sal['allowance']:,}đ"
            } for sal in employee["salary"]
        ])

    with tabs[5]:
        st.markdown("#### Chấm công tháng này")
        st.write(f"Số ngày làm: {employee['attendance']['working_days']}")
        st.write(f"Ngày đi muộn: {employee['attendance']['late']}")
        st.write(f"Nghỉ có phép: {employee['attendance']['leave']}")
        st.write(f"Số giờ OT: {employee['attendance']['ot']}")
        st.write(f"Phép còn lại: {employee['attendance']['annual_leave_left']}")

    with tabs[6]:
        st.markdown("#### Lịch sử đánh giá hiệu suất (KPI/OKR)")
        st.table([
            {
                "Kỳ": perf["period"],
                "KPI": perf["kpi"],
                "Xếp loại": perf["grade"]
            } for perf in employee["performance"]
        ])

    with tabs[7]:
        st.markdown("#### Khen thưởng/Kỷ luật liên quan assignment này")
        st.table(employee["rewards_discipline"])

    with tabs[8]:
        st.markdown("#### Danh sách tài sản đã cấp")
        st.table(employee["assets"])

    with tabs[9]:
        st.markdown("#### Lịch sử đề xuất")
        st.table(employee["requests"])

    with tabs[10]:
        st.markdown("#### Tài liệu liên quan assignment")
        st.table(employee["documents"])

    with tabs[11]:
        st.markdown("#### Tình trạng hiện tại & kế hoạch")
        st.write(f"Gắn kết: {employee['current_plan']['engagement']}")
        st.write(f"Nguy cơ nghỉ việc: {employee['current_plan']['risk']}")
        st.write(f"Giữ chân: {employee['current_plan']['retention']}")
        if employee['current_plan']['risk'] == "Critical":
            st.error("⚠️ Nguy cơ nghỉ việc cao – Cần lưu ý giữ chân nhân sự này!")
        elif employee['current_plan']['risk'] == "High":
            st.warning("⚠️ Nguy cơ nghỉ việc ở mức cao.")
        elif employee['current_plan']['engagement'] == "High":
            st.success("Nhân sự đang có mức gắn kết tốt.")
        else:
            st.info("Tình trạng ổn định.")

    st.divider()
    st.caption("UX xTalent – Employee 360: lịch sử assignment song song, thuyên chuyển, promote – dành cho HR chuyên sâu.")
