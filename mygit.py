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

# Let's test it
if __name__ == "__main__":
    create_repo()
    
    # Check if test.txt exists and add it to staging
    if os.path.exists('test.txt'):
        print("\nFound test.txt! Adding it to staging area...")
        add_file('test.txt')
        print("\nStaging area status:")
        show_staging()
        print("\nCreating first snapshot...")
        commit("My first snapshot!")
        print("\nHistory:")
        show_history()
    else:
        print("\nPlease create test.txt with some content first!")
        print("Example: echo 'Hello World!' > test.txt")
        print("Then run this script again.")