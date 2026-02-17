import re
import json
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class KeystrokeEvent:
    command: str
    timestamp: str
    context: str
    confidence: float

class KeystrokeDetector:
    def __init__(self):
        # Common keyboard shortcuts and commands
        self.keyboard_patterns = {
            # Navigation shortcuts
            r'\bctrl\s+c\b': 'Copy',
            r'\bctrl\s+v\b': 'Paste', 
            r'\bctrl\s+x\b': 'Cut',
            r'\bctrl\s+z\b': 'Undo',
            r'\bctrl\s+y\b': 'Redo',
            r'\bctrl\s+a\b': 'Select All',
            r'\bctrl\s+s\b': 'Save',
            r'\bctrl\s+f\b': 'Find',
            r'\bctrl\s+h\b': 'Replace',
            r'\bctrl\s+w\b': 'Close',
            r'\bctrl\s+q\b': 'Quit',
            r'\bctrl\s+n\b': 'New',
            r'\bctrl\s+o\b': 'Open',
            r'\bctrl\s+p\b': 'Print',
            r'\bctrl\s+tab\b': 'Switch Window',
            r'\balt\s+tab\b': 'Switch Application',
            r'\bctrl\s+alt\s+del\b': 'Task Manager',
            r'\bctrl\s+shift\s+esc\b': 'Task Manager',
            
            # Terminal/Command Line
            r'\bctrl\s+d\b': 'EOF/Exit Terminal',
            r'\bctrl\s+l\b': 'Clear Terminal',
            r'\bctrl\s+r\b': 'Search History',
            r'\bctrl\s+g\b': 'Cancel Search',
            r'\bctrl\s+u\b': 'Clear Line',
            r'\bctrl\s+k\b': 'Clear to End',
            r'\bctrl\s+w\b': 'Delete Word',
            r'\bctrl\s+e\b': 'End of Line',
            r'\bctrl\s+a\b': 'Beginning of Line',
            
            # Editor shortcuts
            r'\bctrl\s+/\b': 'Comment/Uncomment',
            r'\bctrl\s+d\b': 'Duplicate Line',
            r'\bctrl\s+shift\s+k\b': 'Delete Line',
            r'\bctrl\s+shift\s+up\b': 'Move Line Up',
            r'\bctrl\s+shift\s+down\b': 'Move Line Down',
            r'\bctrl\s+g\b': 'Go to Line',
            r'\bctrl\s+shift\s+f\b': 'Format',
            r'\bctrl\s+shift\s+o\b': 'Recent Files',
            
            # Browser shortcuts
            r'\bctrl\s+t\b': 'New Tab',
            r'\bctrl\s+w\b': 'Close Tab',
            r'\bctrl\s+shift\s+t\b': 'Reopen Tab',
            r'\bctrl\s+r\b': 'Reload',
            r'\bctrl\s+shift\s+r\b': 'Hard Reload',
            r'\bctrl\s+h\b': 'History',
            r'\bctrl\s+j\b': 'Downloads',
            r'\bctrl\s+shift\s+j\b': 'Developer Tools',
            r'\bf5\b': 'Reload',
            r'\bf11\b': 'Fullscreen',
            r'\bf12\b': 'Developer Tools',
            
            # Function keys
            r'\bf1\b': 'Help',
            r'\bf2\b': 'Rename',
            r'\bf3\b': 'Find Next',
            r'\bf5\b': 'Refresh/Reload',
            r'\bf10\b': 'Menu',
            r'\bf11\b': 'Fullscreen',
            r'\bf12\b': 'Developer Tools',
            
            # Windows specific
            r'\bwin\s+r\b': 'Run Dialog',
            r'\bwin\s+e\b': 'File Explorer',
            r'\bwin\s+d\b': 'Show Desktop',
            r'\bwin\s+l\b': 'Lock Screen',
            r'\bwin\s+tab\b': 'Task View',
            r'\balt\s+f4\b': 'Close Window',
            r'\bprint\s+screen\b': 'Screenshot',
            r'\bsysrq\b': 'System Request',
            
            # Mac specific
            r'\bcmd\s+c\b': 'Copy (Mac)',
            r'\bcmd\s+v\b': 'Paste (Mac)',
            r'\bcmd\s+x\b': 'Cut (Mac)',
            r'\bcmd\s+z\b': 'Undo (Mac)',
            r'\bcmd\s+shift\s+z\b': 'Redo (Mac)',
            r'\bcmd\s+s\b': 'Save (Mac)',
            r'\bcmd\s+q\b': 'Quit (Mac)',
            r'\bcmd\s+w\b': 'Close (Mac)',
            r'\bcmd\s+space\b': 'Spotlight',
            r'\bcmd\s+tab\b': 'Switch App (Mac)',
            r'\bcmd\s+option\s+esc\b': 'Force Quit (Mac)',
            
            # Escape key
            r'\besc\b': 'Escape/Cancel',
            r'\bescape\b': 'Escape/Cancel',
            
            # Arrow keys
            r'\bup\s+arrow\b': 'Up Arrow',
            r'\bdown\s+arrow\b': 'Down Arrow',
            r'\bleft\s+arrow\b': 'Left Arrow',
            r'\bright\s+arrow\b': 'Right Arrow',
            r'\bpage\s+up\b': 'Page Up',
            r'\bpage\s+down\b': 'Page Down',
            r'\bhome\b': 'Home',
            r'\bend\b': 'End',
            r'\binsert\b': 'Insert',
            r'\bdelete\b': 'Delete',
            r'\bbackspace\b': 'Backspace',
            r'\benter\b': 'Enter',
            r'\breturn\b': 'Return',
            r'\bspace\b': 'Space',
            r'\btab\b': 'Tab',
            r'\bshift\s+tab\b': 'Shift+Tab',
            
            # Special keys
            r'\bcaps\s+lock\b': 'Caps Lock',
            r'\bnum\s+lock\b': 'Num Lock',
            r'\bscroll\s+lock\b': 'Scroll Lock',
            r'\bpause\b': 'Pause/Break',
        }
        
        # Command patterns (what people type)
        self.command_patterns = {
            # Basic commands
            r'\bls\b': 'List directory',
            r'\bcd\b': 'Change directory',
            r'\bpwd\b': 'Print working directory',
            r'\bmkdir\b': 'Make directory',
            r'\brmdir\b': 'Remove directory',
            r'\brm\b': 'Remove files',
            r'\bcp\b': 'Copy files',
            r'\bmv\b': 'Move files',
            r'\bcat\b': 'Display file contents',
            r'\bless\b': 'View file',
            r'\bmore\b': 'View file',
            r'\bhead\b': 'Show file beginning',
            r'\btail\b': 'Show file end',
            r'\bgrep\b': 'Search text',
            r'\bfind\b': 'Find files',
            r'\bchmod\b': 'Change permissions',
            r'\bchown\b': 'Change owner',
            r'\bkill\b': 'Kill process',
            r'\bps\b': 'Show processes',
            r'\btop\b': 'Process monitor',
            r'\bdf\b': 'Disk space',
            r'\bdu\b': 'Disk usage',
            r'\bfree\b': 'Memory usage',
            r'\buname\b': 'System info',
            r'\bwhoami\b': 'Current user',
            r'\bdate\b': 'Show date',
            r'\bclear\b': 'Clear screen',
            r'\bexit\b': 'Exit',
            r'\bquit\b': 'Quit',
            r'\bhelp\b': 'Help',
            r'\bman\b': 'Manual pages',
            
            # Windows commands
            r'\bdir\b': 'List directory (Windows)',
            r'\bcls\b': 'Clear screen (Windows)',
            r'\btype\b': 'Display file (Windows)',
            r'\bdel\b': 'Delete files (Windows)',
            r'\bcopy\b': 'Copy files (Windows)',
            r'\bmove\b': 'Move files (Windows)',
            r'\bren\b': 'Rename files (Windows)',
            r'\battrib\b': 'File attributes (Windows)',
            r'\bchkdsk\b': 'Check disk (Windows)',
            r'\bformat\b': 'Format disk (Windows)',
            r'\bipconfig\b': 'IP configuration (Windows)',
            r'\bping\b': 'Ping command',
            r'\bnetstat\b': 'Network statistics',
            r'\btasklist\b': 'Show tasks (Windows)',
            r'\btaskkill\b': 'Kill task (Windows)',
            r'\bsysteminfo\b': 'System info (Windows)',
            
            # Git commands
            r'\bgit\s+status\b': 'Git status',
            r'\bgit\s+add\b': 'Git add',
            r'\bgit\s+commit\b': 'Git commit',
            r'\bgit\s+push\b': 'Git push',
            r'\bgit\s+pull\b': 'Git pull',
            r'\bgit\s+clone\b': 'Git clone',
            r'\bgit\s+branch\b': 'Git branch',
            r'\bgit\s+checkout\b': 'Git checkout',
            r'\bgit\s+merge\b': 'Git merge',
            r'\bgit\s+rebase\b': 'Git rebase',
            r'\bgit\s+log\b': 'Git log',
            r'\bgit\s+diff\b': 'Git diff',
            r'\bgit\s+reset\b': 'Git reset',
            
            # Package managers
            r'\bapt-get\b': 'Debian package manager',
            r'\bapt\b': 'Debian package manager',
            r'\byum\b': 'RPM package manager',
            r'\bdnf\b': 'RPM package manager',
            r'\bpacman\b': 'Arch package manager',
            r'\bpip\b': 'Python package manager',
            r'\bnpm\b': 'Node.js package manager',
            r'\byarn\b': 'Node.js package manager',
            r'\bbrew\b': 'Homebrew package manager',
            r'\bchoco\b': 'Chocolatey package manager',
            
            # Editors
            r'\bvi\b': 'Vi editor',
            r'\bvim\b': 'Vim editor',
            r'\bnano\b': 'Nano editor',
            r'\bemacs\b': 'Emacs editor',
            r'\bcode\b': 'VS Code editor',
            r'\bsubl\b': 'Sublime Text',
            r'\batom\b': 'Atom editor',
            r'\bnotepad\b': 'Notepad',
            
            # Programming languages
            r'\bpython\b': 'Python interpreter',
            r'\bpython3\b': 'Python 3 interpreter',
            r'\bnode\b': 'Node.js runtime',
            r'\bnpm\b': 'Node.js package manager',
            r'\bjava\b': 'Java runtime',
            r'\bjavac\b': 'Java compiler',
            r'\bgcc\b': 'C compiler',
            r'\bg\+\+\b': 'C++ compiler',
            r'\bmake\b': 'Build tool',
            r'\bcargo\b': 'Rust package manager',
            r'\bgolang\b': 'Go language',
            
            # Docker
            r'\bdocker\b': 'Docker command',
            r'\bdocker-compose\b': 'Docker Compose',
            r'\bkubectl\b': 'Kubernetes CLI',
            
            # File extensions and patterns
            r'\.py\b': 'Python file',
            r'\.js\b': 'JavaScript file',
            r'\.html\b': 'HTML file',
            r'\.css\b': 'CSS file',
            r'\.json\b': 'JSON file',
            r'\.xml\b': 'XML file',
            r'\.txt\b': 'Text file',
            r'\.md\b': 'Markdown file',
            r'\.sh\b': 'Shell script',
            r'\.bat\b': 'Batch file',
            r'\.ps1\b': 'PowerShell script',
        }
    
    def extract_keystrokes_from_text(self, text: str) -> List[KeystrokeEvent]:
        """Extract keystroke events from text"""
        events = []
        text_lower = text.lower()
        
        # Check for keyboard shortcuts
        for pattern, action in self.keyboard_patterns.items():
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                # Get context around the match
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()
                
                events.append(KeystrokeEvent(
                    command=action,
                    timestamp="",  # Would need video timestamp analysis
                    context=context,
                    confidence=0.9
                ))
        
        # Check for typed commands
        for pattern, action in self.command_patterns.items():
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                # Get context around the match
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()
                
                events.append(KeystrokeEvent(
                    command=action,
                    timestamp="",
                    context=context,
                    confidence=0.8
                ))
        
        return events
    
    def analyze_video_content(self, video_data: Dict) -> Dict:
        """Analyze video content for keystrokes"""
        all_text = ""
        
        # Combine all text sources
        if 'title' in video_data:
            all_text += video_data['title'] + " "
        
        if 'description' in video_data:
            all_text += video_data['description'] + " "
        
        if 'summary' in video_data:
            all_text += video_data['summary'] + " "
        
        # Add comments
        if 'comments' in video_data:
            for comment in video_data['comments']:
                all_text += comment.get('text', '') + " "
        
        # Extract keystrokes
        keystrokes = self.extract_keystrokes_from_text(all_text)
        
        # Remove duplicates and sort by confidence
        unique_keystrokes = {}
        for event in keystrokes:
            key = f"{event.command}_{event.context[:50]}"
            if key not in unique_keystrokes or event.confidence > unique_keystrokes[key].confidence:
                unique_keystrokes[key] = event
        
        return {
            'total_keystrokes': len(unique_keystrokes),
            'keystroke_events': list(unique_keystrokes.values()),
            'keyboard_shortcuts': [k for k in unique_keystrokes.values() if 'ctrl' in k.command.lower() or 'cmd' in k.command.lower() or 'alt' in k.command.lower() or 'win' in k.command.lower()],
            'typed_commands': [k for k in unique_keystrokes.values() if not any(shortcut in k.command.lower() for shortcut in ['ctrl', 'cmd', 'alt', 'win', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12'])],
            'file_operations': [k for k in unique_keystrokes.values() if any(op in k.command.lower() for op in ['copy', 'paste', 'cut', 'delete', 'move', 'rename'])],
            'navigation_commands': [k for k in unique_keystrokes.values() if any(nav in k.command.lower() for nav in ['cd', 'ls', 'dir', 'find', 'search'])]
        }
    
    def get_keystroke_statistics(self, analysis_result: Dict) -> Dict:
        """Get statistics about keystrokes"""
        events = analysis_result['keystroke_events']
        
        return {
            'total_events': len(events),
            'keyboard_shortcuts': len(analysis_result['keyboard_shortcuts']),
            'typed_commands': len(analysis_result['typed_commands']),
            'file_operations': len(analysis_result['file_operations']),
            'navigation_commands': len(analysis_result['navigation_commands']),
            'most_common_commands': self._get_most_common_commands(events),
            'operating_system_hints': self._detect_operating_system(events)
        }
    
    def _get_most_common_commands(self, events: List[KeystrokeEvent]) -> List[Dict]:
        """Get most common commands"""
        command_counts = {}
        for event in events:
            command_counts[event.command] = command_counts.get(event.command, 0) + 1
        
        # Sort by count and return top 10
        sorted_commands = sorted(command_counts.items(), key=lambda x: x[1], reverse=True)
        return [{'command': cmd, 'count': count} for cmd, count in sorted_commands[:10]]
    
    def _detect_operating_system(self, events: List[KeystrokeEvent]) -> Dict:
        """Detect which operating system is being used"""
        os_indicators = {
            'Windows': ['win+', 'cmd', 'powershell', 'tasklist', 'ipconfig', 'dir', 'cls', 'notepad'],
            'Mac': ['cmd+', 'option+', 'control+', 'spotlight', 'force quit'],
            'Linux': ['ctrl+', 'alt+', 'terminal', 'bash', 'sh', 'apt', 'yum', 'dnf']
        }
        
        os_scores = {os_name: 0 for os_name in os_indicators.keys()}
        
        for event in events:
            command_lower = event.command.lower()
            context_lower = event.context.lower()
            
            for os_name, indicators in os_indicators.items():
                for indicator in indicators:
                    if indicator in command_lower or indicator in context_lower:
                        os_scores[os_name] += 1
        
        # Determine most likely OS
        if max(os_scores.values()) == 0:
            return {'detected_os': 'Unknown', 'confidence': 0.0, 'scores': os_scores}
        
        detected_os = max(os_scores, key=os_scores.get)
        confidence = os_scores[detected_os] / sum(os_scores.values())
        
        return {
            'detected_os': detected_os,
            'confidence': round(confidence, 2),
            'scores': os_scores
        }
