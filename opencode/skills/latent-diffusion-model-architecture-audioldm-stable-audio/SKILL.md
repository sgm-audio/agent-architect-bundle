---
name: latent-diffusion-model-architecture-audioldm-stable-audio
description: >-
  Use this skill when the user is working on or asking about AudioLDM, Stable Audio, latent diffusion for audio, text-to-audio generation, or diffusion-based audio synthesis.
version: 1.0.0
---

# SKILL: Latent Diffusion Model Architecture (AudioLDM/Stable Audio)

## CAPABILITIES
- Implement latent diffusion models for high-fidelity audio generation
- Fine-tune pre-trained AudioLDM or Stable Audio models on custom datasets
- Generate audio samples using text-to-audio or audio-to-audio translation
- Optimize inference for real-time or near-real-time audio generation
- Implement classifier-free guidance for controlled generation

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| Text prompts or audio conditioning signals | Generated audio waveforms |
| Pre-trained model checkpoints | Fine-tuned model weights |
| Training audio dataset | Learned latent diffusion model |
| Inference parameters (steps, guidance scale) | Generated audio samples |
| Computational constraints (memory, latency) | Optimized inference pipeline |

## IMPLEMENTATION PATTERN

```python
# Latent Diffusion Model for Audio Generation (AudioLDM/Stable Audio style)
import torch
import torch.nn as nn
from diffusers import AutoencoderKL, UNet2DConditionModel, DDIMScheduler
from transformers import CLIPTextModel, CLIPTokenizer

class AudioLDMPipeline:
    def __init__(self, 
                 vae_path: str = "cvssp/audioldm-s-full-v2",
                 unet_path: str = "cvssp/audioldm-s-full-v2",
                 text_encoder_path: str = "openai/clip-vit-large-patch14",
                 scheduler_path: str = "cvssp/audioldm-s-full-v2"):
        # Load components
        self.vae = AutoencoderKL.from_pretrained(vae_path, subfolder="vae")
        self.unet = UNet2DConditionModel.from_pretrained(unet_path, subfolder="unet")
        self.text_encoder = CLIPTextModel.from_pretrained(text_encoder_path)
        self.tokenizer = CLIPTokenizer.from_pretrained(text_encoder_path)
        self.scheduler = DDIMScheduler.from_pretrained(scheduler_path, subfolder="scheduler")
        
        # Set to evaluation mode
        self.vae.eval()
        self.unet.eval()
        self.text_encoder.eval()
        
        # Move to appropriate device
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.vae.to(self.device)
        self.unet.to(self.device)
        self.text_encoder.to(self.device)
        
        # Latent space scaling factor (from VAE)
        self.scale_factor = 0.18215  # Typical for AudioLDM
        
    def encode_audio(self, audio_waveform):
        """Convert audio waveform to latent representation"""
        # Preprocess audio to mel-spectrogram
        mel_spectrogram = self.audio_to_mel(audio_waveform)
        
        # Encode to latent space
        with torch.no_grad():
            latent = self.vae.encode(mel_spectrogram.unsqueeze(0).unsqueeze(0)) \
                             .latent_dist.sample()
            latent = latent * self.scale_factor
        return latent
    
    def decode_latent(self, latent):
        """Convert latent representation to audio waveform"""
        with torch.no_grad():
            latent = latent / self.scale_factor
            mel_spectrogram = self.vae.decode(latent).sample
            audio_waveform = self.mel_to_audio(mel_spectrogram)
        return audio_waveform
    
    def audio_to_mel(self, audio_waveform):
        """Convert waveform to mel-spectrogram (simplified)"""
        # In practice, use librosa or torchaudio
        # This is a placeholder for the actual implementation
        mel_spectrogram = torch.stft(audio_waveform, 
                                   n_fft=1024, 
                                   hop_length=256,
                                   win_length=1024,
                                   window=torch.hann_window(1024),
                                   return_complex=True)
        mel_spectrogram = torch.abs(mel_spectrogram)
        # Convert to mel scale (simplified)
        mel_spectrogram = torch.nn.functional.interpolate(
            mel_spectrogram.unsqueeze(1), 
            size=(64, mel_spectrogram.shape[-1]), 
            mode='bilinear'
        ).squeeze(1)
        return mel_spectrogram.log()  # Log mel-spectrogram
    
    def mel_to_audio(self, mel_spectrogram):
        """Convert mel-spectrogram to waveform (simplified)"""
        # In practice, use Griffin-Lim or neural vocoder
        # This is a placeholder for the actual implementation
        mel_spectrogram = torch.exp(mel_spectrogram)  # Inverse log
        mel_spectrogram = torch.nn.functional.interpolate(
            mel_spectrogram.unsqueeze(1), 
            size=(mel_spectrogram.shape[-2], 512),  # Assume 512 freq bins
            mode='bilinear'
        ).squeeze(1)
        # Griffin-Lim iteration (simplified)
        audio_waveform = torch.istft(mel_spectrogram, 
                                   n_fft=1024, 
                                   hop_length=256,
                                   win_length=1024,
                                   window=torch.hann_window(1024),
                                   length=audio_waveform_length)
        return audio_waveform
    
    def generate_audio(self, 
                      prompt: str, 
                      num_inference_steps: int = 50,
                      guidance_scale: float = 7.5,
                      audio_length_in_s: float = 10.0,
                      negative_prompt: str = ""):
        """Generate audio from text prompt using latent diffusion"""
        # Tokenize prompts
        text_input = self.tokenizer(
            prompt,
            padding="max_length",
            max_length=self.tokenizer.model_max_length,
            truncation=True,
            return_tensors="pt"
        )
        
        if negative_prompt:
            negative_input = self.tokenizer(
                negative_prompt,
                padding="max_length",
                max_length=self.tokenizer.model_max_length,
                truncation=True,
                return_tensors="pt"
            )
        
        # Encode text
        with torch.no_grad():
            text_embeddings = self.text_encoder(text_input.input_ids.to(self.device))[0]
            
            if negative_prompt:
                negative_embeddings = self.text_encoder(negative_input.input_ids.to(self.device))[0]
                # Classifier-free guidance: concatenate [negative, positive] embeddings
                text_embeddings = torch.cat([negative_embeddings, text_embeddings])
        
        # Calculate latent dimensions based on audio length
        # Assuming 16kHz sample rate, 256 hop length, 64 mel bins
        latent_height = 64
        latent_length = int((audio_length_in_s * 16000) / 256)  # Approximate
        latent_length = (latent_length // 8) * 8  # Make divisible by 8 for UNet
        
        # Initialize latent noise
        batch_size = 2 if negative_prompt else 1
        latents = torch.randn(
            (batch_size, self.vae.latent_channels, latent_height, latent_length),
            device=self.device
        )
        
        # Set scheduler timesteps
        self.scheduler.set_timesteps(num_inference_steps)
        
        # Diffusion process
        for t in self.scheduler.timesteps:
            # Expand latents for classifier-free guidance
            latent_model_input = torch.cat([latents] * 2) if negative_prompt else latents
            latent_model_input = self.scheduler.scale_model_input(latent_model_input, t)
            
            # Predict noise
            with torch.no_grad():
                noise_pred = self.unet(
                    latent_model_input,
                    t,
                    encoder_hidden_states=text_embeddings
                ).sample
            
            # Perform guidance
            if negative_prompt:
                noise_pred_uncond, noise_pred_text = noise_pred.chunk(2)
                noise_pred = noise_pred_uncond + guidance_scale * (noise_pred_text - noise_pred_uncond)
            
            # Compute previous sample
            latents = self.scheduler.step(noise_pred, t, latents).prev_sample
        
        # Decode latent to audio
        with torch.no_grad():
            audio = self.decode_latent(latents)
        
        return audio
    
    def fine_tune(self, 
                 train_dataset, 
                 learning_rate: float = 1e-5,
                 epochs: int = 10,
                 batch_size: int = 4,
                 gradient_accumulation_steps: int = 4):
        """Fine-tune the UNet on custom audio dataset"""
        # Set models to training mode
        self.unet.train()
        self.vae.requires_grad_(False)
        self.text_encoder.requires_grad_(False)
        
        # Optimizer
        optimizer = torch.optim.AdamW(self.unet.parameters(), lr=learning_rate)
        
        # Training loop
        for epoch in range(epochs):
            for step, batch in enumerate(train_dataset):
                # Get audio waveforms and text prompts
                audio_waveforms = batch["audio"]  # List of waveforms
                prompts = batch["text"]           # List of text prompts
                
                # Encode audio to latents
                with torch.no_grad():
                    latents = torch.stack([
                        self.encode_audio(waveform) for waveform in audio_waveforms
                    ])
                    latents = latents * self.scale_factor  # Scale as in training
                
                # Sample noise
                noise = torch.randn_like(latents)
                timesteps = torch.randint(
                    0, self.scheduler.config.num_train_timesteps, 
                    (latents.shape[0],), device=self.device
                ).long()
                
                # Add noise to latents
                noisy_latents = self.scheduler.add_noise(latents, noise, timesteps)
                
                # Encode text prompts
                text_input = self.tokenizer(
                    prompts,
                    padding="max_length",
                    max_length=self.tokenizer.model_max_length,
                    truncation=True,
                    return_tensors="pt"
                ).to(self.device)
                
                with torch.no_grad():
                    encoder_hidden_states = self.text_encoder(text_input.input_ids)[0]
                
                # Predict noise
                model_pred = self.unet(noisy_latents, timesteps, encoder_hidden_states).sample
                
                # Calculate loss
                loss = nn.functional.mse_loss(model_pred, noise)
                
                # Backpropagation
                loss.backward()
                
                if (step + 1) % gradient_accumulation_steps == 0:
                    optimizer.step()
                    optimizer.zero_grad()
                
                # Logging
                if step % 100 == 0:
                    print(f"Epoch {epoch}, Step {step}, Loss: {loss.item():.4f}")
            
            # Validation/saving logic would go here
            print(f"Epoch {epoch} completed")
        
        # Set back to evaluation mode
        self.unet.eval()
```

