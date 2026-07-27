// Lightbox (seulement si les éléments existent)
const lightbox = document.getElementById("lightbox");
const lightboxImg = document.getElementById("lightbox-img");

if (lightbox && lightboxImg) {
    document.querySelectorAll(".gallery-item img").forEach(img => {
        img.addEventListener("click", () => {
            lightbox.style.display = "flex";
            lightboxImg.src = img.src;
        });
    });

    lightbox.addEventListener("click", () => {
        lightbox.style.display = "none";
    });
}

// Contact form avec LOGS DE DEBUG
const form = document.getElementById("contact-form");
const statusText = document.getElementById("form-status");

if (form) {
    console.log("✅ Formulaire trouvé !");
    
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        console.log("🚀 Formulaire soumis !");
        
        const formData = new FormData(form);
        const data = {
            nom: formData.get('nom'),
            email: formData.get('email'),
            message: formData.get('message')
        };
        
        console.log("📝 Données récupérées:", data);
        
        if (statusText) {
            statusText.textContent = 'Envoi en cours...';
            statusText.className = 'status loading';
        }
        
        try {
            console.log("📡 Envoi vers API...");
            const response = await fetch('https://dzcfmjxc3b.execute-api.eu-north-1.amazonaws.com/prod/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            console.log("📨 Réponse reçue:", response.status, response.statusText);
            const result = await response.json();
            console.log("📋 Résultat:", result);
            
            if (response.ok) {
                if (statusText) {
                    statusText.textContent = result.message;
                    statusText.className = 'status success';
                }
                form.reset();
            } else {
                if (statusText) {
                    statusText.textContent = result.error || 'Erreur lors de l\'envoi';
                    statusText.className = 'status error';
                }
            }
        } catch (error) {
            console.error("❌ Erreur complète:", error);
            if (statusText) {
                statusText.textContent = 'Erreur de connexion';
                statusText.className = 'status error';
            }
        }
    });
} else {
    console.error("❌ Formulaire non trouvé ! Vérifiez l'ID 'contact-form'");
}

// Gallery (seulement si les éléments existent)
function randomizeGallery() {
    const items = document.querySelectorAll('.gallery-item');
    const gallery = document.querySelector('.gallery');
    if (!items.length || !gallery) return;

    const viewportHeight = window.innerHeight;
    gallery.style.height = `${viewportHeight}px`;

    const galleryWidth = gallery.clientWidth;
    const minSize = 300;
    const maxSize = 400;
    const margin = 20;

    items.forEach(item => {
        item.style.position = 'absolute';
        item.style.left = '0';
        item.style.top = '0';
        item.style.transform = 'none';
    });

    const avgWidth = (minSize + maxSize) / 2;
    const columns = Math.floor(galleryWidth / (avgWidth + margin));
    const rowHeight = maxSize * 1.2;

    let currentY = margin;
    let currentX = (galleryWidth - (columns * (avgWidth + margin) - margin)) / 2;

    items.forEach((item, index) => {
        const randomWidth = Math.floor(Math.random() * (maxSize - minSize + 1)) + minSize;
        const randomHeight = randomWidth * (0.75 + Math.random() * 0.3);
        item.style.width = `${randomWidth}px`;
        item.style.height = `${randomHeight}px`;

        const col = index % columns;
        const row = Math.floor(index / columns);
        const posX = currentX + col * (avgWidth + margin);
        const posY = currentY + row * rowHeight;

        item.style.left = `${posX}px`;
        item.style.top = `${posY}px`;
        item.style.transform = `rotate(${Math.floor(Math.random() * 10) - 5}deg)`;
    });
}

window.addEventListener('load', randomizeGallery);
window.addEventListener('resize', () => {
    setTimeout(randomizeGallery, 300);
});
