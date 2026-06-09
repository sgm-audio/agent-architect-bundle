---
name: open-source-license-compliance-automation-fossology
description: >-
  Use this skill when the user is working on or asking about FOSSology, open source license compliance, SPDX, license scanning, or automated license compatibility checking.
version: 1.0.0
---

# SKILL: Open Source License Compliance Automation (FOSSology)

## CAPABILITIES
- Automate open source license compliance scanning using FOSSology or similar tools
- Generate accurate Software Bills of Materials (SBOMs) in SPDX format
- Detect license conflicts and copyleft contamination in proprietary codebases
- Track license obligations and maintain compliance documentation
- Integrate compliance checks into CI/CD pipelines for continuous monitoring

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| Source code repositories | Scanned dependency tree with license information |
| Build artifacts (binaries, libraries) | Identified components and their licenses |
| License policy requirements | Compliance status and violation reports |
| SPDX license expressions | Normalized license identifiers and exceptions |
| Build system configuration | Integrated compliance checks in build process |

## IMPLEMENTATION PATTERN

```bash
# Open Source License Compliance Automation using FOSSology
#!/bin/bash

# Configuration
REPO_URL="https://github.com/yourcompany/your-audio-plugin"
OUTPUT_DIR="./compliance_report"
FOSSOLOGY_URL="http://localhost:8080"  # FOSSology web interface
AGENT_NAME="audio-plugin-compliance"
UPLOAD_DIR="/tmp/fossology_upload"

# Function to check if FOSSology is running
check_fossology() {
    if ! curl -s "${FOSSOLOGY_URL}/rest/api/info" > /dev/null; then
        echo "Error: FOSSology is not running at ${FOSSOLOGY_URL}"
        echo "Please start FOSSology using: docker run -d -p 8080:8080 fossology/fossology"
        return 1
    fi
    return 0
}

# Function to prepare source code for upload
prepare_source() {
    local repo_dir="$1"
    local upload_dir="$2"
    
    # Create clean export (exclude build artifacts, etc.)
    mkdir -p "${upload_dir}"
    
    # Copy source files (adjust patterns as needed)
    cp -r "${repo_dir}/src" "${upload_dir}/" 2>/dev/null || true
    cp -r "${repo_dir}/include" "${upload_dir}/" 2>/dev/null || true
    cp -r "${repo_dir}/lib" "${upload_dir}/" 2>/dev/null || true
    cp "${repo_dir}/"*.[ch] "${upload_dir}/" 2>/dev/null || true
    cp "${repo_dir}/"*.[ch]pp "${upload_dir}/" 2>/dev/null || true
    cp "${repo_dir}/Makefile" "${upload_dir}/" 2>/dev/null || true
    cp "${repo_dir}/CMakeLists.txt" "${upload_dir}/" 2>/dev/null || true
    cp "${repo_dir}/package.json" "${upload_dir}/" 2>/dev/null || true
    
    # Create manifest
    cat > "${upload_dir}/manifest.txt" << EOF
Uploaded by: $AGENT_NAME
Date: $(date -Iseconds)
Repository: $REPO_URL
EOF
}

# Function to upload to FOSSology
upload_to_fossology() {
    local upload_dir="$1"
    local upload_name="$2"
    
    # Create agent if it doesn't exist
    if ! curl -s -X GET "${FOSSOLOGY_URL}/rest/agents?name=${AGENT_NAME}" | grep -q '"name"'; then
        curl -s -X POST "${FOSSOLOGY_URL}/rest/agents" \
             -H "Content-Type: application/json" \
             -d "{\"name\":\"${AGENT_NAME}\",\"description\":\"Automated compliance agent for audio plugins\"}"
    fi
    
    # Get agent ID
    AGENT_ID=$(curl -s -X GET "${FOSSOLOGY_URL}/rest/agents?name=${AGENT_NAME}" | \
               grep -o '"id":[0-9]*' | cut -d'"' -f4)
    
    # Create upload
    RESPONSE=$(curl -s -X POST "${FOSSOLOGY_URL}/rest/uploads" \
               -F "upload=@${upload_dir}/manifest.txt;filename=manifest.txt" \
               -F "upload=@${upload_dir}/src;filename=src;type=directory" \
               -F "upload=@${upload_dir}/include;filename=include;type=directory" \
               -F "upload=@${upload_dir}/lib;filename=lib;type=directory" \
               -H "Authorization: token ${AGENT_ID}")
    
    UPLOAD_ID=$(echo "$RESPONSE" | grep -o '"id":[0-9]*' | cut -d'"' -f4)
    echo "Upload ID: $UPLOAD_ID"
    
    # Schedule analysis
    curl -s -X POST "${FOSSOLOGY_URL}/rest/uploads/${UPLOAD_ID}/analyze" \
         -H "Content-Type: application/json" \
         -d "{\"agent_id\":\"${AGENT_ID}\",\"nomarch\":\"true\",\"nosanitize\":\"true\"}"
    
    return $UPLOAD_ID
}

# Function to wait for analysis completion
wait_for_analysis() {
    local upload_id="$1"
    local timeout=${2:-300}  # 5 minutes default
    local elapsed=0
    local interval=10
    
    while [ $elapsed -lt $timeout ]; do
        STATUS=$(curl -s -X GET "${FOSSOLOGY_URL}/rest/uploads/${upload_id}" | \
                 grep -o '"status":"[^"]*"' | cut -d'"' -f4)
        
        if [ "$STATUS" = "finished" ]; then
            echo "Analysis completed"
            return 0
        elif [ "$STATUS" = "error" ]; then
            echo "Analysis failed"
            return 1
        fi
        
        sleep $interval
        elapsed=$((elapsed + interval))
        echo -n "."
    done
    
    echo "Timeout waiting for analysis completion"
    return 1
}

# Function to generate SPDX SBOM
generate_spdx_sbom() {
    local upload_id="$1"
    local output_file="$2"
    
    # Request SPDX output
    curl -s -X GET "${FOSSOLOGY_URL}/rest/uploads/${upload_id}/spdx" \
         -H "Accept: application/vnd.spdx+json" \
         -o "$output_file"
    
    if [ -s "$output_file" ]; then
        echo "SPDX SBOM generated: $output_file"
        return 0
    else
        echo "Failed to generate SPDX SBOM"
        return 1
    fi
}

# Function to check license compliance
check_license_compliance() {
    local sbom_file="$1"
    local policy_file="$2"  # Optional policy file
    
    # For demonstration, we'll do a simple check
    # In practice, use tools like jaspy, licensee, or integrate with FOSSology's REST API
    
    echo "Checking license compliance..."
    
    # Extract license information from SPDX
    if [ -f "$sbom_file" ]; then
        # Count different license types
        echo "License summary:"
        grep -o '"licenseIdentifiers":\[[^]]*' "$sbom_file" | \
            tr '[],' '\n' | \
            grep -v '^$' | \
            sort | \
            uniq -c | \
            sort -nr
        
        # Check for problematic licenses (example: strong copyleft)
        echo -e "\nChecking for strong copyleft licenses..."
        if grep -q '"GPL-3.0"\|"AGPL-3.0"\|"GFDL-1.3"' "$sbom_file"; then
            echo "WARNING: Strong copyleft licenses detected - may require source code disclosure"
            return 1
        else
            echo "No strong copyleft licenses detected"
            return 0
        fi
    else
        echo "Error: SBOM file not found"
        return 1
    fi
}

# Main execution
main() {
    echo "Starting Open Source License Compliance Automation"
    
    # Check prerequisites
    if ! check_fossology; then
        exit 1
    fi
    
    # Parse arguments (simplified)
    while [[ $# -gt 0 ]]; do
        case $1 in
            --repo)
                REPO_URL="$2"
                shift 2
                ;;
            --output)
                OUTPUT_DIR="$2"
                shift 2
                ;;
            *)
                echo "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    # Create output directory
    mkdir -p "$OUTPUT_DIR"
    
    # Clone or update repository
    REPO_DIR="${OUTPUT_DIR}/source"
    if [ -d "${REPO_DIR}" ]; then
        echo "Updating existing repository..."
        cd "${REPO_DIR}" && git pull
    else
        echo "Cloning repository..."
        git clone "$REPO_URL" "$REPO_DIR"
    fi
    
    # Prepare source for upload
    UPLOAD_DIR="${OUTPUT_DIR}/upload"
    prepare_source "$REPO_DIR" "$UPLOAD_DIR"
    
    # Upload to FOSSology
    echo "Uploading source code to FOSSology..."
    UPLOAD_ID=$(upload_to_fossology "$UPLOAD_DIR" "audio-plugin-source")
    
    if [ $? -ne 0 ]; then
        echo "Failed to upload to FOSSology"
        exit 1
    fi
    
    # Wait for analysis
    echo "Waiting for analysis to complete..."
    if ! wait_for_analysis "$UPLOAD_ID"; then
        echo "Analysis failed or timed out"
        exit 1
    fi
    
    # Generate SPDX SBOM
    SBOM_FILE="${OUTPUT_DIR}/audio-plugin-sbom.spdx"
    echo "Generating SPDX SBOM..."
    if ! generate_spdx_sbom "$UPLOAD_ID" "$SBOM_FILE"; then
        echo "Failed to generate SPDX SBOM"
        exit 1
    fi
    
    # Check license compliance
    echo "Checking license compliance..."
    if check_license_compliance "$SBOM_FILE"; then
        echo "License compliance check passed"
    else
        echo "License compliance check failed - see warnings above"
        # Depending on policy, you might want to exit with error
    fi
    
    # Generate human-readable report
    REPORT_FILE="${OUTPUT_DIR}/compliance_report.html"
    echo "Generating HTML report..."
    curl -s -X GET "${FOSSOLOGY_URL}/rest/uploads/${UPLOAD_ID}/nomos_browse" \
         -o "$REPORT_FILE"
    
    echo "Compliance automation completed successfully"
    echo "Reports available in: ${OUTPUT_DIR}"
    echo "  - SPDX SBOM: audio-plugin-sbom.spdx"
    echo "  - HTML Report: compliance_report.html"
}

# Run main function with all arguments
main "$@"
```

