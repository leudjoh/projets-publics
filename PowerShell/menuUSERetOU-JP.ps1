Get-ADComputer -Filter * | ft
$NomSRV = Read-Host "Indiquez le nom de serveur pour les dossiers perso"

$CSVFile = "C:\script\liste.csv"
$CSVData = Import-CSV -Path $CSVFile -Delimiter ";" -Encoding UTF8
$chemindomain = (get-addomain).distinguishedname
$upnmail = $env:USERDNSDOMAIN.ToLower()
$chemingroupes="OU=GROUPES,"+$chemindomain
$dossierperso = "\\$NomSRV\PARTAGE\PERSO"
$dossierservices = "\\$NomSRV\PARTAGE\SERVICES"


function pause($message="Appuyer sur touche pour continuer")
{
Write-host -NoNewline $message
$null = $Host.UI.RawUI.ReadKey("noecho,includeKeydown")
Write-host ""
}


function users ()
{
Foreach($Utilisateur in $CSVData){

    $UtilisateurPrenom = $Utilisateur.Prenom
    $UtilisateurNom = $Utilisateur.Nom
    $UtilisateurLogin = $UtilisateurPrenom + "." + $UtilisateurNom
    $UtilisateurEmail = $UtilisateurLogin+"@"+$upnmail
    $UtilisateurMotDePasse = "Formation2023"
    $UtilisateurFonction = $Utilisateur.Fonction.toUpper()

    # Vérifier la présence de l'utilisateur dans l'AD
    if (Get-ADUser -Filter {SamAccountName -eq $UtilisateurLogin})
    {
        Write-Warning "L'identifiant $UtilisateurLogin existe déjà dans l'AD"
    }
    else
    {
        New-ADUser -Name "$UtilisateurNom $UtilisateurPrenom" `
                    -DisplayName "$UtilisateurNom $UtilisateurPrenom" `
                    -GivenName $UtilisateurPrenom `
                    -Surname $UtilisateurNom `
                    -SamAccountName $UtilisateurLogin `
                    -UserPrincipalName $UtilisateurLogin+"@"+$upnmail `
                    -EmailAddress $UtilisateurEmail `
                    -Title $UtilisateurFonction `
                    -Path "OU=$UtilisateurFonction,OU=UTILISATEURS,$chemindomain" `
                    -AccountPassword(ConvertTo-SecureString $UtilisateurMotDePasse -AsPlainText -Force) `
                    -ChangePasswordAtLogon $true `
                    -Enabled $true

        Add-ADGroupMember "GDL_$UtilisateurFonction" -Members $UtilisateurLogin
        creationdossiers($UtilisateurLogin,$UtilisateurFonction)
        Write-Output "Création de l'utilisateur : $UtilisateurLogin ($UtilisateurNom $UtilisateurPrenom)"
    }
}
}

function creationdossiers()
{
        $existe = Test-Path -Path $dossierservices\$UtilisateurFonction
        
        if (!$existe)
            {New-item -ItemType Directory -Name $UtilisateurFonction -Path $dossierservices -verbose}

        New-Item -ItemType Directory -Name $UtilisateurLogin -Path $dossierperso -verbose
}

function ouusersgroupe ()
{
Foreach($Utilisateur in $CSVData){

    $UtilisateurFonction = $Utilisateur.Fonction.toUpper()
    try {
    New-ADOrganizationalUnit -Name $UtilisateurFonction -Path "OU=UTILISATEURS,$chemindomain" -verbose -ProtectedFromAccidentalDeletion $false
    New-ADGroup -GroupCategory Security -GroupScope DomainLocal -Name "GDL_$UtilisateurFonction" -Path $chemingroupes -Verbose
    }
            catch{}

}
}

function creationsous()
{    
    New-ADOrganizationalUnit -Name GROUPES -Path $chemindomain -verbose -ProtectedFromAccidentalDeletion $false
    New-ADOrganizationalUnit -Name IMPRIMANTES -Path $chemindomain -verbose -ProtectedFromAccidentalDeletion $false
    New-ADOrganizationalUnit -Name ORDINATEURS -Path $chemindomain -verbose -ProtectedFromAccidentalDeletion $false
    New-ADOrganizationalUnit -Name FIXE -Path "OU=ORDINATEURS,$dnsdomaine" -verbose -ProtectedFromAccidentalDeletion $false
    New-ADOrganizationalUnit -Name PORTABLE -Path "OU=ORDINATEURS,$dnsdomaine" -verbose -ProtectedFromAccidentalDeletion $false
    New-ADOrganizationalUnit -Name SERVEURS -Path $chemindomain -verbose -ProtectedFromAccidentalDeletion $false
    New-ADOrganizationalUnit -Name UTILISATEURS -Path $chemindomain -verbose -ProtectedFromAccidentalDeletion $false
}



function menu ()
{
    Clear-Host
    Write-Host "Menu Script"

    Write-host "1: Creation Unite d'organisation CORPORATE"
    Write-host "2: Creation Unite d'organisation en lots"
    Write-host "3: Creation Utilisateurs en LOTS"
    write-host "Q: Quittez le script"
    $choix = Read-Host "votre choix ?"
    switch ($choix)
        {
        1 {creationsous;pause;menu}
        2 {ouusersgroupe;pause;menu}
        3 {users;pause;menu}
        Q {exit}
        default {menu}
        }
}
menu