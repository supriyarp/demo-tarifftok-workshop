#!/usr/bin/env python3
"""
Generate dynamic HTML viewer that loads CSV data at runtime
"""
import pandas as pd
import os
from pathlib import Path

def generate_dynamic_html_viewer():
    """Generate HTML viewer that dynamically loads CSV data"""
    
    # Data files to process
    data_files = [
        {'id': 'tariffs', 'name': 'Tariffs', 'file': 'tariffs.csv', 'icon': '📈'},
        {'id': 'products', 'name': 'Products', 'file': 'products.csv', 'icon': '🛍️'},
        {'id': 'suppliers', 'name': 'Suppliers', 'file': 'suppliers.csv', 'icon': '🏭'},
        {'id': 'markets', 'name': 'Markets', 'file': 'markets.csv', 'icon': '🌍'},
        {'id': 'cost-transit', 'name': 'Cost & Transit', 'file': 'cost_transit.csv', 'icon': '🚚'},
        {'id': 'sales-daily', 'name': 'Sales Daily', 'file': 'sales_daily.csv', 'icon': '📅'},
        {'id': 'sales-weekly', 'name': 'Sales Weekly', 'file': 'sales_weekly.csv', 'icon': '📊'}
    ]
    
    # Generate complete HTML
    html_content = generate_dynamic_html_template(data_files)
    
    # Save HTML file
    output_file = "../data_viewer_dynamic.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"🎉 Dynamic HTML viewer generated: {output_file}")
    print(f"📊 Data files: {len(data_files)}")
    print("💡 This version loads CSV data dynamically at runtime")
    
    return output_file

