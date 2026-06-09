---
name: quantization-aware-training-qat-for-edge-ai
description: >-
  Use this skill when the user is working on or asking about quantization-aware training, QAT, INT8 quantization for audio models, model compression for edge deployment, or tflite/ONNX quantization.
version: 1.0.0
---

# SKILL: Quantization-Aware Training (QAT) for Edge AI

## CAPABILITIES
- Train neural networks with simulated quantization effects for deployment on edge hardware
- Optimize models for integer arithmetic (INT8) execution on accelerators like NPUs, DSPs
- Maintain accuracy while reducing model size and computational complexity
- Deploy quantized models on edge devices (mobile, embedded, IoT) with minimal latency
- Integrate quantization-aware training into existing deep learning workflows

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| Floating-point neural network model | Quantized model (INT8) with comparable accuracy |
| Training dataset | Quantized model weights and activation scales |
| Target hardware specifications (NPU, DSP, CPU) | Optimized quantization configuration |
| Accuracy and latency requirements | Quantization scheme (symmetric, asymmetric, per-channel) |
| Model architecture (CNN, RNN, Transformer) | Quantization-aware training configuration |

## IMPLEMENTATION PATTERN

```python
# Quantization-Aware Training Example using PyTorch
import torch
import torch.nn as nn
import torch.quantization
from torch.quantization import QuantStub, DeQuantStub

# Example: Quantizable CNN for audio classification
class AudioCNN(nn.Module):
    def __init__(self, num_classes=10):
        super(AudioCNN, self).__init__()
        # QuantStub converts tensors from float to quantized
        self.quant = QuantStub()
        # Feature extraction layers
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        # Classifier
        self.classifier = nn.Sequential(
            nn.Linear(128 * 4 * 4, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes)
        )
        # DeQuantStub converts tensors from quantized to float
        self.dequant = DeQuantStub()
    
    def forward(self, x):
        # Quantize input
        x = self.quant(x)
        # Feature extraction
        x = self.features(x)
        # Flatten
        x = torch.flatten(x, 1)
        # Classification
        x = self.classifier(x)
        # Dequantize output
        x = self.dequant(x)
        return x

def train_qat_model(model, train_loader, criterion, optimizer, device, epochs=10):
    # Set model to quantization-aware training mode
    model.train()
    model.qconfig = torch.quantization.get_default_qat_qconfig('fbgemm')
    # Prepare the model for QAT (inserts quantization and dequantization nodes)
    torch.quantization.prepare_qat(model, inplace=True)
    
    for epoch in range(epochs):
        running_loss = 0.0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            # Zero the parameter gradients
            optimizer.zero_grad()
            
            # Forward pass
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            # Backward pass and optimize
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
        
        print(f'Epoch {epoch+1}, Loss: {running_loss/len(train_loader):.3f}')
    
    # Convert the trained QAT model to a quantized model
    model.eval()
    # Convert to quantized model
    quantized_model = torch.quantization.convert(model.eval(), inplace=False)
    return quantized_model

# Example usage
if __name__ == "__main__":
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Create model
    model = AudioCNN(num_classes=10).to(device)
    
    # Define loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    # Assume we have a train_loader (omitted for brevity)
    # train_loader = ...
    
    # Train with QAT
    quantized_model = train_qat_model(model, train_loader, criterion, optimizer, device, epochs=15)
    
    # Save the quantized model
    torch.save(quantized_model.state_dict(), "audio_cnn_quantized.pth")
    
    # Test the quantized model
    # test_model(quantized_model, test_loader, device)
```

## EDGE CASES & FALLBACKS
- **Accuracy Drop**: Use quantization-aware training instead of post-training quantization, or adjust quantization scheme
- **Unsupported Operations**: Replace unsupported layers with quantizable alternatives or use float fallbacks
- **Dynamic Range Issues**: Use per-channel quantization for weights or histogram-based calibration
- **Performance Degradation**: Optimize memory access patterns, use operator fusion, or reduce model complexity
- **Hardware Incompatibility**: Verify quantization scheme matches target accelerator (e.g., TensorFlow Lite vs PyTorch QNNPACK)
- **Model Size**: Use pruning or knowledge distillation in combination with quantization
- **Training Instability**: Use learning rate scheduling, gradient clipping, or batch normalization folding
- **Activation Quantization**: Use moving average of min/max or histogram-based calibration for activations
- **Weight Quantization**: Use per-tensor or per-channel weighting, consider logarithmic quantization for wide distributions

## INTEGRATION POINTS
- Deep Learning Frameworks: PyTorch, TensorFlow, JAX
- Quantization Tools: TensorFlow Lite, ONNX Runtime Quantization, Intel Neural Compressor
- Hardware Accelerators: Google Edge TPU, Qualcomm Hexagon NPU, Apple Neural Engine, ARM Ethos-N
- Deployment Formats: TensorFlow Lite (.tflite), ONNX, TorchScript
- Calibration Datasets: Representative subsets of training data for post-training quantization
- Benchmarking Tools: MLPerf, AI Benchmark, custom latency and accuracy tests
- Optimization Techniques: Operator fusion, buffer reuse, memory pooling
- Model Zoos: TensorFlow Hub, PyTorch Torchvision, Hugging Face Models
- Edge Deployment: Android NNAPI, iOS Core ML, Linux VENNX, microcontroller CMSIS-NN

## EXECUTION EXAMPLES

**Input:** "Quantize a speech command recognition model for deployment on a microcontroller"
**Output:**
```python
# Assuming we have a trained model for speech commands
model = SpeechCommandCNN(num_classes=30).to(device)

# Prepare for QAT
model.qconfig = torch.quantization.get_default_qat_qconfig('qnnpack')
torch.quantization.prepare_qat(model, inplace=True)

# Train with QAT (using speech commands dataset)
for epoch in range(20):
    train_one_epoch(model, train_loader, criterion, optimizer, device)
    validate(model, val_loader, device)

# Convert to quantized model
quantized_model = torch.quantization.convert(model.eval(), inplace=False)

# Further optimize for microcontroller (e.g., using CMSIS-NN)
# Convert to C code or static library for deployment on ARM Cortex-M
# This step would use tools like X-CUBE-AI or similar to generate optimized C code
```

**Input:** "Deploy a quantized audio effects model on a smartphone DSP"
**Output:**
```python
# After QAT and conversion
quantized_model = torch.quantization.convert(model.eval(), inplace=False)

# Export to ONNX for cross-platform deployment
dummy_input = torch.randn(1, 1, 128, 128)  # Example input shape
torch.onnx.export(quantized_model, 
                  dummy_input, 
                  "audio_effects_quantized.onnx",
                  export_params=True,
                  opset_version=11,
                  do_constant_folding=True,
                  input_names=['input'],
                  output_names=['output'],
                  dynamic_axes={'input': {0: 'batch_size'}, 
                                'output': {0: 'batch_size'}})

# The ONNX model can then be run on Android using the NNAPI delegate
# or on iOS using Core ML Tools to convert to .mlmodel
# For DSP-specific deployment, use the vendor's SDK (e.g., Qualcomm SNPE)
```