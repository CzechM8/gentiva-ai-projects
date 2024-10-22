import xml.etree.ElementTree as ET
import networkx as nx
from typing import List, Dict, Optional
import json
import matplotlib.pyplot as plt

class ArchiMateElement:
    def __init__(self, id: str, name: str, type: str, layer: str):
        self.id = id
        self.name = name
        self.type = type
        self.layer = layer
        self.relationships = []
        self.properties = {}

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'layer': self.layer,
            'relationships': self.relationships,
            'properties': self.properties
        }

class ArchiMateAnalyzer:
    def __init__(self):
        self.elements = {}
        self.relationships = {}
        self.graph = nx.DiGraph()

        # Define ArchiMate layers
        self.layers = {
            'business': ['business-actor', 'business-role', 'business-process', 'business-function'],
            'application': ['application-component', 'application-service', 'application-interface'],
            'technology': ['node', 'device', 'system-software', 'technology-service']
        }

        # Define common risks by element type
        self.element_risks = {
            'business-process': [
                'Process efficiency',
                'Business continuity',
                'Compliance requirements',
                'Resource allocation'
            ],
            'application-component': [
                'Technical debt',
                'Scalability limitations',
                'Integration complexity',
                'Maintenance overhead'
            ],
            'technology-service': [
                'Service availability',
                'Performance bottlenecks',
                'Security vulnerabilities',
                'Infrastructure dependencies'
            ]
        }

    def parse_archimate_model(self, file_path: str):
        """Parse ArchiMate model from XML file"""
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Parse elements
        for elem in root.findall(".//element"):
            element = ArchiMateElement(
                id=elem.get('identifier'),
                name=elem.get('name'),
                type=elem.get('xsi:type'),
                layer=self._determine_layer(elem.get('xsi:type'))
            )

            # Parse properties
            for prop in elem.findall(".//property"):
                element.properties[prop.get('key')] = prop.get('value')

            self.elements[element.id] = element
            self.graph.add_node(element.id, **element.to_dict())

        # Parse relationships
        for rel in root.findall(".//relationship"):
            source = rel.get('source')
            target = rel.get('target')
            rel_type = rel.get('xsi:type')

            if source and target:  # Only add if both source and target exist
                self.relationships[rel.get('identifier')] = {
                    'source': source,
                    'target': target,
                    'type': rel_type
                }

                self.graph.add_edge(source, target, type=rel_type)
                if source in self.elements:
                    self.elements[source].relationships.append(rel.get('identifier'))
                if target in self.elements:
                    self.elements[target].relationships.append(rel.get('identifier'))

    def _determine_layer(self, element_type: str) -> str:
        """Determine ArchiMate layer for element type"""
        if element_type:
            element_type = element_type.lower()
            for layer, types in self.layers.items():
                if any(t in element_type for t in types):
                    return layer
        return 'unknown'

    def analyze_model(self):
        """Analyze the ArchiMate model"""
        analysis = {
            'elements': [],
            'relationships': [],
            'layers': {
                'business': {'elements': 0, 'dependencies': 0},
                'application': {'elements': 0, 'dependencies': 0},
                'technology': {'elements': 0, 'dependencies': 0}
            },
            'risks': [],
            'recommendations': []
        }

        # Analyze elements
        for element_id, element in self.elements.items():
            # Count elements per layer
            if element.layer in analysis['layers']:
                analysis['layers'][element.layer]['elements'] += 1

            # Get element risks
            risks = []
            if element.type in self.element_risks:
                risks.extend(self.element_risks[element.type])

            analysis['elements'].append({
                'id': element_id,
                'name': element.name,
                'type': element.type,
                'layer': element.layer,
                'risks': risks
            })
            analysis['risks'].extend(risks)

        # Generate recommendations
        if analysis['risks']:
            analysis['recommendations'] = [
                {
                    'category': 'Architecture',
                    'suggestions': [
                        'Review and optimize layer dependencies',
                        'Consider implementing microservices',
                        'Strengthen security measures',
                        'Improve scalability'
                    ]
                }
            ]

        return analysis

    def export_analysis(self, analysis, filename='analysis_results.json'):
        """Export analysis results to JSON"""
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=4)
