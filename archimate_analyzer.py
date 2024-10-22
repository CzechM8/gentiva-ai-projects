import xml.etree.ElementTree as ET
import networkx as nx
import tkinter
from dataclasses import dataclass

from typing import List, Dict, Optional
import json


@dataclass
class ArchiMateElement:
    id: str
    name: str
    type: str
    layer: str
    relationships: List[str]
    properties: Dict[str, str]


class ArchiMateAnalyzer:
    def __init__(self):
        self.elements = {}
        self.relationships = {}
        self.graph = nx.DiGraph()

        # Define ArchiMate layers
        self.layers = {
            'business': ['business-actor', 'business-role',
                         'business-process',
                         'business-function'],
            'application': ['application-component', 'application-service',
                            'application-interface'],
            'technology': ['node', 'device', 'system-software',
                           'technology-service']
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

        # Define relationship risks
        self.relationship_risks = {
            'serving': [
                'Service level agreements',
                'Dependency management',
                'Interface stability'
            ],
            'realization': [
                'Implementation complexity',
                'Resource requirements',
                'Technical feasibility'
            ],
            'assignment': [
                'Resource allocation',
                'Responsibility clarity',
                'Skill requirements'
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
                layer=self._determine_layer(elem.get('xsi:type')),
                relationships=[],
                properties={}
            )

            # Parse properties
            for prop in elem.findall(".//property"):
                element.properties[prop.get('key')] = prop.get('value')

            self.elements[element.id] = element
            self.graph.add_node(element.id, **vars(element))

        # Parse relationships
        for rel in root.findall(".//relationship"):
            source = rel.get('source')
            target = rel.get('target')
            rel_type = rel.get('xsi:type')

            self.relationships[rel.get('identifier')] = {
                'source': source,
                'target': target,
                'type': rel_type
            }

            self.graph.add_edge(source, target, type=rel_type)
            self.elements[source].relationships.append(rel.get('identifier'))
            self.elements[target].relationships.append(rel.get('identifier'))

    def _determine_layer(self, element_type: str) -> str:
        """Determine ArchiMate layer for element type"""
        for layer, types in self.layers.items():
            if any(t in element_type.lower() for t in types):
                return layer
        return 'unknown'

    def analyze_model(self):
        """Perform comprehensive analysis of the ArchiMate model"""
        analysis = {
            'elements': self._analyze_elements(),
            'relationships': self._analyze_relationships(),
            'layers': self._analyze_layers(),
            'risks': [],
            'recommendations': []
        }

        # Aggregate risks
        all_risks = []
        for element_analysis in analysis['elements']:
            all_risks.extend(element_analysis['risks'])
        for rel_analysis in analysis['relationships']:
            all_risks.extend(rel_analysis['risks'])

        analysis['risks'] = all_risks
        analysis['recommendations'] = self._generate_recommendations(all_risks)

        return analysis

    def _analyze_elements(self):
        """Analyze individual elements"""
        element_analysis = []

        for element_id, element in self.elements.items():
            risks = []

            # Check element-specific risks
            if element.type in self.element_risks:
                risks.extend(self.element_risks[element.type])

            # Check connectivity
            connections = list(self.graph.neighbors(element_id))
            if len(connections) > 5:
                risks.append(
                    f"High coupling: {element.name} has many dependencies"
                )

            # Check layer alignment
            if not self._check_layer_alignment(element):
                risks.append(
                    f"Layer misalignment: {element.name} has cross-layer dependencies"
                )

            element_analysis.append({
                'id': element_id,
                'name': element.name,
                'type': element.type,
                'layer': element.layer,
                'risks': risks,
                'complexity_score': self._calculate_complexity_score(element)
            })

        return element_analysis

    def _analyze_relationships(self):
        """Analyze relationships between elements"""
        relationship_analysis = []

        for rel_id, rel in self.relationships.items():
            risks = []

            # Check relationship-specific risks
            if rel['type'] in self.relationship_risks:
                risks.extend(self.relationship_risks[rel['type']])

            # Check for circular dependencies
            if self._has_circular_dependency(rel['source'], rel['target']):
                risks.append(f"Circular dependency detected between {self.elements[rel['source']].name} and {self.elements[rel['target']].name}")

            relationship_analysis.append({
                'id': rel_id,
                'source': self.elements[rel['source']].name,
                'target': self.elements[rel['target']].name,
                'type': rel['type'],
                'risks': risks
            })

        return relationship_analysis

    def _analyze_layers(self):
        """Analyze layer interactions and dependencies"""
        layer_analysis = {
            'business': {'elements': 0, 'dependencies': 0},
            'application': {'elements': 0, 'dependencies': 0},
            'technology': {'elements': 0, 'dependencies': 0}
        }

        # Count elements per layer
        for element in self.elements.values():
            if element.layer in layer_analysis:
                layer_analysis[element.layer]['elements'] += 1

        # Analyze cross-layer dependencies
        for rel in self.relationships.values():
            source_layer = self.elements[rel['source']].layer
            target_layer = self.elements[rel['target']].layer

            if source_layer != target_layer:
                layer_analysis[source_layer]['dependencies'] += 1
                layer_analysis[target_layer]['dependencies'] += 1

        return layer_analysis

    def _check_layer_alignment(self, element: ArchiMateElement) -> bool:
        """Check if element has appropriate layer alignment"""
        neighbors = list(self.graph.neighbors(element.id))
        for neighbor_id in neighbors:
            neighbor = self.elements[neighbor_id]
            if abs(self._get_layer_level(element.layer) - self._get_layer_level(neighbor.layer)) > 1:
                return False
        return True

    def _get_layer_level(self, layer: str) -> int:
        """Get numeric level for layer"""
        layers = {'business': 0, 'application': 1, 'technology': 2}
        return layers.get(layer, -1)

    def _has_circular_dependency(self, source: str, target: str) -> bool:
        """Check for circular dependencies"""
        try:
            path = nx.shortest_path(self.graph, target, source)
            return len(path) > 0
        except nx.NetworkXNoPath:
            return False

    def _calculate_complexity_score(self, element: ArchiMateElement) -> float:
        """Calculate complexity score for an element"""
        # Factors contributing to complexity:
        # 1. Number of relationships
        # 2. Types of relationships
        # 3. Cross-layer dependencies
        # 4. Properties complexity

        score = 0

        # Relationship complexity
        score += len(element.relationships) * 1.5

        # Cross-layer complexity
        neighbors = list(self.graph.neighbors(element.id))
        cross_layer_count = sum(1 for n in neighbors if self.elements[n].layer != element.layer)
        score += cross_layer_count * 2

        # Properties complexity
        score += len(element.properties) * 0.5

        return round(score, 2)

    def _generate_recommendations(self, risks: List[str]):
        """Generate recommendations based on identified risks"""
        recommendations = []

        # Group risks by category
        risk_categories = {
            'architecture': [],
            'integration': [],
            'security': [],
            'performance': []
        }

        for risk in risks:
            if any(keyword in risk.lower() for keyword in ['layer', 'dependency', 'coupling']):
                risk_categories['architecture'].append(risk)
            elif any(keyword in risk.lower() for keyword in ['interface', 'connection', 'relationship']):
                risk_categories['integration'].append(risk)
            elif any(keyword in risk.lower() for keyword in ['security', 'vulnerability', 'access']):
                risk_categories['security'].append(risk)
            elif any(keyword in risk.lower() for keyword in ['performance', 'scalability', 'efficiency']):
                risk_categories['performance'].append(risk)

        # Generate recommendations for each category
        if risk_categories['architecture']:
            recommendations.append({
                'category': 'Architecture',
                'risks': risk_categories['architecture'],
                'suggestions': [
                    'Review and simplify layer interactions',
                    'Reduce coupling between components',
                    'Consider microservices architecture',
                    'Implement clear separation of concerns'
                ]
            })

        if risk_categories['integration']:
            recommendations.append({
                'category': 'Integration',
                'risks': risk_categories['integration'],
                'suggestions': [
                    'Standardize interfaces',
                    'Implement API gateway',
                    'Use event-driven architecture',
                    'Define clear service contracts'
                ]
            })

        return recommendations

    def export_analysis(self, analysis, filename='archimate_analysis.json'):
        """Export analysis results to JSON"""
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=4)
        print(f"Analysis exported to {filename}")

    def visualize_model(self):
        """Create visualization of the ArchiMate model"""
        pos = nx.spring_layout(self.graph)

        # Create separate graphs for each layer
        layer_graphs = {
            'business': nx.DiGraph(),
            'application': nx.DiGraph(),
            'technology': nx.DiGraph()
        }

        # Populate layer graphs
        for element_id, element in self.elements.items():
            if element.layer in layer_graphs:
                layer_graphs[element.layer].add_node(element_id, **vars(element))

        for rel_id, rel in self.relationships.items():
            source_layer = self.elements[rel['source']].layer
            target_layer = self.elements[rel['target']].layer
            if source_layer == target_layer and source_layer in layer_graphs:
                layer_graphs[source_layer].add_edge(rel['source'], rel['target'])

        return layer_graphs


# Example usage
if __name__ == "__main__":
    analyzer = ArchiMateAnalyzer()

    # Parse ArchiMate model
    analyzer.parse_archimate_model('architecture.xml')

    # Analyze model
    analysis = analyzer.analyze_model()

    # Export analysis
    analyzer.export_analysis(analysis)

    # Visualize model
    layer_graphs = analyzer.visualize_model()
