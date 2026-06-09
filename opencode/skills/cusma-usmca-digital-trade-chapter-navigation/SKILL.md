---
name: cusma-usmca-digital-trade-chapter-navigation
description: >-
  Use this skill when the user is working on or asking about CUSMA, USMCA, digital trade chapter, Canada-US trade for software, or cross-border digital product compliance.
version: 1.0.0
---

# SKILL: CUSMA/USMCA Digital Trade Chapter Navigation

## CAPABILITIES
- Structure cross-border data flows and IP licensing to leverage CUSMA/USMCA digital trade provisions
- Ensure compliance with rules on customs duties for digital products
- Navigate data localization requirements and cross-border data transfer rules
- Implement effective digital rights management systems compliant with treaty provisions
- Structure business operations to benefit from treaty protections for digital products

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| Business model and product specifications | CUSMA/USMCA-compliant business structure |
| Data flow specifications | Cross-border data transfer compliance plan |
| IP licensing arrangements | Treaty-compliant licensing agreements |
| Digital product characteristics | Customs duty exemption determination |
| Regulatory compliance requirements | Risk assessment and mitigation strategies |

## IMPLEMENTATION PATTERN

```python
# CUSMA/USMCA Digital Trade Compliance System
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json

class CUSMADigitalTradeNavigator:
    def __init__(self):
        # CUSMA/USMCA Digital Trade Chapter Key Provisions
        self.digital_trade_provisions = {
            'customs_duties': {
                'article': '19.3',
                'prohibition': 'No customs duties on digital products transmitted electronically',
                'definition': 'Digital product = computer program, text, video, image, sound recording that is digitally encoded',
                'exclusions': ['telecommunications service', 'financial service']
            },
            'cross_border_data_flow': {
                'article': '19.11',
                'principle': 'Free flow of data across borders',
                'exceptions': [
                    'protection of personal information',
                    'legitimate public policy objectives'
                ],
                'requirement': 'Non-discriminatory treatment'
            },
            'data_localization': {
                'article': '19.12',
                'prohibition': 'No requirement to use or locate computing facilities in territory',
                'exception': 'Legitimate public policy objective'
            },
            'source_code': {
                'article': '19.14',
                'protection': 'No required transfer or access to source code',
                'exception': 'Critical infrastructure'
            },
            'crypto_algorithms': {
                'article': '19.15',
                'prohibition': 'No restrictions on use of cryptography',
                'exception': 'Law enforcement investigations'
            }
        }
        
        # Digital product definitions from CUSMA
        self.digital_product_types = [
            'computer programs',
            'text',
            'video',
            'images',
            'sound recordings',
            'digital products that are digitally encoded'
        ]
        
        # Exclusions from digital product definition
        self.digital_product_exclusions = [
            'telecommunications service',
            'financial service',
            'service where user accesses digital product remotely'
        ]
    
    def is_digital_product_exempt_from_duties(self, 
                                            product_description: str,
                                            delivery_method: str) -> Tuple[bool, str]:
        """
        Determine if a product is exempt from customs duties under CUSMA/USMCA
        Returns: (is_exempt, explanation)
        """
        # Check delivery method
        if delivery_method not in ['electronic transmission', 'digital transmission']:
            return False, "Product must be transmitted electronically to qualify for duty exemption"
        
        # Check if product matches digital product definition
        product_lower = product_description.lower()
        
        # Check for exclusions first
        for exclusion in self.digital_product_exclusions:
            if exclusion in product_lower:
                return False, f"Product excluded: {exclusion} is not considered a digital product under CUSMA"
        
        # Check for digital product characteristics
        is_digital = False
        matched_type = None
        for product_type in self.digital_product_types:
            if product_type in product_lower:
                is_digital = True
                matched_type = product_type
                break
        
        if not is_digital:
            # Check for common digital product indicators
            digital_indicators = [
                'software', 'app', 'plugin', 'vst', 'au', 'aax', 'clap',
                'audio effect', 'virtual instrument', 'sample library',
                'preset', 'impulse response', 'wavetable'
            ]
            
            for indicator in digital_indicators:
                if indicator in product_lower:
                    is_digital = True
                    matched_type = indicator
                    break
        
        if is_digital:
            return True, f"Product qualifies as digital product ({matched_type}) transmitted electronically - exempt from customs duties under CUSMA/USMCA Article 19.3"
        else:
            return False, "Product does not meet definition of digital product under CUSMA/USMCA"
    
    def assess_cross_border_data_transfer_risk(self, 
                                             data_types: List[str],
                                             transfer_countries: List[str],
                                             transfer_purpose: str) -> Dict:
        """
        Assess risk associated with cross-border data transfers under CUSMA/USMCA
        """
        risk_assessment = {
            'overall_risk': 'low',
            'issues': [],
            'mitigations': [],
            'compliant': True
        }
        
        # Check for personal information
        personal_data_indicators = [
            'personal', 'private', 'confidential', 'sensitive',
            'voice recording', 'vocal', 'biometric', 'health',
            'financial', 'payment', 'identity'
        ]
        
        has_personal_data = any(
            indicator in ' '.join(data_types).lower() 
            for indicator in personal_data_indicators
        )
        
        if has_personal_data:
            risk_assessment['issues'].append(
                "Transfer may involve personal information - subject to privacy protections"
            )
            risk_assessment['mitigations'].append(
                "Ensure compliance with PIPEDA/GDPR and implement appropriate safeguards"
            )
            risk_assessment['overall_risk'] = 'medium'
        
        # Check transfer purpose
        if transfer_purpose in ['law enforcement', 'national security']:
            risk_assessment['issues'].append(
                "Transfer for law enforcement/national security may have additional requirements"
            )
            risk_assessment['mitigations'].append(
                "Ensure compliance with applicable legal processes and treaties"
            )
        
        # Check if transfers are to/from CUSMA countries
        cusma_countries = ['canada', 'united states', 'mexico', 'usa', 'us']
        non_cusma_transfers = [
            country for country in transfer_countries 
            if country.lower() not in cusma_countries
        ]
        
        if non_cusma_transfers:
            risk_assessment['notes'] = f"Transfers to non-CUSMA countries ({', '.join(non_cusma_transfers)}) subject to other agreements"
        
        # Determine overall compliance
        if risk_assessment['overall_risk'] == 'low' and len(risk_assessment['issues']) == 0:
            risk_assessment['compliant'] = True
        else:
            risk_assessment['compliant'] = False
            
        return risk_assessment
    
    def check_data_localization_compliance(self, 
                                         computing_facility_requirements: List[str]) -> Dict:
        """
        Check if computing facility requirements comply with CUSMA/USMCA data localization rules
        """
        compliance_check = {
            'compliant': True,
            'violations': [],
            'recommendations': []
        }
        
        # Check for requirements to locate facilities in specific territories
        localization_indicators = [
            'must be located', 'required to be in', 'shall be situated',
            'located in canada', 'located in usa', 'located in mexico'
        ]
        
        for req in computing_facility_requirements:
            req_lower = req.lower()
            for indicator in localization_indicators:
                if indicator in req_lower:
                    # Check if it's for a legitimate public policy objective
                    # This would require legal analysis - flag for review
                    compliance_check['violations'].append(
                        f"Potential data localization requirement: {req}"
                    )
                    compliance_check['compliant'] = False
                    break
        
        if not compliance_check['compliant']:
            compliance_check['recommendations'].append(
                "Review requirements to ensure they don't violate CUSMA/USMCA Article 19.12"
            )
            compliance_check['recommendations'].append(
                "Ensure any facility location requirements serve a legitimate public policy objective"
            )
        else:
            compliance_check['recommendations'].append(
                "No apparent data localization violations detected"
            )
        
        return compliance_check
    
    def assess_source_code_protection(self, 
                                    source_code_requests: List[str]) -> Dict:
        """
        Assess requests for source code access/transfer against CUSMA/USMCA protections
        """
        protection_assessment = {
            'protected': True,
            'violations': [],
            'exceptions_that_may_apply': [],
            'recommendations': []
        }
        
        # Check for requests that may violate source code protections
        request_indicators = [
            'source code', 'source code access', 'source code transfer',
            'access to source', 'transfer of source', 'disclose source',
            'provide source', 'share source code'
        ]
        
        for request in source_code_requests:
            request_lower = request.lower()
            for indicator in request_indicators:
                if indicator in request_lower:
                    protection_assessment['violations'].append(
                        f"Potential source code protection violation: {request}"
                    )
                    protection_assessment['protected'] = False
                    
                    # Check for potential exceptions
                    exception_indicators = [
                        'critical infrastructure', 'national security',
                        'law enforcement', 'investigation'
                    ]
                    
                    for exception in exception_indicators:
                        if exception in request_lower:
                            protection_assessment['exceptions_that_may_apply'].append(exception)
                    
                    break
        
        if protection_assessment['violations']:
            protection_assessment['recommendations'].append(
                "Review requests against CUSMA/USMCA Article 19.14 protections"
            )
            protection_assessment['recommendations'].append(
                "Ensure any source code access is limited to what is strictly necessary"
            )
            protection_assessment['recommendations'].append(
                "Consider implementing technical protections to prevent unnecessary source code exposure"
            )
        else:
            protection_assessment['recommendations'].append(
                "No apparent source code protection issues detected"
            )
        
        return protection_assessment
    
    def generate_compliance_report(self, 
                                 business_activities: Dict) -> Dict:
        """
        Generate comprehensive CUSMA/USMCA digital trade compliance report
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'sections': {},
            'overall_compliance': True,
            'summary': {
                'total_checks': 0,
                'passed_checks': 0,
                'failed_checks': 0,
                'warnings': 0
            }
        }
        
        # Section 1: Digital product customs duties
        if 'digital_products' in business_activities:
            for product in business_activities['digital_products']:
                is_exempt, explanation = self.is_digital_product_exempt_from_duties(
                    product['description'], 
                    product['delivery_method']
                )
                
                report['sections'][f"digital_product_{product['id']}"] = {
                    'check': 'Customs duty exemption for digital products',
                    'product': product['description'],
                    'delivery_method': product['delivery_method'],
                    'result': 'EXEMPT' if is_exempt else 'NOT EXEMPT',
                    'explanation': explanation,
                    'compliant': is_exempt  # Exempt = compliant with duty prohibition
                }
                
                report['summary']['total_checks'] += 1
                if is_exempt:
                    report['summary']['passed_checks'] += 1
                else:
                    report['summary']['failed_checks'] += 1
                    report['overall_compliance'] = False
        
        # Section 2: Cross-border data flows
        if 'data_transfers' in business_activities:
            for transfer in business_activities['data_transfers']:
                risk_assessment = self.assess_cross_border_data_transfer_risk(
                    transfer['data_types'],
                    transfer['countries'],
                    transfer['purpose']
                )
                
                report['sections'][f"data_transfer_{transfer['id']}"] = {
                    'check': 'Cross-border data transfer compliance',
                    'data_types': transfer['data_types'],
                    'countries': transfer['countries'],
                    'purpose': transfer['purpose'],
                    'result': 'COMPLIANT' if risk_assessment['compliant'] else 'NON-COMPLIANT',
                    'risk_level': risk_assessment['overall_risk'],
                    'issues': risk_assessment['issues'],
                    'mitigations': risk_assessment['mitigations'],
                    'compliant': risk_assessment['compliant']
                }
                
                report['summary']['total_checks'] += 1
                if risk_assessment['compliant']:
                    report['summary']['passed_checks'] += 1
                else:
                    report['summary']['failed_checks'] += 1
                    report['overall_compliance'] = False
                
                # Count warnings for medium risk
                if risk_assessment['overall_risk'] == 'medium':
                    report['summary']['warnings'] += 1
        
        # Section 3: Data localization
        if 'computing_facilities' in business_activities:
            for facility in business_activities['computing_facilities']:
                localization_check = self.check_data_localization_compliance(
                    facility['requirements']
                )
                
                report['sections'][f"facility_{facility['id']}"] = {
                    'check': 'Data localization compliance',
                    'facility': facility['description'],
                    'requirements': facility['requirements'],
                    'result': 'COMPLIANT' if localization_check['compliant'] else 'NON-COMPLIANT',
                    'violations': localization_check['violations'],
                    'recommendations': localization_check['recommendations'],
                    'compliant': localization_check['compliant']
                }
                
                report['summary']['total_checks'] += 1
                if localization_check['compliant']:
                    report['summary']['passed_checks'] += 1
                else:
                    report['summary']['failed_checks'] += 1
                    report['overall_compliance'] = False
        
        # Section 4: Source code protections
        if 'source_code_requests' in business_activities:
            for request in business_activities['source_code_requests']:
                protection_check = self.assess_source_code_protection([request])
                
                report['sections'][f"source_code_request_{request['id'] if 'id' in request else 'unknown'}"] = {
                    'check': 'Source code protection compliance',
                    'request': request['description'] if 'description' in request else str(request),
                    'result': 'PROTECTED' if protection_check['protected'] else 'POTENTIAL_VIOLATION',
                    'violations': protection_check['violations'],
                    'exceptions_that_may_apply': protection_check['exceptions_that_may_apply'],
                    'recommendations': protection_check['recommendations'],
                    'compliant': protection_check['protected']
                }
                
                report['summary']['total_checks'] += 1
                if protection_check['protected']:
                    report['summary']['passed_checks'] += 1
                else:
                    report['summary']['failed_checks'] += 1
                    report['overall_compliance'] = False
        
        # Add recommendations section
        report['recommendations'] = self._generate_recommendations(report)
        
        return report
    
    def _generate_recommendations(self, report: Dict) -> List[str]:
        """Generate recommendations based on compliance report"""
        recommendations = []
        
        if not report['overall_compliance']:
            recommendations.append(
                "Address all compliance violations before implementing business activities"
            )
        
        # Add specific recommendations based on failed checks
        for section_id, section in report['sections'].items():
            if not section.get('compliant', True):
                if 'Customs duty' in section['check']:
                    recommendations.append(
                        "Ensure digital products are properly classified and delivered electronically "
                        "to qualify for customs duty exemption under CUSMA/USMCA Article 19.3"
                    )
                elif 'data transfer' in section['check']:
                    recommendations.append(
                        "Implement appropriate data transfer mechanisms that respect privacy laws "
                        "while benefiting from CUSMA/USMCA free flow of data provisions"
                    )
                elif 'localization' in section['check']:
                    recommendations.append(
                        "Review computing facility requirements to ensure they don't constitute "
                        "impermissible data localization under CUSMA/USMCA Article 19.12"
                    )
                elif 'source code' in section['check']:
                    recommendations.append(
                        "Protect source code from unnecessary disclosure in accordance with "
                        "CUSMA/USMCA Article 19.14"
                    )
        
        # Add general best practices
        recommendations.extend([
            "Maintain documentation of CUSMA/USMCA compliance efforts",
            "Regularly review business activities for ongoing compliance",
            "Consult with legal counsel specializing in international trade law",
            "Consider obtaining advance rulings from customs authorities for complex cases",
            "Participate in industry consultations on digital trade implementation"
        ])
        
        return list(set(recommendations))  # Remove duplicates

# Usage example
def assess_audio_plugin_business_model():
    """Example: Assess compliance for an audio plugin business"""
    navigator = CUSMADigitalTradeNavigator()
    
    # Define business activities
    business_activities = {
        'digital_products': [
            {
                'id': 'plugin_001',
                'description': 'Professional audio VST3/AU plugin with advanced EQ and compression',
                'delivery_method': 'electronic transmission'
            },
            {
                'id': 'sample_lib_001',
                'description': 'Orchestral sample library for music production',
                'delivery_method': 'electronic transmission'
            },
            {
                'id': 'preset_pack_001',
                'description': 'Preset pack for electronic music synthesis',
                'delivery_method': 'electronic transmission'
            }
        ],
        'data_transfers': [
            {
                'id': 'transfer_001',
                'data_types': ['usage statistics', 'performance metrics'],
                'countries': ['canada', 'united states'],
                'purpose': 'product improvement and analytics'
            },
            {
                'id': 'transfer_002',
                'data_types': ['crash reports', 'error logs'],
                'countries': ['canada', 'united states', 'mexico'],
                'purpose': 'technical support and bug fixing'
            }
        ],
        'computing_facilities': [
            {
                'id': 'facility_001',
                'description': 'Cloud-based license validation service',
                'requirements': [
                    'Primary servers located in United States',
                    'Backup servers in Canada',
                    'Load balancing across North American regions'
                ]
            }
        ],
        'source_code_requests': [
            {
                'id': 'request_001',
                'description': 'Request for source code review as part of security audit',
                'context': 'Third-party security assessment'
            }
        ]
    }
    
    # Generate compliance report
    report = navigator.generate_compliance_report(business_activities)
    
    # Print summary
    print("=== CUSMA/USMCA Digital Trade Compliance Report ===")
    print(f"Timestamp: {report['timestamp']}")
    print(f"Overall Compliance: {'COMPLIANT' if report['overall_compliance'] else 'NON-COMPLIANT'}")
    print(f"\nSummary:")
    print(f"  Total Checks: {report['summary']['total_checks']}")
    print(f"  Passed: {report['summary']['passed_checks']}")
    print(f"  Failed: {report['summary']['failed_checks']}")
    print(f"  Warnings: {report['summary']['warnings']}")
    
    print(f"\nDetailed Results:")
    for section_id, section in report['sections'].items():
        status = "✓ PASS" if section.get('compliant', True) else "✗ FAIL"
        print(f"  {status} {section['check']}: {section.get('result', 'N/A')}")
        if 'explanation' in section:
            print(f"      Explanation: {section['explanation']}")
        if section.get('violations'):
            print(f"      Violations: {', '.join(section['violations'])}")
    
    print(f"\nRecommendations:")
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    return report

# Example usage
if __name__ == "__main__":
    report = assess_audio_plugin_business_model()
```

