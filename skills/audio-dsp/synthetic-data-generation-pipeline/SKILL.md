---
name: synthetic-data-generation-pipeline
description: ">-"
version: 1.0.0
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Synthetic Data Generation Pipeline", "opencode-migrated"]
    related_skills: []
---


# SKILL: Synthetic Data Generation Pipeline

## CAPABILITIES
- Generate synthetic audio data for training machine learning models
- Create label-perfect datasets using physical modeling synthesis
- Avoid copyright issues by generating original synthetic content
- Scale data generation to produce large datasets efficiently
- Implement quality control mechanisms for synthetic data

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| Physical model parameters (instrument specifications) | Synthetic audio waveforms |
| Desired dataset characteristics (size, diversity, labels) | Labeled synthetic dataset |
| Quality requirements (SNR, clipping, artifacts) | Quality-controlled audio files |
| Generation constraints (time, computational resources) | Optimized synthesis pipeline |
| Metadata specifications | Dataset manifest and documentation |

## IMPLEMENTATION PATTERN

```python
# Synthetic Data Generation Pipeline for Audio ML
import numpy as np
import scipy.signal
import scipy.io.wavfile
import librosa
import json
import os
from concurrent.futures import ProcessPoolExecutor
from typing import Dict, List, Tuple, Optional
import random

# Physical modeling synthesizer (simplified example: plucked string)
class StringSynthesizer:
    def __init__(self, 
                 sample_rate: int = 48000,
                 string_length: float = 0.65,  # meters
                 tension: float = 80.0,        # Newtons
                 linear_density: float = 0.0005, # kg/m
                 damping: float = 0.001):
        self.sample_rate = sample_rate
        self.string_length = string_length
        self.tension = tension
        self.linear_density = linear_density
        self.damping = damping
        
        # Calculate fundamental frequency
        self.f0 = (1.0 / (2.0 * string_length)) * np.sqrt(tension / linear_density)
        self.max_delay = int(sample_rate * string_length / np.sqrt(tension / linear_density))
        
    def pluck(self, 
              midi_note: int, 
              velocity: float = 0.8,
              duration: float = 2.0) -> np.ndarray:
        """Pluck string synthesizer"""
        # Convert MIDI note to frequency
        f0 = 440.0 * 2.0 ** ((midi_note - 69) / 12.0)
        
        # Calculate delay length for fractional delay
        delay_len = self.sample_rate / f0
        delay_len_int = int(np.floor(delay_len))
        frac_part = delay_len - delay_len_int
        
        # Initialize delay line (circular buffer)
        delay_line = np.zeros(delay_len_int + 1)  # +1 for fractional delay
        
        # Initialize output
        output_length = int(duration * self.sample_rate)
        output = np.zeros(output_length)
        
        # Initialize excitation (impulse with velocity)
        excitation = np.zeros(delay_len_int + 1)
        excitation[0] = velocity  # Pluck at position 0
        
        # Simple lowpass filter for pluck position
        # In practice, this would be more sophisticated
        pluck_position = 0.3  # Pluck at 30% of string length
        pluck_pos_samples = int(pluck_position * delay_len)
        if pluck_pos_samples < len(excitation):
            excitation[pluck_pos_samples] = velocity * 0.5  # Secondary excitation
        
        # Feedback filter (simple lowpass)
        feedback_coeff = 0.5  # Lowpass filter coefficient
        
        # Main synthesis loop
        for n in range(output_length):
            # Read from delay line
            output[n] = delay_line[0]
            
            # Apply excitation
            delay_line[0] += excitation[0] if n < len(excitation) else 0
            
            # Apply damping and feedback
            sample_out = delay_line[0]
            dampened = sample_out * (1.0 - self.damping)
            filtered = feedback_coeff * dampened + (1.0 - feedback_coeff) * delay_line[1]
            
            # Shift delay line
            delay_line[:-1] = delay_line[1:]
            delay_line[-1] = filtered
            
            # Shift excitation
            if n < len(excitation) - 1:
                excitation[:-1] = excitation[1:]
                excitation[-1] = 0.0
        
        return output

# Dataset generator
class SyntheticAudioDatasetGenerator:
    def __init__(self, 
                 output_dir: str,
                 sample_rate: int = 48000,
                 duration_range: Tuple[float, float] = (1.0, 3.0),
                 velocity_range: Tuple[float, float] = (0.1, 1.0)):
        self.output_dir = output_dir
        self.sample_rate = sample_rate
        self.duration_range = duration_range
        self.velocity_range = velocity_range
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "audio"), exist_ok=True)
        
        # Initialize synthesizers
        self.synthesizers = {
            "string": StringSynthesizer(sample_rate=sample_rate),
            # Add more synthesizers as needed (drum, wind, etc.)
        }
        
        # Dataset metadata
        self.metadata = {
            "samples": [],
            "dataset_info": {
                "sample_rate": sample_rate,
                "duration_range": duration_range,
                "velocity_range": velocity_range,
                "generation_date": str(np.datetime64('now')),
                "total_samples": 0
            }
        }
    
    def generate_string_note(self, 
                           midi_note: int,
                           velocity: Optional[float] = None,
                           duration: Optional[float] = None) -> np.ndarray:
        """Generate a single string note"""
        if velocity is None:
            velocity = random.uniform(*self.velocity_range)
        if duration is None:
            duration = random.uniform(*self.duration_range)
        
        audio = self.synthesizers["string"].pluck(
            midi_note=midi_note,
            velocity=velocity,
            duration=duration
        )
        return audio
    
    def generate_dataset(self, 
                        num_samples: int,
                        instrument: str = "string",
                        note_range: Tuple[int, int] = (40, 80),  # MIDI note range
                        filename_prefix: str = "synthetic") -> None:
        """Generate a dataset of synthetic audio"""
        print(f"Generating {num_samples} synthetic {instrument} samples...")
        
        for i in range(num_samples):
            # Randomly select parameters
            midi_note = random.randint(*note_range)
            velocity = random.uniform(*self.velocity_range)
            duration = random.uniform(*self.duration_range)
            
            # Generate audio
            if instrument == "string":
                audio = self.generate_string_note(midi_note, velocity, duration)
            else:
                raise ValueError(f"Instrument {instrument} not supported")
            
            # Normalize to prevent clipping
            if np.max(np.abs(audio)) > 0:
                audio = audio / np.max(np.abs(audio)) * 0.95  # Leave some headroom
            
            # Save audio file
            filename = f"{filename_prefix}_{i:06d}.wav"
            filepath = os.path.join(self.output_dir, "audio", filename)
            scipy.io.wavfile.write(filepath, self.sample_rate, audio.astype(np.float32))
            
            # Record metadata
            sample_info = {
                "filename": filename,
                "filepath": filepath,
                "midi_note": midi_note,
                "velocity": float(velocity),
                "duration": float(duration),
                "instrument": instrument,
                "sample_rate": self.sample_rate,
                "length_samples": len(audio),
                "length_seconds": len(audio) / self.sample_rate
            }
            self.metadata["samples"].append(sample_info)
            
            # Progress update
            if (i + 1) % 1000 == 0:
                print(f"Generated {i+1}/{num_samples} samples")
        
        # Update dataset info
        self.metadata["dataset_info"]["total_samples"] = num_samples
        
        # Save metadata
        metadata_path = os.path.join(self.output_dir, "dataset_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(self.metadata, f, indent=2)
        
        print(f"Dataset generation complete. Saved to {self.output_dir}")
    
    def validate_dataset(self) -> Dict[str, float]:
        """Validate generated dataset for quality issues"""
        print("Validating dataset...")
        issues = {
            "clipping": 0,
            "dc_offset": 0.0,
            "silent": 0,
            "too_short": 0,
            "too_long": 0
        }
        
        for sample in self.metadata["samples"]:
            filepath = sample["filepath"]
            audio, sr = scipy.io.wavfile.read(filepath)
            
            # Convert to float if needed
            if audio.dtype == np.int16:
                audio = audio.astype(np.float32) / 32768.0
            elif audio.dtype == np.int32:
                audio = audio.astype(np.float32) / 2147483648.0
            
            # Check for clipping
            if np.max(np.abs(audio)) >= 0.99:
                issues["clipping"] += 1
            
            # Check for DC offset
            dc_offset = np.mean(np.abs(audio))
            issues["dc_offset"] += dc_offset
            
            # Check for silent audio
            if np.max(np.abs(audio)) < 1e-4:
                issues["silent"] += 1
            
            # Check duration
            duration = sample["length_seconds"]
            if duration < self.duration_range[0] * 0.8:
                issues["too_short"] += 1
            if duration > self.duration_range[1] * 1.2:
                issues["too_long"] += 1
        
        # Average DC offset
        if self.metadata["samples"]:
            issues["dc_offset"] /= len(self.metadata["samples"])
        
        print("Validation complete.")
        for key, value in issues.items():
            print(f"  {key}: {value}")
        
        return issues

# Example usage
def generate_string_dataset():
    """Generate a dataset of synthetic string notes"""
    generator = SyntheticAudioDatasetGenerator(
        output_dir="./synthetic_string_dataset",
        sample_rate=48000,
        duration_range=(0.5, 3.0),
        velocity_range=(0.2, 1.0)
    )
    
    # Generate 5000 samples covering guitar range (E2 to E6 ~ MIDI 40 to 88)
    generator.generate_dataset(
        num_samples=5000,
        instrument="string",
        note_range=(40, 88),
        filename_prefix="guitar"
    )
    
    # Validate the dataset
    issues = generator.validate_dataset()
    
    # Print summary
    print(f"Generated {generator.metadata['dataset_info']['total_samples']} samples")
    print(f"Clipping: {issues['clipping']} samples")
    print(f"Average DC offset: {issues['dc_offset']:.6f}")
    
    return generator

# More advanced physical models can be added:
# - Drum synthesizers (using nonlinear elements)
# - Wind instrument models (using digital waveguides)
# - Vocal tract models (using source-filter theory)
# - FM synthesizers
# - Granular synthesizers

## EDGE CASES & FALLBACKS
- **Insufficient Variability**: Increase parameter ranges or add more synthesis techniques
- **Copyright Concerns**: Verify synthetic nature through audio analysis and documentation
- **Generation Speed**: Use GPU acceleration, batch processing, or simplify models
- **Audio Quality Issues**: Implement post-processing filters or use higher quality models
- **Metadata Mismatch**: Validate metadata against audio files regularly
- **Disk Space Limitations**: Implement on-the-fly generation or compression
- **Sample Rate Conversion**: Resample audio to match target rate if needed
- **Clipping Prevention**: Use automatic gain control or limiting during generation
- **DC Offset**: Remove DC offset during post-processing or generation
- **Silent Samples**: Detect and regenerate silent samples

## INTEGRATION POINTS
- Audio Processing: Librosa, Torchaudio, SciPy, SoundFile
- Physical Modeling: Synthesis ToolKit (STK), Faust, Modalysis
- Machine Learning: TensorFlow, PyTorch, scikit-learn
- Dataset Management: Hugging Face Datasets, TensorFlow Datasets, PyTorch DataLoader
- Quality Assessment: PESQ, STOI, POLQA, MATLAB Audio Toolbox
- Storage Formats: WAV, FLAC, MP3, OGG
- Cloud Storage: AWS S3, Google Cloud Storage, Azure Blob Storage
- Version Control: DVC (Data Version Control) for large datasets
- Documentation: README, dataset cards, data sheets
- Deployment: Data loaders for training pipelines, preprocessing scripts

## EXECUTION EXAMPLES

**Input:** "Generate a dataset of 10,000 synthetic piano notes for onset detection training"
**Output:**
```python
# Piano synthesizer would need to be implemented (more complex than string)
# For demonstration, we'll use the string synthesizer as a placeholder
# In practice, implement or use a piano physical model

