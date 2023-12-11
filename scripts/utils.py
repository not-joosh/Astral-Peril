import pygame

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 16)
        self.color = (255, 255, 255)
        self.hover_color = (200, 200, 200)
        self.border_radius = 5
        self.is_hovered = False

    def draw(self, surface):
        if self.is_hovered:
            pygame.draw.rect(surface, self.hover_color, self.rect, border_radius=self.border_radius)
        else:
            pygame.draw.rect(surface, self.color, self.rect, border_radius=self.border_radius)
        
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.is_hovered = True
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                self.is_hovered = False
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Button clicked, perform action here
                pass
