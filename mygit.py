import os
import hashlib
import json

def create_repo():
    # Create a folder called .mygit (like Git's .git folder)
    if os.path.exists('.mygit'):
        print("Repository already exists!")
        return False
    
    os.mkdir('.mygit')
    
    # Create an empty "staging area" file
    with open('.mygit/staging.json', 'w') as f:
        json.dump({}, f)
    
    print("Created .mygit folder - this is where we'll store our version history!")
    return True

def get_file_id(content):
    # Create a unique ID (hash) for any text content
    # This is like a fingerprint - same content = same ID
    return hashlib.sha1(content.encode()).hexdigest()

def save_file_content(filename):
    # Read the file
    with open(filename, 'r') as f:
        content = f.read()
    
    # Get unique ID for this content
    file_id = get_file_id(content)
    
    # Save the content in our .mygit folder using the ID as filename
    with open(f'.mygit/{file_id}', 'w') as f:
        f.write(content)
    
    print(f"Saved '{filename}' with ID: {file_id}")
    return file_id

def add_file(filename):
    # This is like "git add filename"
    print(f"Adding {filename} to staging area...")
    
    # Save the file content and get its ID
    file_id = save_file_content(filename)
    
    # Make sure staging.json exists
    if not os.path.exists('.mygit/staging.json'):
        with open('.mygit/staging.json', 'w') as f:
            json.dump({}, f)
    
    # Read current staging area
    with open('.mygit/staging.json', 'r') as f:
        staging = json.load(f)
    
    # Add this file to staging area
    staging[filename] = file_id
    
    # Save updated staging area
    with open('.mygit/staging.json', 'w') as f:
        json.dump(staging, f, indent=2)
    
    print(f"✓ {filename} is now staged for the next snapshot")

def show_staging():
    # Show what files are ready to be saved in next snapshot
    
    # Make sure staging.json exists
    if not os.path.exists('.mygit/staging.json'):
        with open('.mygit/staging.json', 'w') as f:
            json.dump({}, f)
    
    with open('.mygit/staging.json', 'r') as f:
        staging = json.load(f)
    
    if not staging:
        print("Nothing staged for snapshot")
    else:
        print("Files ready for next snapshot:")
        for filename, file_id in staging.items():
            print(f"  {filename} ({file_id[:8]}...)")

def commit(message):
    # This is like "git commit -m 'message'"
    print(f"Creating snapshot with message: '{message}'")
    
    # Make sure staging.json exists
    if not os.path.exists('.mygit/staging.json'):
        print("Nothing to commit - no files staged!")
        return
    
    # Read what files are staged
    with open('.mygit/staging.json', 'r') as f:
        staging = json.load(f)
    
    if not staging:
        print("Nothing to commit - no files staged!")
        return
    
    # Create a snapshot record
    import time
    snapshot = {
        'message': message,
        'timestamp': time.time(),
        'files': staging.copy()  # Copy the staged files
    }
    
    # Generate ID for this snapshot
    snapshot_content = json.dumps(snapshot, sort_keys=True)
    snapshot_id = get_file_id(snapshot_content)
    
    # Save the snapshot
    with open(f'.mygit/snapshot_{snapshot_id}', 'w') as f:
        json.dump(snapshot, f, indent=2)
    
    # Clear the staging area (files are now committed)
    with open('.mygit/staging.json', 'w') as f:
        json.dump({}, f)
    
    print(f"✓ Created snapshot {snapshot_id[:8]} - '{message}'")
    print(f"  Committed {len(staging)} file(s)")
    return snapshot_id

def show_diff(filename, version1="current", version2="staged"):
    # Show what changed between two versions of a file
    # version1/version2 can be: "current", "staged", or a snapshot_id
    
    def get_file_content(filename, version):
        if version == "current":
            # Read current file from disk
            if not os.path.exists(filename):
                return None
            with open(filename, 'r') as f:
                return f.read()
        
        elif version == "staged":
            # Read staged version
            if not os.path.exists('.mygit/staging.json'):
                return None
            with open('.mygit/staging.json', 'r') as f:
                staging = json.load(f)
            if filename not in staging:
                return None
            # Get content from stored file
            file_id = staging[filename]
            if not os.path.exists(f'.mygit/{file_id}'):
                return None
            with open(f'.mygit/{file_id}', 'r') as f:
                return f.read()
        
        else:
            # version should be a snapshot_id
            snapshot_file = f'.mygit/snapshot_{version}'
            if not os.path.exists(snapshot_file):
                return None
            with open(snapshot_file, 'r') as f:
                snapshot = json.load(f)
            if filename not in snapshot['files']:
                return None
            file_id = snapshot['files'][filename]
            if not os.path.exists(f'.mygit/{file_id}'):
                return None
            with open(f'.mygit/{file_id}', 'r') as f:
                return f.read()
    
    # Get both versions
    content1 = get_file_content(filename, version1)
    content2 = get_file_content(filename, version2)
    
    # Handle missing files
    if content1 is None and content2 is None:
        print(f"File '{filename}' not found in both versions")
        return
    elif content1 is None:
        print(f"File '{filename}' was added in {version2}")
        print(f"+ Content: {content2}")
        return
    elif content2 is None:
        print(f"File '{filename}' was deleted from {version1}")
        print(f"- Content: {content1}")
        return
    
    # Compare content
    if content1 == content2:
        print(f"No changes in '{filename}' between {version1} and {version2}")
        return
    
    print(f"Changes in '{filename}' from {version1} to {version2}:")
    print("=" * 50)
    
    # Simple line-by-line diff
    lines1 = content1.split('\n')
    lines2 = content2.split('\n')
    
    max_lines = max(len(lines1), len(lines2))
    
    for i in range(max_lines):
        line1 = lines1[i] if i < len(lines1) else ""
        line2 = lines2[i] if i < len(lines2) else ""
        
        if line1 != line2:
            if line1 and not line2:
                print(f"- {line1}")
            elif line2 and not line1:
                print(f"+ {line2}")
            elif line1 != line2:
                print(f"- {line1}")
                print(f"+ {line2}")
        else:
            print(f"  {line1}")

