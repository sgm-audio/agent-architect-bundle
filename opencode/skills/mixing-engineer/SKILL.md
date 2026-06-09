---
name: mixing-engineer
description: Professional audio mixing techniques including balance, EQ, compression, spatialization, effects, and automation. Use when mixing multi-track recordings, achieving professional balance, creating spatial depth, or preparing tracks for mastering.
license: MIT
allowed-tools:
  - read
  - write
  - bash
metadata:
  category: audio-production
  subcategory: mixing
  difficulty: advanced
  tools: eq, compression, reverb, delay, automation
---

# Mixing Engineer Agent

## Mixing Fundamentals

### The Mixing Philosophy

- **Balance**: Achieve proper instrument levels
- **Clarity**: Ensure each element is audible
- **Depth**: Create three-dimensional space
- **Dynamics**: Preserve musical expression
- **Emotion**: Support the song's emotional intent

### Critical Listening

- **Frequency awareness**: Identify problematic frequencies
- **Dynamic perception**: Recognize dynamic issues
- **Spatial awareness**: Understand stereo field
- **Emotional response**: Evaluate emotional impact
- **Technical accuracy**: Verify technical standards

## Signal Flow

### Input Chain

1. **Source**: Original recording
2. **Preamp**: Initial gain staging
3. **Converter**: Analog-to-digital conversion
4. **Interface**: Audio interface
5. **DAW**: Digital Audio Workstation

### Mixing Chain

1. **Gain Staging**: Proper level setup
2. **EQ**: Frequency balance
3. **Compression**: Dynamic control
4. **Saturation**: Harmonic enhancement
5. **Spatial Effects**: Reverb and delay
6. **Automation**: Dynamic changes
7. **Bus Processing**: Group processing
8. **Master Bus**: Final processing

## Balance and Levels

### Volume Relationships

- **Lead elements**: Vocals, main instruments (0 to -6dB)
- **Supporting elements**: Rhythm section, harmonies (-6 to -12dB)
- **Background elements**: Pads, textures (-12 to -18dB)
- **Effects**: Reverb, delay (-18 to -24dB)

### Genre-Specific Balance

- **Pop**: Vocal-centric, tight rhythm section
- **Rock**: Guitar-forward, powerful drums
- **Electronic**: Bass-heavy, synthetic elements
- **Jazz**: Natural dynamics, acoustic balance
- **Classical**: Natural perspective, dynamic range

### Level Setting Techniques

- **Start with faders**: Rough balance before processing
- **Reference tracks**: Compare with professional mixes
- **Mono compatibility**: Check balance in mono
- **Headroom**: Leave space for mastering (-6dBFS max)
- **Consistency**: Maintain consistent levels

## Equalization (EQ)

### EQ Principles

- **Cut before boost**: Remove problems before adding presence
- **Bandwidth control**: Use appropriate Q values
- **Frequency selection**: Target specific problem areas
- **Dynamic EQ**: Frequency-specific dynamic control
- **Linear phase**: Transparent EQ when needed

### Frequency Ranges

- **Sub-bass (20-60Hz)**: Power and weight
- **Bass (60-250Hz)**: Warmth and fullness
- **Low-mids (250-500Hz)**: Body and thickness
- **Mids (500Hz-2kHz)**: Presence and clarity
- **High-mids (2-5kHz)**: Attack and definition
- **Presence (5-10kHz)**: Air and brightness
- **Air (10-20kHz)**: Sparkle and brilliance

### EQ Techniques

- **High-pass filtering**: Remove low-end rumble
- **Low-cut filters**: Clean up muddy frequencies
- **Notch filtering**: Remove resonant frequencies
- **Shelving EQ**: Broad frequency adjustments
- **Bell EQ**: Precise frequency control

### Instrument-Specific EQ

- **Vocals**: Clarity (2-5kHz), air (10-15kHz), body (200-500Hz)
- **Kick drum**: Attack (3-5kHz), body (60-100Hz), click (2-4kHz)
- **Snare**: Crack (1-3kHz), body (150-250Hz), snap (5-8kHz)
- **Bass**: Definition (800Hz-1.5kHz), warmth (80-120Hz)
- **Guitars**: Body (200-400Hz), clarity (2-4kHz), air (10kHz+)

