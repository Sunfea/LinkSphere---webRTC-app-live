"""
Database Schema Fixer
Adds missing columns to the rooms table
"""
import sqlite3

db_path = "backend/test.db"

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔧 Fixing database schema...")
    
    # Check current schema
    cursor.execute("PRAGMA table_info(rooms)")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"Current columns: {columns}")
    
    # Add missing columns if they don't exist
    if 'name' not in columns:
        print("  Adding 'name' column...")
        cursor.execute("ALTER TABLE rooms ADD COLUMN name TEXT")
        print("  ✅ Added 'name' column")
    else:
        print("  ℹ️ 'name' column already exists")
    
    if 'description' not in columns:
        print("  Adding 'description' column...")
        cursor.execute("ALTER TABLE rooms ADD COLUMN description TEXT")
        print("  ✅ Added 'description' column")
    else:
        print("  ℹ️ 'description' column already exists")
    
    conn.commit()
    
    # Verify new schema
    cursor.execute("PRAGMA table_info(rooms)")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"\n✅ Updated columns: {columns}")
    
    conn.close()
    print("\n🎉 Database schema fixed successfully!")
    print("Now restart the server to apply changes.")
    
except Exception as e:
    print(f"❌ Error: {e}")
