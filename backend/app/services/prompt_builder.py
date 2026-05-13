import re
from dataclasses import dataclass


TECHNICAL_REPLACEMENTS = {
    "Ollama": "TravelSense AI",
    "ollama": "TravelSense AI",
    "Qwen2.5": "TravelSense AI",
    "qwen2.5": "TravelSense AI",
    "Qwen": "TravelSense AI",
    "qwen": "TravelSense AI",
}


@dataclass(frozen=True)
class MessageAnalysis:
    """Lightweight travel context extracted before prompting the local model."""

    language: str
    emotion: str
    intent: str
    entities: dict[str, str]
    missing_context: list[str]


def analyze_message(message: str) -> MessageAnalysis:
    """Extract simple signals that make a small local model answer more consistently."""

    normalized = message.lower()
    destination_mentions = _extract_destinations(message)
    entities = {
        "duration": _extract_duration(message),
        "budget": _extract_budget(normalized),
        "destination": destination_mentions[0] if destination_mentions else "",
        "destinations": ", ".join(destination_mentions) if len(destination_mentions) > 1 else "",
        "travel_style": _extract_travel_style(normalized),
        "people": _extract_people(message),
        "season": _extract_season(normalized),
    }
    cleaned_entities = {key: value for key, value in entities.items() if value}

    intent = _detect_intent(normalized, cleaned_entities)
    emotion = _detect_emotion(normalized)
    missing_context = _detect_missing_context(intent, cleaned_entities)

    return MessageAnalysis(
        language=_detect_language(normalized),
        emotion=emotion,
        intent=intent,
        entities=cleaned_entities,
        missing_context=missing_context,
    )


def build_travelsense_prompt(user_message: str) -> str:
    """Build a focused TravelSense prompt for Ollama's generate endpoint."""

    analysis = analyze_message(user_message)
    entity_lines = _format_entities(analysis.entities)
    missing_lines = _format_list(
        analysis.missing_context,
        fallback="aucune" if analysis.language == "french" else "none",
    )
    response_plan = _response_plan_for_intent(analysis.intent, analysis.language)
    output_format = _output_format_for_intent(analysis.intent, analysis.language)
    few_shot_example = _few_shot_example_for_intent(analysis.intent, analysis.language)
    example_section = (
        f"\n\nExemple court :\n{few_shot_example}"
        if analysis.language == "french" and few_shot_example
        else f"\n\nShort example:\n{few_shot_example}"
        if few_shot_example
        else ""
    )
    constraints = _format_list(
        _critical_constraints(analysis),
        fallback="aucune" if analysis.language == "french" else "none",
    )

    if analysis.language == "french":
        return f"""
Tu es TravelSense AI, un compagnon IA touristique premium et empathique.

Ton rôle :
- Aider le voyageur à planifier, comparer et optimiser ses voyages.
- Comprendre ses contraintes, préférences, émotions et incertitudes.
- Donner des recommandations claires en laissant la décision finale au voyageur.

Contexte détecté :
- langue : français
- intention : {analysis.intent}
- émotion : {analysis.emotion}
- éléments :
{entity_lines}
- informations manquantes :
{missing_lines}
- contraintes importantes :
{constraints}

Règles de réponse :
- Réponds en français.
- Ne mentionne jamais les détails techniques, modèles locaux, providers, API, datasets ou backend.
- Sois chaleureux, rassurant, concret et concis.
- Ne donne pas une checklist générique quand l'utilisateur demande une recommandation.
- Si l'utilisateur semble confus ou stressé, donne seulement 2 ou 3 options et simplifie l'étape suivante.
- Si des informations clés manquent, donne quand même une première aide utile, puis pose au maximum 3 questions courtes.
- Ne prétends jamais réserver, garantir les prix, la sécurité, les visas ou les horaires.
- Pour sécurité, visa et prix, conseille de vérifier des sources officielles ou actuelles.
- N'ajoute pas de jours de départ ou de retour sauf si l'utilisateur les demande.
- Évite les phrases génériques comme "en tant qu'IA".
- Utilise des titres courts.
- Utilise des listes numérotées quand tu compares plusieurs options.
- Évite les longs paragraphes.
- Une idée = une ligne courte.
- N'utilise pas de tableau.
- Ne dépasse pas 5 sections courtes.
- Termine toujours par une prochaine étape claire.
- Reste sous 170 mots sauf si l'utilisateur demande un itinéraire détaillé.

Plan de réponse pour cette intention :
{response_plan}

Format de sortie obligatoire :
{output_format}{example_section}

Message utilisateur :
\"\"\"{user_message.strip()}\"\"\"

Réponse TravelSense AI :
""".strip()

    return f"""
You are TravelSense AI, a premium and empathic AI travel companion.

Your job:
- Help the traveler plan, compare, and optimize trips.
- Understand constraints, preferences, emotion, and uncertainty.
- Give clear recommendations while keeping the final decision with the traveler.

Detected context:
- language: English
- intent: {analysis.intent}
- emotion: {analysis.emotion}
- entities:
{entity_lines}
- missing information:
{missing_lines}
- critical constraints:
{constraints}

Response rules:
- Answer in the same language as the user's message.
- Do not mention technical implementation, local models, providers, APIs, datasets, or backend details.
- Be warm, reassuring, concrete, and concise.
- Do not give a generic travel checklist when the user asks for recommendations.
- If the user seems confused or stressed, give only 2 or 3 options and simplify the next step.
- If key details are missing, still give a useful first recommendation, then ask up to 3 short questions.
- Never claim to book, reserve, or guarantee live prices, safety, visas, or opening hours.
- For safety, visa, and price-sensitive advice, recommend checking official or current sources.
- Prefer practical structure: short intro, recommended option or comparison, simple plan, next step.
- Avoid generic chatbot phrases such as "as an AI language model".
- Do not describe yourself as a system, tool, model, or recommendation engine.
- Use compact bullets. Do not use nested bullets unless the user asks for detail.
- Do not add departure or return travel days unless the user asks for them.
- Use short headings.
- Use numbered lists when comparing options.
- Avoid long paragraphs.
- One idea = one short line.
- Do not use tables.
- Maximum 5 short sections.
- Always end with a clear next step.
- Keep the answer under 170 words unless the user explicitly asks for a detailed itinerary.

Response plan for this intent:
{response_plan}

Required output format:
{output_format}{example_section}

User message:
\"\"\"{user_message.strip()}\"\"\"

TravelSense AI response:
""".strip()


