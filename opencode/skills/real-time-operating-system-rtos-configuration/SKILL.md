---
name: real-time-operating-system-rtos-configuration
description: >-
  Use this skill when the user is working on or asking about RTOS, FreeRTOS, Zephyr, real-time OS for audio, task scheduling for embedded audio, or configuring an RTOS for DSP.
version: 1.0.0
---

# SKILL: Real-Time Operating System (RTOS) Configuration

## CAPABILITIES
- Configure RTOS kernels (FreeRTOS, Zephyr, ThreadX) for deterministic audio processing
- Implement priority-based preemptive scheduling for audio tasks
- Manage inter-task communication (queues, semaphores, mutexes) for audio data flow
- Optimize memory usage and stack allocation for real-time constraints
- Implement tickless idle mode for power efficiency in battery-operated devices

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| Audio processing requirements (latency, jitter, throughput) | RTOS configuration parameters |
| Task specifications (periodicity, execution time, deadlines) | Task creation and scheduling parameters |
| Resource requirements (memory, peripherals, shared data) | Memory allocation and synchronization primitives |
| Hardware specifications (CPU, clock speed, memory) | Port layer and hardware-specific configuration |
| Power constraints (battery life, sleep modes) | Power management configuration |

## IMPLEMENTATION PATTERN

