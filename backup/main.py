import streamlit as st
import streamlit_antd_components as sac
import pandas as pd
import matplotlib.pyplot as plt

from page_hr_overview import page_hr_overview   # import hàm đã tạo
from page_hr_churn import page_hr_churn   # import hàm đã tạo
from page_person_profile import page_person_profile   # import hàm đã tạo
from page_work_relationship import page_work_relationship 
from page_employee_profile import page_employee_profile
from page_employee_360_manager_view import page_employee_360_manager_view
from page_hr_dashboard import page_hr_dashboard
from page_hr_workforce_overview import page_hr_workforce_overview
from page_hr_churn_new import page_hr_churn_new



# Cấu hình trang
st.set_page_config(page_title="xTalent Dashboard", layout="wide")
# Dashboard Menu (sử dụng SAC menu)


menu_items = [
    sac.MenuItem('Trang chủ (Dashboard)', icon='dashboard', children=[
        sac.MenuItem('Tổng quan nhân sự', icon='pie-chart'),
        sac.MenuItem('Tổng quan nhân sự other', icon='pie-chart'),
        sac.MenuItem('Biến động nhân sự', icon='bar-chart'),
        sac.MenuItem('Biến động nhân sự other', icon='bar-chart'),
        sac.MenuItem('Cảnh báo & nhắc nhở', icon='alert'),
        sac.MenuItem('Lịch sử hoạt động', icon='history'),
    ]),
    sac.MenuItem('Hồ sơ nhân sự (Core HR)', icon='team', children=[
        sac.MenuItem('Danh sách nhân viên', icon='user', children=[
            sac.MenuItem('Hồ sơ cá nhân', icon='idcard'),
            sac.MenuItem('Hồ sơ nhân viên', icon='idcard'),
            sac.MenuItem('Hồ sơ nhân viên - Manager View', icon='idcard'),
            sac.MenuItem('Quan hệ lao động', icon='solution'),
            sac.MenuItem('Hợp đồng & Phụ lục', icon='file-done'),
            sac.MenuItem('Lịch sử làm việc', icon='schedule'),
            sac.MenuItem('Liên kết các thực thể pháp lý', icon='apartment'),
        ]),
        sac.MenuItem('Vị trí & Công việc', icon='pushpin', children=[
            sac.MenuItem('Danh mục Job & Position', icon='unordered-list'),
            sac.MenuItem('Gán vị trí nhân sự', icon='user-switch'),
        ]),
        sac.MenuItem('Quản lý tổ chức', icon='cluster', children=[
            sac.MenuItem('Sơ đồ tổ chức', icon='branches'),
            sac.MenuItem('Đơn vị & BU', icon='bank'),
            sac.MenuItem('Vị trí & Khối chức năng', icon='deployment-unit'),
            sac.MenuItem('Phân quyền truy cập dữ liệu', icon='safety'),
        ]),
        sac.MenuItem('Quản lý tài khoản ngân hàng & liên hệ', icon='contacts', children=[
            sac.MenuItem('Ngân hàng cá nhân', icon='credit-card'),
            sac.MenuItem('Người thân liên hệ', icon='phone'),
        ]),
        sac.MenuItem('Tài liệu nhân sự', icon='file-text', children=[
            sac.MenuItem('Lưu trữ tài liệu', icon='save'),
            sac.MenuItem('Phân loại & tìm kiếm', icon='search'),
        ]),
        sac.MenuItem('Biểu mẫu & phê duyệt', icon='file-done', children=[
            sac.MenuItem('Yêu cầu cập nhật hồ sơ', icon='edit'),
            sac.MenuItem('Theo dõi luồng duyệt', icon='interaction'),
        ]),
    ]),
    sac.MenuItem('Chấm công – Lịch làm việc', icon='calendar', children=[
        sac.MenuItem('Cài đặt ca làm việc & lịch', icon='setting', children=[
            sac.MenuItem('Danh mục ca (Shifts)', icon='clock-circle'),
            sac.MenuItem('Mẫu lịch (Patterns)', icon='table'),
            sac.MenuItem('Gán lịch (Schedule Assignment)', icon='carry-out'),
        ]),
        sac.MenuItem('Máy chấm công & dữ liệu vào ra', icon='desktop'),
        sac.MenuItem('Phân tích vi phạm & cảnh báo', icon='warning', children=[
            sac.MenuItem('Vi phạm giờ làm', icon='close-circle'),
            sac.MenuItem('Thống kê vào trễ - về sớm', icon='rise'),
        ]),
        sac.MenuItem('Tổng hợp dữ liệu công', icon='calculator', children=[
            sac.MenuItem('Tổng hợp theo nhân viên', icon='usergroup-add'),
            sac.MenuItem('Tổng hợp theo đơn vị', icon='home'),
        ]),
    ]),
    sac.MenuItem('Quản lý Nghỉ phép (Absence)', icon='rest', children=[
        sac.MenuItem('Quản lý loại phép & hạn mức', icon='snippets', children=[
            sac.MenuItem('Danh mục loại nghỉ', icon='unordered-list'),
            sac.MenuItem('Thiết lập hạn mức nghỉ', icon='sliders'),
            sac.MenuItem('Tài khoản phép (Absence Wallet)', icon='wallet'),
        ]),
        sac.MenuItem('Theo dõi & xử lý yêu cầu nghỉ', icon='solution', children=[
            sac.MenuItem('Đăng ký nghỉ', icon='form'),
            sac.MenuItem('Lịch sử nghỉ', icon='history'),
            sac.MenuItem('Phê duyệt nghỉ', icon='safety-certificate'),
        ]),
        sac.MenuItem('Theo dõi nghỉ đặc thù', icon='medicine-box', children=[
            sac.MenuItem('Nghỉ bệnh', icon='heart'),
            sac.MenuItem('Thai sản', icon='woman'),
            sac.MenuItem('Nghỉ lễ quốc gia', icon='flag'),
        ]),
        sac.MenuItem('Quy định chuyển phép & cộng phép', icon='swap', children=[
            sac.MenuItem('Quy tắc cộng dồn / chuyển phép năm', icon='retweet'),
        ]),
    ]),
    sac.MenuItem('Tổng đãi ngộ (Total Reward)', icon='trophy', children=[
        sac.MenuItem('Lương cố định (Fixed Pay)', icon='dollar', children=[
            sac.MenuItem('Bậc lương – Thang lương', icon='unordered-list'),
            sac.MenuItem('Lịch sử tăng lương', icon='line-chart'),
            sac.MenuItem('Định biên lương theo vị trí', icon='align-left'),
        ]),
        sac.MenuItem('Lương biến đổi – Thưởng (Variable Pay)', icon='gift', children=[
            sac.MenuItem('Thưởng định kỳ (STI)', icon='calendar-check'),
            sac.MenuItem('Cổ phiếu/Quyền chọn (LTI)', icon='stock'),
            sac.MenuItem('Hoa hồng/KPI', icon='trophy'),
        ]),
        sac.MenuItem('Phúc lợi – Bảo hiểm (Benefit)', icon='insurance', children=[
            sac.MenuItem('Chương trình bảo hiểm', icon='safety-certificate'),
            sac.MenuItem('Chương trình phúc lợi mở rộng', icon='like'),
        ]),
        sac.MenuItem('Ghi nhận & khen thưởng (Recognition)', icon='star', children=[
            sac.MenuItem('Điểm thưởng', icon='star'),
            sac.MenuItem('Quà tặng & kỷ niệm chương', icon='gift'),
        ]),
        sac.MenuItem('Offer & Giữ chân', icon='smile', children=[
            sac.MenuItem('Đề xuất offer', icon='file-add'),
            sac.MenuItem('Chương trình giữ chân nhân sự', icon='team'),
        ]),
    ]),
    sac.MenuItem('Tính lương (Payroll)', icon='calculator', children=[
        sac.MenuItem('Cài đặt lịch lương', icon='calendar', children=[
            sac.MenuItem('Tần suất trả lương', icon='schedule'),
            sac.MenuItem('Nhóm lương – Lịch lương', icon='unordered-list'),
        ]),
        sac.MenuItem('Tính lương & xác nhận', icon='check-circle', children=[
            sac.MenuItem('Dữ liệu đầu vào', icon='cloud-upload'),
            sac.MenuItem('Kết quả lương', icon='check-square'),
            sac.MenuItem('Truy xuất dữ liệu lương', icon='download'),
        ]),
        sac.MenuItem('Kết nối hệ thống ngoài (Payroll Gateway)', icon='gateway', children=[
            sac.MenuItem('Giao tiếp xuất file', icon='export'),
            sac.MenuItem('Kết nối hệ thống kế toán', icon='link'),
        ]),
    ]),
    sac.MenuItem('Báo cáo & Phân tích', icon='bar-chart', children=[
        sac.MenuItem('Báo cáo nhân sự', icon='profile'),
        sac.MenuItem('Báo cáo công & nghỉ', icon='file-search'),
        sac.MenuItem('Báo cáo lương & đãi ngộ', icon='file-done'),
        sac.MenuItem('Báo cáo tuân thủ', icon='security-scan'),
        sac.MenuItem('Truy vấn dữ liệu tùy chọn (BI mini)', icon='search'),
    ]),
    sac.MenuItem('Cấu hình & hệ thống', icon='setting', children=[
        sac.MenuItem('Quản lý danh mục (code list)', icon='tags'),
        sac.MenuItem('Phân quyền & vai trò (RBAC)', icon='safety'),
        sac.MenuItem('Tùy chỉnh giao diện', icon='skin'),
        sac.MenuItem('Webhook & tích hợp API', icon='api'),
        sac.MenuItem('Nhật ký hệ thống & audit log', icon='file-protect'),
    ]),
]


