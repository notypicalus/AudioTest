from moviepy.editor import VideoFileClip
import librosa
import noisereduce as nr
import soundfile as sf
from scipy.signal import butter, filtfilt

print("Libraries installed and imported successfully!")

def extract_audio_from_video(input_video, output_audio):
    video = VideoFileClip(input_video)
    video.audio.write_audiofile(output_audio)

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def enhance_audio(input_audio, output_audio):
    y, sr = librosa.load(input_audio, sr=None)

    # Noise reduction
    reduced_noise = nr.reduce_noise(y=y, sr=sr)
    
    # Equalization (bandpass filter for voice)
    filtered_audio = bandpass_filter(reduced_noise, 85.0, 255.0, sr)
    
    # Volume normalization
    y_norm = librosa.util.normalize(filtered_audio)
    
    # Save enhanced audio
    sf.write(output_audio, y_norm, sr)

def combine_audio_with_video(input_video, input_audio, output_video):
    video = VideoFileClip(input_video)
    audio = VideoFileClip(input_audio).audio
    final_video = video.set_audio(audio)
    final_video.write_videofile(output_video, codec="libx264", audio_codec="aac")

# Full process
input_video = 'input_video.mov'
extracted_audio = 'extracted_audio.wav'
enhanced_audio = 'enhanced_audio.wav'
output_video = 'output_video.mov'

extract_audio_from_video(input_video, extracted_audio)
enhance_audio(extracted_audio, enhanced_audio)
combine_audio_with_video(input_video, enhanced_audio, output_video)

