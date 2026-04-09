function pause ($message="appuyer sur une touche pour continuer")
{
write-host $message
$null = $host.UI.rawUI.ReadKey("noecho,includekeydown")
write-host
}

function win22core()
{
$NomVM=read-host "Nom de la VM"
$tailleMEM=read-host "taille de la mémoire désirée (en Gb)"
$memory = [int]$tailleMEM * 1GB
#$memory= invoke-expression $tailleMEM
$vSwitches = Get-VMSwitch
for ($i = 0; $i -lt $vSwitches.Count; $i++) {
    Write-Host "$i : $($vSwitches[$i].Name) - $($vSwitches[$i].SwitchType)"
}
[int]$index = -1
do {
    $input = Read-Host "Entrez le numéro du commutateur réseau que vous souhaitez utiliser"
    $isValid = [int]::TryParse($input, [ref]$index) -and $index -ge 0 -and $index -lt $vSwitches.Count

    if (-not $isValid) {
        Write-Host "Entrée invalide. Veuillez entrer un nombre entre 0 et $($vSwitches.Count - 1)." -ForegroundColor Red
    }
} while (-not $isValid)
$comutateur = $vSwitches[$index].Name
Write-Host "Vous avez choisi : $comutateur"
$app=New-Object -com shell.application
$folderObject = $app.BrowseForFolder(0, "Sélectionner le dossier dans lequel stocker la VM", 0, "")
if ($folderObject -eq $null) {
    Write-Host "Aucun dossier sélectionné. Opération annulée." -ForegroundColor Yellow
    return
}
$folder = $folderObject.Self.Path
Write-Host "Création de la VM : " -NoNewline; Write-Host $NomVM -ForegroundColor Cyan -NoNewline; Write-Host " avec " -NoNewline; Write-Host "$tailleMEM GO" -ForegroundColor Cyan -NoNewline; Write-Host ", sur le Vswitch " -NoNewline; Write-Host $comutateur -ForegroundColor Cyan -NoNewline; Write-Host " dans le dossier " -NoNewline; Write-Host $folder\$NomVM -ForegroundColor Cyan
$confirm = Read-Host "Voulez-vous continuer ? (o/n)"
    if ($confirm -ne "o") {
        Write-Host "Opération annulée." -ForegroundColor Yellow
        return
    }
New-vm -name "$NomVM" -path "$folder" -memorystartupbytes $memory -Generation 1 -switch $comutateur
mkdir "$folder\$NomVM\VHD"
copy-item -path "E:\sysprep\WS2022-sysprep-CORE.vhdx" -destination "$folder\$NomVM\VHD\$NomVM.vhdx"
add-vmharddiskdrive -vmname "$NomVM" -path "$folder\$NomVM\VHD\$NomVM.vhdx"
set-vm -name "$NomVM" -processorcount 2
set-vm -name "$NomVM" -checkpointtype disabled | Start-Sleep -Seconds 1
$HDV = Get-VMHardDiskDrive -VMname $NomVM
Set-VMFirmware -VMName $NomVM -FirstBootDevice $HDV
start-vm "$NomVM"
$vm = Get-VM -Name $NomVM -ErrorAction SilentlyContinue
if ($vm) {
    Write-Host "✅ La VM '$NomVM' a été créée avec succès." -ForegroundColor Green
} else {
    Write-Host "❌ Échec de la création de la VM '$NomVM'." -ForegroundColor Red
    return
}
}

