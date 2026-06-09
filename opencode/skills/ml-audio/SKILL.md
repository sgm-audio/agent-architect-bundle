---
name: ml-audio
description: Machine learning for audio applications including audio classification, speech recognition, music information retrieval, audio generation, and audio analysis. Use when working with ML models for audio, training audio neural networks, or implementing AI audio solutions.
license: MIT
allowed-tools:
  - read
  - write
  - bash
metadata:
  category: ai-machine-learning
  subcategory: audio
  difficulty: advanced
  tools: neural-networks, audio-processing, classification, generation
---

# ML Audio Agent

## Introduction to ML Audio

### Audio ML Applications

- **Audio classification**: Genre classification, instrument recognition
- **Speech processing**: Speech recognition, speaker identification
- **Music information retrieval**: Beat tracking, chord recognition
- **Audio generation**: Music generation, sound synthesis
- **Audio analysis**: Feature extraction, pattern recognition

### Audio Data Characteristics

- **High dimensionality**: Large feature spaces
- **Temporal nature**: Sequential data processing
- **Variability**: Wide range of audio characteristics
- **Noise sensitivity**: Robustness to noise
- **Real-time requirements**: Low latency processing

## Audio Feature Extraction

### Time-Domain Features

- **Zero-crossing rate**: Signal frequency content
- **Energy**: Signal power
- **Entropy of energy**: Signal complexity
- **Short-time energy**: Time-localized energy
- **Envelope**: Signal amplitude contour

### Frequency-Domain Features

- **Spectrogram**: Time-frequency representation
- **MFCCs**: Mel-frequency cepstral coefficients
- **Spectral centroid**: Brightness measure
- **Spectral rolloff**: Frequency below which most energy lies
- **Spectral flux**: Spectral change over time

### Perceptual Features

- **Loudness**: Perceived volume
- **Pitch**: Fundamental frequency
- **Timbre**: Sound quality characteristics
- **Harmony**: Harmonic content
- **Rhythm**: Temporal patterns

### Deep Learning Features

- **CNN features**: Convolutional neural network representations
- **RNN features**: Recurrent neural network states
- **Transformer features**: Attention-based representations
- **Autoencoder features**: Learned compressed representations
- **GAN features**: Generative adversarial representations

## Audio Neural Networks

### Convolutional Neural Networks (CNNs)

- **Spectrogram processing**: 2D convolution on spectrograms
- **1D convolution**: Direct audio signal processing
- **Temporal convolution**: Time-aware processing
- **Multi-scale convolution**: Different receptive fields
- **Residual connections**: Deep network training

### Recurrent Neural Networks (RNNs)

- **LSTM networks**: Long short-term memory
- **GRU networks**: Gated recurrent units
- **Bidirectional RNNs**: Context from both directions
- **Attention mechanisms**: Focus on important parts
- **Sequence-to-sequence**: Input-output sequence mapping

### Transformer Networks

- **Self-attention**: Context-aware processing
- **Positional encoding**: Sequence position information
- **Multi-head attention**: Multiple attention mechanisms
- **Encoder-decoder**: Sequence transformation
- **Pre-training**: Large-scale pretraining

### Autoencoders

- **Vanilla autoencoders**: Basic encoding-decoding
- **Variational autoencoders**: Probabilistic encoding
- **Denoising autoencoders**: Noise-robust learning
- **Sparse autoencoders**: Sparse representations
- **Convolutional autoencoders**: Spatial feature learning

### Generative Adversarial Networks (GANs)

- **Vanilla GANs**: Basic adversarial training
- **DCGANs**: Deep convolutional GANs
- **WGANs**: Wasserstein GANs
- **CycleGANs**: Unpaired image-to-image translation
- **StyleGANs**: Style-based generation

## Audio Classification

### Genre Classification

- **Feature extraction**: Relevant audio features
- **Model architecture**: Appropriate neural network
- **Training data**: Labeled genre examples
- **Evaluation metrics**: Accuracy, precision, recall
- **Real-time classification**: Low-latency processing

### Instrument Recognition

- **Timbral features**: Instrument-specific characteristics
- **Pitch analysis**: Pitch-based identification
- **Temporal patterns**: Playing technique recognition
- **Multi-instrument**: Simultaneous instrument detection
- **Polyphonic recognition**: Multiple instruments

### Speech Recognition

- **Acoustic modeling**: Speech sound modeling
- **Language modeling**: Language structure modeling
- **End-to-end**: Direct speech-to-text
- **Keyword spotting**: Specific word detection
- **Speaker identification**: Speaker recognition

### Audio Event Detection

