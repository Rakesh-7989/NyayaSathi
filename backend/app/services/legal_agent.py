from typing import Optional
from app.services.rag_pipeline import rag_pipeline


COMPLAINT_TEMPLATES = {
    "consumer": """తేదీ: {date}
నుండి: {name}, {address}
సంబంధించి: వినియోగదారుల ఫిర్యాదు

గౌరవనీయ అధికారులకు,
నేను {name}, {address} నివాసి. నేను {product_or_service} ను {date_of_purchase} న కొనుగోలు చేశాను.
{complaint_description}
కావున దయచేసి నా ఫిర్యాదును పరిగణించి తగిన చర్యలు తీసుకోవాల్సిందిగా విన్నవించుకుంటున్నాను.

{signature}""",
    "police": """తేదీ: {date}
నుండి: {name}, {address}
సంబంధించి: పోలీసు ఫిర్యాదు

గౌరవనీయ పోలీసు అధికారులకు,
నేను {name}, {address} నివాసి. ఈ క్రింది విషయాన్ని మీ దృష్టికి తీసుకురావడానికి ఈ ఫిర్యాదు సమర్పిస్తున్నాను:
{incident_description}

తేదీ: {incident_date}
స్థలం: {incident_place}
దయచేసి తగిన చర్యలు తీసుకోవాల్సిందిగా విన్నవించుకుంటున్నాను.

{signature}""",
    "legal_notice": """తేదీ: {date}
నుండి: {sender_name}, {sender_address}
ద్వారా: {lawyer_name} (వకీలు)
సంబంధించి: చట్టపరమైన నోటీసు

ప్రియమైన {recipient_name},
మీకు ఈ నోటీసు ద్వారా తెలియజేయడం జరుగుతున్నది:
{notice_description}

కావున {deadline_days} రోజులలోపు {demand} చేయవలసిందిగా మా క్లయింట్ తరపున నోటీసు ఇవ్వడం జరుగుతున్నది.
లేకపోతే చట్టపరమైన చర్యలు తీసుకోవలసి వస్తుంది.

{signature}""",
    "rti": """తేదీ: {date}
నుండి: {name}, {address}
సంబంధించి: RTI దరఖాస్తు

గౌరవనీయ ప్రజా సమాచార అధికారి గారికి,
నేను {name}, {address} నివాసి. RTI చట్టం 2005 ప్రకారం ఈ క్రింది సమాచారాన్ని అభ్యర్థిస్తున్నాను:
{information_requested}

దయచేసి {timeframe} రోజులలోపు సమాచారం అందించగలరు.

{signature}""",
    "cyber_crime": """తేదీ: {date}
నుండి: {name}, {address}
సంబంధించి: సైబర్ నేర ఫిర్యాదు

గౌరవనీయ సైబర్ క్రైమ్ అధికారులకు,
{incident_description}
ఇది సైబర్ నేరం కావున దయచేసి చర్యలు తీసుకోవాల్సిందిగా విన్నవించుకుంటున్నాను.

{signature}""",
    "labour": """తేదీ: {date}
నుండి: {name}, {address}
సంబంధించి: లేబర్ ఫిర్యాదు

గౌరవనీయ లేబర్ అధికారులకు,
నేను {company_name} లో {designation} గా పనిచేస్తున్నాను.
{complaint_description}
దయచేసి నా ఫిర్యాదును పరిగణించి తగిన చర్యలు తీసుకోవాల్సిందిగా విన్నవించుకుంటున్నాను.

{signature}""",
}


