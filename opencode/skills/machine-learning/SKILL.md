---
name: machine-learning
description: Machine learning algorithms, model training, neural networks, deep learning, feature engineering, model evaluation, MLOps, and ML frameworks. Use when working with ML models, training pipelines, data preprocessing, model deployment, or AI/ML projects.
---

# Machine Learning Skills

## Core ML Concepts

### Supervised Learning
- **Classification**: Binary and multi-class classification
- **Regression**: Linear, polynomial, and nonlinear regression
- **Sequence labeling**: Named entity recognition, POS tagging
- **Ensemble methods**: Random forests, gradient boosting

### Unsupervised Learning
- **Clustering**: K-means, DBSCAN, hierarchical clustering
- **Dimensionality reduction**: PCA, t-SNE, UMAP, autoencoders
- **Anomaly detection**: Isolation forests, one-class SVM
- **Association rules**: Market basket analysis

### Semi-supervised and Self-supervised
- **Pseudo-labeling**: Use predicted labels for unlabeled data
- **Contrastive learning**: SimCLR, MoCo approaches
- **Pretext tasks**: Self-supervised representation learning

## Data Preprocessing

### Feature Engineering
- **Feature scaling**: Standardization, normalization, min-max scaling
- **Encoding**: One-hot, label encoding, target encoding
- **Feature selection**: Correlation, importance, recursive elimination
- **Feature creation**: Polynomial features, interactions, binning
- **Text features**: TF-IDF, word embeddings, text vectorization

### Data Cleaning
- **Missing values**: Imputation strategies (mean, median, KNN)
- **Outlier detection**: Z-scores, IQR, isolation forests
- **Data validation**: Schema enforcement, type checking
- **Data augmentation**: Image, text, and tabular augmentation

### Data Splitting
- **Train/validation/test**: Standard data splits
- **Cross-validation**: K-fold, stratified, time-series split
- **Data leakage prevention**: Proper temporal and group splits

## Neural Networks

### Architecture Types
- **MLP**: Multi-layer perceptrons for tabular data
- **CNNs**: Convolutional neural networks for images
- **RNNs/LSTMs/GRUs**: Sequential data processing
- **Transformers**: Attention-based architectures
- **GANs**: Generative adversarial networks
- **Autoencoders**: Representation learning and generation

### Training Techniques
- **Backpropagation**: Gradient computation and weight updates
- **Optimization**: SGD, Adam, AdamW, RMSprop
- **Learning rate scheduling**: Step, exponential, cosine annealing
- **Batch normalization**: Internal covariate shift reduction
- **Dropout**: Regularization via neuron dropping
- **Early stopping**: Prevent overfitting
- **Gradient clipping**: Prevent exploding gradients

### Activation Functions
- **ReLU variants**: ReLU, Leaky ReLU, PReLU, ELU
- **Sigmoid/Softmax**: Output layer for classification
- **Tanh**: Hidden layer alternative

## Deep Learning Frameworks

### PyTorch
- **Tensors**: Creating and manipulating tensors
- **Datasets/DataLoaders**: Efficient data loading
- **nn.Module**: Custom model definition
- **Autograd**: Automatic differentiation
- **torch.optim**: Optimization algorithms
- **Distributed training**: Multi-GPU, multi-node training
- **TorchScript**: Model serialization and deployment

### TensorFlow/Keras
- **Sequential/Functional API**: Model building
- **Custom layers**: Extend functionality
- **tf.data**: Data pipeline construction
- **tf.keras.optimizers**: Training optimizers
- **TensorBoard**: Training visualization
- **TensorFlow Lite**: Mobile deployment
- **TensorFlow.js**: Browser deployment

### JAX
- **Functional transforms**: JIT, grad, vmap, pmap
- **Flax**: Neural network library
- **Haiku**: Simple neural network library

## Model Evaluation

### Metrics
- **Classification**: Accuracy, precision, recall, F1, AUC-ROC
- **Regression**: MSE, RMSE, MAE, R², MAPE
- **Ranking**: NDCG, MAP
- **Segmentation**: IoU, Dice coefficient
- **Object detection**: mAP, precision/recall per class

### Analysis
- **Confusion matrix**: Classification breakdown
- **ROC curves**: Threshold analysis
- **Learning curves**: Overfitting/underfitting diagnosis
- **Feature importance**: Permutation importance, SHAP values
- **Error analysis**: Systematic error investigation

### Model Validation
- **Holdout validation**: Simple train/test split
- **Cross-validation**: K-fold, stratified
- **Bootstrapping**: Confidence intervals
- **Statistical tests**: Model comparison significance

## Natural Language Processing

### Text Processing
- **Tokenization**: Word, subword, character tokenization
- **Stemming/Lemmatization**: Text normalization
- **Stop word removal**: Common word filtering
- **Named entity recognition**: Entity extraction
- **Part-of-speech tagging**: Syntactic analysis

### Embeddings
- **Word2Vec**: Skip-gram and CBOW
- **GloVe**: Global word vectors
- **FastText**: Subword embeddings
- **Transformers**: BERT, RoBERTa, GPT embeddings

### NLP Tasks
- **Text classification**: Sentiment, spam, topic
- **Machine translation**: Seq2seq, Transformer
- **Question answering**: Extractive, generative
- **Text generation**: Language modeling
- **Summarization**: Extractive, abstractive
- **Text similarity**: Semantic search

