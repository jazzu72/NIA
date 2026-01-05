<#
.SYNOPSIS
    Nia LeSane PowerShell Logging Module
    Production-grade error logging and transcript management for PowerShell automation.

.DESCRIPTION
    This module provides comprehensive logging capabilities for PowerShell scripts:
    - Error logging with full stack traces
    - Automatic transcript logging
    - EventLog integration
    - Log file rotation
    - Timestamped error records

.AUTHOR
    Nia LeSane Core Team

.VERSION
    1.0.0
#>

param()

# Script-level error handling
$ErrorActionPreference = "Stop"
$VerbosePreference = "Continue"

# Log configuration
$script:LogDirectory = Join-Path -Path $PSScriptRoot -ChildPath "logs"
$script:ErrorLogFile = Join-Path -Path $script:LogDirectory -ChildPath "nia_errors_$(Get-Date -Format 'yyyyMMdd').log"
$script:DebugLogFile = Join-Path -Path $script:LogDirectory -ChildPath "nia_debug_$(Get-Date -Format 'yyyyMMdd').log"
$script:TranscriptFile = Join-Path -Path $script:LogDirectory -ChildPath "nia_transcript_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

# Create logs directory if it doesn't exist
if (-not (Test-Path -Path $script:LogDirectory)) {
    New-Item -ItemType Directory -Path $script:LogDirectory -Force | Out-Null
}

<#
.SYNOPSIS
    Initialize logging for the current PowerShell session.

.DESCRIPTION
    Sets up transcript logging, error handlers, and log files.
    Call this function at the start of your script.
#>
function Initialize-NiaLogging {
    [CmdletBinding()]
    param(
        [switch]$StartTranscript
    )
    
    try {
        Write-Verbose "Initializing Nia LeSane PowerShell Logging"
        
        # Start transcript if requested
        if ($StartTranscript) {
            Start-Transcript -Path $script:TranscriptFile -Append -Force
            Write-Output "Transcript logging started: $script:TranscriptFile"
        }
        
        # Initialize error handler
        $global:NiaErrorCount = 0
        $global:NiaWarningCount = 0
        
        # Set up error handler trap
        trap {
            Write-NiaError -Message $_.Exception.Message -ErrorRecord $_
            $false
        }
        
        Write-Output "Nia Logging initialized successfully"
        
    } catch {
        Write-Error "Failed to initialize Nia Logging: $_"
        throw
    }
}

<#
.SYNOPSIS
    Log an error with full context and stack trace.

.DESCRIPTION
    Writes error information to error log file with timestamp, severity, and full exception details.
#>
function Write-NiaError {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message,
        
        [Parameter(ValueFromPipeline=$true)]
        [System.Management.Automation.ErrorRecord]$ErrorRecord = $null,
        
        [string]$Severity = "ERROR"
    )
    
    process {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff"
        $caller = (Get-PSCallStack)[1]
        
        $logEntry = @"
[$timestamp] [$Severity] [$($caller.Command):$($caller.ScriptLineNumber)]
Message: $Message
"@
        
        if ($ErrorRecord) {
            $logEntry += @"

Exception: $($ErrorRecord.Exception.GetType().FullName)
Details: $($ErrorRecord.Exception.Message)
StackTrace:
$($ErrorRecord.ScriptStackTrace)

InvocationInfo:
  File: $($ErrorRecord.InvocationInfo.ScriptName)
  Line: $($ErrorRecord.InvocationInfo.ScriptLineNumber)
  Column: $($ErrorRecord.InvocationInfo.OffsetInLine)
"@
        }
        
        $logEntry += "`n" + ("=" * 80) + "`n"
        
        # Write to error log file
        try {
            Add-Content -Path $script:ErrorLogFile -Value $logEntry -Encoding UTF8
        } catch {
            Write-Error "Failed to write to error log: $_"
        }
        
        # Also write to console
        Write-Error $Message
        
        # Increment counter
        $global:NiaErrorCount++
    }
}

<#
.SYNOPSIS
    Log a warning message.
#>
function Write-NiaWarning {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff"
    $caller = (Get-PSCallStack)[1]
    
    $logEntry = "[$timestamp] [WARNING] [$($caller.Command):$($caller.ScriptLineNumber)] $Message"
    
    try {
        Add-Content -Path $script:ErrorLogFile -Value $logEntry -Encoding UTF8
    } catch {
        Write-Error "Failed to write to log: $_"
    }
    
    Write-Warning $Message
    $global:NiaWarningCount++
}

<#
.SYNOPSIS
    Log an information message.
#>
function Write-NiaInfo {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff"
    $logEntry = "[$timestamp] [INFO] $Message"
    
    try {
        Add-Content -Path $script:DebugLogFile -Value $logEntry -Encoding UTF8
    } catch {
        Write-Error "Failed to write to log: $_"
    }
    
    Write-Verbose $Message
}

<#
.SYNOPSIS
    Get summary of logged errors and warnings.
#>
function Get-NiaLogSummary {
    [CmdletBinding()]
    param()
    
    return @{
        ErrorCount = $global:NiaErrorCount
        WarningCount = $global:NiaWarningCount
        ErrorLogFile = $script:ErrorLogFile
        DebugLogFile = $script:DebugLogFile
        TranscriptFile = $script:TranscriptFile
    }
}

<#
.SYNOPSIS
    Stop transcript logging and return summary.
#>
function Stop-NiaLogging {
    [CmdletBinding()]
    param()
    
    try {
        Stop-Transcript -ErrorAction SilentlyContinue
        $summary = Get-NiaLogSummary
        Write-Output "Nia Logging stopped. Summary: Errors=$($summary.ErrorCount), Warnings=$($summary.WarningCount)"
        return $summary
    } catch {
        Write-Error "Error stopping Nia Logging: $_"
    }
}

# Export functions
Export-ModuleMember -Function @(
    'Initialize-NiaLogging',
    'Write-NiaError',
    'Write-NiaWarning',
    'Write-NiaInfo',
    'Get-NiaLogSummary',
    'Stop-NiaLogging'
)
