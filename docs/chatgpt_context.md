Je travaille sur un projet M1 Big Data / UGC et Digital Mobile nommé TravelSense AI.

========================
1. CAHIER DES CHARGES
========================

Sujet : Conception d’un compagnon IA intelligent dans le domaine du tourisme.

Le compagnon IA doit aller au-delà d’un simple chatbot. Il doit être capable de comprendre, conseiller, accompagner et interagir de manière naturelle et empathique avec l’utilisateur, en tenant compte du contexte et des émotions.

Exigences obligatoires :
- Collecte de données textuelles réelles : articles + commentaires issus des réseaux sociaux.
- Justification des sources choisies.
- Méthode de collecte.
- Stratégie marketing digitale :
  - diagnostic du marché actuel ;
  - benchmark des compagnons IA en général ;
  - benchmark dans le contexte touristique ;
  - segmentation du marché ;
  - au moins deux personas.
- Pipeline NLP :
  - nettoyage ;
  - prétraitement ;
  - représentation ;
  - analyse ;
  - classification.
- Tâches NLP :
  - sentiment analysis ;
  - classification ;
  - résumé ;
  - NER / extraction d’information.
- LLM obligatoire :
  - intégration d’un modèle de langage ;
  - prompt engineering ;
  - RAG recommandé ;
  - réponses contextualisées.
- Émotion et empathie obligatoires :
  - détection des émotions ;
  - adaptation de la réponse ;
  - rôle de conseiller intelligent.
- Application fonctionnelle :
  - interface ;
  - chatbot / compagnon IA ;
  - avatar si possible ;
  - modules NLP + LLM + émotion ;
  - stockage.

Livrables :
- Application fonctionnelle.
- Rapport : introduction, données, NLP, émotion, LLM, architecture, implémentation, résultats, discussion.
- Présentation de 10 à 15 minutes.

========================
2. POSITIONNEMENT DU PROJET
========================

Nom : TravelSense AI.

Domaine : tourisme digital / travel-tech.

TravelSense AI est lui-même le compagnon IA à développer. Ce n’est pas un outil qui analyse d’autres assistants IA pour l’utilisateur final.

Rôle produit :
TravelSense AI dialogue avec l’utilisateur, analyse son message, comprend ses besoins, contraintes et préférences, puis le guide dans :
- la planification ;
- la comparaison ;
- l’optimisation ;
- le choix de destination ;
- la création d’itinéraire ;
- la réassurance.

Exemple :
Utilisateur :
“J’ai 5 jours, un budget moyen, je veux une destination culturelle mais je suis perdu.”

TravelSense AI doit comprendre :
- durée : 5 jours ;
- budget : moyen ;
- préférence : culture ;
- émotion : confusion ;
- besoin : recommandation + comparaison + planification.

Puis il doit répondre avec un ton rassurant, proposer 2 ou 3 destinations, comparer les options et suggérer un plan clair.

Important :
L’analyse des opinions sur les “AI travel assistants” sert seulement à l’étude marketing / étude de perception. Ce n’est pas la mission produit directe de TravelSense AI. Cette analyse permet de comprendre comment les internautes perçoivent les assistants IA de voyage : utiles, pratiques, trop génériques, peu fiables, inspirants, etc., afin de mieux positionner TravelSense AI.

========================
3. PROBLÉMATIQUE
========================

Problématique retenue :
Les informations touristiques existent déjà, mais elles sont dispersées entre TikTok, Instagram, YouTube, Reddit, forums, Tripadvisor, Google Reviews, blogs, plateformes de réservation et moteurs de recherche.

Pour préparer un voyage, l’utilisateur doit consulter plusieurs sources afin d’obtenir une vision complète :
- avis ;
- prix ;
- sécurité ;
- itinéraires ;
- recommandations locales ;
- activités ;
- retours d’expérience.

Cette fragmentation crée :
- surcharge d’information ;
- avis contradictoires ;
- perte de temps ;
- stress de planification ;
- manque de personnalisation.

