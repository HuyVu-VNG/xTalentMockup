def page_hr_overview():
    import streamlit as st
    from streamlit_elements import elements, dashboard, mui, nivo

    # Thông báo đầu trang
    st.info("Tổng quan nhanh: Nhân sự toàn công ty tăng so với tháng trước.")
    st.warning("Có 2 hợp đồng sẽ hết hạn trong 7 ngày tới!")

    # KPI metrics
    kpi_data = [
        {"label": "Tổng nhân viên", "value": "205", "delta": "+5", "color": "green", "tooltip": "Tổng số nhân viên công ty đến thời điểm hiện tại."},
        {"label": "Tuyển mới tháng này", "value": "7", "delta": "+2", "color": "blue", "tooltip": "Nhân viên mới trong tháng này."},
        {"label": "Tỷ lệ nghỉ việc", "value": "2.4%", "delta": "-0.4%", "color": "red", "tooltip": "Tỷ lệ nghỉ việc so với tháng trước."},
        {"label": "Thử việc", "value": "11", "delta": "", "color": "orange", "tooltip": "Số nhân viên đang thử việc."},
        {"label": "Chính thức", "value": "180", "delta": "", "color": "green", "tooltip": "Số nhân viên chính thức."},
        {"label": "Tỷ lệ Nữ/Nam", "value": "45%/55%", "delta": "", "color": "purple", "tooltip": "Tỷ lệ nữ/nam trong công ty."}
    ]
    cols = st.columns(len(kpi_data))
    for i, col in enumerate(cols):
        with col:
            st.markdown(
                f"""
                <div style="background:{kpi_data[i]['color']};padding:12px;border-radius:10px;color:white;position:relative">
                    <b>{kpi_data[i]['label']}</b>
                    <span style="float:right;font-size:1.2em" title="{kpi_data[i]['tooltip']}">ℹ️</span>
                    <div style="font-size:2em">{kpi_data[i]['value']}</div>
                    <div>{kpi_data[i]['delta']}</div>
                </div>
                """, unsafe_allow_html=True
            )

    st.divider()

    # Data cho chart và bảng
    dept_data = [
        {"id": "IT", "value": 70},
        {"id": "Kế toán", "value": 60},
        {"id": "Nhân sự", "value": 40},
        {"id": "Vận hành", "value": 20},
        {"id": "Khác", "value": 15}
    ]
    bar_data = [
        {"Tháng": "03/2024", "Tuyển mới": 5, "Nghỉ việc": 2},
        {"Tháng": "04/2024", "Tuyển mới": 7, "Nghỉ việc": 3},
        {"Tháng": "05/2024", "Tuyển mới": 4, "Nghỉ việc": 1},
        {"Tháng": "06/2024", "Tuyển mới": 6, "Nghỉ việc": 2},
    ]
    table_rows = [
        {"Phòng ban": "IT", "Tuyển mới": 2, "Nghỉ việc": 0, "Tổng biến động": 2},
        {"Phòng ban": "Kế toán", "Tuyển mới": 1, "Nghỉ việc": 2, "Tổng biến động": 3},
        {"Phòng ban": "Nhân sự", "Tuyển mới": 1, "Nghỉ việc": 1, "Tổng biến động": 2},
    ]

    # Dashboard layout
    layout = [
        dashboard.Item("pie", 0, 0, 4, 4, isDraggable=False, isResizable=False),
        dashboard.Item("bar", 5, 0, 4, 4, isDraggable=False, isResizable=False),
        dashboard.Item("table", 0, 4, 12, 4, isDraggable=False, isResizable=False),
    ]

    # CHÚ Ý: chỉ dùng streamlit_elements component trong elements context!
    with elements("dashboard"):
        with dashboard.Grid(layout, draggableHandle=".MuiCard-root"):
            # Pie Chart block
            with mui.Card(key="pie", sx={"p": 2, "m": 1, "minHeight": 350}):
                mui.Typography("Cơ cấu nhân sự theo phòng ban", variant="h6")
                nivo.Pie(
                    data=dept_data,
                    margin={"top": 20, "right": 80, "bottom": 20, "left": 80},
                    innerRadius=0.5,
                    padAngle=0.7,
                    cornerRadius=3,
                    activeOuterRadiusOffset=8,
                    colors={"scheme": "set3"},
                    borderWidth=1,
                    arcLinkLabelsSkipAngle=10,
                    arcLinkLabelsTextColor="#333333",
                    arcLinkLabelsThickness=2,
                    arcLabelsRadiusOffset=0.5,
                    arcLabelsTextColor="#000",
                    legends=[
                        {
                            "anchor": "right",
                            "direction": "column",
                            "justify": False,
                            "translateX": 80,
                            "translateY": 0,
                            "itemsSpacing": 5,
                            "itemWidth": 60,
                            "itemHeight": 18,
                            "itemTextColor": "#999",
                            "itemDirection": "left-to-right",
                            "symbolSize": 12,
                        }
                    ],
                    tooltip=lambda d: f"{d['id']}: {d['value']} người"
                )

            # Bar Chart block
            with mui.Card(key="bar", sx={"p": 2, "m": 1, "minHeight": 350}):
                mui.Typography("Biến động nhân sự theo tháng", variant="h6")
                nivo.Bar(
                    data=bar_data,
                    keys=["Tuyển mới", "Nghỉ việc"],
                    indexBy="Tháng",
                    margin={"top": 20, "right": 20, "bottom": 50, "left": 50},
                    padding=0.3,
                    groupMode="grouped",
                    colors={"scheme": "pastel1"},
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

            # Table block
            with mui.Card(key="table", sx={"p": 2, "m": 1}):
                mui.Typography("Phòng ban nhiều biến động", variant="h6")
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
                            ]
                        ),
                    )
                )