- **Event classification**: Identify specific events
- **Temporal localization**: When events occur
- **Multi-event**: Multiple simultaneous events
- **Weak labeling**: Partial annotations
- **Sound separation**: Isolate individual events

## Audio Generation

### Music Generation

- **Melody generation**: Create melodic sequences
- **Harmony generation**: Generate chord progressions
- **Rhythm generation**: Create rhythmic patterns
- **Full composition**: Complete musical pieces
- **Style transfer**: Apply musical styles

### Sound Synthesis

- **Instrument synthesis**: Generate instrument sounds
- **Environmental sounds**: Create environmental audio
- **Special effects**: Generate sound effects
- **Voice synthesis**: Generate speech and singing
- **Texture synthesis**: Generate ambient textures

### Audio Style Transfer

- **Timbre transfer**: Change sound characteristics
- **Style mixing**: Combine different styles
- **Domain adaptation**: Adapt to different domains
- **Feature transfer**: Transfer learned features
- **Creative applications**: Artistic style transfer

## Audio Analysis

### Audio Segmentation

- **Music/speech segmentation**: Classify audio segments
- **Scene segmentation**: Identify acoustic scenes
- **Event segmentation**: Detect audio events
- **Structural segmentation**: Identify musical structure
- **Temporal segmentation**: Time-based segmentation

### Audio Similarity

- **Content-based similarity**: Similar audio content
- **Feature-based similarity**: Similar audio features
- **Semantic similarity**: Similar meaning
- **Temporal similarity**: Similar temporal patterns
- **Hybrid similarity**: Multiple similarity measures

### Audio Fingerprinting

- **Content fingerprints**: Unique audio signatures
- **Robust fingerprints**: Resistant to distortion
- **Fast matching**: Efficient fingerprint matching
- **Large-scale indexing**: Massive fingerprint databases
- **Copyright detection**: Identify copyrighted material

## Audio Processing Pipelines

### Data Preprocessing

- **Audio loading**: Load audio files
- **Resampling**: Convert sample rates
- **Normalization**: Normalize audio levels
- **Noise reduction**: Reduce background noise
- **Feature extraction**: Extract audio features

### Model Training

- **Dataset preparation**: Prepare training data
- **Model architecture**: Design neural network
- **Training configuration**: Set training parameters
- **Training execution**: Train the model
- **Validation**: Validate model performance

### Inference Pipeline

- **Input processing**: Prepare input data
- **Model inference**: Run model prediction
- **Post-processing**: Process model output
- **Result formatting**: Format results
- **Output delivery**: Deliver results

## Implementation Details

### Audio Data Formats

- **WAV files**: Uncompressed audio
- **MP3 files**: Compressed audio
- **FLAC files**: Lossless compression
- **RAW audio**: Raw audio data
- **Spectrograms**: Time-frequency representations

### Feature Engineering

- **Manual features**: Hand-crafted features
- **Learned features**: Neural network features
- **Hybrid features**: Combination of both
- **Dimensionality reduction**: Reduce feature dimensions
- **Feature selection**: Select relevant features

### Model Architectures

- **CNN architectures**: Convolutional networks
- **RNN architectures**: Recurrent networks
- **Transformer architectures**: Attention-based networks
- **Hybrid architectures**: Combination of architectures
- **Custom architectures**: Specialized designs

## Tools and Libraries

### Deep Learning Frameworks

- **TensorFlow**: Google's deep learning framework
- **PyTorch**: Facebook's deep learning framework
- **Keras**: High-level neural networks API
- **MXNet**: Flexible deep learning framework
- **Caffe**: Convolutional architecture for fast feature embedding

### Audio Processing Libraries

- **Librosa**: Python audio analysis library
- **Essentia**: C++ library for audio analysis
- **Madmom**: Music signal processing library
- **PyAudio**: Python audio I/O
- **SoundFile**: Audio file I/O

### ML Audio Libraries

- **torchaudio**: PyTorch audio library
- **tensorflow.audio**: TensorFlow audio processing
- **kapre**: Audio preprocessing layers
- **nnAudio**: Neural network audio processing
- **audiomentations**: Audio data augmentation

## Training and Evaluation

### Dataset Preparation

- **Data collection**: Gather audio data
- **Labeling**: Annotate audio data
- **Splitting**: Train/validation/test split
- **Augmentation**: Data augmentation techniques
- **Normalization**: Normalize audio features

### Training Process

- **Loss functions**: Define training objectives
- **Optimization**: Choose optimization algorithms
- **Hyperparameters**: Set model parameters
- **Early stopping**: Prevent overfitting
- **Checkpointing**: Save model checkpoints

### Evaluation Metrics

