def page_work_relationship(person=None, work_relationships=None):
    import streamlit as st
    from streamlit_elements import elements, mui
    from streamlit_agraph import agraph, Node, Edge, Config

    # Dummy person và work_relationships (nếu không truyền vào)
    if person is None:
        person = {
            "id": "person-001",
            "name": "Nguyễn Văn A",
            "avatar": "https://randomuser.me/api/portraits/men/65.jpg",
        }
    if work_relationships is None:
        work_relationships = [
            {
                "id": "wr-abc",
                "legal_entity": "Công ty ABC",
                "relationship_type": "Nhân viên chính thức",
                "emp_code": "EMP001",
                "status": "Active",
                "from_date": "2021-01-15",
                "to_date": None,
                "assignments": [
                    {
                        "id": "as-1",
                        "job_title": "Lập trình viên chính",
                        "department": "Phòng CNTT",
                        "emp_code": "EMP001",
                        "status": "Active",
                        "from_date": "2021-01-15",
                        "to_date": None,
                        "contract": "HD-001",
                    }
                ]
            },
            {
                "id": "wr-xyz",
                "legal_entity": "Công ty XYZ",
                "relationship_type": "Cộng tác viên",
                "emp_code": "EMPX23",
                "status": "Inactive",
                "from_date": "2020-03-01",
                "to_date": "2022-12-31",
                "assignments": [
                    {
                        "id": "as-2",
                        "job_title": "Tư vấn CNTT",
                        "department": "Phòng Dự án",
                        "emp_code": "EMPX23",
                        "status": "Đã kết thúc",
                        "from_date": "2020-03-01",
                        "to_date": "2022-12-31",
                        "contract": "HD-002",
                    }
                ]
            },
        ]

    st.subheader("🤝 Quan hệ lao động")
    st.caption("1 nhân sự có thể có nhiều quan hệ lao động với các pháp nhân khác nhau, mỗi quan hệ có nhiều vị trí/assignment.")

    # --- Bảng chi tiết Work Relationship ---
    with elements("workrel-table"):
        mui.Typography("Danh sách quan hệ lao động (Work Relationships)", variant="h6")
        for wr in work_relationships:
            with mui.Accordion(defaultExpanded=False, sx={"mb": 2}):
                with mui.AccordionSummary():
                    mui.Avatar("🏢", sx={"mr": 2})
                    mui.Typography(f"{wr['legal_entity']} - {wr['relationship_type']} (Emp Code: {wr['emp_code']})", sx={"fontWeight": 600, "mr":2})
                    mui.Chip(label=wr['status'], color="success" if wr['status']=="Active" else "warning", size="small")
                    mui.Typography(f"Từ: {wr['from_date']} {'→ Đến: '+wr['to_date'] if wr['to_date'] else ''}", sx={"ml":2})
                with mui.AccordionDetails():
                    mui.Typography("Assignments:", variant="subtitle1")
                    mui.TableContainer(
                        mui.Table(
                            mui.TableHead(
                                mui.TableRow(
                                    mui.TableCell("Job"),
                                    mui.TableCell("Phòng ban"),
                                    mui.TableCell("Trạng thái"),
                                    mui.TableCell("Từ"),
                                    mui.TableCell("Đến"),
                                    mui.TableCell("Contract"),
                                )
                            ),
                            mui.TableBody(
                                *[
                                    mui.TableRow(
                                        mui.TableCell(a["job_title"]),
                                        mui.TableCell(a["department"]),
                                        mui.TableCell(a["status"]),
                                        mui.TableCell(a["from_date"]),
                                        mui.TableCell(a["to_date"] or "Hiện tại"),
                                        mui.TableCell(a["contract"]),
                                    )
                                    for a in wr["assignments"]
                                ]
                            ),
                        )
                    )

    st.divider()

    # --- Graph trực quan các quan hệ ---
    st.markdown("### Sơ đồ mối liên hệ lao động (Person – Work Relationship – Assignment)")

    nodes = []
    edges = []

    # Node person
    nodes.append(Node(id=person["id"], label=person["name"], shape="circularImage", image=person["avatar"], size=50, color="#1565c0"))

    # Node work relationship (legal entity)
    for wr in work_relationships:
        wr_node_id = wr["id"]
        nodes.append(Node(id=wr_node_id, label=f"{wr['legal_entity']}\n{wr['relationship_type']}", size=30, color="#5e35b1"))
        edges.append(Edge(source=person["id"], target=wr_node_id, label="Work Rel."))

        # Node assignment
        for a in wr["assignments"]:
            as_node_id = a["id"]
            nodes.append(Node(id=as_node_id, label=f"{a['job_title']}\n{a['department']}", size=25, color="#43a047"))
            edges.append(Edge(source=wr_node_id, target=as_node_id, label="Assignment"))

            # Node contract (tuỳ chọn)
            if "contract" in a and a["contract"]:
                c_node_id = f"ct-{a['contract']}"
                nodes.append(Node(id=c_node_id, label=f"HĐ: {a['contract']}", size=18, color="#ef6c00"))
                edges.append(Edge(source=as_node_id, target=c_node_id, label="Contract"))

    config = Config(
        width=800,
        height=500,
        directed=True,
        nodeHighlightBehavior=True,
        highlightColor="#f50057",
        collapsible=True,
        node={'labelProperty':'label'},
        link={'labelProperty':'label', 'renderLabel': True}
    )

    agraph(nodes=nodes, edges=edges, config=config)

    st.caption("Sơ đồ trên giúp HR dễ dàng hình dung quan hệ giữa nhân sự - pháp nhân - các vị trí và hợp đồng. Có thể mở rộng để thể hiện nhiều tầng quan hệ hơn.")
