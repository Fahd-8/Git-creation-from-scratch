**MyGit - Simple Version Control System**

A learning project to understand how Git works by building a simplified version control system from scratch.

*Project Overview*

We're developing a simplified version control application to understand how Git is created and how it works. This is purely for educational purposes - to see the core concepts behind Git by implementing them step by step.

*Implementation Steps*

<!-- Step 1: Basic Foundation -->
Create a folder to store our "version history" (similar to Git's `.git` folder)

<!-- Step 2: File Storage System -->
Save file content and generate unique IDs for each file (using hashing, like Git does)

<!-- Step 3: Staging Area -->
Keep track of what files we want to save (implementing Git's "staging area" concept)

<!-- Step 4: Commit System -->
Create snapshots (commits) of our staged files with commit messages

*Usage Examples*

**Basic Command Structure**

```bash
# See available commands
python mygit.py

# Add files to staging
python mygit.py add test.txt
python mygit.py add file2.txt

# Check what's staged
python mygit.py status

# Create a snapshot
python mygit.py commit "My first commit"

# See history
python mygit.py history
```

### Complete Workflow Example
```bash
# Add more files and commit again
echo "New content" > file3.txt
python mygit.py add file3.txt
python mygit.py commit "Added file3"
python mygit.py history
```

## How It Compares to Real Git

### Core Similarities ✓
- **Command line interface**: When you type `git add file.txt`, Git's program reads your command and calls its internal "add" function - just like our script does
- **Functions doing the work**: Git has thousands of functions, but the core concepts are the same:
  - `git add` → calls Git's staging function
  - `git commit` → calls Git's commit function  
  - `git status` → calls Git's status function
- **File storage**: Git stores everything in `.git/` folder (we use `.mygit/`), using hashes for file IDs, just like we do

### What We've Implemented
- ✓ Hash files for unique IDs
- ✓ Stage files before committing
- ✓ Create snapshots with messages
- ✓ Store everything in a hidden folder

### Main Differences from Real Git

| Aspect | Real Git | Our MyGit |
|--------|----------|-----------|
| **Scale** | Handles millions of files, complex merging, networking | Simple file tracking |
| **Optimization** | Compresses files, efficient storage algorithms | Basic storage |
| **Features** | Branches, remotes, merging, diffing, etc. | Basic add/commit/status |
| **Language** | Written in C (faster performance) | Python (easier to understand) |

## Key Concepts Learned

1. **Version Control Architecture**: The fundamental structure is the same as Git
2. **Hashing**: Using unique IDs to track file versions
3. **Staging**: Preparing files before creating commits
4. **Snapshots**: Capturing the state of files at specific points in time
5. **Command Interface**: How version control systems process user commands

## Conclusion

You've built a real (simplified) version control system! The architecture is identical to Git - the main difference is that Git has many more features and optimizations. This project demonstrates that version control systems, while complex in their full implementations, are built on relatively simple core concepts.

The foundation you've created could be extended with additional features like:
- Branching and merging
- Remote repositories
- File diffing
- Conflict resolution
- And much more...

This hands-on approach provides a solid understanding of how Git and other version control systems work under the hood.