"""
Summary generation tool using Gemini.
"""
import logging
import os
import google.generativeai as genai

from schemas.state import AgentState

logger = logging.getLogger(__name__)

if "GEMINI_API_KEY" in os.environ:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])


def generate_summary(state: AgentState, output_path: str = "summary.md") -> str:
    """
    Generate the final discharge summary using Gemini based ONLY on validated AgentState.
    Never infers facts. Missing information becomes 'Not Documented'.
    """
    logger.info("Starting summary generation.")
    
    diagnoses_str = "\n".join([f"- {d.fact}" for d in state.diagnoses]) if state.diagnoses else "Not Documented"
    allergies_str = "\n".join([f"- {a.fact}" for a in state.allergies]) if state.allergies else "Not Documented"
    procedures_str = "\n".join([f"- {p.fact}" for p in state.procedures]) if state.procedures else "Not Documented"
    pending_str = "\n".join([f"- {p.fact}" for p in state.pending_results]) if state.pending_results else "Not Documented"
    
    meds_str = ""
    if state.medications:
        for m in state.medications:
            med = m.fact
            if hasattr(med, 'name'):
                meds_str += f"- {med.name} | Dosage: {med.context.dosage} | Frequency: {med.context.frequency} | Route: {med.context.route} | Status: {med.context.status}\n"
    else:
        meds_str = "Not Documented"

    state_text = f"""
    DIAGNOSES:
    {diagnoses_str}
    
    MEDICATIONS:
    {meds_str}
    
    ALLERGIES:
    {allergies_str}
    
    PROCEDURES:
    {procedures_str}
    
    PENDING RESULTS:
    {pending_str}
    """
    
    prompt = f"""
    You are an expert clinical documentation assistant.
    Write a clear, structured Markdown Discharge Summary based ONLY on the provided clinical evidence.
    
    CRITICAL RULES:
    - NEVER infer, guess, or fabricate clinical information.
    - If a field or category is missing or empty, explicitly state "Not Documented".
    - Organize into standard clinical headings: Diagnoses, Medications, Allergies, Procedures, Pending Results.
    - Do not invent patient names, dates, or hospital locations unless they are strictly provided in the text.
    
    Provided Evidence:
    {state_text}
    """
    
    try:
        model = genai.GenerativeModel('gemini-3.5-flash')
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(temperature=0.0)
        )
        summary_markdown = response.text
    except Exception as e:
        logger.error(f"Summary generation failed: {e}")
        summary_markdown = "# Discharge Summary\n\nGeneration Failed due to API error."
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary_markdown)
        
    logger.info(f"Summary successfully written to {output_path}")
    return summary_markdown
