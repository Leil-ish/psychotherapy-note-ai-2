# Clinical AI Prompt Engineer Take-Home Exercise - Supplemental Test Case: Risk Assessment

## Project Overview

This repository contains a supplemental test case conducted as part of the practical exercise for the Clinical AI Prompt Engineer role at Upheal. The goal of this specific sub-project was to validate the refined prompt (`prompt_v2.txt` from the main project) on a focused clinical scenario involving a suicide risk assessment. This tests the prompt's ability to handle critical safety-related content accurately.

## Methodology & Project Steps

The project followed these key steps:

1.  **Data Acquisition & Preparation:**
    * Selected and downloaded a short YouTube vignette depicting a suicide risk assessment using `yt-dlp`.
    * Extracted the audio track from the video.
    * Transcribed the audio using OpenAI's `Whisper` model (`medium` model size) to generate a text transcript.
    * Saved the cleaned transcript as `data/risk_assessment_transcript.txt`.

2.  **Prompt Implementation (Using Refined Prompt v2):**
    * Utilized the refined prompt (`prompt_v2.txt`) developed in the main iteration of the take-home exercise. This prompt includes strong constraints against visual hallucination and clear structuring for SOAP, MSE, and Risk Assessment sections.
    * Used Python (`scripts/01_generate_note.py`) and the Google Gemini API (`Gemini 2.0 Flash`) with `google-generativeai` library to generate a clinical note from the risk assessment transcript.
    * Saved the generated note as `outputs/risk_assessment_output.txt`.

3.  **Definition of Evaluation Criteria:**
    * The same evaluation criteria defined in the main project (see `evaluation/evaluation_criteria.txt`) were used, with a particular focus on **Criterion 1 (Clinical Accuracy)** and **Criterion 5 (Responsible Risk Assessment)** for this test case.

4.  **Output Analysis (Descriptive Statistics):**
    * Utilized a modified version of the Python script (`scripts/02_analyze_output.py`) using `textstat` to perform descriptive statistical analysis on the generated note (`outputs/risk_assessment_output.txt`), calculating:
        * Total Word Count & Sentence Count
        * Average Sentence Length
        * Flesch-Kincaid Grade Level & Flesch Reading Ease
        * Word Count per major section (SOAP, MSE, Risk)
        * Sentence Count per SOAP subsection (Subjective, Objective, Assessment, Plan)
    * The script prints results to the console, which were then copied to `outputs/analysis_results.csv` for this submission.

5.  **Evaluation of Risk Assessment Note:**
    * Evaluated the generated note (`outputs/risk_assessment_output.txt`) against the defined criteria (see `evaluation/evaluation_output.md`).
    * **Key Findings:** The refined prompt (`prompt_v2.txt`) performed excellently. It accurately captured the client's disclosure of suicidal ideation ("I don't even want to be alive") and other pertinent details from the vignette. The Risk Assessment section of the note was appropriately detailed, correctly identifying the presence of SI, assigning a high-risk level, and noting the need for immediate further assessment and safety planning. The note was free of visual hallucinations and maintained a professional tone.

## Technology Stack

* **Programming Language:** Python 3.11
* **LLM API:** Google Gemini API (Model: `Gemini 2.0 Flash`) via `google-generativeai` library
* **Audio Transcription:** OpenAI Whisper (`medium` model)
* **Audio Acquisition:** `yt-dlp`
* **Audio Processing:** `ffmpeg`
* **Text Analysis:** `textstat` library

## Repository Structure

├── data/
│   └── risk_assessment_transcript.txt # Cleaned transcript (Risk vignette)
│   └── risk_assessment_audio.mp3    # (Optional) Downloaded audio file
│
├── prompts/
│   └── prompt_v2.txt                # Refined prompt text used
│
├── scripts/
│   ├── 01_generate_note.py          # Python script to call Gemini API
│   └── 02_analyze_output.py         # Script for statistical analysis (single file mode)
│
├── outputs/
│   ├── risk_assessment_output.txt   # Clinical note from Risk transcript + prompt v2
│   └── analysis_results.csv         # Console output of stats for this note copied here
│
├── evaluation/
│   ├── evaluation_criteria.txt      # Definition of evaluation criteria
│   └── evaluation_output.md         # Evaluation notes for risk_assessment_output.txt
│
├── .gitignore                       # Standard Python gitignore
├── requirements.txt                 # Python package requirements
└── README.md                        # This file


## Setup and Usage

1.  **Clone Repository:** `git clone https://github.com/Leil-ish/psychotherapy-note-ai-2`
2.  **Install Requirements:** Ensure Python 3.11 and FFmpeg are installed. Then run: `pip install -r requirements.txt`
3.  **API Key:** Set your Google AI Studio API key as an environment variable: `$env:GOOGLE_API_KEY='YOUR_API_KEY'` (Windows PowerShell) or `export GOOGLE_API_KEY='YOUR_API_KEY'` (Linux/macOS).
4.  **Run Generation:**
    * To generate the risk assessment note: `python scripts/01_generate_note.py --prompt prompts/prompt_v2.txt --transcript data/risk_assessment_transcript.txt --output outputs/risk_assessment_output.txt --model gemini-2.0-flash`
5.  **Run Analysis:**
    * The script `scripts/02_analyze_output.py` requires the input filename as an argument for single file analysis.
    * Run: `python scripts/02_analyze_output.py outputs/risk_assessment_output.txt`
    * Copy the printed "Statistics for..." table from the console into `outputs/analysis_results.csv` (or a `.txt` file).

## Results & Discussion

This supplemental test case successfully validated the refined prompt (`prompt_v2.txt`) on a challenging clinical scenario focused on suicide risk assessment. The LLM, guided by the refined prompt, accurately extracted and presented the critical safety information, including direct client quotes about suicidal ideation. The generated Risk Assessment section was clinically appropriate, highlighting the high-risk level and the need for immediate intervention.

The prompt's constraints against visual hallucination were also effective with this new transcript. This demonstrates the robustness and improved accuracy of the refined prompt in handling sensitive and critical clinical information based solely on transcript data.
And here's the updated content for requirements.txt for both projects (it will be the same):