function win22gui()
{
$NomVM=read-host "Nom de la VM"
$tailleMEM=read-host "taille de la mémoire désirée (en Gb)"
$memory = [int]$tailleMEM * 1GB
#$memory= invoke-expression $tailleMEM
$vSwitches = Get-VMSwitch
for ($i = 0; $i -lt $vSwitches.Count; $i++) {
    Write-Host "$i : $($vSwitches[$i].Name) - $($vSwitches[$i].SwitchType)"
}
[int]$index = -1
do {
    $input = Read-Host "Entrez le numéro du commutateur réseau que vous souhaitez utiliser"
    $isValid = [int]::TryParse($input, [ref]$index) -and $index -ge 0 -and $index -lt $vSwitches.Count

    if (-not $isValid) {
        Write-Host "Entrée invalide. Veuillez entrer un nombre entre 0 et $($vSwitches.Count - 1)." -ForegroundColor Red
    }
} while (-not $isValid)
$comutateur = $vSwitches[$index].Name
Write-Host "Vous avez choisi : $comutateur"
$app=New-Object -com shell.application
$folderObject = $app.BrowseForFolder(0, "Sélectionner le dossier dans lequel stocker la VM", 0, "")
if ($folderObject -eq $null) {
    Write-Host "Aucun dossier sélectionné. Opération annulée." -ForegroundColor Yellow
    return
}
$folder = $folderObject.Self.Path
Write-Host "Création de la VM : " -NoNewline; Write-Host $NomVM -ForegroundColor Cyan -NoNewline; Write-Host " avec " -NoNewline; Write-Host "$tailleMEM GO" -ForegroundColor Cyan -NoNewline; Write-Host ", sur le Vswitch " -NoNewline; Write-Host $comutateur -ForegroundColor Cyan -NoNewline; Write-Host " dans le dossier " -NoNewline; Write-Host $folder\$NomVM -ForegroundColor Cyan
$confirm = Read-Host "Voulez-vous continuer ? (o/n)"
    if ($confirm -ne "o") {
        Write-Host "Opération annulée." -ForegroundColor Yellow
        return
    }
New-vm -name "$NomVM" -path "$folder" -memorystartupbytes $memory -Generation 2 -switch $comutateur
mkdir "$folder\$NomVM\VHD"
copy-item -path "E:\sysprep\WIN2022sysprepGUI.vhdx" -destination "$folder\$NomVM\VHD\$NomVM.vhdx"
add-vmharddiskdrive -vmname "$NomVM" -path "$folder\$NomVM\VHD\$NomVM.vhdx"
set-vm -name "$NomVM" -processorcount 2
set-vm -name "$NomVM" -checkpointtype disabled | Start-Sleep -Seconds 1
$HDV = Get-VMHardDiskDrive -VMname $NomVM
Set-VMFirmware -VMName $NomVM -FirstBootDevice $HDV
start-vm "$NomVM"
$vm = Get-VM -Name $NomVM -ErrorAction SilentlyContinue
if ($vm) {
    Write-Host "✅ La VM '$NomVM' a été créée avec succès." -ForegroundColor Green
} else {
    Write-Host "❌ Échec de la création de la VM '$NomVM'." -ForegroundColor Red
    return
}
}

function W11-PRO()
{
$NomVM=read-host "Nom de la VM"
$tailleMEM=read-host "taille de la mémoire désirée (en Gb)"
$memory = [int]$tailleMEM * 1GB
#$memory= invoke-expression $tailleMEM
$vSwitches = Get-VMSwitch
for ($i = 0; $i -lt $vSwitches.Count; $i++) {
    Write-Host "$i : $($vSwitches[$i].Name) - $($vSwitches[$i].SwitchType)"
}
[int]$index = -1
do {
    $input = Read-Host "Entrez le numéro du commutateur réseau que vous souhaitez utiliser"
    $isValid = [int]::TryParse($input, [ref]$index) -and $index -ge 0 -and $index -lt $vSwitches.Count

    if (-not $isValid) {
        Write-Host "Entrée invalide. Veuillez entrer un nombre entre 0 et $($vSwitches.Count - 1)." -ForegroundColor Red
    }
} while (-not $isValid)
$comutateur = $vSwitches[$index].Name
Write-Host "Vous avez choisi : $comutateur"
$app=New-Object -com shell.application
$folderObject = $app.BrowseForFolder(0, "Sélectionner le dossier dans lequel stocker la VM", 0, "")
if ($folderObject -eq $null) {
    Write-Host "Aucun dossier sélectionné. Opération annulée." -ForegroundColor Yellow
    return
}
$folder = $folderObject.Self.Path
Write-Host "Création de la VM : " -NoNewline; Write-Host $NomVM -ForegroundColor Cyan -NoNewline; Write-Host " avec " -NoNewline; Write-Host "$tailleMEM GO" -ForegroundColor Cyan -NoNewline; Write-Host ", sur le Vswitch " -NoNewline; Write-Host $comutateur -ForegroundColor Cyan -NoNewline; Write-Host " dans le dossier " -NoNewline; Write-Host $folder\$NomVM -ForegroundColor Cyan
$confirm = Read-Host "Voulez-vous continuer ? (o/n)"
    if ($confirm -ne "o") {
        Write-Host "Opération annulée." -ForegroundColor Yellow
        return
    }
New-vm -name "$NomVM" -path "$folder" -memorystartupbytes $memory -Generation 2 -switch $comutateur
mkdir "$folder\$NomVM\VHD"
copy-item -path "E:\sysprep\W11-PRO.vhdx" -destination "$folder\$NomVM\VHD\$NomVM.vhdx"
add-vmharddiskdrive -vmname "$NomVM" -path "$folder\$NomVM\VHD\$NomVM.vhdx"
set-vm -name "$NomVM" -processorcount 2
set-vm -name "$NomVM" -checkpointtype disabled | Start-Sleep -Seconds 1
$HDV = Get-VMHardDiskDrive -VMname $NomVM
Set-VMFirmware -VMName $NomVM -FirstBootDevice $HDV
start-vm "$NomVM"
$vm = Get-VM -Name $NomVM -ErrorAction SilentlyContinue
if ($vm) {
    Write-Host "✅ La VM '$NomVM' a été créée avec succès." -ForegroundColor Green
} else {
    Write-Host "❌ Échec de la création de la VM '$NomVM'." -ForegroundColor Red
    return
}
}