with st.sidebar:
    st.title("xTalent")
    menu_id = sac.menu(items=menu_items, size='md',indent=10, color='indigo', open_all=False)


if menu_id in [None, 'Trang chủ (Dashboard)']:
    page_hr_dashboard()

elif menu_id == 'Tổng quan nhân sự':
    st.subheader("📊 Tổng quan Nhân sự")
    page_hr_overview()
elif menu_id == 'Tổng quan nhân sự other':
    page_hr_workforce_overview()
elif menu_id == 'Biến động nhân sự':
    st.subheader("📊 Biến Động Nhân sự")
    page_hr_churn()
elif menu_id == 'Biến động nhân sự other':
    page_hr_churn_new()
elif menu_id == 'Hồ sơ cá nhân':
    page_person_profile()
elif menu_id == 'Hồ sơ nhân viên':
    page_employee_profile()
elif menu_id == 'Hồ sơ nhân viên - Manager View':
    page_employee_360_manager_view()
    
elif menu_id == 'Quan hệ lao động':
    page_work_relationship()
elif menu_id == 'Hồ sơ':
    st.subheader("👤 Quản lý Hồ sơ Nhân viên")
    st.write("Tại đây bạn quản lý hồ sơ từng nhân viên, có thể nhập/tìm kiếm/sửa thông tin.")
elif menu_id == 'Tuyển dụng':
    st.subheader("📝 Quản lý Tuyển dụng")
    st.write("Module quản lý các chiến dịch tuyển dụng, vị trí, ứng viên.")
elif menu_id == 'Chấm công':
    st.subheader("⏰ Chấm công")
    st.write("Chức năng chấm công, xem lịch sử chấm công của nhân viên.")
elif menu_id == 'Lương thưởng':
    st.subheader("💰 Quản lý Lương thưởng")
    st.write("Tính lương, thưởng, xem phiếu lương.")
elif menu_id == 'Đánh giá':
    st.subheader("⭐ Đánh giá Nhân sự")
    st.write("Quản lý, thực hiện, tổng hợp đánh giá hiệu suất nhân viên.")
elif menu_id == 'Báo cáo':
    st.subheader("📈 Báo cáo tổng hợp")
    st.write("Tổng hợp báo cáo theo từng phân hệ.")

# (Có thể thêm footer, logo, hoặc component khác ở đây)
