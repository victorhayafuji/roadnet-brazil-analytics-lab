#requires -Version 7
<#
    tasks.ps1 — atalhos de desenvolvimento do RoadNet Brazil Analytics Lab.

    Uso (a partir da raiz do repositório):
        pwsh ./tasks.ps1 Setup              # cria a venv e instala dependências
        pwsh ./tasks.ps1 DbInit             # cria schemas + tabelas raw (roda os DDL)
        pwsh ./tasks.ps1 IngestPavimentada  # carrega a malha pavimentada na raw
        pwsh ./tasks.ps1 Sample             # gera amostras versionáveis em data/sample/

    Observação: o Python real deste ambiente é `py -3` (3.12); o `python` do PATH
    pode ser o stub da Windows Store. Depois do Setup usamos o python da venv.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet('Setup', 'DbInit', 'Rls', 'IngestPavimentada', 'Sample', 'Stage')]
    [string]$Command
)

$ErrorActionPreference = 'Stop'
$Root = $PSScriptRoot
$VenvPython = Join-Path $Root '.venv\Scripts\python.exe'

function Use-VenvPython {
    if (-not (Test-Path $VenvPython)) {
        throw "venv não encontrada. Rode primeiro: pwsh ./tasks.ps1 Setup"
    }
    return $VenvPython
}

switch ($Command) {
    'Setup' {
        Write-Host '==> Criando venv com py -3 ...'
        py -3 -m venv (Join-Path $Root '.venv')
        Write-Host '==> Atualizando pip e instalando requirements.txt ...'
        & $VenvPython -m pip install --upgrade pip
        & $VenvPython -m pip install -r (Join-Path $Root 'requirements.txt')
        Write-Host '==> Pronto. Copie .env.example para .env e preencha as credenciais.'
    }

    'DbInit' {
        $py = Use-VenvPython
        Write-Host '==> Criando schemas, tabelas raw e habilitando RLS ...'
        & $py -m pipelines.utils.run_sql `
            'sql/ddl/00_create_schemas.sql' `
            'sql/ddl/01_raw_tables.sql' `
            'sql/ddl/02_enable_rls.sql'
    }

    'Rls' {
        $py = Use-VenvPython
        Write-Host '==> Habilitando Row Level Security nas tabelas raw ...'
        & $py -m pipelines.utils.run_sql 'sql/ddl/02_enable_rls.sql'
    }

    'Stage' {
        $py = Use-VenvPython
        $files = @(Get-ChildItem (Join-Path $Root 'sql\staging\*.sql') |
            Sort-Object Name | ForEach-Object { $_.FullName })
        if ($files.Count -eq 0) { Write-Warning 'Nenhum .sql em sql/staging/.'; break }
        Write-Host "==> Executando staging ($($files.Count) arquivo(s)) ..."
        & $py -m pipelines.utils.run_sql @files
    }

    'IngestPavimentada' {
        $py = Use-VenvPython
        Write-Host '==> Ingerindo malha pavimentada ...'
        & $py -m pipelines.ingest.load_pavimentada
    }

    'Sample' {
        $sampleDir = Join-Path $Root 'data\sample'
        New-Item -ItemType Directory -Force -Path $sampleDir | Out-Null
        $files = @{
            'levantamentos_pavimentada_2026_05.csv'     = 'data\raw\dnit\condicoes_pavimento\levantamentos_pavimentada_2026_05.csv'
            'levantamentos_nao_pavimentada_2026_05.csv' = 'data\raw\dnit\condicoes_pavimento\levantamentos_nao_pavimentada_2026_05.csv'
        }
        foreach ($name in $files.Keys) {
            $src = Join-Path $Root $files[$name]
            if (-not (Test-Path $src)) {
                Write-Warning "Origem ausente, pulando: $src"
                continue
            }
            $dest = Join-Path $sampleDir ($name -replace '\.csv$', '_sample.csv')
            # Header + 500 linhas de dados, preservando encoding UTF-8.
            Get-Content -Path $src -TotalCount 501 -Encoding utf8 |
                Set-Content -Path $dest -Encoding utf8
            Write-Host "==> Amostra gerada: $dest"
        }
    }
}
