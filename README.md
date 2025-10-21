# xl2usernames

A Python tool for generating username combinations from Excel files containing employee or user names. Useful for penetration testing, OSINT, and security assessments.



## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/xl2usernames.git
cd xl2usernames

# Install dependencies
pip3 install -r requirements.txt
```

### Platform-Specific Installation

**Debian/Ubuntu/Kali:**
```bash
sudo apt install python3-pip
pip3 install -r requirements.txt
```

**Arch/Manjaro:**
```bash
sudo pacman -S python-pandas python-openpyxl python-xlrd
```

**Fedora/RHEL:**
```bash
sudo dnf install python3-pip
pip3 install -r requirements.txt
```

**macOS:**
```bash
brew install python3
pip3 install -r requirements.txt
```

### Requirements

```
pandas>=1.3.0
openpyxl>=3.0.0
xlrd>=2.0.0
```

## Usage

### Basic Usage

```bash
# Generate usernames (saves to ./usernames.list by default)
python3 username_generator.py -t employees.xlsx

# Specify output location
python3 username_generator.py -t employees.xlsx -o /tmp/usernames.list

# Specify output filename in current directory
python3 username_generator.py -t employees.xlsx -o users.txt

# Verbose output
python3 username_generator.py -t employees.xlsx -v

# Specify column name
python3 username_generator.py -t employees.xlsx -c "Full Name"

# Combine options
python3 username_generator.py -t employees.xlsx -c "Employee Name" -o users.list -v
```

## Username Generation Patterns

For a name like **"Dilanka Kaushal Hewage"**, the tool generates:

### Single Names
- `dilanka`
- `kaushal`
- `hewage`

### Two-Part Combinations
- `dilankahewage`
- `hewagadilanka`
- `dilankakaushal`
- `kaushalhewage`
- `kaushaldilanka`
- `hewagekaushal`

### Initial Combinations
- `dhewage` (first initial + last)
- `dilankah` (first + last initial)
- `hdilanka` (last initial + first)

### Three-Part Combinations
- `dilankakauschalhewage` (all parts)
- `dkhewage` (all initials + last)
- `dilankakhewage` (first + middle initial + last)

### Common Formats
- `dilanka.hewage`
- `dilanka_hewage`
- `d.hewage`

## Example Output

```
$ python3 username_generator.py -t employees.xlsx -v

[+] Loading Excel file: employees.xlsx
[+] Found 16 rows and 4 columns
[+] Auto-detected name column: 'Full Name'
[+] Extracted 15 names

[+] Processing: Dilanka Kaushal Hewage
    Generated 23 combinations
[+] Processing: Arthur Edwards
    Generated 15 combinations
...

[+] Total unique usernames: 187
[+] Output saved to: /home/user/usernames.list

[+] Done!
```

## Use Cases

### Penetration Testing
```bash
# Generate usernames for brute force attacks
python3 username_generator.py -t company_employees.xlsx -o users.txt

# Use with hydra
hydra -L users.txt -P passwords.txt ssh://target.com
```

### OSINT Investigations
```bash
# Generate possible usernames for social media enumeration
python3 username_generator.py -t persons_of_interest.xlsx -o targets.list
```

### Security Audits
```bash
# Check for weak username patterns in organization
python3 username_generator.py -t hr_export.xlsx -o audit_users.list
```

## Command-Line Options

| Option | Description |
|--------|-------------|
| `-t, --target` | Path to Excel file (required) |
| `-o, --output` | Output file path (default: ./usernames.list) |
| `-c, --column` | Column name containing names (auto-detect if not specified) |
| `-v, --verbose` | Show detailed processing information |
| `-h, --help` | Show help message |

## Error Handling

The tool handles common issues gracefully:

- **File not found**: Clear error message with file path
- **Permission denied**: Automatic fallback to `/tmp/` directory
- **Invalid column**: Shows available columns and prompts for selection
- **Malformed data**: Skips invalid entries and continues processing


## License

MIT License - see LICENSE file for details

## Disclaimer

This tool is intended for legal security testing and educational purposes only. Users are responsible for ensuring they have proper authorization before testing any systems or networks. The authors assume no liability for misuse of this tool.

## Author

**n0p5l1d3r**

## Acknowledgments

- Inspired by common penetration testing workflows
- Built for the security community

---

⭐ If you find this tool useful, please consider giving it a star!
