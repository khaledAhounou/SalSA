"""
Align imported dlls/functions to executable functionality.
"""

# list of targeted functions and their descriptions
targets = {
  'accept': 'This function is used to listen for incoming connections. This function indicates that the program will listen for incoming connections on a socket. It is mostly used by malware to communicate with their Command and Communication server.',
  'AdjustTokenPrivileges': 'This function is used to enable or disable specific access privileges. In a process injection attack, this function is used by malware to gain additional permissions.',
  'AttachThreadInput': 'This function attaches the input processing from one thread to another so that the second thread receives input events such as keyboard and mouse events. Keyloggers and other spyware use this function.',
  'bind': 'This function is used to associate a local address to a socket in order to listen for incoming connections.',
  'BitBlt': 'This function is used to copy graphic data from one device to another. Spyware sometimes uses this function to capture screenshots.',
  'CertOpenSystemStore': 'This function is used to access the certificates stored on the local system.',
  'CheckRemoteDebuggerPresent': 'Determines whether the specified process is being debugged. Used by malware to detect and evade reversing.',
  'connect': 'This function is used to connect to a remote socket. Malware often uses low-level functionality to connect to a command-and-control server. It is mostly used by malware to communicate with their Command and Communication server.',
  'ConnectNamedPipe': 'This function is used to create a server pipe for interprocess communication that will wait for a client pipe to connect. Backdoors and reverse shells sometimes use ConnectNamedPipe to simplify connectivity to a command-and-control server.',
  'ControlService': 'This function is used to start, stop, modify, or send a signal to a running service. If malware is using its own malicious service, code needs to be analyzed that implements the service in order to determine the purpose of the call.',
  'CreateFile': 'Creates a new file or opens an existing file.',
  'CreateFileMapping': 'This function is used to create a handle to a file mapping that loads a file into memory and makes it accessible via memory addresses. Launchers, loaders, and injectors use this function to read and modify PE files.',
  'CreateMutex': 'This function creates a mutual exclusion object that can be used by malware to ensure that only a single instance of the malware is running on a system at any given time. Malware often uses fixed names for mutexes, which can be good host-based indicators to detect additional installations of the malware.',
  'CreateProcess': 'This function creates and launches a new process. If malware creates a new process, new process needs to be analyzed as well.',
  'CreateRemoteThread': 'This function is used to start a thread in a remote process. Launchers and stealth malware use CreateRemoteThread to inject code into a different process.',
  'CreateService': 'This function is used to create a service that can be started at boot time. Malware uses CreateService for persistence, stealth, or to load kernel drivers.',
  'CreateToolhelp32Snapshot': 'This function is used to create a snapshot of processes, heaps, threads, and modules. Malware often uses this function as part of code that iterates through processes or threads.',
  'CryptAcquireContext': 'This function is often the first function used by malware to initialize the use of Windows encryption.',
  'DeviceIoControl': 'This function sends a control message from user space to a device driver. Kernel malware that needs to pass information between user space and kernel space often use this function.',
  'EnableExecuteProtectionSupport': 'This function is used to modify the Data Execution Protection (DEP) settings of the host, making it more susceptible to attack.',
  'EnumProcesses': 'This function is used to enumerate through running processes on the system. Malware often enumerates through processes to find a process into which to inject.',
  'EnumProcessModules': 'This function is used to enumerate the loaded modules (executables and DLLs) for a given process. Malware enumerates through modules when doing an injection.',
  'FindFirstFile': 'This function is used to search through a directory and enumerate the file system.',
  'FindNextFile': 'This function is used to search through a directory and enumerate the file system.',
  'FindResource': 'This function is used to find a resource in an executable or loaded DLL. Malware sometimes uses resources to store strings, configuration information, or other malicious files. If this function is used, then check for an .rsrc section in the malware`s PE header.',
  'FindWindow': 'This function is used to search for an open window on the desktop. Sometimes this function is used as an anti-debugging technique to search for OllyDbg windows.',
  'FtpPutFile': 'This function is used to upload a file to remote FTP server.',
  'GetAdaptersInfo': 'This function is used to obtain information about the network adapters on the system. Backdoors sometimes call GetAdaptersInfo in the information-gathering phase to gather information about infected machines. In some cases, it`s used to gather MAC addresses to check for VMware as part of anti-virtual machine techniques.',
  'GetAsyncKeyState': 'This function is used to determine whether a particular key is being pressed. Malware sometimes uses this function to implement a keylogger.',
  'GetClipboardData': 'This function is used to read user clipboard data and is sometimes used in keyloggers.',
  'GetDC': 'This function returns a handle to a device context for a window or the whole screen. Spyware that takes screen captures often uses this function.',
  'GetForegroundWindow': 'This function returns a handle to the window currently in the foreground of the desktop. Keyloggers commonly use this function to determine in which window the user is entering his keystrokes.',
  'gethostbyname': 'This function is used to perform a DNS lookup on a particular hostname prior to making an IP connection to a remote host. Hostnames that serve as command-and-control servers often make good network-based signatures.',
  'gethostname': 'This function is used to retrieve the hostname of the computer. Backdoors sometimes use gethostname in information gathering phase of the victim machine.',
  'GetKeyState': 'This function is used by keyloggers to obtain the status of a particular key on the keyboard.',
  'GetModuleFilename': 'This function returns the filename of a module that is loaded in the current process. Malware can use this function to modify or copy files in the currently running process.',
  'GetModuleHandle': 'This function is used to obtain a handle to an already loaded module. Malware may use GetModuleHandle to locate and modify code in a loaded module or to search for a good location to inject code.',
  'GetProcAddress': 'This function is used to retrieve the address of a function in a DLL loaded into memory. This is used to import functions from other DLLs in addition to the functions imported in the PE file header.',
  'GetStartupInfo': 'This function is used to retrieve a structure containing details about how the current process was configured to run, such as where the standard handles are directed.',
  'GetSystemDefaultLangId': 'This function returns the default language settings for the system. These are used by malwares by specifically designed for region-based attacks.',
  'GetTempPath': 'This function returns the temporary file path. If malware call this function, check whether it reads or writes any files in the temporary file path.',
  'GetThreadContext': 'This function returns the context structure of a given thread. The context for a thread stores all the thread information, such as the register values and current state.',
  'GetVersionEx': 'This function returns information about which version of Windows is currently running. This can be used as part of a victim survey, or to select between different offsets for undocumented structures that have changed between different versions of Windows.',
  'GetWindowDC': 'This function retrieves the device context (DC) for the entire window, including title bar, menus, and scroll bars. Used to take a screenshot of a particular GUI window (like a browser).',
  'GetWindowsDirectory': 'This function returns the file path to the Windows directory (usually C:\Windows). Malware sometimes uses this call to determine into which directory to install additional malicious programs.',
  'GetWindowText': 'This function gets the title of all program windows for the current user. Used to enumerate processes that have a GUI interface.',
  'HttpOpenRequest': 'This function sets up the OS resources for an HTTP request.',
  'HttpSendRequest': 'This function actually makes an outgoing HTTP connection.',
  'inet_addr': 'This function converts an IP address string like 127.0.0.1 so that it can be used by functions such as connect. The string specified can sometimes be used as a network-based signature.',
  'InternetOpen': 'This function initializes the high-level Internet access functions from WinINet, such as InternetOpenUrl and InternetReadFile. Searching for InternetOpen is a good way to find the start of Internet access functionality. One of the parameters to InternetOpen is the User-Agent, which can sometimes make a good network-based signature.',
  'InternetOpenUrl': 'This function opens a specific URL for a connection using FTP, HTTP, or HTTPS.URLs, if fixed, can often be good network-based signatures.',
  'InternetReadFile': 'This function reads data from a previously opened URL.',
  'InternetWriteFile': 'This function writes data to a previously opened URL.',
  'IsDebuggerPresent': 'Determines whether the calling process is being debugged by a user-mode debugger. Used by malware to detect and evade reversing.',
  'IsNTAdmin': 'This function checks if the user has administrator privileges.',
  'IsWoW64Process': 'This function is used by a 32-bit process to determine if it is running on a 64-bit operating system.',
  'LdrLoadDll': 'This is a low-level function to load a DLL into a process, just like LoadLibrary. Normal programs use LoadLibrary, and the presence of this import may indicate a program that is attempting to be stealthy.',
  'LoadLibrary': 'This is the standard fucntion to load a DLL into a process at runtime.',
  'LoadResource': 'This function loads a resource from a PE file into memory. Malware sometimes uses resources to store strings, configuration information, or other malicious files.',
  'LsaEnumerateLogonSessions': 'This function is used to enumerate through logon sessions on the current system, which can be used as part of a credential stealer.',
  'MapViewOfFile': 'This function is used to map a file into memory and makes the contents of the file accessible via memory addresses. Launchers, loaders, and injectors use this function to read and modify PE files. By using MapViewOfFile, the malware can avoid using WriteFile to modify the contents of a file.',
  'MapVirtualKey': 'This function is used to translate a virtual-key code into a character value. It is often used by keylogging malware.',
  'Module32First/Module32Next': 'This function is used to enumerate through modules loaded into a process. Injectors use this function to determine where to inject code.',
  'NetScheduleJobAdd': 'This function submits a request for a program to be run at a specified date and time. Malware can use NetScheduleJobAdd to run a different program. This is an important indicator to see the program that is scheduled to run at future time.',
  'NetShareEnum': 'This function is used to enumerate network shares.',
  'NtQueryDirectoryFile': 'This function returns information about files in a directory. Rootkits commonly hook this function in order to hide files.',
  'NtQueryInformationProcess': 'This function is used to return various information about a specified process. This function is sometimes used as an anti-debugging technique because it can return the same information as CheckRemoteDebuggerPresent.',
  'NtSetInformationProcess': 'This function is used to change the privilege level of a program or to bypass Data Execution Prevention (DEP).',
  'OpenMutex': 'This function opens a handle to a mutual exclusion object that can be used by malware to ensure that only a single instance of malware is running on a system at any given time. Malware often uses fixed names for mutexes, which can be good host-based indicators.',
  'OpenProcess': 'This function is used to open a handle to another process running on the system. This handle can be used to read and write to the other process memory or to inject code into the other process.',
  'OutputDebugString': 'This function is used to output a string to a debugger if one is attached. This can be used as an anti-debugging technique.',
  'PeekNamedPipe': 'This function is used to copy data from a named pipe without removing data from the pipe. This function is popular with reverse shells.',
  'Process32First': 'This function is used to begin enumerating processes from a previous call to CreateToolhelp32Snapshot. Malware often enumerates through processes to find a process into which to inject.',
  'Process32Next': 'This function is used to begin enumerating processes from a previous call to CreateToolhelp32Snapshot. Malware often enumerates through processes to find a process into which to inject.',
  'QueueUserAPC': 'This function is used to execute code for a different thread. Malware sometimes uses QueueUserAPC to inject code into another process.',
  'ReadProcessMemory': 'This function is used to read the memory of a remote process.',
  'recv': 'This function is used to receive data from a remote machine. Malware often uses this function to receive data from a remote command-and-control server.',
  'RegisterHotKey': 'This function is used to register a handler to be notified anytime a user enters a particular key combination (like CTRL-ALT-J), regardless of which window is active when the user presses the key combination. This function is sometimes used by spyware that remains hidden from the user until the key combination is pressed.',
  'RegOpenKey': 'This function is used to open a handle to a registry key for reading and editing. Registry keys are sometimes written as a way for software to achieve persistence on a host. The registry also contains a whole host of operating system and application setting information.',
  'ResumeThread': 'This function is used to resume a previously suspended thread. ResumeThread is used as part of several injection techniques.',
  'RtlCreateRegistryKey': 'This function is used to create a registry from kernel-mode code.',
  'RtlWriteRegistryValue': 'This function is used to write a value to the registry from kernel-mode code.',
  'SamIConnect': 'This function is used to connect to the Security Account Manager (SAM) in order to make future calls that access credential information. Hash-dumping programs access the SAM database in order to retrieve the hash of users` login passwords.',
  'SamIGetPrivateData': 'This function is used to query the private information about a specific user from the Security Account Manager (SAM) database. Hash-dumping programs access the SAM database in order to retrieve the hash of users` login passwords.',
  'SamQueryInformationUse': 'This function is used to query information about a specific user in the Security Account Manager (SAM) database. Hash-dumping programs access the SAM database in order to retrieve the hash of users` login passwords.',
  'send': 'This function is used to send data to a remote machine. It is often used by malwares to send data to a remote command-and-control server.',
  'SetFileTime': 'This function is used to modify the creation, access, or last modified time of a file. Malware often uses this function to conceal malicious activity.',
  'SetThreadContext': 'This function is used to modify the context of a given thread. Some injection techniques use SetThreadContext.',
  'SetWindowsHookEx': 'This function is used to set a hook function to be called whenever a certain event is called. Commonly used with keyloggers and spyware, this function also provides an easy way to load a DLL into all GUI processes on the system. This function is sometimes added by the compiler.',
  'SfcTerminateWatcherThread': 'This function is used to disable Windows file protection and modify files that otherwise would be protected.',
  'ShellExecute': 'This function is used to execute another program.',
  'StartServiceCtrlDispatcher': 'This function is used by a service to connect the main thread of the process to the service control manager. Any process that runs as a service must call this function within 30 seconds of startup. Locating this function in malware will tell that the function should be run as a service.',
  'SuspendThread': 'This function is used to suspend a thread so that it stops running. Malware will sometimes suspend a thread in order to modify it by performing code injection.',
  'System': 'This function is used to run another program provided by some C runtime libraries. On Windows, this function serves as a wrapper function to CreateProcess.',
  'Thread32First/Thread32Next': 'This function is used to iterate through the threads of a process. Injectors use these functions to find an appropriate thread into which to inject.',
  'Toolhelp32ReadProcessMemory': 'This function is used to read the memory of a remote process.',
  'URLDownloadToFile': 'This function is used to download a file from a web server and save it to disk. This function is popular with downloaders because it implements all the functionality of a downloader in one function call.',
  'VirtualAllocEx': 'This function is a memory-allocation routine that can allocate memory in a remote process. Malware sometimes uses VirtualAllocEx as part of process injection.',
  'VirtualProtectEx': 'This function is used to change the protection on a region of memory. Malware may use this function to change a read-only section of memory to an executable.',
  'WideCharToMultiByte': 'This function is used to convert a Unicode string into an ASCII string.',
  'WinExec': 'This function is used to execute another program.',
  'WriteProcessMemory': 'This function is used to write data to a remote process. Malware uses WriteProcessMemory as part of process injection.',
  'WSAStartup': 'This function is used to initialize low-level network functionality. Finding calls to WSAStartup can often be an easy way to locate the start of network related functionality.',
}

