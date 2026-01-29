import pygame
import numpy as np
import math


class SoundManager:
    """Manager for game sounds and music"""
    
    def __init__(self):
        self.sounds = {}
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self._load_sounds()
    
    def _load_sounds(self):
        """Load all game sounds - create beep sounds programmatically"""
        try:
            # Create simple beep sounds for different game events
            self.sounds['jump'] = self._create_beep(440, 100)      # A4 note
            self.sounds['coin'] = self._create_beep(880, 150)      # A5 note (higher)
            self.sounds['powerup'] = self._create_beep(660, 200)   # E5 note
            self.sounds['hit'] = self._create_beep(220, 100)       # A3 note (lower)
            self.sounds['victory'] = self._create_victory_sound()
        except Exception as e:
            print(f"Error loading sounds: {e}")
    
    def _create_beep(self, frequency, duration_ms):
        """Create a simple beep sound using numpy"""
        try:
            sample_rate = 22050
            duration_sec = duration_ms / 1000.0
            num_samples = int(sample_rate * duration_sec)
            
            # Generate time array
            t = np.linspace(0, duration_sec, num_samples, False)
            
            # Generate sine wave
            wave = np.sin(2 * np.pi * frequency * t) * 0.3
            
            # Convert to 16-bit PCM
            wave_int = np.int16(wave * 32767)
            
            # Create stereo sound (duplicate for both channels)
            stereo = np.zeros((num_samples, 2), dtype=np.int16)
            stereo[:, 0] = wave_int
            stereo[:, 1] = wave_int
            
            # Create pygame sound
            sound = pygame.mixer.Sound(buffer=stereo.tobytes())
            return sound
        except Exception as e:
            print(f"Error creating beep: {e}")
            return None
    
    def _create_victory_sound(self):
        """Create a simple victory sound sequence"""
        try:
            sample_rate = 22050
            duration_per_note = 0.3  # 300ms per note
            
            # Three ascending notes
            frequencies = [440, 550, 660]  # A, C#, E
            
            all_waves = []
            for freq in frequencies:
                duration_sec = duration_per_note
                num_samples = int(sample_rate * duration_sec)
                t = np.linspace(0, duration_sec, num_samples, False)
                
                # Envelope: fade in and out
                envelope = np.ones(num_samples)
                fade_samples = int(sample_rate * 0.05)
                envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
                envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
                
                wave = np.sin(2 * np.pi * freq * t) * 0.3 * envelope
                all_waves.append(wave)
            
            # Concatenate all notes
            full_wave = np.concatenate(all_waves)
            wave_int = np.int16(full_wave * 32767)
            
            # Create stereo sound
            stereo = np.zeros((len(wave_int), 2), dtype=np.int16)
            stereo[:, 0] = wave_int
            stereo[:, 1] = wave_int
            
            sound = pygame.mixer.Sound(buffer=stereo.tobytes())
            return sound
        except Exception as e:
            print(f"Error creating victory sound: {e}")
            return None
    
    def play(self, sound_name):
        """Play a sound effect"""
        if sound_name in self.sounds and self.sounds[sound_name] is not None:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Error playing sound {sound_name}: {e}")
    
    def stop_all(self):
        """Stop all sounds"""
        try:
            pygame.mixer.stop()
        except:
            pass