Problématique centrale :
Comment concevoir un compagnon IA touristique capable de comprendre l’utilisateur en conversation et de transformer des informations touristiques dispersées en recommandations de voyage claires, personnalisées et rassurantes ?

========================
4. OBJECTIFS
========================

Objectif produit :
Créer un compagnon IA touristique qui dialogue avec l’utilisateur et l’aide à planifier, comparer et optimiser son voyage.

Objectif utilisateur :
Réduire la confusion, gagner du temps, recevoir des recommandations adaptées et garder le contrôle final de la décision.

Objectif marketing :
Comprendre le marché, les segments, les attentes et les freins liés aux assistants IA dans le tourisme.

Objectif étude de perception :
Analyser les opinions des internautes sur les AI travel assistants afin d’identifier l’utilité perçue, les limites, les freins de confiance et les arguments de positionnement.

Objectif data :
Collecter des articles, commentaires réseaux sociaux, avis et contenus UGC pour soutenir l’analyse du marché et préparer les modules NLP/RAG.

========================
5. PRÉSENTATION / PARTIE MARKETING
========================

La présentation est destinée à une prof de digital marketing. Elle doit donc être structurée comme une vraie analyse marketing, pas seulement technique.

Structure générale souhaitée :
1. Cadrage du projet
2. Problématique
3. Objectifs
4. Diagnostic du marché
5. Tendances tourisme + IA
6. Benchmark général
7. Benchmark tourisme
8. Segmentation
9. Personas
10. Stratégie marketing digitale
11. Sources de données
12. Justification des sources
13. Méthode de collecte

Premières slides recommandées :
1. Titre — TravelSense AI
2. Cadrage
3. Cadrage général
4. Nature du projet : compagnon IA, pas chatbot
5. Périmètre : où intervient TravelSense AI ?
6. Problématique : information disponible mais dispersée
7. Proposition de valeur
8. Cas d’usage concret
9. Objectifs du projet
10. Transition vers le diagnostic marché

Proposition de valeur :
TravelSense AI aide les voyageurs à passer de :
“Je suis perdu, il y a trop d’informations”
à :
“J’ai un plan clair, adapté à mon profil et à mes contraintes.”

Phrase forte :
TravelSense AI ne décide pas à la place du voyageur : il l’aide à mieux décider.

Benchmark général :
- ChatGPT
- Gemini
- Claude
- Microsoft Copilot

Benchmark tourisme :
- Layla.ai
- Mindtrip
- Tripadvisor AI Trip Builder / Trips
- Expedia in ChatGPT
- KAYAK.ai

Insight important :
AI Trust Gap — les voyageurs acceptent l’IA pour inspirer, comparer et planifier, mais ils veulent garder le contrôle pour réserver ou décider. TravelSense AI doit donc être positionné comme compagnon d’aide à la décision, pas comme outil qui réserve automatiquement.

Segmentation :
- Jeunes voyageurs / étudiants
- Touristes internationaux
- Familles
- Voyageurs solo
- Voyageurs expérientiels
- Digital nomads

Personas à garder :
1. Lina, 22 ans, étudiante, budget limité, utilise TikTok, Instagram, YouTube Shorts, Google Maps. Elle veut organiser un court séjour avec ses amis sans dépasser son budget. Émotion : confusion/stress lié au budget.
2. Thomas, 31 ans, touriste international curieux, utilise Google, Tripadvisor, YouTube, Reddit, blogs et plateformes de réservation. Il veut une expérience culturelle et locale mais doute de la fiabilité des informations. Émotion : curiosité + inquiétude.

========================
6. DATASETS À CONSTRUIRE
========================

Il faut construire plusieurs datasets.

Dataset 1 — Articles touristiques pour RAG
Rôle :
Fournir une base documentaire fiable au LLM.

Sources :
- blogs de voyage ;
- guides touristiques ;
- sites institutionnels ;
- articles sur destinations ;
- articles travel-tech ;
- guides de villes ;
- contenus sur budget, sécurité, saisons, activités.

Colonnes :
doc_id, title, source, source_url, source_type, country, destination, language, category, content, summary, use_for_rag

