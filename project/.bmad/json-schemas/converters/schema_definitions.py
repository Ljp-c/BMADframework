# -*- coding: utf-8 -*-

def validate_json(data, schema_name):
    """Validate JSON data"""
    if not isinstance(data, dict):
        return False
    return True

def validate_required_fields(data, required_fields):
    """Check for missing required fields"""
    missing = [f for f in required_fields if f not in data]
    return missing