function changeIPnom()
{
Get-NetIPAddress | ft
$intindex = read-host "saisir l'interface index de la carte reseau"
$iphost = read-host "saisir la nouvelle ip de la machine"
$mask = read-host "saisir le masque sous reseau en CIDR"
$ipgw = read-host "saisir la passerelle par defaut"
Remove-NetRoute -InterfaceIndex $intindex -Confirm:$false
Remove-NetIPAddress -InterfaceIndex $intindex -Confirm:$false
New-NetIPAddress -InterfaceIndex $intindex -AddressFamily IPv4 -IPaddress $iphost -PrefixLength $mask -DefaultGateway $ipgw
$nompc = Read-Host "saisir le nom de la machine"
Rename-Computer -newname $nompc
shutdown -t 0 -r
}

function ADDS()
{
$nodomaine=read-host "saisir le nom de domaine"
$nomnetbios=read-host "saisir le netbios du domaine"
Add-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools -IncludeAllSubFeature
Import-Module ADDSDeployment
Install-ADDSForest `
-CreateDnsDelegation:$false `
-DatabasePath "C:\Windows\NTDS" `
-DomainMode "WinThreshold" `
-DomainName $nodomaine `
-DomainNetbiosName $nomnetbios `
-ForestMode "WinThreshold" `
-InstallDns:$true `
-LogPath "C:\Windows\NTDS" `
-NoRebootOnCompletion:$false `
-SysvolPath "C:\Windows\SYSVOL" `
-Force:$true
}

function reverse()
{
 get-dnsclientserveraddress | ft
 $indexint = read-host "saisir l'inteface index"
 $serveurad = read-host "saisir l'IP du serveur DNS"
 get-dnsclientserveraddress -interfaceindex $indexint -addressfamily IPv6 | set-dnsclientserveraddress -resetserveraddress
 set-dnsclientserveraddress -interfaceindex $indexint -serveraddress $serveurad
 $zoneinverse = read-host "saisir l'ip du reseau au format IP/CIDR (ex : 192.168.1.0/24)"
 add-dnsserverprimaryzone -network $zoneinverse -replicationscope domain -dynamicupdate secure
 ipconfig /registerdns
 $forwarderIP = Read-Host "Saisir l'adresse IP du DNS à ajouter en forwarder (ou appuyez sur Entrée pour ignorer)"
 if (![string]::IsNullOrWhiteSpace($forwarderIP)) 
  {
    try {
        Add-DnsServerForwarder -IPAddress $forwarderIP -ErrorAction Stop
        Write-Host "`n✅ DNS forwarder ajouté avec succès : $forwarderIP"
        }
    catch {
        Write-Warning "⚠️ Impossible d'ajouter le DNS forwarder : $($_.Exception.Message)"
          }
  }
 else {
    Write-Host "⏭️  Ajout du DNS forwarder ignoré."
      }
}

