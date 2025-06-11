def page_person_profile(person=None, work_relationships=None):
    import streamlit as st
    from streamlit_elements import elements, mui
    import datetime
    import streamlit_folium
    import folium
    from streamlit_echarts import st_echarts
    import plotly.graph_objects as go

    def tab_job_matching():
        st.markdown("## 🗺️ Bản đồ Cơ hội Nghề nghiệp (Job Matching Map)")
        st.info(
            "Biểu đồ này giúp bạn hình dung các **cơ hội phát triển nghề nghiệp** nội bộ theo năng lực, bằng cấp, chứng chỉ, kỹ năng của mình. "
            "Mỗi luồng thể hiện khả năng kết nối từ năng lực hiện tại đến vị trí công việc trong tổ chức."
        )

        # 1. Labels theo đúng từng node trong option
        labels = [
            "Nguyễn Văn A",               # 0 - Worker
            "Đại học CNTT",               # 1 - Degree
            "Năng lực Lập trình",         # 2 - Comp
            "Năng lực Phân tích dữ liệu", # 3 - Comp
            "Chứng chỉ PMP",              # 4 - Cert
            "Python",                     # 5 - Skill
            "SQL",                        # 6 - Skill
            "Quản lý dự án",              # 7 - Skill
            "Business Analysis",          # 8 - Skill
            "Senior Developer",           # 9 - Job
            "Data Analyst",               # 10 - Job
            "Project Manager",            # 11 - Job
            "Business Analyst"            # 12 - Job
        ]

        # 2. Luồng (source, target, value) tương ứng với ECharts
        links = [
            # Worker -> Degree/Comp/Cert
            (0, 1, 1),
            (0, 2, 1),
            (0, 4, 1),
            (0, 3, 1),
            # Degree/Comp/Cert -> Skills
            (1, 5, 1),
            (2, 5, 1),
            (4, 7, 1),
            (3, 6, 1),
            (3, 8, 1),
            # Skills -> Jobs
            (5, 9, 1),
            (6, 10, 1),
            (8, 12, 1),
            (7, 11, 1),
            (8, 11, 1),   # cross skill
        ]

        # 3. Màu node (theo depth)
        node_colors = [
            "#ffe599",     # 0 - Worker
            "#a4c2f4",     # 1 - Degree
            "#a4c2f4",     # 2 - Comp
            "#a4c2f4",     # 3 - Comp
            "#a4c2f4",     # 4 - Cert
            "#b6d7a8",     # 5 - Skill
            "#b6d7a8",     # 6 - Skill
            "#b6d7a8",     # 7 - Skill
            "#b6d7a8",     # 8 - Skill
            "#e06666",     # 9 - Job
            "#e06666",     # 10 - Job
            "#e06666",     # 11 - Job
            "#e06666",     # 12 - Job
        ]

        # 4. Tạo Sankey Diagram
        fig = go.Figure(go.Sankey(
            node = dict(
                pad = 18,
                thickness = 26,
                line = dict(color = "#888", width = 0.5),
                label = labels,
                color = node_colors,
                hovertemplate='%{label}<extra></extra>',
            ),
            link = dict(
                source = [src for src, tgt, val in links],
                target = [tgt for src, tgt, val in links],
                value  = [val for src, tgt, val in links],
                color = "rgba(160,160,160,0.32)",
                hovertemplate='Từ %{source.label} → %{target.label}<br>Sức mạnh: %{value}<extra></extra>',
            )
        ))

        fig.update_layout(
            title="Bản đồ Cơ hội Nghề nghiệp (Job Matching Map)",
            title_x=0.5,
            font=dict(size=13, color="#333"),
            margin=dict(l=10, r=10, t=40, b=10),
            height=540,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("💡 Mỗi luồng minh hoạ năng lực/bằng cấp/chứng chỉ của bạn liên kết đến kỹ năng then chốt và các vị trí công việc nội bộ phù hợp.")

    # Để nhúng: với tab hoặc riêng page, gọi tab_job_matching()

    # 1. Dummy data (nếu chưa truyền vào)
    if person is None:
        person = {
            "avatar": "https://randomuser.me/api/portraits/men/65.jpg",
            "name": "Nguyễn Văn A",
            "gender": "Nam",
            "dob": "1993-05-22",
            "xtalent_code": "PERSON-2024-001",
            "email": "nguyenvana@xtalent.vn",
            "phone": "0909 123 456",
            "address": "Z123 Đường 13, Q.7, TP.HCM",
            "lat": 10.758278, "lng": 106.7210879,  # to show on map ,
            "emergency_contact": "Nguyễn Thị B - 0909 999 888",
            "degree": "Đại học CNTT",
            "relatives": ["Nguyễn Thị B (vợ)", "Nguyễn Văn C (con)"],
            "identity": {"type": "CMND", "number": "123456789", "issued": "2010-01-01"},
            "bank": {"name": "Vietcombank", "acc": "123456789", "branch": "PGD Sài Gòn"},
            "payment": {"method": "Bank", "note": "Chuyển khoản lương ngày 28 hàng tháng"},
        }

    if work_relationships is None:
        work_relationships = [
            {
                "legal_entity": "Công ty ABC",
                "relationship_type": "Nhân viên chính thức",
                "emp_code": "EMP001",
                "status": "Active",
                "from_date": "2021-01-15",
                "to_date": None,
                "assignments": [
                    {
                        "job_title": "Lập trình viên chính",
                        "department": "Phòng CNTT",
                        "status": "Active",
                        "assignment_code": "A1",
                        "from_date": "2021-01-15",
                        "to_date": None,
                    }
                ]
            },
            {
                "legal_entity": "Công ty XYZ",
                "relationship_type": "Cộng tác viên",
                "emp_code": "EMPX23",
                "status": "Inactive",
                "from_date": "2020-03-01",
                "to_date": "2022-12-31",
                "assignments": [
                    {
                        "job_title": "Tư vấn CNTT",
                        "department": "Phòng Dự án",
                        "status": "Đã kết thúc",
                        "assignment_code": "A2",
                        "from_date": "2020-03-01",
                        "to_date": "2022-12-31",
                    }
                ]
            },
        ]

    st.subheader("👤 Hồ Sơ Cá Nhân")
    with elements("profile-card"):
        # --- Hồ sơ cá nhân ---
        with mui.Paper(sx={"p":3, "display":"flex", "alignItems":"center", "gap":3, "mb":3, "boxShadow":3, "borderRadius":2}):
            mui.Avatar(src=person["avatar"], sx={"width":96, "height":96, "mr":3})
            with mui.Box():
                mui.Typography(person["name"], variant="h5", sx={"fontWeight":600})
                mui.Typography(f"ID xTalent: {person['xtalent_code']}", variant="body2")
                mui.Typography(f"Giới tính: {person['gender']} | Ngày sinh: {datetime.datetime.strptime(person['dob'], '%Y-%m-%d').strftime('%d/%m/%Y')}", variant="body2")
                mui.Typography(f"Email: {person['email']} | ĐT: {person['phone']}", variant="body2")

    # TABS UI
    tabs = st.tabs([
        "Thông tin cá nhân", "Liên hệ", "Mở rộng","Quan hệ lao động", "Khen thưởng/Kỷ luật", "Tài liệu scan", "Bản đồ Cơ hội nghề nghiệp", "Bản đồ cơ hội nghề nghiệp - Plotly"
    ])
    with tabs[0]:
        st.write("**Ngày sinh:**", datetime.datetime.strptime(person["dob"], "%Y-%m-%d").strftime("%d/%m/%Y"))
        st.write("**Giới tính:**", person["gender"])
        st.write("**Địa chỉ:**", person["address"])
        # Hiển thị bản đồ
        m = folium.Map(location=[person["lat"], person["lng"]], zoom_start=15)
        folium.Marker([person["lat"], person["lng"]], tooltip=person["address"]).add_to(m)
        streamlit_folium.folium_static(m, width=500, height=250)

    with tabs[1]:
        st.write("**Email:**", person["email"])
        st.write("**Điện thoại:**", person["phone"])
        st.write("**Liên hệ khẩn cấp:**", person["emergency_contact"])

    with tabs[2]:
        st.write("**Bằng cấp:**", person["degree"])
        st.write("**Người thân:**", ", ".join(person["relatives"]))
        st.write("**Giấy tờ tuỳ thân:**", f"{person['identity']['type']} số {person['identity']['number']} (cấp: {person['identity']['issued']})")
        st.write("**Ngân hàng:**", f"{person['bank']['name']} – {person['bank']['acc']} ({person['bank']['branch']})")
        st.write("**Thông tin thanh toán:**", f"{person['payment']['method']} – {person['payment']['note']}")

    with tabs[3]:
        st.markdown("### Danh sách Quan hệ lao động (Work Relationships)")
        for idx, wr in enumerate(work_relationships, 1):
            st.markdown(f"#### {idx}. {wr['legal_entity']} – {wr['relationship_type']} (Emp Code: {wr['emp_code']})")
            st.write(
                f"**Trạng thái:** {wr['status']} | "
                f"**Từ:** {wr['from_date']}"
                + (f" → **Đến:** {wr['to_date']}" if wr['to_date'] else "")
            )
            st.markdown("**Assignments:**")
            # Assignment table
            st.table([
                {
                    "Code": a["assignment_code"],
                    "Job": a["job_title"],
                    "Phòng ban": a["department"],
                    "Trạng thái": a["status"],
                    "Từ": a["from_date"],
                    "Đến": a["to_date"] or "Hiện tại",
                }
                for a in wr["assignments"]
            ])
    # Khen thưởng/Kỷ luật
    with tabs[4]:
        st.markdown("### Lịch sử Khen thưởng & Kỷ luật")
        reward_punish_list = [
            {"Ngày": "2022-11-01", "Loại": "Khen thưởng", "Tên": "Bằng khen tập đoàn", "Nội dung": "Hoàn thành xuất sắc dự án ERP"},
            {"Ngày": "2023-03-10", "Loại": "Kỷ luật", "Tên": "Khiển trách", "Nội dung": "Đi làm trễ nhiều lần"},
            # ... thêm dòng ...
        ]
        st.table(reward_punish_list)
        st.info("Chỉ các quyết định cấp toàn cá nhân (Person) mới xuất hiện ở đây. Các quyết định theo assignment xem chi tiết trong tab Quan hệ lao động.")

    # Tài liệu scan (Scan documents)
    with tabs[5]:
        st.markdown("### Tài liệu scan đính kèm")
        doc_list = [
            {"Loại": "CMND/CCCD", "Tệp": "cmnd_nguyenvana.pdf", "Ngày upload": "2022-01-05"},
            {"Loại": "Bằng đại học", "Tệp": "bang_daihoc.pdf", "Ngày upload": "2021-06-01"},
            # ... thêm dòng ...
        ]
        st.table(doc_list)
        st.info("Chỉ những tài liệu hồ sơ gốc của cá nhân. Hồ sơ hợp đồng, giấy tờ pháp nhân sẽ lưu kèm assignment.")

    st.divider()
    st.caption("UX xTalent: 1 Person – N Work Relationships (Legal Entity) – N Assignments (Job/Dept/Code). Phù hợp chuẩn HR quốc tế.")

        # Tab 6: Job Matching Map (Career Opportunity Map)
    with tabs[6]:
        st.markdown("### 🗺️ Cơ hội nghề nghiệp nội bộ (Job Matching Map)")
        st.info("""
        Biểu đồ dưới đây giúp bạn hình dung các **cơ hội phát triển nghề nghiệp** phù hợp trong tổ chức, dựa trên hồ sơ năng lực, bằng cấp, chứng chỉ của bạn. Mỗi luồng là một khả năng nối giữa năng lực/bằng cấp/chứng chỉ của bạn đến kỹ năng then chốt và các vị trí công việc có thể tiếp cận nội bộ.
        """)

        # # Dummy data: degree, competency, certification của Nguyễn Văn A
        # degree = "Đại học CNTT"
        # competencies = ["Python", "SQL", "Quản lý dự án", "Phân tích nghiệp vụ"]
        # certifications = ["PMI Agile Certified", "AWS Practitioner"]

        # # Skills bạn đang có
        # skills = ["Lập trình", "Quản trị hệ thống", "Phân tích dữ liệu", "Quản lý dự án"]

        # # Mapping sang các Job nội bộ
        # jobs = [
        #     "Senior Developer",
        #     "System Analyst",
        #     "Project Coordinator",
        #     "Data Analyst",
        #     "Scrum Master"
        # ]

        # # Các mối liên kết dummy: Degree/Competency/Certification → Skill → Job
        # nodes = [
        #     {"name": person["name"], "itemStyle": {"color": "#94c3e5"}},  # Worker node

        #     # Lớp Degree/Competency/Certification
        #     {"name": degree, "itemStyle": {"color": "#ffe599"}},
        #     *[{"name": c, "itemStyle": {"color": "#ffe599"}} for c in competencies],
        #     *[{"name": c, "itemStyle": {"color": "#ffe599"}} for c in certifications],

        #     # Lớp Skill
        #     *[{"name": s, "itemStyle": {"color": "#b6d7a8"}} for s in skills],

        #     # Lớp Job
        #     *[{"name": j, "itemStyle": {"color": "#b4a7d6"}} for j in jobs]
        # ]

        # links = []
        # # Worker → Degree/Competency/Certification
        # links.append({"source": person["name"], "target": degree, "value": 2})
        # for c in competencies:
        #     links.append({"source": person["name"], "target": c, "value": 2})
        # for c in certifications:
        #     links.append({"source": person["name"], "target": c, "value": 2})

        # # Degree/Competency/Certification → Skill
        # links += [
        #     {"source": degree, "target": "Lập trình", "value": 2},
        #     {"source": "Quản lý dự án", "target": "Quản lý dự án", "value": 2},
        #     {"source": "PMI Agile Certified", "target": "Quản lý dự án", "value": 2},
        #     {"source": "Phân tích nghiệp vụ", "target": "Phân tích dữ liệu", "value": 2},
        #     {"source": "SQL", "target": "Phân tích dữ liệu", "value": 1.5},
        #     {"source": "AWS Practitioner", "target": "Quản trị hệ thống", "value": 1.5},
        #     {"source": "Python", "target": "Lập trình", "value": 2}
        # ]

        # # Skill → Job
        # links += [
        #     {"source": "Lập trình", "target": "Senior Developer", "value": 2},
        #     {"source": "Quản trị hệ thống", "target": "System Analyst", "value": 1.2},
        #     {"source": "Quản lý dự án", "target": "Project Coordinator", "value": 2},
        #     {"source": "Phân tích dữ liệu", "target": "Data Analyst", "value": 1.5},
        #     {"source": "Quản lý dự án", "target": "Scrum Master", "value": 1.2},
        #     {"source": "Lập trình", "target": "Scrum Master", "value": 1},
        # ]

        # option = {
        #     "title": {"text": "Bản đồ cơ hội nghề nghiệp nội bộ", "left": "center"},
        #     "tooltip": {"trigger": "item", "triggerOn": "mousemove"},
        #     "series": [
        #         {
        #             "type": "sankey",
        #             "data": nodes,
        #             "links": links,
        #             "emphasis": {"focus": "adjacency"},
        #             "levels": [
        #                 {"depth": 0, "itemStyle": {"color": "#94c3e5"}},
        #                 {"depth": 1, "itemStyle": {"color": "#ffe599"}},
        #                 {"depth": 2, "itemStyle": {"color": "#b6d7a8"}},
        #                 {"depth": 3, "itemStyle": {"color": "#b4a7d6"}},
        #             ],
        #             "lineStyle": {"curveness": 0.5, "color": "gradient"},
        #             "nodeGap": 24
        #         }
        #     ]
        # }

        # st_echarts(option, height="480px")

        # option = {
        #     "series": [
        #         {
        #             "type": "sankey",
        #             "data": [
        #                 {"name": "A"}, {"name": "B"}, {"name": "C"}
        #             ],
        #             "links": [
        #                 {"source": "A", "target": "B", "value": 10},
        #                 {"source": "B", "target": "C", "value": 15}
        #             ]
        #         }
        #     ]
        # }
        option = {
            "title": {"text": "Bản đồ Cơ hội Nghề nghiệp (Job Matching Map)", "left": "center"},
            "tooltip": {"trigger": "item", "triggerOn": "mousemove"},
            "series": [
                {
                    "type": "sankey",
                    "data": [
                        # Workers
                        {"name": "Nguyễn Văn A"},
                        # Degree/Comp/Cert
                        {"name": "Đại học CNTT"},
                        
                        {"name": "Năng lực Lập trình"},
                        {"name": "Năng lực Phân tích dữ liệu"},
                        {"name": "Chứng chỉ PMP"},
                        # Skills
                        {"name": "Python"},
                        {"name": "SQL"},
                        {"name": "Quản lý dự án"},
                        {"name": "Business Analysis"},
                        # Jobs
                        {"name": "Senior Developer"},
                        {"name": "Data Analyst"},
                        {"name": "Project Manager"},
                        {"name": "Business Analyst"},
                    ],
                    "links": [
                        # Nguyễn Văn A -> bằng cấp/năng lực/chứng chỉ
                        {"source": "Nguyễn Văn A", "target": "Đại học CNTT", "value": 1},
                        {"source": "Nguyễn Văn A", "target": "Năng lực Lập trình", "value": 1},
                        {"source": "Nguyễn Văn A", "target": "Chứng chỉ PMP", "value": 1},
                        {"source": "Nguyễn Văn A", "target": "Năng lực Phân tích dữ liệu", "value": 1},
                        # Degree/Comp/Cert -> Skills
                        {"source": "Đại học CNTT", "target": "Python", "value": 1},
                        {"source": "Năng lực Lập trình", "target": "Python", "value": 1},
                        {"source": "Chứng chỉ PMP", "target": "Quản lý dự án", "value": 1},
                        {"source": "Năng lực Phân tích dữ liệu", "target": "SQL", "value": 1},
                        {"source": "Năng lực Phân tích dữ liệu", "target": "Business Analysis", "value": 1},
                        
                        # Skills -> Jobs
                        {"source": "Python", "target": "Senior Developer", "value": 1},
                        {"source": "SQL", "target": "Data Analyst", "value": 1},
                        {"source": "Business Analysis", "target": "Business Analyst", "value": 1},
                        {"source": "Quản lý dự án", "target": "Project Manager", "value": 1},
                        {"source": "Business Analysis", "target": "Project Manager", "value": 1},  # cross skill
                    ],
                    "emphasis": {"focus": "adjacency"},
                    "lineStyle": {"color": "gradient", "curveness": 0.5},
                    "levels": [
                        {"depth": 0, "itemStyle": {"color": "#ffe599"}},       # Worker
                        {"depth": 1, "itemStyle": {"color": "#a4c2f4"}},       # Degree/Comp/Cert
                        {"depth": 2, "itemStyle": {"color": "#b6d7a8"}},       # Skill
                        {"depth": 3, "itemStyle": {"color": "#e06666"}},       # Job
                    ],
                    "label": {
                        "fontSize": 13,
                        "color": "#333",
                        "fontWeight": "bold"
                    },
                    "nodeGap": 18,
                    "nodeAlign": "justify",  # nodes giãn đều các cột
                }
            ]
        }

        st_echarts(option, height="400px")

        st.caption("""
        👉 Mỗi đường dẫn thể hiện năng lực hoặc chứng chỉ hiện tại của bạn, những kỹ năng tương ứng và các vị trí công việc mà bạn đã sẵn sàng hoặc có tiềm năng chuyển đổi trong tổ chức.
        """)
    with tabs[7]:
        tab_job_matching()

# ----- BỔ SUNG: THÊM TÊN TAB MỚI vào dòng tạo tabs:
# tabs = st.tabs([
#     "Thông tin cá nhân", "Liên hệ", "Mở rộng", "Quan hệ lao động", "Khen thưởng/Kỷ luật", "Tài liệu scan", **"Bản đồ Cơ hội nghề nghiệp"**
# ])