def get_last_snapshot_id():
    # Get the most recent snapshot ID
    snapshots = []
    for filename in os.listdir('.mygit'):
        if filename.startswith('snapshot_'):
            with open(f'.mygit/{filename}', 'r') as f:
                snapshot = json.load(f)
                snapshot['id'] = filename.replace('snapshot_', '')
                snapshots.append(snapshot)
    
    if not snapshots:
        return None
    
    # Sort by timestamp and return most recent
    snapshots.sort(key=lambda x: x['timestamp'], reverse=True)
    return snapshots[0]['id']

def show_history():
    # Show all snapshots we've created
    snapshots = []
    
    # Find all snapshot files
    for filename in os.listdir('.mygit'):
        if filename.startswith('snapshot_'):
            with open(f'.mygit/{filename}', 'r') as f:
                snapshot = json.load(f)
                snapshot['id'] = filename.replace('snapshot_', '')
                snapshots.append(snapshot)
    
    # Sort by timestamp (newest first)
    snapshots.sort(key=lambda x: x['timestamp'], reverse=True)
    
    if not snapshots:
        print("No snapshots yet")
        return
    
    print("Snapshot history:")
    for snapshot in snapshots:
        import datetime
        time_str = datetime.datetime.fromtimestamp(snapshot['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        print(f"  {snapshot['id'][:8]} - {snapshot['message']} ({time_str})")
        print(f"    Files: {', '.join(snapshot['files'].keys())}")

# Let's test it with command line interface
if __name__ == "__main__":
    import sys
    
    # Make sure we have a repository
    if not os.path.exists('.mygit'):
        create_repo()
    
    # Check what command the user wants
    if len(sys.argv) == 1:
        # No command given, show help
        print("MyGit - Simple Version Control")
        print("Commands:")
        print("  python mygit.py add <filename>     - Add file to staging")
        print("  python mygit.py commit '<message>' - Create snapshot")
        print("  python mygit.py status             - Show staging area")
        print("  python mygit.py history            - Show all snapshots")
        print("  python mygit.py diff <filename>    - Show changes vs staged")
        print("  python mygit.py diff <filename> current last - Show changes vs last commit")
        
    elif sys.argv[1] == "add":
        if len(sys.argv) != 3:
            print("Usage: python mygit.py add <filename>")
        else:
            filename = sys.argv[2]
            if os.path.exists(filename):
                add_file(filename)
            else:
                print(f"File '{filename}' not found!")
    
    elif sys.argv[1] == "commit":
        if len(sys.argv) != 3:
            print("Usage: python mygit.py commit '<message>'")
        else:
            message = sys.argv[2]
            commit(message)
    
    elif sys.argv[1] == "status":
        show_staging()
    
    elif sys.argv[1] == "history":
        show_history()
    
    elif sys.argv[1] == "diff":
        if len(sys.argv) < 3:
            print("Usage: python mygit.py diff <filename>")
            print("       python mygit.py diff <filename> current staged")
            print("       python mygit.py diff <filename> current last")
        else:
            filename = sys.argv[2]
            if len(sys.argv) == 3:
                # Default: compare current with staged
                show_diff(filename, "current", "staged")
            elif len(sys.argv) == 5 and sys.argv[4] == "last":
                # Compare current with last commit
                last_id = get_last_snapshot_id()
                if last_id:
                    show_diff(filename, "current", last_id)
                else:
                    print("No commits yet to compare with")
            else:
                version1 = sys.argv[3] if len(sys.argv) > 3 else "current"
                version2 = sys.argv[4] if len(sys.argv) > 4 else "staged"
                show_diff(filename, version1, version2)
    
    else:
        print(f"Unknown command: {sys.argv[1]}")
        print("Run 'python mygit.py' for help")