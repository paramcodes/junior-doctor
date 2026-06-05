"""
Main entry point for Sprint 5: Outputs.
"""
import argparse
import logging
import sys

from ingestion.pdf_reader import extract_pages
from ingestion.ocr import apply_ocr_fallback
from extraction.evidence_extractor import extract_evidence_from_page
from tools.evidence_aggregator import aggregate_states
from agent.loop import run_agent_loop
from outputs.summary_generator import generate_summary
from outputs.trace_exporter import export_trace
from outputs.review_flag_exporter import export_review_flags

# Configure logging according to engineering constraints
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Main execution pipeline for document ingestion and text extraction.
    """
    parser = argparse.ArgumentParser(description="Discharge Summary - PDF Ingestion")
    parser.add_argument("pdf_path", type=str, help="Path to the PDF file to process.")
    args = parser.parse_args()
    
    logger.info(f"Starting ingestion pipeline for {args.pdf_path}")
    
    try:
        # Step 1: Text Extraction (PyMuPDF)
        pages = extract_pages(args.pdf_path)
        
        # Step 2: OCR Fallback (Tesseract)
        pages = apply_ocr_fallback(args.pdf_path, pages)
        
        # Step 3: Print page statistics
        print(f"Total Pages Processed: {len(pages)}")
        
        # Step 4: Extract evidence
        logger.info("Starting Gemini evidence extraction for all pages...")
        page_states = []
        for page in pages:
            state = extract_evidence_from_page(page, document_name=args.pdf_path)
            page_states.append(state)
            
        # Step 5: Aggregate states
        aggregated_state = aggregate_states(page_states)
        
        print("\n=== Extracted Evidence ===")
        print("\n[Diagnoses]")
        for d in aggregated_state.diagnoses:
            print(f"- {d.fact} (Page {d.page_number}) | Source: {d.source_text}")
            
        print("\n[Medications]")
        for m in aggregated_state.medications:
            med = m.fact
            print(f"- {med.name} | {med.context.dosage} | {med.context.frequency} | {med.context.route} | {med.context.status} (Page {m.page_number})")
            print(f"  Source: {m.source_text}")
            
        print("\n[Allergies]")
        for a in aggregated_state.allergies:
            print(f"- {a.fact} (Page {a.page_number}) | Source: {a.source_text}")
            
        print("\n[Procedures]")
        for p in aggregated_state.procedures:
            print(f"- {p.fact} (Page {p.page_number}) | Source: {p.source_text}")
            
        print("\n[Pending Results]")
        for p in aggregated_state.pending_results:
            print(f"- {p.fact} (Page {p.page_number}) | Source: {p.source_text}")
        
        # Step 6: Agent Loop (Sprint 4)
        logger.info("Starting deterministic agent loop...")
        aggregated_state = run_agent_loop(aggregated_state)
        
        print("\n=== Agent Execution Trace ===")
        if getattr(aggregated_state, "execution_trace", None):
            for step in aggregated_state.execution_trace:
                print(f" -> {step}")
        else:
            print("No execution trace found.")
        
        print("\n=== Review Flags ===")
        if not aggregated_state.review_flags:
            print("No review flags found.")
        else:
            for i, flag in enumerate(aggregated_state.review_flags, 1):
                print(f"\nFlag {i}: [{flag.severity}] {flag.reason}")
                if flag.missing_information:
                    print(f"  Missing Info: {flag.missing_information}")
                if flag.conflict:
                    print(f"  Conflict Field: {flag.conflict.field}")
                    print(f"  Conflict Details: {flag.conflict.description}")
        
        print("\n==========================")
        
        # Step 7: Export Results (Sprint 5)
        logger.info("Generating and exporting final outputs...")
        generate_summary(aggregated_state, "summary.md")
        export_trace(aggregated_state, "trace.md")
        export_review_flags(aggregated_state, "review_flags.md")
        
        print("\nPipeline execution complete. Generated outputs: summary.md, trace.md, review_flags.md\n")
            
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
