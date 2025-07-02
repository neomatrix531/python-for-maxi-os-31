import os
import turtle
import turtle
import random
import sys
import tempfile
import shutil
import subprocess


# Set up the window and turtle
screen = turtle.Screen()
screen.bgcolor("black")
t = turtle.Turtle()
t.speed(0)  # Fastest speed
t.width(2)
colors = ["red", "orange", "yellow", "green", "cyan", "blue", "magenta", "white"]

# Draw spirograph
for x in range(72):
    t.color(random.choice(colors))
    t.circle(100)
    t.left(5)
    t.penup()
    t.forward(5)
    t.pendown()

# Hide the turtle and display the window
t.hideturtle()
turtle.done()
print("Maxi OS 31.X")

def run_code(language, code):
    # Set up temp directory
    with tempfile.TemporaryDirectory() as tempdir:
        os.chdir(tempdir)
        if language == "c":
            src = "prog.c"
            exe = "./prog"
            with open(src, "w") as f:
                f.write(code)
            compile_cmd = ["gcc", src, "-o", "prog", "-lm"]
        elif language == "cpp":
            src = "prog.cpp"
            exe = "./prog"
            with open(src, "w") as f:
                f.write(code)
            compile_cmd = ["g++", src, "-o", "prog", "-lm"]
        elif language == "csharp":
            src = "prog.cs"
            exe = "prog.exe"
            with open(src, "w") as f:
                f.write(code)
            compile_cmd = ["mcs", src]
        else:
            print("Unsupported language:", language)
            return

        # Compile
        print("Compiling...")
        compile_proc = subprocess.run(compile_cmd, capture_output=True, text=True)
        if compile_proc.returncode != 0:
            print("Compilation failed:\n", compile_proc.stderr)
            return

        # Run
        print("Running...")
        if language == "csharp":
            run_cmd = ["mono", exe]
        else:
            run_cmd = [exe]
        run_proc = subprocess.run(run_cmd, capture_output=True, text=True)
        print("Program output:\n", run_proc.stdout)
        if run_proc.stderr:
            print("Program errors:\n", run_proc.stderr)

        # Play output.wav if it exists
        if os.path.exists("output.wav"):
            if sys.platform.startswith("linux"):
                subprocess.run(["aplay", "output.wav"])
            elif sys.platform == "darwin":
                subprocess.run(["afplay", "output.wav"])
            elif sys.platform == "win32":
                # Windows: best effort (requires Windows Media Player or similar)
                os.startfile("output.wav")
            else:
                print("Unknown platform. Please play output.wav manually.")
        else:
            print("No output.wav file generated.")

if __name__ == "__main__":
    # Example usage:
    c_example = r'''
#include <stdio.h>
#include <math.h>
#include <stdint.h>
#define SAMPLERATE 44100
#define DURATION 1
#define FREQ 523.25
int main() {
    FILE *f = fopen("output.wav", "wb");
    if (!f) return 1;
    int datasize = SAMPLERATE * DURATION * 2;
    fwrite("RIFF",1,4,f);
    int filesize = 36+datasize;
    fwrite(&filesize,4,1,f);
    fwrite("WAVEfmt ",1,8,f);
    int fmt_chunk_size=16;
    fwrite(&fmt_chunk_size,4,1,f);
    short audio_format=1, num_channels=1;
    int sample_rate=SAMPLERATE, byte_rate=SAMPLERATE*2;
    short block_align=2, bits_per_sample=16;
    fwrite(&audio_format,2,1,f);
    fwrite(&num_channels,2,1,f);
    fwrite(&sample_rate,4,1,f);
    fwrite(&byte_rate,4,1,f);
    fwrite(&block_align,2,1,f);
    fwrite(&bits_per_sample,2,1,f);
    fwrite("data",1,4,f);
    fwrite(&datasize,4,1,f);
    for(int i=0;i<SAMPLERATE*DURATION;i++){
        double t=(double)i/SAMPLERATE;
        int16_t sample=(int16_t)(sin(2*M_PI*FREQ*t)*32767);
        fwrite(&sample,2,1,f);
    }
    fclose(f);
    return 0;
}
'''
    # Change language and code as desired!
    run_code("c", c_example)
