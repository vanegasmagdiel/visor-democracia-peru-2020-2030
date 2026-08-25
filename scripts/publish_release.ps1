[CmdletBinding()]
param(
    [string]$PackagePath = "",
    [string]$Repo = "vanegasmagdiel/visor-democracia-peru-2020-2030",
    [string]$CandidateBranch = "codex/v2.1.0-scientific-refactor",
    [string]$Version = "2.1.0",
    [string]$OsfProjectId = $env:OSF_PROJECT_ID,
    [string]$OsfToken = $env:OSF_TOKEN,
    [switch]$UseCurrentDirectory,
    [switch]$SkipOsf,
    [switch]$PublishRelease,
    [switch]$NoPause
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$EmbeddedRepoRoot = (Resolve-Path (Join-Path $ScriptRoot "..")).Path
$ExpectedConceptDoi = "10.5281/zenodo.22080540"
$ExpectedStableDoi = "10.5281/zenodo.22080541"
$CandidateLabel = "v$Version-rc.1"
$WorkRoot = $null
$CloneRoot = $null

function Write-Step([string]$Message) {
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

function Write-Ok([string]$Message) {
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Assert-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "No se encontro '$Name' en PATH. Instale el requisito y vuelva a ejecutar."
    }
}

function Invoke-Native {
    param(
        [Parameter(Mandatory=$true)][string]$File,
        [Parameter(Mandatory=$true)][string[]]$Arguments,
        [string]$WorkingDirectory = ""
    )
    if ($WorkingDirectory) { Push-Location $WorkingDirectory }
    try {
        & $File @Arguments
        if ($LASTEXITCODE -ne 0) {
            throw "Fallo ($LASTEXITCODE): $File $($Arguments -join ' ')"
        }
    }
    finally {
        if ($WorkingDirectory) { Pop-Location }
    }
}

function Invoke-Capture {
    param(
        [Parameter(Mandatory=$true)][string]$File,
        [Parameter(Mandatory=$true)][string[]]$Arguments,
        [string]$WorkingDirectory = ""
    )
    if ($WorkingDirectory) { Push-Location $WorkingDirectory }
    try {
        $Result = (& $File @Arguments 2>$null | Out-String).Trim()
        if ($LASTEXITCODE -ne 0) { return $null }
        return $Result
    }
    finally {
        if ($WorkingDirectory) { Pop-Location }
    }
}

function Resolve-Python {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        return @{ Exe = "py"; Prefix = @("-3") }
    }
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return @{ Exe = "python"; Prefix = @() }
    }
    throw "No se encontro Python 3.11 o superior."
}

function Invoke-Python {
    param([string[]]$Arguments, [string]$WorkingDirectory = "")
    $AllArgs = @($script:Python.Prefix) + $Arguments
    Invoke-Native -File $script:Python.Exe -Arguments $AllArgs -WorkingDirectory $WorkingDirectory
}

function Find-Package {
    if ($PackagePath) {
        if (-not (Test-Path -LiteralPath $PackagePath -PathType Leaf)) {
            throw "No existe el paquete indicado: $PackagePath"
        }
        return (Resolve-Path -LiteralPath $PackagePath).Path
    }
    $Names = @(
        "visor_democracia_peru_2020_2030_v2.1.0-rc.1.zip",
        "visor-democracia-peru-2020-2030_v2.1.0-rc.1.zip"
    )
    $Folders = @(
        $EmbeddedRepoRoot,
        (Join-Path $env:USERPROFILE "Downloads"),
        (Join-Path $env:USERPROFILE "Descargas")
    ) | Select-Object -Unique
    foreach ($Folder in $Folders) {
        foreach ($Name in $Names) {
            $Candidate = Join-Path $Folder $Name
            if (Test-Path -LiteralPath $Candidate -PathType Leaf) {
                return (Resolve-Path -LiteralPath $Candidate).Path
            }
        }
    }
    $Newest = Get-ChildItem -Path $Folders -Filter "*v2.1.0*rc*.zip" -File -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($Newest) { return $Newest.FullName }
    throw "No se localizo el ZIP v2.1.0-rc.1. Use -PackagePath con la ruta completa."
}

