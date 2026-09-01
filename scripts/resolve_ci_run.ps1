[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$Repo,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-fA-F]{40}$')][string]$CommitSha,
    [string]$Workflow = "tests.yml",
    [string]$Event = "pull_request",
    [ValidateRange(5, 1800)][int]$TimeoutSeconds = 720,
    [ValidateRange(1, 60)][int]$PollSeconds = 5,
    [switch]$Quiet
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) no esta disponible."
}

$Deadline = (Get-Date).AddSeconds($TimeoutSeconds)
$ConsecutiveQueryErrors = 0
while ((Get-Date) -lt $Deadline) {
    $Output = (& gh run list --repo $Repo --workflow $Workflow --commit $CommitSha --event $Event --limit 20 --json databaseId,status,conclusion,url,createdAt 2>$null | Out-String).Trim()
    $ExitCode = $LASTEXITCODE
    if ($ExitCode -eq 0) {
        $ConsecutiveQueryErrors = 0
        if ($Output) {
            try {
                $Parsed = $Output | ConvertFrom-Json
                $Runs = if ($null -eq $Parsed) { @() } else { @($Parsed) }
                $RunIds = @()
                foreach ($Run in $Runs) {
                    $IdProperty = $Run.PSObject.Properties["databaseId"]
                    if ($null -ne $IdProperty -and $null -ne $IdProperty.Value -and ([string]$IdProperty.Value).Trim()) {
                        $RunIds += [Int64]$IdProperty.Value
                    }
                }
                if ($RunIds.Count -gt 0) {
                    $NewestRunId = $RunIds | Sort-Object -Descending | Select-Object -First 1
                    [Console]::Out.WriteLine([string]$NewestRunId)
                    exit 0
                }
            }
            catch {
                if (-not $Quiet) { Write-Host "[ESPERA] JSON de GitHub Actions aun no interpretable; reintentando..." -ForegroundColor Yellow }
            }
        }
    }
    else {
        $ConsecutiveQueryErrors += 1
        if ($ConsecutiveQueryErrors -ge 4) {
            throw "GitHub CLI no pudo consultar runs del commit en cuatro intentos consecutivos."
        }
    }
    if (-not $Quiet) { Write-Host "[ESPERA] Aun no existe un run de $Workflow/$Event para $CommitSha." -ForegroundColor Yellow }
    Start-Sleep -Seconds $PollSeconds
}
throw "No se encontro un run de $Workflow/$Event para el commit $CommitSha dentro del tiempo permitido."
