import pygame

def handle_key_press():
    out_put = {"run": True}
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            out_put["run"] = False
            return out_put
    return out_put