function disk3()
{
# Récupère toutes les VM et les stocke dans une variable
$vms = Get-VM

# Affiche les VM avec un index
for ($i = 0; $i -lt $vms.Count; $i++) {
    Write-Host "$i : $($vms[$i].Name) - $($vms[$i].State)"
}

# Initialisation de l'index
[int]$index = -1

# Boucle de sélection avec validation
do {
    $input = Read-Host "Entrez le numéro de la VM que vous souhaitez utiliser"
    $isValid = [int]::TryParse($input, [ref]$index) -and $index -ge 0 -and $index -lt $vms.Count
    if (-not $isValid) {
        Write-Host "Entrée invalide. Veuillez entrer un nombre entre 0 et $($vms.Count - 1)." -ForegroundColor Red
    }
} while (-not $isValid)

 # Récupération du nom de la VM sélectionnée
$vmname2 = $vms[$index].Name
Write-Host "Vous avez choisi : $vmname2" -ForegroundColor Cyan

$cheminVMsup =  Split-Path -Path (Get-VMHardDiskDrive -VMName "$vmname2")[0].Path
New-VHD -Path $cheminVMsup"\bdd.vhdx" -sizebytes 4196MB
New-VHD -Path $cheminVMsup"\log.vhdx" -sizebytes 4196MB
New-VHD -Path $cheminVMsup"\sysvol.vhdx" -sizebytes 4196MB

Add-VMHardDiskDrive -VMName $vmname2 -controllertype SCSI -ControllerNumber 0 -Path $cheminVMsup"\bdd.vhdx"
Add-VMHardDiskDrive -VMName $vmname2 -controllertype SCSI -ControllerNumber 0 -Path $cheminVMsup"\log.vhdx"
Add-VMHardDiskDrive -VMName $vmname2 -controllertype SCSI -ControllerNumber 0 -Path $cheminVMsup"\sysvol.vhdx"

}

function ADDSCORP()
{
Get-Disk | ft
$diskbdd = Read-Host "Saisir le numéro de disque pour la BDD"
Initialize-Disk -number $diskbdd
New-Partition -DiskNumber $diskbdd -DriveLetter B -size 4GB
Format-Volume -DriveLetter B -FileSystem NTFS -Confirm:$false -NewFileSystemLabel BDD
Get-Disk | ft
$disklog = Read-Host "Saisir le numéro de disque pour les LOGS"
Initialize-Disk -number $disklog
New-Partition -DiskNumber $disklog -DriveLetter L -size 4GB
Format-Volume -DriveLetter L -FileSystem NTFS -Confirm:$false -NewFileSystemLabel LOG
Get-Disk | ft
$disksysvol = Read-Host "Saisir le numéro de disque pour le SYSVOL"
Initialize-Disk -number $disksysvol
New-Partition -DiskNumber $disksysvol -DriveLetter S -size 4GB
Format-Volume -DriveLetter S -FileSystem NTFS -Confirm:$false -NewFileSystemLabel SYSVOL

$nodomaine=read-host "saisir le nom de domaine"
$nomnetbios=read-host "saisir le netbios du domaine"
Add-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools -IncludeAllSubFeature
Import-Module ADDSDeployment
Install-ADDSForest `
-CreateDnsDelegation:$false `
-DatabasePath "B:\NTDS" `
-DomainMode "WinThreshold" `
-DomainName $nodomaine `
-DomainNetbiosName $nomnetbios `
-ForestMode "WinThreshold" `
-InstallDns:$true `
-LogPath "L:\NTDS" `
-NoRebootOnCompletion:$false `
-SysvolPath "S:\SYSVOL" `
-Force:$true
}


function ipad2 ()
{
Get-DnsClientServerAddress | ft
$ideint = Read-Host "Saisir l'interface index"
$dnsad = Read-Host "Saisir l'adresse IP du serveur dns du domain AD"
Set-DnsClientServerAddress -InterfaceIndex $ideint -ServerAddresses $dnsad
$addomain = Read-Host "Saisir le domaine à joindre"
$credentials = Get-credential
Add-Computer -DomainName $addomain -Restart -Credential $credentials
}

function adredonde ()
{
Get-Disk | ft
$diskbdd = Read-Host " Saisir le numero de disque pour la BDD"
Initialize-Disk -Number $diskbdd
New-Partition -DiskNumber $diskbdd -DriveLetter B -Size 4GB
Format-Volume -DriveLetter B -FileSystem NTFS -Confirm:$false -NewFileSystemLabel BDD
Get-Disk | ft
$disklogs = Read-Host " Saisir le numero de disque pour les LOGS"
Initialize-Disk -Number $disklogs
New-Partition -DiskNumber $disklogs -DriveLetter L -Size 4GB
Format-Volume -DriveLetter L -FileSystem NTFS -Confirm:$false -NewFileSystemLabel LOGS
Get-Disk | ft
$disksysvol = Read-Host " Saisir le numero de disque pour le SYSVOL"
Initialize-Disk -Number $disksysvol
New-Partition -DiskNumber $disksysvol -DriveLetter S -Size 4GB
Format-Volume -DriveLetter S -FileSystem NTFS -Confirm:$false -NewFileSystemLabel SYSVOL

$namadom = Read-Host "Saisir le nom de domaine"
Add-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools -IncludeAllSubFeature
Import-Module ADDSDeployment
Install-ADDSDomainController `
-NoGlobalCatalog:$false `
-CreateDnsDelegation:$false `
-CriticalReplicationOnly:$false `
-DatabasePath "B:\NTDS" `
-DomainName $namadom `
-InstallDns:$true `
-LogPath "L:\NTDS" `
-NoRebootOnCompletion:$false `
-SiteName "Default-First-Site-Name" `
-SysvolPath "S:\SYSVOL" `
-Force:$true
}

