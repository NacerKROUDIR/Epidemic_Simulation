from pygame import gfxdraw
import pygame
from numpy import clip, interp, round


class Label:
    def __init__(self, display, font, text, position, background_color=(220, 220, 220)):
        self.display = display
        self.font = font
        self.text = font.render(str(round(self.text, 2)),True, (0, 0, 0), background_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.bottomright = position

    def update_text(self, text):
        self.text = text

    def draw(self):
        self.display.blit(self.text, self.text_rect)


class Slider:
    def __init__(self, display, font, label, position, width=200, height=22, valueRange=(2,10000), initial_value=3, buttonRadius=10, buttonColor=(80,80,80), sliderBarColor=(200,200,200), textColor = (0,0,0), textBGColor=(220, 220, 220), append_text=""):
        self.display = display
        self.font = font
        self.label = label
        self.position = position
        self.width = width
        self.height = height
        self.valueRange = valueRange
        self.buttonRadius = buttonRadius
        self.buttonColor = buttonColor
        self.sliderBarColor = sliderBarColor
        self.textColor = textColor
        self.textBGColor = textBGColor
        self.append_text = append_text
        self.sliderBar = pygame.Rect(position, (width, height))
        self.minXBarPosition = self.position[0] + self.buttonRadius
        self.maxXBarPosition = self.position[0] + self.width - self.buttonRadius - 1
        self.minYBarPosition = self.position[1] + self.height / 2 - self.buttonRadius
        self.maxYBarPosition = self.position[1] + self.height / 2 + self.buttonRadius + 1
        self.centerX = int(interp(initial_value, self.valueRange, (self.minXBarPosition, self.maxXBarPosition)))
        self.centerY = int(position[1] + (height/2))
        self.pressed = False
        self.value = initial_value
        label = self.font.render(self.label, True, self.textColor, self.textBGColor)
        self.labelRect = label.get_rect()
        self.labelRect.bottomright = (self.minXBarPosition-15, self.minYBarPosition + self.height - 2)
        value = self.font.render(str(int(self.value)), True, self.textColor, self.textBGColor)
        self.valueRect = value.get_rect()
        self.valueRect.bottomleft = (self.maxXBarPosition+15, self.minYBarPosition + self.height - 3)

    def draw(self):
        pygame.draw.rect(self.display, self.sliderBarColor, self.sliderBar, border_radius=10)
        gfxdraw.circle(self.display, self.centerX, self.centerY, self.buttonRadius, self.buttonColor)
        gfxdraw.filled_circle(self.display, self.centerX, self.centerY, self.buttonRadius, self.buttonColor)
        label = self.font.render(self.label, True, self.textColor, self.textBGColor)
        self.display.blit(label, self.labelRect)
        value = self.font.render(str(self.value)+self.append_text, True, self.textColor, self.textBGColor)
        self.display.blit(value, self.valueRect)
        return self.check_click()

    def check_click(self):
        action=False
        if pygame.mouse.get_pressed()[0]:
            mouseX, mouseY = pygame.mouse.get_pos()
            if self.pressed:
                self.centerX = clip(mouseX, self.minXBarPosition, self.maxXBarPosition)
                self.value = int(interp(self.centerX, (self.minXBarPosition, self.maxXBarPosition), self.valueRange))
                action = True
            else:
                if self.minXBarPosition < mouseX < self.maxXBarPosition and self.minYBarPosition < mouseY < self.maxYBarPosition:
                    self.centerX = clip(mouseX, self.minXBarPosition, self.maxXBarPosition)
                    self.pressed = True
                    action = True
                    self.value = int(interp(self.centerX, (self.minXBarPosition, self.maxXBarPosition), self.valueRange))
        else:
            if self.pressed:
                action=True
                self.pressed = False
        return action


class Toggle:
    def __init__(self, display, font,  label, position, width=40, height=22, initial_value=False, buttonRadius=10, buttonColor=(80,80,80), toggleBarColorOff=(200,200,200), toggleBarColorOn=(28, 217, 28), textColor = (0,0,0), textBGColor=(220, 220, 220)):
        self.display = display
        self.font = font
        self.label = label
        self.position = position
        self.width = width
        self.height = height
        self.buttonRadius = buttonRadius
        self.buttonColor = buttonColor
        self.toggleBarColorOff = toggleBarColorOff
        self.toggleBarColorOn = toggleBarColorOn
        self.textColor = textColor
        self.textBGColor = textBGColor
        self.toggleBar = pygame.Rect(position, (width, height))
        self.minXBarPosition = self.position[0] + self.buttonRadius
        self.maxXBarPosition = self.position[0] + self.width - self.buttonRadius - 1
        self.minYBarPosition = self.position[1] + self.height / 2 - self.buttonRadius
        self.maxYBarPosition = self.position[1] + self.height / 2 + self.buttonRadius + 1
        self.value = initial_value
        if self.value:
            self.centerX = self.maxXBarPosition
            self.color = self.toggleBarColorOn
        else:
            self.centerX = self.minXBarPosition
            self.color = self.toggleBarColorOff
        self.centerY = int(position[1] + (height/2))
        self.pressed = False
        label = self.font.render(self.label, True, self.textColor, self.textBGColor)
        self.labelRect = label.get_rect()
        self.labelRect.bottomright = (self.minXBarPosition-20, self.minYBarPosition + self.height - 2)

    def draw(self):
        pygame.draw.rect(self.display, self.color, self.toggleBar, border_radius=10)
        gfxdraw.circle(self.display, self.centerX, self.centerY, self.buttonRadius, self.buttonColor)
        gfxdraw.filled_circle(self.display, self.centerX, self.centerY, self.buttonRadius, self.buttonColor)
        label = self.font.render(self.label, True, self.textColor, self.textBGColor)
        self.display.blit(label, self.labelRect)
        return self.check_click()

    def check_click(self):
        action = False
        if pygame.mouse.get_pressed()[0]:
            mouseX, mouseY = pygame.mouse.get_pos()
            if self.toggleBar.collidepoint((mouseX, mouseY)):
                if not self.pressed:
                    if self.value:
                        self.value = False
                        self.centerX = self.minXBarPosition
                        self.color = self.toggleBarColorOff
                    else:
                        self.value = True
                        self.centerX = self.maxXBarPosition
                        self.color = self.toggleBarColorOn
                    self.pressed = True
        else:
            if self.pressed:
                self.pressed = False
                action = True
        return action


class Button:
    """tutorial: https://www.youtube.com/watch?v=8SzTzvrWaAA"""
    def __init__(self, display, font, text, width, height, position, elevation=3):
        self.display = display
        self.font = font
        self.text = text
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_position = position[1]
        self.top_rect = pygame.Rect(position, (width, height))
        self.top_color = '#34BF49'
        self.bottom_rect = pygame.Rect(position, (width, height))
        self.bottom_color = '#297829'
        self.text_surf = self.font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        self.pressed = False

    def draw(self):
        self.top_rect.y = self.original_y_position - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
        pygame.draw.rect(self.display, self.bottom_color, self.bottom_rect)
        pygame.draw.rect(self.display, self.top_color, self.top_rect)
        self.display.blit(self.text_surf, self.text_rect)
        return self.check_click()

    def check_click(self):
        action = False
        mouse_position = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_position):
            self.top_color = '#419E41'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                if self.pressed:
                    # Do stuff
                    self.dynamic_elevation = self.elevation
                    action = True
                    self.pressed = False
        else:
            self.top_color = '#34BF49'
        return action