## EDGE CASES & FALLBACKS
- **Out-of-Memory Errors**: Use gradient checkpointing, reduce batch size, or enable CPU offloading
- **Low-Quality Generation**: Increase inference steps, adjust guidance scale, or improve training data quality
- **Training Instability**: Use learning rate warmup, gradient clipping, or EMA (Exponential Moving Average)
- **Inference Latency**: Use fewer DDIM steps, compile model with torch.compile(), or use TensorRT
- **Mode Collapse**: Increase classifier-free guidance scale, use diverse training data, or add noise to prompts
- **Text-Audio Misalignment**: Improve text encoder quality, use longer training sequences, or implement cross-attention losses
- **Vocoder Artifacts**: Use high-quality vocoder (HiFi-GAN, WaveGrad) or increase mel-spectrogram resolution
- **Length Mismatch**: Implement dynamic length handling or use padding/truncation strategies
- **Noise Sensitivity**: Add noise augmentation during training or use denormalization techniques

## INTEGRATION POINTS
- Audio Processing: Librosa, Torchaudio, SoX, FFmpeg
- Deep Learning Framework: PyTorch, TensorFlow, JAX
- Model Hubs: Hugging Face Hub, GitHub, ModelScope
- Vocoders: HiFi-GAN, WaveGrad, NSF, DiffWave
- Text Encoders: CLIP, T5, BERT, Text-to-Text Transfer Transformer
- Datasets: AudioCrowd, Freesound, WavText5K, AudioSet, ESC-50
- Evaluation: PESQ, STOI, MOSNet, Inception Score, FAD
- Deployment: ONNX, TorchScript, TensorRT, CoreML
- Audio Effects: Pedalboard, Audiolatch, Guitar Rig
- DAW Integration: VST3, AU, AAX, CLAP plugins
- Cloud Services: AWS SageMaker, Google Vertex AI, Azure Machine Learning

