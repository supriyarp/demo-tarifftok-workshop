#!/usr/bin/env python3
"""
CRUD Server for Retail Tariff Data
Provides REST API endpoints for Create, Read, Update, Delete operations
"""

import os
import csv
import json
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
DATA_DIR = "retail_tariff_data"
PORT = 5001

# Data validation rules for each table
VALIDATION_RULES = {
    "tariffs": {
        "country": {"type": "string", "required": True, "max_length": 50},
        "product_type": {"type": "string", "required": True, "max_length": 50},
        "current_tariff": {"type": "float", "required": True, "min": 0, "max": 1},
        "start_time": {"type": "date", "required": True}
    },
    "products": {
        "product_id": {"type": "string", "required": True, "max_length": 20},
        "product_name": {"type": "string", "required": True, "max_length": 100},
        "product_type": {"type": "string", "required": True, "max_length": 50},
        "country_of_origin": {"type": "string", "required": True, "max_length": 50},
        "AUR": {"type": "float", "required": True, "min": 0},
        "base_cost": {"type": "float", "required": True, "min": 0},
        "weight_kg": {"type": "float", "required": True, "min": 0},
        "supplier_id": {"type": "string", "required": True, "max_length": 20}
    },
    "suppliers": {
        "supplier_id": {"type": "string", "required": True, "max_length": 20},
        "country": {"type": "string", "required": True, "max_length": 50},
        "risk": {"type": "string", "required": True, "choices": ["Low", "Medium", "High"]},
        "capacity_limit_qtr": {"type": "integer", "required": True, "min": 0},
        "lead_time_days": {"type": "integer", "required": True, "min": 0},
        "base_cost_multiplier": {"type": "float", "required": True, "min": 0},
        "freight_adj": {"type": "float", "required": True, "min": 0},
        "supplier_quality_score": {"type": "integer", "required": True, "min": 1, "max": 5},
        "lead_time_variation": {"type": "float", "required": True, "min": 0}
    },
    "markets": {
        "market_id": {"type": "string", "required": True, "max_length": 20},
        "market_name": {"type": "string", "required": True, "max_length": 100},
        "region": {"type": "string", "required": True, "max_length": 50},
        "country": {"type": "string", "required": True, "max_length": 50},
        "population": {"type": "integer", "required": False, "min": 0}
    },
    "cost_transit": {
        "product_id": {"type": "string", "required": True, "max_length": 20},
        "origin_country": {"type": "string", "required": True, "max_length": 50},
        "destination_market": {"type": "string", "required": True, "max_length": 50},
        "lane": {"type": "string", "required": True, "max_length": 100},
        "lead_time_days": {"type": "float", "required": True, "min": 0},
        "transit_time_days": {"type": "integer", "required": True, "min": 0},
        "cost_of_sourcing": {"type": "float", "required": True, "min": 0},
        "freight_per_unit": {"type": "float", "required": True, "min": 0},
        "incoterm": {"type": "string", "required": False, "max_length": 10}
    },
    "sales_weekly": {
        "week_id": {"type": "string", "required": True, "max_length": 20},
        "product_id": {"type": "string", "required": True, "max_length": 20},
        "market_id": {"type": "string", "required": True, "max_length": 20},
        "week_start": {"type": "date", "required": True},
        "units_sold": {"type": "integer", "required": True, "min": 0},
        "revenue": {"type": "float", "required": True, "min": 0}
    },
    "sales_daily": {
        "sale_id": {"type": "string", "required": True, "max_length": 20},
        "product_id": {"type": "string", "required": True, "max_length": 20},
        "market_id": {"type": "string", "required": True, "max_length": 20},
        "sale_date": {"type": "date", "required": True},
        "units_sold": {"type": "integer", "required": True, "min": 0},
        "unit_price": {"type": "float", "required": True, "min": 0}
    }
}

def validate_data(table_name, data):
    """Validate data against table rules"""
    if table_name not in VALIDATION_RULES:
        return False, f"Unknown table: {table_name}"
    
    rules = VALIDATION_RULES[table_name]
    errors = []
    
    for field, rule in rules.items():
        value = data.get(field)
        
        # Check required fields
        if rule.get("required", False) and (value is None or value == ""):
            errors.append(f"{field} is required")
            continue
        
        # Skip validation for empty optional fields
        if not rule.get("required", False) and (value is None or value == ""):
            continue
        
        # Type validation
        if rule["type"] == "string":
            if not isinstance(value, str):
                errors.append(f"{field} must be a string")
            elif "max_length" in rule and len(value) > rule["max_length"]:
                errors.append(f"{field} must be {rule['max_length']} characters or less")
        elif rule["type"] == "integer":
            try:
                int_val = int(value)
                if "min" in rule and int_val < rule["min"]:
                    errors.append(f"{field} must be at least {rule['min']}")
                if "max" in rule and int_val > rule["max"]:
                    errors.append(f"{field} must be at most {rule['max']}")
            except (ValueError, TypeError):
                errors.append(f"{field} must be an integer")
        elif rule["type"] == "float":
            try:
                float_val = float(value)
                if "min" in rule and float_val < rule["min"]:
                    errors.append(f"{field} must be at least {rule['min']}")
                if "max" in rule and float_val > rule["max"]:
                    errors.append(f"{field} must be at most {rule['max']}")
            except (ValueError, TypeError):
                errors.append(f"{field} must be a number")
        elif rule["type"] == "date":
            try:
                datetime.strptime(value, "%Y-%m-%d")
            except (ValueError, TypeError):
                errors.append(f"{field} must be a valid date (YYYY-MM-DD)")
        elif rule["type"] == "email":
            if "@" not in str(value) or "." not in str(value):
                errors.append(f"{field} must be a valid email address")
        
        # Choice validation
        if "choices" in rule and value not in rule["choices"]:
            errors.append(f"{field} must be one of: {', '.join(rule['choices'])}")
    
    return len(errors) == 0, errors

