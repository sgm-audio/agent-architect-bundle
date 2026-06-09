---
name: local-llms
description: Running large language models locally, including model deployment, inference optimization, quantization, fine-tuning, and local AI assistants. Use when working with local LLM deployment, Ollama, LM Studio, llama.cpp, text generation, or privacy-focused AI.
---

# Local Large Language Models Skills

## Model Selection and Download

### Popular Open Models
- **Llama 3/3.1**: Meta's flagship open model (8B, 70B, 405B)
- **Mistral/Mixtral**: Efficient sparse mixture of experts
- **Phi-3**: Microsoft's small, capable models
- **Qwen**: Alibaba's multilingual models
- **Gemma**: Google's open models
- **Falcon**: Technology Innovation Institute models
- **Mistral NeMo**: Cutting-edge instruction following

### Specialized Models
- **Code models**: CodeLlama, DeepSeek Coder, Qwen-Coder
- **Math models**: WizardMath, Abel, Minerva
- **Roleplay models**: Various fine-tuned variants
- **Embedding models**: For semantic search, BGE, nomic-embed-text

### Finding Models
- **Hugging Face**: Primary source for model weights
- **Ollama library**: Curated optimized models
- **The Bloke**: GGUF quantized models
- **Model scopes**: Various model repositories

## Ollama

### Installation and Setup
- **Install Ollama**: `curl -fsSL https://ollama.com/install.sh | sh`
- **Verify installation**: `ollama --version`
- **Run as service**: Background service with auto-start
- **GPU support**: CUDA and Metal acceleration

### Basic Usage
- **List models**: `ollama list`
- **Pull models**: `ollama pull <model>`
- **Run model**: `ollama run <model>`
- **Remove model**: `ollama rm <model>`

### API Server
- **Start server**: `ollama serve`
- **Generate endpoint**: `/api/generate`
- **Chat endpoint**: `/api/chat`
- **Embeddings**: `/api/embeddings`
- **Streaming**: Stream responses for real-time output

### Model Management
- **Create from Modelfile**: Customize with Modelfile
- **Environment variables**: Configure Ollama
- **Model paths**: Custom model storage locations

## llama.cpp

### Building
- **Build from source**: Compile for maximum performance
- **CUDA support**: NVIDIA GPU acceleration
- **Metal support**: Apple Silicon acceleration
- **OpenBLAS**: CPU optimization

### Running Models
- **GGUF format**: Load quantized GGUF files
- **Interactive mode**: Chat with model
- **API server**: Expose OpenAI-compatible API
- **Benchmarking**: Measure performance

### Quantization
- **Q2_K - Q8_0**: Various quantization levels
- **IQ2/IQ3**: Improved quantization methods
- **K-quants**: Knowledge-distilled quantizations
- **Model size vs quality**: Trade-off considerations

## LM Studio

### GUI Features
- **Model browser**: Search and download models
- **Chat interface**: User-friendly chat UI
- **Model settings**: Context length, temperature, etc.
- **Fine-tune support**: Some fine-tuning capabilities

### Local Server
- **OpenAI-compatible API**: `/v1/chat/completions`
- **Local embedding server**: For RAG applications
- **Cross-platform**: Windows, Mac, Linux

## Text Generation Web UI

### Installation
- **Python environment**: Create and activate venv
- **CUDA/CPU**: Choose appropriate version
- **First-run setup**: Initial configuration

### Interface
- **Chat mode**: Conversational interface
- **Notebook mode**: Text generation with parameters
- **Parameters panel**: Adjust generation settings

### Extensions
- **Custom CSS**: UI customization
- **API access**: OpenAI-compatible endpoint
- **Model merging**: Combine model weights

## API Integration

### OpenAI-Compatible APIs
- **Base URL**: Configure for local endpoint
- **API keys**: Set dummy key for local models
- **Streaming**: Enable for real-time responses
- **Chat format**: Use chat/completions endpoint

### Code Integration
- **Python client**: OpenAI client with custom base URL
- **LangChain**: Local LLM integration
- **LlamaIndex**: Local RAG with local models
- **AutoGen**: Multi-agent systems