## EXECUTION EXAMPLES

**Input:** "Generate a 10-second audio clip of 'rainforest ambience with distant thunder'"
**Output:**
```python
# Initialize pipeline
pipeline = AudioLDMPipeline()

# Generate audio
audio = pipeline.generate_audio(
    prompt="rainforest ambience with distant thunder",
    num_inference_steps=50,
    guidance_scale=7.5,
    audio_length_in_s=10.0
)

# Save audio (using librosa or soundfile)
import soundfile as sf
sf.write("rainforest_thunder.wav", audio.cpu().numpy().squeeze(), 16000)
```

**Input:** "Fine-tune AudioLDM on a dataset of bird sounds for species-specific generation"
**Output:**
```python
# Initialize pipeline
pipeline = AudioLDMPipeline()

# Prepare bird sound dataset (pseudo-code)
bird_dataset = BirdSoundDataset(
    root_path="/path/to/bird/sounds",
    annotations_file="/path/to/bird/annotations.csv",
    transform=AudioLDMPreprocess()
)

# Fine-tune
pipeline.fine_tune(
    train_dataset=bird_dataset,
    learning_rate=1e-5,
    epochs=20,
    batch_size=2,
    gradient_accumulation_steps=8
)

# Generate bird sounds
audio = pipeline.generate_audio(
    prompt="Northern Cardinal song",
    num_inference_steps=30,
    guidance_scale=5.0,
    audio_length_in_s=5.0
)
sf.write("cardinal_song.wav", audio.cpu().numpy().squeeze(), 16000)
```