## EDGE CASES & FALLBACKS
- **FOSSology Unavailable**: Fall back to alternative tools like ScanCode, Licensee, or manual review
- **Large Codebases**: Implement incremental scanning or exclude large binary assets
- **Proprietary Code**: Create allowlists for known proprietary components
- **License Detection Errors**: Maintain override list for commonly misidentified licenses
- **Complex Dependencies**: Handle nested dependencies and bundled libraries properly
- **Build System Variations**: Adapt preparation script for different build systems (CMake, Make, Maven, etc.)
- **Network Issues**: Implement retry mechanisms with exponential backoff
- **Authentication**: Add support for authenticated FOSSology instances
- **Scan Timeout**: Adjust analysis parameters for large or complex projects
- **False Positives**: Implement review process to validate automated findings

## INTEGRATION POINTS
- Build Systems: CMake, Make, Maven, Gradle, npm, yarn
- Version Control: Git, SVN, Mercurial
- CI/CD: Jenkins, GitLab CI, GitHub Actions, Azure Pipelines, CircleCI
- Containerization: Docker, Podman, Kubernetes
- Alternative Scanners: ScanCode, Licensee, FOSSLight, Black Duck, Snyk
- SPDX Tools: jaspy, sbom-tools, cyclonedx-bom
- License Policies: SPDX License List, Fedora Licensing Database, Debian Licensing
- Issue Trackers: Jira, GitHub Issues, YouTrack for tracking compliance tasks
- Documentation: Confluence, Wikis for publishing compliance reports
- Legal Review: Integration with legal approval workflows for license exceptions
- Package Managers: npm, pip, Cargo, Conan for dependency license checking