def clean_assistant_response(response: str) -> str:
    """Remove common model artifacts before returning text to the frontend."""

    cleaned = re.sub(r"<think>.*?</think>", "", response, flags=re.IGNORECASE | re.DOTALL)
    cleaned = cleaned.strip()

    for original, replacement in TECHNICAL_REPLACEMENTS.items():
        cleaned = cleaned.replace(original, replacement)

    cleaned = re.sub(
        r"^\s*(Réponse TravelSense AI:|Reponse TravelSense AI:|TravelSense AI response:|Assistant:)\s*",
        "",
        cleaned,
        flags=re.IGNORECASE | re.MULTILINE,
    )
    cleaned = cleaned.replace("As an AI language model,", "I can help with that.")
    cleaned = cleaned.replace("as an AI language model,", "I can help with that.")
    cleaned = re.sub(r"[ \t]+$", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    return cleaned.strip()


def ensure_response_quality(response: str, analysis: MessageAnalysis) -> str:
    """Use a deterministic travel answer when the small model misses hard constraints."""

    if _fallback_reason(response, analysis):
        return _fallback_response(analysis)

    return response


def get_fallback_reason(response: str, analysis: MessageAnalysis) -> str | None:
    """Expose fallback diagnostics to the backend route without changing the response."""

    return _fallback_reason(response, analysis)


def _has_structure(response: str) -> bool:
    """Detect whether the answer is readable enough for the chat UI."""

    if re.search(r"^\s*\d+\.", response, flags=re.MULTILINE):
        return True

    useful_headings = [
        "Mon choix",
        "Prochaine étape",
        "Mes 3 meilleures options",
        "My pick",
        "Next step",
        "Best 3 options",
        "Itinéraire proposé",
        "Suggested itinerary",
    ]
    if any(heading.lower() in response.lower() for heading in useful_headings):
        return True

    readable_lines = [line for line in response.splitlines() if line.strip()]
    return len(readable_lines) >= 4


def _needs_fallback(response: str, analysis: MessageAnalysis) -> bool:
    return _fallback_reason(response, analysis) is not None


def _fallback_reason(response: str, analysis: MessageAnalysis) -> str | None:
    text = response.lower()
    stripped = response.strip()

    if not stripped:
        return "empty_response"

    if len(stripped) < 20:
        return "too_short"

    if any(
        marker in text
        for marker in [
            "destination -",
            "recommendation system",
            "as an ai language model",
            "ollama",
            "qwen",
            "backend",
            "provider",
            "dataset",
            " api ",
            "[destination",
            "[option",
            "[short",
            "[une ",
        ]
    ):
        return "technical_or_placeholder_artifact"
    if re.search(r"\[[^\]]+\]", response):
        return "placeholder_artifact"

    paragraph_heavy = len(response) > 420 and len([line for line in response.splitlines() if line.strip()]) <= 2
    if analysis.intent != "general_travel_advice" and paragraph_heavy and not _has_structure(response):
        return "broken_unstructured_response"

    wrong_language = _wrong_language_reason(response, analysis)
    if wrong_language:
        return wrong_language

    destination = analysis.entities.get("destination", "")
    if destination and analysis.intent in {"itinerary_request", "activity_search", "safety_question"}:
        if _destination_ignored(response, destination):
            return "detected_destination_ignored"

    if analysis.intent == "itinerary_request":
        if analysis.language == "french" and any(
            marker in text for marker in ["aéroport", "aeroport", "vol ", "vols", "paris", "retour", "voiture pour lisbonne"]
        ):
            return "invented_origin_or_travel_logistics"

    return None


def _wrong_language_reason(response: str, analysis: MessageAnalysis) -> str | None:
    text = response.lower()

    if analysis.language == "french":
        french_markers = [
            " le ",
            " la ",
            " les ",
            " des ",
            " pour ",
            "avec",
            "jour",
            "prochaine",
            "budget",
            "itinéraire",
            "sécurité",
            "à ",
            "é",
        ]
        english_markers = [" the ", " with ", " day ", " next step", " budget tip", " suggested itinerary"]
        if not any(marker in text for marker in french_markers) and any(marker in text for marker in english_markers):
            return "wrong_language"

    if analysis.language == "english":
        french_markers = [" le ", " la ", " les ", " avec ", " jour ", " prochaine étape", " itinéraire", " sécurité"]
        english_markers = [" the ", " with ", " day ", " next", " budget", " trip", " travel"]
        if not any(marker in text for marker in english_markers) and any(marker in text for marker in french_markers):
            return "wrong_language"

    return None


def _destination_ignored(response: str, destination: str) -> bool:
    expected = _normalize_destination(destination)
    if not expected:
        return False

    response_destinations = {_normalize_destination(item) for item in _extract_destinations(response)}
    if expected in response_destinations:
        return False

    return expected not in _normalize_destination(response)


def _fallback_response(analysis: MessageAnalysis) -> str:
    if analysis.language == "french":
        return _fallback_response_fr(analysis)

    return _fallback_response_en(analysis)


def _fallback_response_en(analysis: MessageAnalysis) -> str:
    if analysis.intent == "destination_recommendation":
        return (
            "No worries, we can narrow this down to 3 clear options.\n\n"
            "Best 3 options\n\n"
            "1. Lisbon, Portugal\n"
            "Why: cultural, walkable, and easy to organize on a medium budget.\n"
            "Budget: medium\n"
            "Pace: relaxed over 5 days.\n\n"
            "2. Istanbul, Turkey\n"
            "Why: history, food, and very different neighborhoods.\n"
            "Budget: medium to accessible\n"
            "Pace: immersive but manageable.\n\n"
            "3. Rome, Italy\n"
            "Why: museums, ruins, and architecture.\n"
            "Budget: medium to high\n"
            "Pace: rich but more intense.\n\n"
            "My pick\n"
            "Lisbon, if you want a cultural trip that feels clear and simple to plan.\n\n"
            "Next step\n"
            "Do you prefer museums, local food, or historic streets?"
        )

    if analysis.intent == "itinerary_request":
        destination = analysis.entities.get("destination", "the destination")
        days = _duration_days(analysis.entities.get("duration", "")) or 3
        return _build_itinerary(destination, days, "english")

    if analysis.intent == "destination_comparison":
        return (
            "Here is the short version so you can choose calmly.\n\n"
            "Comparison\n"
            "1. Rome - Strengths: museums, ruins, and classic history. Limitation: busier and pricier. Best for: deep culture.\n"
            "2. Lisbon - Strengths: walkable, warm, and easier on budget. Limitation: fewer major ancient sites. Best for: relaxed culture.\n\n"
            "Recommendation\n"
            "Choose Rome for iconic history, or Lisbon for a simpler and lighter trip.\n\n"
            "Next step\n"
            "What matters more to you: budget, museums, or relaxed pacing?"
        )

    if analysis.intent == "budget_optimization":
        return (
            "You can keep the trip comfortable without overspending.\n\n"
            "Budget plan\n"
            "- Save on: public transport, simple local meals, and free viewpoints.\n"
            "- Do not over-save on: location and late-night transport.\n"
            "- Priority: book a well-located stay and limit paid attractions.\n\n"
            "Next step\n"
            "Share your destination and daily budget, and I will make it more precise."
        )

    if analysis.intent == "safety_question":
        destination = analysis.entities.get("destination", "your destination")
        return (
            f"It is smart to check safety before choosing {destination}.\n\n"
            "What to check\n"
            "- Stay in central, well-reviewed areas and avoid isolated streets late at night.\n"
            "- Check recent traveler feedback and local transport advice.\n"
            "- Check official and current sources before deciding.\n\n"
            "Next step\n"
            "Tell me if you are traveling solo, as a couple, or with family."
        )

    return (
        "I can help you make this simpler.\n"
        "- Share your destination or travel style.\n"
        "- Add your duration and budget.\n"
        "- I will turn it into a clear plan.\n\n"
        "Next step\n"
        "What destination are you considering?"
    )


def _fallback_response_fr(analysis: MessageAnalysis) -> str:
    if analysis.intent == "destination_recommendation":
        return (
            "Pas de panique, on va réduire le choix à 3 options claires.\n\n"
            "Mes 3 meilleures options\n\n"
            "1. Lisbonne, Portugal\n"
            "Pourquoi : culturelle, agréable à pied et adaptée à un budget moyen.\n"
            "Budget : moyen\n"
            "Rythme : tranquille sur 5 jours.\n\n"
            "2. Istanbul, Turquie\n"
            "Pourquoi : histoire, gastronomie et quartiers très variés.\n"
            "Budget : moyen à accessible\n"
            "Rythme : immersif mais faisable.\n\n"
            "3. Rome, Italie\n"
            "Pourquoi : musées, ruines et architecture.\n"
            "Budget : moyen à élevé\n"
            "Rythme : riche mais plus intense.\n\n"
            "Mon choix\n"
            "Lisbonne, si tu veux un voyage culturel clair et simple à organiser.\n\n"
            "Prochaine étape\n"
            "Tu préfères musées, cuisine locale ou quartiers historiques ?"
        )

    if analysis.intent == "itinerary_request":
        destination = analysis.entities.get("destination", "la destination")
        days = _duration_days(analysis.entities.get("duration", "")) or 3
        return _build_itinerary(destination, days, "french")

    if analysis.intent == "destination_comparison":
        return (
            "Voici la version courte pour choisir calmement.\n\n"
            "Comparaison\n"
            "1. Rome - Forces : musées, ruines et grande histoire. Limite : plus chère et plus intense. Idéal pour : culture profonde.\n"
            "2. Lisbonne - Forces : agréable à pied, chaleureuse et plus simple côté budget. Limite : moins de grands sites antiques. Idéal pour : culture détendue.\n\n"
            "Recommandation\n"
            "Choisis Rome pour l'histoire iconique, ou Lisbonne pour un voyage plus simple et fluide.\n\n"
            "Prochaine étape\n"
            "Tu privilégies le budget, les musées ou un rythme tranquille ?"
        )

    if analysis.intent == "budget_optimization":
        return (
            "Tu peux garder un voyage agréable sans trop dépenser.\n\n"
            "Plan budget\n"
            "- Économiser sur : transports publics, repas locaux simples et points de vue gratuits.\n"
            "- Ne pas trop économiser sur : localisation du logement et transport tard le soir.\n"
            "- Priorité : logement bien placé et peu d'activités payantes par jour.\n\n"
            "Prochaine étape\n"
            "Donne-moi ta destination et ton budget par jour pour affiner."
        )

    if analysis.intent == "safety_question":
        destination = analysis.entities.get("destination", "ta destination")
        return (
            f"C'est une bonne idée de vérifier la sécurité avant de choisir {destination}.\n\n"
            "À vérifier\n"
            "- Reste dans des zones centrales et bien notées.\n"
            "- Évite les rues isolées tard le soir et vérifie les transports locaux.\n"
            "- Consulte des sources officielles et actuelles avant de décider.\n\n"
            "Prochaine étape\n"
            "Tu voyages solo, en couple ou en famille ?"
        )

    return (
        "Je peux t'aider à simplifier ça.\n"
        "- Donne-moi une destination ou un style de voyage.\n"
        "- Ajoute la durée et le budget.\n"
        "- Je te prépare un plan clair.\n\n"
        "Prochaine étape\n"
        "Quelle destination tu envisages ?"
    )


def _build_itinerary(destination: str, days: int, language: str) -> str:
    days = max(1, min(days, 7))

    if language == "french":
        intro = f"Respire, on garde ça simple : voici un plan clair de {days} jours à {destination}."
        templates = [
            ("centre historique", "quartier local ou musée abordable", "balade panoramique"),
            ("marché local", "quartier créatif", "dîner simple dans une adresse locale"),
            ("promenade douce", "dernier quartier incontournable", "coucher de soleil ou café calme"),
            ("visite culturelle courte", "pause dans un parc", "soirée légère sans activité chère"),
            ("excursion proche et économique", "retour tranquille", "repas local simple"),
            ("quartier moins touristique", "boutiques locales", "promenade de nuit dans une zone animée"),
            ("matinée libre pour refaire ton coup de coeur", "déjeuner local", "fin de journée sans te presser"),
        ]
        lines = [intro, "", "Itinéraire proposé", ""]
        for index in range(days):
            morning, afternoon, evening = templates[index]
            lines.extend(
                [
                    f"Jour {index + 1}",
                    f"Matin : {morning}.",
                    f"Après-midi : {afternoon}.",
                    f"Soir : {evening}.",
                    "",
                ]
            )
        lines.extend(
            [
                "Astuce budget",
                "Marche, transports publics, snacks locaux et une seule activité payante par jour.",
                "",
                "Prochaine étape",
                "Je peux te transformer ça en planning heure par heure.",
            ]
        )
        return "\n".join(lines)

    intro = f"Take a breath, we can keep this simple: here is a clear {days}-day plan for {destination} on a careful budget."
    templates = [
        ("historic center", "local neighborhood or affordable museum", "scenic walk"),
        ("local market", "creative district", "simple local dinner"),
        ("slow morning walk", "final must-see area", "sunset viewpoint or calm cafe"),
        ("short cultural visit", "park break", "light evening without expensive activities"),
        ("nearby low-cost excursion", "easy return", "simple local meal"),
        ("less touristy area", "local shops", "evening walk in a lively district"),
        ("free morning for your favorite spot", "local lunch", "unhurried final evening"),
    ]
    lines = [intro, "", "Suggested itinerary", ""]
    for index in range(days):
        morning, afternoon, evening = templates[index]
        lines.extend(
            [
                f"Day {index + 1}",
                f"Morning: {morning}.",
                f"Afternoon: {afternoon}.",
                f"Evening: {evening}.",
                "",
            ]
        )
    lines.extend(
        [
            "Budget tip",
            "Walk, use public transport, eat local, and choose one paid attraction per day.",
            "",
            "Next step",
            "I can turn this into an hour-by-hour plan.",
        ]
    )
    return "\n".join(lines)


def _duration_days(duration: str) -> int | None:
    if not duration:
        return None

    match = re.search(r"\d{1,2}", duration)
    if not match:
        return None

    value = int(match.group(0))
    if any(unit in duration.lower() for unit in ["week", "semaine"]):
        return value * 7

    return value


def _detect_language(text: str) -> str:
    french_markers = [
        " je ",
        " veux ",
        " partir",
        " voyage",
        " jours",
        " petit budget",
        " budget moyen",
        " stressé",
        " stressée",
        " perdu",
        " où ",
        " à ",
        "séjour",
    ]
    padded = f" {text} "

    if any(marker in padded for marker in french_markers) or re.search(r"[àâçéèêëîïôûùüÿñæœ]", text):
        return "french"

    return "english"


def _critical_constraints(analysis: MessageAnalysis) -> list[str]:
    constraints = []
    entities = analysis.entities
    french = analysis.language == "french"

    if "duration" in entities:
        if french:
            constraints.append(f"Utiliser exactement cette durée : {entities['duration']}.")
        else:
            constraints.append(f"Use exactly this duration: {entities['duration']}.")

    if "destination" in entities:
        if french:
            constraints.append(f"Se concentrer sur cette destination : {entities['destination']}.")
        else:
            constraints.append(f"Focus on this destination: {entities['destination']}.")

    if "budget" in entities:
        if french:
            constraints.append(f"Traiter ce budget comme une contrainte : {entities['budget']}.")
        else:
            constraints.append(f"Treat this budget as a constraint: {entities['budget']}.")

    if analysis.intent == "itinerary_request" and "destination" in entities:
        if french:
            constraints.append("Supposer que le voyage commence dans la destination ; ne pas inventer une ville de départ.")
        else:
            constraints.append("Assume the traveler starts in the destination; do not invent origin-city travel.")

    return constraints


def _output_format_for_intent(intent: str, language: str) -> str:
    """Return a strict visible structure for each travel intent."""

    if language == "french":
        formats = {
            "destination_recommendation": (
                "[Une phrase courte et rassurante]\n\n"
                "Mes 3 meilleures options\n\n"
                "1. [Destination, pays]\n"
                "Pourquoi : [raison courte]\n"
                "Budget : [niveau budget]\n"
                "Rythme : [rythme conseillé]\n\n"
                "2. [Destination, pays]\n"
                "Pourquoi : [raison courte]\n"
                "Budget : [niveau budget]\n"
                "Rythme : [rythme conseillé]\n\n"
                "3. [Destination, pays]\n"
                "Pourquoi : [raison courte]\n"
                "Budget : [niveau budget]\n"
                "Rythme : [rythme conseillé]\n\n"
                "Mon choix\n"
                "[Recommandation courte]\n\n"
                "Prochaine étape\n"
                "[Une seule question finale]"
            ),
            "itinerary_request": (
                "[Une phrase courte, rassurante et pratique]\n\n"
                "Itinéraire proposé\n\n"
                "Jour 1\n"
                "Matin : [activité courte]\n"
                "Après-midi : [activité courte]\n"
                "Soir : [activité courte]\n\n"
                "Jour 2\n"
                "Matin : [activité courte]\n"
                "Après-midi : [activité courte]\n"
                "Soir : [activité courte]\n\n"
                "Astuce budget\n"
                "[Conseil court]\n\n"
                "Prochaine étape\n"
                "[Étape claire]"
            ),
            "destination_comparison": (
                "[Phrase courte]\n\n"
                "Comparaison\n"
                "1. [Option] - Forces : [court]. Limite : [court]. Idéal pour : [court].\n"
                "2. [Option] - Forces : [court]. Limite : [court]. Idéal pour : [court].\n"
                "3. [Option si utile] - Forces : [court]. Limite : [court]. Idéal pour : [court].\n\n"
                "Recommandation\n"
                "[Choix clair mais non imposé]\n\n"
                "Prochaine étape\n"
                "[Étape claire]"
            ),
            "budget_optimization": (
                "[Phrase courte]\n\n"
                "Plan budget\n"
                "- Économiser sur : [court]\n"
                "- Ne pas trop économiser sur : [court]\n"
                "- Priorité : [court]\n\n"
                "Prochaine étape\n"
                "[Étape claire]"
            ),
            "safety_question": (
                "[Phrase calme et prudente]\n\n"
                "À vérifier\n"
                "- [Conseil pratique sans garantie]\n"
                "- [Conseil pratique sans garantie]\n"
                "- Vérifie les sources officielles et actuelles avant de décider.\n\n"
                "Prochaine étape\n"
                "[Étape claire]"
            ),
            "general_travel_advice": (
                "[Réponse directe]\n"
                "- [Point 1]\n"
                "- [Point 2]\n"
                "- [Point 3 maximum]\n\n"
                "Prochaine étape\n"
                "[Étape claire]"
            ),
        }
        return formats.get(intent, formats["general_travel_advice"])

    formats = {
        "destination_recommendation": (
            "[One short reassuring sentence]\n\n"
            "Best 3 options\n\n"
            "1. [Destination, country]\n"
            "Why: [short reason]\n"
            "Budget: [budget level]\n"
            "Pace: [recommended pace]\n\n"
            "2. [Destination, country]\n"
            "Why: [short reason]\n"
            "Budget: [budget level]\n"
            "Pace: [recommended pace]\n\n"
            "3. [Destination, country]\n"
            "Why: [short reason]\n"
            "Budget: [budget level]\n"
            "Pace: [recommended pace]\n\n"
            "My pick\n"
            "[Short recommendation]\n\n"
            "Next step\n"
            "[One final question only]"
        ),
        "itinerary_request": (
            "[One short practical sentence]\n\n"
            "Suggested itinerary\n\n"
            "Day 1\n"
            "Morning: [short activity]\n"
            "Afternoon: [short activity]\n"
            "Evening: [short activity]\n\n"
            "Day 2\n"
            "Morning: [short activity]\n"
            "Afternoon: [short activity]\n"
            "Evening: [short activity]\n\n"
            "Budget tip\n"
            "[Short tip]\n\n"
            "Next step\n"
            "[Clear next step]"
        ),
        "destination_comparison": (
            "[Short sentence]\n\n"
            "Comparison\n"
            "1. [Option] - Strengths: [short]. Limitation: [short]. Best for: [short].\n"
            "2. [Option] - Strengths: [short]. Limitation: [short]. Best for: [short].\n"
            "3. [Option if useful] - Strengths: [short]. Limitation: [short]. Best for: [short].\n\n"
            "Recommendation\n"
            "[Clear but non-forcing recommendation]\n\n"
            "Next step\n"
            "[Clear next step]"
        ),
        "budget_optimization": (
            "[Short sentence]\n\n"
            "Budget plan\n"
            "- Save on: [short]\n"
            "- Do not over-save on: [short]\n"
            "- Priority: [short]\n\n"
            "Next step\n"
            "[Clear next step]"
        ),
        "safety_question": (
            "[Calm, careful sentence]\n\n"
            "What to check\n"
            "- [Practical advice with no guarantee]\n"
            "- [Practical advice with no guarantee]\n"
            "- Check official and current sources before deciding.\n\n"
            "Next step\n"
            "[Clear next step]"
        ),
        "general_travel_advice": (
            "[Direct answer]\n"
            "- [Point 1]\n"
            "- [Point 2]\n"
            "- [Point 3 maximum]\n\n"
            "Next step\n"
            "[Clear next step]"
        ),
    }
    return formats.get(intent, formats["general_travel_advice"])


def _few_shot_example_for_intent(intent: str, language: str) -> str:
    """Tiny examples only; the local model has limited context."""

    if intent != "destination_recommendation":
        return ""

    if language == "french":
        return (
            "Pas de panique, on garde seulement 3 options simples.\n\n"
            "Mes 3 meilleures options\n\n"
            "1. Lisbonne, Portugal\n"
            "Pourquoi : culture, marche facile et ambiance douce.\n"
            "Budget : moyen\n"
            "Rythme : tranquille.\n\n"
            "2. Rome, Italie\n"
            "Pourquoi : musées et sites historiques.\n"
            "Budget : moyen à élevé\n"
            "Rythme : intense.\n\n"
            "3. Istanbul, Turquie\n"
            "Pourquoi : histoire, quartiers vivants et gastronomie.\n"
            "Budget : moyen\n"
            "Rythme : immersif.\n\n"
            "Mon choix\n"
            "Lisbonne pour commencer sans te disperser.\n\n"
            "Prochaine étape\n"
            "Tu préfères musées, cuisine locale ou quartiers historiques ?"
        )

    return (
        "No worries, we can narrow this down to 3 clear options.\n\n"
        "Best 3 options\n\n"
        "1. Lisbon, Portugal\n"
        "Why: culture, walkability, and a calm pace.\n"
        "Budget: medium\n"
        "Pace: relaxed.\n\n"
        "2. Rome, Italy\n"
        "Why: museums and historic sites.\n"
        "Budget: medium to high\n"
        "Pace: intense.\n\n"
        "3. Istanbul, Turkey\n"
        "Why: history, lively neighborhoods, and food.\n"
        "Budget: medium\n"
        "Pace: immersive.\n\n"
        "My pick\n"
        "Lisbon if you want a clear and simple cultural trip.\n\n"
        "Next step\n"
        "Do you prefer museums, local food, or historic streets?"
    )


def _response_plan_for_intent(intent: str, language: str) -> str:
    if language == "french":
        plans = {
            "destination_recommendation": (
                "- Commence par une phrase rassurante.\n"
                "- Choisis exactement 3 vraies villes ou destinations adaptées au style et au budget.\n"
                "- Pour chaque destination, écris une ligne compacte : ville, pays, pourquoi c'est adapté, budget, rythme.\n"
                "- Bons exemples culturels : Lisbonne, Rome, Istanbul, Marrakech, Vienne, Barcelone, Athènes.\n"
                "- Termine par 'Mon choix :' puis 'Prochaine étape :' en une phrase courte."
            ),
            "itinerary_request": (
                "- Commence par une phrase rassurante et pratique.\n"
                "- Propose exactement le nombre de jours détecté, dans la destination détectée.\n"
                "- Pour chaque jour : matin, après-midi, soir en version courte.\n"
                "- Ajoute une note budget simple et une astuce pour réduire le stress.\n"
                "- Ne crée pas de jours supplémentaires."
            ),
            "destination_comparison": (
                "- Compare 2 ou 3 destinations en puces courtes.\n"
                "- Critères : adéquation, budget, ambiance, facilité, compromis principal.\n"
                "- Recommande une option gagnante sans décider à la place du voyageur."
            ),
            "budget_optimization": (
                "- Donne une stratégie budget réaliste et simple.\n"
                "- Dis où économiser et où éviter de trop économiser.\n"
                "- Si aucune destination n'est donnée, propose 2 ou 3 destinations abordables."
            ),
            "safety_question": (
                "- Garde un ton calme et prudent.\n"
                "- Donne des conseils pratiques sans garantie absolue.\n"
                "- Conseille de vérifier les recommandations officielles actuelles."
            ),
            "family_trip": (
                "- Priorise confort, sécurité, trajets courts et activités flexibles.\n"
                "- Suggère des zones ou activités adaptées aux familles.\n"
                "- Demande l'âge des enfants seulement si nécessaire."
            ),
            "activity_search": (
                "- Propose une liste compacte d'activités groupées par style.\n"
                "- Ajoute une idée locale ou moins évidente.\n"
                "- Termine par une méthode simple pour choisir."
            ),
            "general_travel_advice": (
                "- Donne une réponse directe et utile.\n"
                "- Si la demande est vague, propose un chemin de planification simple et pose une question."
            ),
        }

        return plans.get(intent, plans["general_travel_advice"])

    plans = {
        "destination_recommendation": (
            "- Start with one reassuring sentence.\n"
            "- Choose exactly 3 real named cities or destinations that fit the user's style and budget.\n"
            "- For each destination, write one compact line with: city, country, why it fits, budget fit, and pace.\n"
            "- Good cultural examples include Lisbon, Rome, Istanbul, Marrakech, Vienna, Barcelona, and Athens.\n"
            "- Do not copy placeholder words such as Destination, Budget, or Pace as the answer.\n"
            "- End with 'My pick:' and 'Next:' using one short sentence each.\n"
            "- Never answer by saying the user should first choose a destination."
        ),
        "itinerary_request": (
            "- Start with one practical sentence.\n"
            "- Give a compact day-by-day itinerary using exactly the detected duration and destination.\n"
            "- Include pacing, one local food/activity idea, and a budget note.\n"
            "- Do not create extra days.\n"
            "- End with one question only if a key detail is missing."
        ),
        "destination_comparison": (
            "- Compare 2 or 3 destinations in short bullets.\n"
            "- Use criteria: fit, budget, atmosphere, ease, and main tradeoff.\n"
            "- Pick a recommended winner, but keep the final decision with the traveler."
        ),
        "budget_optimization": (
            "- Give a realistic low-friction budget strategy.\n"
            "- Mention where to save and where not to over-save.\n"
            "- If no destination is given, suggest 2 or 3 budget-friendly destinations."
        ),
        "safety_question": (
            "- Use a calm and careful tone.\n"
            "- Give practical safety considerations, not guarantees.\n"
            "- Recommend checking official current travel advice before final decisions."
        ),
        "family_trip": (
            "- Prioritize comfort, safety, short transfers, and flexible activities.\n"
            "- Suggest family-friendly areas or activity types.\n"
            "- Ask about ages only if needed."
        ),
        "activity_search": (
            "- Suggest a compact list of activities grouped by style.\n"
            "- Include one local or less obvious idea.\n"
            "- End with a simple way to choose between them."
        ),
        "general_travel_advice": (
            "- Give a direct helpful answer.\n"
            "- If the request is vague, propose a simple planning path and ask one clarifying question."
        ),
    }

    return plans.get(intent, plans["general_travel_advice"])


def _detect_emotion(text: str) -> str:
    emotion_keywords = [
        ("confusion", ["confused", "lost", "perdu", "perdue", "je ne sais pas", "hesitate", "hésite"]),
        ("stress", ["stress", "stressed", "urgent", "anxious", "angoisse", "pression"]),
        ("worry", ["worried", "worry", "afraid", "peur", "inquiet", "inquiète", "safe", "sécurité"]),
        ("excitement", ["excited", "can't wait", "hâte", "trop content", "enthousiaste"]),
        ("frustration", ["frustrated", "annoyed", "marre", "frustré", "frustrée", "compliqué"]),
        ("curiosity", ["curious", "curieux", "curieuse", "discover", "découvrir", "explore"]),
    ]

    for emotion, keywords in emotion_keywords:
        if any(keyword in text for keyword in keywords):
            return emotion

    return "neutral"


def _detect_intent(text: str, entities: dict[str, str]) -> str:
    if any(keyword in text for keyword in ["compare", "comparison", "versus", "vs", "better", "which one", "comparer"]):
        return "destination_comparison"

    if any(keyword in text for keyword in ["itinerary", "programme", "itinéraire", "jour par jour", "day by day"]):
        return "itinerary_request"

    if any(keyword in text for keyword in ["safe", "safety", "danger", "security", "sécurité", "dangereux"]):
        return "safety_question"

    if any(keyword in text for keyword in ["family", "kids", "children", "famille", "enfants"]):
        return "family_trip"

    if any(keyword in text for keyword in ["activities", "things to do", "visit", "activités", "que faire", "visiter"]):
        return "activity_search"

    if "destination" in entities and "duration" in entities and any(
        keyword in text for keyword in ["plan", "trip", "travel", "go", "partir", "voyage", "séjour"]
    ):
        return "itinerary_request"

    if "destination" not in entities and (
        "travel_style" in entities
        or any(keyword in text for keyword in ["where", "destination", "recommend", "suggest", "où", "recommande", "partir"])
    ):
        return "destination_recommendation"

    if any(
        keyword in text
        for keyword in ["optimize budget", "reduce cost", "save money", "cheaper", "économiser", "optimiser", "réduire"]
    ):
        return "budget_optimization"

    intent_keywords = [
        ("itinerary_request", ["itinerary", "plan", "programme", "itinéraire", "jour par jour", "days in"]),
        ("destination_recommendation", ["where", "destination", "recommend", "suggest", "où", "recommande"]),
    ]

    for intent, keywords in intent_keywords:
        if any(keyword in text for keyword in keywords):
            return intent

    return "general_travel_advice"


def _extract_duration(message: str) -> str:
    patterns = [
        r"\b(\d{1,2})\s*[- ]?\s*(day|days|jour|jours|j)\b",
        r"\b(\d{1,2})\s*[- ]?\s*(week|weeks|semaine|semaines)\b",
        r"\b(for|pendant)\s+(\d{1,2})\s*(day|days|jour|jours|week|weeks|semaine|semaines)\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, message)
        if match:
            return match.group(0)

    return ""


def _extract_budget(text: str) -> str:
    budget_keywords = [
        ("low", ["low budget", "small budget", "cheap", "budget limité", "petit budget", "pas cher"]),
        ("medium", ["medium budget", "moderate budget", "budget moyen", "moyen"]),
        ("high", ["high budget", "luxury", "premium", "budget élevé", "luxe"]),
    ]

    for budget, keywords in budget_keywords:
        if any(keyword in text for keyword in keywords):
            return budget

    money_match = re.search(r"(\$|€|£|dt|tnd)\s?\d+|\d+\s?(\$|€|£|dt|tnd)", text, flags=re.IGNORECASE)
    if money_match:
        return money_match.group(0)

    return ""


def _extract_destination(message: str) -> str:
    destinations = _extract_destinations(message)
    return destinations[0] if destinations else ""


def _extract_destinations(message: str) -> list[str]:
    common_destinations = {
        "lisbon": "Lisbon",
        "lisbonne": "Lisbonne",
        "rome": "Rome",
        "istanbul": "Istanbul",
        "marrakech": "Marrakech",
        "paris": "Paris",
        "barcelona": "Barcelona",
        "barcelone": "Barcelone",
        "tunis": "Tunis",
        "tokyo": "Tokyo",
        "bali": "Bali",
        "dubai": "Dubai",
        "dubaï": "Dubaï",
    }
    found: list[str] = []
    normalized = message.lower()

    destination_pattern = "|".join(re.escape(destination) for destination in common_destinations)
    for match in re.finditer(rf"\b({destination_pattern})\b", normalized, flags=re.IGNORECASE):
        found.append(common_destinations[match.group(1).lower()])

    generic_words = {
        "the",
        "destination",
        "trip",
        "travel",
        "voyage",
        "séjour",
        "budget",
        "culture",
        "cultural",
    }
    patterns = [
        r"\b(?:to|in|for|dans|à|a|pour)\s+([A-ZÀ-Ý][\wÀ-ÿ'-]+(?:\s+[A-ZÀ-Ý][\wÀ-ÿ'-]+){0,2})",
    ]

    for pattern in patterns:
        match = re.search(pattern, message)
        if match:
            candidate = match.group(1).strip()
            if candidate.lower() not in generic_words:
                found.append(candidate)

    deduped = []
    seen = set()
    for destination in found:
        key = _normalize_destination(destination)
        if key and key not in seen:
            seen.add(key)
            deduped.append(destination)

    return deduped


def _normalize_destination(value: str) -> str:
    normalized = value.lower().strip()
    normalized = normalized.replace("dubaï", "dubai")
    normalized = normalized.replace("lisbonne", "lisbon")
    normalized = normalized.replace("barcelone", "barcelona")
    normalized = re.sub(r"[^a-z0-9]+", " ", normalized)
    return normalized.strip()


def _extract_travel_style(text: str) -> str:
    styles = [
        "culture",
        "cultural",
        "culturel",
        "culturelle",
        "beach",
        "plage",
        "nature",
        "adventure",
        "aventure",
        "family",
        "famille",
        "luxury",
        "luxe",
        "food",
        "gastronomie",
        "nightlife",
        "shopping",
        "relax",
        "romantic",
        "romantique",
    ]
    detected = [style for style in styles if style in text]
    return ", ".join(detected)


def _extract_people(message: str) -> str:
    patterns = [
        r"\b(\d{1,2})\s*(people|persons|personnes|amis|friends|adults|adultes)\b",
        r"\b(couple|solo|alone|seul|seule|family|famille)\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, message, flags=re.IGNORECASE)
        if match:
            return match.group(0)

    return ""


def _extract_season(text: str) -> str:
    seasons = [
        "spring",
        "summer",
        "autumn",
        "winter",
        "printemps",
        "été",
        "automne",
        "hiver",
        "june",
        "july",
        "august",
        "december",
        "juin",
        "juillet",
        "août",
        "décembre",
    ]
    detected = [season for season in seasons if season in text]
    return ", ".join(detected)


def _detect_missing_context(intent: str, entities: dict[str, str]) -> list[str]:
    missing = []

    if "destination" not in entities and intent in {
        "itinerary_request",
        "activity_search",
        "safety_question",
    }:
        missing.append("destination")

    if "duration" not in entities and intent in {
        "itinerary_request",
        "destination_recommendation",
        "destination_comparison",
    }:
        missing.append("duration")

    if "budget" not in entities and intent in {
        "destination_recommendation",
        "budget_optimization",
        "destination_comparison",
    }:
        missing.append("budget")

    if "travel_style" not in entities and intent == "destination_recommendation":
        missing.append("travel style")

    return missing


def _format_entities(entities: dict[str, str]) -> str:
    if not entities:
        return "  - none"

    return "\n".join(f"  - {key}: {value}" for key, value in entities.items())


def _format_list(items: list[str], fallback: str) -> str:
    if not items:
        return f"  - {fallback}"

    return "\n".join(f"  - {item}" for item in items)