```c
// FreeRTOS-based Audio Processing System
#include <FreeRTOS.h>
#include <task.h>
#include <queue.h>
#include <semphr.h>
#include <timers.h>

// Audio buffer definitions
#define AUDIO_BUFFER_SIZE  128
#define NUM_AUDIO_BUFFERS  4
#define SAMPLE_RATE        48000
#define AUDIO_TASK_PRIORITY (configMAX_PRIORITIES - 1) // Highest priority

// Audio buffer structure
typedef struct {
    int16_t samples[AUDIO_BUFFER_SIZE * 2]; // Stereo 16-bit
    uint32_t timestamp;
    uint8_t  bufferId;
} AudioBuffer_t;

// RTOS objects
static QueueHandle_t audioInputQueue  = NULL;
static QueueHandle_t audioOutputQueue = NULL;
static SemaphoreHandle_t audioProcessSemaphore = NULL;
static TaskHandle_t audioInputTaskHandle  = NULL;
static TaskHandle_t audioProcessTaskHandle = NULL;
static TaskHandle_t audioOutputTaskHandle = NULL;

// Audio processing state (shared between tasks)
typedef struct {
    float32_t gainLeft  = 1.0f;
    float32_t gainRight = 1.0f;
    float32_t smoothedGainLeft  = 1.0f;
    float32_t smoothedGainRight = 1.0f;
    // Add your DSP state here
} AudioProcessorState_t;

static AudioProcessorState_t gAudioState;

// Forward declarations
void audioInputTask(void *pvParameters);
void audioProcessTask(void *pvParameters);
void audioOutputTask(void *pvParameters);
void audioTimerCallback(TimerHandle_t xTimer);

// Hardware initialization functions (platform-specific)
extern void audioHardwareInit(void);
extern void audioStartDMA(void);
extern void audioStopDMA(void);
extern bool audioReadBuffer(AudioBuffer_t* buffer);
extern bool audioWriteBuffer(const AudioBuffer_t* buffer);

void setup_audio_rtos(void) {
    // Create RTOS objects
    audioInputQueue  = xQueueCreate(NUM_AUDIO_BUFFERS, sizeof(AudioBuffer_t));
    audioOutputQueue = xQueueCreate(NUM_AUDIO_BUFFERS, sizeof(AudioBuffer_t));
    audioProcessSemaphore = xSemaphoreCreateBinary();
    
    // Create audio tasks
    xTaskCreate(audioInputTask,  "AudioIn",  configMINIMAL_STACK_SIZE * 4, NULL, AUDIO_TASK_PRIORITY, &audioInputTaskHandle);
    xTaskCreate(audioProcessTask, "AudioProc", configMINIMAL_STACK_SIZE * 4, NULL, AUDIO_TASK_PRIORITY, &audioProcessTaskHandle);
    xTaskCreate(audioOutputTask, "AudioOut", configMINIMAL_STACK_SIZE * 4, NULL, AUDIO_TASK_PRIORITY, &audioOutputTaskHandle);
    
    // Create timer for periodic parameter updates (optional)
    // TimerHandle_t paramTimer = xTimerCreate("ParamUpdate", pdMS_TO_TICKS(10), pdTRUE, NULL, audioTimerCallback);
    // xTimerStart(paramTimer, 0);
    
    // Initialize hardware
    audioHardwareInit();
    
    // Start audio DMA/processing
    audioStartDMA();
    
    // Start scheduler
    vTaskStartScheduler();
}

// Audio input task - reads from hardware
void audioInputTask(void *pvParameters) {
    AudioBuffer_t buffer;
    BaseType_t qStatus;
    
    for (;;) {
        // Read audio buffer from hardware (blocking with timeout)
        if (audioReadBuffer(&buffer)) {
            // Send to processing queue
            qStatus = xQueueSendToBack(audioInputQueue, &buffer, pdMS_TO_TICKS(1));
            if (qStatus != pdPASS) {
                // Handle queue full - drop buffer or implement overflow strategy
            }
        }
        
        // Yield to allow other tasks to run
        taskYIELD();
    }
}

// Audio processing task - performs DSP
void audioProcessTask(void *pvParameters) {
    AudioBuffer_t inBuffer, outBuffer;
    BaseType_t qStatus;
    TickType_t wakeTime = xTaskGetTickCount();
    
    for (;;) {
        // Wait for input buffer or timeout
        qStatus = xQueueReceive(audioInputQueue, &inBuffer, pdMS_TO_TICKS(10));
        
        if (qStatus == pdPASS) {
            // Process audio buffer
            processAudioBuffer(&inBuffer, &outBuffer);
            
            // Send to output queue
            qStatus = xQueueSendToBack(audioOutputQueue, &outBuffer, pdMS_TO_TICKS(1));
            if (qStatus != pdPASS) {
                // Handle queue full
            }
            
            // Signal that processing is done (optional)
            xSemaphoreGive(audioProcessSemaphore);
        }
        
        // Periodic execution - maintain timing
        vTaskDelayUntil(&wakeTime, pdMS_TO_TICKS(1));
    }
}

// Audio output task - writes to hardware
void audioOutputTask(void *pvParameters) {
    AudioBuffer_t buffer;
    BaseType_t qStatus;
    
    for (;;) {
        // Get buffer from processing queue
        qStatus = xQueueReceive(audioOutputQueue, &buffer, portMAX_DELAY);
        
        if (qStatus == pdPASS) {
            // Write to hardware
            if (!audioWriteBuffer(&buffer)) {
                // Handle write error
            }
            
            // Buffer is now free to be reused (implementation dependent)
        }
    }
}

// Audio processing function (your DSP code)
void processAudioBuffer(const AudioBuffer_t* input, AudioBuffer_t* output) {
    // Copy timestamp and buffer ID
    output->timestamp = input->timestamp;
    output->bufferId  = input->bufferId;
    
    // Process audio samples (stereo 16-bit)
    const int16_t* inSamples  = input->samples;
    int16_t* outSamples = output->samples;
    const uint32_t numSamples = AUDIO_BUFFER_SIZE * 2; // Stereo
    
    // Apply smoothed gain changes to avoid zipper noise
    gAudioState.smoothedGainLeft  = gAudioState.smoothedGainLeft  * 0.9f  + gAudioState.gainLeft  * 0.1f;
    gAudioState.smoothedGainRight = gAudioState.smoothedGainRight * 0.9f  + gAudioState.gainRight * 0.1f;
    
    // Apply gain to each sample
    for (uint32_t i = 0; i < numSamples; i += 2) {
        // Left channel
        int32_t leftSample  = ((int32_t)inSamples[i]) * gAudioState.smoothedGainLeft;
        outSamples[i] = (int16_t)clamp(leftSample, -32768, 32767);
        
        // Right channel
        int32_t rightSample = ((int32_t)inSamples[i+1]) * gAudioState.smoothedGainRight;
        outSamples[i+1] = (int16_t)clamp(rightSample, -32768, 32767);
    }
}

// Helper function for clamping
static inline int32_t clamp(int32_t value, int32_t min, int32_t max) {
    if (value < min) return min;
    if (value > max) return max;
    return value;
}

// Timer callback for periodic updates (optional)
void audioTimerCallback(TimerHandle_t xTimer) {
    // Example: Update parameters from potentiometers or other slow-changing sources
    // This runs in timer task context - keep it short!
    // BaseType_t higherPriorityTaskWoken = pdFALSE;
    // vTaskNotifyGiveFromISR(audioProcessTaskHandle, &higherPriorityTaskWoken);
    // portYIELD_FROM_ISR(higherPriorityTaskWoken);
}

// Optional: Task for handling control inputs (potentiometers, buttons, etc.)
void controlTask(void *pvParameters) {
    for (;;) {
        // Read controls (e.g., potentiometers via ADC)
        // Update gAudioState.gainLeft/Right based on input
        
        // Delay to avoid consuming too much CPU
        vTaskDelay(pdMS_TO_TICKS(10)); // 10ms update rate for controls
    }
}
```