## EXECUTION EXAMPLES

**Input:** "Scan a VST3 audio plugin repository for license compliance"
**Output:**
```
$ ./license_compliance_scan.sh --repo https://github.com/example/audio-vst3-plugin --output ./compliance

Starting Open Source License Compliance Automation
Cloning repository...
Updating existing repository...
Preparing source code for upload...
Uploading source code to FOSSology...
Upload ID: 1245
Waiting for analysis to complete...
Analysis completed
Generating SPDX SBOM...
SPDX SBOM generated: ./compliance/audio-plugin-sbom.spdx
Checking license compliance...
License summary:
      5 MIT
      3 BSD-2-Clause
      2 Apache-2.0
      1 GPL-3.0
WARNING: Strong copyleft licenses detected - may require source code disclosure
Generating HTML report...
Compliance automation completed successfully
Reports available in: ./compliance
  - SPDX SBOM: audio-plugin-sbom.spdx
  - HTML Report: compliance_report.html
```

**Input:** "Automate license compliance checks in CI/CD pipeline for every pull request"
**Output:**
```yaml
# Example GitHub Actions workflow
name: License Compliance Check

on:
  pull_request:
    branches: [ main ]
  push:
    branches: [ main ]

jobs:
  license-compliance:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up FOSSology (using Docker)
      run: |
        docker run -d -p 8080:8080 --name fossology fossology/fossology
        # Wait for FOSSology to start
        sleep 10
    
    - name: Run license compliance scan
      run: |
        ./license_compliance_scan.sh --repo . --output ./compliance
    
    - name: Upload compliance report
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: compliance-report
        path: ./compliance/
    
    - name: Clean up FOSSology container
      if: always()
      run: |
        docker stop fossology
        docker rm fossology
```