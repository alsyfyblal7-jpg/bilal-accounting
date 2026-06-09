"""
بلال المحاسبي البسيط - النسخة الكاملة (Offline 100%)
يعمل بدون إنترنت تماماً عبر سيرفر محلي مدمج وواجهة Flet WebView
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import threading
import flet as ft
from datetime import datetime

# ملف البيانات المحلي
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "bilal_data.json")

def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {"customers": [], "settings": {"name": "البقالة", "logo": None}}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# قالب HTML المعدل ليعمل بدون إنترنت (تم استبدال أيقونات FontAwesome بأيقونات نصية ورموز تعبيرية لضمان عملها Offline)
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#059669">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <title>بلال المحاسبي البسيط</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            background-color: #f3f4f6;
            color: #1f2937;
            padding-bottom: 24px;
        }

        .header {
            background: linear-gradient(135deg, #059669, #047857);
            color: white;
            padding: 20px 16px;
            position: sticky;
            top: 0;
            z-index: 50;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }

        .header-title {
            font-size: 1.25rem;
            font-weight: bold;
            margin-bottom: 4px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            padding: 16px;
        }

        .stat-card {
            background: white;
            padding: 16px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            border-right: 4px solid #059669;
        }

        .stat-card.danger {
            border-right-color: #dc2626;
        }

        .stat-label {
            font-size: 0.85rem;
            color: #6b7280;
        }

        .stat-value {
            font-size: 1.2rem;
            font-weight: bold;
            margin-top: 4px;
        }

        .search-box {
            padding: 0 16px 12px;
        }

        .search-input {
            width: 100%;
            padding: 12px 16px;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            font-size: 0.95rem;
            background-color: white;
            outline: none;
        }

        .customer-list {
            padding: 0 16px;
        }

        .customer-card {
            background: white;
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
        }

        .customer-info h4 {
            font-size: 1.05rem;
            margin-bottom: 4px;
        }

        .customer-info p {
            font-size: 0.85rem;
            color: #6b7280;
        }

        .customer-balance {
            text-align: left;
            font-weight: bold;
        }

        .balance-debt { color: #dc2626; }
        .balance-credit { color: #059669; }

        /* الأزرار العائمة الثابتة بالأسفل */
        .fab {
            position: fixed;
            bottom: 24px;
            left: 24px;
            background-color: #059669;
            color: white;
            width: 56px;
            height: 56px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 10px rgba(5,150,105,0.4);
            font-size: 24px;
            border: none;
            cursor: pointer;
            z-index: 100;
        }

        /* الشاشات المنبثقة Modals */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            align-items: flex-end;
        }

        .modal.active {
            display: flex;
        }

        .modal-content {
            background: white;
            width: 100%;
            border-top-left-radius: 20px;
            border-top-right-radius: 20px;
            padding: 24px 16px;
            max-height: 85vh;
            overflow-y: auto;
        }

        .modal-title {
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 16px;
            display: flex;
            justify-content: space-between;
        }

        .close-btn {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #6b7280;
        }

        .form-group {
            margin-bottom: 16px;
        }

        .form-group label {
            display: block;
            font-size: 0.9rem;
            color: #4b5563;
            margin-bottom: 6px;
        }

        .form-control {
            width: 100%;
            padding: 12px;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            font-size: 1rem;
            outline: none;
        }

        .btn {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            margin-top: 8px;
        }

        .btn-primary {
            background-color: #059669;
            color: white;
        }

        /* تفاصيل العميل */
        .tx-item {
            padding: 12px;
            border-bottom: 1px solid #f3f4f6;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .icon-btn {
            background: #f3f4f6;
            border: none;
            padding: 8px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1.1rem;
        }
        
        .icon-btn.danger {
            background: #fee2e2;
            color: #dc2626;
        }
    </style>
</head>
<body>

    <div class="header">
        <div class="header-title" id="store-name">بلال المحاسبي</div>
        <div style="font-size: 0.85rem; opacity: 0.9;">إدارة الحسابات بكل سهولة وبلدون إنترنت</div>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-label">إجمالي لنا (ديون)</div>
            <div class="stat-value" id="total-debt" style="color: #dc2626;">0 ر.ي</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">عدد العملاء</div>
            <div class="stat-value" id="total-customers">0</div>
        </div>
    </div>

    <div class="search-box">
        <input type="text" class="search-input" id="search-input" placeholder="🔍 ابحث عن عميل..." oninput="renderCustomers()">
    </div>

    <div class="customer-list" id="customer-list"></div>

    <button class="fab" onclick="openModal('add-customer-modal')">➕</button>

    <div id="add-customer-modal" class="modal">
        <div class="modal-content">
            <div class="modal-title">
                <span>إضافة عميل جديد</span>
                <button class="close-btn" onclick="closeModal('add-customer-modal')">&times;</button>
            </div>
            <div class="form-group">
                <label>اسم العميل *</label>
                <input type="text" id="cust-name" class="form-control" placeholder="أدخل اسم العميل الثنائي أو الثلاثي">
            </div>
            <div class="form-group">
                <label>رقم الهاتف (اختياري)</label>
                <input type="tel" id="cust-phone" class="form-control" placeholder="77xxxxxxx">
            </div>
            <button class="btn btn-primary" onclick="addCustomer()">حفظ العميل</button>
        </div>
    </div>

    <div id="customer-detail-modal" class="modal">
        <div class="modal-content" style="max-height: 90vh;">
            <div class="modal-title">
                <span id="detail-title">تفاصيل العميل</span>
                <button class="close-btn" onclick="closeModal('customer-detail-modal')">&times;</button>
            </div>
            
            <div style="display: flex; gap: 8px; margin-bottom: 16px;">
                <button class="btn" style="background-color: #fee2e2; color: #dc2626; margin:0;" onclick="openTxModal('debt')">🛑 تسجيل دين (عليه)</button>
                <button class="btn" style="background-color: #d1fae5; color: #059669; margin:0;" onclick="openTxModal('pay')">💵 تسجيل سداد (له)</button>
            </div>

            <h4 style="margin-bottom: 8px; font-size: 0.95rem; color: #4b5563;">سجل العمليات:</h4>
            <div id="tx-history" style="border: 1px solid #e5e7eb; border-radius: 8px; max-height: 250px; overflow-y: auto;"></div>
            
            <button class="btn icon-btn danger" style="margin-top: 20px; width: auto;" id="delete-cust-btn">🗑️ حذف الحساب بالكامل</button>
        </div>
    </div>

    <div id="tx-modal" class="modal" style="z-index: 1100;">
        <div class="modal-content">
            <div class="modal-title">
                <span id="tx-modal-title">إضافة عملية</span>
                <button class="close-btn" onclick="closeModal('tx-modal')">&times;</button>
            </div>
            <div class="form-group">
                <label>المبلغ *</label>
                <input type="number" id="tx-amount" class="form-control" placeholder="0.00" inputmode="decimal">
            </div>
            <div class="form-group">
                <label>البيان / التفاصيل</label>
                <input type="text" id="tx-desc" class="form-control" placeholder="مثلاً: كيس دقيق، صابون، إلخ...">
            </div>
            <button class="btn btn-primary" id="tx-submit-btn">حفظ العملية</button>
        </div>
    </div>

    <script>
        let appData = { customers: [] };
        let currentCustomerId = null;

        async function loadAppData() {
            try {
                const response = await fetch('/api/data');
                appData = await response.json();
                renderCustomers();
            } catch (e) {
                console.error("خطأ في تحميل البيانات", e);
            }
        }

        async function saveAppData() {
            try {
                await fetch('/api/data', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(appData)
                });
                renderCustomers();
            } catch (e) {
                alert("تعذر حفظ التغييرات محلياً!");
            }
        }

        function openModal(id) {
            document.getElementById(id).classList.add('active');
        }

        function closeModal(id) {
            document.getElementById(id).classList.remove('active');
        }

        function addCustomer() {
            const name = document.getElementById('cust-name').value.trim();
            const phone = document.getElementById('cust-phone').value.trim();
            
            if(!name) {
                alert("يرجى إدخال اسم العميل");
                return;
            }

            const newCust = {
                id: 'c_' + Date.now(),
                name: name,
                phone: phone,
                transactions: [],
                createdAt: new Date().toISOString()
            };

            appData.customers.push(newCust);
            saveAppData();
            
            // تصفية الحقول
            document.getElementById('cust-name').value = '';
            document.getElementById('cust-phone').value = '';
            closeModal('add-customer-modal');
        }

        function getCustomerBalance(cust) {
            let bal = 0;
            cust.transactions.forEach(t => {
                if(t.type === 'debt') bal += t.amount;
                if(t.type === 'pay') bal -= t.amount;
            });
            return bal;
        }

        function renderCustomers() {
            const search = document.getElementById('search-input').value.toLowerCase();
            const listDiv = document.getElementById('customer-list');
            listDiv.innerHTML = '';

            let totalDebt = 0;
            let count = 0;

            appData.customers.forEach(cust => {
                if(search && !cust.name.toLowerCase().includes(search)) return;
                
                count++;
                const bal = getCustomerBalance(cust);
                if (bal > 0) totalDebt += bal;

                const card = document.createElement('div');
                card.className = 'customer-card';
                card.onclick = () => openCustomerDetail(cust.id);

                card.innerHTML = `
                    <div class="customer-info">
                        <h4>${cust.name}</h4>
                        <p>${cust.phone ? '📱 ' + cust.phone : 'لا يوجد رقم هاتف'}</p>
                    </div>
                    <div class="customer-balance ${bal > 0 ? 'balance-debt' : 'balance-credit'}">
                        ${bal === 0 ? 'خالي' : bal + ' ر.ي'}
                    </div>
                `;
                listDiv.appendChild(card);
            });

            document.getElementById('total-customers').innerText = count;
            document.getElementById('total-debt').innerText = totalDebt + ' ر.ي';
        }

        function openCustomerDetail(id) {
            currentCustomerId = id;
            const cust = appData.customers.find(c => c.id === id);
            if(!cust) return;

            document.getElementById('detail-title').innerText = cust.name;
            
            const historyDiv = document.getElementById('tx-history');
            historyDiv.innerHTML = '';

            if(cust.transactions.length === 0) {
                historyDiv.innerHTML = '<div style="padding:16px; text-align:center; color:#6b7280;">لا توجد عمليات مسجلة لهذا العميل</div>';
            } else {
                // عرض العمليات من الأحدث للأقدم
                [...cust.transactions].reverse().forEach(t => {
                    const item = document.createElement('div');
                    item.className = 'tx-item';
                    const dateStr = new Date(t.date).toLocaleDateString('ar-YE', {month:'short', day:'numeric'});
                    
                    item.innerHTML = `
                        <div>
                            <div style="font-weight:bold; color:${t.type==='debt'?'#dc2626':'#059669'}">
                                ${t.type==='debt'?'🛑 عليه: ':'💵 سدد: '} ${t.amount} ر.ي
                            </div>
                            <div style="font-size:0.8rem; color:#6b7280;">${t.description || 'بدون بيان'}</div>
                        </div>
                        <div style="font-size:0.8rem; color:#9ca3af;">
                            ${dateStr}
                            <button class="icon-btn danger" style="padding:2px 6px; margin-right:8px; font-size:0.8rem;" onclick="deleteTx('${t.id}', event)">✕</button>
                        </div>
                    `;
                    historyDiv.appendChild(item);
                });
            }

            document.getElementById('delete-cust-btn').onclick = () => {
                if(confirm(`هل أنت متأكد من حذف حساب العميل (${cust.name}) نهائياً؟`)) {
                    appData.customers = appData.customers.filter(c => c.id !== id);
                    saveAppData();
                    closeModal('customer-detail-modal');
                }
            };

            openModal('customer-detail-modal');
        }

        function openTxModal(type) {
            document.getElementById('tx-modal-title').innerText = type === 'debt' ? 'تسجيل مبلغ على العميل (دين)' : 'تسجيل مبلغ مستلم (سداد)';
            document.getElementById('tx-amount').value = '';
            document.getElementById('tx-desc').value = '';
            
            document.getElementById('tx-submit-btn').onclick = () => {
                const amount = parseFloat(document.getElementById('tx-amount').value);
                const desc = document.getElementById('tx-desc').value.trim();

                if(!amount || amount <= 0) {
                    alert("يرجى إدخال مبلغ صحيح");
                    return;
                }

                const cust = appData.customers.find(c => c.id === currentCustomerId);
                if(cust) {
                    cust.transactions.push({
                        id: 't_' + Date.now(),
                        type: type,
                        amount: amount,
                        description: desc,
                        date: new Date().toISOString()
                    });
                    saveAppData();
                    closeModal('tx-modal');
                    openCustomerDetail(currentCustomerId); // تحديث القائمة الداخلية
                }
            };

            openModal('tx-modal');
        }

        function deleteTx(txId, event) {
            event.stopPropagation(); // منع إغلاق المودال الرئيسي
            if(!confirm("هل تريد حذف هذه العملية؟")) return;

            const cust = appData.customers.find(c => c.id === currentCustomerId);
            if(cust) {
                cust.transactions = cust.transactions.filter(t => t.id !== txId);
                saveAppData();
                openCustomerDetail(currentCustomerId);
            }
        }

        // بدء تحميل البيانات عند فتح التطبيق
        window.onload = loadAppData;
    </script>
</body>
</html>
'''

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
        elif self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            data = load_data()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/data':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                save_data(data)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "ok"}')
            except Exception as e:
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass

def run_server():
    # تشغيل السيرفر المحلي في الخلفية صامت تماماً لتلبية طلبات التطبيق بدون إنترنت
    server = HTTPServer(('127.0.0.1', 8000), RequestHandler)
    server.serve_forever()

def main(page: ft.Page):
    # إعدادات واجهة Flet التي تحمل الـ WebView
    page.title = "Belal Accountant"
    page.padding = 0
    
    # تشغيل السيرفر المحلي فوراً
    threading.Thread(target=run_server, daemon=True).start()
    
    # استدعاء السيرفر المحرك الداخلي المخفي
    wv = ft.WebView(
        url="http://127.0.0.1:8000",
        expand=True
    )
    
    page.add(wv)

if __name__ == "__main__":
    ft.app(target=main)