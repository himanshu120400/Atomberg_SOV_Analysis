import os
import json
import openai
from dotenv import load_dotenv
from agents.data_fetcher import fetch_Google_Search_results, fetch_youtube_results
from analysis import generate_keyword_summary, generate_final_strategic_report

def generate_related_keywords(seed_keyword: str, brand_name: str, num_keywords: int = 5) -> list:
    print(f"Brainstorming keywords related to '{seed_keyword}'")
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = f"""
    You are an expert SEO and marketing strategist for the brand "{brand_name}".
    Your task is to brainstorm a list of related search keywords based on the primary seed keyword: "{seed_keyword}".

    Think about different user intents:
    -   **Informational:** "how do smart fans work"
    -   **Commercial Investigation:** "best smart fan India", "{brand_name} vs competitor"
    -   **Long-tail:** "energy efficient smart fan with light and remote"

    Generate a list of {num_keywords} unique, high-value keywords.
    Return your response as a single, clean JSON array of strings.
    Example: ["keyword 1", "keyword 2", "keyword 3"]
    """
    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL_NAME", "gpt-4o"),
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.4
        )
        keyword_list = json.loads(response.choices[0].message.content)
        if isinstance(keyword_list, dict):
            for key, value in keyword_list.items():
                if isinstance(value, list):
                    print(f"Brainstormed Keywords: {value}")
                    return value
        elif isinstance(keyword_list, list):
             print(f"Brainstormed Keywords: {keyword_list}")
             return keyword_list
        
        raise ValueError("LLM did not return a list of keywords.")

    except Exception as e:
        print(f"Error generating keywords: {e}. Falling back to seed keyword.")
        return [seed_keyword]


class AtombergSOVOrchestrator:
    def __init__(self, brand_name, competitors):
        self.brand_name = brand_name
        self.competitors = competitors

    def analyze_single_keyword(self, keyword: str) -> dict:
        google_results = fetch_Google_Search_results(keyword)
        youtube_results = fetch_youtube_results(keyword)
        
        if not google_results and not youtube_results:
            return {"keyword": keyword, "error": "No data found on any platform."}
        
        analysis_data = {"google_results": google_results, "youtube_results": youtube_results}
        keyword_summary = generate_keyword_summary(
            analysis_data=analysis_data,
            brand_name=self.brand_name,
            keyword=keyword
        )
        return keyword_summary


if __name__ == '__main__':
    load_dotenv()
    ATOMBERG_BRAND = "Atomberg"
    ATOMBERG_COMPETITORS = ["Usha", "Havells", "Bajaj", "Orient", "Crompton"]
    SEED_KEYWORD = "smart fan"
    
    keywords_to_analyze = generate_related_keywords(SEED_KEYWORD, ATOMBERG_BRAND)

    orchestrator = AtombergSOVOrchestrator(
        brand_name=ATOMBERG_BRAND,
        competitors=ATOMBERG_COMPETITORS
    )
    
    all_keyword_summaries = []
    print("\n--- Starting Multi-Keyword SoV Analysis ---")
    for keyword in keywords_to_analyze:
        summary = orchestrator.analyze_single_keyword(keyword)
        all_keyword_summaries.append(summary)
        print("-" * 20)

    if all_keyword_summaries:
        final_report = generate_final_strategic_report(all_keyword_summaries, ATOMBERG_BRAND)
        
        print("\n\n" + "="*50)
        print("    Final Multi-Keyword Strategic Report")
        print("="*50 + "\n")
        print(final_report)
    else:
        print("No data was analyzed. Final report could not be generated.")