"""
Bible JSON Converter - Remove Verse Numbers
Removes verse numbering from Bible JSON files
Input: Flat array structure with verse numbers
Output: Flat array structure without verse numbers
"""

import json
import sys
import os
import re
from pathlib import Path


def remove_verse_numbers(input_data):
    """
    Remove verse numbers from Bible JSON
    
    Args:
        input_data: Dictionary with Bible data in flat array format
        
    Returns:
        Dictionary with verse numbers removed from all verses
    """
    
    bible_name = input_data.get("name", "Unknown Bible")
    books = input_data.get("books", [])
    
    stats = {
        'books': 0,
        'chapters': 0,
        'verses': 0,
        'verses_cleaned': 0
    }
    
    print(f"\n📖 Processing: {bible_name}")
    print("=" * 60)
    
    cleaned_books = []
    
    for book in books:
        book_name = book.get("name", "Unknown")
        book_number = book.get("book_number", 0)
        testament = book.get("testament", "Unknown")
        chapters = book.get("chapters", [])
        
        # Process each chapter
        cleaned_chapters = []
        for chapter in chapters:
            cleaned_verses = []
            for verse in chapter:
                stats['verses'] += 1
                
                # Remove leading verse numbers (e.g., "1 ", "2 ", "10 ", etc.)
                cleaned_verse = re.sub(r'^\d+\s+', '', verse)
                
                if cleaned_verse != verse:
                    stats['verses_cleaned'] += 1
                
                cleaned_verses.append(cleaned_verse)
            
            cleaned_chapters.append(cleaned_verses)
            stats['chapters'] += 1
        
        # Create cleaned book object
        cleaned_book = {
            "name": book_name,
            "book_number": book_number,
            "testament": testament,
            "chapters": cleaned_chapters
        }
        
        cleaned_books.append(cleaned_book)
        stats['books'] += 1
        
        # Progress output
        testament_icon = "📜" if testament == "Old" else "✝️ "
        print(f"{testament_icon} {book_name:<25} {len(cleaned_chapters):>3} chapters  {testament} Testament")
    
    # Print summary
    print("=" * 60)
    print(f"✅ Processing Complete!")
    print(f"   📚 Total Books: {stats['books']}")
    print(f"   📑 Total Chapters: {stats['chapters']}")
    print(f"   📝 Total Verses: {stats['verses']:,}")
    print(f"   🧹 Verses Cleaned: {stats['verses_cleaned']:,}")
    print()
    
    return {
        "name": bible_name,
        "books": cleaned_books
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
    
    print("\n" + "=" * 60)
    print("   BIBLE JSON CONVERTER - PRODUCTION READY")
    print("   Nested → Flat Array Structure for Flutter/Isar")
    print("=" * 60)
    print()
    
    # Get input file path from user
    print("📁 Enter the input file path:")
    print("   Example: bible/ASV/ASV_bible.json")
    print("   or: bible/KJV/KJV_Bible.json")
    INPUT_FILE = input("   Path: ").strip()
    
    # Check if input file exists
    if not os.path.exists(INPUT_FILE):
        print(f"\n❌ Input file not found: {INPUT_FILE}")
        print(f"   Please check the file path and try again.")
        print()
        sys.exit(1)
    
    # Extract Bible name from filename
    filename = os.path.basename(INPUT_FILE)
    # Remove _bible.json or _Bible.json and use the prefix as name
    BIBLE_NAME = filename.replace('_bible.json', '').replace('_Bible.json', '').replace('.json', '')
    
    # Generate output filename
    input_dir = os.path.dirname(INPUT_FILE)
    OUTPUT_FILE = os.path.join(input_dir, f"{BIBLE_NAME}_clean.json")
    
    print(f"\n📖 Bible Version: {BIBLE_NAME}")
    print(f"💾 Output will be saved to: {OUTPUT_FILE}")
    print()
    
    # Load input
    input_data = load_json_file(INPUT_FILE)
    
    # Remove verse numbers from the Bible data
    output_data = remove_verse_numbers(input_data)
    
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
