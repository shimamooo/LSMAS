#!/usr/bin/env python3
"""
Script to count the number of entries in a JSON file.
Supports various JSON structures including lists, dictionaries, and nested structures.
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Union, Dict, List, Any


def count_json_entries(data: Union[Dict, List, Any]) -> int:
    """
    Count the number of entries in a JSON data structure.
    
    Args:
        data: The JSON data (dict, list, or other)
    
    Returns:
        int: Number of entries
    """
    if isinstance(data, list):
        return len(data)
    elif isinstance(data, dict):
        return len(data)
    elif isinstance(data, (str, int, float, bool)) or data is None:
        return 1
    else:
        # For other types, try to get length or return 1
        try:
            return len(data)
        except TypeError:
            return 1


def analyze_json_structure(data: Union[Dict, List, Any], max_depth: int = 3, current_depth: int = 0) -> str:
    """
    Analyze and describe the structure of JSON data.
    
    Args:
        data: The JSON data to analyze
        max_depth: Maximum depth to analyze
        current_depth: Current depth in recursion
    
    Returns:
        str: Description of the structure
    """
    if current_depth >= max_depth:
        return "..."
    
    if isinstance(data, list):
        if len(data) == 0:
            return "empty list"
        elif len(data) == 1:
            return f"list with 1 item: {analyze_json_structure(data[0], max_depth, current_depth + 1)}"
        else:
            sample_item = analyze_json_structure(data[0], max_depth, current_depth + 1)
            return f"list with {len(data)} items (sample: {sample_item})"
    
    elif isinstance(data, dict):
        if len(data) == 0:
            return "empty dict"
        else:
            keys = list(data.keys())[:3]
            key_str = ", ".join(keys)
            if len(data) > 3:
                key_str += f" ... and {len(data) - 3} more"
            return f"dict with {len(data)} keys: {key_str}"
    
    elif isinstance(data, (str, int, float, bool)) or data is None:
        return f"{type(data).__name__}: {str(data)[:50]}"
    
    else:
        return f"unknown type: {type(data).__name__}"


def main():
    parser = argparse.ArgumentParser(description="Count entries in a JSON file")
    parser.add_argument("json_file", help="Path to the JSON file")
    parser.add_argument("--analyze", "-a", action="store_true", 
                       help="Analyze and show the structure of the JSON")
    parser.add_argument("--pretty", "-p", action="store_true",
                       help="Pretty print the count with more details")
    
    args = parser.parse_args()
    
    json_path = Path(args.json_file)
    
    if not json_path.exists():
        print(f"Error: File '{json_path.name}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON file: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    count = count_json_entries(data)
    
    if args.pretty:
        print(f"JSON File Analysis: {json_path.name}")
        print(f"File path: {json_path.absolute()}")
        print(f"Total entries: {count:,}")
        print(f"Data type: {type(data).__name__}")
        
        if args.analyze:
            print(f"Structure: {analyze_json_structure(data)}")
        
        if isinstance(data, list):
            if count > 0:
                print(f"First item type: {type(data[0]).__name__}")
                if isinstance(data[0], dict):
                    print(f"🔑 Sample keys: {list(data[0].keys())[:5]}")
        elif isinstance(data, dict):
            print(f"🔑 Top-level keys: {list(data.keys())[:10]}")
    
    else:
        print(count)
        
        if args.analyze:
            print(f"Structure: {analyze_json_structure(data)}")


if __name__ == "__main__":
    main()
