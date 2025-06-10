#!/usr/bin/env python3
# author: Ali Ural
# date: 06-09-2025
# description: examPrep, flashcard viewer that displays random QnA's. 

import pygame
from PIL import Image, ImageDraw, ImageFont
import os
import random
import sys

# Configuration

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
BACKGROUND_COLOR = (0, 0, 0) 
TEXT_COLOR = (255,255,255) 
INFO_BG_COLOR = (0,0,0) 

class ImageFlashcardAppPygame:
    def __init__(self):
        """Initializes the application"""
        pygame.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Image Flashcard Viewer (Pygame)")
        self.font = pygame.font.SysFont("Helvetica", 24)
        self.clock = pygame.time.Clock()

        self.question_path = "questions"
        self.answer_path = "answers"
        self.image_pairs = []
        self.current_pair = None
        self.current_question_surface = None
        self.current_answer_surface = None
        self.answer_visible = False
        
        self.setup_images()
        if not self.image_pairs:
            print("Error: No matching image pairs found. Please check your 'questions' and 'answers' folders.")
            self.draw_error_message("No image pairs found in 'questions' and 'answers' folders.")
            pygame.time.wait(5000) 
            self.quit_app()

    def create_dummy_images(self):
        """Creates dummy question and answer images using Pillow if folders don't exist."""
        print("Creating dummy image folders and files...")
        if not os.path.exists(self.question_path):
            os.makedirs(self.question_path)
        if not os.path.exists(self.answer_path):
            os.makedirs(self.answer_path)

        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except IOError:
            print("Arial font not found, using default.")
            font = ImageFont.load_default() 

        for i in range(1, 4):
            q_img = Image.new('RGB', (600, 300), color=(73, 109, 137))
            d = ImageDraw.Draw(q_img)
            d.text((20, 20), f"This is Question {i}", fill=(255, 255, 0), font=font)
            q_img.save(os.path.join(self.question_path, f"image{i}.png"))

            a_img = Image.new('RGB', (600, 300), color=(137, 73, 109))
            d = ImageDraw.Draw(a_img)
            d.text((20, 20), f"This is Answer {i}", fill=(255, 255, 255), font=font)
            a_img.save(os.path.join(self.answer_path, f"image{i}.png"))
        
        print("Dummy setup complete. Please restart the application to load the new images.")



    def setup_images(self):
        """Loads every question image."""
        if not os.path.exists(self.question_path) or not os.path.exists(self.answer_path):
            self.create_dummy_images()
            self.draw_error_message("Created dummy image folders. Please restart the app.", 3000)
            self.quit_app()

        question_files = sorted(os.listdir(self.question_path))

        self.image_pairs = []
        for q_file in question_files:
            q_path = os.path.join(self.question_path, q_file)
            a_path = os.path.join(self.answer_path, q_file)
            a_path = a_path if os.path.exists(a_path) else None   
            self.image_pairs.append((q_path, a_path))

        print(f"Found {len(self.image_pairs)} questions "
            f"({sum(a is not None for _, a in self.image_pairs)} have answers).")

    def load_and_scale_image(self, path, is_question):
        """Loads an image and scales it to fit its designated screen area."""
        if path is None:                         
            return None

        try:
            image = pygame.image.load(path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            return None

        max_width = self.screen.get_width() - 40 
        max_height = (self.screen.get_height() // 2) - 40 

        img_rect = image.get_rect()
        scale_w = max_width / img_rect.width
        scale_h = max_height / img_rect.height
        scale = min(scale_w, scale_h)

        if scale < 1: 
            new_width = int(img_rect.width * scale)
            new_height = int(img_rect.height * scale)
            image = pygame.transform.smoothscale(image, (new_width, new_height))
        
        return image

    def show_random_question(self):
        """Selects a random question and prepares it for display."""
        if not self.image_pairs:
            return
            
        self.answer_visible = False
        self.current_answer_surface = None
        
        self.current_pair = random.choice(self.image_pairs)
        self.current_qname = os.path.basename(self.current_pair[0])   
        self.current_question_surface = self.load_and_scale_image(self.current_pair[0], True)

    def show_answer(self):
        """Prepares the corresponding answer for display."""
        if not self.current_pair:
            return

        self.answer_visible = True
        self.current_answer_surface = self.load_and_scale_image(self.current_pair[1], is_question=False)

    def handle_input(self):
        """Processes user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_app()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.answer_visible:
                        self.show_random_question()
                    else:
                        self.show_answer()
                elif event.key == pygame.K_ESCAPE:
                    self.quit_app()
            if event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                if self.current_pair:
                    self.current_question_surface = self.load_and_scale_image(self.current_pair[0], True)
                    if self.answer_visible:
                         self.current_answer_surface = self.load_and_scale_image(self.current_pair[1], False)


    def draw_elements(self):
        """Draws all elements to the screen."""
        self.screen.fill(BACKGROUND_COLOR)

        if self.current_question_surface:
            rect = self.current_question_surface.get_rect(centerx=self.screen.get_width() // 2, y=20)
            self.screen.blit(self.current_question_surface, rect)
        
        if self.answer_visible and self.current_answer_surface:
            answer_y_pos = (self.screen.get_height() // 2) + 10 
            rect = self.current_answer_surface.get_rect(centerx=self.screen.get_width() // 2, y=answer_y_pos)
            self.screen.blit(self.current_answer_surface, rect)

        info_bar_rect = pygame.Rect(0,
                                    self.screen.get_height() - 40,
                                    self.screen.get_width(),
                                    40)
        pygame.draw.rect(self.screen, INFO_BG_COLOR, info_bar_rect)

        label = ""
        if self.answer_visible and self.current_pair:
            q_file = self.current_qname
            a_file = os.path.basename(self.current_pair[1]) if self.current_pair[1] else "--"
            label = f"   |   Q: {q_file}  "

        info_text = self.font.render(
            "[Space] answer/next   [Esc] quit" + label,
            True,
            TEXT_COLOR
        )
        self.screen.blit(info_text, info_text.get_rect(center=info_bar_rect.center))
        pygame.display.flip()

    def draw_error_message(self, message, wait_ms=0):
        """Displays an error message on the screen."""
        self.screen.fill(BACKGROUND_COLOR)
        error_text = self.font.render(message, True, (200, 0, 0))
        text_rect = error_text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(error_text, text_rect)
        pygame.display.flip()
        if wait_ms > 0:
            pygame.time.wait(wait_ms)
            
    def run(self):
        """The main loop of the application."""
        if self.image_pairs:
            self.show_random_question()

        running = True
        while running:
            self.handle_input()
            self.draw_elements()
            self.clock.tick(30) 

    def quit_app(self):
        """Shuts down Pygame and exits the program."""
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = ImageFlashcardAppPygame()
    app.run()

