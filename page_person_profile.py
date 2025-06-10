def page_person_profile(person=None, work_relationships=None):
    import streamlit as st
    from streamlit_elements import elements, mui
    import datetime
    import streamlit_folium
    import folium

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
        "Thông tin cá nhân", "Liên hệ", "Mở rộng","Quan hệ lao động", "Khen thưởng/Kỷ luật", "Tài liệu scan"
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