class StartButton(Button):
    def __init__(self, display, font, text, pressed_text, width, height, position, paused=True):
        Button.__init__(self, display, font, text, width, height, position)
        self.pressed_text = pressed_text
        self.paused = paused

    def pause(self):
        if self.paused:
            self.text_surf = self.font.render(self.pressed_text, True, '#FFFFFF')
            self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        else:
            self.text_surf = self.font.render(self.text, True, '#FFFFFF')
            self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        self.paused = not self.paused

    def check_click(self):
        mouse_position = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_position):
            self.top_color = '#419E41'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                if self.pressed:
                    # Do stuff
                    self.pause()
                    self.dynamic_elevation = self.elevation
                    self.pressed = False
        else:
            self.top_color = '#34BF49'


class ResetButton(Button):
    def __init__(self, display, font, text, width, height, position, populate):
        Button.__init__(self, display, font, text, width, height, position)
        self.populate = populate

    def reset(self, space, particles, population, initially_infected):
        if len(particles) != 0:
            for particle in particles:
                space.remove(particle.body, particle.shape)
        return self.populate(population, initially_infected)

    def check_click(self):
        action = False
        mouse_position = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_position):
            self.top_color = '#419E41'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                if self.pressed:
                    self.dynamic_elevation = self.elevation
                    action = True
                    self.pressed = False
        else:
            self.top_color = '#34BF49'
        return action


class HoldButton(Button):
    def __init__(self, display, font, text, width, height, position, pressed=False, elevation=3):
        Button.__init__(self, display, font, text, width, height, position, elevation=elevation)
        self.pressed = pressed
        self.disable = False

    def disable_click(self):
        self.disable = True

    def check_click(self):
        action = False
        mouse_position = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_position):
            if not self.pressed:
                if pygame.mouse.get_pressed()[0]:
                    self.pressed = True
                    action = True
        if self.disable:
            self.pressed = False
            self.disable = False
        else:
            if not self.pressed:
                self.top_color = '#34BF49'
            else:
                self.top_color = '#419E41'
        return action


class ActiveButton:
    def __init__(self, display, font, texts, widths, height, position, elevation=3):
        self.x, self.y = position
        self.button1 = HoldButton(display, font, texts[0], widths[0], height, position, True, elevation=elevation)
        self.button2 = HoldButton(display, font, texts[1], widths[1], height, (self.x + widths[0], self.y), elevation=elevation)
        self.button3 = HoldButton(display, font, texts[2], widths[2], height, (self.x + widths[0] + widths[1], self.y), elevation=elevation)
        self.mode = 0

    def draw(self):
        action = False
        if self.button1.draw():
            self.mode = 0
            self.button2.disable_click()
            self.button3.disable_click()
            action = True
        if self.button2.draw():
            self.mode = 1
            self.button1.disable_click()
            self.button3.disable_click()
            action = True
        if self.button3.draw():
            self.mode = 2
            self.button1.disable_click()
            self.button2.disable_click()
            action = True
        return action
