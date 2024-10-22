from archimate_analyzer import ArchiMateAnalyzer

import json


def analyze_archimate_model(model_path, output_path='analysis_results.json'):
    """
    Analyze an ArchiMate model and generate a report
    """
    # Initialize the analyzer
    analyzer = ArchiMateAnalyzer()

    # Parse and analyze the model
    try:
        # Load and parse the model
        analyzer.parse_archimate_model(model_path)

        # Perform analysis
        analysis = analyzer.analyze_model()

        # Export results
        analyzer.export_analysis(analysis, output_path)

        # Print summary
        print_analysis_summary(analysis)

        return analysis

    except Exception as e:
        print(f"Error analyzing model: {str(e)}")
        return None


def print_analysis_summary(analysis):
    """
    Print a human-readable summary of the analysis
    """
    print("\n=== ArchiMate Analysis Summary ===")

    # Element statistics
    print("\nElement Analysis:")
    element_count = len(analysis['elements'])
    high_risk_elements = sum(1 for elem in analysis['elements'] if len(elem['risks']) > 2)
    print(f"Total Elements: {element_count}")
    print(f"High Risk Elements: {high_risk_elements}")

    # Layer statistics
    print("\nLayer Analysis:")
    for layer, stats in analysis['layers'].items():
        print(f"{layer.capitalize()} Layer:")
        print(f"  Elements: {stats['elements']}")
        print(f"  Dependencies: {stats['dependencies']}")

    # Risk summary
    print("\nTop Risks:")
    risks = analysis['risks']
    risk_categories = {}
    for risk in risks:
        category = risk.split(':')[0] if ':' in risk else 'Other'
        risk_categories[category] = risk_categories.get(category, 0) + 1

    for category, count in risk_categories.items():
        print(f"{category}: {count} risks")

    # Recommendations
    print("\nKey Recommendations:")
    for i, rec in enumerate(analysis['recommendations'], 1):
        print(f"\n{i}. {rec['category']}:")
        for suggestion in rec['suggestions'][:2]:  # Show top 2 suggestions
            print(f"   - {suggestion}")


# Example 1: Analyzing a model from Archi tool export
def analyze_archi_export():
    """
    Example of analyzing a model exported from Archi tool
    """
    model_path = "path/to/your/archi_model.xml"
    return analyze_archimate_model(model_path, "archi_analysis.json")


# Example 2: Analyzing a model from Enterprise Architect export
def analyze_ea_export():
    """
    Example of analyzing a model exported from Enterprise Architect
    """
    model_path = "path/to/your/ea_model.xml"
    return analyze_archimate_model(model_path, "ea_analysis.json")


# Example usage with custom visualization
def analyze_with_visualization(model_path):
    """
    Analyze model and generate visualizations
    """
    analyzer = ArchiMateAnalyzer()

    # Parse and analyze
    analyzer.parse_archimate_model(model_path)
    analysis = analyzer.analyze_model()

    # Get layer visualizations
    layer_graphs = analyzer.visualize_model()

    # Export both analysis and visualizations
    analyzer.export_analysis(analysis, "full_analysis.json")

    return analysis, layer_graphs


if __name__ == "__main__":
    # Example 1: Basic analysis
    print("Running basic analysis...")
    model_path = "your_archimate_model.xml"  # Replace with your model path
    results = analyze_archimate_model(model_path)

    # Example 2: Analysis with visualization
    print("\nRunning analysis with visualization...")
    analysis, graphs = analyze_with_visualization(model_path)