# constant for an unknown import by ordinal
ORDINAL_DESC = 'Ordinal is decoded at runtime. To see ordinal mapping, Download the DLL and use the parse_exports() method of the PE class.'

# common ordinal mappings that are optimized by compilers
common_ord_mappings = {
  # oleauth32.dll ordinal mapping
  'oleaut32.dll': {
    2:   'SysAllocString',
    3:   'SysReAllocString',
    4:   'SysAllocStringLen',
    5:   'SysReAllocStringLen',
    6:   'SysFreeString',
    7:   'SysStringLen',
    8:   'VariantInit',
    9:   'VariantClear',
    10:  'VariantCopy',
    11:  'VariantCopyInd',
    12:  'VariantChangeType',
    13:  'VariantTimeToDosDateTime',
    14:  'DosDateTimeToVariantTime',
    15:  'SafeArrayCreate',
    16:  'SafeArrayDestroy',
    17:  'SafeArrayGetDim',
    18:  'SafeArrayGetElemsize',
    19:  'SafeArrayGetUBound',
    20:  'SafeArrayGetLBound',
    21:  'SafeArrayLock',
    22:  'SafeArrayUnlock',
    23:  'SafeArrayAccessData',
    24:  'SafeArrayUnaccessData',
    25:  'SafeArrayGetElement',
    26:  'SafeArrayPutElement',
    27:  'SafeArrayCopy',
    28:  'DispGetParam',
    29:  'DispGetIDsOfNames',
    30:  'DispInvoke',
    31:  'CreateDispTypeInfo',
    32:  'CreateStdDispatch',
    33:  'RegisterActiveObject',
    34:  'RevokeActiveObject',
    35:  'GetActiveObject',
    36:  'SafeArrayAllocDescriptor',
    37:  'SafeArrayAllocData',
    38:  'SafeArrayDestroyDescriptor',
    39:  'SafeArrayDestroyData',
    40:  'SafeArrayRedim',
    41:  'SafeArrayAllocDescriptorEx',
    42:  'SafeArrayCreateEx',
    43:  'SafeArrayCreateVectorEx',
    44:  'SafeArraySetRecordInfo',
    45:  'SafeArrayGetRecordInfo',
    46:  'VarParseNumFromStr',
    47:  'VarNumFromParseNum',
    48:  'VarI2FromUI1',
    49:  'VarI2FromI4',
    50:  'VarI2FromR4',
    51:  'VarI2FromR8',
    52:  'VarI2FromCy',
    53:  'VarI2FromDate',
    54:  'VarI2FromStr',
    55:  'VarI2FromDisp',
    56:  'VarI2FromBool',
    57:  'SafeArraySetIID',
    58:  'VarI4FromUI1',
    59:  'VarI4FromI2',
    60:  'VarI4FromR4',
    61:  'VarI4FromR8',
    62:  'VarI4FromCy',
    63:  'VarI4FromDate',
    64:  'VarI4FromStr',
    65:  'VarI4FromDisp',
    66:  'VarI4FromBool',
    67:  'SafeArrayGetIID',
    68:  'VarR4FromUI1',
    69:  'VarR4FromI2',
    70:  'VarR4FromI4',
    71:  'VarR4FromR8',
    72:  'VarR4FromCy',
    73:  'VarR4FromDate',
    74:  'VarR4FromStr',
    75:  'VarR4FromDisp',
    76:  'VarR4FromBool',
    77:  'SafeArrayGetVartype',
    78:  'VarR8FromUI1',
    79:  'VarR8FromI2',
    80:  'VarR8FromI4',
    81:  'VarR8FromR4',
    82:  'VarR8FromCy',
    83:  'VarR8FromDate',
    84:  'VarR8FromStr',
    85:  'VarR8FromDisp',
    86:  'VarR8FromBool',
    87:  'VarFormat',
    88:  'VarDateFromUI1',
    89:  'VarDateFromI2',
    90:  'VarDateFromI4',
    91:  'VarDateFromR4',
    92:  'VarDateFromR8',
    93:  'VarDateFromCy',
    94:  'VarDateFromStr',
    95:  'VarDateFromDisp',
    96:  'VarDateFromBool',
    97:  'VarFormatDateTime',
    98:  'VarCyFromUI1',
    99:  'VarCyFromI2',
    100: 'VarCyFromI4',
    101: 'VarCyFromR4',
    102: 'VarCyFromR8',
    103: 'VarCyFromDate',
    104: 'VarCyFromStr',
    105: 'VarCyFromDisp',
    106: 'VarCyFromBool',
    107: 'VarFormatNumber',
    108: 'VarBstrFromUI1',
    109: 'VarBstrFromI2',
    110: 'VarBstrFromI4',
    111: 'VarBstrFromR4',
    112: 'VarBstrFromR8',
    113: 'VarBstrFromCy',
    114: 'VarBstrFromDate',
    115: 'VarBstrFromDisp',
    116: 'VarBstrFromBool',
    117: 'VarFormatPercent',
    118: 'VarBoolFromUI1',
    119: 'VarBoolFromI2',
    120: 'VarBoolFromI4',
    121: 'VarBoolFromR4',
    122: 'VarBoolFromR8',
    123: 'VarBoolFromDate',
    124: 'VarBoolFromCy',
    125: 'VarBoolFromStr',
    126: 'VarBoolFromDisp',
    127: 'VarFormatCurrency',
    128: 'VarWeekdayName',
    129: 'VarMonthName',
    130: 'VarUI1FromI2',
    131: 'VarUI1FromI4',
    132: 'VarUI1FromR4',
    133: 'VarUI1FromR8',
    134: 'VarUI1FromCy',
    135: 'VarUI1FromDate',
    136: 'VarUI1FromStr',
    137: 'VarUI1FromDisp',
    138: 'VarUI1FromBool',
    139: 'VarFormatFromTokens',
    140: 'VarTokenizeFormatString',
    141: 'VarAdd',
    142: 'VarAnd',
    143: 'VarDiv',
    144: 'DllCanUnloadNow',
    145: 'DllGetClassObject',
    146: 'DispCallFunc',
    147: 'VariantChangeTypeEx',
    148: 'SafeArrayPtrOfIndex',
    149: 'SysStringByteLen',
    150: 'SysAllocStringByteLen',
    151: 'DllRegisterServer',
    152: 'VarEqv',
    153: 'VarIdiv',
    154: 'VarImp',
    155: 'VarMod',
    156: 'VarMul',
    157: 'VarOr',
    158: 'VarPow',
    159: 'VarSub',
    160: 'CreateTypeLib',
    161: 'LoadTypeLib',
    162: 'LoadRegTypeLib',
    163: 'RegisterTypeLib',
    164: 'QueryPathOfRegTypeLib',
    165: 'LHashValOfNameSys',
    166: 'LHashValOfNameSysA',
    167: 'VarXor',
    168: 'VarAbs',
    169: 'VarFix',
    170: 'OaBuildVersion',
    171: 'ClearCustData',
    172: 'VarInt',
    173: 'VarNeg',
    174: 'VarNot',
    175: 'VarRound',
    176: 'VarCmp',
    177: 'VarDecAdd',
    178: 'VarDecDiv',
    179: 'VarDecMul',
    180: 'CreateTypeLib2',
    181: 'VarDecSub',
    182: 'VarDecAbs',
    183: 'LoadTypeLibEx',
    184: 'SystemTimeToVariantTime',
    185: 'VariantTimeToSystemTime',
    186: 'UnRegisterTypeLib',
    187: 'VarDecFix',
    188: 'VarDecInt',
    189: 'VarDecNeg',
    190: 'VarDecFromUI1',
    191: 'VarDecFromI2',
    192: 'VarDecFromI4',
    193: 'VarDecFromR4',
    194: 'VarDecFromR8',
    195: 'VarDecFromDate',
    196: 'VarDecFromCy',
    197: 'VarDecFromStr',
    198: 'VarDecFromDisp',
    199: 'VarDecFromBool',
    200: 'GetErrorInfo',
    201: 'SetErrorInfo',
    202: 'CreateErrorInfo',
    203: 'VarDecRound',
    204: 'VarDecCmp',
    205: 'VarI2FromI1',
    206: 'VarI2FromUI2',
    207: 'VarI2FromUI4',
    208: 'VarI2FromDec',
    209: 'VarI4FromI1',
    210: 'VarI4FromUI2',
    211: 'VarI4FromUI4',
    212: 'VarI4FromDec',
    213: 'VarR4FromI1',
    214: 'VarR4FromUI2',
    215: 'VarR4FromUI4',
    216: 'VarR4FromDec',
    217: 'VarR8FromI1',
    218: 'VarR8FromUI2',
    219: 'VarR8FromUI4',
    220: 'VarR8FromDec',
    221: 'VarDateFromI1',
    222: 'VarDateFromUI2',
    223: 'VarDateFromUI4',
    224: 'VarDateFromDec',
    225: 'VarCyFromI1',
    226: 'VarCyFromUI2',
    227: 'VarCyFromUI4',
    228: 'VarCyFromDec',
    229: 'VarBstrFromI1',
    230: 'VarBstrFromUI2',
    231: 'VarBstrFromUI4',
    232: 'VarBstrFromDec',
    233: 'VarBoolFromI1',
    234: 'VarBoolFromUI2',
    235: 'VarBoolFromUI4',
    236: 'VarBoolFromDec',
    237: 'VarUI1FromI1',
    238: 'VarUI1FromUI2',
    239: 'VarUI1FromUI4',
    240: 'VarUI1FromDec',
    241: 'VarDecFromI1',
    242: 'VarDecFromUI2',
    243: 'VarDecFromUI4',
    244: 'VarI1FromUI1',
    245: 'VarI1FromI2',
    246: 'VarI1FromI4',
    247: 'VarI1FromR4',
    248: 'VarI1FromR8',
    249: 'VarI1FromDate',
    250: 'VarI1FromCy',
    251: 'VarI1FromStr',
    252: 'VarI1FromDisp',
    253: 'VarI1FromBool',
    254: 'VarI1FromUI2',
    255: 'VarI1FromUI4',
    256: 'VarI1FromDec',
    257: 'VarUI2FromUI1',
    258: 'VarUI2FromI2',
    259: 'VarUI2FromI4',
    260: 'VarUI2FromR4',
    261: 'VarUI2FromR8',
    262: 'VarUI2FromDate',
    263: 'VarUI2FromCy',
    264: 'VarUI2FromStr',
    265: 'VarUI2FromDisp',
    266: 'VarUI2FromBool',
    267: 'VarUI2FromI1',
    268: 'VarUI2FromUI4',
    269: 'VarUI2FromDec',
    270: 'VarUI4FromUI1',
    271: 'VarUI4FromI2',
    272: 'VarUI4FromI4',
    273: 'VarUI4FromR4',
    274: 'VarUI4FromR8',
    275: 'VarUI4FromDate',
    276: 'VarUI4FromCy',
    277: 'VarUI4FromStr',
    278: 'VarUI4FromDisp',
    279: 'VarUI4FromBool',
    280: 'VarUI4FromI1',
    281: 'VarUI4FromUI2',
    282: 'VarUI4FromDec',
    283: 'BSTR_UserSize',
    284: 'BSTR_UserMarshal',
    285: 'BSTR_UserUnmarshal',
    286: 'BSTR_UserFree',
    287: 'VARIANT_UserSize',
    288: 'VARIANT_UserMarshal',
    289: 'VARIANT_UserUnmarshal',
    290: 'VARIANT_UserFree',
    291: 'LPSAFEARRAY_UserSize',
    292: 'LPSAFEARRAY_UserMarshal',
    293: 'LPSAFEARRAY_UserUnmarshal',
    294: 'LPSAFEARRAY_UserFree',
    295: 'LPSAFEARRAY_Size',
    296: 'LPSAFEARRAY_Marshal',
    297: 'LPSAFEARRAY_Unmarshal',
    298: 'VarDecCmpR8',
    299: 'VarCyAdd',
    300: 'DllUnregisterServer',
    301: 'OACreateTypeLib2',
    303: 'VarCyMul',
    304: 'VarCyMulI4',
    305: 'VarCySub',
    306: 'VarCyAbs',
    307: 'VarCyFix',
    308: 'VarCyInt',
    309: 'VarCyNeg',
    310: 'VarCyRound',
    311: 'VarCyCmp',
    312: 'VarCyCmpR8',
    313: 'VarBstrCat',
    314: 'VarBstrCmp',
    315: 'VarR8Pow',
    316: 'VarR4CmpR8',
    317: 'VarR8Round',
    318: 'VarCat',
    319: 'VarDateFromUdateEx',
    322: 'GetRecordInfoFromGuids',
    323: 'GetRecordInfoFromTypeInfo',
    325: 'SetVarConversionLocaleSetting',
    326: 'GetVarConversionLocaleSetting',
    327: 'SetOaNoCache',
    329: 'VarCyMulI8',
    330: 'VarDateFromUdate',
    331: 'VarUdateFromDate',
    332: 'GetAltMonthNames',
    333: 'VarI8FromUI1',
    334: 'VarI8FromI2',
    335: 'VarI8FromR4',
    336: 'VarI8FromR8',
    337: 'VarI8FromCy',
    338: 'VarI8FromDate',
    339: 'VarI8FromStr',
    340: 'VarI8FromDisp',
    341: 'VarI8FromBool',
    342: 'VarI8FromI1',
    343: 'VarI8FromUI2',
    344: 'VarI8FromUI4',
    345: 'VarI8FromDec',
    346: 'VarI2FromI8',
    347: 'VarI2FromUI8',
    348: 'VarI4FromI8',
    349: 'VarI4FromUI8',
    360: 'VarR4FromI8',
    361: 'VarR4FromUI8',
    362: 'VarR8FromI8',
    363: 'VarR8FromUI8',
    364: 'VarDateFromI8',
    365: 'VarDateFromUI8',
    366: 'VarCyFromI8',
    367: 'VarCyFromUI8',
    368: 'VarBstrFromI8',
    369: 'VarBstrFromUI8',
    370: 'VarBoolFromI8',
    371: 'VarBoolFromUI8',
    372: 'VarUI1FromI8',
    373: 'VarUI1FromUI8',
    374: 'VarDecFromI8',
    375: 'VarDecFromUI8',
    376: 'VarI1FromI8',
    377: 'VarI1FromUI8',
    378: 'VarUI2FromI8',
    379: 'VarUI2FromUI8',
    401: 'OleLoadPictureEx',
    402: 'OleLoadPictureFileEx',
    411: 'SafeArrayCreateVector',
    412: 'SafeArrayCopyData',
    413: 'VectorFromBstr',
    414: 'BstrFromVector',
    415: 'OleIconToCursor',
    416: 'OleCreatePropertyFrameIndirect',
    417: 'OleCreatePropertyFrame',
    418: 'OleLoadPicture',
    419: 'OleCreatePictureIndirect',
    420: 'OleCreateFontIndirect',
    421: 'OleTranslateColor',
    422: 'OleLoadPictureFile',
    423: 'OleSavePictureFile',
    424: 'OleLoadPicturePath',
    425: 'VarUI4FromI8',
    426: 'VarUI4FromUI8',
    427: 'VarI8FromUI8',
    428: 'VarUI8FromI8',
    429: 'VarUI8FromUI1',
    430: 'VarUI8FromI2',
    431: 'VarUI8FromR4',
    432: 'VarUI8FromR8',
    433: 'VarUI8FromCy',
    434: 'VarUI8FromDate',
    435: 'VarUI8FromStr',
    436: 'VarUI8FromDisp',
    437: 'VarUI8FromBool',
    438: 'VarUI8FromI1',
    439: 'VarUI8FromUI2',
    440: 'VarUI8FromUI4',
    441: 'VarUI8FromDec',
    442: 'RegisterTypeLibForUser',
    443: 'UnRegisterTypeLibForUser',
  },
  # ws2_32.dll ordinal mapping
  'ws2_32.dll': {
    1:   'accept',
    2:   'bind',
    3:   'closesocket',
    4:   'connect',
    5:   'getpeername',
    6:   'getsockname',
    7:   'getsockopt',
    8:   'htonl',
    9:   'htons',
    10:  'ioctlsocket',
    11:  'inet_addr',
    12:  'inet_ntoa',
    13:  'listen',
    14:  'ntohl',
    15:  'ntohs',
    16:  'recv',
    17:  'recvfrom',
    18:  'select',
    19:  'send',
    20:  'sendto',
    21:  'setsockopt',
    22:  'shutdown',
    23:  'socket',
    24:  'GetAddrInfoW',
    25:  'GetNameInfoW',
    26:  'WSApSetPostRoutine',
    27:  'FreeAddrInfoW',
    28:  'WPUCompleteOverlappedRequest',
    29:  'WSAAccept',
    30:  'WSAAddressToStringA',
    31:  'WSAAddressToStringW',
    32:  'WSACloseEvent',
    33:  'WSAConnect',
    34:  'WSACreateEvent',
    35:  'WSADuplicateSocketA',
    36:  'WSADuplicateSocketW',
    37:  'WSAEnumNameSpaceProvidersA',
    38:  'WSAEnumNameSpaceProvidersW',
    39:  'WSAEnumNetworkEvents',
    40:  'WSAEnumProtocolsA',
    41:  'WSAEnumProtocolsW',
    42:  'WSAEventSelect',
    43:  'WSAGetOverlappedResult',
    44:  'WSAGetQOSByName',
    45:  'WSAGetServiceClassInfoA',
    46:  'WSAGetServiceClassInfoW',
    47:  'WSAGetServiceClassNameByClassIdA',
    48:  'WSAGetServiceClassNameByClassIdW',
    49:  'WSAHtonl',
    50:  'WSAHtons',
    51:  'gethostbyaddr',
    52:  'gethostbyname',
    53:  'getprotobyname',
    54:  'getprotobynumber',
    55:  'getservbyname',
    56:  'getservbyport',
    57:  'gethostname',
    58:  'WSAInstallServiceClassA',
    59:  'WSAInstallServiceClassW',
    60:  'WSAIoctl',
    61:  'WSAJoinLeaf',
    62:  'WSALookupServiceBeginA',
    63:  'WSALookupServiceBeginW',
    64:  'WSALookupServiceEnd',
    65:  'WSALookupServiceNextA',
    66:  'WSALookupServiceNextW',
    67:  'WSANSPIoctl',
    68:  'WSANtohl',
    69:  'WSANtohs',
    70:  'WSAProviderConfigChange',
    71:  'WSARecv',
    72:  'WSARecvDisconnect',
    73:  'WSARecvFrom',
    74:  'WSARemoveServiceClass',
    75:  'WSAResetEvent',
    76:  'WSASend',
    77:  'WSASendDisconnect',
    78:  'WSASendTo',
    79:  'WSASetEvent',
    80:  'WSASetServiceA',
    81:  'WSASetServiceW',
    82:  'WSASocketA',
    83:  'WSASocketW',
    84:  'WSAStringToAddressA',
    85:  'WSAStringToAddressW',
    86:  'WSAWaitForMultipleEvents',
    87:  'WSCDeinstallProvider',
    88:  'WSCEnableNSProvider',
    89:  'WSCEnumProtocols',
    90:  'WSCGetProviderPath',
    91:  'WSCInstallNameSpace',
    92:  'WSCInstallProvider',
    93:  'WSCUnInstallNameSpace',
    94:  'WSCUpdateProvider',
    95:  'WSCWriteNameSpaceOrder',
    96:  'WSCWriteProviderOrder',
    97:  'freeaddrinfo',
    98:  'getaddrinfo',
    99:  'getnameinfo',
    101: 'WSAAsyncSelect',
    102: 'WSAAsyncGetHostByAddr',
    103: 'WSAAsyncGetHostByName',
    104: 'WSAAsyncGetProtoByNumber',
    105: 'WSAAsyncGetProtoByName',
    106: 'WSAAsyncGetServByPort',
    107: 'WSAAsyncGetServByName',
    108: 'WSACancelAsyncRequest',
    109: 'WSASetBlockingHook',
    110: 'WSAUnhookBlockingHook',
    111: 'WSAGetLastError',
    112: 'WSASetLastError',
    113: 'WSACancelBlockingCall',
    114: 'WSAIsBlocking',
    115: 'WSAStartup',
    116: 'WSACleanup',
    151: '__WSAFDIsSet',
    500: 'WEP',
  },
}

ALERT_FMT = """
Suspicious Imports:

\t{0}
"""

def run(peobject):
  # array to hold list of final alerts
  alerts = []
  found = []
  # search for functionality in imports list
  for dll in peobject.parse_imports():
    # loop through each function in the DLL
    for f in dll['functions']:
      name = f['name']
      # check for dll import by ordinal and try to resolve it
      if f['ordinal']:
        if dll['dll'].lower() in common_ord_mappings:
          name = common_ord_mappings[dll['dll'].lower()][f['ordinal']]
        else:
          # unknown dll with ordinal import
          found.append('[' + dll['dll'] + '] ordinal(' + hex(f['ordinal']) + '): ' + ORDINAL_DESC)
      # check for function in targets
      if name in targets:
        found.append('[' + dll['dll'] + '] ' + name + ': ' + targets[name])
  # format alert
  if found:
    alerts.append(ALERT_FMT.format('\n\t'.join(found)))
  return alerts
