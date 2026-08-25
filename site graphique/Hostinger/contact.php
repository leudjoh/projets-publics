<?php

declare(strict_types=1);

use PHPMailer\PHPMailer\Exception;
use PHPMailer\PHPMailer\PHPMailer;

header('Content-Type: application/json; charset=UTF-8');

// --------------------------------------------------
// Configuration
// --------------------------------------------------

$config = require __DIR__ . '../private/config.php';

require __DIR__ . '/vendor/autoload.php';

// --------------------------------------------------
// Réponse JSON
// --------------------------------------------------

function respond(int $statusCode, bool $success, string $message): never
{
    http_response_code($statusCode);

    echo json_encode(
        [
            'success' => $success,
            'message' => $message,
        ],
        JSON_UNESCAPED_UNICODE
    );

    exit;
}

// --------------------------------------------------
// Autoriser uniquement POST
// --------------------------------------------------

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    respond(
        405,
        false,
        'Méthode non autorisée.'
    );
}

// --------------------------------------------------
// Honeypot anti-bot
// --------------------------------------------------
//
// Ce champ sera ajouté au formulaire HTML plus tard.
// Un utilisateur normal ne le remplira pas.
// Beaucoup de bots rempliront automatiquement tous les champs.
// --------------------------------------------------

if (!empty($_POST['website'] ?? '')) {
    // On répond comme si tout s'était bien passé
    // pour ne pas révéler la présence du honeypot.
    respond(
        200,
        true,
        'Votre message a bien été envoyé.'
    );
}

// --------------------------------------------------
// Récupération des données
// --------------------------------------------------

$nom = trim((string) ($_POST['nom'] ?? ''));
$email = trim((string) ($_POST['email'] ?? ''));
$message = trim((string) ($_POST['message'] ?? ''));

// --------------------------------------------------
// Validation
// --------------------------------------------------

if ($nom === '' || $email === '' || $message === '') {
    respond(
        400,
        false,
        'Tous les champs sont obligatoires.'
    );
}

if (mb_strlen($nom) > 100) {
    respond(
        400,
        false,
        'Le nom est trop long.'
    );
}

if (mb_strlen($email) > 254) {
    respond(
        400,
        false,
        'L’adresse e-mail est trop longue.'
    );
}

if (mb_strlen($message) > 5000) {
    respond(
        400,
        false,
        'Le message est trop long.'
    );
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    respond(
        400,
        false,
        'L’adresse e-mail n’est pas valide.'
    );
}

// --------------------------------------------------
// Protection supplémentaire de l'adresse Reply-To
// --------------------------------------------------

if (
    preg_match('/[\r\n]/', $nom) ||
    preg_match('/[\r\n]/', $email)
) {
    respond(
        400,
        false,
        'Données invalides.'
    );
}

// --------------------------------------------------
// Création de l'e-mail
// --------------------------------------------------

$mail = new PHPMailer(true);

try {

    // SMTP
    $mail->isSMTP();
    $mail->Host = $config['smtp']['host'];
    $mail->SMTPAuth = true;
    $mail->Username = $config['smtp']['username'];
    $mail->Password = $config['smtp']['password'];

    // Hostinger : SMTP sécurisé sur port 465
    $mail->SMTPSecure = PHPMailer::ENCRYPTION_SMTPS;
    $mail->Port = 465;

    // Pas de debug SMTP en production
    $mail->SMTPDebug = 0;

    // UTF-8
    $mail->CharSet = 'UTF-8';

    // --------------------------------------------------
    // Expéditeur
    // --------------------------------------------------

    // IMPORTANT :
    // Toujours utiliser ton adresse Hostinger comme expéditeur.
    $mail->setFrom(
        $config['mail']['from'],
        $config['mail']['from_name']
    );

    // --------------------------------------------------
    // Destinataire
    // --------------------------------------------------

    $mail->addAddress(
        $config['mail']['to']
    );

    // --------------------------------------------------
    // Réponse au visiteur
    // --------------------------------------------------

    $mail->addReplyTo(
        $email,
        $nom
    );

    // --------------------------------------------------
    // Sujet
    // --------------------------------------------------

    $mail->Subject = "Nouveau message - Djodjo's Gallery";

    // --------------------------------------------------
    // Contenu HTML
    // --------------------------------------------------

    $safeNom = htmlspecialchars(
        $nom,
        ENT_QUOTES | ENT_SUBSTITUTE,
        'UTF-8'
    );

    $safeEmail = htmlspecialchars(
        $email,
        ENT_QUOTES | ENT_SUBSTITUTE,
        'UTF-8'
    );

    $safeMessage = nl2br(
        htmlspecialchars(
            $message,
            ENT_QUOTES | ENT_SUBSTITUTE,
            'UTF-8'
        )
    );

    $mail->isHTML(true);

    $mail->Body = "
        <h2>Nouveau message depuis Djodjo's Gallery</h2>

        <p>
            <strong>Nom :</strong><br>
            {$safeNom}
        </p>

        <p>
            <strong>Email :</strong><br>
            {$safeEmail}
        </p>

        <p>
            <strong>Message :</strong><br>
            {$safeMessage}
        </p>
    ";

    // --------------------------------------------------
    // Version texte
    // --------------------------------------------------

    $mail->AltBody =
        "Nouveau message depuis Djodjo's Gallery\n\n" .
        "Nom : {$nom}\n" .
        "Email : {$email}\n\n" .
        "Message :\n{$message}";

    // --------------------------------------------------
    // Envoi
    // --------------------------------------------------

    $mail->send();

    respond(
        200,
        true,
        'Votre message a bien été envoyé.'
    );

} catch (Exception $e) {

    // IMPORTANT :
    // Ne jamais envoyer $e->getMessage() au navigateur.
    // Cela pourrait révéler des informations internes.
    error_log(
        'Erreur formulaire contact : ' . $e->getMessage()
    );

    respond(
        500,
        false,
        "Une erreur est survenue lors de l'envoi."
    );
}