## Compression

### Compression Basics

- **Ratio**: Amount of compression (1.5:1 to 10:1)
- **Threshold**: Level where compression begins
- **Attack**: How quickly compression engages
- **Release**: How quickly compression releases
- **Makeup gain**: Compensation for volume reduction

### Compression Types

- **Vocal compression**: Smooth, consistent level control
- **Drum bus compression**: Glue and punch
- **Parallel compression**: Blend compressed and uncompressed
- **Multiband compression**: Frequency-specific control
- **Sidechain compression**: Dynamic ducking effects

### Compression Settings

- **Vocals**: Ratio 2:1 to 4:1, attack 10-30ms, release 100-300ms
- **Drums**: Ratio 4:1 to 8:1, attack 1-10ms, release 50-150ms
- **Bass**: Ratio 2:1 to 4:1, attack 10-30ms, release 100-300ms
- **Guitars**: Ratio 2:1 to 4:1, attack 10-50ms, release 100-300ms
- **Mix bus**: Ratio 1.5:1 to 2:1, attack 10-30ms, release 100-300ms

## Spatial Processing

### Panning Techniques

- **Center**: Kick, snare, bass, lead vocal
- **Left/Right**: Rhythm guitars, keyboards, backing vocals
- **Wide**: Hi-hats, overheads, effects
- **Automation**: Dynamic panning movement

### Reverb Types

- **Room reverb**: Small space, natural ambience
- **Hall reverb**: Large space, orchestral feel
- **Plate reverb**: Smooth, dense reverb
- **Spring reverb**: Bouncy, vintage character
- **Convolution reverb**: Realistic acoustic spaces

### Delay Techniques

- **Slap delay**: Short, subtle doubling
- **Ping-pong delay**: Stereo movement
- **Tempo-synced delay**: Musical timing
- **Filtered delay**: Frequency-specific repeats
- **Modulated delay**: Chorus-like effects

### Spatial Enhancement

- **Stereo widening**: Expand stereo field
- **Mid/side processing**: Separate mid and side components
- **Haas effect**: Precedence effect for width
- **Phase manipulation**: Stereo image control
- **Depth processing**: Front-to-back positioning

## Effects Processing

### Creative Effects

- **Modulation**: Chorus, flanger, phaser
- **Distortion**: Overdrive, saturation, fuzz
- **Pitch shifting**: Harmonization, octaver
- **Frequency shifting**: Radical frequency changes
- **Granular effects**: Microscopic sound manipulation

### Dynamic Effects

- **Gates**: Noise reduction, rhythmic effects
- **Expanders**: Gentle dynamic expansion
- **Transient shapers**: Attack and sustain control
- **De-essers**: Sibilant reduction
- **Limiters**: Peak control

### Creative Processing

- **Reverse effects**: Backwards sounds
- **Pitch modulation**: Vibrato and warble
- **Formant shifting**: Vocal character changes
- **Spectral processing**: Frequency domain manipulation
- **Granular synthesis**: Grain-based effects

## Automation

### Automation Types

- **Volume automation**: Dynamic level changes
- **Pan automation**: Stereo movement
- **Send automation**: Effect level changes
- **Parameter automation**: Plugin parameter changes
- **Mute automation**: Selective muting

### Automation Techniques

- **Ride automation**: Manual level adjustments
- **Snapshot automation**: Scene changes
- **LFO automation**: Rhythmic parameter changes
- **Envelope automation**: ADSR-like changes
- **Random automation**: Creative variations

### Automation Strategies

- **Build automation**: Gradual increases
- **Break automation**: Sudden changes
- **Emphasis automation**: Highlight important moments
- **Movement automation**: Create dynamic interest
- **Transition automation**: Smooth between sections

## Bus Processing

### Bussing Techniques

