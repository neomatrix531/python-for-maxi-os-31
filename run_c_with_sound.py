import subprocess
import os
import sys
import time

# Write user's C code to a temp file
user_code = r"""
#include <stdio.h>
#include <math.h>
#include <stdint.h>

#define SAMPLERATE 44100
#define DURATION 2
#define FREQ 440

int main() {
    FILE *f = fopen("output.wav", "wb");
    if (!f) return 1;

    // WAV header
    int datasize = SAMPLERATE * DURATION * 2;
    fwrite("RIFF", 1, 4, f);
    int filesize = 36 + datasize;
    fwrite(&filesize, 4, 1, f);
    fwrite("WAVEfmt ", 1, 8, f);
    int fmt_chunk_size = 16;
    fwrite(&fmt_chunk_size, 4, 1, f);
    short audio_format = 1, num_channels = 1;
    int sample_rate = SAMPLERATE, byte_rate = SAMPLERATE * 2;
    short block_align = 2, bits_per_sample = 16;
    fwrite(&audio_format, 2, 1, f);
    fwrite(&num_channels, 2, 1, f);
    fwrite(&sample_rate, 4, 1, f);
    fwrite(&byte_rate, 4, 1, f);
    fwrite(&block_align, 2, 1, f);
    fwrite(&bits_per_sample, 2, 1, f);
    fwrite("data", 1, 4, f);
    fwrite(&datasize, 4, 1, f);

    // Sine wave
    for (int i = 0; i < SAMPLERATE * DURATION; ++i) {
        double t = (double)i / SAMPLERATE;
        int16_t sample = (int16_t)(sin(2 * M_PI * FREQ * t) * 32767);
        fwrite(&sample, 2, 1, f);
    }

    fclose(f);
    return 0;
}
"""

with open('user_code.c', 'w') as f:
    f.write(user_code)

# Compile the C code
compile_result = subprocess.run(['gcc', 'user_code.c', '-o', 'user_prog', '-lm'])

if compile_result.returncode != 0:
    print("Compilation failed.")
    sys.exit(1)

# Run the compiled binary (generates output.wav)
run_result = subprocess.run(['./user_prog'])

if run_result.returncode != 0:
    print("Program execution failed.")
    sys.exit(1)

# Play the generated wav file (uses 'aplay' for Linux, 'afplay' for Mac)
if sys.platform.startswith('linux'):
    subprocess.run(['aplay', 'output.wav'])
elif sys.platform == 'darwin':
    subprocess.run(['afplay', 'output.wav'])
else:
    print("Please play output.wav manually.")

# Cleanup
os.remove('user_code.c')
os.remove('user_prog')
os.remove('output.wav')
