"""
Bible JSON Converter -
Converts nested Bible JSON to Flat Array Structure for Flutter/Isar
Input: {Book: {Chapter: {Verse: text}}}
Output: Flat array structure with verse numbers
"""

import json
import sys
import os
from pathlib import Path

# Complete 66 canonical books in order
BOOK_INFO = [
    # Old Testament (39 books)
    ("Genesis", "Old"), ("Exodus", "Old"), ("Leviticus", "Old"), ("Numbers", "Old"),
    ("Deuteronomy", "Old"), ("Joshua", "Old"), ("Judges", "Old"), ("Ruth", "Old"),
    ("1 Samuel", "Old"), ("2 Samuel", "Old"), ("1 Kings", "Old"), ("2 Kings", "Old"),
    ("1 Chronicles", "Old"), ("2 Chronicles", "Old"), ("Ezra", "Old"), ("Nehemiah", "Old"),
    ("Esther", "Old"), ("Job", "Old"), ("Psalms", "Old"), ("Proverbs", "Old"),
    ("Ecclesiastes", "Old"), ("Song of Solomon", "Old"), ("Isaiah", "Old"), ("Jeremiah", "Old"),
    ("Lamentations", "Old"), ("Ezekiel", "Old"), ("Daniel", "Old"), ("Hosea", "Old"),
    ("Joel", "Old"), ("Amos", "Old"), ("Obadiah", "Old"), ("Jonah", "Old"),
    ("Micah", "Old"), ("Nahum", "Old"), ("Habakkuk", "Old"), ("Zephaniah", "Old"),
    ("Haggai", "Old"), ("Zechariah", "Old"), ("Malachi", "Old"),
    # New Testament (27 books)
    ("Matthew", "New"), ("Mark", "New"), ("Luke", "New"), ("John", "New"),
    ("Acts", "New"), ("Romans", "New"), ("1 Corinthians", "New"), ("2 Corinthians", "New"),
    ("Galatians", "New"), ("Ephesians", "New"), ("Philippians", "New"), ("Colossians", "New"),
    ("1 Thessalonians", "New"), ("2 Thessalonians", "New"), ("1 Timothy", "New"), ("2 Timothy", "New"),
    ("Titus", "New"), ("Philemon", "New"), ("Hebrews", "New"), ("James", "New"),
    ("1 Peter", "New"), ("2 Peter", "New"), ("1 John", "New"), ("2 John", "New"),
    ("3 John", "New"), ("Jude", "New"), ("Revelation", "New")
]

# Common alternate book name variants mapped to canonical BOOK_INFO names
# Keys are lower-cased variants that may appear in input files.
BOOK_NAME_ALIASES = {
    "psalm": "Psalms",
    "psalms": "Psalms",
    "song of songs": "Song of Solomon",
    "song of solomon": "Song of Solomon",
    # add more aliases here as needed
}

