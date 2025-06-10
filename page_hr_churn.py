def page_hr_churn():
    import streamlit as st
    from streamlit_elements import elements, dashboard, mui, nivo
    from datetime import datetime

    # Dummy data biến động
    churn_kpi = [
        {"label": "Tổng biến động", "value": "11", "color": "purple"},
        {"label": "Tuyển mới", "value": "7", "color": "blue"},
        {"label": "Nghỉ việc", "value": "3", "color": "red"},
        {"label": "Điều chuyển", "value": "1", "color": "orange"},
    ]
    cols = st.columns(len(churn_kpi))
    for i, col in enumerate(cols):
        with col:
            st.markdown(
                f"""
                <div style="background:{churn_kpi[i]['color']};padding:12px;border-radius:10px;color:white;position:relative">
                    <b>{churn_kpi[i]['label']}</b>
                    <div style="font-size:2em">{churn_kpi[i]['value']}</div>
                </div>
                """, unsafe_allow_html=True
            )
    st.divider()

    # Data cho chart
    bar_data = [
        {"Tháng": "03/2024", "Tuyển mới": 3, "Nghỉ việc": 1, "Điều chuyển": 0},
        {"Tháng": "04/2024", "Tuyển mới": 2, "Nghỉ việc": 1, "Điều chuyển": 1},
        {"Tháng": "05/2024", "Tuyển mới": 1, "Nghỉ việc": 1, "Điều chuyển": 0},
        {"Tháng": "06/2024", "Tuyển mới": 1, "Nghỉ việc": 0, "Điều chuyển": 0},
    ]

    # Timeline data (list of event)
    timeline_events = [
        {"date": "2024-06-07", "name": "Nguyễn Văn A", "type": "Tuyển mới", "color": "blue"},
        {"date": "2024-06-03", "name": "Lê Thị B", "type": "Nghỉ việc", "color": "red"},
        {"date": "2024-05-21", "name": "Phạm C", "type": "Điều chuyển", "color": "orange"},
        {"date": "2024-05-15", "name": "Trần D", "type": "Tuyển mới", "color": "blue"},
    ]

    # Table chi tiết
    table_rows = [
        {"Ngày": "2024-06-07", "Nhân viên": "Nguyễn Văn A", "Loại": "Tuyển mới", "Phòng ban": "IT", "Ghi chú": ""},
        {"Ngày": "2024-06-03", "Nhân viên": "Lê Thị B", "Loại": "Nghỉ việc", "Phòng ban": "Kế toán", "Ghi chú": "Chuyển công ty"},
        {"Ngày": "2024-05-21", "Nhân viên": "Phạm C", "Loại": "Điều chuyển", "Phòng ban": "Vận hành → Nhân sự", "Ghi chú": "Định biên mới"},
        {"Ngày": "2024-05-15", "Nhân viên": "Trần D", "Loại": "Tuyển mới", "Phòng ban": "Nhân sự", "Ghi chú": ""},
        # ... có thể thêm dòng
    ]

    # LAYOUT DASHBOARD: bar + timeline ngang hàng, table bên dưới
    layout = [
        dashboard.Item("bar", 0, 0, 5, 4, isDraggable=False, isResizable=False),
        dashboard.Item("timeline", 5, 0, 5, 4, isDraggable=False, isResizable=False),
        dashboard.Item("table", 0, 4, 12, 4, isDraggable=False, isResizable=False),
    ]

    # Filter đơn giản
    with st.expander("Bộ lọc"):
        month = st.selectbox("Chọn tháng", ["Tất cả"] + [row["Tháng"] for row in bar_data])
        churn_type = st.multiselect("Loại biến động", ["Tuyển mới", "Nghỉ việc", "Điều chuyển"], default=["Tuyển mới", "Nghỉ việc", "Điều chuyển"])
        # Thực tế có thể filter bảng theo month/type

    with elements("dashboard-churn"):
        with dashboard.Grid(layout, draggableHandle=".MuiCard-root"):
            # BAR CHART
            with mui.Card(key="bar", sx={"p": 2, "m": 1, "minHeight": 320}):
                mui.Typography("Biến động nhân sự theo tháng", variant="h6")
                nivo.Bar(
                    data=bar_data,
                    keys=churn_type,
                    indexBy="Tháng",
                    margin={"top": 20, "right": 20, "bottom": 50, "left": 50},
                    padding=0.3,
                    groupMode="grouped",
                    colors={"scheme": "category10"},
                    axisBottom={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "Tháng",
                        "legendPosition": "middle",
                        "legendOffset": 32,
                    },
                    axisLeft={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "Số người",
                        "legendPosition": "middle",
                        "legendOffset": -40,
                    },
                    tooltip=lambda d: f"{d['id']}: {d['value']}",
                    labelSkipWidth=12,
                    labelSkipHeight=12,
                )

            # TIMELINE (vertical card list)
            with mui.Card(key="timeline", sx={"p": 2, "m": 1, "minHeight": 320}):
                mui.Typography("Timeline biến động", variant="h6")
                for event in sorted(timeline_events, key=lambda x: x["date"], reverse=True):
                    with mui.Paper(sx={"my": 1, "p": 1, "bgcolor": "#f6f8fa"}):
                        mui.Typography(
                            f"{event['date']} – {event['name']}",
                            variant="subtitle1",
                            sx={"color": event["color"]}
                        )
                        mui.Typography(
                            f"{event['type']}",
                            variant="body2",
                            sx={"fontWeight": "bold"}
                        )

            # BẢNG CHI TIẾT
            with mui.Card(key="table", sx={"p": 2, "m": 1, "minHeight": 240}):
                mui.Typography("Danh sách biến động chi tiết", variant="h6")
                mui.TableContainer(
                    mui.Table(
                        mui.TableHead(
                            mui.TableRow(
                                *[mui.TableCell(col) for col in table_rows[0].keys()]
                            )
                        ),
                        mui.TableBody(
                            *[
                                mui.TableRow(
                                    *[mui.TableCell(str(cell)) for cell in row.values()]
                                )
                                for row in table_rows
                                if (month == "Tất cả" or row["Ngày"][5:7] == month[0:2]) and row["Loại"] in churn_type
                            ]
                        ),
                    )
                )