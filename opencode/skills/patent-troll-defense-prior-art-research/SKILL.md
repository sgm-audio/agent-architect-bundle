---
name: patent-troll-defense-prior-art-research
description: >-
  Use this skill when the user is working on or asking about patent troll defense, prior art research, invalidating patents, patent litigation defense, or protecting open source from patent claims.
version: 1.0.0
---

# SKILL: Patent Troll Defense & Prior Art Research

## CAPABILITIES
- Develop defensive publication strategies to prevent patent troll claims
- Maintain prior art databases to invalidate obvious DSP technique patents
- Conduct freedom-to-operate (FTO) analyses for audio technologies
- Implement monitoring systems for new patent filings in relevant domains
- Create documentation practices that establish clear invention timelines

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| DSP algorithm specifications | Prior art search strategies and databases |
| Patent landscape analysis reports | Freedom-to-operate opinions and risk assessments |
| Invention disclosures | Defensive publications and invention records |
| Competitor patent portfolios | Patent mapping and threat analysis |
| Legal requirements for documentation | Invention disclosure forms and lab notebooks |

## IMPLEMENTATION PATTERN

```python
# Patent Troll Defense System
import hashlib
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import requests
import yaml

class PatentDefenseSystem:
    def __init__(self, 
                 storage_dir: str = "./patent_defense",
                 watchlist_keywords: List[str] = None):
        self.storage_dir = storage_dir
        self.watchlist_keywords = watchlist_keywords or [
            "audio processing", "digital signal processing", "filter",
            "compressor", "equalizer", "reverb", "delay", "modulation",
            "synthesizer", "oscillator", "filter", "adaptive filter",
            "noise reduction", "echo cancellation", "beamforming"
        ]
        
        # Create storage directories
        os.makedirs(storage_dir, exist_ok=True)
        os.makedirs(os.path.join(storage_dir, "inventions"), exist_ok=True)
        os.makedirs(os.path.join(storage_dir, "publications"), exist_ok=True)
        os.makedirs(os.path.join(storage_dir, "prior_art"), exist_ok=True)
        os.makedirs(os.path.join(storage_dir, "monitoring"), exist_ok=True)
        
        # Load existing data
        self.inventions = self._load_inventions()
        self.prior_art_db = self._load_prior_art()
    
    def _load_inventions(self) -> Dict:
        """Load invention records"""
        inventions_file = os.path.join(self.storage_dir, "inventions", "registry.json")
        if os.path.exists(inventions_file):
            with open(inventions_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_inventions(self):
        """Save invention records"""
        inventions_file = os.path.join(self.storage_dir, "inventions", "registry.json")
        with open(inventions_file, 'w') as f:
            json.dump(self.inventions, f, indent=2)
    
    def _load_prior_art(self) -> Dict:
        """Load prior art database"""
        prior_art_file = os.path.join(self.storage_dir, "prior_art", "database.json")
        if os.path.exists(prior_art_file):
            with open(prior_art_file, 'r') as f:
                return json.load(f)
        return {"entries": []}
    
    def _save_prior_art(self):
        """Save prior art database"""
        prior_art_file = os.path.join(self.storage_dir, "prior_art", "database.json")
        with open(prior_art_file, 'w') as f:
            json.dump(self.prior_art_db, f, indent=2)
    
    def record_invention(self, 
                        title: str,
                        description: str,
                        inventors: List[str],
                        date: Optional[str] = None,
                        documents: List[str] = None) -> str:
        """Record a new invention for defensive purposes"""
        if date is None:
            date = datetime.now().isoformat()
        
        # Generate unique ID
        invention_id = hashlib.sha256(
            f"{title}{''.join(inventors)}{date}".encode()
        ).hexdigest()[:16]
        
        invention_record = {
            "id": invention_id,
            "title": title,
            "description": description,
            "inventors": inventors,
            "date": date,
            "documents": documents or [],
            "status": "recorded",
            "timestamp": datetime.now().isoformat()
        }
        
        # Save invention record
        invention_path = os.path.join(
            self.storage_dir, 
            "inventions", 
            f"{invention_id}.json"
        )
        with open(invention_path, 'w') as f:
            json.dump(invention_record, f, indent=2)
        
        # Update registry
        self.inventions[invention_id] = {
            "title": title,
            "date": date,
            "inventors": inventors,
            "path": invention_path
        }
        self._save_inventions()
        
        return invention_id
    
    def create_defensive_publication(self, 
                                   invention_id: str,
                                   publication_title: Optional[str] = None,
                                   publication_venue: str = "Technical Blog",
                                   additional_context: str = "") -> str:
        """Create a defensive publication for an invention"""
        if invention_id not in self.inventions:
            raise ValueError(f"Invention {invention_id} not found")
        
        invention = self.inventions[invention_id]
        
        if publication_title is None:
            publication_title = f"Technical Description: {invention['title']}"
        
        publication_content = f"""
Title: {publication_title}
Authors: {', '.join(invention['inventors'])}
Date: {invention['date']}
Venue: {publication_venue}

Abstract:
{invention['description']}

{additional_context}

Detailed Description:
{invention['description']}

Implementation Details:
[Include any relevant implementation details, algorithms, or diagrams here]

Prior Art Statement:
This publication is made for defensive purposes to prevent others from obtaining 
patents on the subject matter disclosed herein.
"""
        
        # Save publication
        pub_id = hashlib.sha256(
            f"{publication_title}{invention['date']}".encode()
        ).hexdigest()[:16]
        
        publication_path = os.path.join(
            self.storage_dir,
            "publications",
            f"{pub_id}.txt"
        )
        with open(publication_path, 'w') as f:
            f.write(publication_content)
        
        # Update invention record
        invention_path = invention["path"]
        with open(invention_path, 'r') as f:
            invention_record = json.load(f)
        
        invention_record["defensive_publication"] = {
            "id": pub_id,
            "title": publication_title,
            "venue": publication_venue,
            "date": datetime.now().isoformat(),
            "path": publication_path
        }
        invention_record["status"] = "published_defensively"
        
        with open(invention_path, 'w') as f:
            json.dump(invention_record, f, indent=2)
        
        return pub_id
    
    def add_prior_art(self, 
                     title: str,
                     authors: List[str],
                     publication_date: str,
                     source: str,
                     content: str,
                     url: Optional[str] = None) -> str:
        """Add prior art to the database"""
        prior_art_id = hashlib.sha256(
            f"{title}{''.join(authors)}{publication_date}{source}".encode()
        ).hexdigest()[:16]
        
        prior_art_entry = {
            "id": prior_art_id,
            "title": title,
            "authors": authors,
            "publication_date": publication_date,
            "source": source,
            "content": content,
            "url": url,
            "date_added": datetime.now().isoformat()
        }
        
        self.prior_art_db["entries"].append(prior_art_entry)
        self._save_prior_art()
        
        return prior_art_id
    
    def search_prior_art(self, 
                        keywords: List[str]) -> List[Dict]:
        """Search prior art database for relevant entries"""
        results = []
        keywords_lower = [k.lower() for k in keywords]
        
        for entry in self.prior_art_db["entries"]:
            # Simple text search - in practice use proper search indexing
            content_lower = (entry["title"] + " " + 
                           " ".join(entry["authors"]) + " " + 
                           entry["content"]).lower()
            
            if any(keyword in content_lower for keyword in keywords_lower):
                results.append(entry)
        
        return results
    
    def generate_fto_analysis(self, 
                           invention_description: str,
                           keywords: List[str]) -> Dict:
        """Generate a freedom-to-operate analysis"""
        # Search for relevant prior art
        relevant_prior_art = self.search_prior_art(keywords)
        
        # In practice, this would involve more sophisticated analysis
        # For now, we'll provide a basic assessment
        
        fto_report = {
            "invention_description": invention_description,
            "search_keywords": keywords,
            "relevant_prior_art_count": len(relevant_prior_art),
            "relevant_prior_art": relevant_prior_art[:10],  # Limit to top 10
            "risk_assessment": "medium" if len(relevant_prior_art) > 5 else "low",
            "recommendations": [
                "Consider conducting a professional patent search",
                "Review identified prior art for potential conflicts",
                "Document invention thoroughly with dates and witnesses",
                "Consider filing a provisional patent application if appropriate"
            ]
        }
        
        # Add defensive publication recommendation
        fto_report["recommendations"].append(
            "Create a defensive publication to establish prior art"
        )
        
        return fto_report
    
    def monitor_new_patents(self, 
                          weeks: int = 4) -> List[Dict]:
        """Monitor for new patent publications (placeholder)"""
        # In practice, this would connect to patent office APIs or use monitoring services
        # For demonstration, we'll return a placeholder
        
        monitoring_report = {
            "period_weeks": weeks,
            "keywords_monitored": self.watchlist_keywords,
            "new_patents_found": 0,
            "patents": [],
            "last_check": datetime.now().isoformat(),
            "note": "This is a placeholder implementation. In practice, connect to "
                   "patent office APIs (USPTO, EPO, WIPO) or use commercial monitoring services."
        }
        
        # Save monitoring report
        monitoring_file = os.path.join(
            self.storage_dir,
            "monitoring",
            f"patent_monitor_{datetime.now().strftime('%Y%m%d')}.json"
        )
        with open(monitoring_file, 'w') as f:
            json.dump(monitoring_report, f, indent=2)
        
        return [monitoring_report]

# Usage example
def example_patent_defense_workflow():
    """Example workflow for patent troll defense"""
    # Initialize the defense system
    defense_system = PatentDefenseSystem(
        storage_dir="./my_audio_patent_defense",
        watchlist_keywords=[
            "audio filter", "adaptive noise reduction", 
            "dynamic range compressor", "parametric equalizer",
            "reverberation algorithm", "pitch detection"
        ]
    )
    
    # Record a new invention
    invention_id = defense_system.record_invention(
        title="Adaptive Notch Filter for Hum Removal",
        description="""An adaptive notch filter that automatically tracks and removes 
        50/60Hz hum and its harmonics from audio signals. The filter uses a 
        phase-locked loop to estimate the fundamental frequency of the hum and 
        adjusts notch filter coefficients in real-time to maintain optimal 
        rejection while minimizing effects on the desired audio signal.""",
        inventors=["Jane Audio Engineer", "John DSP Specialist"],
        documents=["design_spec.pdf", "simulation_results.m"]
    )
    
    print(f"Recorded invention with ID: {invention_id}")
    
    # Create a defensive publication
    pub_id = defense_system.create_defensive_publication(
        invention_id=invention_id,
        publication_title="Adaptive Notch Filter for Power Line Hum Removal in Audio Signals",
        publication_venue="Company Technical Blog",
        additional_context="This invention was developed for use in professional audio equipment."
    )
    
    print(f"Created defensive publication with ID: {pub_id}")
    
    # Add some prior art (example)
    defense_system.add_prior_art(
        title="Adaptive Filtering for Noise Cancellation",
        authors=["Smith, J.", "Johnson, A."],
        publication_date="2010-03-15",
        source="IEEE Transactions on Signal Processing",
        content="Describes an adaptive filter structure for noise cancellation applications...",
        url="https://doi.org/10.1109/TSP.2010.123456"
    )
    
    # Conduct FTO analysis for a new idea
    fto_analysis = defense_system.generate_fto_analysis(
        invention_description="""A machine learning-based approach to audio noise reduction 
        that uses neural networks to distinguish between speech and noise in the 
        frequency domain.""",
        keywords=[
            "neural network", "noise reduction", "audio", "machine learning",
            "deep learning", "speech enhancement", "DNN", "CNN", "RNN"
        ]
    )
    
    print(f"FTO Analysis Risk Level: {fto_analysis['risk_assessment']}")
    print(f"Relevant Prior Art Found: {fto_analysis['relevant_prior_art_count']}")
    
    # Set up patent monitoring
    monitoring_results = defense_system.monitor_new_patents(weeks=4)
    print(f"Patent monitoring check completed at: {monitoring_results[0]['last_check']}")
    
    return {
        "invention_id": invention_id,
        "publication_id": pub_id,
        "fto_analysis": fto_analysis,
        "monitoring_results": monitoring_results
    }

if __name__ == "__main__":
    example_patent_defense_workflow()
```

