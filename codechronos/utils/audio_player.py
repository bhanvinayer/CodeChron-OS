"""
Audio Player - Handles sound effects and music
"""

import pygame
import os
from typing import Dict, Optional
import threading

class AudioPlayer:
    """Manages audio playback for the application"""
    
    def __init__(self):
        self.initialized = False
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music_playing = False
        self.volume = 0.7
        self.sfx_volume = 0.5
        self.init_pygame()
    
    def init_pygame(self):
        """Initialize pygame mixer"""
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.initialized = True
        except pygame.error as e:
            print(f"Could not initialize audio: {e}")
            self.initialized = False
    
    def load_sound(self, name: str, filepath: str) -> bool:
        """Load a sound effect"""
        if not self.initialized:
            return False
        
        try:
            if os.path.exists(filepath):
                self.sounds[name] = pygame.mixer.Sound(filepath)
                return True
            else:
                # Create placeholder sound data for missing files
                self.sounds[name] = self._create_placeholder_sound(name)
                return True
        except pygame.error as e:
            print(f"Could not load sound {name}: {e}")
            return False
    
    def play_sound(self, name: str, volume: Optional[float] = None) -> bool:
        """Play a sound effect"""
        if not self.initialized or name not in self.sounds:
            return False
        
        try:
            sound = self.sounds[name]
            if volume is not None:
                sound.set_volume(volume)
            else:
                sound.set_volume(self.sfx_volume)
            
            sound.play()
            return True
        except pygame.error as e:
            print(f"Could not play sound {name}: {e}")
            return False
    
    def play_mac_boot_sound(self):
        """Play the classic Mac boot sound"""
        if "mac_boot" not in self.sounds:
            self.load_sound("mac_boot", "assets/audio/mac-boot.wav")
        
        self.play_sound("mac_boot", 0.8)
    
    def play_button_click(self):
        """Play button click sound"""
        if "button_click" not in self.sounds:
            self.sounds["button_click"] = self._create_click_sound()
        
        self.play_sound("button_click", 0.3)
    
    def play_window_open(self):
        """Play window open sound"""
        if "window_open" not in self.sounds:
            self.sounds["window_open"] = self._create_window_sound()
        
        self.play_sound("window_open", 0.4)
    
    def play_era_transition(self, era: str):
        """Play era transition sound"""
        sound_name = f"transition_{era}"
        
        if sound_name not in self.sounds:
            self.sounds[sound_name] = self._create_transition_sound(era)
        
        self.play_sound(sound_name, 0.6)
    
    def play_background_music(self, era: str):
        """Play background music for an era"""
        if not self.initialized:
            return
        
        music_files = {
            "mac1984": "assets/audio/mac_ambient.mp3",
            "block2015": "assets/audio/block_theme.mp3", 
            "vibe2025": "assets/audio/vibe_ambient.mp3"
        }
        
        music_file = music_files.get(era)
        if music_file and os.path.exists(music_file):
            try:
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.set_volume(self.volume * 0.3)  # Quiet background music
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self.music_playing = True
            except pygame.error as e:
                print(f"Could not play background music: {e}")
    
    def stop_background_music(self):
        """Stop background music"""
        if self.initialized and self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False
    
    def set_volume(self, volume: float):
        """Set master volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        
        if self.music_playing:
            pygame.mixer.music.set_volume(self.volume * 0.3)
    
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def _create_placeholder_sound(self, name: str) -> pygame.mixer.Sound:
        """Create a placeholder sound when file is missing"""
        import numpy as np
        
        # Generate simple tone based on sound name
        if "boot" in name:
            # Pleasant startup chime
            duration = 1.5
            sample_rate = 22050
            frequency = 440  # A4
            
            t = np.linspace(0, duration, int(sample_rate * duration))
            wave = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 2)  # Decay
            wave = (wave * 32767).astype(np.int16)
            
        elif "click" in name:
            # Short click sound
            duration = 0.1
            sample_rate = 22050
            frequency = 800
            
            t = np.linspace(0, duration, int(sample_rate * duration))
            wave = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 50)
            wave = (wave * 16383).astype(np.int16)
            
        elif "window" in name:
            # Window open/close sound
            duration = 0.3
            sample_rate = 22050
            
            t = np.linspace(0, duration, int(sample_rate * duration))
            wave = (np.sin(2 * np.pi * 600 * t) + 
                   np.sin(2 * np.pi * 800 * t)) * np.exp(-t * 8)
            wave = (wave * 16383).astype(np.int16)
            
        else:
            # Generic beep
            duration = 0.2
            sample_rate = 22050
            frequency = 880
            
            t = np.linspace(0, duration, int(sample_rate * duration))
            wave = np.sin(2 * np.pi * frequency * t)
            wave = (wave * 16383).astype(np.int16)
        
        # Convert to stereo
        stereo_wave = np.array([[w, w] for w in wave])
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def _create_click_sound(self) -> pygame.mixer.Sound:
        """Create a button click sound"""
        return self._create_placeholder_sound("click")
    
    def _create_window_sound(self) -> pygame.mixer.Sound:
        """Create a window open sound"""
        return self._create_placeholder_sound("window")
    
    def _create_transition_sound(self, era: str) -> pygame.mixer.Sound:
        """Create era transition sound"""
        import numpy as np
        
        duration = 1.0
        sample_rate = 22050
        
        if era == "mac1984":
            # Retro 8-bit style
            frequencies = [440, 554, 659, 880]
        elif era == "block2015":
            # Playful ascending tones
            frequencies = [330, 415, 523, 659, 831]
        elif era == "vibe2025":
            # Futuristic swoosh
            frequencies = [220, 440, 880, 1760]
        else:
            frequencies = [440, 880]
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        wave = np.zeros_like(t)
        
        for i, freq in enumerate(frequencies):
            start_time = i * (duration / len(frequencies))
            end_time = (i + 1) * (duration / len(frequencies))
            
            mask = (t >= start_time) & (t < end_time)
            wave[mask] += np.sin(2 * np.pi * freq * (t[mask] - start_time))
        
        # Apply envelope
        wave *= np.exp(-t * 2)
        wave = (wave * 16383).astype(np.int16)
        
        # Convert to stereo
        stereo_wave = np.array([[w, w] for w in wave])
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def preload_sounds(self):
        """Preload common sounds"""
        common_sounds = [
            ("button_click", "assets/audio/click.wav"),
            ("window_open", "assets/audio/window.wav"),
            ("mac_boot", "assets/audio/mac-boot.wav")
        ]
        
        for name, filepath in common_sounds:
            self.load_sound(name, filepath)
    
    def cleanup(self):
        """Clean up audio resources"""
        if self.initialized:
            pygame.mixer.quit()
            self.initialized = False

# Global instance
audio_player = AudioPlayer()

# Preload sounds in a separate thread to avoid blocking
def preload_sounds_async():
    audio_player.preload_sounds()

if audio_player.initialized:
    threading.Thread(target=preload_sounds_async, daemon=True).start()