- **Drum bus**: Group drum processing
- **Vocal bus**: Group vocal processing
- **Instrument bus**: Group instrument processing
- **Effect bus**: Group effect processing
- **Mix bus**: Final mix processing

### Bus Processing

- **Compression**: Glue and cohesion
- **EQ**: Tonal balance
- **Saturation**: Harmonic enhancement
- **Stereo processing**: Width and depth
- **Limiting**: Peak control

### Parallel Processing

- **Parallel compression**: Blend compressed and uncompressed
- **Parallel EQ**: Blend processed and unprocessed
- **Parallel saturation**: Blend clean and saturated
- **Parallel effects**: Blend dry and wet signals
- **Parallel distortion**: Blend clean and distorted

## Mixing for Different Genres

### Pop Mixing

- **Vocal prominence**: Clear, upfront vocals
- **Tight rhythm**: Precise timing and groove
- **Polished sound**: Professional, commercial quality
- **Wide stereo**: Expansive stereo field
- **Competitive loudness**: Loud, impactful mix

### Rock Mixing

- **Guitar power**: Strong guitar presence
- **Drum punch**: Powerful, impactful drums
- **Natural dynamics**: Preserve musical expression
- **Analog warmth**: Vintage character
- **Live feel**: Natural, organic sound

### Electronic Mixing

- **Bass focus**: Strong, defined low-end
- **Synthetic clarity**: Clear synthetic elements
- **Creative effects**: Unique sound design
- **Stereo width**: Enhanced stereo field
- **Loudness**: High RMS levels

### Jazz Mixing

- **Natural dynamics**: Preserve musical expression
- **Acoustic balance**: Natural instrument balance
- **Room sound**: Natural ambience
- **Minimal processing**: Subtle enhancement
- **Dynamic range**: Preserve musical dynamics

### Classical Mixing

- **Natural perspective**: Realistic instrument placement
- **Minimal processing**: Transparent enhancement
- **Dynamic range**: Maximum preservation
- **Room acoustics**: Natural concert hall sound
- **Balance**: Natural orchestral balance

## Technical Considerations

### Phase and Polarity

- **Phase alignment**: Ensure proper phase relationships
- **Polarity inversion**: Fix phase cancellation
- **Correlation metering**: Monitor stereo phase
- **Mono compatibility**: Check in mono
- **Phase rotation**: Adjust phase relationships

### Frequency Management

- **Frequency masking**: Avoid frequency conflicts
- **Spectrum analysis**: Visual frequency monitoring
- **EQ carving**: Create space for each element
- **Dynamic EQ**: Frequency-specific dynamic control
- **Harmonic balance**: Maintain musical harmony

### Dynamic Range

- **Compression**: Control dynamic range
- **Limiting**: Peak control
- **Expansion**: Gentle dynamic enhancement
- **Transient shaping**: Attack and sustain control
- **Automation**: Dynamic level changes

## Mixing Workflow

### Preparation

- **Session organization**: Logical track layout
- **Gain staging**: Proper level setup
- **Color coding**: Visual organization
- **Track naming**: Clear identification
- **Template setup**: Consistent starting point

### Rough Mix

- **Fader balance**: Initial level relationships
- **Panning**: Basic stereo placement
- **Rough EQ**: Basic frequency adjustments
- **Basic compression**: Initial dynamic control
- **Reference listening**: Evaluate overall balance

### Detailed Mix

- **Individual processing**: Detailed track processing
- **Bus processing**: Group processing
- **Effects**: Spatial and creative effects
- **Automation**: Dynamic changes
- **Fine tuning**: Detailed adjustments

### Final Mix

- **Master bus processing**: Final processing
- **Quality control**: Technical and artistic checks
- **Reference comparison**: Professional reference tracks
- **Client review**: Feedback incorporation
- **Delivery**: Final mix delivery

## Quality Control

### Technical Checks

- **Level metering**: Verify proper levels
- **Frequency analysis**: Check frequency balance
- **Phase correlation**: Monitor stereo phase
- **Loudness metering**: Verify loudness standards
- **Bit depth**: Ensure proper bit depth

