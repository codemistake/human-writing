param(
    [ValidateSet('opencode','claude','codex','cursor','all')]
    [string]$Target = 'opencode'
)

$Source = Split-Path -Parent $MyInvocation.MyCommand.Path

function Install-Skill([string]$Base) {
    $Dest = Join-Path $Base 'human-writing'
    New-Item -ItemType Directory -Force -Path $Dest | Out-Null
    @('SKILL.md','GLOBAL_RULES.md','SOURCES.md','THIRD_PARTY_LICENSES.md','LICENSE') | ForEach-Object {
        Copy-Item -Force (Join-Path $Source $_) (Join-Path $Dest $_)
    }
    Write-Host "Installed human-writing -> $Dest"
}

$homeDir = $HOME
switch ($Target) {
    'opencode' { Install-Skill (Join-Path $homeDir '.config/opencode/skills') }
    'claude'   { Install-Skill (Join-Path $homeDir '.claude/skills') }
    'codex'    { Install-Skill (Join-Path $homeDir '.codex/skills') }
    'cursor'   { Install-Skill (Join-Path $homeDir '.cursor/skills') }
    'all' {
        Install-Skill (Join-Path $homeDir '.config/opencode/skills')
        Install-Skill (Join-Path $homeDir '.claude/skills')
        Install-Skill (Join-Path $homeDir '.codex/skills')
        Install-Skill (Join-Path $homeDir '.cursor/skills')
    }
}

Write-Host 'Global rules were NOT modified. Merge GLOBAL_RULES.md into your AGENTS.md/CLAUDE.md manually.'