## EDGE CASES & FALLBACKS
- **Ambiguous Product Classification**: Seek advance rulings from customs authorities when product classification is unclear
- **Conflicting Obligations**: When CUSMA/USMCA conflicts with other treaties, apply the principle of treaty hierarchy and specific conflict resolution clauses
- **Evolving Technology**: Regularly review interpretations as new digital products and business models emerge
- **Privacy Law Conflicts**: Balance free data flow provisions with PIPEDA/GDPR requirements through appropriate safeguards
- **National Security Exceptions**: Ensure any invocations of national security exceptions are legitimate and proportionate
- **Enforcement Variability**: Recognize that implementation may vary between CUSMA parties and maintain flexibility
- **Small Business Exemptions**: Be aware of de minimis thresholds and simplified procedures for low-value shipments
- **Regulatory Changes**: Monitor for amendments or interpretations that may affect digital trade provisions
- **Dispute Resolution**: Understand the CUSMA/USMCA dispute settlement process for digital trade issues
- **Industry-Specific Considerations**: Account for sector-specific annexes or side letters that may modify general provisions

## INTEGRATION POINTS
- Legal Frameworks: CUSMA/USMCA Text, Customs Acts (Canada/US/Mexico), Competition Laws
- Government Agencies: Canada Border Services Agency (CBSA), US Customs and Border Protection (CBP), Mexican Customs
- Privacy Authorities: Office of the Privacy Commissioner of Canada (OPC), Federal Trade Commission (FTC), INAI (Mexico)
- IP Offices: Canadian Intellectual Property Office (CIPO), USPTO, IMPI (Mexico)
- Standards Bodies: ISO, IEC, W3C for technical standards that interface with trade rules
- Financial Institutions: Banks, payment processors for cross-border transactions
- Industry Associations: Canadian Audio Distributors Association (CADA), NAMM, AES
- Professional Services: International trade lawyers, customs brokers, trade consultants
- Compliance Tools: Automated customs classification software, trade compliance management systems
- Monitoring Services: Trade agreement watch services, regulatory alert services
- Dispute Resolution: NAFTA Secretariat (for legacy issues), CUSMA/USMCA dispute settlement panels
- Academic Resources: University research centers specializing in international trade law
- Government Programs: Export Development Canada (EDC), Small Business Administration (SBA), ProMéxico

