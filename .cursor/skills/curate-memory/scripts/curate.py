import os
import re
from datetime import datetime

# Configuration
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../_memory"))
DECISIONS_FILE = os.path.join(BASE_DIR, "DECISIONS_IN_PROGRESS.md")
ARCHIVE_DIR = os.path.join(BASE_DIR, "DECISIONS_ARCHIVE")
NOTES_DIR = os.path.join(BASE_DIR, "SESSION_NOTES")

# Statuses that trigger archiving
ARCHIVE_STATUSES = [
    "✅➡️", "❌", "✅ Validado", "❌ Rejeitado", 
    "✅ Decided", "✅ Confirmado", "✅ Resolvido",
    "🟢 Solução", "DONE"
]

def curate_decisions():
    if not os.path.exists(DECISIONS_FILE):
        print(f"File not found: {DECISIONS_FILE}")
        return

    with open(DECISIONS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    archived_items = []
    
    # Simple line-by-line archiving for tables
    in_table = False
    for line in lines:
        is_row = line.strip().startswith("|") and line.strip().endswith("|")
        
        if is_row:
            # Check if this is a header or separator row
            if "---" in line or line.lower().count("status") > 0:
                new_lines.append(line)
                continue
            
            # Check if status exists in row
            should_archive = any(status in line for status in ARCHIVE_STATUSES)
            
            if should_archive:
                archived_items.append(line.strip())
                print(f"  [Archive] {line.strip()[:50]}...")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    if archived_items:
        # Create archive file for current month
        archive_name = f"{datetime.now().strftime('%Y-%m')}_archived_decisions.md"
        archive_path = os.path.join(ARCHIVE_DIR, archive_name)
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
        
        with open(archive_path, "a", encoding="utf-8") as f:
            f.write(f"\n### Archived on {datetime.now().strftime('%Y-%m-%d')}\n")
            f.write("| ID | Topic/Hypothesis | Status | Decision/Finding | Notes |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- |\n")
            for item in archived_items:
                f.write(item + "\n")
        
        # Write back cleaned decisions file
        with open(DECISIONS_FILE, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        
        print(f"Sucessfully archived {len(archived_items)} items to {archive_name}")
    else:
        print("No items to archive.")

def curate_session_notes():
    # Logic to extract "(In Progress)" session notes and move to shared file
    # This is more complex as it involves block parsing. 
    # For now, let's focus on the decisions tracker.
    pass

if __name__ == "__main__":
    print("Running Memory Curations...")
    curate_decisions()
    print("Curation complete.")
