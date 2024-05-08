import pygame

navigation_action = "stay"


def handle_key_press():
    global navigation_action
    out_put = {"run": True}
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            out_put["run"] = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                navigation_action = "left"
            if event.key == pygame.K_d:
                navigation_action = "right"
            if event.key == pygame.K_w:
                navigation_action = "up"
            if event.key == pygame.K_s:
                navigation_action = "down"
    return out_put


class HumanController:
    def get_action(self):
        global navigation_action
        out_put = navigation_action
        navigation_action = "stay"
        return out_put
