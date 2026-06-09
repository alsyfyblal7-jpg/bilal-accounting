"""
بلال المحاسبي البسيط - النسخة الكاملة
جميع الميزات متوفرة
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
from datetime import datetime

# ملف البيانات
import os
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

# HTML الكامل
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
            font-family: 'Segoe UI', Tahoma, Arial, sans-serif;
            -webkit-tap-highlight-color: transparent;
        }
        html, body {
            height: 100%;
            overflow: hidden;
        }
        body {
            background: #f0f2f5;
        }
        #app {
            height: 100%;
            overflow-y: auto;
        }
        
        /* ===== Header Styles ===== */
        .header {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            padding: 45px 20px 25px;
        }
        .header-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .header-logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .header-logo img {
            width: 45px;
            height: 45px;
            border-radius: 12px;
            object-fit: cover;
            border: 2px solid rgba(255,255,255,0.3);
        }
        .header h1 {
            font-size: 22px;
        }
        .header p {
            opacity: 0.8;
            font-size: 13px;
        }
        .settings-btn {
            background: rgba(255,255,255,0.2);
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 20px;
            color: white;
            font-size: 20px;
            cursor: pointer;
        }
        .total-card {
            background: rgba(255,255,255,0.15);
            border-radius: 15px;
            padding: 15px;
            margin-top: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .total-card .amount {
            font-size: 26px;
            font-weight: bold;
        }
        .total-card .label {
            font-size: 12px;
            opacity: 0.8;
        }
        
        /* ===== Search ===== */
        .search-container {
            padding: 0 15px;
            margin-top: -15px;
        }
        .search-box {
            background: white;
            border-radius: 15px;
            padding: 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .search-box input {
            width: 100%;
            padding: 15px 20px;
            border: none;
            font-size: 15px;
            text-align: right;
        }
        .search-box input:focus {
            outline: none;
        }
        
        /* ===== Customer List ===== */
        .list-header {
            padding: 15px 20px 10px;
            color: #6b7280;
            font-size: 13px;
            display: flex;
            justify-content: space-between;
        }
        .customers-list {
            padding: 0 15px 100px;
        }
        .customer-card {
            background: white;
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            cursor: pointer;
            transition: transform 0.2s;
        }
        .customer-card:active {
            transform: scale(0.98);
        }
        .customer-avatar {
            width: 50px;
            height: 50px;
            border-radius: 25px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 20px;
            flex-shrink: 0;
        }
        .avatar-debt { background: linear-gradient(135deg, #f87171, #dc2626); }
        .avatar-ok { background: linear-gradient(135deg, #4ade80, #16a34a); }
        .avatar-credit { background: linear-gradient(135deg, #60a5fa, #2563eb); }
        .avatar-warning { background: linear-gradient(135deg, #fbbf24, #f59e0b); }
        .customer-info {
            flex: 1;
            text-align: right;
            min-width: 0;
        }
        .customer-name {
            font-weight: bold;
            font-size: 16px;
            color: #1f2937;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .customer-phone {
            font-size: 13px;
            color: #9ca3af;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 5px;
        }
        .customer-balance {
            text-align: left;
            flex-shrink: 0;
        }
        .balance-amount {
            font-weight: bold;
            font-size: 17px;
        }
        .balance-debt { color: #dc2626; }
        .balance-ok { color: #16a34a; }
        .balance-credit { color: #2563eb; }
        .balance-label {
            font-size: 10px;
            color: #9ca3af;
        }
        .arrow-icon {
            color: #d1d5db;
            font-size: 18px;
        }
        
        /* ===== Empty State ===== */
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #9ca3af;
        }
        .empty-state .icon {
            font-size: 70px;
            margin-bottom: 15px;
        }
        .empty-state p {
            margin: 5px 0;
        }
        
        /* ===== FAB ===== */
        .fab {
            position: fixed;
            bottom: 25px;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 60px;
            border-radius: 30px;
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            border: none;
            font-size: 32px;
            box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4);
            cursor: pointer;
            z-index: 100;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .fab:active {
            transform: translateX(-50%) scale(0.9);
        }
        
        /* ===== Modal ===== */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            align-items: flex-end;
            justify-content: center;
        }
        .modal-overlay.active { display: flex; }
        .modal-content {
            background: white;
            border-radius: 25px 25px 0 0;
            padding: 20px 25px 30px;
            width: 100%;
            max-width: 500px;
            max-height: 90vh;
            overflow-y: auto;
            animation: slideUp 0.3s ease;
        }
        @keyframes slideUp {
            from { transform: translateY(100%); }
            to { transform: translateY(0); }
        }
        .modal-handle {
            width: 40px;
            height: 4px;
            background: #e5e7eb;
            border-radius: 2px;
            margin: 0 auto 20px;
        }
        .modal-title {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;
        }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #374151;
            font-size: 14px;
        }
        .form-group input, .form-group textarea {
            width: 100%;
            padding: 14px 16px;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            font-size: 16px;
            text-align: right;
            transition: border-color 0.2s;
        }
        .form-group input:focus, .form-group textarea:focus {
            outline: none;
            border-color: #10b981;
        }
        .form-group .hint {
            font-size: 12px;
            color: #9ca3af;
            margin-top: 5px;
        }
        .input-with-btn {
            display: flex;
            gap: 10px;
        }
        .input-with-btn input {
            flex: 1;
        }
        .input-with-btn button {
            width: 50px;
            height: 50px;
            border: 2px solid #10b981;
            background: #f0fdf4;
            border-radius: 12px;
            color: #10b981;
            font-size: 20px;
            cursor: pointer;
            flex-shrink: 0;
        }
        .contact-picker-btn {
            background: linear-gradient(135deg, #fef3c7, #fde68a);
            border: 2px dashed #f59e0b;
            border-radius: 12px;
            padding: 12px;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            color: #b45309;
            font-weight: 500;
            cursor: pointer;
            margin-bottom: 15px;
        }
        
        /* ===== Buttons ===== */
        .btn {
            padding: 14px 25px;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
            transition: transform 0.2s;
        }
        .btn:active {
            transform: scale(0.98);
        }
        .btn-primary {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
        }
        .btn-secondary {
            background: #f3f4f6;
            color: #6b7280;
        }
        .btn-danger {
            background: linear-gradient(135deg, #f87171, #dc2626);
            color: white;
        }
        .btn-success {
            background: linear-gradient(135deg, #4ade80, #16a34a);
            color: white;
        }
        .btn-whatsapp {
            background: #25d366;
            color: white;
        }
        .btn-sms {
            background: #8b5cf6;
            color: white;
        }
        .btn-blue {
            background: linear-gradient(135deg, #60a5fa, #3b82f6);
            color: white;
        }
        .btn-row {
            display: flex;
            gap: 10px;
        }
        .btn-row .btn {
            flex: 1;
        }
        
        /* ===== Detail Page ===== */
        .detail-header {
            padding: 45px 20px 30px;
            text-align: center;
            color: white;
            position: relative;
        }
        .detail-header.debt { background: linear-gradient(135deg, #f87171, #dc2626); }
        .detail-header.ok { background: linear-gradient(135deg, #10b981, #059669); }
        .detail-header.credit { background: linear-gradient(135deg, #60a5fa, #2563eb); }
        .detail-header.warning { background: linear-gradient(135deg, #fbbf24, #f59e0b); }
        
        .back-btn {
            position: absolute;
            top: 45px;
            right: 15px;
            background: rgba(255,255,255,0.2);
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 20px;
            color: white;
            font-size: 20px;
            cursor: pointer;
        }
        .menu-btn {
            position: absolute;
            top: 45px;
            left: 15px;
            background: rgba(255,255,255,0.2);
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 20px;
            color: white;
            font-size: 20px;
            cursor: pointer;
        }
        .detail-avatar {
            width: 80px;
            height: 80px;
            border-radius: 40px;
            background: rgba(255,255,255,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 12px;
            font-size: 32px;
            font-weight: bold;
        }
        .detail-name {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .detail-phone {
            opacity: 0.8;
            font-size: 14px;
        }
        .balance-card {
            background: rgba(255,255,255,0.2);
            border-radius: 15px;
            padding: 15px 20px;
            margin-top: 15px;
            display: inline-block;
            min-width: 200px;
        }
        .balance-card .label {
            font-size: 12px;
            opacity: 0.8;
        }
        .balance-card .value {
            font-size: 28px;
            font-weight: bold;
        }
        .balance-card .currency {
            font-size: 14px;
            opacity: 0.8;
        }
        .limit-info {
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid rgba(255,255,255,0.2);
            font-size: 13px;
        }
        .limit-info div {
            display: flex;
            justify-content: space-between;
            margin: 5px 0;
        }
        .over-limit-badge {
            background: rgba(255,255,255,0.3);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 10px;
            display: inline-block;
        }
        
        /* ===== Message Buttons ===== */
        .msg-buttons {
            display: flex;
            gap: 8px;
            justify-content: center;
            margin-top: 15px;
            flex-wrap: wrap;
        }
        .msg-btn {
            padding: 8px 14px;
            border: none;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .msg-btn.whatsapp { background: #25d366; color: white; }
        .msg-btn.sms { background: #8b5cf6; color: white; }
        .msg-btn.pdf { background: #3b82f6; color: white; }
        
        /* ===== Action Buttons ===== */
        .action-buttons {
            display: flex;
            gap: 12px;
            padding: 0 15px;
            margin-top: -18px;
        }
        .action-btn {
            flex: 1;
            padding: 15px;
            border: none;
            border-radius: 15px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            background: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .action-btn:active {
            transform: scale(0.95);
        }
        .action-btn.debt { color: #dc2626; }
        .action-btn.payment { color: #16a34a; }
        
        /* ===== Transactions ===== */
        .section-title {
            padding: 20px 20px 10px;
            font-weight: bold;
            color: #6b7280;
            font-size: 14px;
        }
        .transactions-list {
            padding: 0 15px 30px;
        }
        .transaction-item {
            background: white;
            padding: 14px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .tx-icon {
            width: 42px;
            height: 42px;
            border-radius: 21px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            flex-shrink: 0;
        }
        .tx-icon.debt { background: #fef2f2; }
        .tx-icon.payment { background: #f0fdf4; }
        .tx-info {
            flex: 1;
            text-align: right;
            min-width: 0;
        }
        .tx-desc {
            font-weight: 500;
            color: #1f2937;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .tx-date {
            font-size: 12px;
            color: #9ca3af;
            margin-top: 3px;
        }
        .tx-amount {
            font-weight: bold;
            font-size: 16px;
            flex-shrink: 0;
        }
        .tx-amount.debt { color: #dc2626; }
        .tx-amount.payment { color: #16a34a; }
        .tx-delete {
            background: none;
            border: none;
            color: #d1d5db;
            font-size: 18px;
            cursor: pointer;
            padding: 5px;
        }
        .tx-delete:hover {
            color: #ef4444;
        }
        
        /* ===== Settings Page ===== */
        .settings-header {
            background: linear-gradient(135deg, #475569, #1e293b);
            color: white;
            padding: 45px 20px 25px;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .settings-content {
            padding: 20px 15px 50px;
        }
        .settings-card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        .settings-card h3 {
            font-size: 16px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .logo-upload {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }
        .logo-preview {
            width: 70px;
            height: 70px;
            border-radius: 15px;
            background: #f3f4f6;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            border: 2px dashed #d1d5db;
            cursor: pointer;
            overflow: hidden;
        }
        .logo-preview img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .logo-info {
            flex: 1;
        }
        .logo-info p {
            font-size: 13px;
            color: #6b7280;
        }
        .logo-info button {
            margin-top: 8px;
            padding: 6px 12px;
            border: none;
            background: #fee2e2;
            color: #dc2626;
            border-radius: 8px;
            font-size: 12px;
            cursor: pointer;
        }
        .app-info {
            text-align: center;
            padding: 30px;
        }
        .app-info .icon {
            font-size: 50px;
            margin-bottom: 10px;
        }
        .app-info h3 {
            font-size: 18px;
            margin-bottom: 5px;
        }
        .app-info p {
            color: #9ca3af;
            font-size: 14px;
        }
        .contact-card {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
        }
        .contact-card h4 {
            font-size: 14px;
            color: #374151;
            margin-bottom: 15px;
            text-align: center;
        }
        .contact-links {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .contact-link {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 15px;
            background: #f9fafb;
            border-radius: 10px;
            text-decoration: none;
            color: #374151;
        }
        .contact-link:active {
            background: #f3f4f6;
        }
        .contact-link-info {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .contact-link-icon {
            width: 35px;
            height: 35px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }
        .contact-link-icon.instagram { background: linear-gradient(135deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); color: white; }
        .contact-link-icon.telegram { background: #0088cc; color: white; }
        .contact-link-icon.email { background: #ea4335; color: white; }
        .contact-link span {
            font-size: 14px;
        }
        .contact-link small {
            color: #9ca3af;
            font-size: 12px;
        }
        
        /* ===== Dropdown Menu ===== */
        .dropdown-menu {
            display: none;
            position: absolute;
            top: 90px;
            left: 15px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            overflow: hidden;
            z-index: 100;
            min-width: 160px;
        }
        .dropdown-menu.active {
            display: block;
        }
        .dropdown-item {
            padding: 14px 18px;
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            border: none;
            background: none;
            width: 100%;
            text-align: right;
            font-size: 14px;
        }
        .dropdown-item:hover {
            background: #f3f4f6;
        }
        .dropdown-item.danger {
            color: #dc2626;
        }
        .dropdown-item.danger:hover {
            background: #fef2f2;
        }
        
        /* ===== Confirm Dialog ===== */
        .confirm-dialog {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            border-radius: 20px;
            padding: 25px;
            width: calc(100% - 50px);
            max-width: 350px;
            text-align: center;
            z-index: 1001;
        }
        .confirm-icon {
            font-size: 50px;
            margin-bottom: 15px;
        }
        .confirm-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .confirm-message {
            color: #6b7280;
            font-size: 14px;
            margin-bottom: 20px;
        }
        
        /* ===== Preview Box ===== */
        .preview-box {
            background: #f0fdf4;
            border: 1px solid #86efac;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .preview-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 10px;
            color: #166534;
            font-size: 13px;
        }
        .preview-content {
            background: white;
            border-radius: 10px;
            padding: 12px;
            font-size: 13px;
            line-height: 1.6;
            white-space: pre-wrap;
            color: #374151;
        }
        
        /* ===== Statement Preview ===== */
        .statement-preview {
            background: linear-gradient(135deg, #10b981, #059669);
            border-radius: 15px;
            padding: 20px;
            color: white;
            margin-bottom: 20px;
        }
        .statement-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }
        .statement-customer {
            text-align: right;
        }
        .statement-customer h4 {
            font-size: 18px;
            margin-bottom: 3px;
        }
        .statement-customer p {
            font-size: 13px;
            opacity: 0.8;
        }
        .statement-date {
            font-size: 12px;
            opacity: 0.7;
            text-align: left;
        }
        .statement-balance {
            background: rgba(255,255,255,0.2);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
        }
        .statement-balance .label {
            font-size: 12px;
            opacity: 0.8;
        }
        .statement-balance .amount {
            font-size: 28px;
            font-weight: bold;
        }
        .statement-footer {
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
            font-size: 13px;
        }
        .statement-footer span {
            background: rgba(255,255,255,0.2);
            padding: 5px 12px;
            border-radius: 20px;
        }
        
        /* Print styles */
        @media print {
            body { padding: 0 !important; }
        }
    </style>
</head>
<body>
    <div id="app"></div>

    <script>
        // ===== Data =====
        let data = %%DATA%%;
        let currentView = 'list';
        let selectedCustomer = null;
        let selectedCustomerIndex = -1;

        // ===== Helpers =====
        function getBalance(customer) {
            let balance = 0;
            (customer.transactions || []).forEach(tx => {
                if (tx.type === 'debt') balance += tx.amount;
                else balance -= tx.amount;
            });
            return balance;
        }

        function formatCurrency(amount) {
            return Math.abs(amount).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
        }

        function fmtMoney(amount) {
            return formatCurrency(amount) + ' ' + getCurrencySymbol();
        }

        function formatDate(dateStr) {
            const days = ['الأحد', 'الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت'];
            const d = new Date(dateStr);
            return days[d.getDay()] + ' ' + d.toLocaleDateString('en-CA');
        }

        function formatTime(dateStr) {
            const d = new Date(dateStr);
            return d.toLocaleTimeString('en-US', {hour: '2-digit', minute: '2-digit', hour12: false});
        }

        function generateId() {
            return Date.now().toString() + Math.random().toString(36).substr(2, 9);
        }

        function saveData() {
            fetch('/save', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
        }

        function getStoreName() {
            return data.settings?.name || 'البقالة';
        }

        function getStoreLogo() {
            return data.settings?.logo || null;
        }

        function getCurrency() {
            const code = data.settings?.currency || 'SAR';
            const currencies = {
                'SAR': {name: 'ريال سعودي', symbol: 'ريال'},
                'YER': {name: 'ريال يمني', symbol: 'ر.ي'},
                'USD': {name: 'دولار أمريكي', symbol: '$'},
                'EUR': {name: 'يورو', symbol: '€'},
                'AED': {name: 'درهم إماراتي', symbol: 'د.إ'},
                'KWD': {name: 'دينار كويتي', symbol: 'د.ك'},
                'BHD': {name: 'دينار بحريني', symbol: 'د.ب'},
                'OMR': {name: 'ريال عماني', symbol: 'ر.ع'},
                'QAR': {name: 'ريال قطري', symbol: 'ر.ق'},
                'EGP': {name: 'جنيه مصري', symbol: 'ج.م'},
                'JOD': {name: 'دينار أردني', symbol: 'د.أ'},
                'LBP': {name: 'ليرة لبنانية', symbol: 'ل.ل'},
                'SDG': {name: 'جنيه سوداني', symbol: 'ج.س'},
                'TRY': {name: 'ليرة تركية', symbol: '₺'},
                'GBP': {name: 'جنيه استرليني', symbol: '£'},
            };
            return currencies[code] || currencies['SAR'];
        }

        function getCurrencySymbol() {
            return getCurrency().symbol;
        }

        function isOverLimit(customer) {
            const limit = customer.creditLimit || 0;
            if (limit <= 0) return false;
            return getBalance(customer) >= limit;
        }

        function getRemainingCredit(customer) {
            const limit = customer.creditLimit || 0;
            if (limit <= 0) return Infinity;
            return Math.max(0, limit - getBalance(customer));
        }

        // Contact Picker API
        async function pickContact() {
            if ('contacts' in navigator && 'ContactsManager' in window) {
                try {
                    const contacts = await navigator.contacts.select(['name', 'tel'], {multiple: false});
                    if (contacts && contacts.length > 0) {
                        const name = contacts[0].name?.[0] || '';
                        let phone = contacts[0].tel?.[0] || '';
                        phone = phone.replace(/[\\s\\-\\(\\)]/g, '');
                        return {name, phone};
                    }
                } catch (e) {
                    console.log('Contact picker error:', e);
                }
            }
            return null;
        }

        // ===== PDF Generation =====
        function generatePDF() {
            const c = selectedCustomer;
            const balance = getBalance(c);
            const storeName = getStoreName();
            const storeLogo = getStoreLogo();
            const curr = getCurrencySymbol();
            const transactions = [...(c.transactions || [])].sort((a, b) => new Date(b.date) - new Date(a.date));
            const today = formatDate(new Date().toISOString());
            
            let txRows = '';
            transactions.forEach((tx, i) => {
                const isDebt = tx.type === 'debt';
                txRows += `
                    <tr style="background:${i % 2 === 0 ? '#f9fafb' : 'white'}">
                        <td style="padding:10px 6px;text-align:center;border-bottom:1px solid #e5e7eb;font-size:11px">${formatDate(tx.date)}</td>
                        <td style="padding:10px 6px;text-align:center;border-bottom:1px solid #e5e7eb">${formatTime(tx.date)}</td>
                        <td style="padding:10px 6px;text-align:right;border-bottom:1px solid #e5e7eb">${tx.description}</td>
                        <td style="padding:10px 6px;text-align:center;border-bottom:1px solid #e5e7eb;color:${isDebt ? '#dc2626' : '#ccc'};font-weight:bold">${isDebt ? '+'+formatCurrency(tx.amount) : '-'}</td>
                        <td style="padding:10px 6px;text-align:center;border-bottom:1px solid #e5e7eb;color:${!isDebt ? '#16a34a' : '#ccc'};font-weight:bold">${!isDebt ? '-'+formatCurrency(tx.amount) : '-'}</td>
                    </tr>`;
            });
            
            const pdfHtml = `<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<title>كشف حساب - ${c.name}</title>
<style>
    * { margin:0; padding:0; box-sizing:border-box; font-family: 'Segoe UI', Tahoma, Arial, sans-serif; }
    body { background: white; padding: 20px; direction: rtl; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    @media print {
        body { padding: 0; }
        .no-print { display: none !important; }
        @page { margin: 10mm; }
    }
    table { width: 100%; border-collapse: collapse; }
    th, td { padding: 8px; }
</style>
</head>
<body>
    <div class="no-print" style="text-align:center;padding:15px;background:#10b981;color:white;border-radius:12px;margin-bottom:20px">
        <button onclick="window.print()" style="background:white;color:#10b981;border:none;padding:15px 50px;border-radius:12px;font-size:18px;font-weight:bold;cursor:pointer">
            🖨️ طباعة / حفظ PDF
        </button>
        <p style="margin-top:10px;font-size:13px;opacity:0.9">اختر "حفظ كـ PDF" من خيارات الطابعة</p>
    </div>

    <div style="background:linear-gradient(135deg,#10b981,#059669);padding:25px;border-radius:15px;text-align:center;color:white;margin-bottom:20px">
        ${storeLogo ? `<img src="${storeLogo}" style="width:60px;height:60px;border-radius:12px;object-fit:cover;margin-bottom:10px;border:3px solid rgba(255,255,255,0.3)">` : ''}
        <h1 style="font-size:24px">${storeName}</h1>
        <p style="opacity:0.8;font-size:14px;margin-top:8px">كشف حساب العميل</p>
        <p style="opacity:0.7;font-size:12px;margin-top:5px">${today}</p>
    </div>
    
    <div style="background:#f9fafb;padding:20px;border-radius:12px;margin-bottom:20px">
        <div style="display:flex;justify-content:space-between">
            <div><p style="color:#6b7280;font-size:12px">رقم الجوال</p><p style="font-size:16px;font-weight:bold;margin-top:5px">${c.phone || 'غير محدد'}</p></div>
            <div style="text-align:right"><p style="color:#6b7280;font-size:12px">اسم العميل</p><p style="font-size:18px;font-weight:bold;margin-top:5px">${c.name}</p></div>
        </div>
    </div>
    
    <div style="background:${balance > 0 ? '#fef2f2' : '#f0fdf4'};border:2px solid ${balance > 0 ? '#fca5a5' : '#86efac'};padding:25px;border-radius:12px;text-align:center;margin-bottom:20px">
        <p style="color:#6b7280;font-size:14px">${balance > 0 ? 'المبلغ المستحق' : 'الرصيد'}</p>
        <p style="font-size:32px;font-weight:bold;color:${balance > 0 ? '#dc2626' : '#16a34a'};margin-top:10px">${formatCurrency(balance)} ${curr}</p>
        ${c.creditLimit > 0 ? `<p style="color:#6b7280;font-size:12px;margin-top:10px">سقف المديونية: ${formatCurrency(c.creditLimit)} ${curr}</p>` : ''}
    </div>
    
    <h3 style="font-size:16px;margin:20px 0 15px;padding-bottom:10px;border-bottom:2px solid #e5e7eb">📋 سجل المعاملات (${transactions.length})</h3>
    
    ${transactions.length > 0 ? `
        <table>
            <thead>
                <tr style="background:#10b981;color:white">
                    <th style="padding:12px 6px;text-align:center;border-radius:8px 0 0 0;font-size:12px">التاريخ</th>
                    <th style="padding:12px 6px;text-align:center;font-size:12px">الوقت</th>
                    <th style="padding:12px 6px;text-align:right;font-size:12px">البيان</th>
                    <th style="padding:12px 6px;text-align:center;font-size:12px">دين (+)</th>
                    <th style="padding:12px 6px;text-align:center;border-radius:0 8px 0 0;font-size:12px">سداد (-)</th>
                </tr>
            </thead>
            <tbody>${txRows}</tbody>
        </table>
    ` : '<p style="text-align:center;color:#9ca3af;padding:30px">لا توجد معاملات</p>'}
    
    <div style="margin-top:30px;padding-top:20px;border-top:2px solid #e5e7eb;text-align:center">
        <p style="color:#9ca3af;font-size:11px">تم إنشاء هذا الكشف بواسطة تطبيق بلال المحاسبي البسيط</p>
        <p style="color:#9ca3af;font-size:11px;margin-top:5px">${storeName} - ${today}</p>
    </div>
</body>
</html>`;
            
            // Open in new window for printing
            const printWindow = window.open('', '_blank');
            if (printWindow) {
                printWindow.document.write(pdfHtml);
                printWindow.document.close();
            } else {
                alert('الرجاء السماح بالنوافذ المنبثقة لتحميل الكشف');
            }
        }

        // ===== Render =====
        function render() {
            const app = document.getElementById('app');
            if (currentView === 'list') {
                app.innerHTML = renderList();
            } else if (currentView === 'detail') {
                app.innerHTML = renderDetail();
            } else if (currentView === 'settings') {
                app.innerHTML = renderSettings();
            }
        }

        function renderList() {
            const customers = data.customers || [];
            const totalDebt = customers.reduce((sum, c) => sum + Math.max(0, getBalance(c)), 0);
            const storeName = getStoreName();
            const storeLogo = getStoreLogo();

            let customersHtml = '';
            if (customers.length === 0) {
                customersHtml = `
                    <div class="empty-state">
                        <div class="icon">👥</div>
                        <p style="font-size:18px;font-weight:bold;">لا يوجد عملاء بعد</p>
                        <p>اضغط + لإضافة عميل جديد</p>
                    </div>`;
            } else {
                customers.forEach((c, i) => {
                    const balance = getBalance(c);
                    const hasDebt = balance > 0;
                    const hasCredit = balance < 0;
                    const overLimit = isOverLimit(c);
                    
                    let avatarClass = 'avatar-ok';
                    let balanceClass = 'balance-ok';
                    let statusText = 'لا دين';
                    
                    if (overLimit) {
                        avatarClass = 'avatar-warning';
                        balanceClass = 'balance-debt';
                        statusText = '⚠️ تجاوز السقف';
                    } else if (hasDebt) {
                        avatarClass = 'avatar-debt';
                        balanceClass = 'balance-debt';
                        statusText = 'عليه دين';
                    } else if (hasCredit) {
                        avatarClass = 'avatar-credit';
                        balanceClass = 'balance-credit';
                        statusText = 'له رصيد';
                    }
                    
                    customersHtml += `
                        <div class="customer-card" onclick="openCustomer(${i})">
                            <div class="customer-avatar ${avatarClass}">${c.name[0]}</div>
                            <div class="customer-info">
                                <div class="customer-name">${c.name}</div>
                                <div class="customer-phone"><span>${c.phone || 'بدون رقم'}</span>📱</div>
                            </div>
                            <div class="customer-balance">
                                <div class="balance-amount ${balanceClass}">${formatCurrency(balance)}</div>
                                <div class="balance-label">${statusText}</div>
                            </div>
                            <span class="arrow-icon">‹</span>
                        </div>
                    `;
                });
            }

            return `
                <div class="header">
                    <div class="header-top">
                        <button class="settings-btn" onclick="goToSettings()">⚙️</button>
                        <div class="header-logo">
                            <div style="text-align:right">
                                <h1>${storeName} 🏪</h1>
                                <p>إدارة حسابات العملاء</p>
                            </div>
                            ${storeLogo ? `<img src="${storeLogo}" alt="Logo">` : ''}
                        </div>
                    </div>
                    <div class="total-card">
                        <div>💰</div>
                        <div style="text-align:left">
                            <div class="label">إجمالي الديون المستحقة</div>
                            <div class="amount">${formatCurrency(totalDebt)} <span style="font-size:14px">${getCurrencySymbol()}</span></div>
                        </div>
                    </div>
                </div>
                
                <div class="search-container">
                    <div class="search-box">
                        <input type="text" id="searchInput" placeholder="🔍 ابحث عن عميل بالاسم أو الرقم..." oninput="filterCustomers()">
                    </div>
                </div>
                
                <div class="list-header">
                    <span>${customers.length} عميل</span>
                    <span id="searchClear" style="display:none;cursor:pointer;color:#10b981" onclick="clearSearch()">مسح البحث</span>
                </div>
                
                <div class="customers-list" id="customersList">${customersHtml}</div>
                
                <button class="fab" onclick="showAddCustomerModal()">+</button>
                
                ${renderAddCustomerModal()}
            `;
        }

        function renderAddCustomerModal() {
            return `
                <div class="modal-overlay" id="addCustomerModal">
                    <div class="modal-content">
                        <div class="modal-handle"></div>
                        <div class="modal-title">👤 إضافة عميل جديد</div>
                        
                        <button class="contact-picker-btn" onclick="pickContactForAdd()">
                            📱 اختيار من جهات الاتصال
                        </button>
                        
                        <div style="display:flex;align-items:center;gap:10px;margin-bottom:15px">
                            <div style="flex:1;height:1px;background:#e5e7eb"></div>
                            <span style="color:#9ca3af;font-size:12px">أو أدخل يدوياً</span>
                            <div style="flex:1;height:1px;background:#e5e7eb"></div>
                        </div>
                        
                        <div class="form-group">
                            <label>اسم العميل *</label>
                            <input type="text" id="newName" placeholder="مثال: أبو محمد">
                        </div>
                        
                        <div class="form-group">
                            <label>رقم الجوال</label>
                            <input type="tel" id="newPhone" placeholder="05XXXXXXXX" dir="ltr" style="text-align:right">
                        </div>
                        
                        <div class="form-group">
                            <label>سقف المديونية (اختياري)</label>
                            <input type="number" id="newLimit" placeholder="0 يعني بدون حد" dir="ltr" style="text-align:right">
                            <div class="hint">عند وصول العميل للحد سيتم تنبيهك</div>
                        </div>
                        
                        <button class="btn btn-primary" onclick="addCustomer()">إضافة العميل ✓</button>
                        <button class="btn btn-secondary" onclick="hideModal('addCustomerModal')">إلغاء</button>
                    </div>
                </div>
            `;
        }

        function renderDetail() {
            const c = selectedCustomer;
            const balance = getBalance(c);
            const hasDebt = balance > 0;
            const hasCredit = balance < 0;
            const limit = c.creditLimit || 0;
            const overLimit = isOverLimit(c);
            const remaining = getRemainingCredit(c);
            const transactions = [...(c.transactions || [])].sort((a, b) => new Date(b.date) - new Date(a.date));
            const storeName = getStoreName();

            let headerClass = 'ok';
            let statusLabel = 'الرصيد';
            if (overLimit) {
                headerClass = 'warning';
                statusLabel = 'المبلغ المستحق';
            } else if (hasDebt) {
                headerClass = 'debt';
                statusLabel = 'المبلغ المستحق';
            } else if (hasCredit) {
                headerClass = 'credit';
                statusLabel = 'رصيد متبقي';
            }

            let txHtml = '';
            if (transactions.length === 0) {
                txHtml = `
                    <div class="empty-state">
                        <div class="icon">📭</div>
                        <p style="font-size:16px;font-weight:bold;">لا توجد معاملات</p>
                        <p>ابدأ بتسجيل دين أو سداد</p>
                    </div>`;
            } else {
                transactions.forEach((tx) => {
                    const isDebt = tx.type === 'debt';
                    txHtml += `
                        <div class="transaction-item">
                            <div class="tx-icon ${isDebt ? 'debt' : 'payment'}">${isDebt ? '📝' : '💰'}</div>
                            <div class="tx-info">
                                <div class="tx-desc">${tx.description}</div>
                                <div class="tx-date">${formatDate(tx.date)} • ${formatTime(tx.date)}</div>
                            </div>
                            <div class="tx-amount ${isDebt ? 'debt' : 'payment'}">${isDebt ? '+' : '-'}${formatCurrency(tx.amount)}</div>
                            <button class="tx-delete" onclick="confirmDeleteTx('${tx.id}')">🗑️</button>
                        </div>
                    `;
                });
            }

            return `
                <div class="detail-header ${headerClass}">
                    <button class="back-btn" onclick="goBack()">→</button>
                    <button class="menu-btn" onclick="toggleMenu()">⋮</button>
                    
                    <div class="dropdown-menu" id="customerMenu">
                        <button class="dropdown-item" onclick="showEditModal()">✏️ تعديل البيانات</button>
                        <button class="dropdown-item danger" onclick="confirmDeleteCustomer()">🗑️ حذف العميل</button>
                    </div>
                    
                    ${overLimit ? '<div class="over-limit-badge">⚠️ تجاوز سقف المديونية!</div>' : ''}
                    
                    <div class="detail-avatar">${c.name[0]}</div>
                    <div class="detail-name">${c.name}</div>
                    <div class="detail-phone">📱 ${c.phone || 'بدون رقم'}</div>
                    
                    <div class="balance-card">
                        <div class="label">${statusLabel}</div>
                        <div class="value">${formatCurrency(balance)}</div>
                        <div class="currency">${getCurrency().name}</div>
                        ${limit > 0 ? `
                            <div class="limit-info">
                                <div><span>سقف المديونية:</span><strong>${fmtMoney(limit)}</strong></div>
                                ${hasDebt && !overLimit ? `<div><span>المتبقي للسقف:</span><strong>${fmtMoney(remaining)}</strong></div>` : ''}
                            </div>
                        ` : ''}
                    </div>
                    
                    <div class="msg-buttons">
                        ${hasDebt ? `
                            <button class="msg-btn whatsapp" onclick="showWhatsAppModal()">💬 واتساب</button>
                            <button class="msg-btn sms" onclick="sendSMS()">📱 SMS</button>
                        ` : ''}
                        <button class="msg-btn pdf" onclick="showStatementModal()">📋 كشف حساب</button>
                    </div>
                </div>
                
                <div class="action-buttons">
                    <button class="action-btn debt" onclick="showTxModal('debt')">📝 تسجيل دين</button>
                    <button class="action-btn payment" onclick="showTxModal('payment')">💰 تسجيل سداد</button>
                </div>
                
                <div class="section-title">📋 سجل المعاملات (${transactions.length})</div>
                <div class="transactions-list">${txHtml}</div>
                
                ${renderTxModal()}
                ${renderEditModal()}
                ${renderWhatsAppModal()}
                ${renderStatementModal()}
                ${renderConfirmDialog()}
                ${renderLimitAlertModal()}
            `;
        }

        function renderTxModal() {
            return `
                <div class="modal-overlay" id="txModal">
                    <div class="modal-content">
                        <div class="modal-handle"></div>
                        <div class="modal-title" id="txModalTitle">تسجيل</div>
                        
                        <div class="form-group">
                            <label>المبلغ (${getCurrencySymbol()}) *</label>
                            <input type="number" id="txAmount" placeholder="0.00" dir="ltr" style="text-align:center;font-size:24px;font-weight:bold;">
                        </div>
                        
                        <div class="form-group">
                            <label>الوصف (اختياري)</label>
                            <input type="text" id="txDesc" placeholder="مثال: مشتريات بقالة">
                        </div>
                        
                        <input type="hidden" id="txType">
                        
                        <button class="btn" id="txSubmitBtn" onclick="addTransaction()">تسجيل ✓</button>
                        <button class="btn btn-secondary" onclick="hideModal('txModal')">إلغاء</button>
                    </div>
                </div>
            `;
        }

        function renderEditModal() {
            const c = selectedCustomer;
            return `
                <div class="modal-overlay" id="editModal">
                    <div class="modal-content">
                        <div class="modal-handle"></div>
                        <div class="modal-title">✏️ تعديل بيانات العميل</div>
                        
                        <button class="contact-picker-btn" onclick="pickContactForEdit()">
                            📱 اختيار من جهات الاتصال
                        </button>
                        
                        <div class="form-group">
                            <label>الاسم</label>
                            <input type="text" id="editName" value="${c?.name || ''}">
                        </div>
                        
                        <div class="form-group">
                            <label>رقم الجوال</label>
                            <input type="tel" id="editPhone" value="${c?.phone || ''}" dir="ltr" style="text-align:right">
                        </div>
                        
                        <div class="form-group">
                            <label>سقف المديونية</label>
                            <input type="number" id="editLimit" value="${c?.creditLimit || 0}" dir="ltr" style="text-align:right">
                            <div class="hint">0 يعني بدون حد للمديونية</div>
                        </div>
                        
                        <button class="btn btn-primary" onclick="saveCustomerEdit()">حفظ ✓</button>
                        <button class="btn btn-secondary" onclick="hideModal('editModal')">إلغاء</button>
                    </div>
                </div>
            `;
        }

        function renderWhatsAppModal() {
            const c = selectedCustomer;
            const balance = getBalance(c);
            const storeName = getStoreName();
            
            const message = `السلام عليكم ورحمة الله وبركاته 🙏

أخي الكريم *${c?.name}*

نود تذكيرك بأن لديك مبلغ مستحق لدى *${storeName}*

💰 المبلغ المستحق: *${fmtMoney(balance)}*

نرجو التكرم بالسداد في أقرب وقت ممكن.

شاكرين لكم تعاملكم معنا 🌹
${storeName}`;

            return `
                <div class="modal-overlay" id="whatsappModal">
                    <div class="modal-content">
                        <div class="modal-handle"></div>
                        <div class="modal-title">💬 إرسال تذكير واتساب</div>
                        
                        <div class="preview-box">
                            <div class="preview-header">👁️ معاينة الرسالة</div>
                            <div class="preview-content">${message}</div>
                        </div>
                        
                        <div class="form-group">
                            <label>رقم جوال العميل</label>
                            <div class="input-with-btn">
                                <input type="tel" id="waPhone" value="${c?.phone || ''}" placeholder="05XXXXXXXX" dir="ltr" style="text-align:right">
                                <button onclick="pickContactForWhatsApp()">📱</button>
                            </div>
                        </div>
                        
                        <button class="btn btn-whatsapp" onclick="sendWhatsApp()">إرسال واتساب 💬</button>
                        <button class="btn btn-secondary" onclick="hideModal('whatsappModal')">إلغاء</button>
                    </div>
                </div>
            `;
        }

        function renderStatementModal() {
            const c = selectedCustomer;
            const balance = getBalance(c);
            const storeName = getStoreName();
            const storeLogo = getStoreLogo();
            const txCount = c?.transactions?.length || 0;

            return `
                <div class="modal-overlay" id="statementModal">
                    <div class="modal-content">
                        <div class="modal-handle"></div>
                        <div class="modal-title">📋 كشف حساب العميل</div>
                        
                        <div class="statement-preview">
                            <div class="statement-header">
                                <div class="statement-date">${formatDate(new Date().toISOString())}</div>
                                <div class="statement-customer">
                                    ${storeLogo ? `<img src="${storeLogo}" style="width:40px;height:40px;border-radius:10px;float:left;margin-left:10px">` : ''}
                                    <h4>${c?.name}</h4>
                                    <p>${c?.phone || 'بدون رقم'}</p>
                                </div>
                            </div>
                            <div class="statement-balance">
                                <div class="label">${balance > 0 ? 'المبلغ المستحق' : 'الرصيد'}</div>
                                <div class="amount">${fmtMoney(balance)}</div>
                            </div>
                            <div class="statement-footer">
                                <span>${txCount} معاملة</span>
                                <span>${storeName}</span>
                            </div>
                        </div>
                        
                        <button class="btn btn-blue" onclick="generatePDF()">📥 تحميل PDF</button>
                        
                        <div style="display:flex;align-items:center;gap:10px;margin:15px 0">
                            <div style="flex:1;height:1px;background:#e5e7eb"></div>
                            <span style="color:#9ca3af;font-size:12px">أو</span>
                            <div style="flex:1;height:1px;background:#e5e7eb"></div>
                        </div>
                        
                        <div class="form-group">
                            <label>إرسال الكشف عبر واتساب</label>
                            <div class="input-with-btn">
                                <input type="tel" id="stmtPhone" value="${c?.phone || ''}" placeholder="05XXXXXXXX" dir="ltr" style="text-align:right">
                                <button onclick="pickContactForStatement()">📱</button>
                            </div>
                        </div>
                        
                        <button class="btn btn-whatsapp" onclick="sendStatementWhatsApp()">📤 إرسال واتساب</button>
                        <button class="btn btn-secondary" onclick="hideModal('statementModal')">إغلاق</button>
                    </div>
                </div>
            `;
        }

        function renderConfirmDialog() {
            return `
                <div class="modal-overlay" id="confirmDialog">
                    <div class="confirm-dialog">
                        <div class="confirm-icon" id="confirmIcon">⚠️</div>
                        <div class="confirm-title" id="confirmTitle">تأكيد</div>
                        <div class="confirm-message" id="confirmMessage">هل أنت متأكد؟</div>
                        <div class="btn-row">
                            <button class="btn btn-danger" id="confirmYesBtn">نعم</button>
                            <button class="btn btn-secondary" onclick="hideModal('confirmDialog')">إلغاء</button>
                        </div>
                    </div>
                </div>
            `;
        }

        function renderLimitAlertModal() {
            const c = selectedCustomer;
            const balance = getBalance(c);
            const limit = c?.creditLimit || 0;

            return `
                <div class="modal-overlay" id="limitAlertModal">
                    <div class="confirm-dialog" style="max-width:380px">
                        <div class="confirm-icon">⚠️</div>
                        <div class="confirm-title">تنبيه: تجاوز سقف المديونية!</div>
                        <div class="confirm-message">العميل <strong>${c?.name}</strong> وصل للحد الأقصى للمديونية</div>
                        <div style="background:#fef3c7;border-radius:12px;padding:15px;margin-bottom:15px;text-align:right">
                            <div style="display:flex;justify-content:space-between;margin-bottom:8px">
                                <strong style="color:#dc2626">${fmtMoney(balance)}</strong>
                                <span style="color:#6b7280">المبلغ المستحق:</span>
                            </div>
                            <div style="display:flex;justify-content:space-between">
                                <strong>${fmtMoney(limit)}</strong>
                                <span style="color:#6b7280">سقف المديونية:</span>
                            </div>
                        </div>
                        <div class="btn-row">
                            <button class="btn btn-whatsapp" onclick="sendLimitAlert()">📱 إرسال تنبيه</button>
                            <button class="btn btn-secondary" onclick="hideModal('limitAlertModal')">إغلاق</button>
                        </div>
                    </div>
                </div>
            `;
        }

        function renderSettings() {
            const storeName = getStoreName();
            const storeLogo = getStoreLogo();
            
            return `
                <div class="settings-header">
                    <button class="back-btn" style="position:static" onclick="goBack()">→</button>
                    <div>
                        <h1 style="font-size:20px">⚙️ الإعدادات</h1>
                        <p style="opacity:0.8;font-size:13px">إعدادات التطبيق والنسخ الاحتياطي</p>
                    </div>
                </div>
                
                <div class="settings-content">
                    <div class="settings-card">
                        <h3>🏪 بيانات المتجر</h3>
                        
                        <div class="logo-upload">
                            <div class="logo-preview" onclick="document.getElementById('logoInput').click()">
                                ${storeLogo ? `<img src="${storeLogo}" alt="Logo">` : '📷'}
                            </div>
                            <input type="file" id="logoInput" accept="image/*" style="display:none" onchange="uploadLogo(event)">
                            <div class="logo-info">
                                <p>اضغط لاختيار شعار المتجر</p>
                                <p style="font-size:11px">يظهر في كشف الحساب والرسائل</p>
                                ${storeLogo ? `<button onclick="removeLogo()">إزالة الشعار</button>` : ''}
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label>اسم المتجر</label>
                            <input type="text" id="storeName" value="${storeName}" placeholder="مثال: بقالة أبو محمد">
                        </div>
                        
                        <div class="form-group">
                            <label>💱 العملة</label>
                            <select id="currencySelect" style="width:100%;padding:14px 16px;border:2px solid #e5e7eb;border-radius:12px;font-size:16px;text-align:right;background:white;appearance:auto">
                                <option value="SAR" ${(data.settings?.currency || 'SAR') === 'SAR' ? 'selected' : ''}>🇸🇦 ريال سعودي (ريال)</option>
                                <option value="YER" ${data.settings?.currency === 'YER' ? 'selected' : ''}>🇾🇪 ريال يمني (ر.ي)</option>
                                <option value="USD" ${data.settings?.currency === 'USD' ? 'selected' : ''}>🇺🇸 دولار أمريكي ($)</option>
                                <option value="EUR" ${data.settings?.currency === 'EUR' ? 'selected' : ''}>🇪🇺 يورو (€)</option>
                                <option value="AED" ${data.settings?.currency === 'AED' ? 'selected' : ''}>🇦🇪 درهم إماراتي (د.إ)</option>
                                <option value="KWD" ${data.settings?.currency === 'KWD' ? 'selected' : ''}>🇰🇼 دينار كويتي (د.ك)</option>
                                <option value="BHD" ${data.settings?.currency === 'BHD' ? 'selected' : ''}>🇧🇭 دينار بحريني (د.ب)</option>
                                <option value="OMR" ${data.settings?.currency === 'OMR' ? 'selected' : ''}>🇴🇲 ريال عماني (ر.ع)</option>
                                <option value="QAR" ${data.settings?.currency === 'QAR' ? 'selected' : ''}>🇶🇦 ريال قطري (ر.ق)</option>
                                <option value="EGP" ${data.settings?.currency === 'EGP' ? 'selected' : ''}>🇪🇬 جنيه مصري (ج.م)</option>
                                <option value="JOD" ${data.settings?.currency === 'JOD' ? 'selected' : ''}>🇯🇴 دينار أردني (د.أ)</option>
                                <option value="LBP" ${data.settings?.currency === 'LBP' ? 'selected' : ''}>🇱🇧 ليرة لبنانية (ل.ل)</option>
                                <option value="SDG" ${data.settings?.currency === 'SDG' ? 'selected' : ''}>🇸🇩 جنيه سوداني (ج.س)</option>
                                <option value="TRY" ${data.settings?.currency === 'TRY' ? 'selected' : ''}>🇹🇷 ليرة تركية (₺)</option>
                                <option value="GBP" ${data.settings?.currency === 'GBP' ? 'selected' : ''}>🇬🇧 جنيه استرليني (£)</option>
                            </select>
                        </div>
                        
                        <button class="btn btn-primary" onclick="saveSettings()">حفظ الإعدادات ✓</button>
                    </div>
                    
                    <div class="settings-card">
                        <h3>💾 النسخ الاحتياطي</h3>
                        <button class="btn btn-blue" onclick="exportData()">📤 تصدير البيانات</button>
                        <button class="btn btn-secondary" onclick="document.getElementById('importFile').click()">📥 استيراد البيانات</button>
                        <input type="file" id="importFile" accept=".json" style="display:none" onchange="importData(event)">
                    </div>
                    
                    <div class="settings-card">
                        <div class="app-info">
                            <div class="icon">📱</div>
                            <h3>بلال المحاسبي البسيط</h3>
                            <p>الإصدار 1.0.0</p>
                            <p style="margin-top:10px;font-size:12px">تطبيق لإدارة حسابات العملاء والديون</p>
                        </div>
                        
                        <div class="contact-card">
                            <h4>📞 تواصل مع المطور</h4>
                            <div class="contact-links">
                                <a href="https://instagram.com/alsyfyblal7" target="_blank" class="contact-link">
                                    <div class="contact-link-info">
                                        <div class="contact-link-icon instagram">📸</div>
                                        <div>
                                            <span>انستقرام</span><br>
                                            <small>@alsyfyblal7</small>
                                        </div>
                                    </div>
                                    <span>←</span>
                                </a>
                                <a href="https://t.me/belal77878" target="_blank" class="contact-link">
                                    <div class="contact-link-info">
                                        <div class="contact-link-icon telegram">✈️</div>
                                        <div>
                                            <span>تيلجرام</span><br>
                                            <small>@belal77878</small>
                                        </div>
                                    </div>
                                    <span>←</span>
                                </a>
                                <a href="mailto:alsyfyblal7@gmail.com" class="contact-link">
                                    <div class="contact-link-info">
                                        <div class="contact-link-icon email">✉️</div>
                                        <div>
                                            <span>البريد الإلكتروني</span><br>
                                            <small>alsyfyblal7@gmail.com</small>
                                        </div>
                                    </div>
                                    <span>←</span>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }

        // ===== Actions =====
        function showAddCustomerModal() {
            document.getElementById('addCustomerModal').classList.add('active');
            setTimeout(() => document.getElementById('newName').focus(), 300);
        }

        function hideModal(id) {
            document.getElementById(id).classList.remove('active');
        }

        async function pickContactForAdd() {
            const contact = await pickContact();
            if (contact) {
                if (contact.name) document.getElementById('newName').value = contact.name;
                if (contact.phone) document.getElementById('newPhone').value = contact.phone;
            } else {
                alert('الوصول لجهات الاتصال غير متاح في هذا المتصفح.\\nيمكنك إدخال البيانات يدوياً.');
            }
        }

        async function pickContactForEdit() {
            const contact = await pickContact();
            if (contact) {
                if (contact.name) document.getElementById('editName').value = contact.name;
                if (contact.phone) document.getElementById('editPhone').value = contact.phone;
            }
        }

        async function pickContactForWhatsApp() {
            const contact = await pickContact();
            if (contact && contact.phone) {
                document.getElementById('waPhone').value = contact.phone;
            }
        }

        async function pickContactForStatement() {
            const contact = await pickContact();
            if (contact && contact.phone) {
                document.getElementById('stmtPhone').value = contact.phone;
            }
        }

        function addCustomer() {
            const name = document.getElementById('newName').value.trim();
            const phone = document.getElementById('newPhone').value.trim();
            const limit = parseFloat(document.getElementById('newLimit').value) || 0;
            
            if (!name) {
                alert('الرجاء إدخال اسم العميل');
                return;
            }
            
            const customer = {
                id: generateId(),
                name: name,
                phone: phone,
                creditLimit: limit,
                transactions: [],
                createdAt: new Date().toISOString()
            };
            
            data.customers.push(customer);
            saveData();
            hideModal('addCustomerModal');
            
            selectedCustomerIndex = data.customers.length - 1;
            selectedCustomer = customer;
            currentView = 'detail';
            render();
        }

        function openCustomer(index) {
            selectedCustomerIndex = index;
            selectedCustomer = data.customers[index];
            currentView = 'detail';
            render();
        }

        function goBack() {
            currentView = 'list';
            selectedCustomer = null;
            selectedCustomerIndex = -1;
            render();
        }

        function goToSettings() {
            currentView = 'settings';
            render();
        }

        function toggleMenu() {
            document.getElementById('customerMenu').classList.toggle('active');
        }

        function showEditModal() {
            document.getElementById('customerMenu').classList.remove('active');
            document.getElementById('editName').value = selectedCustomer.name;
            document.getElementById('editPhone').value = selectedCustomer.phone || '';
            document.getElementById('editLimit').value = selectedCustomer.creditLimit || 0;
            document.getElementById('editModal').classList.add('active');
        }

        function saveCustomerEdit() {
            const name = document.getElementById('editName').value.trim();
            const phone = document.getElementById('editPhone').value.trim();
            const limit = parseFloat(document.getElementById('editLimit').value) || 0;
            
            if (!name) {
                alert('الرجاء إدخال اسم العميل');
                return;
            }
            
            data.customers[selectedCustomerIndex].name = name;
            data.customers[selectedCustomerIndex].phone = phone;
            data.customers[selectedCustomerIndex].creditLimit = limit;
            selectedCustomer = data.customers[selectedCustomerIndex];
            
            saveData();
            hideModal('editModal');
            render();
        }

        function confirmDeleteCustomer() {
            document.getElementById('customerMenu').classList.remove('active');
            document.getElementById('confirmIcon').textContent = '🗑️';
            document.getElementById('confirmTitle').textContent = 'حذف العميل';
            document.getElementById('confirmMessage').innerHTML = `هل أنت متأكد من حذف <strong>${selectedCustomer.name}</strong>؟<br><span style="color:#dc2626;font-size:12px">سيتم حذف جميع المعاملات</span>`;
            document.getElementById('confirmYesBtn').onclick = deleteCustomer;
            document.getElementById('confirmDialog').classList.add('active');
        }

        function deleteCustomer() {
            data.customers.splice(selectedCustomerIndex, 1);
            saveData();
            hideModal('confirmDialog');
            goBack();
        }

        function showTxModal(type) {
            const isDebt = type === 'debt';
            document.getElementById('txType').value = type;
            document.getElementById('txModalTitle').textContent = isDebt ? '📝 تسجيل دين جديد' : '💰 تسجيل سداد';
            document.getElementById('txDesc').value = '';
            document.getElementById('txDesc').placeholder = isDebt ? 'مثال: مشتريات بقالة' : 'مثال: سداد جزئي';
            document.getElementById('txAmount').value = '';
            document.getElementById('txSubmitBtn').className = isDebt ? 'btn btn-danger' : 'btn btn-success';
            document.getElementById('txModal').classList.add('active');
            setTimeout(() => document.getElementById('txAmount').focus(), 300);
        }

        function addTransaction() {
            const amount = parseFloat(document.getElementById('txAmount').value);
            const desc = document.getElementById('txDesc').value.trim();
            const type = document.getElementById('txType').value;
            
            if (!amount || amount <= 0) {
                alert('الرجاء إدخال مبلغ صحيح');
                return;
            }
            
            const tx = {
                id: generateId(),
                type: type,
                amount: amount,
                description: desc || (type === 'debt' ? 'مشتريات' : 'سداد'),
                date: new Date().toISOString()
            };
            
            data.customers[selectedCustomerIndex].transactions.push(tx);
            selectedCustomer = data.customers[selectedCustomerIndex];
            
            saveData();
            hideModal('txModal');
            render();
            
            if (type === 'debt' && isOverLimit(selectedCustomer)) {
                setTimeout(() => {
                    document.getElementById('limitAlertModal').classList.add('active');
                }, 300);
            }
        }

        function confirmDeleteTx(txId) {
            document.getElementById('confirmIcon').textContent = '⚠️';
            document.getElementById('confirmTitle').textContent = 'حذف المعاملة';
            document.getElementById('confirmMessage').textContent = 'هل أنت متأكد من حذف هذه المعاملة؟';
            document.getElementById('confirmYesBtn').onclick = () => deleteTx(txId);
            document.getElementById('confirmDialog').classList.add('active');
        }

        function deleteTx(txId) {
            const txIndex = data.customers[selectedCustomerIndex].transactions.findIndex(t => t.id === txId);
            if (txIndex !== -1) {
                data.customers[selectedCustomerIndex].transactions.splice(txIndex, 1);
                selectedCustomer = data.customers[selectedCustomerIndex];
                saveData();
            }
            hideModal('confirmDialog');
            render();
        }

        function filterCustomers() {
            const query = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.customer-card');
            const clearBtn = document.getElementById('searchClear');
            
            clearBtn.style.display = query ? 'inline' : 'none';
            
            cards.forEach((card, i) => {
                const c = data.customers[i];
                const match = c.name.toLowerCase().includes(query) || (c.phone || '').includes(query);
                card.style.display = match ? 'flex' : 'none';
            });
        }

        function clearSearch() {
            document.getElementById('searchInput').value = '';
            filterCustomers();
        }

        function showWhatsAppModal() {
            document.getElementById('whatsappModal').classList.add('active');
        }

        function sendWhatsApp() {
            const phone = document.getElementById('waPhone').value.trim();
            if (!phone) {
                alert('الرجاء إدخال رقم الجوال');
                return;
            }
            
            const balance = getBalance(selectedCustomer);
            const storeName = getStoreName();
            let formattedPhone = phone.replace(/[\\s\\-]/g, '');
            if (formattedPhone.startsWith('05')) formattedPhone = '966' + formattedPhone.substr(1);
            if (formattedPhone.startsWith('+')) formattedPhone = formattedPhone.substr(1);
            
            const msg = `السلام عليكم ورحمة الله وبركاته 🙏

أخي الكريم *${selectedCustomer.name}*

نود تذكيرك بأن لديك مبلغ مستحق لدى *${storeName}*

💰 المبلغ المستحق: *${fmtMoney(balance)}*

نرجو التكرم بالسداد في أقرب وقت ممكن.

شاكرين لكم تعاملكم معنا 🌹
${storeName}`;
            
            window.open('https://wa.me/' + formattedPhone + '?text=' + encodeURIComponent(msg));
            hideModal('whatsappModal');
        }

        function sendSMS() {
            const phone = selectedCustomer.phone;
            if (!phone) {
                alert('لا يوجد رقم جوال للعميل');
                return;
            }
            
            const balance = getBalance(selectedCustomer);
            const storeName = getStoreName();
            let formattedPhone = phone.replace(/[\\s\\-]/g, '');
            if (formattedPhone.startsWith('05')) formattedPhone = '+966' + formattedPhone.substr(1);
            
            const msg = `السلام عليكم
${selectedCustomer.name}، لديك مبلغ مستحق لدى ${storeName} بقيمة ${fmtMoney(balance)}.
نرجو السداد في أقرب وقت.
شكراً لتعاملكم معنا.`;
            
            window.open('sms:' + formattedPhone + '?body=' + encodeURIComponent(msg));
        }

        function showStatementModal() {
            document.getElementById('statementModal').classList.add('active');
        }

        function sendStatementWhatsApp() {
            const phone = document.getElementById('stmtPhone').value.trim();
            if (!phone) {
                alert('الرجاء إدخال رقم الجوال');
                return;
            }
            
            const balance = getBalance(selectedCustomer);
            const storeName = getStoreName();
            const transactions = [...(selectedCustomer.transactions || [])].sort((a, b) => new Date(b.date) - new Date(a.date));
            
            let formattedPhone = phone.replace(/[\\s\\-]/g, '');
            if (formattedPhone.startsWith('05')) formattedPhone = '966' + formattedPhone.substr(1);
            if (formattedPhone.startsWith('+')) formattedPhone = formattedPhone.substr(1);
            
            let txList = '';
            transactions.slice(0, 10).forEach((tx, i) => {
                const isDebt = tx.type === 'debt';
                txList += `${i + 1}. ${isDebt ? '📝' : '💰'} ${isDebt ? '+' : '-'}${fmtMoney(tx.amount)} - ${tx.description}\\n`;
            });
            if (transactions.length > 10) {
                txList += `\\n... و ${transactions.length - 10} معاملات أخرى`;
            }
            
            const msg = `📋 *كشف حساب - ${storeName}*

👤 العميل: *${selectedCustomer.name}*
📅 التاريخ: ${formatDate(new Date().toISOString())}

━━━━━━━━━━━━━━━━
💰 *${balance > 0 ? 'المبلغ المستحق' : 'الرصيد'}:*
*${fmtMoney(balance)}*
${selectedCustomer.creditLimit > 0 ? `📊 سقف المديونية: ${fmtMoney(selectedCustomer.creditLimit)}` : ''}
━━━━━━━━━━━━━━━━

📜 *آخر المعاملات:*
${txList || 'لا توجد معاملات'}

━━━━━━━━━━━━━━━━
شكراً لتعاملكم معنا 🙏
*${storeName}*`;
            
            window.open('https://wa.me/' + formattedPhone + '?text=' + encodeURIComponent(msg));
            hideModal('statementModal');
        }

        function sendLimitAlert() {
            const phone = selectedCustomer.phone;
            if (!phone) {
                alert('لا يوجد رقم جوال للعميل');
                hideModal('limitAlertModal');
                return;
            }
            
            const balance = getBalance(selectedCustomer);
            const limit = selectedCustomer.creditLimit;
            const storeName = getStoreName();
            
            let formattedPhone = phone.replace(/[\\s\\-]/g, '');
            if (formattedPhone.startsWith('05')) formattedPhone = '966' + formattedPhone.substr(1);
            if (formattedPhone.startsWith('+')) formattedPhone = formattedPhone.substr(1);
            
            const msg = `السلام عليكم ورحمة الله وبركاته 🙏

أخي الكريم *${selectedCustomer.name}*

نود إعلامك بأن حسابك لدى *${storeName}* قد وصل إلى الحد الأقصى للمديونية.

💰 المبلغ المستحق: *${fmtMoney(balance)}*
📊 سقف المديونية: *${fmtMoney(limit)}*

نرجو التكرم بسداد جزء من المبلغ لتتمكن من متابعة التعامل.

شاكرين لكم تفهمكم 🌹
${storeName}`;
            
            window.open('https://wa.me/' + formattedPhone + '?text=' + encodeURIComponent(msg));
            hideModal('limitAlertModal');
        }

        function uploadLogo(event) {
            const file = event.target.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = function(e) {
                data.settings = data.settings || {};
                data.settings.logo = e.target.result;
                saveData();
                render();
            };
            reader.readAsDataURL(file);
        }

        function removeLogo() {
            data.settings = data.settings || {};
            data.settings.logo = null;
            saveData();
            render();
        }

        function saveSettings() {
            const name = document.getElementById('storeName').value.trim();
            const currency = document.getElementById('currencySelect').value;
            data.settings = data.settings || {};
            data.settings.name = name || 'البقالة';
            data.settings.currency = currency;
            saveData();
            alert('✓ تم حفظ الإعدادات');
            render();
        }

        function exportData() {
            const json = JSON.stringify(data, null, 2);
            const blob = new Blob([json], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'bilal_backup_' + new Date().toISOString().split('T')[0] + '.json';
            a.click();
            URL.revokeObjectURL(url);
        }

        function importData(event) {
            const file = event.target.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const imported = JSON.parse(e.target.result);
                    if (imported.customers) {
                        data = imported;
                        saveData();
                        alert('✓ تم استيراد البيانات بنجاح');
                        render();
                    } else {
                        alert('ملف غير صالح');
                    }
                } catch (err) {
                    alert('خطأ في قراءة الملف');
                }
            };
            reader.readAsText(file);
        }

        // Close dropdowns when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.menu-btn') && !e.target.closest('.dropdown-menu')) {
                const menu = document.getElementById('customerMenu');
                if (menu) menu.classList.remove('active');
            }
        });

        // Initial render
        render();
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
            
            data = load_data()
            html = HTML_TEMPLATE.replace('%%DATA%%', json.dumps(data, ensure_ascii=False))
            self.wfile.write(html.encode('utf-8'))
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/save':
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

def main():
    port = 8000
    server = HTTPServer(('0.0.0.0', port), RequestHandler)
    
    print()
    print("=" * 50)
    print("   📱 بلال المحاسبي البسيط - النسخة الكاملة")
    print("=" * 50)
    print()
    print("   ✅ التطبيق يعمل الآن!")
    print()
    print("   📱 افتح المتصفح على هذا الرابط:")
    print()
    print(f"      👉 http://localhost:{port}")
    print()
    
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        print(f"   📶 أو من جهاز آخر على نفس الشبكة:")
        print(f"      👉 http://{ip}:{port}")
        print()
    except:
        pass
    
    print("   ⏹️  للإيقاف اضغط: Ctrl + C")
    print()
    print("=" * 50)
    print()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n   👋 تم إيقاف التطبيق\n")
        server.shutdown()

if __name__ == "__main__":
    main()
