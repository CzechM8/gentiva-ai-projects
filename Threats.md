# Threat Model: MPG Claims Data Pipeline

## 1. System Overview

**Data Classification**: Healthcare Claims Data (PHI/PII)
**Regulatory Requirements**: HIPAA, HITECH

## 2. Trust Boundaries

### External to Internal Boundaries

- MPG → MOVEit Cloud
- MOVEit Cloud → CLTDC
- CLTDC → GHS Azure
- Ursa Cloud → GHS Azure

### Internal Trust Boundaries

- Input Data Store → Databricks
- Databricks → Output Data Store
- Ursa Studio → PostgreSQL Database

## 3. Data Flows & Threats

### Flow 1: MPG → MOVEit Cloud

**Threats**:

- Man-in-the-middle attacks
- Data exposure during transmission
- Authentication bypass
- Unauthorized access to MOVEit Cloud
- Denial of Service

**Mitigations**:

- TLS encryption for data in transit
- Strong authentication mechanisms
- Access control lists
- Rate limiting
- Audit logging

### Flow 2: MOVEit Cloud → CLTDC

**Threats**:

- Unauthorized access to automation server
- Configuration tampering
- Malware injection
- Data tampering during transfer

**Mitigations**:

- Network segmentation
- Host-based security
- File integrity monitoring
- Secure configuration management

### Flow 3: CLTDC → Azure Data Store

**Threats**:

- Unauthorized cloud access
- Storage account compromise
- Data exfiltration
- Service account compromise

**Mitigations**:

- Azure Private Endpoints
- Managed Identities
- Network Security Groups
- Just-in-time access

### Flow 4: Data Processing

**Threats**:

- Unauthorized data access in Databricks
- SQL injection in PostgreSQL
- Privilege escalation
- Data leakage through processing
- Resource exhaustion

**Mitigations**:

- Data encryption at rest
- Role-based access control
- Resource quotas
- Query parameterization
- Activity monitoring

## 4. Attack Vectors

### Infrastructure Level

- Cloud service misconfigurations
- Weak network security
- Unpatched vulnerabilities
- Insecure API endpoints

### Application Level

- Authentication weaknesses
- Authorization bypasses
- Input validation failures
- Business logic flaws

### Data Level

- Insufficient encryption
- Key management issues
- Data retention violations
- Backup exposure

## 5. Critical Assets

### Data Assets

- Raw claims data
- Normalized claims data
- Configuration data
- Authentication credentials

### System Assets

- MOVEit infrastructure
- Azure storage accounts
- Databricks workspace
- PostgreSQL database

## 6. Recommended Controls

### Technical Controls

1. Encryption:

   - TLS 1.3 for transit
   - AES-256 for storage
   - Key rotation policy

2. Access Control:

   - Multi-factor authentication
   - Just-in-time access
   - Principle of least privilege
   - Regular access reviews

3. Monitoring:
   - Security information and event management (SIEM)
   - File integrity monitoring
   - Anomaly detection
   - Audit logging

### Process Controls

1. Security Operations:

   - Incident response plan
   - Change management
   - Backup procedures
   - Disaster recovery

2. Compliance:
   - Regular audits
   - Vulnerability assessments
   - Penetration testing
   - Compliance reporting

## 7. Risk Matrix

### High Risk

- Unauthorized access to PHI
- Data exfiltration
- Service compromise

### Medium Risk

- Temporary service disruption
- Performance degradation
- Configuration errors

### Low Risk

- Failed access attempts
- Minor configuration changes
- Routine processing errors

## 8. Incident Response Considerations

### Detection Capabilities

- Log monitoring
- Alert thresholds
- Automated responses
- Security dashboards

### Response Procedures

- Incident classification
- Escalation paths
- Communication plans
- Recovery procedures

## 9. Testing & Validation

### Regular Testing

- Penetration testing
- Vulnerability scanning
- Configuration review
- Access control validation

### Compliance Validation

- HIPAA compliance checks
- Security control testing
- Audit preparation
- Documentation review
