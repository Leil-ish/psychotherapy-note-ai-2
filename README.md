# Clinical AI Prompt Engineer Take-Home Exercise - Upheal

## Project Overview

This repository contains the submission for the practical exercise component of the interview process for the Clinical AI Prompt Engineer role at Upheal. The goal of this project was to demonstrate the ability to acquire clinical data (a therapy session transcript), design and implement prompts for a Large Language Model (LLM) to generate structured clinical notes (SOAP, MSE, Risk Assessment), evaluate the output using defined clinical criteria, perform comparative analysis, and iteratively refine the prompt for improved quality based on that evaluation. The project also includes a supplemental test case using a focused risk assessment vignette to further validate the refined prompt.

## Methodology & Project Steps

The project followed these key steps:

1.  **Data Acquisition & Preparation (Annabeth Session):**
    * Selected and downloaded a therapeutic session video ("Annabeth" session) from YouTube using `yt-dlp`.
    * Extracted the audio track from the video.
    * Transcribed the audio using OpenAI's `Whisper` model (`medium` model size) to generate a text transcript.
    * Saved the cleaned transcript as `data/risk_assessment_transcript.txt`.

2.  **Initial Prompt Design & Implementation (v1):**
    * Designed a structured zero-shot prompt (`prompts/prompt_v2.txt`) for the Google Gemini API (using `gemini--flash-latest`) instructing it to generate a clinical note including:
        * SOAP Note (Subjective, Objective, Assessment, Plan)
        * Mental Status Examination (MSE)
        * Risk Assessment
    * Defined the expected information for each section and included constraints against inference and for professional tone.
    * Used Python (`scripts/01_generate_note.py`) and the `google-generativeai` library to generate the first version of the clinical note (`outputs/output_v1.txt`).

3.  **Definition of Evaluation Criteria:**
    * Defined the following criteria for clinical evaluation of the generated note's quality:
        * **Criterion 1:** Clinical Accuracy: Does the note accurately reflect likely details from the transcript without hallucinating facts or making unsupported interpretations?
        * **Criterion 2:** Professional Tone & Objectivity: Does the tone match what would be expected from an experienced clinician AEB being nonjudgmental, objective, and appropriately detailed?
        * **Criterion 3:** Completeness: Are all requested sections (SOAP, MSE, Risk) present and appropriately addressed based on transcript content?
        * **Criterion 4:** Clinical Relevance/Salience: Does the note capture clinically significant information vs. conversational filler?
        * **Criterion 5:** Responsible Risk Assessment: Are safety related details highlighted in a way that makes them easily accessible and clinically appropriate?

4.  **Output Analysis (Descriptive Statistics):**
    * Developed a Python script (`scripts/02_analyze_output.py`) using `textstat` to perform descriptive statistical analysis on generated notes, calculating