function Find-SourceRoot([string]$ExtractRoot) {
    $Candidates = Get-ChildItem -LiteralPath $ExtractRoot -Filter "pyproject.toml" -File -Recurse
    foreach ($Item in $Candidates) {
        $Root = $Item.Directory.FullName
        if ((Test-Path (Join-Path $Root "docs\index.html")) -and
            (Test-Path (Join-Path $Root "data\model_config_v2_1.json")) -and
            (Test-Path (Join-Path $Root "CITATION.cff"))) {
            return $Root
        }
    }
    throw "El paquete no contiene una raiz valida con pyproject.toml, docs\index.html y data\model_config_v2_1.json."
}

function Confirm-Upload {
    Write-Host "Este proceso validara el paquete y publicara una rama/PR en GitHub." -ForegroundColor Yellow
    if (-not $SkipOsf) {
        Write-Host "Si proporciona GUID y token OSF, subira solo suplementos permitidos; nunca el ZIP." -ForegroundColor Yellow
    }
    if ($PublishRelease) {
        Write-Host "MODO FINAL solicitado: puede fusionar, etiquetar y crear un GitHub Release que active Zenodo." -ForegroundColor Red
    }
    $Answer = Read-Host "Escriba SI para continuar"
    if ($Answer -cne "SI") { throw "Operacion cancelada por el usuario." }
}

function Test-PackageHash([string]$ZipPath) {
    $Sidecar = "$ZipPath.sha256"
    if (-not (Test-Path -LiteralPath $Sidecar -PathType Leaf)) {
        throw "Falta el checksum lateral: $Sidecar"
    }
    $Expected = ((Get-Content -LiteralPath $Sidecar -Raw).Trim() -split "\s+")[0].ToLowerInvariant()
    if ($Expected -notmatch "^[a-f0-9]{64}$") { throw "El archivo SHA-256 tiene formato invalido." }
    $Actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $ZipPath).Hash.ToLowerInvariant()
    if ($Actual -ne $Expected) { throw "SHA-256 no coincide. Paquete rechazado antes de extraer." }
    Write-Ok "Integridad SHA-256 confirmada: $Actual"
}

function Configure-GitIdentity([string]$RepoRoot) {
    $Login = Invoke-Capture -File "gh" -Arguments @("api", "user", "--jq", ".login")
    if (-not $Login) { throw "No se pudo obtener el usuario autenticado de GitHub." }
    $Name = Invoke-Capture -File "gh" -Arguments @("api", "user", "--jq", ".name")
    if (-not $Name -or $Name -eq "null") { $Name = $Login }
    $UserId = Invoke-Capture -File "gh" -Arguments @("api", "user", "--jq", ".id")
    if (-not $UserId) { throw "No se pudo obtener el ID del usuario GitHub." }
    $Email = "${UserId}+${Login}@users.noreply.github.com"
    Invoke-Native -File "git" -Arguments @("config", "user.name", $Name) -WorkingDirectory $RepoRoot
    Invoke-Native -File "git" -Arguments @("config", "user.email", $Email) -WorkingDirectory $RepoRoot
    Invoke-Native -File "git" -Arguments @("config", "core.autocrlf", "false") -WorkingDirectory $RepoRoot
    Write-Ok "Identidad Git configurada con correo noreply; no se solicitan datos manuales."
}

