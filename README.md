# Atomberg Share of Voice (SoV) Analysis Agent

This project is an AI-powered analysis tool designed to automatically measure and report on the digital Share of Voice (SoV) for the brand Atomberg. It analyzes search results from multiple platforms to provide strategic insights for the marketing and content teams.

## Features

* **Dynamic Keyword Generation:** Starts with a single "seed" keyword (e.g., "smart fan") and uses an AI to brainstorm a list of related, high-value keywords to analyze.
* **Multi-Platform Analysis:** Fetches and analyzes top search results from both **Google Search** (for web content) and **YouTube** (for video content and engagement).
* **Advanced Metrics:** Calculates key performance indicators:
    * **Simple SoV:** Measures brand visibility based on mention count.
    * **Weighted SoV (wSoV):** Measures brand influence based on YouTube video views.
    * **Share of Positive Voice (SoPV):** Measures brand perception using sentiment analysis.
* **Automated Strategic Reporting:** Synthesizes all findings into a final, comprehensive markdown report that includes a situational analysis and actionable recommendations.

## Tech Stack

* **Core Language:** Python
* **AI & Language Models:** OpenAI (GPT-4o)
* **Data Fetching:** SerpApi (for Google and Youtube results)
* **Orchestration:** A custom procedural orchestrator (`main.py`) manages the workflow.

## Setup and Usage

Follow these steps to set up and run the project locally.

### 1. Prerequisites

* Python 3.8+
* An OpenAI API Key
* A SerpApi API Key

### 2. Installation

Clone the repository and navigate into the project directory.

```bash
# Create a virtual environment
python -m venv .venv

# Activate the environment
# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# On macOS/Linux:
# source .venv/bin/activate

# Install the required packages
pip install -r requirements.txt