## EDGE CASES & FALLBACKS
- **Priority Inversion**: Use priority inheritance mutexes for shared resources
- **Stack Overflow**: Enable stack checking (configCHECK_FOR_STACK_OVERFLOW) and monitor stack usage
- **Queue Overflows**: Implement buffer pooling or drop-oldest strategy for audio buffers
- **Interrupt Latency**: Keep ISRs extremely short; defer processing to tasks
- **Memory Fragmentation**: Use static allocation where possible; consider memory pools
- **Tickless Mode Issues**: Ensure timeout values are compatible with tickless idle
- **Compiler Optimization**: Use volatile for shared variables and memory barriers where needed
- **Hardware DMA Conflicts**: Ensure proper cache maintenance when using DMA with buffers
- **Scheduler Locking**: Minimize critical sections; use shortest possible disabling of interrupts

## INTEGRATION POINTS
- RTOS Kernels: FreeRTOS, Zephyr, ThreadX, Micrium µC/OS-III, RTX
- Development Platforms: STM32, ESP32, nRF52, Teensy, Raspberry Pi Pico
- Audio Hardware: I2S, SAI, SPI, USB Audio, Parallel Audio Interfaces
- Debugging: SEGGER SystemView, Tracealyzer, RTOS-aware debugging in IDEs
- Performance Analysis: CPU utilization monitoring, stack watermarking, trace recording
- Power Management: Tickless idle, low-power modes, dynamic voltage frequency scaling
- File Systems: LittleFS, FATFS for audio logging and preset storage
- Networking: lwIP, ESP-NOW for wireless audio transmission
- USB: Device and host stacks for MIDI, audio, and control interfaces
- Build Systems: CMake with FreeRTOS, STM32CubeIDE, PlatformIO, Arduino core with FreeRTOS

## EXECUTION EXAMPLES

