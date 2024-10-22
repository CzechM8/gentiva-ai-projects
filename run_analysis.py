from archimate_analyzer import ArchiMateAnalyzer
import json
import os
import sys


def run_analysis(model_path):
    """Run analysis on an ArchiMate model file"""
    # Check if file exists
    if not os.path.exists(model_path):
        print(f"Error: File not found at {model_path}")
        return

    # Initialize analyzer
    print(f"\nInitializing analysis for: {model_path}")
    analyzer = ArchiMateAnalyzer()

    try:
        # Parse the model
        print("Parsing ArchiMate model...")
        analyzer.parse_archimate_model(model_path)

        # Run analysis
        print("Running analysis...")
        analysis = analyzer.analyze_model()

        # Create output filename
        output_file = os.path.splitext(model_path)[0] + "_analysis.json"

        # Export results
        print(f"Exporting analysis to: {output_file}")
        analyzer.export_analysis(analysis, output_file)

        # Print summary
        print("\n=== Analysis Summary ===")
        print(f"Elements analyzed: {len(analysis['elements'])}")
        print(f"Risks identified: {len(analysis['risks'])}")
        print("\nRisks by layer:")
        for layer, stats in analysis['layers'].items():
            print(f"- {layer.capitalize()}: {stats['elements']} elements")

        return analysis

    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        return None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_analysis.py <path_to_archimate_model.xml>")
    else:
        model_path = sys.argv[1]
        run_analysis(model_path)