### Embeddings
- **Local embeddings**: nomic-embed-text, BGE
- **Vector databases**: Chroma, FAISS, Qdrant
- **Semantic search**: Build local search systems

## Fine-Tuning

### LoRA Fine-Tuning
- **Axolotl**: Popular fine-tuning tool
- **Unsloth**: Memory-efficient fine-tuning
- **QLoRA**: 4-bit quantized fine-tuning
- **Training data**: Prepare instruction datasets

### Training Process
- **Data preparation**: Format as instruction pairs
- **Configuration**: Training parameters
- **Training**: GPU memory management
- **Export**: Merge adapters with base model

### Parameter-Efficient Methods
- **LoRA**: Low-rank adaptation
- **QLoRA**: Quantized LoRA
- **AdapterFusion**: Multiple task adapters

## Model Optimization

### Quantization Techniques
- **GGML**: llama.cpp's quantization format
- **GGUF**: Updated format with better tooling
- **AWQ**: Activation-aware weight quantization
- **GPTQ**: Post-training quantization
- **SmoothQuant**: Activation quantization

### Performance Optimization
- **KV cache quantization**: Reduce memory usage
- **Flash Attention**: Memory-efficient attention
- **Context extension**: Techniques for longer contexts
- **Batch processing**: Multiple prompts efficiently

### Hardware Optimization
- **GPU offloading**: Load model partially in VRAM
- **CPU fallback**: Run on CPU if no GPU
- **Multi-GPU**: Distribute across GPUs
- **Apple Silicon**: Metal acceleration

## RAG (Retrieval-Augmented Generation)

### Embedding Models
- **Local embedding models**: BGE, nomic-embed-text
- **Embedding quantization**: Reduce embedding size
- **Multilingual**: Support multiple languages

### Vector Stores
- **Chroma**: Lightweight vector database
- **FAISS**: Facebook's similarity search
- **Qdrant**: Production-ready vector search
- **Milvus**: Scalable vector database

### RAG Pipeline
- **Document loading**: PDF, markdown, text
- **Text splitting**: Chunk documents intelligently
- **Embedding**: Generate embeddings
- **Retrieval**: Query vector store
- **Generation**: Combine context with prompt

### Advanced RAG
- **Hybrid search**: Combine keyword and semantic
- **Reranking**: Improve retrieval quality
- **Query transformation**: Rewrite queries
- **Multi-modal RAG**: Handle images and text

## Security and Privacy

### Local Deployment Benefits
- **Data privacy**: No data leaves your machine
- **Offline operation**: Works without internet
- **Cost control**: No API costs after model download
- **Customization**: Full control over models

### Security Considerations
- **Model sources**: Verify model integrity
- **Input validation**: Sanitize user inputs
- **Resource limits**: Prevent resource exhaustion
- **API authentication**: If exposing as service

## Troubleshooting

### Out of Memory (OOM)
- **Reduce context length**: Lower n_ctx
- **Use quantization**: Switch to lower-bit quantization
- **GPU offload**: Partially load model
- **Swap to CPU**: Fall back to CPU inference

### Slow Performance
- **Quantization level**: Use faster quantized models
- **GPU acceleration**: Ensure CUDA/Metal is active
- **Batch size**: Increase for throughput
- **Context length**: Reduce for speed

### Model Quality Issues
- **Try different model**: Find better base model
- **Adjust parameters**: Temperature, top_p, top_k
- **System prompt**: Craft better system message
- **Fine-tune**: Domain-specific fine-tuning

## Advanced Use Cases

### Chatbots
- **Character chatbots**: Roleplay with custom prompts
- **Documentation Q&A**: RAG over docs
- **Code assistants**: Programming help

### Automation
- **Script generation**: Write shell scripts, code
- **Text processing**: Batch transformation
- **Summ textarization**: Summarize documents

### Local AI Assistant
- **Voice input**: Speech-to-text integration
- **Vision**: Image understanding models
- **Multi-modal**: Combined capabilities

### Specialized Applications
- **Writing assistance**: Grammar, style improvement
- **Research assistant**: Paper analysis, summarization
- **Personal knowledge base**: Private Q&A system