## EDGE CASES & FALLBACKS
- **Public Disclosure Risks**: Balance defensive publishing with trade secret considerations
- **Incomplete Documentation**: Implement invention disclosure forms with required fields
- **Prior Art Search Limitations**: Use multiple search strategies and professional search services
- **Algorithm Complexity**: Simplify descriptions for publications while preserving novelty
- **Timing Issues**: Publish defensively before public disclosure or product launch
- **International Considerations**: Account for different patent laws in various jurisdictions
- **Cost Management**: Prioritize defensive publishing for core innovations
- **Maintenance Overhead**: Implement automated reminders for periodic portfolio reviews
- **Legal Review**: Have patent counsel review defensive publications before release
- **Employee Training**: Educate staff on invention disclosure and documentation practices

## INTEGRATION POINTS
- Patent Databases: USPTO, EPO, WIPO, Google Patents, Lens.org
- Invention Tracking: LabArchives, Benchling, custom LIMS systems
- Publication Platforms: arXiv, ResearchGate, company blogs, technical conferences
- Monitoring Services: Patent monitoring services (PatSnap, Innography, Questel)
- Legal Services: Patent attorneys, IP law firms, in-house IP counsel
- Documentation Tools: Electronic lab notebooks, version control systems (Git)
- Collaboration Tools: Confluence, SharePoint, Notion for invention documentation
- Standards: ISO 9001, ISO 56000 (innovation management), IEEE intellectual property standards
- Financial Systems: IP valuation tools, insurance for IP infringement defense
- Government Resources: USPTO Inventors Assistance Center, CIPO, EPO Patent Information Services

