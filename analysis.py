import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

def generate_keyword_summary(analysis_data: dict, brand_name: str, keyword: str) -> dict:
    print(f"Generating JSON summary for keyword: '{keyword}'...")
    
    prompt = f"""
    Analyze the following data for the keyword "{keyword}" and the brand "{brand_name}".
    The data contains two sets of results: 'google_results' and 'youtube_results'.
    Data: {json.dumps(analysis_data, indent=2)}

    Your task is to calculate metrics for EACH source separately.

    1.  **For Google Search Results:**
        * **SoV (Mention-based):** `(Number of results mentioning "{brand_name}") / (Total Google results) * 100`
        * **SoPV (Sentiment-based):** `(Number of POSITIVE sentiment results for "{brand_name}") / (Total results mentioning "{brand_name}") * 100`

    2.  **For YouTube Results:**
        * **wSoV (Engagement-based):** `(Total views of videos mentioning "{brand_name}") / (Total views of all videos) * 100`
        * **SoPV (Sentiment-based):** `(Total views of POSITIVE sentiment videos for "{brand_name}") / (Total views of ALL videos mentioning "{brand_name}") * 100`

    Return a single JSON object containing separate keys for 'google_analysis' and 'youtube_analysis', and a final 'combined_insight'.
    Example: {{"keyword": "smart fan", "google_analysis": {{"sov": 10.0, "sopv": 75.0}}, "youtube_analysis": {{"wsov": 5.5, "sopv": 90.0}}, "combined_insight": "Brand has low visibility but high positive sentiment on both platforms."}}
    """
    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL_NAME", "gpt-4o"),
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.2
        )
        summary = json.loads(response.choices[0].message.content)
        print(f"JSON summary for '{keyword}' created.")
        return summary
    except Exception as e:
        print(f"Error generating JSON summary for '{keyword}': {e}")
        return {"keyword": keyword, "error": str(e)}


def generate_final_strategic_report(all_summaries: list, brand_name: str) -> str:
    print("Synthesizing all platform data into a final strategic report...")

    prompt = f"""
    You are the Head of Marketing Strategy at "{brand_name}". You have just received a comprehensive analysis covering both Google Search and YouTube for multiple keywords.
    Your task is to synthesize this multi-platform data into a single, high-level executive report.

    Here is the data from all keyword analyses:
    {json.dumps(all_summaries, indent=2)}

    Follow these steps:
    1.  **Executive Summary:** Summarize our brand's overall digital presence.
    2.  **Platform Performance Analysis:** Compare and contrast our performance on Google vs. YouTube. For example, are we stronger in text-based content (Google) or video content (YouTube)? Where is our sentiment better?
    3.  **Keyword Opportunity Analysis:** Identify the keywords where we have the biggest opportunity for growth on each platform.
    4.  **Overall Strategic Recommendations:** Provide 3 high-level, actionable recommendations that leverage the insights from comparing the two platforms. For example, "Create YouTube video reviews to address topics we rank well for on Google."

    Structure this as a polished, final markdown report.
    """
    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL_NAME", "gpt-4o"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        print("Final strategic report generated successfully.")
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating final report: {e}")
        return "Error: Could not generate the final strategic report."