function DNS-AD2()
{
get-dnsclientserveraddress | ft
$indexint = read-host "saisir l'inteface index"
$serveurad = read-host "saisir les IP des serveurs DNS (ex:192.168.0.1,192.168.0.2,127.0.0.1)"
get-dnsclientserveraddress -interfaceindex $indexint -addressfamily IPv6 | set-dnsclientserveraddress -resetserveraddress
set-dnsclientserveraddress -interfaceindex $indexint -serveraddress $serveurad
}

# function dhcp()
# {
# $rangedeb = Read-Host "Saisir le debut de l'etendue"
# $rangefin = Read-Host "Sairir la fin de l'etendue"
# $maskdhcp = Read-Host "Saisir le masque"
# $networkdhcp = Read-Host "Saisir l'adresse du reseau"
# $domainedhcp = Read-Host "Saisir le nom de domaine"
# $dnsdhcp = Read-Host "Saisir le dns du domaine"
# $gwdhcp = Read-Host "Saisir la passerelle"
# $dhcpname = Read-Host "Saisir le nom de l'étendue"
# $fqdndhcp = Read-Host "Saisir le FQDN du serveur DHCP (namenetbios.nomdedomaine)"

# Install-WindowsFeature DHCP -IncludeManagementTools
# Set-ItemProperty -Path registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\ServerManager\Roles\12 -Name ConfigurationState -Value 2
# Add-DhcpServerv4Scope -Name $dhcpname -StartRange $rangedeb -EndRange $rangefin -SubnetMask $maskdhcp -state Active
# Set-DhcpServerv4OptionValue $networkdhcp -DnsDomain $domainedhcp -DnsServer $dnsdhcp -Router $gwdhcp
# Add-DhcpServerInDC -DnsName $fqdndhcp
# }
function dhcp() 
{
    # Récupère l'interface principale avec une adresse IPv4 active
    $ipInfo = Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.PrefixOrigin -ne 'WellKnown' -and $_.IPAddress -notlike '169.*' } | Sort-Object InterfaceIndex | Select-Object -First 1

    if (-not $ipInfo) {
        Write-Host "Impossible de récupérer automatiquement les infos réseau."
        return
    }

    $ipFull     = $ipInfo.IPAddress
    $prefix     = $ipInfo.PrefixLength
    $gateway    = (Get-NetRoute -DestinationPrefix "0.0.0.0/0" | Where-Object { $_.InterfaceIndex -eq $ipInfo.InterfaceIndex }).NextHop
    $dnsServers = (Get-DnsClientServerAddress -InterfaceIndex $ipInfo.InterfaceIndex -AddressFamily IPv4).ServerAddresses
    $dns        = $dnsServers -join ','

    # Convertit le masque en format décimal
    function Convert-PrefixToMask ($prefix) {
        $maskBytes = [math]::Pow(2, 32) - [math]::Pow(2, 32 - $prefix)
        [IPAddress]$maskBytes
    }

    $mask = Convert-PrefixToMask $prefix

    # Récupère le réseau
    $baseIP = ($ipFull -split '\.')[0..2] -join '.'
    $network = "$baseIP.0"

    Write-Host "`nInformations détectées automatiquement :"
    Write-Host "Adresse IP     : $ipFull"
    Write-Host "Masque         : $mask"
    Write-Host "Passerelle     : $gateway"
    Write-Host "Serveur(s) DNS : $dns"
    Write-Host "Réseau         : $network/24"

    # L'utilisateur n’entre que les derniers octets pour la plage
    $startOctet = Read-Host "Saisir le dernier octet de début de plage"
    $endOctet   = Read-Host "Saisir le dernier octet de fin de plage"

    $rangeStart = "$baseIP.$startOctet"
    $rangeEnd   = "$baseIP.$endOctet"
    $domain = (Get-WmiObject Win32_ComputerSystem).Domain
    $fqdn = [System.Net.Dns]::GetHostByName(($env:COMPUTERNAME)).HostName
    $scopeName  = Read-Host "Saisir le nom de l'étendue"

    # Installation et configuration DHCP
    Install-WindowsFeature DHCP -IncludeManagementTools
    Set-ItemProperty -Path registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\ServerManager\Roles\12 -Name ConfigurationState -Value 2

    Add-DhcpServerv4Scope -Name $scopeName -StartRange $rangeStart -EndRange $rangeEnd -SubnetMask $mask -State Active
    Set-DhcpServerv4OptionValue -ScopeID $network -DnsDomain $domain -DnsServer $dns -Router $gateway
    Add-DhcpServerInDC -DnsName $fqdn

    Write-Host "`nÉtendue DHCP '$scopeName' créée avec succès sur le réseau $network."
}