def get_csv_path(table_name):
    """Get the CSV file path for a table"""
    return os.path.join(DATA_DIR, f"{table_name}.csv")

def read_csv_data(table_name):
    """Read data from CSV file"""
    csv_path = get_csv_path(table_name)
    if not os.path.exists(csv_path):
        return []
    
    with open(csv_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_csv_data(table_name, data):
    """Write data to CSV file"""
    csv_path = get_csv_path(table_name)
    
    if not data:
        # Create empty file with headers
        with open(csv_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([])
        return
    
    # Write data with headers
    with open(csv_path, 'w', newline='', encoding='utf-8') as file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# API Routes

@app.route('/api/tables', methods=['GET'])
def get_tables():
    """Get list of available tables"""
    tables = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.csv'):
            table_name = filename[:-4]  # Remove .csv extension
            tables.append({
                'name': table_name,
                'file': filename,
                'path': f"/api/tables/{table_name}"
            })
    return jsonify(tables)

@app.route('/api/tables/<table_name>', methods=['GET'])
def get_table_data(table_name):
    """Get paginated data from a table"""
    try:
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        
        # Read all data
        all_data = read_csv_data(table_name)
        total_count = len(all_data)
        
        # Calculate pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_data = all_data[start_idx:end_idx]
        
        return jsonify({
            'table': table_name,
            'data': paginated_data,
            'count': total_count,
            'page': page,
            'per_page': per_page,
            'total_pages': (total_count + per_page - 1) // per_page,
            'has_next': end_idx < total_count,
            'has_prev': page > 1
        })
    except Exception as e:
        logger.error(f"Error reading table {table_name}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tables/<table_name>/<int:row_id>', methods=['GET'])
def get_row(table_name, row_id):
    """Get a specific row by index"""
    try:
        data = read_csv_data(table_name)
        if 0 <= row_id < len(data):
            return jsonify({
                'table': table_name,
                'row_id': row_id,
                'data': data[row_id]
            })
        else:
            return jsonify({'error': 'Row not found'}), 404
    except Exception as e:
        logger.error(f"Error reading row {row_id} from {table_name}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tables/<table_name>', methods=['POST'])
def create_row(table_name):
    """Create a new row"""
    try:
        new_data = request.get_json()
        
        # Validate data
        is_valid, errors = validate_data(table_name, new_data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400
        
        # Read existing data
        data = read_csv_data(table_name)
        
        # Add new row
        data.append(new_data)
        
        # Write back to CSV
        write_csv_data(table_name, data)
        
        logger.info(f"Created new row in {table_name}")
        return jsonify({
            'message': 'Row created successfully',
            'table': table_name,
            'row_id': len(data) - 1,
            'data': new_data
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating row in {table_name}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tables/<table_name>/<int:row_id>', methods=['PUT'])
def update_row(table_name, row_id):
    """Update an existing row"""
    try:
        updated_data = request.get_json()
        
        # Validate data
        is_valid, errors = validate_data(table_name, updated_data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400
        
        # Read existing data
        data = read_csv_data(table_name)
        
        if 0 <= row_id < len(data):
            # Update the row
            data[row_id] = updated_data
            
            # Write back to CSV
            write_csv_data(table_name, data)
            
            logger.info(f"Updated row {row_id} in {table_name}")
            return jsonify({
                'message': 'Row updated successfully',
                'table': table_name,
                'row_id': row_id,
                'data': updated_data
            })
        else:
            return jsonify({'error': 'Row not found'}), 404
            
    except Exception as e:
        logger.error(f"Error updating row {row_id} in {table_name}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tables/<table_name>/<int:row_id>', methods=['DELETE'])
def delete_row(table_name, row_id):
    """Delete a row"""
    try:
        # Read existing data
        data = read_csv_data(table_name)
        
        if 0 <= row_id < len(data):
            # Remove the row
            deleted_data = data.pop(row_id)
            
            # Write back to CSV
            write_csv_data(table_name, data)
            
            logger.info(f"Deleted row {row_id} from {table_name}")
            return jsonify({
                'message': 'Row deleted successfully',
                'table': table_name,
                'row_id': row_id,
                'deleted_data': deleted_data
            })
        else:
            return jsonify({'error': 'Row not found'}), 404
            
    except Exception as e:
        logger.error(f"Error deleting row {row_id} from {table_name}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/validation-rules/<table_name>', methods=['GET'])
def get_validation_rules(table_name):
    """Get validation rules for a table"""
    if table_name in VALIDATION_RULES:
        return jsonify({
            'table': table_name,
            'rules': VALIDATION_RULES[table_name]
        })
    else:
        return jsonify({'error': 'Table not found'}), 404

# Serve static files (HTML viewer)
@app.route('/')
def serve_index():
    return send_from_directory('../..', 'data_viewer_crud.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('../..', filename)

if __name__ == '__main__':
    print(f"🚀 Starting CRUD Server on port {PORT}")
    print(f"📁 Data directory: {DATA_DIR}")
    print(f"🌐 API endpoints:")
    print(f"   GET    /api/tables - List all tables")
    print(f"   GET    /api/tables/<name> - Get table data")
    print(f"   POST   /api/tables/<name> - Create new row")
    print(f"   PUT    /api/tables/<name>/<id> - Update row")
    print(f"   DELETE /api/tables/<name>/<id> - Delete row")
    print(f"🔧 Validation rules available for all tables")
    print(f"📊 Open http://localhost:{PORT} to view the CRUD interface")
    
    app.run(host='0.0.0.0', port=PORT, debug=True)