Volume conseillé :
20 à 40 articles, 5 à 10 destinations, français + anglais.

Dataset 2 — Commentaires / avis UGC voyageurs
Rôle :
Pipeline NLP : sentiment, émotions, intention, thèmes, frustrations.

Sources :
- Tripadvisor ;
- Google Reviews ;
- Reddit ;
- YouTube ;
- TikTok ;
- forums voyage ;
- commentaires Instagram ;
- Booking reviews si accessibles.

Colonnes :
comment_id, text_raw, source, platform, source_type, destination, language, topic, sentiment_label, emotion_label, intent_label, date_collecte, url_source

Labels sentiment :
positive, neutral, negative

Labels émotion :
confusion, stress, curiosity, excitement, worry, frustration, satisfaction

Labels intention :
destination_recommendation, itinerary_request, comparison, budget_optimization, safety_question, family_trip, activity_search, general_advice

Volume conseillé :
300 à 500 commentaires/avis.

Dataset 3 — Catalogue structuré des destinations
Rôle :
Moteur de recommandation simple.

Colonnes :
destination, country, region, type, budget_level, ideal_duration, best_season, best_for, activities, transport_notes, safety_note, pros, cons

Exemples destinations :
Istanbul, Lisbonne, Rome, Bali, Tokyo, Tunis, Barcelone, Paris, Dubaï, Marrakech.

Dataset 4 — Opinions sur les AI travel assistants
Rôle :
Étude marketing / e-réputation / perception de l’utilité des AI travel assistants.

Sources :
- Reddit ;
- YouTube ;
- Product Hunt ;
- App Store ;
- Google Play ;
- articles reviews ;
- commentaires sur Layla.ai, Mindtrip, KAYAK.ai, Tripadvisor AI Trip Builder.

Colonnes :
id, text, source, platform, assistant_name, topic, sentiment_label, trust_level, usefulness_label, date_collecte, url_source

Topics :
usefulness, trust, accuracy, generic_recommendations, time_saving, booking_fear, planning_help

Volume conseillé :
100 à 200 opinions + 10 à 20 articles reviews.

Dataset 5 — Conversations de test
Rôle :
Tester l’assistant.

Colonnes :
test_id, user_message, expected_intent, expected_emotion, expected_entities, expected_behavior

Exemple :
User message :
“I have 5 days and I want a cultural trip but I’m confused”
Expected :
intent = destination_recommendation
emotion = confusion
entities = duration=5 days, preference=culture
behavior = reassure, compare 2-3 destinations, propose itinerary

Volume conseillé :
30 à 50 cas de test.

========================
7. STACK TECHNIQUE ACTUELLE
========================

Décision importante :
On n’utilise pas l’API OpenAI car elle est payante. On utilise un LLM local via Ollama.

LLM local :
- Ollama installé et fonctionnel.
- Modèle choisi : qwen2.5:0.5b
- Raison : modèle léger adapté au PC, car llama3.2 demandait trop de RAM.
- Test Ollama avec Python réussi.
- Backend communique avec Ollama.

Architecture :
Frontend React + Vite
↓
Backend FastAPI
↓
Ollama local
↓
Qwen2.5:0.5b
↓
Réponse assistant

Backend :
- FastAPI
- endpoint /chat fonctionnel
- POST http://127.0.0.1:8000/chat
- L’endpoint reçoit :
  { "message": "..." }
- L’endpoint retourne au minimum :
  {
    "user_message": "...",
    "assistant_response": "...",
    "provider": "ollama",
    "model": "qwen2.5:0.5b"
  }
- Côté UI, ne jamais afficher provider/model.

Frontend :
- React + Vite
- Interface web premium, pas Streamlit.
- Streamlit a été abandonné car l’objectif est une vraie web app pro.

========================
8. DIRECTION UI/UX ACTUELLE
========================

Objectif UI :
Créer une vraie web app premium d’AI travel companion, pas une interface universitaire, pas un dashboard technique.

