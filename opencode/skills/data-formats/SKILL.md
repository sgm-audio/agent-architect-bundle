---
name: data-formats
description: JSON, XML, and gzipped XML parsing, processing, validation, querying, and transformation. Use when working with data files, APIs, configuration files, XML documents, or compressed data formats.
---

# Data Formats Skills (JSON, XML, Gzipped XML)

## JSON

### Basic Operations
- **Parse JSON**: Read and parse JSON files
- **Pretty print**: Format JSON with indentation
- **Minify**: Remove whitespace
- **Validate**: Check JSON syntax
- **Query**: Extract values from JSON

### Tools
- **jq**: Command-line JSON processor
- **python -m json.tool**: Built-in JSON formatter
- **Node.js**: JSON parsing with node
- **Online validators**: Browser-based validation

### jq Examples
```bash
# Extract field
jq '.field' file.json

# Extract nested field
jq '.parent.child' file.json

# Array operations
jq '.items[]' file.json

# Filter
jq '.items[] | select(.value > 10)' file.json

# Map/transform
jq '[.items[] | {name: .title, id: .id}]' file.json

# Aggregation
jq '[.items[].price] | add' file.json
```

### JSON in Code
- **Python**: `json.load()`, `json.loads()`, `json.dump()`, `json.dumps()`
- **JavaScript**: `JSON.parse()`, `JSON.stringify()`
- **Go**: `encoding/json` package

### JSON Schema
- **Validation**: Validate against JSON Schema
- **Draft support**: Draft 4, 6, 7, 2019-09, 2020-12
- **Tools**: ajv, jsonschema

### JSON Lines (JSONL)
- **Parse**: One object per line
- **Process**: Stream processing
- **Tools**: jq supports JSONL

## XML

### Basic Operations
- **Parse XML**: Read XML documents
- **Pretty print**: Format XML
- **Validate**: Check well-formedness
- **XPath queries**: Extract elements
- **XSLT transforms**: Transform to other formats

### Tools
- **xmllint**: XML validation and formatting
- **xmlstarlet**: XML command-line tools
- **xsltproc**: XSLT processor
- **xpath**: XPath evaluation

### xmlstarlet Examples
```bash
# Validate XML
xmlstarlet val -w file.xml

# Format/pretty print
xmlstarlet fo file.xml

# Extract with XPath
xmlstarlet sel -t -v '//item/@id' file.xml

# Extract all titles
xmlstarlet sel -t -m '//book/title' -v '.' -n books.xml

# Transform with XSLT
xmlstarlet tr style.xsl data.xml
```

### XPath
- **Select elements**: `/root/child`
- **Attributes**: `@attribute`
- **Predicates**: `[position()]`, `[last()]`, `[@attr='value']`
- **Functions**: `text()`, `contains()`, `starts-with()`
- **Axes**: `//descendant`, `//parent`

### XSLT
- **Templates**: Match and transform
- **XPath**: Select content to transform
- **Output methods**: XML, HTML, text
- **Parameters**: Pass parameters to transforms

### Python XML
- **ElementTree**: `ET.parse()`, `ET.Element`, `ET.SubElement`
- **lxml**: Advanced XML processing
- **minidom**: DOM-based parsing

### XML in JavaScript
- **DOMParser**: Parse XML in browser
- **Node.js**: xml2js, fast-xml-parser

## Gzipped XML

### Decompression
- **gunzip**: Decompress .gz files
- **zcat**: View compressed file
- **gzip -d**: Decompress
- **Python gzip**: Decompress in code

### Pipeline Operations
```bash
# Decompress and parse
gunzip -c file.xml.gz | xmlstarlet fo -

# Search in compressed
gunzip -c logs.xml.gz | xmllint --xpath '//error' -

# Decompress to file
gunzip -c compressed.xml.gz > output.xml
```

