#!/usr/bin/env python3
"""
Generate CRUD-enabled HTML viewer for retail tariff data
Creates an interactive data viewer with full Create, Read, Update, Delete capabilities
"""

import os
import json
from pathlib import Path

def create_crud_html_viewer():
    """Create HTML viewer with CRUD capabilities"""
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Retail Tariff Data - CRUD Viewer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }

        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .controls {
            padding: 20px 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }

        .table-selector {
            display: flex;
            gap: 10px;
            align-items: center;
        }

        .table-selector select {
            padding: 10px 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            background: white;
            cursor: pointer;
            transition: border-color 0.3s;
        }

        .table-selector select:focus {
            outline: none;
            border-color: #667eea;
        }

        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .btn-primary {
            background: #667eea;
            color: white;
        }

        .btn-primary:hover {
            background: #5a6fd8;
            transform: translateY(-2px);
        }

        .btn-success {
            background: #28a745;
            color: white;
        }

        .btn-success:hover {
            background: #218838;
            transform: translateY(-2px);
        }

        .btn-danger {
            background: #dc3545;
            color: white;
        }

        .btn-danger:hover {
            background: #c82333;
            transform: translateY(-2px);
        }

        .btn-secondary {
            background: #6c757d;
            color: white;
        }

        .btn-secondary:hover {
            background: #5a6268;
            transform: translateY(-2px);
        }

        .btn-warning {
            background: #ffc107;
            color: #212529;
        }

        .btn-warning:hover {
            background: #e0a800;
            transform: translateY(-2px);
        }

        .status-bar {
            padding: 15px 30px;
            background: #e3f2fd;
            border-bottom: 1px solid #bbdefb;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }

        .status-info {
            display: flex;
            gap: 20px;
            align-items: center;
        }

        .status-item {
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 14px;
            color: #1976d2;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 40px;
            color: #666;
        }

        .loading.show {
            display: block;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .table-container {
            padding: 30px;
            overflow-x: auto;
        }

        .data-table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .data-table th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 12px;
            text-align: left;
            font-weight: 600;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .data-table td {
            padding: 12px;
            border-bottom: 1px solid #e9ecef;
            font-size: 14px;
            vertical-align: middle;
        }

        .data-table tr:hover {
            background: #f8f9fa;
        }

        .data-table tr.editing {
            background: #fff3cd;
        }

        .editable {
            border: 1px solid #ddd;
            padding: 8px;
            border-radius: 4px;
            width: 100%;
            font-size: 14px;
            transition: border-color 0.3s;
        }

        .editable:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
        }

        .editable.invalid {
            border-color: #dc3545;
            background: #fff5f5;
        }

        .action-buttons {
            display: flex;
            gap: 5px;
            justify-content: center;
        }

        .action-buttons .btn {
            padding: 6px 12px;
            font-size: 12px;
        }

        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
            backdrop-filter: blur(5px);
        }

        .modal.show {
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            max-width: 500px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
        }

        .modal-header {
            margin-bottom: 20px;
            text-align: center;
        }

        .modal-header h2 {
            color: #2c3e50;
            margin-bottom: 10px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #2c3e50;
        }

        .form-group input, .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }

        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #667eea;
        }

        .form-group .error {
            color: #dc3545;
            font-size: 12px;
            margin-top: 5px;
        }

        .modal-footer {
            display: flex;
            gap: 10px;
            justify-content: flex-end;
            margin-top: 30px;
        }

        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }

        .alert.show {
            display: block;
        }

        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .alert-info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }

        .filters {
            display: flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
        }

        .filter-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .filter-group label {
            font-size: 12px;
            color: #666;
            font-weight: 600;
        }

        .filter-group select {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 12px;
            background: white;
        }

        .pagination-controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 0;
            border-top: 1px solid #e9ecef;
            margin-top: 20px;
        }

        .pagination-info {
            font-size: 14px;
            color: #666;
            font-weight: 600;
        }

        .pagination-buttons {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .page-numbers {
            display: flex;
            gap: 5px;
        }

        .page-number {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
        }

        .page-number:hover {
            background: #f8f9fa;
            border-color: #667eea;
        }

        .page-number.active {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }

        .page-number:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        @media (max-width: 768px) {
            .controls {
                flex-direction: column;
                align-items: stretch;
            }
            
            .table-selector, .filters {
                justify-content: center;
            }
            
            .status-bar {
                flex-direction: column;
                text-align: center;
            }
            
            .action-buttons {
                flex-direction: column;
            }
            
            .pagination-controls {
                flex-direction: column;
                gap: 15px;
                text-align: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏪 Retail Tariff Data</h1>
            <p>Interactive CRUD Data Viewer with Real-time Updates</p>
        </div>

        <div class="controls">
            <div class="table-selector">
                <label for="tableSelect">📊 Table:</label>
                <select id="tableSelect">
                    <option value="">Select a table...</option>
                </select>
                <button class="btn btn-primary" onclick="loadTableData()">
                    🔄 Refresh
                </button>
            </div>

            <div class="filters" id="filters">
                <!-- Dynamic filters will be added here -->
            </div>

            <div>
                <button class="btn btn-success" onclick="showAddModal()">
                    ➕ Add Row
                </button>
                <button class="btn btn-secondary" onclick="clearFilters()">
                    🧹 Clear Filters
                </button>
                <button class="btn btn-warning" onclick="exportData()">
                    📥 Export CSV
                </button>
            </div>
        </div>

        <div class="status-bar">
            <div class="status-info">
                <div class="status-item">
                    <span>📋 Table:</span>
                    <span id="currentTable">None</span>
                </div>
                <div class="status-item">
                    <span>📊 Records:</span>
                    <span id="recordCount">0</span>
                </div>
                <div class="status-item">
                    <span>👁️ Visible:</span>
                    <span id="visibleCount">0</span>
                </div>
            </div>
            <div class="status-item">
                <span>🔄 Last Updated:</span>
                <span id="lastUpdated">Never</span>
            </div>
        </div>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Loading data...</p>
        </div>

        <div class="table-container" id="tableContainer">
            <div class="alert alert-info" id="infoAlert">
                Select a table from the dropdown above to view and edit data.
            </div>
            
            <!-- Pagination Controls -->
            <div class="pagination-controls" id="paginationControls" style="display: none;">
                <div class="pagination-info">
                    <span id="paginationInfo">Page 1 of 1</span>
                </div>
                <div class="pagination-buttons">
                    <button class="btn btn-secondary" id="prevPage" onclick="loadTableData(currentPage - 1)" disabled>
                        ← Previous
                    </button>
                    <span class="page-numbers" id="pageNumbers"></span>
                    <button class="btn btn-secondary" id="nextPage" onclick="loadTableData(currentPage + 1)" disabled>
                        Next →
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Add/Edit Modal -->
    <div class="modal" id="addModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modalTitle">Add New Row</h2>
            </div>
            
            <div class="alert" id="modalAlert"></div>
            
            <form id="addForm">
                <div id="formFields">
                    <!-- Dynamic form fields will be added here -->
                </div>
                
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" onclick="hideAddModal()">
                        Cancel
                    </button>
                    <button type="submit" class="btn btn-primary" id="submitBtn">
                        Save
                    </button>
                </div>
            </form>
        </div>
    </div>

    <script>
        // Global variables
        let currentTable = '';
        let tableData = [];
        let filteredData = [];
        let validationRules = {};
        let editingRowId = null;
        let currentPage = 1;
        let perPage = 50;
        let totalPages = 1;
        let totalCount = 0;

        // API Base URL
        const API_BASE = 'http://localhost:5001/api';

        // Initialize the application
        document.addEventListener('DOMContentLoaded', function() {
            loadTables();
            setupEventListeners();
        });

        function setupEventListeners() {
            document.getElementById('tableSelect').addEventListener('change', function() {
                if (this.value) {
                    loadTableData();
                }
            });

            document.getElementById('addForm').addEventListener('submit', function(e) {
                e.preventDefault();
                saveRow();
            });
        }

        async function loadTables() {
            try {
                const response = await fetch(`${API_BASE}/tables`);
                const tables = await response.json();
                
                const select = document.getElementById('tableSelect');
                select.innerHTML = '<option value="">Select a table...</option>';
                
                tables.forEach(table => {
                    const option = document.createElement('option');
                    option.value = table.name;
                    option.textContent = table.name.charAt(0).toUpperCase() + table.name.slice(1).replace('_', ' ');
                    select.appendChild(option);
                });
            } catch (error) {
                showAlert('error', 'Failed to load tables: ' + error.message);
            }
        }

        async function loadTableData(page = 1) {
            const tableSelect = document.getElementById('tableSelect');
            currentTable = tableSelect.value;
            
            if (!currentTable) {
                showAlert('info', 'Please select a table first.');
                return;
            }

            showLoading(true);
            currentPage = page;
            
            try {
                // Load paginated data and validation rules in parallel
                const [dataResponse, rulesResponse] = await Promise.all([
                    fetch(`${API_BASE}/tables/${currentTable}?page=${page}&per_page=${perPage}`),
                    fetch(`${API_BASE}/validation-rules/${currentTable}`)
                ]);

                const dataResult = await dataResponse.json();
                const rulesResult = await rulesResponse.json();

                if (dataResult.error) {
                    throw new Error(dataResult.error);
                }

                tableData = dataResult.data;
                filteredData = [...tableData];
                validationRules = rulesResult.rules;
                totalCount = dataResult.count;
                totalPages = dataResult.total_pages;

                updateStatusBar();
                renderTable();
                createPagination();
                
                if (page === 1) {
                    createFilters();
                    showAlert('success', `Loaded ${totalCount} records from ${currentTable} (showing page ${page})`);
                }
                
            } catch (error) {
                showAlert('error', 'Failed to load data: ' + error.message);
                console.error('Error loading data:', error);
            } finally {
                showLoading(false);
            }
        }

        function renderTable() {
            const container = document.getElementById('tableContainer');
            
            if (filteredData.length === 0) {
                container.innerHTML = '<div class="alert alert-info">No data to display.</div>';
                return;
            }

            const headers = Object.keys(filteredData[0]);
            
            let html = `
                <table class="data-table">
                    <thead>
                        <tr>
                            ${headers.map(header => `<th>${header.replace(/_/g, ' ').toUpperCase()}</th>`).join('')}
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            filteredData.forEach((row, index) => {
                // Calculate global row ID for pagination
                const globalRowId = (currentPage - 1) * perPage + index;
                html += `
                    <tr data-row-id="${globalRowId}">
                        ${headers.map(header => `
                            <td>
                                <span class="cell-content" data-field="${header}">${row[header] || ''}</span>
                            </td>
                        `).join('')}
                        <td>
                            <div class="action-buttons">
                                <button class="btn btn-primary" onclick="editRow(${globalRowId})" title="Edit">
                                    ✏️
                                </button>
                                <button class="btn btn-danger" onclick="deleteRow(${globalRowId})" title="Delete">
                                    🗑️
                                </button>
                            </div>
                        </td>
                    </tr>
                `;
            });

            html += '</tbody></table>';
            container.innerHTML = html;
        }

        function createFilters() {
            const filtersContainer = document.getElementById('filters');
            filtersContainer.innerHTML = '';

            if (tableData.length === 0) return;

            const headers = Object.keys(tableData[0]);
            
            headers.forEach(header => {
                const uniqueValues = [...new Set(tableData.map(row => row[header]))].slice(0, 20);
                
                if (uniqueValues.length > 1 && uniqueValues.length <= 20) {
                    const filterGroup = document.createElement('div');
                    filterGroup.className = 'filter-group';
                    
                    filterGroup.innerHTML = `
                        <label>${header.replace(/_/g, ' ')}</label>
                        <select onchange="applyFilters()" data-field="${header}">
                            <option value="">All</option>
                            ${uniqueValues.map(value => `
                                <option value="${value}">${value}</option>
                            `).join('')}
                        </select>
                    `;
                    
                    filtersContainer.appendChild(filterGroup);
                }
            });
        }

        function applyFilters() {
            const filterSelects = document.querySelectorAll('#filters select');
            filteredData = [...tableData];

            filterSelects.forEach(select => {
                const field = select.dataset.field;
                const value = select.value;
                
                if (value) {
                    filteredData = filteredData.filter(row => row[field] == value);
                }
            });

            updateStatusBar();
            renderTable();
        }

        function clearFilters() {
            const filterSelects = document.querySelectorAll('#filters select');
            filterSelects.forEach(select => {
                select.value = '';
            });
            
            filteredData = [...tableData];
            updateStatusBar();
            renderTable();
        }

        function updateStatusBar() {
            document.getElementById('currentTable').textContent = currentTable || 'None';
            document.getElementById('recordCount').textContent = totalCount;
            document.getElementById('visibleCount').textContent = filteredData.length;
            document.getElementById('lastUpdated').textContent = new Date().toLocaleTimeString();
        }

        function createPagination() {
            const controls = document.getElementById('paginationControls');
            const info = document.getElementById('paginationInfo');
            const prevBtn = document.getElementById('prevPage');
            const nextBtn = document.getElementById('nextPage');
            const pageNumbers = document.getElementById('pageNumbers');

            if (totalPages <= 1) {
                controls.style.display = 'none';
                return;
            }

            controls.style.display = 'flex';
            info.textContent = `Page ${currentPage} of ${totalPages} (${totalCount} total records)`;
            
            // Update prev/next buttons
            prevBtn.disabled = currentPage <= 1;
            nextBtn.disabled = currentPage >= totalPages;

            // Create page number buttons
            pageNumbers.innerHTML = '';
            const maxVisiblePages = 5;
            let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
            let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

            if (endPage - startPage + 1 < maxVisiblePages) {
                startPage = Math.max(1, endPage - maxVisiblePages + 1);
            }

            for (let i = startPage; i <= endPage; i++) {
                const pageBtn = document.createElement('button');
                pageBtn.className = `page-number ${i === currentPage ? 'active' : ''}`;
                pageBtn.textContent = i;
                pageBtn.onclick = () => loadTableData(i);
                pageNumbers.appendChild(pageBtn);
            }
        }

        function showAddModal() {
            if (!currentTable) {
                showAlert('error', 'Please select a table first.');
                return;
            }

            editingRowId = null;
            document.getElementById('modalTitle').textContent = 'Add New Row';
            document.getElementById('submitBtn').textContent = 'Save';
            
            createFormFields();
            document.getElementById('addModal').classList.add('show');
        }

        function editRow(rowId) {
            if (!currentTable) return;

            editingRowId = rowId;
            const rowData = tableData[rowId];
            
            document.getElementById('modalTitle').textContent = 'Edit Row';
            document.getElementById('submitBtn').textContent = 'Update';
            
            createFormFields(rowData);
            document.getElementById('addModal').classList.add('show');
        }

        function createFormFields(data = {}) {
            const container = document.getElementById('formFields');
            container.innerHTML = '';

            Object.keys(validationRules).forEach(field => {
                const rule = validationRules[field];
                const value = data[field] || '';
                
                const formGroup = document.createElement('div');
                formGroup.className = 'form-group';
                
                let inputHtml = '';
                if (rule.type === 'string' && rule.choices) {
                    // Dropdown for choices
                    inputHtml = `
                        <select name="${field}" required="${rule.required}">
                            <option value="">Select...</option>
                            ${rule.choices.map(choice => `
                                <option value="${choice}" ${value === choice ? 'selected' : ''}>${choice}</option>
                            `).join('')}
                        </select>
                    `;
                } else {
                    // Text input
                    const inputType = rule.type === 'email' ? 'email' : 
                                    rule.type === 'integer' ? 'number' : 
                                    rule.type === 'float' ? 'number' : 'text';
                    
                    inputHtml = `
                        <input type="${inputType}" 
                               name="${field}" 
                               value="${value}"
                               ${rule.required ? 'required' : ''}
                               ${rule.min !== undefined ? `min="${rule.min}"` : ''}
                               ${rule.max !== undefined ? `max="${rule.max}"` : ''}
                               ${rule.max_length ? `maxlength="${rule.max_length}"` : ''}
                               step="${rule.type === 'float' ? '0.01' : '1'}">
                    `;
                }
                
                formGroup.innerHTML = `
                    <label for="${field}">
                        ${field.replace(/_/g, ' ').toUpperCase()}
                        ${rule.required ? ' *' : ''}
                    </label>
                    ${inputHtml}
                    <div class="error" id="error-${field}"></div>
                `;
                
                container.appendChild(formGroup);
            });
        }

        async function saveRow() {
            const form = document.getElementById('addForm');
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            // Clear previous errors
            document.querySelectorAll('.error').forEach(el => el.textContent = '');

            try {
                let response;
                if (editingRowId !== null) {
                    // Update existing row
                    response = await fetch(`${API_BASE}/tables/${currentTable}/${editingRowId}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data)
                    });
                } else {
                    // Create new row
                    response = await fetch(`${API_BASE}/tables/${currentTable}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data)
                    });
                }

                const result = await response.json();

                if (response.ok) {
                    hideAddModal();
                    loadTableData(); // Reload data
                    showAlert('success', result.message);
                } else {
                    if (result.details) {
                        // Show validation errors
                        result.details.forEach(error => {
                            const field = error.split(' ')[0];
                            const errorEl = document.getElementById(`error-${field}`);
                            if (errorEl) {
                                errorEl.textContent = error;
                            }
                        });
                    } else {
                        showModalAlert('error', result.error);
                    }
                }
            } catch (error) {
                showModalAlert('error', 'Failed to save: ' + error.message);
            }
        }

        async function deleteRow(rowId) {
            if (!confirm('Are you sure you want to delete this row?')) {
                return;
            }

            try {
                const response = await fetch(`${API_BASE}/tables/${currentTable}/${rowId}`, {
                    method: 'DELETE'
                });

                const result = await response.json();

                if (response.ok) {
                    loadTableData(); // Reload data
                    showAlert('success', result.message);
                } else {
                    showAlert('error', result.error);
                }
            } catch (error) {
                showAlert('error', 'Failed to delete: ' + error.message);
            }
        }

        function hideAddModal() {
            document.getElementById('addModal').classList.remove('show');
        }

        function showLoading(show) {
            document.getElementById('loading').classList.toggle('show', show);
        }

        function showAlert(type, message) {
            const alert = document.getElementById('infoAlert');
            alert.className = `alert alert-${type} show`;
            alert.textContent = message;
            
            setTimeout(() => {
                alert.classList.remove('show');
            }, 5000);
        }

        function showModalAlert(type, message) {
            const alert = document.getElementById('modalAlert');
            alert.className = `alert alert-${type} show`;
            alert.textContent = message;
        }

        function exportData() {
            if (filteredData.length === 0) {
                showAlert('error', 'No data to export.');
                return;
            }

            const headers = Object.keys(filteredData[0]);
            const csvContent = [
                headers.join(','),
                ...filteredData.map(row => 
                    headers.map(header => `"${(row[header] || '').toString().replace(/"/g, '""')}"`).join(',')
                )
            ].join('\\n');

            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${currentTable}_export.csv`;
            a.click();
            window.URL.revokeObjectURL(url);

            showAlert('success', `Exported ${filteredData.length} records to CSV.`);
        }

        // Close modal when clicking outside
        document.getElementById('addModal').addEventListener('click', function(e) {
            if (e.target === this) {
                hideAddModal();
            }
        });
    </script>
</body>
</html>"""

    return html_content

def main():
    """Generate the CRUD HTML viewer"""
    print("🚀 Generating CRUD-enabled HTML viewer...")
    
    html_content = create_crud_html_viewer()
    
    # Write to file
    output_file = "../data_viewer_crud.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ CRUD HTML viewer generated: {output_file}")
    print("📋 Features included:")
    print("   • Full CRUD operations (Create, Read, Update, Delete)")
    print("   • Inline editing with validation")
    print("   • Real-time CSV updates")
    print("   • Data filtering and export")
    print("   • Responsive design")
    print("🌐 To use:")
    print("   1. Start CRUD server: python3 crud_server.py")
    print("   2. Open: http://localhost:5001")

if __name__ == "__main__":
    main()