Inspirations :
- Layla.ai pour l’expérience AI travel assistant.
- MonksTrip Travel Agency Landing Page sur Dribbble pour le style premium travel.
- Une référence “touri” fournie par image : interface immersive, dark glassmorphism, AI chat, cartes destinations.
- Mais l’interface a ensuite été simplifiée pour se rapprocher d’une expérience ChatGPT/Grok/Perplexity centrée sur le chat.

Palette finale :
- Deep Navy : #0A1931
- Mist Blue : #B3CFE5
- Ocean Blue : #4A7FA7
- Royal Navy : #1A3D63
- Snow White : #F6FAFD
- Accent optionnel très subtil : #E9C46A
- Interdiction : pas de rose/pink.

Design rules :
- Ne jamais afficher : Ollama, Qwen, LLM, backend, API provider, modèle, université, projet scolaire.
- Ne pas faire un dashboard.
- Ne pas faire une interface AI sloppy.
- Utiliser un style premium travel-tech.
- Utiliser typographie moderne type Plus Jakarta Sans, Manrope ou Inter.
- Garder un design minimal, respirant, moderne.
- Utiliser des transitions et motion légères.
- Les sections après le hero doivent avoir des backgrounds plus clairs, pas trop sombres.
- Réduire la saturation et éviter les effets trop forts.

Structure finale du site :
1. Navbar
2. Hero avec background travel image et chat centré
3. Destinations section
4. How it works
5. Reviews
6. Mobile app promo avec phone mockup + Coming soon
7. Footer

État hero actuel souhaité :
- Garder image de background travel.
- Garder overlay/blur/gradient, mais réduit : l’image doit rester visible.
- Supprimer la section droite “For You” dans le hero.
- Chat centré et prioritaire.
- Expérience proche ChatGPT/Grok :
  - greeting message ;
  - phrase support ;
  - suggestion chips ;
  - input large ;
  - icônes plus, attachment, voice, send.

Comportement chat :
Avant premier message :
- afficher greeting ;
- afficher phrase de support ;
- afficher suggestion chips ;
- afficher input.

Après premier message :
- masquer greeting ;
- masquer support sentence ;
- masquer suggestion chips ;
- passer en mode conversation plein écran/centré ;
- conversation devient l’élément principal ;
- input reste visible en bas ;
- messages scrollent dans la section, la page ne s’allonge pas indéfiniment.

Fonctionnalités chat ajoutées / souhaitées :
- New Chat button.
- Saved/old chats comme ChatGPT.
- possibilité de créer une nouvelle conversation.
- possibilité de revenir aux anciennes conversations.
- stockage local via localStorage pour l’instant.
- titres automatiques à partir du premier message.
- scroll interne pour conversation longue.
- input avec Enter pour envoyer, Shift+Enter pour nouvelle ligne si textarea.
- auto-scroll vers le dernier message.
- long chat ne doit pas faire grandir la première section : il faut un scroll interne.

Important CSS :
.messages-area {
  flex: 1;
  overflow-y: auto;
  min-height: 0;
}

========================
9. PLAN DE CODE À VENIR
========================

Ce qui est fait :
- Ollama fonctionne.
- qwen2.5:0.5b fonctionne.
- Backend FastAPI /chat fonctionne.
- Frontend React/Vite existe.
- UI a été fortement améliorée et est en cours de polish.
- Direction UI actuelle : AI chat website premium + travel-tech, centré sur chat.

Ce qui reste à faire ensuite :
1. Finaliser UI polish :
   - réduire blur/gradient du hero ;
   - enlever conteneurs inutiles ;
   - vérifier New Chat + saved chats ;
   - vérifier scroll interne ;
   - vérifier responsive mobile ;
   - vérifier sections light background ;
   - améliorer transitions/motion.
2. Ajouter modules NLP backend :
   - émotion ;
   - intention ;
   - extraction durée/budget/préférences/destinations ;
   - sentiment.
3. Ajouter catalogue destinations.
4. Ajouter datasets CSV initiaux.
5. Ajouter RAG simple :
   - articles_tourism.csv ;
   - chunking ;
   - embeddings ou fallback TF-IDF ;
   - récupération top 3 documents ;
   - contexte envoyé au LLM.