### Streaming Large Files
- **Memory-efficient**: Don't load entire file
- **Chunked reading**: Process in chunks
- **SAX parsing**: Event-based XML parsing

### Combined Processing
```bash
# Find in gzipped XML
gzcat file.xml.gz | grep -i "pattern"

# Extract with XPath
gunzip -c data.xml.gz | xmlstarlet sel -t -v '//record/id'

# Validate compressed
gunzip -c schema.xml.gz | xmlstarlet val - - schema.xsd
```

## Advanced Processing

### Large File Handling
- **Streaming**: Process line by line
- **Chunked parsing**: Parse in chunks
- **Indexes**: Build XML indexes
- **Database import**: Import to SQLite/XDB

### JSON ↔ XML Conversion
- **xml2json**: Convert XML to JSON
- **json2xml**: Convert JSON to XML
- **Manual mapping**: Custom conversion

### Validation

#### JSON Schema
- **ajv**: JSON Schema validator
- **jsonschema**: Python validator
- **online validators**: Browser tools

#### XML Validation
- **DTD**: Document Type Definition
- **XSD**: XML Schema
- **RelaxNG**: Another schema language
- **Schematron**: Rule-based validation

### Query Languages
- **JSONPath**: XPath for JSON
- **JSONiq**: XQuery for JSON
- **XPath 3.1**: Unified XPath for XML/JSON

## Practical Use Cases

### API Responses
- **Parse API JSON**: Handle REST API responses
- **XML APIs**: SOAP and other XML APIs
- **Headers**: Handle Content-Encoding

### Configuration Files
- **JSON configs**: package.json, tsconfig.json
- **XML configs**: Maven POM, Ant builds
- **Convert configs**: Between formats

### Data Exchange
- **REST APIs**: JSON payloads
- **SOAP APIs**: XML messages
- **GraphQL**: JSON responses
- **EDI**: XML-based EDI

### Log Processing
- **Structured logs**: JSON logs
- **System logs**: XML formats
- **Analysis**: Parse and aggregate

### File Operations

#### Search and Extract
```bash
# Find JSON values
jq '.users[] | select(.active == true)' data.json

# Find XML elements
xmlstarlet sel -t -m '//product[price > 100]' -v '@id' -n catalog.xml

# Search compressed
zgrep "error" application.log.xml.gz
```

#### Transform
```bash
# JSON to CSV
jq -r '.[] | [.id, .name, .price] | @csv' items.json

# XML to CSV
xmlstarlet sel -t -m '//row' -v 'concat(id,",",name,",",price)' -n data.xml

# XML to JSON
xml2json < data.xml > data.json
```

## Troubleshooting

### JSON Issues
- **Trailing commas**: Common syntax error
- **Unicode**: Encoding issues
- **Numbers**: Floating point precision
- **Keys**: Duplicate keys not allowed

### XML Issues
- **Encoding**: Declare encoding properly
- **Entities**: Escape special characters
- **Namespaces**: Handle xmlns properly
- **Well-formed**: Close all tags

### Performance
- **Large files**: Use streaming
- **Memory**: Don't load full file
- **Indexes**: Pre-index for queries

## Programming Examples

### Python
```python
import json
import gzip
import xml.etree.ElementTree as ET

# JSON
with open('data.json') as f:
    data = json.load(f)

# Gzipped XML
with gzip.open('data.xml.gz', 'rt') as f:
    tree = ET.parse(f)
```

### JavaScript
```javascript
// JSON
const data = JSON.parse(jsonString);

// Gzipped XML (Node.js)
const zlib = require('zlib');
const fs = require('fs');
const xml = zlib.gunzipSync(fs.readFileSync('data.xml.gz')).toString();
```

### Bash
```bash
# Process JSON
jq '.data.items[] | select(.id > 10)' response.json

# Process XML
xmlstarlet sel -t -m '//item' -v '@id' -n data.xml

# Process gzipped XML
cat data.xml.gz | gunzip | xmlstarlet fo -
```
