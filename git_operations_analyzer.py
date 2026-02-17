import re
import json
from typing import Dict, List, Tuple

class GitOperationsAnalyzer:
    def __init__(self):
        self.read_operations = {
            'git log': 'View commit history',
            'git status': 'Check repository status', 
            'git diff': 'View changes between commits',
            'git show': 'Show commit details',
            'git branch': 'List branches (read-only)',
            'git branch -r': 'List remote branches',
            'git remote -v': 'Show remote repositories',
            'git tag': 'List tags',
            'git log --oneline': 'Compact commit history',
            'git log --graph': 'Graphical commit history',
            'git log --stat': 'Commit history with statistics',
            'git diff --staged': 'View staged changes',
            'git diff HEAD': 'View all changes',
            'git ls-files': 'List tracked files',
            'git blame': 'Show file modification history',
            'git reflog': 'Show reference history',
            'git stash list': 'List stashes'
        }
        
        self.non_read_operations = {
            'git add': 'Stage files for commit',
            'git add -p': 'Stage specific parts of files',
            'git add -i': 'Interactive staging',
            'git commit': 'Create a new commit',
            'git commit -m': 'Commit with message',
            'git commit --amend': 'Modify last commit',
            'git branch <name>': 'Create new branch',
            'git checkout': 'Switch branches or restore files',
            'git checkout -b': 'Create and switch to new branch',
            'git merge': 'Merge branches',
            'git rebase': 'Rebase commits',
            'git rebase --abort': 'Abort rebase operation',
            'git rebase --continue': 'Continue rebase after conflicts',
            'git push': 'Push changes to remote',
            'git pull': 'Pull changes from remote',
            'git fetch': 'Fetch from remote without merging',
            'git clone': 'Clone repository',
            'git reset': 'Reset current HEAD to specified state',
            'git reset --hard': 'Hard reset (discards changes)',
            'git reset --soft': 'Soft reset (keeps changes staged)',
            'git stash': 'Stash changes',
            'git stash pop': 'Apply and remove stash',
            'git stash apply': 'Apply stash without removing',
            'git stash drop': 'Remove stash',
            'git tag <name>': 'Create tag',
            'git cherry-pick': 'Apply commits from another branch',
            'git revert': 'Create new commit that undoes previous commit',
            'git rm': 'Remove files from working directory and index',
            'git mv': 'Move or rename files',
            'git clean': 'Remove untracked files',
            'git init': 'Initialize repository',
            'git remote add': 'Add remote repository',
            'git remote remove': 'Remove remote repository'
        }
    
    def analyze_text_for_git_operations(self, text: str) -> Dict[str, List[str]]:
        """Analyze text to find Git operations and categorize them"""
        found_read_ops = []
        found_non_read_ops = []
        
        # Convert to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # Check for read operations
        for op in self.read_operations.keys():
            if op.lower() in text_lower:
                found_read_ops.append(f"{op} - {self.read_operations[op]}")
        
        # Check for non-read operations  
        for op in self.non_read_operations.keys():
            if op.lower() in text_lower:
                found_non_read_ops.append(f"{op} - {self.non_read_operations[op]}")
        
        return {
            'read_operations': found_read_ops,
            'non_read_operations': found_non_read_ops
        }
    
    def get_operation_summary(self) -> Dict[str, Dict[str, str]]:
        """Get complete summary of all Git operations"""
        return {
            'read_operations': self.read_operations,
            'non_read_operations': self.non_read_operations
        }
    
    def categorize_operation(self, operation: str) -> str:
        """Categorize a single operation as read or non-read"""
        operation_lower = operation.lower().strip()
        
        for read_op in self.read_operations.keys():
            if operation_lower.startswith(read_op.lower()):
                return 'read'
        
        for non_read_op in self.non_read_operations.keys():
            if operation_lower.startswith(non_read_op.lower()):
                return 'non-read'
        
        return 'unknown'
