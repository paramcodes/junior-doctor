"""
Gemini evidence extraction module.
"""
import json
import logging
import os
from typing import List

import google.generativeai as genai

from schemas.page import Page
from schemas.evidence import Evidence
from schemas.medication import Medication, MedicationContext
from schemas.state import AgentState

logger = logging.getLogger(__name__)

# Configure API Key if available in environment
if "GEMINI_API_KEY" in os.environ:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])


def extract_evidence_from_page(page: Page, document_name: str) -> AgentState:
    """
    Use Gemini to extract clinical evidence from a single page.
    
    Args:
        page (Page): The page object containing text to analyze.
        document_name (str): The name of the source document for provenance.
        
    Returns:
        AgentState: A state object containing extracted evidence for this page.
    """
    logger.info(f"Extracting evidence from page {page.page_number} of {document_name}")
    
    state = AgentState()
    state.pages.append(page)
    
    if not page.text.strip():
        logger.warning(f"Page {page.page_number} is empty, skipping extraction.")
        return state

    prompt = f"""
    You are an expert clinical data extractor prioritizing safety over completeness.
    Unknown > Wrong. Never fabricate, never infer, never guess.
    
    Extract the following clinical entities from the text provided:
    - Diagnoses
    - Medications (with dosage, frequency, route, and status like Admission/Discharge/Discontinued)
    - Allergies
    - Procedures
    - Pending Results

    For each entity, you MUST extract the exact "source_text" snippet from the text that proves it.
    If a field or entire category is missing, use "Not Documented". 
    
    Respond strictly in JSON format with the following exact structure:
    {{
        "diagnoses": [{{"fact": "...", "source_text": "..."}}],
        "medications": [{{"name": "...", "dosage": "...", "frequency": "...", "route": "...", "status": "...", "source_text": "..."}}],
        "allergies": [{{"fact": "...", "source_text": "..."}}],
        "procedures": [{{"fact": "...", "source_text": "..."}}],
        "pending_results": [{{"fact": "...", "source_text": "..."}}]
    }}

    Text to analyze:
    {page.text}
    """
    
    try:
        model = genai.GenerativeModel('gemini-3.5-flash')
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.0
            )
        )
        
        data = json.loads(response.text)
    except Exception as e:
        logger.error(f"Gemini extraction failed for page {page.page_number}: {e}")
        # Return state with just the page, gracefully handling failures
        return state
        
    # Process Diagnoses
    for item in data.get("diagnoses", []):
        state.diagnoses.append(Evidence(
            fact=item.get("fact", "Not Documented"),
            page_number=page.page_number,
            source_document=document_name,
            source_text=item.get("source_text", "Not Documented")
        ))
        
    # Process Medications
    for item in data.get("medications", []):
        med = Medication(
            name=item.get("name", "Not Documented"),
            context=MedicationContext(
                dosage=item.get("dosage", "Not Documented"),
                frequency=item.get("frequency", "Not Documented"),
                route=item.get("route", "Not Documented"),
                status=item.get("status", "Not Documented")
            )
        )
        state.medications.append(Evidence(
            fact=med,
            page_number=page.page_number,
            source_document=document_name,
            source_text=item.get("source_text", "Not Documented")
        ))
        
    # Process Allergies
    for item in data.get("allergies", []):
        state.allergies.append(Evidence(
            fact=item.get("fact", "Not Documented"),
            page_number=page.page_number,
            source_document=document_name,
            source_text=item.get("source_text", "Not Documented")
        ))
        
    # Process Procedures
    for item in data.get("procedures", []):
        state.procedures.append(Evidence(
            fact=item.get("fact", "Not Documented"),
            page_number=page.page_number,
            source_document=document_name,
            source_text=item.get("source_text", "Not Documented")
        ))
        
    # Process Pending Results
    for item in data.get("pending_results", []):
        state.pending_results.append(Evidence(
            fact=item.get("fact", "Not Documented"),
            page_number=page.page_number,
            source_document=document_name,
            source_text=item.get("source_text", "Not Documented")
        ))
        
    return state