**Input:** "Configure FreeRTOS for double-buffered audio I/O with 1ms processing deadline"
**Output:**
```c
// Double-buffered audio I/O configuration
#define AUDIO_BUFFER_SIZE    256
#define NUM_AUDIO_BUFFERS    2  // Double buffering
#define AUDIO_PROCESS_DEADLINE_MS 1

// In setup_audio_rtos():
// Create queues with appropriate depth
audioInputQueue  = xQueueCreate(NUM_AUDIO_BUFFERS, sizeof(AudioBuffer_t*));
audioOutputQueue = xQueueCreate(NUM_AUDIO_BUFFERS, sizeof(AudioBuffer_t*));

// Modify tasks to use buffer pointers instead of copying
void audioInputTask(void *pvParameters) {
    AudioBuffer_t* buffer;
    for (;;) {
        buffer = getNextInputBuffer(); // Hardware-specific function
        if (buffer != NULL) {
            xQueueSendToBack(audioInputQueue, &buffer, pdMS_TO_TICKS(0));
        }
        vTaskDelayUntil(&lastWakeTime, pdMS_TO_TICKS(1));
    }
}

// Audio processing task with deadline monitoring
void audioProcessTask(void *pvParameters) {
    AudioBuffer_t* inBuffer  = NULL;
    AudioBuffer_t* outBuffer = NULL;
    TickType_t startTime, endTime;
    uint32_t deadlineMisses = 0;
    
    for (;;) {
        // Wait for input buffer
        if (xQueueReceive(audioInputQueue, &inBuffer, pdMS_TO_TICKS(10)) == pdPASS) {
            // Get output buffer
            outBuffer = getOutputBuffer(); // Hardware-specific
            
            startTime = xTaskGetTickCount();
            processAudioBuffer(inBuffer, outBuffer);
            endTime = xTaskGetTickCount();
            
            // Check deadline
            if ((endTime - startTime) > pdMS_TO_TICKS(AUDIO_PROCESS_DEADLINE_MS)) {
                deadlineMisses++;
                // Handle deadline miss (e.g., reduce quality, notify user)
            }
            
            // Send output buffer
            xQueueSendToBack(audioOutputQueue, &outBuffer, pdMS_TO_TICKS(0));
            
            // Release input buffer
            releaseInputBuffer(inBuffer);
        }
    }
}
```

**Input:** "Implement interrupt-driven audio I/O with RTOS task processing"
**Output:**
```c
// Interrupt-driven audio with RTOS processing
#define AUDIO_BUFFER_SIZE  64
#define NUM_AUDIO_BUFFERS  4

// Audio buffer ring buffer
static AudioBuffer_t audioBuffers[NUM_AUDIO_BUFFERS];
static volatile uint32_t writeIndex = 0;
static volatile uint32_t readIndex  = 0;
static SemaphoreHandle_t bufferAvailableSemaphore = NULL;

// ISR for audio interrupt (platform-specific)
void AUDIO_IRQHandler(void) {
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    
    // Get buffer from hardware
    AudioBuffer_t* buffer = &audioBuffers[writeIndex];
    if (hardwareReadAudioBuffer(buffer)) {
        // Advance write index
        writeIndex = (writeIndex + 1) % NUM_AUDIO_BUFFERS;
        
        // Signal that buffer is available
        xSemaphoreGiveFromISR(bufferAvailableSemaphore, &xHigherPriorityTaskWoken);
        
        // Check for buffer overflow
        if (((writeIndex + 1) % NUM_AUDIO_BUFFERS) == readIndex) {
            // Handle overflow - drop oldest buffer or set error flag
        }
    }
    
    // Context switch if needed
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}

// Audio processing task
void audioProcessTask(void *pvParameters) {
    AudioBuffer_t buffer;
    
    for (;;) {
        // Wait for buffer with timeout
        if (xSemaphoreTake(bufferAvailableSemaphore, pdMS_TO_TICKS(5)) == pdPASS) {
            // Read buffer (with protection against concurrent access)
            uint32_t currentReadIndex = readIndex;
            buffer = audioBuffers[currentReadIndex];
            readIndex = (currentReadIndex + 1) % NUM_AUDIO_BUFFERS;
            
            // Process buffer
            processAudioBuffer(&buffer, &buffer); // In-place processing
            
            // Write buffer back to hardware
            hardwareWriteAudioBuffer(&buffer);
        }
    }
}

// Setup function
void setup_audio_rtos(void) {
    // Create semaphore for buffer signaling
    bufferAvailableSemaphore = xSemaphoreCreateBinary();
    
    // Create processing task
    xTaskCreate(audioProcessTask, "AudioProc", 
                configMINIMAL_STACK_SIZE * 4, NULL, 
                configMAX_PRIORITIES - 1, NULL);
    
    // Initialize hardware and enable interrupts
    audioHardwareInit();
    hardwareEnableAudioInterrupt();
    
    // Start scheduler
    vTaskStartScheduler();
}
```