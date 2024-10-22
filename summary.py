# Print summary
with open("analysis_results.json", "r") as f:
    results = json.load(f)

print(f"Total elements analyzed: {len(results['elements'])}")
print(f"Identified risks: {len(results['risks'])}")
print("\nKey recommendations:")
for rec in results['recommendations']:
    print(f"- {rec['category']}: {rec['suggestions'][0]}")
