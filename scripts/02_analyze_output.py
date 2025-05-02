import pathlib
import re
import textstat
import sys
import argparse # Import argparse for command-line arguments

# --- Helper Functions (Keep these as they were) ---

def parse_sections(text):
    """
    Parses the clinical note text into major sections using regex.
    Handles headings that might be at the very start of the file.
    Assumes headings like **1. SOAP Note:**, **2. ...**, **3. ...**
    """
    sections = {'SOAP': '', 'MSE': '', 'Risk': '', 'Header': '', 'Other': ''}
    # Regex to find the start of each main section heading
    # Allows matching at start of string (\A) OR after a newline (\n)
    pattern = r'(?:\n|\A)\s*\*\*(\d\.\s*(?:SOAP Note|Mental Status Examination \(MSE\)|Risk Assessment))\*\*\s*\n?'

    matches = list(re.finditer(pattern, text))

    if not matches:
        # If no major sections found, treat whole text as SOAP for analysis purposes maybe? Or just 'Other'.
        # This might happen if analyzing just a subsection snippet.
        print("Warning: Could not find standard section headings (SOAP, MSE, Risk). Analyzing full text.", file=sys.stderr)
        # Assign based on common starting point, or fallback to 'Other'
        if text.strip().startswith("* **Subjective:**"):
             sections['SOAP'] = text.strip()
        elif text.strip().startswith("* **Appearance:**"):
             sections['MSE'] = text.strip()
        elif text.strip().startswith("* **Suicidal Ideation (SI):**"):
             sections['Risk'] = text.strip()
        else:
            sections['Other'] = text.strip()
        return sections # Return early if no standard sections found

    # --- Logic to parse sections if headings *are* found ---
    first_match_start = matches[0].start()
    if first_match_start > 0:
        sections['Header'] = text[:first_match_start].strip()
    else:
         sections['Header'] = ''

    for i, match in enumerate(matches):
        start_pos = match.end()
        end_pos = matches[i+1].start() if (i + 1) < len(matches) else len(text)
        section_text = text[start_pos:end_pos].strip()
        heading_text = match.group(1).lower() # The captured heading text like "1. soap note"

        if 'soap note' in heading_text:
            sections['SOAP'] = section_text
        elif 'mental status examination' in heading_text:
            sections['MSE'] = section_text
        elif 'risk assessment' in heading_text:
            sections['Risk'] = section_text
        else:
            # Capture unexpected sections if any
            sections['Other'] += section_text + "\n"

    sections['Other'] = sections['Other'].strip() # Clean up 'Other' section
    return sections


def calculate_stats(file_path):
    """
    Loads text from a file, parses sections AND SOAP subsections using
    robust line-by-line checking, and calculates statistics.
    """
    try:
        print(f"\n--- Analyzing File: {file_path.name} ---")
        with open(file_path, 'r', encoding='utf-8') as f:
            full_text = f.read()

        if not full_text or full_text.startswith("Error:"):
             print(f"Skipping analysis for {file_path.name} due to error content or empty file.")
             return None

        # Parse major sections first using regex
        sections = parse_sections(full_text)
        stats = {}

        # --- Basic counts on full text ---
        stats['Total Word Count'] = len(full_text.split())
        stats['Total Sentence Count'] = textstat.sentence_count(full_text)
        stats['Average Sentence Length'] = round(textstat.avg_sentence_length(full_text), 2)

        # --- Readability (on full text) ---
        stats['Flesch-Kincaid Grade'] = textstat.flesch_kincaid_grade(full_text)
        stats['Flesch Reading Ease'] = textstat.flesch_reading_ease(full_text)

        # --- Word counts per MAJOR section ---
        stats['Word Count SOAP'] = len(sections.get('SOAP', '').split()) if sections.get('SOAP') else 0
        stats['Word Count MSE'] = len(sections.get('MSE', '').split()) if sections.get('MSE') else 0
        stats['Word Count Risk'] = len(sections.get('Risk', '').split()) if sections.get('Risk') else 0
        # Add count for 'Other' if section parsing failed
        if not stats['Word Count SOAP'] and not stats['Word Count MSE'] and not stats['Word Count Risk']:
             stats['Word Count Other/Full'] = len(sections.get('Other', '').split()) if sections.get('Other') else 0


        # --- Parse SOAP Subsections using robust line checking ---
        soap_text = sections.get('SOAP', '')
        soap_subsection_lines = {'Subjective': [], 'Objective': [], 'Assessment': [], 'Plan': []}
        current_subsection = None
        heading_markers = {
            "* **Subjective:**": "Subjective",
            "* **Objective:**": "Objective",
            "* **Assessment:**": "Assessment",
            "* **Plan:**": "Plan"
        }

        if soap_text: # Only parse subsections if SOAP section exists
            for line in soap_text.splitlines():
                stripped_line = line.strip()
                matched_heading_key = None
                for marker, section_name in heading_markers.items():
                    if stripped_line.startswith(marker):
                        current_subsection = section_name
                        matched_heading_key = marker
                        break
                if matched_heading_key:
                    content_on_heading_line = stripped_line[len(matched_heading_key):].strip()
                    if content_on_heading_line:
                        soap_subsection_lines[current_subsection].append(content_on_heading_line)
                elif current_subsection:
                    if line.strip():
                         soap_subsection_lines[current_subsection].append(line.strip())

        # Calculate sentence counts for SOAP subsections
        for section_name, lines_list in soap_subsection_lines.items():
            subsection_text = " ".join(lines_list).strip()
            key_name = f'Sentence Count {section_name}'
            stats[key_name] = textstat.sentence_count(subsection_text) if subsection_text else 0

        return stats

    except FileNotFoundError:
        print(f"Error: File not found - {file_path}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error processing file {file_path}: {e}", file=sys.stderr)
        return None

# --- Main execution block ---
if __name__ == "__main__":
    # Setup Argument Parser to accept filename
    parser = argparse.ArgumentParser(description="Calculate statistics for a clinical note file.")
    parser.add_argument("input_file", help="Path to the text file to analyze (e.g., outputs/risk_assessment_output.txt).")
    args = parser.parse_args()

    # Get the file path from arguments
    target_file_path = pathlib.Path(args.input_file)

    # Calculate stats for the target file
    stats_target = calculate_stats(target_file_path)

    # --- Print Results for the Single File ---
    print(f"\n\n--- Statistics for {target_file_path.name} ---")
    if stats_target:
        # Define the order of metrics to print
        metrics = [
            'Total Word Count', 'Total Sentence Count', 'Average Sentence Length',
            'Flesch-Kincaid Grade', 'Flesch Reading Ease',
            'Word Count SOAP', 'Word Count MSE', 'Word Count Risk', 'Word Count Other/Full', # Added Other count
            'Sentence Count Subjective', 'Sentence Count Objective',
            'Sentence Count Assessment', 'Sentence Count Plan'
        ]
        # Print header
        print(f"{'Metric':<28} | {'Value':<10}")
        print("-" * 45) # Adjust separator length
        # Print each metric row
        for metric in metrics:
            # Only print metrics that are relevant (e.g., have a non-zero value or are always calculated)
            value = stats_target.get(metric) # Use get to avoid KeyError if metric not calculated
            if value is not None: # Check if the key exists and has a value
                 # Basic check to hide counts if they are zero and not essential like totals
                 is_essential_count = 'Total' in metric or 'Average' in metric or 'Grade' in metric or 'Ease' in metric
                 if value != 0 or is_essential_count:
                      print(f"{metric:<28} | {str(value):<10}")
    else:
        print(f"Could not generate statistics for {target_file_path.name}.")