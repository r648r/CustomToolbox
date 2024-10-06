// Insérer le div avec deux textareas après l'élément <nav>
document.querySelector('nav')?.insertAdjacentHTML('afterend', `
    <div style="
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: #fff;
      padding: 10px;
      border: 1px solid #ccc;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      z-index: 1000;
      width: 750px; /* Ajusté pour accueillir deux textareas avec titres */
      max-width: 90%; /* Responsive */
      height: 300px;
      overflow: auto;
      border-radius: 8px;
      display: flex;
      flex-direction: column;
    ">
      <!-- Bouton de fermeture -->
      <button style="
        position: absolute;
        top: 10px;
        right: 10px;
        background: transparent;
        border: none;
        font-size: 20px;
        cursor: pointer;
      " onclick="this.parentElement.style.display='none'">&times;</button>
      
      <!-- Container pour les titres -->
      <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
        <!-- Titre pour le textarea rouge -->
        <h3 style="
          font-size: 16px;
          color: #000;
          margin: 0;
          width: 48%;
          text-align: left;
        ">Chemins Collectés</h3>
        
        <!-- Titre pour le textarea bleu -->
        <h3 style="
          font-size: 16px;
          color: #000;
          margin: 0;
          width: 48%;
          text-align: left;
        ">Next.js Path</h3>
      </div>
      
      <!-- Container pour les textareas -->
      <div style="display: flex; gap: 10px; flex: 1;">
        <!-- Textarea Rouge -->
        <textarea id="chemins-collectes-textarea" style="
          flex: 1;
          height: 100%;
          resize: none;
          border: 1px solid #f00;
          outline: none;
          font-family: monospace;
          font-size: 14px;
          background: #ffcccc;
          padding: 5px;
          border-radius: 4px;
        " readonly>Chargement des chemins collectés...</textarea>
        
        <!-- Textarea Bleu -->
        <textarea id="nextjs-path-textarea-blue" style="
          flex: 1;
          height: 100%;
          resize: none;
          border: 1px solid #00f;
          outline: none;
          font-family: monospace;
          font-size: 14px;
          background: #cce5ff;
          padding: 5px;
          border-radius: 4px;
        " readonly>Chargement des chemins Next.js...</textarea>
      </div>
    </div>
  `);
  
  // Fonction pour collecter les chemins et les afficher dans les textareas
  (function(){
      // Textarea Rouge : Chemins Collectés
      const textareaRed = document.getElementById('chemins-collectes-textarea');
      // Textarea Bleu : Next.js Path
      const textareaBlue = document.getElementById('nextjs-path-textarea-blue');
      
      // -------------------------
      // Remplissage de la Textarea Bleu avec __BUILD_MANIFEST.sortedPages
      // -------------------------
      try {
          // Vérifiez si __BUILD_MANIFEST est défini
          if (typeof __BUILD_MANIFEST !== 'undefined' && __BUILD_MANIFEST.sortedPages) {
              const sortedPagesJSON = JSON.stringify(__BUILD_MANIFEST.sortedPages, null, 2);
              textareaBlue.value = sortedPagesJSON;
          } else {
              textareaBlue.value = "La variable __BUILD_MANIFEST.sortedPages n'est pas disponible.";
              console.warn("__BUILD_MANIFEST.sortedPages n'est pas défini.");
          }
      } catch (error) {
          textareaBlue.value = "Erreur lors de la récupération de __BUILD_MANIFEST.sortedPages.";
          console.error("Erreur:", error);
      }
  
      // -------------------------
      // Remplissage de la Textarea Rouge avec le résultat de votre script personnalisé
      // -------------------------
      // Expression régulière pour extraire les chemins
      const regex = /(?<=(\"|\'|\\`))\/[a-zA-Z0-9_?&=\/\-\#\.]*?(?=(\"|\'|\\`))/g;
      const results = new Set(); // Utilisation d'un Set pour éviter les doublons
      const scripts = document.getElementsByTagName("script");
      const fetchPromises = [];
  
      // Parcours de tous les scripts pour extraire les chemins des sources
      for(let i = 0; i < scripts.length; i++){
          const src = scripts[i].src;
          if(src){
              const fetchPromise = fetch(src)
                  .then(response => response.text())
                  .then(text => {
                      const matches = text.matchAll(regex);
                      for(let match of matches) {
                          results.add(match[0]);
                      }
                  })
                  .catch(error => {
                      console.error("Une erreur est survenue lors du fetch de :", src, error);
                  });
              fetchPromises.push(fetchPromise);
          }
      }
  
      // Extraction des chemins directement présents dans le contenu de la page
      const pageContent = document.documentElement.outerHTML;
      const pageMatches = pageContent.matchAll(regex);
      for(const match of pageMatches) {
          results.add(match[0]);
      }
  
      // Après que tous les fetch soient terminés, mettre à jour la textarea rouge
      Promise.all(fetchPromises).then(() => {
          if(textareaRed){
              textareaRed.value = Array.from(results).join('\n');
          } else {
              console.error("Textarea Rouge introuvable !");
          }
      }).catch(error => {
          console.error("Une erreur est survenue lors de la collecte des chemins :", error);
          if(textareaRed){
              textareaRed.value = "Erreur lors de la collecte des chemins.";
          }
      });
  
  })();
  