### Large Language Models
- **Fine-tuning**: Domain adaptation
- **Prompt engineering**: Few-shot, chain-of-thought
- **RLHF**: Reinforcement learning from human feedback
- **RAG**: Retrieval-augmented generation

## Computer Vision

### Image Processing
- **Image augmentation**: Rotation, flipping, color jittering
- **Preprocessing**: Resizing, normalization, cropping
- **Image segmentation**: Semantic, instance, panoptic

### Vision Models
- **Image classification**: ResNet, EfficientNet, ViT
- **Object detection**: YOLO, Faster R-CNN, DETR
- **Semantic segmentation**: U-Net, DeepLab
- **Face recognition**: FaceNet, ArcFace
- **Pose estimation**: OpenPose, HRNet

### Generative Vision
- **Image generation**: Diffusion models, GANs
- **Image-to-image**: Style transfer, super-resolution
- **Inpainting**: Image editing andLOps and Deployment

### Experiment completion

## M Tracking
- **MLflow**: Experiment and model tracking
- **Weights & Biases**: Visual experiment tracking
- **TensorBoard**: Training visualization
- **Neptune.ai**: Experiment management

### Model Registry
- **Model versioning**: Track model iterations
- **Model metadata**: Store hyperparameters and metrics
- **Model lineage**: Track data and code provenance

### Feature Stores
- **Feature engineering**: Define and compute features
- **Feature serving**: Low-latency feature lookup
- **Feature versioning**: Track feature changes

### Model Serving
- **REST API**: Flask, FastAPI serving
- **Batch inference**: Scheduled batch predictions
- **Real-time inference**: Low-latency serving
- **Edge deployment**: TensorFlow Lite, ONNX Runtime

### Containerization
- **Docker**: Containerize training and serving
- **Kubernetes**: Scale and manage deployments
- **KServe**: Kubernetes model serving

### CI/CD for ML
- **Pipeline automation**: Data validation, training, evaluation
- **Model testing**: Unit and integration tests
- **A/B testing**: Production model comparison
- **Canary deployments**: Gradual rollout

## AutoML

### Automated Feature Engineering
- **Feature tools**: Automated feature creation
- **AutoML feature selection**: Automatic relevance detection

### Automated Model Selection
- **Auto-sklearn**: Bayesian optimization for sklearn
- **TPOT**: Genetic programming approach
- **Auto-PyTorch**: Neural architecture search

### Neural Architecture Search
- **NAS methods**: Random, grid, Bayesian, evolutionary
- **Hyperparameter tuning**: Optuna, Ray Tune

## Reinforcement Learning

### RL Algorithms
- **Q-learning**: Value-based method
- **SARSA**: On-policy temporal difference
- **DQN**: Deep Q-Networks
- **Policy gradients**: REINFORCE, Actor-Critic
- **PPO**: Proximal Policy Optimization
- **DDPG/SAC**: Continuous control

### Environment Design
- **OpenAI Gym**: Standard RL environments
- **Custom environments**: Define state, action, reward
- **Multi-agent**: Cooperative and competitive settings

### Training Techniques
- **Exploration strategies**: Epsilon-greedy, Boltzmann
- **Reward shaping**: Design effective rewards
- **Curriculum learning**: Progressive difficulty

## Time Series

### Forecasting
- **ARIMA/SARIMA**: Statistical forecasting
- **Prophet**: Facebook's forecasting tool
- **LSTM/GRU**: Deep learning for sequences
- **Transformer**: Temporal fusion transformer

### Time Series Analysis
- **Decomposition**: Trend, seasonality, residuals
- **Stationarity**: Tests and transformations
- **Lag features**: Create time-based features
- **Rolling statistics**: Moving averages, windows

## Model Optimization

### Hyperparameter Tuning
- **Grid search**: Exhaustive search
- **Random search**: Randomized search
- **Bayesian optimization**: Efficient tuning
- **Population-based training**: Evolutionary tuning

### Model Compression
- **Pruning**: Remove unnecessary weights
- **Quantization**: Reduce precision (FP16, INT8)
- **Knowledge distillation**: Train smaller models
- **Architecture search**: Find efficient architectures

### Inference Optimization
- **Batching**: Process multiple inputs
- **Caching**: Cache frequent computations
- **ONNX**: Cross-platform optimization

## Ethics and Fairness

### Bias Detection
- **Demographic parity**: Equal outcome rates
- **Equalized odds**: Equal true/false positive rates
- **Individual fairness**: Similar predictions for similar individuals
- **Fairness metrics**: Multiple fairness criteria

### Bias Mitigation
- **Pre-processing**: Balance training data
- **In-processing**: Fairness constraints
- **Post-processing**: Adjust predictions

### Explainability
- **SHAP**: Feature importance attribution
- **LIME**: Local interpretable explanations
- **Attention visualization**: Transformer interpretability
- **Counterfactuals**: What-if explanations

## Troubleshooting

### Training Issues
- **Slow convergence**: Adjust learning rate, batch size
- **Overfitting**: Add regularization, reduce model size
- **Underfitting**: Increase model capacity
- **NaN losses**: Check for numerical issues, gradient clipping

### Data Issues
- **Class imbalance**: Oversampling, undersampling, SMOTE
- **Data leakage**: Proper train/test separation
- **Missing data**: Imputation or removal
- **Noisy labels**: Noise-robust training