def generate_dynamic_html_template(data_files):
    """Generate HTML template with dynamic data loading"""
    
    # Create data files configuration for JavaScript
    data_files_js = str(data_files).replace("'", '"')
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Retail Tariff Data Viewer - Dynamic</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.8;
            font-size: 1.1em;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        .toc {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        
        .toc h3 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        
        .toc ul {{
            list-style: none;
            padding: 0;
        }}
        
        .toc li {{
            margin: 8px 0;
        }}
        
        .toc a {{
            color: #3498db;
            text-decoration: none;
            padding: 5px 10px;
            border-radius: 5px;
            transition: background-color 0.2s;
        }}
        
        .toc a:hover {{
            background-color: #e3f2fd;
        }}
        
        .table-section {{
            margin-bottom: 40px;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }}
        
        .table-header {{
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            padding: 20px;
            font-size: 1.3em;
            font-weight: 600;
        }}
        
        .table-filters {{
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .filters-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            align-items: end;
        }}
        
        .filter-group {{
            display: flex;
            flex-direction: column;
            gap: 5px;
        }}
        
        .filter-group label {{
            font-weight: 600;
            color: #495057;
            font-size: 0.9em;
        }}
        
        .filter-select {{
            padding: 8px 12px;
            border: 1px solid #ced4da;
            border-radius: 5px;
            background: white;
            font-size: 0.9em;
            transition: border-color 0.2s;
        }}
        
        .filter-select:focus {{
            outline: none;
            border-color: #3498db;
            box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
        }}
        
        .filter-actions {{
            display: flex;
            gap: 10px;
            align-items: end;
        }}
        
        .clear-filters, .export-csv {{
            padding: 8px 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9em;
            font-weight: 600;
            transition: all 0.2s;
        }}
        
        .clear-filters {{
            background: #6c757d;
            color: white;
        }}
        
        .clear-filters:hover {{
            background: #5a6268;
        }}
        
        .export-csv {{
            background: #28a745;
            color: white;
        }}
        
        .export-csv:hover {{
            background: #218838;
        }}
        
        .table-content {{
            overflow-x: auto;
            max-height: 500px;
            overflow-y: auto;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9em;
        }}
        
        th {{
            background: #f8f9fa;
            color: #495057;
            padding: 12px 8px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #dee2e6;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        
        td {{
            padding: 10px 8px;
            border-bottom: 1px solid #dee2e6;
        }}
        
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        tr:hover {{
            background-color: #e3f2fd;
            transition: background-color 0.2s;
        }}
        
        .loading {{
            text-align: center;
            padding: 40px;
            color: #666;
        }}
        
        .error {{
            background: #ffebee;
            color: #c62828;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #c62828;
        }}
        
        .refresh-btn {{
            background: #17a2b8;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            margin-bottom: 20px;
        }}
        
        .refresh-btn:hover {{
            background: #138496;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Retail Tariff Data Viewer - Dynamic</h1>
            <p>Real-time data loading from CSV files with interactive filtering</p>
        </div>
        
        <div class="content">
            <button class="refresh-btn" onclick="loadAllData()">🔄 Refresh Data</button>
            
            <div class="stats" id="stats">
                <div class="stat-card">
                    <div class="stat-number" id="total-records">-</div>
                    <div class="stat-label">Total Records</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="total-tables">-</div>
                    <div class="stat-label">Data Tables</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="last-updated">-</div>
                    <div class="stat-label">Last Updated</div>
                </div>
            </div>
            
            <div class="toc">
                <h3>📋 Table of Contents</h3>
                <ul id="toc-list">
                    <li><a href="#tariffs">📈 Tariffs</a></li>
                    <li><a href="#products">🛍️ Products</a></li>
                    <li><a href="#suppliers">🏭 Suppliers</a></li>
                    <li><a href="#markets">🌍 Markets</a></li>
                    <li><a href="#cost-transit">🚚 Cost & Transit</a></li>
                    <li><a href="#sales-daily">📅 Sales Daily</a></li>
                    <li><a href="#sales-weekly">📊 Sales Weekly</a></li>
                </ul>
            </div>
            
            <div id="data-container">
                <div class="loading">Loading data from CSV files...</div>
            </div>
        </div>
    </div>

    <script>
        // Data files configuration
        const dataFiles = {data_files_js};
        
        let totalRecords = 0;
        let loadedTables = 0;
        let tableData = {{}};

        // Function to parse CSV
        function parseCSV(csvText) {{
            const lines = csvText.trim().split('\\n');
            const headers = lines[0].split(',');
            const data = [];
            
            for (let i = 1; i < lines.length; i++) {{
                const values = lines[i].split(',');
                const row = {{}};
                headers.forEach((header, index) => {{
                    row[header.trim()] = values[index] ? values[index].trim() : '';
                }});
                data.push(row);
            }}
            
            return {{ headers, data }};
        }}

        // Function to create table HTML with filters
        function createTableHTML(id, name, icon, headers, data) {{
            const tableId = `table-${{id}}`;
            const maxRows = 100; // Limit display to first 100 rows for performance
            const displayData = data.slice(0, maxRows);
            
            // Create filter inputs
            const filterInputs = headers.map(col => {{
                const uniqueVals = [...new Set(data.map(row => row[col]))].slice(0, 20);
                const sortedVals = uniqueVals.sort();
                
                return `
                    <div class="filter-group">
                        <label for="filter-${{id}}-${{col}}">${{col}}:</label>
                        <select id="filter-${{id}}-${{col}}" class="filter-select" data-table="${{id}}" data-column="${{col}}">
                            <option value="">All</option>
                            ${{sortedVals.map(val => `<option value="${{val}}">${{val}}</option>`).join('')}}
                        </select>
                    </div>
                `;
            }}).join('');
            
            let tableHTML = `
                <div class="table-section" id="${{id}}">
                    <div class="table-header">
                        ${{icon}} ${{name}} (${{data.length}} records${{data.length > maxRows ? `, showing first ${{maxRows}}` : ''}})
                    </div>
                    <div class="table-filters">
                        <div class="filters-container">
                            ${{filterInputs}}
                            <div class="filter-actions">
                                <button class="clear-filters" data-table="${{id}}">Clear All</button>
                                <button class="export-csv" data-table="${{id}}">Export CSV</button>
                            </div>
                        </div>
                    </div>
                    <div class="table-content">
                        <table id="${{tableId}}">
                            <thead>
                                <tr>
                                    ${{headers.map(header => `<th>${{header}}</th>`).join('')}}
                                </tr>
                            </thead>
                            <tbody>
                                ${{displayData.map(row => 
                                    `<tr>${{headers.map(header => `<td>${{row[header] || ''}}</td>`).join('')}}</tr>`
                                ).join('')}}
                            </tbody>
                        </table>
                    </div>
                </div>
            `;
            
            return tableHTML;
        }}

        // Function to load data file
        async function loadDataFile(fileInfo) {{
            try {{
                const response = await fetch(`retail_tariff_data/${{fileInfo.file}}`);
                if (!response.ok) {{
                    throw new Error(`HTTP error! status: ${{response.status}}`);
                }}
                const csvText = await response.text();
                const {{ headers, data }} = parseCSV(csvText);
                
                // Store data for filtering
                tableData[fileInfo.id] = {{ headers, data }};
                
                totalRecords += data.length;
                loadedTables++;
                
                return createTableHTML(fileInfo.id, fileInfo.name, fileInfo.icon, headers, data);
            }} catch (error) {{
                console.error(`Error loading ${{fileInfo.file}}:`, error);
                
                // Check if it's a CORS error
                const isCorsError = error.message.includes('CORS') || 
                                  error.message.includes('Cross-Origin') ||
                                  error.message.includes('Failed to fetch');
                
                if (isCorsError) {{
                    return `
                        <div class="table-section" id="${{fileInfo.id}}">
                            <div class="table-header">
                                ${{fileInfo.icon}} ${{fileInfo.name}} - CORS Error
                            </div>
                            <div class="error">
                                <h4>🚫 CORS Error Detected</h4>
                                <p>Cannot load CSV files directly from file system due to browser security restrictions.</p>
                                <h5>Solutions:</h5>
                                <ol>
                                    <li><strong>Use Web Server:</strong> Run <code>python3 -m http.server 5002</code> and open <code>http://localhost:5002/data_viewer_dynamic.html</code></li>
                                    <li><strong>Use Embedded Viewer:</strong> Open <code>data_viewer_embedded.html</code> instead (works offline)</li>
                                    <li><strong>Use Update Script:</strong> Run <code>python3 update_data.py</code> to open with web server</li>
                                </ol>
                            </div>
                        </div>
                    `;
                }} else {{
                    return `
                        <div class="table-section" id="${{fileInfo.id}}">
                            <div class="table-header">
                                ${{fileInfo.icon}} ${{fileInfo.name}}
                            </div>
                            <div class="error">
                                Error loading ${{fileInfo.file}}: ${{error.message}}
                            </div>
                        </div>
                    `;
                }}
            }}
        }}

        // Filter functionality
        function filterTable(tableId) {{
            const table = document.getElementById(`table-${{tableId}}`);
            const rows = table.querySelectorAll('tbody tr');
            const filters = document.querySelectorAll(`[data-table="${{tableId}}"]`);
            
            rows.forEach(row => {{
                let showRow = true;
                
                filters.forEach(filter => {{
                    if (filter.value) {{
                        const column = filter.dataset.column;
                        const filterValue = filter.value.toLowerCase();
                        const cellValue = row.querySelector(`td:nth-child(${{Array.from(table.querySelectorAll('th')).findIndex(th => th.textContent.trim() === column) + 1}})`)?.textContent.toLowerCase();
                        
                        if (!cellValue || !cellValue.includes(filterValue)) {{
                            showRow = false;
                        }}
                    }}
                }});
                
                row.style.display = showRow ? '' : 'none';
            }});
            
            // Update visible row count
            updateVisibleCount(tableId);
        }}
        
        function updateVisibleCount(tableId) {{
            const table = document.getElementById(`table-${{tableId}}`);
            const visibleRows = table.querySelectorAll('tbody tr:not([style*="display: none"])');
            const header = document.querySelector(`#${{tableId}} .table-header`);
            const originalText = header.textContent;
            const baseText = originalText.split(' (')[0];
            header.textContent = `${{baseText}} (${{visibleRows.length}} visible rows)`;
        }}
        
        function clearFilters(tableId) {{
            const filters = document.querySelectorAll(`[data-table="${{tableId}}"]`);
            filters.forEach(filter => {{
                filter.value = '';
            }});
            filterTable(tableId);
        }}
        
        function exportTableToCSV(tableId) {{
            const table = document.getElementById(`table-${{tableId}}`);
            const rows = Array.from(table.querySelectorAll('tr'));
            
            const csvContent = rows.map(row => {{
                const cells = Array.from(row.querySelectorAll('th, td'));
                return cells.map(cell => `"${{cell.textContent.replace(/"/g, '""')}}"`).join(',');
            }}).join('\\n');
            
            const blob = new Blob([csvContent], {{ type: 'text/csv' }});
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${{tableId}}_filtered_data.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }}

        // Load all data
        async function loadAllData() {{
            const container = document.getElementById('data-container');
            container.innerHTML = '<div class="loading">Loading data from CSV files...</div>';
            
            // Reset counters
            totalRecords = 0;
            loadedTables = 0;
            tableData = {{}};
            
            try {{
                const tableHTMLs = await Promise.all(dataFiles.map(loadDataFile));
                container.innerHTML = tableHTMLs.join('');
                
                // Update stats
                document.getElementById('total-records').textContent = totalRecords.toLocaleString();
                document.getElementById('total-tables').textContent = loadedTables;
                document.getElementById('last-updated').textContent = new Date().toLocaleTimeString();
                
                // Initialize event listeners
                initializeEventListeners();
                
            }} catch (error) {{
                container.innerHTML = `
                    <div class="error">
                        Failed to load data: ${{error.message}}
                    </div>
                `;
            }}
        }}

        // Initialize event listeners
        function initializeEventListeners() {{
            // Add change event listeners to all filter selects
            document.querySelectorAll('.filter-select').forEach(select => {{
                select.addEventListener('change', function() {{
                    const tableId = this.dataset.table;
                    filterTable(tableId);
                }});
            }});
            
            // Add click event listeners to clear buttons
            document.querySelectorAll('.clear-filters').forEach(button => {{
                button.addEventListener('click', function() {{
                    const tableId = this.dataset.table;
                    clearFilters(tableId);
                }});
            }});
            
            // Add click event listeners to export buttons
            document.querySelectorAll('.export-csv').forEach(button => {{
                button.addEventListener('click', function() {{
                    const tableId = this.dataset.table;
                    exportTableToCSV(tableId);
                }});
            }});
            
            // Initialize visible counts for all tables
            dataFiles.forEach(fileInfo => {{
                if (document.getElementById(`table-${{fileInfo.id}}`)) {{
                    updateVisibleCount(fileInfo.id);
                }}
            }});
        }}

        // Initialize on page load
        document.addEventListener('DOMContentLoaded', loadAllData);
    </script>
</body>
</html>"""
    
    return html_template

if __name__ == "__main__":
    generate_dynamic_html_viewer()