function diskPartage()
{
 # Récupère toutes les VM et les stocke dans une variable
 $vms = Get-VM

 # Affiche les VM avec un index
 for ($i = 0; $i -lt $vms.Count; $i++) {
     Write-Host "$i : $($vms[$i].Name) - $($vms[$i].State)"
 }

 # Initialisation de l'index
 [int]$index = -1

 # Boucle de sélection avec validation
 do {
     $input = Read-Host "Entrez le numéro de la VM que vous souhaitez utiliser"
     $isValid = [int]::TryParse($input, [ref]$index) -and $index -ge 0 -and $index -lt $vms.Count

     if (-not $isValid) {
         Write-Host "Entrée invalide. Veuillez entrer un nombre entre 0 et $($vms.Count - 1)." -ForegroundColor Red
     }
 } while (-not $isValid)

 # Récupération du nom de la VM sélectionnée
 $vmname2 = $vms[$index].Name
 Write-Host "Vous avez choisi : $vmname2" -ForegroundColor Cyan
    # Récupère le chemin du dossier VHD de la VM existante
$disqueExistant = Get-VMHardDiskDrive -VMName $vmname2 | Select-Object -First 1
$vhdDossier = Split-Path $disqueExistant.Path -Parent
$vhdPath = Join-Path $vhdDossier "Partage.vhdx"

# Crée le disque s’il n’existe pas
if (-not (Test-Path $vhdPath)) {
    Write-Host "Création du disque $vhdPath..."
    New-VHD -Path $vhdPath -SizeBytes 10GB -Dynamic
} else {
    Write-Host "Le disque $vhdPath existe déjà." -ForegroundColor Yellow
}

# Attache le disque à la VM
Write-Host "Ajout du disque à la VM $vmname2..."
Add-VMHardDiskDrive -VMName $vmname2 -ControllerType SCSI -ControllerNumber 0 -Path $vhdPath
} 

