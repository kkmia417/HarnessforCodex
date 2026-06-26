<#
.SYNOPSIS
Installs or updates repository Codex skills into a local Codex skills directory.

.EXAMPLE
.\scripts\sync_codex_skills.ps1 -All

.EXAMPLE
.\scripts\sync_codex_skills.ps1 -Skill codex-harness,repo-review

.EXAMPLE
.\scripts\sync_codex_skills.ps1 -All -DestinationRoot "$env:USERPROFILE\.codex\skills-preview"
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory = $true, ParameterSetName = "All")]
    [switch]$All,

    [Parameter(Mandatory = $true, ParameterSetName = "Named")]
    [ValidateNotNullOrEmpty()]
    [string[]]$Skill,

    [string]$DestinationRoot = (Join-Path $env:USERPROFILE ".codex\skills")
)

$ErrorActionPreference = "Stop"

function Get-FullPath {
    param([Parameter(Mandatory = $true)][string]$Path)
    return [System.IO.Path]::GetFullPath($ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Path))
}

function Test-ChildPath {
    param(
        [Parameter(Mandatory = $true)][string]$Parent,
        [Parameter(Mandatory = $true)][string]$Child
    )

    $parentFull = Get-FullPath $Parent
    $childFull = Get-FullPath $Child
    $comparison = [System.StringComparison]::OrdinalIgnoreCase

    if ($childFull.Length -le $parentFull.Length) {
        return $false
    }

    $prefix = $parentFull.TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
    return $childFull.StartsWith($prefix, $comparison)
}

function Get-SkillName {
    param([Parameter(Mandatory = $true)][string]$Name)

    $trimmed = $Name.Trim()
    if ($trimmed -notmatch "^[a-z0-9]+(?:-[a-z0-9]+)*$") {
        throw "Invalid skill name '$Name'. Skill names must be lowercase hyphen-case."
    }
    return $trimmed
}

$repoRoot = Get-FullPath (Join-Path $PSScriptRoot "..")
$sourceRoot = Get-FullPath (Join-Path $repoRoot "skills")
$destinationRootFull = Get-FullPath $DestinationRoot

if (-not (Test-Path -LiteralPath $sourceRoot -PathType Container)) {
    throw "Source skills directory not found: $sourceRoot"
}

if ($PSCmdlet.ParameterSetName -eq "All") {
    $skillNames = Get-ChildItem -LiteralPath $sourceRoot -Directory |
        Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md") -PathType Leaf } |
        Select-Object -ExpandProperty Name
} else {
    $skillNames = $Skill | ForEach-Object { Get-SkillName $_ }
}

$skillNames = @($skillNames | Sort-Object -Unique)
if ($skillNames.Count -eq 0) {
    throw "No skills selected."
}

New-Item -ItemType Directory -Force -Path $destinationRootFull | Out-Null

$syncedCount = 0
foreach ($skillName in $skillNames) {
    $source = Get-FullPath (Join-Path $sourceRoot $skillName)
    $manifest = Join-Path $source "SKILL.md"
    if (-not (Test-ChildPath -Parent $sourceRoot -Child $source) -or -not (Test-Path -LiteralPath $manifest -PathType Leaf)) {
        throw "Repository skill not found: $skillName"
    }

    $destination = Get-FullPath (Join-Path $destinationRootFull $skillName)
    if (-not (Test-ChildPath -Parent $destinationRootFull -Child $destination)) {
        throw "Refusing to write outside destination root: $destination"
    }

    $staging = Get-FullPath (Join-Path $destinationRootFull ".$skillName.sync-$([System.Guid]::NewGuid().ToString('N'))")
    if (-not (Test-ChildPath -Parent $destinationRootFull -Child $staging)) {
        throw "Refusing to stage outside destination root: $staging"
    }

    try {
        if ($PSCmdlet.ShouldProcess($destination, "Install or update skill '$skillName'")) {
            Copy-Item -LiteralPath $source -Destination $staging -Recurse -Force

            if (Test-Path -LiteralPath $destination) {
                Remove-Item -LiteralPath $destination -Recurse -Force
            }

            Move-Item -LiteralPath $staging -Destination $destination
            $syncedCount++
            Write-Host "OK: synced $skillName -> $destination"
        }
    } finally {
        if (Test-Path -LiteralPath $staging) {
            Remove-Item -LiteralPath $staging -Recurse -Force
        }
    }
}

if ($WhatIfPreference) {
    Write-Host "OK: selected $($skillNames.Count) skill(s) for sync to $destinationRootFull"
} else {
    Write-Host "OK: synced $syncedCount skill(s) to $destinationRootFull"
}
