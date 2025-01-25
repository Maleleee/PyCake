import pygame
import sounddevice as sd
import numpy as np
import asyncio


# Function to draw the cake and candle
def draw_cake(screen, candle_lit):
    screen.fill((255, 255, 255))  # White background
    
    # Draw a cute pink cake with multiple layers
    pygame.draw.rect(screen, (255, 192, 203), (150, 300, 200, 100))  # Bottom layer (pink)
    pygame.draw.rect(screen, (255, 182, 193), (170, 250, 160, 50))   # Middle layer (lighter pink)
    pygame.draw.rect(screen, (255, 172, 183), (190, 220, 120, 30))   # Top layer (even lighter pink)
    
    # Add some decorative dots (sprinkles)
    for i in range(10):
        x = np.random.randint(150, 350)
        y = np.random.randint(300, 400)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 3)  # White sprinkles
    
    # Candle
    pygame.draw.rect(screen, (255, 182, 193), (240, 170, 20, 50))  # Pink candle body
    if candle_lit:
        # Make the flame bigger and more animated
        pygame.draw.ellipse(screen, (255, 140, 0), (230, 140, 40, 40))  # Outer flame
        pygame.draw.ellipse(screen, (255, 200, 0), (235, 145, 30, 30))  # Inner flame

    pygame.display.flip()


# Function to detect a "blow" sound
def detect_blow(threshold=5, duration=1):  # Reduced threshold and duration
    print("Listening for a blow...")
    samplerate = 44100  # Sample rate for the microphone
    duration_samples = int(samplerate * duration)

    # Record audio for the specified duration
    try:
        audio_data = sd.rec(duration_samples, samplerate=samplerate, channels=1, dtype='float32')
        sd.wait()  # Wait until recording is finished
        volume = np.linalg.norm(audio_data) * 10  # Calculate volume
        print(f"Detected volume: {volume:.2f}")  # Debug: Show volume level
        return volume > threshold
    except Exception as e:
        print(f"Error with microphone input: {e}")
        return False


async def request_microphone_permission():
    try:
        await asyncio.sleep(0)  # Required for web version
        # The browser will show a permission prompt
        return True
    except Exception as e:
        print(f"Error requesting microphone permission: {e}")
        return False


# Main function to run the program
async def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Blow Out the Candle")
    clock = pygame.time.Clock()

    candle_lit = True
    running = True

    if not await request_microphone_permission():
        print("Microphone permission denied")
        return

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the cake and candle
        draw_cake(screen, candle_lit)

        # Check for blow detection
        if candle_lit:
            if detect_blow(threshold=5, duration=1):  # Much more sensitive threshold
                candle_lit = False  # Extinguish the candle

        clock.tick(30)
        await asyncio.sleep(0)  # Required for web version

    pygame.quit()


if __name__ == '__main__':
    asyncio.run(main())
