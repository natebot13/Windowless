def DPS(game, obj, apply: bool):
    pass

def AGS(game, obj, apply: bool):
    if apply:
        obj.gravity = -obj.gravity
        obj.sprite.scale_y = -obj.sprite.scale_y
    else:
        obj.gravity = -obj.gravity
        obj.sprite.scale_y = -obj.sprite.scale_y


def WS(game, obj, apply: bool):
        if apply:
            obj.drag = obj.drag + 1
        else:
            obj.drag = obj.drag - 1


effects = {
    'none': (DPS, (255, 0, 0, 20)),
    'AGC': (AGS, (0, 255, 0, 20)),
    'WC': (WS, (0, 0, 255, 20))
}