## EXECUTION EXAMPLES

**Input:** "Determine if a new AI-powered audio mastering plugin delivered via download is exempt from customs duties under CUSMA/USMCA"
**Output:**
```
CUSMA/USMCA Digital Trade Compliance Assessment:

Product: AI-powered audio mastering plugin
Delivery Method: Electronic transmission (download)

Analysis:
1. Product delivered electronically ✓
2. Product description analysis:
   - Contains "plugin" - recognized digital product indicator
   - Contains "audio" and "mastering" - consistent with digital product definition
   - No exclusionary terms found (not a telecommunications or financial service)
3. Product qualifies as digital product under CUSMA/USMCA
4. Electronic transmission delivery method satisfies requirement

RESULT: EXEMPT from customs duties under CUSMA/USMCA Article 19.3
Explanation: Product qualifies as digital product (plugin) transmitted electronically - exempt from customs duties under CUSMA/USMCA Article 19.3
```

**Input:** "Assess compliance for a service that processes user voice recordings in the cloud for noise reduction"
**Output:**
```
CUSMA/USMCA Digital Trade Compliance Assessment:

Service: Cloud-based voice noise reduction processing
Data Types: Voice recordings (personal biometric data)
Transfer Countries: Canada → United States → Canada (cloud processing round-trip)
Purpose: Audio processing service

Analysis:
1. Cross-border data transfer involved ✓
2. Data types include voice recordings - potential personal biometric information
3. Transfer involves personal information → MEDIUM RISK
4. Purpose is commercial service provision
5. All transfers occur between CUSMA countries (Canada and US)

RESULT: COMPLIANT with mitigations required
Risk Level: Medium
Issues:
  - Transfer may involve personal information - subject to privacy protections
Mitigations:
  - Ensure compliance with PIPEDA/GDPR and implement appropriate safeguards
  - Obtain explicit consent for voice data processing
  - Implement data minimization and purpose limitation principles
  - Consider data localization options if privacy risks cannot be adequately mitigated
Overall: Service can comply with CUSMA/USMCA while respecting privacy obligations
```