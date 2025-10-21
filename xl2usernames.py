#!/usr/bin/env python3
"""
Username Generator - Extract names from Excel and generate username combinations
Author: n0p5l1d3r
License: MIT
"""

import pandas as pd
import sys
import os
import argparse
from itertools import combinations
import tempfile


def generate_username_combinations(full_name):
    """
    Generate all possible username combinations from a full name.
    Example: "Dilanka Kaushal Hewage" -> dilanka, dilankahewage, dilankakaushal, etc.
    """
    # Clean and split the name
    parts = full_name.lower().strip().split()
    
    if not parts:
        return []
    
    usernames = set()
    
    # Single names (first, middle, last)
    for part in parts:
        usernames.add(part)
    
    # Two-part combinations
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            usernames.add(parts[i] + parts[j])  # firstname + lastname
            usernames.add(parts[j] + parts[i])  # lastname + firstname
    
    # Three-part combinations (if applicable)
    if len(parts) >= 3:
        for combo in combinations(range(len(parts)), 3):
            usernames.add(''.join([parts[i] for i in combo]))
    
    # First letter + last name combinations
    if len(parts) >= 2:
        usernames.add(parts[0][0] + parts[-1])  # d.hewage -> dhewage
        usernames.add(parts[0] + parts[-1][0])  # dilankah
    
    # First name + middle initial + last name
    if len(parts) >= 3:
        usernames.add(parts[0] + parts[1][0] + parts[-1])  # dilankakhewage
    
    # Full name concatenated
    usernames.add(''.join(parts))
    
    return sorted(list(usernames))


def extract_names_from_excel(excel_file, output_file, column_name=None, verbose=False):
    """
    Extract names from Excel file and generate username combinations.
    """
    try:
        # Read Excel file (supports .xlsx and .xls)
        df = pd.read_excel(excel_file)
        
        print(f"[+] Reading Excel file: {excel_file}")
        print(f"[+] Found {len(df)} rows")
        print(f"[+] Columns: {', '.join(df.columns)}\n")
        
        # Try to find name column (common column names)
        name_column = None
        
        if column_name:
            # Use specified column
            if column_name in df.columns:
                name_column = column_name
            else:
                print(f"[-] Column '{column_name}' not found!")
                print(f"[!] Available columns: {', '.join(df.columns)}")
                sys.exit(1)
        else:
            # Auto-detect
            possible_columns = ['name', 'full name', 'fullname', 'full_name', 'employee', 'user']
            
            for col in df.columns:
                if col.lower() in possible_columns:
                    name_column = col
                    break
            
            # If not found, use first column
            if name_column is None:
                print("[!] Could not auto-detect name column. Using first column.")
                name_column = df.columns[0]
        
        print(f"[+] Using column: '{name_column}'")
        
        all_usernames = set()
        
        # Process each name
        for idx, row in df.iterrows():
            name = str(row[name_column]).strip()
            
            # Skip empty or NaN values
            if name and name.lower() not in ['nan', 'none', '']:
                if verbose:
                    print(f"[+] Processing: {name}")
                usernames = generate_username_combinations(name)
                all_usernames.update(usernames)
                if verbose:
                    print(f"    Generated {len(usernames)} combinations")
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Write to output file
        try:
            with open(output_file, 'w') as f:
                for username in sorted(all_usernames):
                    f.write(username + '\n')
            
            print(f"\n[+] Total unique usernames: {len(all_usernames)}")
            print(f"[+] Saved to: {output_file}")
            
        except PermissionError:
            # Fallback to user's home directory if permission denied
            home_dir = os.path.expanduser("~")
            fallback_path = os.path.join(home_dir, "usernames.list")
            
            print(f"[!] Permission denied: {output_file}")
            print(f"[+] Saving to fallback location: {fallback_path}")
            
            try:
                with open(fallback_path, 'w') as f:
                    for username in sorted(all_usernames):
                        f.write(username + '\n')
                
                print(f"[+] Total unique usernames: {len(all_usernames)}")
                print(f"[+] Output saved to: {fallback_path}")
            except PermissionError:
                # Last resort: use system temp directory
                temp_path = os.path.join(tempfile.gettempdir(), "usernames.list")
                print(f"[!] Cannot write to home directory, using temp: {temp_path}")
                
                with open(temp_path, 'w') as f:
                    for username in sorted(all_usernames):
                        f.write(username + '\n')
                
                print(f"[+] Total unique usernames: {len(all_usernames)}")
                print(f"[+] Output saved to: {temp_path}")
        
    except FileNotFoundError:
        print(f"[-] Error: File '{excel_file}' not found!")
        sys.exit(1)
    except Exception as e:
        print(f"[-] Error: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Generate username combinations from Excel file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s -t employees.xlsx
  %(prog)s -t employees.xlsx -o /tmp/usernames.list
  %(prog)s -t employees.xlsx -o usernames.txt -v
  %(prog)s -t employees.xlsx -c "Full Name"
        '''
    )
    
    parser.add_argument('-t', '--target', required=True,
                        help='Target Excel file (.xlsx or .xls)')
    parser.add_argument('-o', '--output', default=None,
                        help='Output file path (default: usernames.list in current directory)')
    parser.add_argument('-c', '--column', default=None,
                        help='Name of column containing names (auto-detect if not specified)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose output')
    
    args = parser.parse_args()
    
    # Set default output to current directory if not specified
    if args.output is None:
        args.output = os.path.join(os.getcwd(), 'usernames.list')
    
    try:
        extract_names_from_excel(args.target, args.output, args.column, args.verbose)
        print(f"\n[+] Done!")
        
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        sys.exit(1)


if __name__ == "__main__":
    main()