function Sync-OsfFile {
    param([string]$ProjectId, [string]$Token, [string]$LocalPath, [string]$RemoteName)
    $Headers = @{ Authorization = "Bearer $Token" }
    $RootUri = "https://files.osf.io/v1/resources/$ProjectId/providers/osfstorage/"
    $Listing = Invoke-RestMethod -Method Get -Uri $RootUri -Headers $Headers
    $Existing = @($Listing.data) | Where-Object { $_.attributes.name -eq $RemoteName } | Select-Object -First 1
    if ($Existing) {
        $UploadUri = [string]$Existing.links.upload
        if ($UploadUri.StartsWith("/")) { $UploadUri = "https://files.osf.io$UploadUri" }
        Invoke-WebRequest -UseBasicParsing -Method Put -Uri $UploadUri -Headers $Headers -InFile $LocalPath -ContentType "application/octet-stream" | Out-Null
        Write-Ok "OSF versionado: $RemoteName"
    }
    else {
        $Encoded = [Uri]::EscapeDataString($RemoteName)
        $UploadUri = "$RootUri`?kind=file&name=$Encoded"
        Invoke-WebRequest -UseBasicParsing -Method Put -Uri $UploadUri -Headers $Headers -InFile $LocalPath -ContentType "application/octet-stream" | Out-Null
        Write-Ok "OSF creado: $RemoteName"
    }
}

function Sync-OsfSupplements([string]$RepoRoot, [string]$CommitSha) {
    if ($SkipOsf) {
        Write-Host "[OMITIDO] Sincronizacion OSF desactivada con -SkipOsf." -ForegroundColor Yellow
        return
    }
    if (-not $OsfProjectId) {
        $script:OsfProjectId = Read-Host "GUID OSF de cinco caracteres (Enter para omitir)"
    }
    if (-not $OsfProjectId) {
        Write-Host "[PENDIENTE] OSF no se modifico: no se proporciono GUID." -ForegroundColor Yellow
        return
    }
    if (-not $OsfToken) {
        $Secure = Read-Host "Token OSF con osf.full_write (entrada oculta)" -AsSecureString
        $Ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($Secure)
        try { $script:OsfToken = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($Ptr) }
        finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($Ptr) }
    }
    if (-not $OsfToken) { throw "No se proporciono token OSF." }

    $ManifestPath = Join-Path $WorkRoot "osf-sync-manifest_$CandidateLabel.json"
    $Manifest = [ordered]@{
        title = "Suplementos metodologicos del visor"
        model_version = $CandidateLabel
        github_commit = $CommitSha
        github_repository = "https://github.com/$Repo"
        zenodo_concept_doi = $ExpectedConceptDoi
        zenodo_stable_version_doi = $ExpectedStableDoi
        relation = "IsSupplementTo"
        generated_at = (Get-Date).ToUniversalTime().ToString("o")
        exclusion = "No repository ZIP, executable viewer, container or third-party report is uploaded to OSF."
    }
    $Manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $ManifestPath -Encoding UTF8

    $Files = [ordered]@{
        "docs\METODOLOGIA.md" = "METODOLOGIA_$CandidateLabel.md"
        "docs\PROVENANCE.md" = "PROVENANCE_$CandidateLabel.md"
        "docs\DECISION_LOG.md" = "DECISION_LOG_$CandidateLabel.md"
        "docs\AUDIT_CLOSURE_PHASES_1_7.md" = "AUDIT_CLOSURE_PHASES_1_7_$CandidateLabel.md"
        "docs\OSF_COMPLEMENT.md" = "OSF_COMPLEMENT_$CandidateLabel.md"
        "data\data_status_registry.csv" = "data_status_registry_$CandidateLabel.csv"
        "data\model_config_v2_1.json" = "model_config_$CandidateLabel.json"
        "data\peru_2025_anchor_summary.csv" = "peru_2025_anchor_summary_$CandidateLabel.csv"
        "data\parameter_elicitation_matrix.csv" = "parameter_elicitation_matrix_$CandidateLabel.csv"
        "data\post_election_evidence_2026.csv" = "post_election_evidence_2026_$CandidateLabel.csv"
        "VALIDATION_REPORT.md" = "VALIDATION_REPORT_$CandidateLabel.md"
    }
    foreach ($Pair in $Files.GetEnumerator()) {
        $Local = Join-Path $RepoRoot $Pair.Key
        if (-not (Test-Path -LiteralPath $Local -PathType Leaf)) { throw "Suplemento OSF ausente: $($Pair.Key)" }
        Sync-OsfFile -ProjectId $OsfProjectId -Token $OsfToken -LocalPath $Local -RemoteName $Pair.Value
    }
    Sync-OsfFile -ProjectId $OsfProjectId -Token $OsfToken -LocalPath $ManifestPath -RemoteName "osf-sync-manifest_$CandidateLabel.json"
    $script:OsfToken = $null
    Remove-Item Env:OSF_TOKEN -ErrorAction SilentlyContinue
    Write-Ok "OSF sincronizado sin duplicar el objeto principal de Zenodo."
}

