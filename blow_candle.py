import pygame
import sounddevice as sd
import numpy as np
import asyncio
import platform
import sys
import io
import base64

print("Game is loading...")

# Check if we're running in the browser
IS_WEB = platform.system() == 'Emscripten'

# Initialize Pygame with special flags for web
pygame.init()
if IS_WEB:
    import platform
    import asyncio
    from pygame.display import set_mode, flip
    CANVAS_WIDTH = 500
    CANVAS_HEIGHT = 500
    screen = set_mode((CANVAS_WIDTH, CANVAS_HEIGHT), flags=pygame.SRCALPHA)
else:
    screen = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Blow Out the Candle!")
clock = pygame.time.Clock()

# Add this constant after the imports and constants
BIRTHDAY_MUSIC = base64.b64decode("""
    {{ I'll provide this data in the next message for better readability }}
""")

# Function to draw the cake and candle
def draw_cake(screen, candle_lit):
    screen.fill((255, 255, 255))  # White background
    
    # Make cake even cuter with more decorations
    # Bottom layer (pink with gradient)
    pygame.draw.rect(screen, (255, 192, 203), (150, 300, 200, 100))  # Base pink
    pygame.draw.rect(screen, (255, 182, 193), (170, 250, 160, 50))   # Middle pink
    pygame.draw.rect(screen, (255, 172, 183), (190, 220, 120, 30))   # Top pink

    # Add frosting details (white decorative lines)
    for y in range(300, 400, 20):
        pygame.draw.arc(screen, (255, 255, 255), (150, y, 200, 20), 0, 3.14, 2)

    # Add more decorative sprinkles
    for i in range(20):
        x = np.random.randint(150, 350)
        y = np.random.randint(220, 400)
        color = np.random.choice([
            (255, 255, 255),  # White
            (255, 105, 180),  # Hot pink
            (255, 220, 220),  # Light pink
        ])
        pygame.draw.circle(screen, color, (x, y), 3)

    # Prettier candle
    pygame.draw.rect(screen, (255, 182, 193), (240, 170, 20, 50))  # Pink candle body
    # Add candle details
    pygame.draw.rect(screen, (255, 192, 203), (242, 170, 16, 50))  # Lighter pink detail

    if candle_lit:
        # Animated flame
        flame_offset = np.sin(pygame.time.get_ticks() * 0.01) * 3
        # Outer flame
        pygame.draw.ellipse(screen, (255, 140, 0), 
                          (230, 140 + flame_offset, 40, 40))
        # Inner flame
        pygame.draw.ellipse(screen, (255, 200, 0), 
                          (235, 145 + flame_offset, 30, 30))

    pygame.display.flip()


# Function to detect a "blow" sound
async def detect_blow(threshold=2, duration=0.5):  # Made even more sensitive
    print("Listening for a blow...")
    samplerate = 44100
    duration_samples = int(samplerate * duration)

    try:
        # For web version, we need to handle audio differently
        if platform.system() == 'Emscripten':
            # This will ensure the microphone is accessed properly in the browser
            await asyncio.sleep(0)
        
        audio_data = sd.rec(duration_samples, samplerate=samplerate, channels=1, dtype='float32')
        sd.wait()
        volume = np.linalg.norm(audio_data) * 10
        print(f"Detected volume: {volume:.2f}")
        return volume > threshold
    except Exception as e:
        print(f"Error with microphone input: {e}")
        return False


async def request_microphone_permission():
    try:
        # For web version, we need to explicitly request microphone access
        if platform.system() == 'Emscripten':  # Checks if running in browser
            print("Requesting microphone permission...")
            # This will trigger the browser's permission prompt
            await asyncio.sleep(0)
            sd.check_input_settings(device=None)
        return True
    except Exception as e:
        print(f"Error requesting microphone permission: {e}")
        return False


# Add this function after the imports and constants
def init_music():
    try:
        if not IS_WEB:  # Only initialize music for desktop version
            pygame.mixer.init()
            music_file = io.BytesIO(BIRTHDAY_MUSIC)
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)  # -1 means loop forever
    except Exception as e:
        print(f"Error loading music: {e}")


# Main function to run the program
async def main():
    print("Main function started...")
    init_music()  # Initialize and start the music
    clock = pygame.time.Clock()
    candle_lit = True
    running = True

    while running:
        if IS_WEB:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    candle_lit = False
                    print("Candle blown out by click!")
                    if not IS_WEB:
                        pygame.mixer.music.stop()  # Stop music when candle is blown out
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    candle_lit = False
                    pygame.mixer.music.stop()  # Stop music when candle is blown out

        # Draw the cake
        draw_cake(screen, candle_lit)
        
        if IS_WEB:
            await asyncio.sleep(0)  # Let the browser breathe
        
        clock.tick(30)

    pygame.quit()


if __name__ == '__main__':
    if IS_WEB:
        print("Running in web mode...")
        asyncio.run(main())
    else:
        print("Running in desktop mode...")
        asyncio.run(main())
