// API hiện tại của backend:
// GET  /api/statistics
// CRUD sinh viên nên dùng:
// GET  /api/students
// POST /api/students
// PUT  /api/students/{id}
// DELETE /api/students/{id}

const API_URL = "http://127.0.0.1:8000/api";
let currentPage = 1;
let modal;

document.addEventListener("DOMContentLoaded", () => {
    modal = new bootstrap.Modal(document.getElementById("studentModal"));
    document.getElementById("student-form").addEventListener("submit", saveStudent);
    loadStats();
    loadStudents(1);
});

async function request(url, options = {}) {
    const res = await fetch(url, {
        ...options,
        headers: {"Content-Type": "application/json", ...(options.headers || {})}
    });
    if (!res.ok) {
        let message = `HTTP ${res.status}`;
        try { const e = await res.json(); message = e.detail || message; } catch {}
        throw new Error(message);
    }
    return res.status === 204 ? null : res.json();
}

async function loadStats() {
    try {
        const data = await request(`${API_URL}/statistics`);
        document.getElementById("total-students").textContent = data.total_students ?? 0;
        document.getElementById("male-students").textContent = data.male_students ?? 0;
        document.getElementById("female-students").textContent = data.female_students ?? 0;
        document.getElementById("total-classes").textContent = data.total_classes ?? 0;
    } catch (e) {
        showAlert("Không tải được thống kê: " + e.message, "danger");
    }
}

async function loadStudents(page = 1) {
    currentPage = page;
    const keyword = encodeURIComponent(document.getElementById("search-input").value.trim());
    const gender = encodeURIComponent(document.getElementById("gender-filter").value);
    try {
        const result = await request(`${API_URL}/students?keyword=${keyword}&gender=${gender}&page=${page}&limit=10`);
        renderStudents(result.data || []);
        renderPagination(result);
    } catch (e) {
        document.getElementById("student-table-body").innerHTML =
            `<tr><td colspan="9" class="text-center text-danger">Không thể tải dữ liệu: ${escapeHtml(e.message)}</td></tr>`;
    }
}

function renderStudents(list) {
    const tbody = document.getElementById("student-table-body");
    if (!list.length) {
        tbody.innerHTML = `<tr><td colspan="9" class="text-center text-muted">Không có sinh viên.</td></tr>`;
        return;
    }
    tbody.innerHTML = list.map(sv => `
        <tr>
            <td>${sv.SinhVienID}</td>
            <td><strong>${escapeHtml(sv.MaSV)}</strong></td>
            <td>${escapeHtml(sv.HoTen)}</td>
            <td>${sv.NgaySinh || ""}</td>
            <td>${sv.GioiTinh || ""}</td>
            <td>${escapeHtml(sv.Email || "")}</td>
            <td>${sv.LopID ?? ""}</td>
            <td><span class="badge bg-info badge-status">${escapeHtml(sv.TrangThai || "")}</span></td>
            <td class="text-nowrap">
                <button class="btn btn-sm btn-warning btn-action" onclick='editStudent(${JSON.stringify(sv)})'>Sửa</button>
                <button class="btn btn-sm btn-danger" onclick="deleteStudent(${sv.SinhVienID})">Xóa</button>
            </td>
        </tr>
    `).join("");
}

function renderPagination(result) {
    const box = document.getElementById("pagination");
    const totalPages = result.total_pages || 1;
    if (totalPages <= 1) { box.innerHTML = ""; return; }
    let html = `<ul class="pagination">`;
    for (let i = 1; i <= totalPages; i++) {
        html += `<li class="page-item ${i === result.page ? "active" : ""}">
                    <button class="page-link" onclick="loadStudents(${i})">${i}</button>
                 </li>`;
    }
    html += `</ul>`;
    box.innerHTML = html;
}

function openAddModal() {
    document.getElementById("student-form").reset();
    document.getElementById("student-id").value = "";
    document.getElementById("modal-title").textContent = "Thêm sinh viên";
    document.getElementById("TrangThai").value = "Đang học";
    modal.show();
}

function editStudent(sv) {
    document.getElementById("student-id").value = sv.SinhVienID;
    document.getElementById("MaSV").value = sv.MaSV || "";
    document.getElementById("HoTen").value = sv.HoTen || "";
    document.getElementById("NgaySinh").value = sv.NgaySinh || "";
    document.getElementById("GioiTinh").value = sv.GioiTinh || "";
    document.getElementById("Email").value = sv.Email || "";
    document.getElementById("SoDienThoai").value = sv.SoDienThoai || "";
    document.getElementById("DiaChi").value = sv.DiaChi || "";
    document.getElementById("LopID").value = sv.LopID || "";
    document.getElementById("TrangThai").value = sv.TrangThai || "Đang học";
    document.getElementById("modal-title").textContent = "Cập nhật sinh viên";
    modal.show();
}

async function saveStudent(event) {
    event.preventDefault();
    const id = document.getElementById("student-id").value;
    const data = {
        MaSV: document.getElementById("MaSV").value.trim(),
        HoTen: document.getElementById("HoTen").value.trim(),
        NgaySinh: document.getElementById("NgaySinh").value || null,
        GioiTinh: document.getElementById("GioiTinh").value || null,
        Email: document.getElementById("Email").value.trim() || null,
        SoDienThoai: document.getElementById("SoDienThoai").value.trim() || null,
        DiaChi: document.getElementById("DiaChi").value.trim() || null,
        LopID: Number(document.getElementById("LopID").value),
        TrangThai: document.getElementById("TrangThai").value
    };

    try {
        await request(id ? `${API_URL}/students/${id}` : `${API_URL}/students`, {
            method: id ? "PUT" : "POST",
            body: JSON.stringify(data)
        });
        modal.hide();
        showAlert(id ? "Cập nhật thành công!" : "Thêm sinh viên thành công!", "success");
        await loadStats();
        await loadStudents(currentPage);
    } catch (e) {
        showAlert("Lưu thất bại: " + e.message, "danger");
    }
}

async function deleteStudent(id) {
    if (!confirm("Bạn có chắc muốn xóa sinh viên này không?")) return;
    try {
        await request(`${API_URL}/students/${id}`, {method:"DELETE"});
        showAlert("Xóa sinh viên thành công!", "success");
        await loadStats();
        await loadStudents(currentPage);
    } catch (e) {
        showAlert("Xóa thất bại: " + e.message, "danger");
    }
}

function resetFilter() {
    document.getElementById("search-input").value = "";
    document.getElementById("gender-filter").value = "";
    loadStudents(1);
}

function showAlert(message, type) {
    document.getElementById("alert-box").innerHTML =
        `<div class="alert alert-${type} alert-dismissible fade show">${escapeHtml(message)}
         <button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>`;
}

function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, c => ({
        "&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#039;"
    }[c]));
}
