[CmdletBinding()]
param(
    [string]$PackagePath = "",
    [string]$Repo = "vanegasmagdiel/visor-democracia-peru-2020-2030",
    [string]$CandidateBranch = "codex/v2.1.0-rc.5-technical-refactor",
    [string]$Version = "2.1.0",
    [ValidatePattern('^rc\.\d+$')][string]$CandidateRc = "rc.5",
    [string]$OsfProjectId = $env:OSF_PROJECT_ID,
    [string]$OsfToken = $env:OSF_TOKEN,
    [switch]$UseCurrentDirectory,
    [switch]$SkipOsf,
    [switch]$DryRun,
    [switch]$PublishRelease,
    [switch]$NoPause
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$EmbeddedRepoRoot = (Resolve-Path (Join-Path $ScriptRoot "..")).Path
$ExpectedConceptDoi = "10.5281/zenodo.22080540"
$ExpectedPreviousVersionDoi = "10.5281/zenodo.22080541"
$CandidateLabel = "v$Version-$CandidateRc"
$ArtifactLabel = if ($PublishRelease) { "v$Version" } else { $CandidateLabel }
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
        return @{ Exe = "py"; Prefix = @("-3.12") }
    }
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return @{ Exe = "python"; Prefix = @() }
    }
    throw "No se encontro Python 3.12."
}

function Invoke-Python {
    param([string[]]$Arguments, [string]$WorkingDirectory = "")
    $AllArgs = @($script:Python.Prefix) + $Arguments
    Invoke-Native -File $script:Python.Exe -Arguments $AllArgs -WorkingDirectory $WorkingDirectory
}

function Assert-Python312 {
    $Version = Invoke-Capture -File $script:Python.Exe -Arguments (@($script:Python.Prefix) + @("-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"))
    if ($Version -ne "3.12") {
        throw "El entorno reproducible exige Python 3.12; se detecto $Version."
    }
    Write-Ok "Python 3.12 confirmado."
}


function Configure-GitHubHttpsTransport {
    Write-Step "Configurando transporte Git HTTPS mediante GitHub CLI"
    Invoke-Native -File "gh" -Arguments @("auth", "setup-git", "--hostname", "github.com")
    $env:GIT_TERMINAL_PROMPT = "0"
    $HttpsRemote = "https://github.com/$Repo.git"
    $Probe = Invoke-Capture -File "git" -Arguments @("ls-remote", $HttpsRemote, "HEAD")
    if (-not $Probe) {
        throw "Git HTTPS no pudo autenticarse mediante GitHub CLI. Ejecute 'gh auth status -h github.com' y, si falta alcance para workflows, 'gh auth refresh -h github.com -s repo,workflow'."
    }
    Write-Ok "Git HTTPS autenticado mediante GitHub CLI; no se requiere clave SSH ni passphrase."
}