- **Classification**: Accuracy, precision, recall, F1-score
- **Regression**: MSE, MAE, R-squared
- **Generation**: Inception score, Fréchet distance
- **Similarity**: Cosine similarity, Euclidean distance
- **Real-time**: Latency, throughput

## Advanced Techniques

### Transfer Learning

- **Pre-trained models**: Use pre-trained networks
- **Fine-tuning**: Adapt pre-trained models
- **Feature extraction**: Use pre-trained features
- **Domain adaptation**: Adapt to new domains
- **Multi-task learning**: Learn multiple tasks

### Few-Shot Learning

- **Meta-learning**: Learn to learn
- **Prototype networks**: Learn class prototypes
- **Matching networks**: Learn to match
- **Relation networks**: Learn relation functions
- **MAML**: Model-agnostic meta-learning

### Self-Supervised Learning

- **Contrastive learning**: Learn similarities
- **Predictive coding**: Predict future frames
- **Masked prediction**: Predict masked inputs
- **Clustering**: Group similar examples
- **Generative modeling**: Learn data distribution

## Real-Time Applications

### Real-Time Classification

- **Low-latency inference**: Fast predictions
- **Streaming processing**: Process continuous audio
- **Buffer management**: Efficient buffer handling
- **Resource optimization**: Efficient resource usage
- **Quality monitoring**: Monitor classification quality

### Real-Time Generation

- **Low-latency generation**: Fast audio generation
- **Streaming generation**: Generate continuous audio
- **Buffer management**: Efficient buffer handling
- **Resource optimization**: Efficient resource usage
- **Quality monitoring**: Monitor generation quality

### Edge Computing

- **Model optimization**: Optimize for edge devices
- **Quantization**: Reduce model precision
- **Pruning**: Remove unnecessary parameters
- **Compilation**: Optimize for specific hardware
- **Deployment**: Deploy to edge devices

## Best Practices

### Data Management

- **Data quality**: Ensure high-quality data
- **Data diversity**: Diverse training data
- **Data privacy**: Protect sensitive data
- **Data versioning**: Version control data
- **Data documentation**: Document data characteristics

### Model Development

- **Model validation**: Validate model performance
- **Model testing**: Test model thoroughly
- **Model monitoring**: Monitor model performance
- **Model updating**: Update models regularly
- **Model documentation**: Document model characteristics

### Production Deployment

- **Performance monitoring**: Monitor system performance
- **Error handling**: Handle errors gracefully
- **Resource management**: Manage system resources
- **Security**: Ensure system security
- **Scalability**: Scale system as needed

## Common Challenges

### Challenge: Limited Data

**Solution**: Data augmentation, transfer learning, few-shot learning

### Challenge: Class Imbalance

**Solution**: Class weighting, oversampling, undersampling

### Challenge: Overfitting

**Solution**: Regularization, dropout, data augmentation

### Challenge: Real-time Requirements

**Solution**: Model optimization, efficient algorithms, hardware acceleration

### Challenge: Noisy Data

**Solution**: Noise reduction, robust features, data cleaning

## Future Trends

### Emerging Technologies

- **Self-supervised learning**: Learn without labels
- **Few-shot learning**: Learn with minimal data
- **Meta-learning**: Learn to learn
- **Neuromorphic computing**: Brain-inspired computing
- **Quantum computing**: Quantum-enhanced learning

### Advanced Applications

- **Personalized audio**: Personalized audio experiences
- **Context-aware audio**: Context-aware processing
- **Multi-modal learning**: Learn from multiple modalities
- **Cross-domain learning**: Learn across domains
- **Explainable AI**: Understandable AI decisions

## Learning Resources

### Courses

- **Coursera**: Deep Learning Specialization
- **Udacity**: AI for Sound
- **Fast.ai**: Practical Deep Learning
- **edX**: Machine Learning with Python
- **Kadenze**: Audio Signal Processing

### Books

- **Deep Learning** by Goodfellow et al.
- **Hands-On Machine Learning** by Aurélien Géron
- **Audio Signal Processing for Music Applications** by Xavier Serra
- **Deep Learning for Audio** by Yoon Kim
- **Machine Learning for Audio** by Paris Smaragdis

### Papers

- **arXiv**: ML audio research papers
- **ICASSP**: IEEE International Conference on Acoustics
- **ISMIR**: International Society for Music Information Retrieval
- **DCASE**: Detection and Classification of Acoustic Scenes
- **NeurIPS**: Neural Information Processing Systems

---

**Note**: This skill provides comprehensive ML audio guidance and techniques. ML audio combines signal processing and machine learning - understand both domains to create effective audio ML solutions.
