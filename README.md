# Bible JSON Converter

Convert nested Bible JSON structure to flat array format optimized for Flutter/Isar offline Bible apps.

## Overview

This tool converts Bible JSON from a nested structure to a flat array format that's perfect for mobile app storage and offline access.

**Input Format:**
```json
{
  "Genesis": {
    "1": {
      "1": "In the beginning God created the heaven and the earth.",
      "2": "And the earth was without form..."
    }
  }
}
```

**Output Format:**
```json
{
  "name": "King James Version",
  "books": [
    {
      "name": "Genesis",
      "book_number": 1,
      "testament": "Old",
      "chapters": [
        [
          "1 In the beginning God created the heaven and the earth.",
          "2 And the earth was without form..."
        ]
      ]
    }
  ]
}
```

## Features

- ✅ Converts 66 canonical books (Old & New Testament)
- ✅ Automatically adds verse numbers to text
- ✅ Maintains proper book ordering
- ✅ UTF-8 support for all translations
- ✅ Production-ready error handling
- ✅ File size and statistics reporting

## Setup

### Prerequisites

- Python 3.7+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/bblauto.git
cd bblauto

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Create data directory
mkdir data
```

## Usage

1. **Place your input file:**
   ```bash
   # Add your Bible JSON file to:
   data/input_bible.json
   ```

2. **Run the converter:**
   ```bash
   python bible_converter.py
   ```

3. **Get your output:**
   ```bash
   # Converted file will be at:
   data/output_bible.json
   ```

## Configuration

Edit `bible_converter.py` to customize:

```python
INPUT_FILE = "data/input_bible.json"
OUTPUT_FILE = "data/output_bible.json"
BIBLE_NAME = "King James Version"  # Change to your translation name
```

## Project Structure

```
bblauto/
├── bible_converter.py    # Main conversion script
├── data/
│   ├── input_bible.json  # Your source Bible (not included)
│   └── output_bible.json # Generated output (not included)
├── README.md
├── LICENSE
└── .gitignore
```

## Output Files

Multiple Bible translations will be added to the `data/` directory over time:
- `output_bible.json` - Current conversion output
- Additional translations coming soon...

**Note:** Output JSON files are not included in this repository. You must provide your own input Bible JSON and generate the output files using the converter script.

## Use Cases

- Flutter/Dart offline Bible apps
- React Native Bible readers
- Isar database storage
- Laravel API backends
- Mobile app development

## Supported Translations

The converter works with any Bible translation in the supported input format. Common translations include:

**Public Domain:**
- King James Version (KJV)
- American Standard Version (ASV)
- Young's Literal Translation (YLT)
- World English Bible (WEB)

**Licensed Translations:**
- English Standard Version (ESV)
- New International Version (NIV)
- New Living Translation (NLT)
- New American Standard Bible (NASB)
- And many more...

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This converter script is released under the MIT License. See [LICENSE](LICENSE) for details.

---

## ⚠️ DISCLAIMER

The Bible text files and JSON outputs that may be generated using this converter are for **educational, personal, non-commercial, and reference purposes only**.

**Important Legal Information:**

- Many Bible translations are **protected by copyright** and may not be legally redistributed or used in other projects without explicit permission from their respective copyright holders.

- Bible text sources may be subject to the Terms of Service of their original providers and the individual licenses for each Bible translation.

- Some translations (such as **KJV, ASV, YLT, and WEB**) are in the **public domain** and may be freely used.

- Others (e.g., **ESV, NIV, NLT, NASB**, etc.) are **licensed translations** and require permission for redistribution or certain commercial uses.

**Your Responsibility:**

- **You are solely responsible** for ensuring you have the proper rights or licenses before using, distributing, or publishing any Bible translations.

- Always verify the copyright status and usage terms for your specific Bible translation before using it in any project.

- Consult with the copyright holder or publisher if you plan to use a licensed translation commercially or for public distribution.

**No Affiliation:**

- This project does not claim ownership of any Bible text.
- This project is not affiliated with any Bible publisher, copyright holder, or content provider.
- All Bible texts remain the property of their respective copyright holders.

**Use at Your Own Risk:**

By using this converter and any resulting files, you agree to respect all applicable copyright laws and licensing terms. The maintainers of this repository assume no liability for any misuse of Bible texts or violation of copyright laws.

---

## Support

For issues or questions, please open an issue on GitHub.

## Roadmap

- [ ] Add batch conversion support
- [ ] Support for additional input formats
- [ ] Verse reference validation
- [ ] Cross-reference linking
- [ ] Search index generation

---

**Made with ❤️ for Bible app developers**