6. Adapter prompt TravelSense AI selon :
   - emotion ;
   - intent ;
   - entities ;
   - RAG context.
7. Ajouter stockage backend si besoin :
   - SQLite conversations ;
   - feedback utilisateur.
8. Ajouter rapport / documentation :
   - architecture ;
   - datasets ;
   - pipeline NLP ;
   - RAG ;
   - module émotion ;
   - résultats / tests.
9. Préparer scénarios de démo.

========================
10. PROMPT SYSTEME TRAVELSENSE AI
========================

Prompt système recommandé :

Tu es TravelSense AI, un compagnon IA touristique empathique.

Ton rôle est d’aider l’utilisateur à planifier, comparer et optimiser son voyage.
Tu dois comprendre ses besoins, contraintes, préférences et son état émotionnel.

Règles :
- répondre avec un ton rassurant et clair ;
- poser des questions si les informations sont insuffisantes ;
- adapter les recommandations au budget, à la durée et aux préférences ;
- expliquer pourquoi chaque recommandation est pertinente ;
- ne pas décider à la place de l’utilisateur ;
- ne pas réserver à la place de l’utilisateur ;
- garder le contrôle final à l’utilisateur ;
- si l’utilisateur est stressé, simplifier et rassurer ;
- si l’utilisateur est confus, proposer peu d’options et structurer la réponse ;
- si l’utilisateur est inquiet, répondre prudemment et recommander de vérifier les sources officielles.

========================
11. MODULE ÉMOTION
========================

Émotions à détecter :
- confusion
- stress
- worry / inquiétude
- excitement / excitation
- frustration
- curiosity / curiosité
- neutral

Adaptation :
confusion → simplifier, 2-3 options max, structure claire.
stress → rassurer, étapes simples.
worry → ton prudent, conseils de vérification.
excitement → ton positif et énergique.
frustration → reconnaître la difficulté, réduire la complexité.
curiosity → donner plus d’explications et suggestions.

========================
12. MODULE INTENTION
========================

Intentions à détecter :
- destination_recommendation
- itinerary_request
- destination_comparison
- budget_optimization
- safety_question
- family_trip
- activity_search
- general_travel_advice

Entités à extraire :
- duration
- budget
- destination mentions
- travel style : culture, beach, nature, adventure, family, luxury, budget, food
- people_count si possible
- season si possible

========================
13. RAG
========================

RAG signifie Retrieval-Augmented Generation.
Dans ce projet, le RAG permet à TravelSense AI de répondre à partir d’une base documentaire touristique construite avec des articles, avis et guides collectés.

Fonctionnement :
1. Collecter articles/guides/avis.
2. Nettoyer les textes.
3. Découper en chunks.
4. Créer embeddings ou TF-IDF.
5. Stocker dans une base vectorielle ou système de recherche.
6. Quand l’utilisateur pose une question, récupérer les passages pertinents.
7. Envoyer le contexte au LLM.
8. Générer une réponse contextualisée.

RAG n’est pas strictement obligatoire dans l’énoncé, mais il est “recommandé”, donc mieux vaut l’intégrer même simplement.

Version simple possible :
- articles_tourism.csv
- destinations_catalog.csv
- fallback TF-IDF retrieval si Chroma/FAISS trop compliqué.

========================
14. IMPORTANT POUR LA SUITE
========================

Quand je continue dans un nouveau chat, il faut m’aider à avancer étape par étape.

Ne pas redonner de grands prompts Codex inutilement sauf si demandé.
Ne pas revenir à Streamlit.
Ne pas proposer OpenAI API payante sauf si demandé.
Ne pas afficher d’infos techniques dans le frontend.
Ne pas refaire tout le projet de zéro.
Toujours garder TravelSense AI comme vraie web app premium de compagnon IA touristique.

Si on continue côté code, il faut travailler par milestones :
1. UI final polish.
2. NLP backend.
3. datasets.
4. RAG.
5. prompt empathique.
6. stockage.
7. tests.
8. rapport et démo.

Si on continue côté présentation/rapport, utiliser le cadrage marketing et technique expliqué ci-dessus.