function Test-And-Build([string]$RepoRoot) {
    Write-Step "Creando entorno reproducible y ejecutando controles"
    $Venv = Join-Path $RepoRoot ".venv"
    Invoke-Python -Arguments @("-m", "venv", $Venv)
    $VenvPython = Join-Path $Venv "Scripts\python.exe"
    Invoke-Native -File $VenvPython -Arguments @("-m", "pip", "install", "--disable-pip-version-check", "-r", "requirements.txt", "pytest") -WorkingDirectory $RepoRoot
    Invoke-Native -File $VenvPython -Arguments @("scripts\rebuild_scenarios.py") -WorkingDirectory $RepoRoot
    Invoke-Native -File $VenvPython -Arguments @("scripts\build_data_dictionary.py") -WorkingDirectory $RepoRoot
    Invoke-Native -File $VenvPython -Arguments @("scripts\sync_public_data.py") -WorkingDirectory $RepoRoot
    Invoke-Native -File $VenvPython -Arguments @("scripts\build_static_viewer.py") -WorkingDirectory $RepoRoot
    Invoke-Native -File $VenvPython -Arguments @("-m", "compileall", "-q", "app.py", "scripts", "tests") -WorkingDirectory $RepoRoot
    Invoke-Native -File $VenvPython -Arguments @("scripts\preflight_check.py") -WorkingDirectory $RepoRoot
    Invoke-Native -File $VenvPython -Arguments @("-m", "pytest", "-q") -WorkingDirectory $RepoRoot
    Invoke-Native -File $VenvPython -Arguments @("scripts\secret_scan.py") -WorkingDirectory $RepoRoot
    Invoke-Native -File $VenvPython -Arguments @("scripts\build_release_manifest.py", "--check") -WorkingDirectory $RepoRoot
    Write-Ok "Rebuild, preflight, tests, secret scan and manifest passed."
}

function Ensure-Pages {
    $Url = Invoke-Capture -File "gh" -Arguments @("api", "repos/$Repo/pages", "--jq", ".html_url")
    if ($Url) {
        Write-Ok "GitHub Pages activo: $Url"
        return
    }
    Write-Step "Activando GitHub Pages desde main/docs"
    $BodyPath = Join-Path $WorkRoot "pages.json"
    '{"source":{"branch":"main","path":"/docs"}}' | Set-Content -LiteralPath $BodyPath -Encoding ASCII
    Get-Content -LiteralPath $BodyPath -Raw | & gh api --method POST "repos/$Repo/pages" --input - | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "No se pudo activar GitHub Pages." }
    Write-Ok "GitHub Pages activado desde main/docs."
}