class LegalAgent:
    async def answer_legal_query(
        self,
        question: str,
        language: str = "te",
        user_context: Optional[dict] = None,
    ):
        result = await rag_pipeline.query(question, language=language)
        return result

    async def generate_complaint(
        self,
        complaint_type: str,
        details: dict,
        language: str = "te",
    ):
        import datetime
        template = COMPLAINT_TEMPLATES.get(complaint_type, "")
        if not template:
            return "ఈ రకం కంప్లయింట్ అందుబాటులో లేదు."
        filled = template.format(
            date=datetime.date.today().strftime("%d-%m-%Y"),
            signature=details.get("name", "మీ పేరు"),
            **details,
        )
        return filled

    async def analyze_document(self, text: str):
        import re
        risks = []
        missing = []
        suggestions = []

        if not text.strip():
            return {
                "summary": "డాక్యుమెంట్ ఖాళీగా ఉంది. దయచేసి సరైన డాక్యుమెంట్ అప్‌లోడ్ చేయండి.",
                "risks": [],
                "missing_clauses": [],
                "suggestions": [],
            }

        text_lower = text.lower()

        if "rent" in text_lower or "lease" in text_lower:
            risks.append("అద్దె పెంపుదల షరతు స్పష్టంగా లేదు")
            risks.append("నోటీసు పీరియడ్ సరిగా లేదు")
            missing.append("మెయింటెనెన్స్ బాధ్యతలు ఎవరికి అనే షరతు లేదు")
            missing.append("సెక్యూరిటీ డిపాజిట్ రీఫండ్ నిబంధన లేదు")
            suggestions.append("అద్దె పెంపుదల % లిమిట్ క్లియర్ గా పేర్కొనండి")
            suggestions.append("ద్వైపార్శ్విక నోటీసు పీరియడ్ 60 రోజులు ఉంచండి")
        elif "salary" in text_lower or "employment" in text_lower:
            risks.append("నోటీసు పీరియడ్ 30 రోజులు మాత్రమే")
            risks.append("కంపెనీకి అనుకూలంగా నాన్-కాంపీట్ క్లాజ్ ఉంది")
            missing.append("PF/ESI నిబంధనలు స్పష్టంగా లేవు")
            suggestions.append("నోటీసు పీరియడ్ 60 రోజులకు పెంచండి")
            suggestions.append("నాన్-కాంపీట్ క్లాజ్ ను తొలగించండి లేదా 6 నెలలకు పరిమితం చేయండి")
        elif "agreement" in text_lower or "contract" in text_lower:
            risks.append("చట్టపరమైన భాష అర్థం చేసుకోవడం కష్టం")
            risks.append("ఏకపక్ష షరతులు ఉన్నాయి")
            missing.append("వివాద పరిష్కార షరతు లేదు")
            missing.append("ఫోర్స్ మేజర్ క్లాజ్ లేదు")
            suggestions.append("సాధారణ భాషలో డాక్యుమెంట్ రాయించండి")
            suggestions.append("వివాదాలకు ఆర్బిట్రేషన్ షరతు జోడించండి")
        else:
            risks.append("డాక్యుమెంట్ టైప్ గుర్తించబడలేదు")
            suggestions.append("డాక్యుమెంట్ ను న్యాయ నిపుణులకు చూపించండి")

        return {
            "summary": f"డాక్యుమెంట్ లో {len(risks)} రిస్క్‌లు మరియు {len(missing)} మిస్సింగ్ క్లాజ్‌లు గుర్తించబడ్డాయి.",
            "risks": risks,
            "missing_clauses": missing,
            "suggestions": suggestions,
        }

    async def legal_health_check(self, responses: dict) -> dict:
        score = 0
        max_score = len(responses) * 10
        recommendations = []
        details = []

        for key, value in responses.items():
            if value is True:
                score += 10

        if max_score > 0:
            percentage = round((score / max_score) * 100)
        else:
            percentage = 0

        if percentage < 40:
            recommendations.append("🔴 మీ లీగల్ డాక్యుమెంట్లు చాలా మిస్ అవుతున్నాయి. వెంటనే సిద్ధం చేసుకోండి.")
            recommendations.append("PAN కార్డు, ఆధార్ లింక్ తప్పనిసరి.")
        elif percentage < 70:
            recommendations.append("⚠️ కొన్ని ముఖ్యమైన డాక్యుమెంట్లు లేవు.")
            recommendations.append("విల్ మరియు ఇన్సూరెన్స్ తప్పకుండా తీసుకోండి.")
        else:
            recommendations.append("✅ మంచి స్కోర్! మీరు లీగల్‌గా సిద్ధంగా ఉన్నారు.")
            recommendations.append("ప్రతి 6 నెలలకు ఒకసారి మీ డాక్యుమెంట్లు తాజాగా ఉన్నాయో లేదో చెక్ చేసుకోండి.")

        return {
            "score": percentage,
            "recommendations": recommendations,
            "details": details,
        }


legal_agent = LegalAgent()