generator = SyntheticAudioDatasetGenerator(
    output_dir="./synthetic_piano_dataset",
    sample_rate=44100,
    duration_range=(0.3, 4.0),
    velocity_range=(0.1, 1.0)
)

# Generate piano-like notes (using string synthesizer as placeholder)
generator.generate_dataset(
    num_samples=10000,
    instrument="string",  # Replace with "piano" when implemented
    note_range=(21, 108),  # Full piano range (A0 to C8)
    filename_prefix="piano"
)

# Validate
issues = generator.validate_dataset()
```

**Input:** "Create a synthetic drum dataset for beat tracking"
**Output:**
```python
# Would implement a drum synthesizer (e.g., based on TR-808, acoustic drum models)
# For demonstration, showing structure

drum_generator = SyntheticAudioDatasetGenerator(
    output_dir="./synthetic_drum_dataset",
    sample_rate=48000,
    duration_range=(0.1, 2.0),  # Short drum hits
    velocity_range=(0.3, 1.0)
)

# Generate kick, snare, hi-hat, etc.
# In practice, would have different synthesizers for each drum type
# Or use a multi-timbral synthesizer with different parameters

# Example for kick drum
drum_generator.generate_dataset(
    num_samples=2000,
    instrument="kick",  # Would need kick synthesizer
    note_range=(36, 36),  # Fixed MIDI note for kick
    filename_prefix="kick"
)

# Similar for snare, hi-hat, etc.
# Then combine into a single dataset or keep separate
```