try {
    Write-Host "============================================================" -ForegroundColor DarkCyan
    Write-Host " VISOR DEMOCRACIA PERU - PUBLICADOR TRANSACCIONAL v2.1.0" -ForegroundColor White
    Write-Host "============================================================" -ForegroundColor DarkCyan
    Confirm-Upload

    Write-Step "Comprobando prerequisitos"
    Assert-Command "git"
    Assert-Command "gh"
    $script:Python = Resolve-Python
    Invoke-Native -File "gh" -Arguments @("auth", "status", "-h", "github.com")
    Invoke-Native -File "gh" -Arguments @("repo", "view", $Repo, "--json", "nameWithOwner,defaultBranchRef")
    Write-Ok "GitHub y repositorio accesibles."

    $Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $Documents = [Environment]::GetFolderPath("MyDocuments")
    $WorkRoot = Join-Path $Documents "visor_publicacion_$Stamp"
    New-Item -ItemType Directory -Path $WorkRoot -Force | Out-Null

    if ($UseCurrentDirectory) {
        $SourceRoot = $EmbeddedRepoRoot
        Write-Ok "Fuente local validada: $SourceRoot"
    }
    else {
        $ZipPath = Find-Package
        Write-Ok "Paquete localizado: $ZipPath"
        Test-PackageHash -ZipPath $ZipPath
        $ExtractRoot = Join-Path $WorkRoot "paquete"
        Expand-Archive -LiteralPath $ZipPath -DestinationPath $ExtractRoot -Force
        $SourceRoot = Find-SourceRoot -ExtractRoot $ExtractRoot
        Write-Ok "Raiz del producto: $SourceRoot"
    }

    Write-Step "Clonando mediante SSH para evitar restricciones de scope OAuth sobre workflows"
    $CloneRoot = Join-Path $WorkRoot "repositorio"
    Invoke-Native -File "git" -Arguments @("clone", "--filter=blob:none", "git@github.com:$Repo.git", $CloneRoot)
    Configure-GitIdentity -RepoRoot $CloneRoot
    Invoke-Native -File "git" -Arguments @("fetch", "origin", "--prune") -WorkingDirectory $CloneRoot
    $RemoteCandidate = Invoke-Capture -File "git" -Arguments @("ls-remote", "--heads", "origin", $CandidateBranch) -WorkingDirectory $CloneRoot
    if ($RemoteCandidate) {
        Invoke-Native -File "git" -Arguments @("switch", "-C", $CandidateBranch, "origin/$CandidateBranch") -WorkingDirectory $CloneRoot
        Invoke-Native -File "git" -Arguments @("merge", "--ff-only", "origin/main") -WorkingDirectory $CloneRoot
    }
    else {
        Invoke-Native -File "git" -Arguments @("switch", "-c", $CandidateBranch, "origin/main") -WorkingDirectory $CloneRoot
    }

    Write-Step "Superponiendo el paquete en el clon validado"
    & robocopy $SourceRoot $CloneRoot /MIR /XD .git .venv .pytest_cache __pycache__ /XF "*.zip" "*.zip.sha256" | Out-Host
    if ($LASTEXITCODE -ge 8) { throw "Robocopy fallo con codigo $LASTEXITCODE." }
    Test-And-Build -RepoRoot $CloneRoot

    Write-Step "Creando commit candidato y publicando la rama"
    Invoke-Native -File "git" -Arguments @("add", "-A") -WorkingDirectory $CloneRoot
    $Staged = Invoke-Capture -File "git" -Arguments @("diff", "--cached", "--name-only") -WorkingDirectory $CloneRoot
    if ($Staged) {
        Invoke-Native -File "git" -Arguments @("commit", "-m", "Scientific refactor v2.1.0-rc.1: phases 1-7") -WorkingDirectory $CloneRoot
    }
    else { Write-Ok "No hay cambios nuevos; se reutilizara el commit candidato existente." }
    Invoke-Native -File "git" -Arguments @("push", "-u", "origin", $CandidateBranch) -WorkingDirectory $CloneRoot
    $CommitSha = Invoke-Capture -File "git" -Arguments @("rev-parse", "HEAD") -WorkingDirectory $CloneRoot
    Write-Ok "Commit GitHub: $CommitSha"

    $PrUrl = Invoke-Capture -File "gh" -Arguments @("pr", "view", $CandidateBranch, "--repo", $Repo, "--json", "url", "--jq", ".url")
    if (-not $PrUrl) {
        $PrBody = @"
Candidate scientific refactor covering phases 1–7.

- separates the secondary-reported 2025 aggregate from latent dimensions;
- publishes bounded parameter elicitation and joint sensitivity;
- aligns CSV/XLSX/app/Pages/metadata/licensing;
- adds transactional GitHub/OSF publication automation;
- preserves v2.0.0 and its Zenodo DOI.

Publication gate: phase 8 and phases 9–11 remain pending. Do not create tag/release/DOI yet.
"@
        $PrUrl = Invoke-Capture -File "gh" -Arguments @("pr", "create", "--repo", $Repo, "--base", "main", "--head", $CandidateBranch, "--draft", "--title", "v2.1.0-rc.1: scientific refactor phases 1-7", "--body", $PrBody)
        if (-not $PrUrl) { throw "No se pudo crear el pull request borrador." }
    }
    Write-Ok "PR candidato: $PrUrl"
    Ensure-Pages
    Sync-OsfSupplements -RepoRoot $CloneRoot -CommitSha $CommitSha

    if ($PublishRelease) {
        Write-Step "Comprobando compuerta final"
        $Citation = Get-Content -LiteralPath (Join-Path $CloneRoot "CITATION.cff") -Raw
        $Notes = Get-Content -LiteralPath (Join-Path $CloneRoot "RELEASE_NOTES.md") -Raw
        if ($Citation -match "rc[.-]?1" -or $Notes -match "release candidate|candidato") {
            throw "La metadata sigue marcada como RC. Incorpore fases 8-11 y retire la marca candidata antes del release final."
        }
        $FinalAnswer = Read-Host "Para fusionar, etiquetar y activar Zenodo escriba exactamente PUBLICAR v$Version"
        if ($FinalAnswer -cne "PUBLICAR v$Version") { throw "Compuerta final no confirmada." }
        Invoke-Native -File "gh" -Arguments @("pr", "ready", $CandidateBranch, "--repo", $Repo)
        Invoke-Native -File "gh" -Arguments @("pr", "merge", $CandidateBranch, "--repo", $Repo, "--squash", "--delete-branch")
        Invoke-Native -File "git" -Arguments @("switch", "main") -WorkingDirectory $CloneRoot
        Invoke-Native -File "git" -Arguments @("pull", "--ff-only", "origin", "main") -WorkingDirectory $CloneRoot
        Test-And-Build -RepoRoot $CloneRoot
        $ExistingTag = Invoke-Capture -File "git" -Arguments @("ls-remote", "--tags", "origin", "refs/tags/v$Version") -WorkingDirectory $CloneRoot
        if ($ExistingTag) { throw "El tag v$Version ya existe; no se sobrescribe una version archivada." }
        $Archive = Join-Path $WorkRoot "visor_democracia_peru_2020_2030_v$Version.zip"
        Invoke-Native -File "git" -Arguments @("archive", "--format=zip", "--output=$Archive", "HEAD") -WorkingDirectory $CloneRoot
        $ArchiveHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $Archive).Hash.ToLowerInvariant()
        $ArchiveSidecar = "$Archive.sha256"
        "$ArchiveHash  $([IO.Path]::GetFileName($Archive))" | Set-Content -LiteralPath $ArchiveSidecar -Encoding ASCII
        Invoke-Native -File "gh" -Arguments @("release", "create", "v$Version", $Archive, $ArchiveSidecar, "--repo", $Repo, "--target", "main", "--title", "Visor Integrado de Democracia del Peru v$Version", "--notes-file", (Join-Path $CloneRoot "RELEASE_NOTES.md"))
        Write-Ok "GitHub Release creado. La integracion GitHub-Zenodo queda activada para acuñar la nueva version DOI."
    }
    else {
        Write-Host "`n[COMPuERTA] No se creo tag, GitHub Release ni DOI. Espere fase 8 y GO de fases 9-11." -ForegroundColor Yellow
    }

    Write-Host "`nRESULTADO" -ForegroundColor Cyan
    Write-Host "Directorio auditado: $WorkRoot"
    Write-Host "PR: $PrUrl"
    Write-Host "Commit: $CommitSha"
    exit 0
}
catch {
    Write-Host "`n[FALLO] $($_.Exception.Message)" -ForegroundColor Red
    if ($WorkRoot) { Write-Host "Directorio preservado para diagnostico: $WorkRoot" -ForegroundColor Yellow }
    Write-Host "No se crea ni sobrescribe un release cuando falla una compuerta." -ForegroundColor Yellow
    exit 1
}