def convert_to_flat_array(input_data, bible_name="King James Version"):
    """
    Convert nested Bible JSON to Flat Array Structure
    
    Input format: {Book: {Chapter: {Verse: text}}}
    Output format: Flat array with verse numbers prepended
    
    Args:
        input_data: Nested dictionary structure
        bible_name: Name of the Bible translation
        
    Returns:
        Dictionary in flat array format ready for Flutter/Isar
    """
    
    # Create lookup for book info
    book_lookup = {name: (idx + 1, testament) for idx, (name, testament) in enumerate(BOOK_INFO)}
    
    books = []
    stats = {
        'books': 0,
        'chapters': 0,
        'verses': 0,
        'old_testament': 0,
        'new_testament': 0
    }
    
    print(f"\n📖 Converting: {bible_name}")
    print("=" * 60)
    
    for book_name, chapters_dict in input_data.items():
        # Normalize common alternate book names (case-insensitive)
        lookup_key = book_name.strip().lower()
        canonical_name = BOOK_NAME_ALIASES.get(lookup_key, book_name)
        if canonical_name != book_name:
            print(f"ℹ️  Normalized: '{book_name}' -> '{canonical_name}'")

        # Get book info from lookup
        if canonical_name in book_lookup:
            book_number, testament = book_lookup[canonical_name]
            book_name_used = canonical_name
        else:
            # Handle books not in standard list
            print(f"⚠️  Warning: '{book_name}' not in standard list")
            book_number = len(books) + 1
            testament = "Old"
            book_name_used = book_name

        # Convert chapters to flat array format
        chapters = []
        for chapter_num in sorted(chapters_dict.keys(), key=int):
            verses_dict = chapters_dict[chapter_num]
            
            # Build verse array with numbers prepended
            verses = []
            for verse_num in sorted(verses_dict.keys(), key=int):
                verse_text = verses_dict[verse_num]
                # Prepend verse number
                numbered_verse = f"{verse_num} {verse_text}"
                verses.append(numbered_verse)
            
            chapters.append(verses)
            stats['verses'] += len(verses)
        
        # Create book object (use the normalized/canonical name where available)
        book_obj = {
            "name": book_name_used,
            "book_number": book_number,
            "testament": testament,
            "chapters": chapters
        }
        
        books.append(book_obj)
        
        # Update stats
        stats['books'] += 1
        stats['chapters'] += len(chapters)
        if testament == "Old":
            stats['old_testament'] += 1
        else:
            stats['new_testament'] += 1
        
        # Progress output
        testament_icon = "📜" if testament == "Old" else "✝️ "
        print(f"{testament_icon} {book_name:<20} #{book_number:<3} {len(chapters):>3} chapters  {testament} Testament")
    
    # Sort books by canonical order
    books.sort(key=lambda x: x["book_number"])
    
    # Print summary
    print("=" * 60)
    print(f"✅ Conversion Complete!")
    print(f"   📚 Total Books: {stats['books']}")
    print(f"   📜 Old Testament: {stats['old_testament']}")
    print(f"   ✝️  New Testament: {stats['new_testament']}")
    print(f"   📑 Total Chapters: {stats['chapters']}")
    print(f"   📝 Total Verses: {stats['verses']:,}")
    print()
    
    return {
        "name": bible_name,
        "books": books
    }


def load_json_file(filepath):
    """Load and parse JSON file with error handling"""
    try:
        print(f"📂 Loading: {filepath}")
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"✓ Loaded successfully\n")
        return data
    except FileNotFoundError:
        print(f"❌ Error: File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {filepath}")
        print(f"   Line {e.lineno}: {e.msg}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading file: {str(e)}")
        sys.exit(1)


def save_json_file(data, filepath, minify=False):
    """Save data to JSON file"""
    try:
        # Create directory if needed
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, "w", encoding="utf-8") as f:
            if minify:
                # Minified for production
                json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
            else:
                # Pretty print for development
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Get file size
        size_bytes = os.path.getsize(filepath)
        size_mb = size_bytes / (1024 * 1024)
        
        print(f"💾 Saved: {filepath}")
        print(f"   Size: {size_mb:.2f} MB ({size_bytes:,} bytes)")
        
    except Exception as e:
        print(f"❌ Error saving file: {str(e)}")
        sys.exit(1)


def main():
    """Main execution function"""
    
    # === CONFIGURATION ===
    INPUT_FILE = "data/input_bible.json"
    OUTPUT_FILE = "data/output_bible.json"
    BIBLE_NAME = "King James Version"
    # =====================
    
    print("\n" + "=" * 60)
    print("   BIBLE JSON CONVERTER - PRODUCTION READY")
    print("   Nested → Flat Array Structure for Flutter/Isar")
    print("=" * 60)
    
    # Check if input file exists
    if not os.path.exists(INPUT_FILE):
        print(f"\n❌ Input file not found: {INPUT_FILE}")
        print(f"   Please upload your full Bible JSON to: {INPUT_FILE}")
        print()
        sys.exit(1)
    
    # Load input
    input_data = load_json_file(INPUT_FILE)
    
    # Convert to flat array structure
    output_data = convert_to_flat_array(input_data, BIBLE_NAME)
    
    # Save output
    print("💾 Saving output file...")
    save_json_file(output_data, OUTPUT_FILE, minify=False)
    
    print("\n" + "=" * 60)
    print("🎉 CONVERSION COMPLETE!")
    print("=" * 60)
    print(f"📄 Output: {OUTPUT_FILE}")
    print()
    
    # Show sample output
    if output_data["books"]:
        first_book = output_data["books"][0]
        print("📝 Sample Output:")
        print(f"   Book: {first_book['name']}")
        print(f"   Testament: {first_book['testament']}")
        print(f"   First verse: {first_book['chapters'][0][0][:70]}...")
    
    print("\n✅ Ready for Laravel upload and Flutter integration!")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