## EXECUTION EXAMPLES

**Input:** "Document a new adaptive audio compressor algorithm for defensive publication"
**Output:**
```
Patent Defense System Workflow:

1. Invention Recording:
   - Title: "Adaptive Audio Compressor with Programmable Knee Characteristics"
   - Description: "An audio compressor that dynamically adjusts its knee characteristic 
                   based on input signal statistics to provide transparent compression 
                   for low-level signals while maintaining aggressive compression 
                   for transients."
   - Inventors: ["Alex Audio Engineer", "Sam DSP Designer"]
   - Date: 2024-01-15
   - Documents: ["algorithm_spec.pdf", "matlab_model.slx", "listening_test_results.docx"]

2. Defensive Publication:
   - Title: "Adive Audio Compressor with Signal-Statistics-Dependent Knee"
   - Venue: Company Technical Research Blog
   - Date: 2024-01-20
   - Content: Detailed description of the algorithm, implementation approach, 
              and experimental results

3. Prior Art Search:
   - Keywords: ["audio compressor", "adaptive knee", "dynamic range compression", 
                "signal statistics", "programmable compressor"]
   - Results: Found 12 relevant prior art references
   - Assessment: Moderate freedom-to-operate risk due to existing adaptive compressor patents

4. Recommendations:
   - File provisional patent application within 12 months
   - Continue defensive publishing for improvements and variations
   - Monitor competitor patent filings in audio dynamics processing
   - Consider licensing strategy for non-core applications
```