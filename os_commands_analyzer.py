import re
from typing import Dict, List

class OSCommandsAnalyzer:
    def __init__(self):
        self.read_operations = {
            # Linux/Unix Read Commands
            'ls': 'List directory contents',
            'cat': 'Display file contents',
            'less': 'View file content page by page',
            'more': 'View file content page by page',
            'head': 'Display first lines of a file',
            'tail': 'Display last lines of a file',
            'grep': 'Search text patterns',
            'find': 'Search for files',
            'locate': 'Find files by name',
            'which': 'Locate a command',
            'whereis': 'Locate binary/source/man page',
            'man': 'Display manual pages',
            'info': 'Display info pages',
            'pwd': 'Print working directory',
            'whoami': 'Display current user',
            'id': 'Display user identity',
            'groups': 'Show groups user belongs to',
            'df': 'Display disk space usage',
            'du': 'Display disk usage',
            'free': 'Display memory usage',
            'top': 'Display running processes',
            'ps': 'Display process status',
            'uptime': 'Show system uptime',
            'uname': 'Display system information',
            'lscpu': 'Display CPU information',
            'lsblk': 'Display block devices',
            'lsusb': 'Display USB devices',
            'lspci': 'Display PCI devices',
            'mount': 'Display mounted filesystems',
            'date': 'Display current date and time',
            'cal': 'Display calendar',
            'history': 'Display command history',
            'env': 'Display environment variables',
            'printenv': 'Print environment variables',
            'alias': 'Display command aliases',
            'type': 'Display command type',
            'stat': 'Display file status',
            'wc': 'Word count',
            'sort': 'Sort lines',
            'uniq': 'Remove duplicate lines',
            'diff': 'Compare files',
            'cmp': 'Compare files byte by byte',
            'file': 'Determine file type',
            'strings': 'Extract printable strings',
            'hexdump': 'Display file in hexadecimal',
            'od': 'Octal dump',
            
            # Windows Read Commands
            'dir': 'List directory contents',
            'type': 'Display file contents',
            'more': 'Display file content page by page',
            'findstr': 'Search text patterns',
            'where': 'Locate a command',
            'whoami': 'Display current user',
            'systeminfo': 'Display system information',
            'wmic': 'Windows Management Instrumentation',
            'tasklist': 'Display running processes',
            'driverquery': 'Display device drivers',
            'netstat': 'Display network connections',
            'ipconfig': 'Display IP configuration',
            'route': 'Display routing table',
            'arp': 'Display ARP table',
            'hostname': 'Display computer name',
            'ver': 'Display Windows version',
            'vol': 'Display volume label',
            'tree': 'Display directory tree',
            'fc': 'Compare files',
            'comp': 'Compare files',
            'cipher': 'Display encryption information',
            'powershell': 'PowerShell get commands',
            'Get-ChildItem': 'PowerShell list directory',
            'Get-Content': 'PowerShell display file',
            'Get-Process': 'PowerShell display processes',
            'Get-Service': 'PowerShell display services',
            'Get-EventLog': 'PowerShell display event logs',
            'Get-ItemProperty': 'PowerShell display properties',
            'Test-Path': 'PowerShell test path existence',
            'Get-Command': 'PowerShell display commands'
        }
        
        self.non_read_operations = {
            # Linux/Unix Write Commands
            'touch': 'Create empty file',
            'mkdir': 'Create directory',
            'rmdir': 'Remove empty directory',
            'rm': 'Remove files/directories',
            'cp': 'Copy files/directories',
            'mv': 'Move/rename files',
            'ln': 'Create links',
            'chmod': 'Change file permissions',
            'chown': 'Change file ownership',
            'chgrp': 'Change group ownership',
            'tar': 'Archive files',
            'gzip': 'Compress files',
            'gunzip': 'Decompress files',
            'zip': 'Create zip archive',
            'unzip': 'Extract zip archive',
            'dd': 'Convert and copy files',
            'fsck': 'File system check',
            'mkfs': 'Create file system',
            'mount': 'Mount file system',
            'umount': 'Unmount file system',
            'fdisk': 'Disk partitioning',
            'parted': 'Partition manipulation',
            'useradd': 'Add user',
            'userdel': 'Delete user',
            'usermod': 'Modify user',
            'passwd': 'Change password',
            'groupadd': 'Add group',
            'groupdel': 'Delete group',
            'kill': 'Terminate processes',
            'killall': 'Kill processes by name',
            'service': 'Manage services',
            'systemctl': 'Systemd service manager',
            'init': 'System initialization',
            'shutdown': 'Shutdown system',
            'reboot': 'Reboot system',
            'halt': 'Stop system',
            'crontab': 'Schedule tasks',
            'at': 'Schedule one-time tasks',
            'batch': 'Schedule batch jobs',
            'nice': 'Set process priority',
            'renice': 'Change process priority',
            'nohup': 'Run command immune to hangups',
            'screen': 'Terminal multiplexer',
            'tmux': 'Terminal multiplexer',
            'export': 'Set environment variables',
            'unset': 'Remove environment variables',
            'alias': 'Create command aliases',
            'unalias': 'Remove command aliases',
            'source': 'Execute commands from file',
            'exec': 'Replace shell with command',
            'exit': 'Exit shell',
            'su': 'Switch user',
            'sudo': 'Execute as superuser',
            'echo': 'Display text or write to files',
            'printf': 'Format and display text',
            'read': 'Read input into variables',
            'tee': 'Read from stdin and write to stdout/files',
            'xargs': 'Build and execute command lines',
            'sed': 'Stream editor',
            'awk': 'Pattern scanning and processing',
            'cut': 'Remove sections from lines',
            'paste': 'Merge lines of files',
            'tr': 'Translate characters',
            'split': 'Split files',
            'csplit': 'Split files contextually',
            'join': 'Join lines of files',
            
            # Windows Write Commands
            'md': 'Make directory',
            'mkdir': 'Make directory',
            'rd': 'Remove directory',
            'rmdir': 'Remove directory',
            'del': 'Delete files',
            'erase': 'Delete files',
            'copy': 'Copy files',
            'xcopy': 'Copy files and directories',
            'robocopy': 'Robust file copy',
            'move': 'Move files',
            'ren': 'Rename files',
            'rename': 'Rename files',
            'attrib': 'Change file attributes',
            'icacls': 'Change file permissions',
            'takeown': 'Take ownership of files',
            'cipher': 'Encrypt/decrypt files',
            'format': 'Format disk',
            'diskpart': 'Disk partitioning',
            'chkdsk': 'Check disk',
            'defrag': 'Defragment disk',
            'compact': 'Compress files',
            'expand': 'Extract files',
            'extract': 'Extract files',
            'makecab': 'Create cabinet files',
            'expand': 'Extract cabinet files',
            'reg': 'Registry operations',
            'regedit': 'Registry editor',
            'schtasks': 'Schedule tasks',
            'at': 'Schedule tasks',
            'net': 'Network operations',
            'net user': 'User management',
            'net localgroup': 'Group management',
            'net share': 'Share management',
            'net use': 'Network connections',
            'net start': 'Start services',
            'net stop': 'Stop services',
            'sc': 'Service control',
            'taskkill': 'Terminate processes',
            'shutdown': 'Shutdown/reboot system',
            'logoff': 'Log off user',
            'runas': 'Run as different user',
            'powershell': 'PowerShell set commands',
            'Set-Content': 'PowerShell write to file',
            'New-Item': 'PowerShell create item',
            'Remove-Item': 'PowerShell remove item',
            'Copy-Item': 'PowerShell copy item',
            'Move-Item': 'PowerShell move item',
            'Rename-Item': 'PowerShell rename item',
            'Set-ItemProperty': 'PowerShell set properties',
            'Start-Process': 'PowerShell start process',
            'Stop-Process': 'PowerShell stop process',
            'Start-Service': 'PowerShell start service',
            'Stop-Service': 'PowerShell stop service',
            'New-Service': 'PowerShell create service',
            'Remove-Service': 'PowerShell remove service',
            'Enable-Service': 'PowerShell enable service',
            'Disable-Service': 'PowerShell disable service',
            'Set-ExecutionPolicy': 'PowerShell execution policy',
            'Register-ScheduledTask': 'PowerShell schedule task',
            'Unregister-ScheduledTask': 'PowerShell remove scheduled task'
        }
        
        self.admin_operations = {
            # Linux/Unix Admin Commands
            'sudo': 'Execute as superuser',
            'su': 'Switch to superuser',
            'visudo': 'Edit sudoers file',
            'passwd': 'Change user password',
            'useradd': 'Add new user',
            'userdel': 'Delete user',
            'usermod': 'Modify user account',
            'groupadd': 'Add new group',
            'groupdel': 'Delete group',
            'chmod': 'Change file permissions',
            'chown': 'Change file ownership',
            'chgrp': 'Change group ownership',
            'iptables': 'Configure firewall rules',
            'ufw': 'Uncomplicated Firewall',
            'firewalld': 'Firewall management',
            'systemctl': 'Systemd service manager',
            'service': 'System V service manager',
            'init': 'System initialization',
            'shutdown': 'Shutdown system',
            'reboot': 'Reboot system',
            'halt': 'Stop system',
            'poweroff': 'Power off system',
            'mount': 'Mount filesystem',
            'umount': 'Unmount filesystem',
            'fsck': 'File system check',
            'mkfs': 'Create file system',
            'fdisk': 'Disk partitioning',
            'parted': 'Partition manipulation',
            'crontab': 'Schedule cron jobs',
            'at': 'Schedule one-time jobs',
            'batch': 'Schedule batch jobs',
            'sysctl': 'Configure kernel parameters',
            'dmesg': 'Print kernel messages',
            'journalctl': 'Query systemd journal',
            'kill': 'Terminate processes',
            'killall': 'Kill processes by name',
            'pkill': 'Kill processes by name/attribute',
            'nice': 'Set process priority',
            'renice': 'Change process priority',
            'nohup': 'Run command immune to hangups',
            'screen': 'Terminal multiplexer',
            'tmux': 'Terminal multiplexer',
            'tcpdump': 'Network packet analyzer',
            'netstat': 'Network statistics',
            'ss': 'Socket statistics',
            'lsof': 'List open files',
            'fuser': 'Identify processes using files',
            'strace': 'Trace system calls',
            'ltrace': 'Trace library calls',
            'gdb': 'GNU debugger',
            'valgrind': 'Memory debugging tool',
            
            # Windows Admin Commands
            'runas': 'Run as different user',
            'powershell': 'PowerShell (admin mode)',
            'cmd': 'Command Prompt (admin)',
            'reg': 'Registry operations',
            'regedit': 'Registry editor',
            'gpedit': 'Group Policy Editor',
            'secpol': 'Security Policy Editor',
            'services.msc': 'Services management',
            'taskmgr': 'Task Manager',
            'compmgmt': 'Computer Management',
            'devmgmt': 'Device Manager',
            'diskmgmt': 'Disk Management',
            'perfmon': 'Performance Monitor',
            'eventvwr': 'Event Viewer',
            'lusrmgr': 'Local Users and Groups',
            'fsmgmt': 'Shared Folders',
            'wmic': 'Windows Management Instrumentation',
            'sfc': 'System File Checker',
            'dism': 'Deployment Image Servicing',
            'chkdsk': 'Check disk',
            'format': 'Format disk',
            'diskpart': 'Disk partitioning',
            'bcdedit': 'Boot Configuration Data',
            'msconfig': 'System Configuration',
            'regsvr32': 'Register DLL',
            'attrib': 'Change file attributes',
            'cipher': 'Encrypt/decrypt files',
            'takeown': 'Take ownership of files',
            'icacls': 'Change file permissions',
            'netsh': 'Network shell',
            'wevtutil': 'Event log utility',
            'Get-Process': 'Get processes (admin)',
            'Stop-Process': 'Stop processes (admin)',
            'Start-Service': 'Start service (admin)',
            'Stop-Service': 'Stop service (admin)',
            'Set-ExecutionPolicy': 'Set execution policy',
            'Enable-PSRemoting': 'Enable PowerShell remoting',
            'Disable-PSRemoting': 'Disable PowerShell remoting',
            'Register-ScheduledTask': 'Create scheduled task',
            'Unregister-ScheduledTask': 'Remove scheduled task',
            'Set-ItemProperty': 'Set registry values',
            'Remove-ItemProperty': 'Remove registry values',
            'New-ItemProperty': 'Create registry values',
            'Get-WinEvent': 'Get Windows events',
            'Clear-WinEvent': 'Clear Windows events',
            'Export-WinEvent': 'Export Windows events',
            
            # Network Admin Commands
            'ipconfig': 'IP configuration',
            'netsh': 'Network shell',
            'route': 'Routing table',
            'arp': 'ARP table',
            'netstat': 'Network connections',
            'tcpdump': 'Packet capture',
            'nmap': 'Network scanner',
            'ping': 'Ping test',
            'traceroute': 'Trace route',
            'nslookup': 'DNS lookup',
            'dig': 'DNS lookup',
            'host': 'DNS lookup',
            'ssh': 'Secure shell',
            'scp': 'Secure copy',
            'rsync': 'Remote sync',
            'wget': 'Download files',
            'curl': 'Transfer data',
            'iptables': 'Firewall rules',
            'ufw': 'Uncomplicated firewall',
            'firewalld': 'Firewall management',
            
            # Security Admin Commands
            'openssl': 'OpenSSL toolkit',
            'gpg': 'GNU Privacy Guard',
            'ssh-keygen': 'SSH key generator',
            'ssh-copy-id': 'Copy SSH keys',
            'fail2ban': 'Ban intrusion detection',
            'selinux': 'Security-Enhanced Linux',
            'apparmor': 'AppArmor security',
            'auditd': 'Audit daemon',
            'ausearch': 'Audit search',
            'aureport': 'Audit report',
            'last': 'Show last logins',
            'lastlog': 'Show last login info',
            'who': 'Who is logged in',
            'w': 'Who is logged in and what they are doing',
            'uptime': 'System uptime',
            'free': 'Memory usage',
            'vmstat': 'Virtual memory statistics',
            'iostat': 'I/O statistics',
            'sar': 'System activity reporter',
            'mpstat': 'Processor statistics',
            'numastat': 'NUMA statistics',
            'slabtop': 'Kernel slab cache',
            'procinfo': 'Process information'
        }
    
    def analyze_text_for_os_commands(self, text: str) -> Dict[str, List[str]]:
        """Analyze text to find OS commands and categorize them"""
        found_read_ops = []
        found_non_read_ops = []
        
        # Convert to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # Check for read operations
        for op in self.read_operations.keys():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(op.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_read_ops.append(f"{op} - {self.read_operations[op]}")
        
        # Check for non-read operations  
        for op in self.non_read_operations.keys():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(op.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_non_read_ops.append(f"{op} - {self.non_read_operations[op]}")
        
        return {
            'read_operations': found_read_ops,
            'non_read_operations': found_non_read_ops
        }
    
    def analyze_text_for_admin_commands(self, text: str) -> List[str]:
        """Analyze text to find admin commands"""
        found_admin_ops = []
        
        # Convert to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # Check for admin operations
        for op in self.admin_operations.keys():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(op.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_admin_ops.append(f"{op} - {self.admin_operations[op]}")
        
        return found_admin_ops
    
    def get_command_summary(self) -> Dict[str, Dict[str, str]]:
        """Get complete summary of all OS commands"""
        return {
            'read_operations': self.read_operations,
            'non_read_operations': self.non_read_operations,
            'admin_operations': self.admin_operations
        }
    
    def categorize_command(self, command: str) -> str:
        """Categorize a single command as read, non-read, or admin"""
        command_lower = command.lower().strip()
        
        for read_op in self.read_operations.keys():
            if command_lower == read_op.lower():
                return 'read'
        
        for non_read_op in self.non_read_operations.keys():
            if command_lower == non_read_op.lower():
                return 'non-read'
        
        for admin_op in self.admin_operations.keys():
            if command_lower == admin_op.lower():
                return 'admin'
        
        return 'unknown'
    
    def get_commands_by_os(self, os_type: str = 'all') -> Dict[str, Dict[str, str]]:
        """Get commands filtered by operating system"""
        if os_type.lower() == 'linux':
            return {
                'read_operations': {k: v for k, v in self.read_operations.items() 
                                 if not any(cmd in k for cmd in ['Get-', 'Set-', 'New-', 'Remove-', 'Start-', 'Stop-', 'Enable-', 'Disable-', 'Test-', 'Register-', 'Unregister-'])},
                'non_read_operations': {k: v for k, v in self.non_read_operations.items() 
                                     if not any(cmd in k for cmd in ['Get-', 'Set-', 'New-', 'Remove-', 'Start-', 'Stop-', 'Enable-', 'Disable-', 'Test-', 'Register-', 'Unregister-'])},
                'admin_operations': {k: v for k, v in self.admin_operations.items() 
                                  if not any(cmd in k for cmd in ['Get-', 'Set-', 'New-', 'Remove-', 'Start-', 'Stop-', 'Enable-', 'Disable-', 'Test-', 'Register-', 'Unregister-'])}
            }
        elif os_type.lower() == 'windows':
            return {
                'read_operations': {k: v for k, v in self.read_operations.items() 
                                 if any(cmd in k for cmd in ['dir', 'type', 'more', 'findstr', 'where', 'whoami', 'systeminfo', 'wmic', 'tasklist', 'Get-', 'Test-'])},
                'non_read_operations': {k: v for k, v in self.non_read_operations.items() 
                                     if any(cmd in k for cmd in ['md', 'mkdir', 'rd', 'rmdir', 'del', 'erase', 'copy', 'xcopy', 'robocopy', 'move', 'ren', 'rename', 'Set-', 'New-', 'Remove-', 'Start-', 'Stop-', 'Enable-', 'Disable-'])},
                'admin_operations': {k: v for k, v in self.admin_operations.items() 
                                  if any(cmd in k for cmd in ['runas', 'powershell', 'cmd', 'reg', 'regedit', 'gpedit', 'secpol', 'services.msc', 'taskmgr', 'compmgmt', 'devmgmt', 'diskmgmt', 'perfmon', 'eventvwr', 'lusrmgr', 'fsmgmt', 'wmic', 'sfc', 'dism', 'chkdsk', 'format', 'diskpart', 'bcdedit', 'msconfig', 'regsvr32', 'attrib', 'cipher', 'takeown', 'icacls', 'netsh', 'wevtutil', 'Get-', 'Set-', 'New-', 'Remove-', 'Start-', 'Stop-', 'Enable-', 'Disable-', 'Register-', 'Unregister-'])}
            }
        else:
            return self.get_command_summary()