function Find-Package {
    if ($PackagePath) {
        if (-not (Test-Path -LiteralPath $PackagePath -PathType Leaf)) {
            throw "No existe el paquete indicado: $PackagePath"
        }
        return (Resolve-Path -LiteralPath $PackagePath).Path
    }
    $Names = @(
        "visor_democracia_peru_2020_2030_$CandidateLabel.zip",
        "visor-democracia-peru-2020-2030_$CandidateLabel.zip"
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
    throw "No se localizo el ZIP $CandidateLabel. Use -PackagePath con la ruta completa."
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
    if ($DryRun) {
        Write-Host "MODO DRY-RUN: valida y reconstruye localmente; no escribe en GitHub, Zenodo ni OSF." -ForegroundColor Green
        return
    }
    Write-Host "Este proceso validara el paquete y publicara una rama/PR en GitHub." -ForegroundColor Yellow
    if (-not $SkipOsf) {
        Write-Host "OSF es opcional. En modo candidato puede sincronizar suplementos; en modo final se intenta solo despues del GitHub Release." -ForegroundColor Yellow
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

    $ManifestPath = Join-Path $WorkRoot "osf-sync-manifest_$ArtifactLabel.json"
    $Manifest = [ordered]@{
        title = "Suplementos metodologicos del visor"
        model_version = $ArtifactLabel
        github_commit = $CommitSha
        github_repository = "https://github.com/$Repo"
        zenodo_concept_doi = $ExpectedConceptDoi
        zenodo_previous_version_doi = $ExpectedPreviousVersionDoi
        zenodo_current_version_doi_status = if ($PublishRelease) { "PENDING_ZENODO_INGEST" } else { "NOT_APPLICABLE_CANDIDATE" }
        relation = "IsSupplementTo"
        generated_at = (Get-Date).ToUniversalTime().ToString("o")
        exclusion = "No repository ZIP, executable viewer, container or third-party report is uploaded to OSF."
    }
    $Manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $ManifestPath -Encoding UTF8

    $Files = [ordered]@{
        "docs\METODOLOGIA.md" = "METODOLOGIA_$ArtifactLabel.md"
        "docs\PROVENANCE.md" = "PROVENANCE_$ArtifactLabel.md"
        "docs\DECISION_LOG.md" = "DECISION_LOG_$ArtifactLabel.md"
        "docs\AUDIT_CLOSURE_PHASES_1_7.md" = "AUDIT_CLOSURE_PHASES_1_7_$ArtifactLabel.md"
        "docs\OSF_COMPLEMENT.md" = "OSF_COMPLEMENT_$ArtifactLabel.md"
        "data\data_status_registry.csv" = "data_status_registry_$ArtifactLabel.csv"
        "data\model_config_v2_1.json" = "model_config_$ArtifactLabel.json"
        "data\peru_2025_anchor_summary.csv" = "peru_2025_anchor_summary_$ArtifactLabel.csv"
        "data\parameter_elicitation_matrix.csv" = "parameter_elicitation_matrix_$ArtifactLabel.csv"
        "data\post_election_evidence_2026.csv" = "post_election_evidence_2026_$ArtifactLabel.csv"
        "VALIDATION_REPORT.md" = "VALIDATION_REPORT_$ArtifactLabel.md"
        "docs\FASE_8_PRISMA.md" = "FASE_8_PRISMA_$ArtifactLabel.md"
        "docs\FASE_8_GATE.md" = "FASE_8_GATE_$ArtifactLabel.md"
        "docs\INFORME_METODOLOGICO_PRISMA_FASE_8_CIERRE_FULLTEXT.md" = "INFORME_METODOLOGICO_PRISMA_FASE_8_CIERRE_FULLTEXT_$ArtifactLabel.md"
        "data\prisma_phase8\phase8_manifest.json" = "phase8_manifest_$ArtifactLabel.json"
        "data\prisma_phase8\search_profiles_105.csv" = "search_profiles_105_$ArtifactLabel.csv"
        "data\prisma_phase8\exclusion_reasons_3.csv" = "exclusion_reasons_3_$ArtifactLabel.csv"
        "data\prisma_phase8\fulltext_decisions_72.csv" = "fulltext_decisions_72_$ArtifactLabel.csv"
        "data\prisma_phase8\fulltext_included_29.csv" = "fulltext_included_29_$ArtifactLabel.csv"
        "data\prisma_phase8\fulltext_excluded_13.csv" = "fulltext_excluded_13_$ArtifactLabel.csv"
        "data\prisma_phase8\fulltext_not_retrieved_30.csv" = "fulltext_not_retrieved_30_$ArtifactLabel.csv"
        "data\prisma_phase8\evidence_integration_map_29.csv" = "evidence_integration_map_29_$ArtifactLabel.csv"
        "data\prisma_phase8\Bibliografia_Incluida_Visor_Democracia_Fulltext_Final_29.ris" = "Bibliografia_Incluida_Visor_Democracia_Fulltext_Final_29_$ArtifactLabel.ris"
        "data\prisma_phase8\Libro_Analisis_PRISMA_Visor_Democracia_R4_3_5_Cierre_Fulltext.xlsx" = "Libro_Analisis_PRISMA_Visor_Democracia_Cierre_Fulltext_$ArtifactLabel.xlsx"
        "docs\assets\figura_s1_prisma_fulltext_final.png" = "Figura_S1_PRISMA_Cierre_Fulltext_$ArtifactLabel.png"
        "RELEASE_INDEPENDENCE_POLICY.md" = "RELEASE_INDEPENDENCE_POLICY_$ArtifactLabel.md"
    }
    foreach ($Pair in $Files.GetEnumerator()) {
        $Local = Join-Path $RepoRoot $Pair.Key
        if (-not (Test-Path -LiteralPath $Local -PathType Leaf)) { throw "Suplemento OSF ausente: $($Pair.Key)" }
        Sync-OsfFile -ProjectId $OsfProjectId -Token $OsfToken -LocalPath $Local -RemoteName $Pair.Value
    }
    Sync-OsfFile -ProjectId $OsfProjectId -Token $OsfToken -LocalPath $ManifestPath -RemoteName "osf-sync-manifest_$ArtifactLabel.json"
    $script:OsfToken = $null
    Remove-Item Env:OSF_TOKEN -ErrorAction SilentlyContinue
    Write-Ok "OSF sincronizado sin duplicar el objeto principal de Zenodo."
}

function Try-SyncOsfAfterRelease([string]$RepoRoot, [string]$CommitSha) {
    try {
        Sync-OsfSupplements -RepoRoot $RepoRoot -CommitSha $CommitSha
    }
    catch {
        Write-Host "[ADVERTENCIA] El GitHub Release ya fue creado, pero OSF no pudo sincronizarse: $($_.Exception.Message)" -ForegroundColor Yellow
        Write-Host "OSF es opcional y puede sincronizarse despues con el SHA final y el DOI real de Zenodo." -ForegroundColor Yellow
        $script:OsfToken = $null
        Remove-Item Env:OSF_TOKEN -ErrorAction SilentlyContinue
    }
}

function Test-And-Build([string]$RepoRoot) {
    Write-Step "Creando entorno reproducible y ejecutando controles"
    $Venv = Join-Path $RepoRoot ".venv"
    Invoke-Python -Arguments @("-m", "venv", $Venv)
    $VenvPython = Join-Path $Venv "Scripts\python.exe"
    Invoke-Native -File $VenvPython -Arguments @("-m", "pip", "install", "--disable-pip-version-check", "-r", "requirements-lock.txt") -WorkingDirectory $RepoRoot
    Invoke-Native -File $VenvPython -Arguments @("scripts\rebuild_scenarios.py") -WorkingDirectory $RepoRoot
    Invoke-Native -File $VenvPython -Arguments @("scripts\build_data_dictionary.py") -WorkingDirectory $RepoRoot
    Invoke-Native -File $VenvPython -Arguments @("scripts\sync_public_data.py") -WorkingDirectory $RepoRoot
    Invoke-Native -File $VenvPython -Arguments @("scripts\build_static_viewer.py") -WorkingDirectory $RepoRoot
    Invoke-Native -File $VenvPython -Arguments @("-m", "compileall", "-q", "app.py", "scripts", "tests") -WorkingDirectory $RepoRoot
    Invoke-Native -File $VenvPython -Arguments @("scripts\preflight_check.py") -WorkingDirectory $RepoRoot
    Invoke-Native -File $VenvPython -Arguments @("scripts\validate_phase8.py") -WorkingDirectory $RepoRoot
    Write-Step "Regenerando inventario despues del rebuild determinista"
    Invoke-Native -File $VenvPython -Arguments @("scripts\build_release_manifest.py") -WorkingDirectory $RepoRoot
    Invoke-Native -File $VenvPython -Arguments @("-m", "pytest", "-q") -WorkingDirectory $RepoRoot
    Invoke-Native -File $VenvPython -Arguments @("scripts\audit_release_independence.py") -WorkingDirectory $RepoRoot
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
    $script:Python = Resolve-Python
    Assert-Python312
    if (-not $DryRun) {
        Assert-Command "gh"
        Invoke-Native -File "gh" -Arguments @("auth", "status", "-h", "github.com")
        Invoke-Native -File "gh" -Arguments @("repo", "view", $Repo, "--json", "nameWithOwner,defaultBranchRef")
        Write-Ok "GitHub y repositorio accesibles."
    }

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

    if ($DryRun) {
        Test-And-Build -RepoRoot $SourceRoot
        $DryRunReport = Join-Path $WorkRoot "DRY_RUN_REPORT.md"
        @"
# Dry-run $CandidateLabel

- Package/source integrity: PASS
- Scientific rebuild: PASS
- Phase 8 full-text validation: PASS
- Tests and secret scan: PASS
- GitHub writes: NOT ATTEMPTED
- Zenodo writes: NOT ATTEMPTED
- OSF writes: NOT ATTEMPTED

This mode is intentionally local and non-destructive.
"@ | Set-Content -LiteralPath $DryRunReport -Encoding UTF8
        Write-Ok "Dry-run concluido sin escrituras externas: $DryRunReport"
        exit 0
    }

    Configure-GitHubHttpsTransport
    Write-Step "Clonando mediante HTTPS autenticado por GitHub CLI"
    $CloneRoot = Join-Path $WorkRoot "repositorio"
    $HttpsRemote = "https://github.com/$Repo.git"
    Invoke-Native -File "git" -Arguments @("clone", "--filter=blob:none", $HttpsRemote, $CloneRoot)
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
        Invoke-Native -File "git" -Arguments @("commit", "-m", "Technical release refactor $CandidateLabel") -WorkingDirectory $CloneRoot
    }
    else { Write-Ok "No hay cambios nuevos; se reutilizara el commit candidato existente." }
    Invoke-Native -File "git" -Arguments @("push", "-u", "origin", $CandidateBranch) -WorkingDirectory $CloneRoot
    $CommitSha = Invoke-Capture -File "git" -Arguments @("rev-parse", "HEAD") -WorkingDirectory $CloneRoot
    Write-Ok "Commit GitHub: $CommitSha"

    # `gh pr view <branch>` exits non-zero when no PR exists. Under strict/native-error
    # settings that can abort the transaction before the create path is reached.
    # `gh pr list` is intentionally used here because "no matches" is a normal empty
    # result with exit code 0.
    $PrListJson = Invoke-Capture -File "gh" -Arguments @("pr", "list", "--repo", $Repo, "--head", $CandidateBranch, "--state", "open", "--json", "url")
    $PrItems = @()
    if ($PrListJson) {
        $ParsedPrItems = $PrListJson | ConvertFrom-Json
        if ($null -ne $ParsedPrItems) {
            $PrItems = @($ParsedPrItems)
        }
    }
    if ($PrItems.Count -gt 0) {
        $PrUrl = [string]$PrItems[0].url
    }
    else {
        $PrUrl = ""
    }
    if (-not $PrUrl) {
        $PrBody = @"
Candidate scientific-software package for v2.1.0.

- separates the secondary-reported 2025 aggregate from latent dimensions;
- publishes bounded parameter elicitation and joint sensitivity;
- aligns CSV/XLSX/app/Pages/metadata/licensing;
- closes the auxiliary PRISMA full-text flow: 72 sought, 42 assessed,
  13 excluded, 29 included and 30 not retrieved;
- closes the Phase 8 evidence layer without coupling it to external publications;
- adds transactional GitHub/OSF publication automation;
- preserves v2.0.0 and its Zenodo DOI.

Publication gate: human approval and final non-RC metadata remain mandatory. Do not create tag/release/DOI from the candidate.
"@
        $PrUrl = Invoke-Capture -File "gh" -Arguments @("pr", "create", "--repo", $Repo, "--base", "main", "--head", $CandidateBranch, "--draft", "--title", "${CandidateLabel}: technical release refactor", "--body", $PrBody)
        if (-not $PrUrl) { throw "No se pudo crear el pull request borrador." }
    }
    Write-Ok "PR candidato: $PrUrl"
    Write-Step "Esperando controles CI del candidato"
    Invoke-Native -File "gh" -Arguments @("pr", "checks", $CandidateBranch, "--repo", $Repo, "--watch")
    Write-Ok "CI del pull request aprobado."
    Ensure-Pages
    if (-not $PublishRelease) {
        Sync-OsfSupplements -RepoRoot $CloneRoot -CommitSha $CommitSha
    }

    if ($PublishRelease) {
        Write-Step "Comprobando compuerta final"
        $Citation = Get-Content -LiteralPath (Join-Path $CloneRoot "CITATION.cff") -Raw
        $Notes = Get-Content -LiteralPath (Join-Path $CloneRoot "RELEASE_NOTES.md") -Raw
        if ($Citation -match "rc[.-]?\d+" -or $Notes -match "release candidate|candidato") {
            throw "La metadata sigue marcada como RC. Incorpore fases 8-11 y retire la marca candidata antes del release final."
        }
        $Phase8Manifest = Get-Content -LiteralPath (Join-Path $CloneRoot "data\prisma_phase8\phase8_manifest.json") -Raw | ConvertFrom-Json
        $Gate = $Phase8Manifest.publication_gate
        if (-not $Gate.fulltext_complete -or -not $Gate.final_prisma_ready -or -not $Gate.release_scientific_validation_ready -or -not $Gate.dependency_lock_ready -or -not $Gate.release_gate_decoupled -or -not $Gate.phase8_canonical_narrative -or -not $Gate.metadata_method_classification) {
            throw "Compuerta cientifico-tecnica cerrada: cierre de evidencia, lock, independencia, narrativa canonica y metadatos deben estar completos."
        }
        if ($Gate.release_doi_status -notin @("HUMAN_APPROVAL_REQUIRED", "GO")) {
            throw "Estado DOI no apto para aprobacion final: $($Gate.release_doi_status)."
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
        $FinalCommitSha = Invoke-Capture -File "git" -Arguments @("rev-parse", "HEAD") -WorkingDirectory $CloneRoot
        if (-not $FinalCommitSha) { throw "No se pudo resolver el SHA final de main antes del GitHub Release." }
        Invoke-Native -File "gh" -Arguments @("release", "create", "v$Version", $Archive, $ArchiveSidecar, "--repo", $Repo, "--target", $FinalCommitSha, "--title", "Visor Integrado de Democracia del Peru v$Version", "--notes-file", (Join-Path $CloneRoot "RELEASE_NOTES.md"))
        Write-Ok "GitHub Release creado sobre commit final $FinalCommitSha. La integracion GitHub-Zenodo queda activada para acuñar la nueva version DOI."
        if (-not $SkipOsf) {
            Write-Step "Sincronizando OSF opcional despues del release"
            Try-SyncOsfAfterRelease -RepoRoot $CloneRoot -CommitSha $FinalCommitSha
        }
    }
    else {
        Write-Host "`n[COMPUERTA] No se creo tag, GitHub Release ni DOI. Revise el PR y apruebe humanamente el candidato." -ForegroundColor Yellow
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
