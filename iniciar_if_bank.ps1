$ErrorActionPreference = "Stop"

function Write-Step {
    param(
        [string]$Message
    )

    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Get-EnvValue {
    param(
        [string]$Name,
        [string]$DefaultValue = ""
    )

    $envFile = Join-Path $script:ProjectRoot ".env"
    if (-not (Test-Path $envFile)) {
        return $DefaultValue
    }

    $line = Get-Content $envFile | Where-Object {
        $_ -match "^\s*$Name\s*="
    } | Select-Object -Last 1

    if (-not $line) {
        return $DefaultValue
    }

    $value = ($line -split "=", 2)[1].Trim()
    return $value.Trim("'`"")
}

function Test-TcpPort {
    param(
        [string]$Host,
        [int]$Port,
        [int]$TimeoutMs = 1500
    )

    $client = New-Object System.Net.Sockets.TcpClient
    try {
        $asyncResult = $client.BeginConnect($Host, $Port, $null, $null)
        if (-not $asyncResult.AsyncWaitHandle.WaitOne($TimeoutMs, $false)) {
            return $false
        }

        $null = $client.EndConnect($asyncResult)
        return $true
    }
    catch {
        return $false
    }
    finally {
        $client.Close()
    }
}

function Get-FreePort {
    param(
        [int]$StartPort = 8000,
        [int]$EndPort = 8010
    )

    for ($port = $StartPort; $port -le $EndPort; $port++) {
        $listener = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
        if (-not $listener) {
            return $port
        }
    }

    throw "Nenhuma porta livre encontrada entre $StartPort e $EndPort."
}

function Invoke-ProjectCommand {
    param(
        [string]$Description,
        [string[]]$Arguments
    )

    Write-Step $Description
    & $script:VenvPython @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao executar: $Description"
    }
}

$script:ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $script:ProjectRoot

Write-Host "Projeto: $script:ProjectRoot" -ForegroundColor Yellow

$systemPython = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $systemPython) {
    throw "Python nao encontrado no PATH. Instale o Python 3 antes de continuar."
}

$venvPath = Join-Path $script:ProjectRoot ".venv"
$script:VenvPython = Join-Path $venvPath "Scripts\\python.exe"

if (-not (Test-Path $script:VenvPython)) {
    Write-Step "Criando ambiente virtual"
    & python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        throw "Nao foi possivel criar a .venv."
    }
}

Invoke-ProjectCommand -Description "Instalando dependencias" -Arguments @("-m", "pip", "install", "-r", "requirements.txt")

$settingsModule = "config.settings.test"
$environmentLabel = "test (SQLite local)"

$envFile = Join-Path $script:ProjectRoot ".env"
if (Test-Path $envFile) {
    $postgresHost = Get-EnvValue -Name "POSTGRES_HOST" -DefaultValue "localhost"
    $postgresPort = [int](Get-EnvValue -Name "POSTGRES_PORT" -DefaultValue "5432")

    if (Test-TcpPort -Host $postgresHost -Port $postgresPort) {
        $settingsModule = "config.settings.dev"
        $environmentLabel = "dev (PostgreSQL)"
    }
    else {
        Write-Host "PostgreSQL nao respondeu em $postgresHost`:$postgresPort. Vou iniciar em modo test." -ForegroundColor Yellow
    }
}
else {
    Write-Host "Arquivo .env nao encontrado. Vou iniciar em modo test." -ForegroundColor Yellow
}

Invoke-ProjectCommand -Description "Executando system check" -Arguments @("manage.py", "check", "--settings=$settingsModule")
Invoke-ProjectCommand -Description "Aplicando migracoes" -Arguments @("manage.py", "migrate", "--settings=$settingsModule")
Invoke-ProjectCommand -Description "Sincronizando catalogo de investimentos" -Arguments @("manage.py", "sync_investment_products", "--settings=$settingsModule")
Invoke-ProjectCommand -Description "Carregando dados de apresentacao" -Arguments @("manage.py", "load_presentation_data", "--settings=$settingsModule")

$port = Get-FreePort

Write-Host ""
Write-Host "Ambiente selecionado: $environmentLabel" -ForegroundColor Green
Write-Host "Servidor iniciando em: http://127.0.0.1:$port/api/schema/swagger/" -ForegroundColor Green
Write-Host "Para parar, pressione CTRL + C." -ForegroundColor Green

& $script:VenvPython "manage.py" "runserver" "127.0.0.1:$port" "--settings=$settingsModule"