### Listening Environment

- **Studio monitors**: Flat frequency response
- **Reference headphones**: Consistent listening
- **Multiple systems**: Car, phone, laptop testing
- **A/B comparison**: Reference track comparison
- **Different volumes**: Check at various levels

### Quality Assurance

- **Mono compatibility**: Check in mono
- **Phase issues**: Identify phase problems
- **Frequency balance**: Verify tonal balance
- **Dynamic range**: Check dynamic preservation
- **Overall impact**: Evaluate emotional impact

## Advanced Techniques

### Mid/Side Processing

- **Mid processing**: Center channel enhancement
- **Side processing**: Stereo field enhancement
- **Width control**: Adjust stereo width
- **Balance**: Control mid/side balance
- **Imaging**: Enhance stereo depth

### Parallel Processing

- **Parallel compression**: Blend compressed and uncompressed
- **Parallel EQ**: Blend processed and unprocessed
- **Parallel saturation**: Blend clean and saturated
- **Parallel effects**: Blend dry and wet signals
- **Parallel distortion**: Blend clean and distorted

### Dynamic Processing

- **Multiband compression**: Frequency-specific control
- **Dynamic EQ**: Frequency-specific dynamic control
- **Transient shaping**: Attack and sustain control
- **De-essing**: Sibilant reduction
- **Limiting**: Peak control

## Mixing Tools

### Essential Plugins

- **EQ**: FabFilter Pro-Q, Waves SSL E-Channel
- **Compression**: Universal Audio 1176, Waves CLA-76
- **Reverb**: Valhalla Room, Lexicon PCM
- **Delay**: Soundtoys EchoBoy, Waves H-Delay
- **Saturation**: Softube Saturation Knob, Soundtoys Decapitator

### Analysis Tools

- **Spectrum analyzer**: Visual frequency analysis
- **Loudness meter**: LUFS and RMS metering
- **Phase correlation meter**: Stereo phase monitoring
- **Level meter**: Peak and RMS level monitoring
- **Frequency analyzer**: Detailed frequency analysis

## Best Practices

### Before Mixing

- **Quality source**: Start with good recordings
- **Organized session**: Logical track layout
- **Reference tracks**: Professional comparison material
- **Clear vision**: Understand the song's goals
- **Proper gain staging**: Start with correct levels

### During Mixing

- **Take breaks**: Fresh ears for critical listening
- **Reference regularly**: Compare with professional mixes
- **Less is more**: Subtle processing often works best
- **Context matters**: Consider the whole mix
- **Save versions**: Keep multiple iterations

### After Mixing

- **Quality control**: Technical and artistic checks
- **Client review**: Incorporate feedback
- **Documentation**: Record settings and decisions
- **Backup**: Secure final mixes
- **Delivery**: Proper file delivery

## Troubleshooting

### Issue: Mix Sounds Muddy

**Solution**: High-pass filtering, reduce low-mid content, carve space

### Issue: Mix Lacks Clarity

**Solution**: EQ adjustments, reduce masking, enhance presence

### Issue: Mix Sounds Narrow

**Solution**: Stereo widening, panning adjustments, spatial effects

### Issue: Mix Lacks Impact

**Solution**: Compression, transient shaping, level adjustments

### Issue: Mix Sounds Harsh

**Solution**: De-essing, EQ cuts, reduce high-frequency content

## Continuous Learning

### Skill Development

- **Study mixes**: Analyze professional mixes
- **Practice regularly**: Mix different genres
- **Get feedback**: Professional critiques
- **Experiment**: Try new techniques
- **Stay updated**: Learn new tools and methods

### Resources

- **Books**: Mixing engineering textbooks
- **Courses**: Professional mixing courses
- **Workshops**: Hands-on learning experiences
- **Forums**: Professional mixing communities
- **Mentorship**: Learn from experienced mixers

---

**Note**: This skill provides comprehensive mixing guidance and techniques. Mixing is both technical and artistic - develop your ears, understand the tools, and create mixes that serve the music.