function DossPartage()
{
        
    Get-Disk | ft
    $diskparta = Read-Host "Saisir le numéro de disque pour le partage"
    Initialize-Disk -number $diskparta
    New-Partition -DiskNumber $diskparta -DriveLetter Z -size 10GB
    Format-Volume -DriveLetter Z -FileSystem NTFS -Confirm:$false -NewFileSystemLabel PARTAGE
    New-Item -Name PARTAGE -ItemType Directory -Path Z:\
    New-SmbShare -Name Partage -Path Z:\PARTAGE -FullAccess "Administrateurs" -ReadAccess "Utilisateurs" 
    New-Item -Name PERSO -ItemType Directory -Path Z:\PARTAGE
    New-SmbShare -Name Perso -Path Z:\PARTAGE\PERSO -FullAccess "Administrateurs" -ReadAccess "Utilisateurs" 
    New-Item -Name SERVICES -ItemType Directory -Path Z:\PARTAGE
    New-SmbShare -Name Services -Path Z:\PARTAGE\SERVICES -FullAccess "Administrateurs" -ReadAccess "Utilisateurs" 
}

    #récupération du chemin du script
$scriptPath = $MyInvocation.MyCommand.Path
function invok()
{
    # Récupère toutes les VM et les stocke dans une variable
    $vms = Get-VM

    # Affiche les VM avec un index
    for ($i = 0; $i -lt $vms.Count; $i++) {
        Write-Host "$i : $($vms[$i].Name) - $($vms[$i].State)"
    }

    # Initialisation de l'index
    [int]$index = -1

    # Boucle de sélection avec validation
    do {
        $input = Read-Host "Entrez le numéro de la VM que vous souhaitez utiliser"
        $isValid = [int]::TryParse($input, [ref]$index) -and $index -ge 0 -and $index -lt $vms.Count

        if (-not $isValid) {
            Write-Host "Entrée invalide. Veuillez entrer un nombre entre 0 et $($vms.Count - 1)." -ForegroundColor Red
        }
    } while (-not $isValid)

    # Récupération du nom de la VM sélectionnée
    $vmname3 = $vms[$index].Name
    Write-Host "Vous avez choisi : $vmname3" -ForegroundColor Cyan

    # Lancement du script distant
    Invoke-Command -VMName $vmname3 -FilePath $scriptPath
}

function menu()
{
    Get-PSSession | Remove-PSSession
    clear-host
    Write-Host @"
+========================================================================================+
|  POWERSHELL CONSOLE - USER MENU                                                        | 
+========================================================================================+
|                                                                                        |
|    1) Creation VM WindowsServer Core 2022                                              |
|    2) Creation VM WindowsServer Graphique 2022                                         |
|    3) Création PC Client Windows 11                                                    |
|      /\ Après création vérifier la VM dans hyper-v et configurer le mot de passe /\    |
|                                                                                        |
|    4) Ajouter 3 disques dur à un DC  (AD corporate)                                    |
|    4b) Ajouter un disque de 10 Go à une VM (dossier partagés)                                      |
|                                                                                        |   
|  5) Invoquer le menu sur une VM au choix (à répéter pour chaques choix suivants)       |
|    6) Changer l'IP et nom de poste                                                     |
|         controleur principal                                                           |
|             7) Installation active directory corporate                                 |
|             8) Gestion DNS et zone inversee                                            |
|         controleur secondaire                                                          |
|             9) AD2 changer ip du DNS et jointure domaine                               |
|            10) Installation AD secondaire (AD corporate)                               |
|            11) Configurer DNS sur AD secondaire                                        |
|                                                                                        |
|    12) Configurer DHCP                                                                 |
|                                                                                        |
|    13) Creer les dossiers partagés (AD corporate)                                      |
|                                                                                        |
|    Q) Quittez le script                                                                |
|                                                                                        |
+========================================================================================+
"@
    $choix = read-host "votre choix?"
    switch ($choix)
        {
        1 {win22core;pause;menu}
        2 {win22gui;pause;menu}
        3 {W11-PRO;pause;menu}
        4 {disk3;pause;menu}
        5 {invok;pause;menu}
        6 {changeIPnom;pause;menu}
        7 {ADDSCORP;pause;menu}
        8 {reverse;pause;menu}
        9 {ipad2;pause;menu}
        10 {adredonde;pause;menu}
        11 {DNS-AD2;pause;menu}
        12 {dhcp;pause;menu}
        4b {diskPartage;pause;menu}
        13 {DossPartage;pause;menu}
        #{ADDS;pause;menu}
        Q {exit}
        default{menu}
        }
}
menu