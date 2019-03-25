def DummyPlugSystem(game, obj, state:str):
    pass

def AntiGravity(game, obj, state:str):
    if state == "enter":
        obj.gravity = -obj.gravity
        obj.sprite.scale_y = -obj.sprite.scale_y
    elif state == "stay":
        pass
    elif state == "leave":
        obj.gravity = -obj.gravity
        obj.sprite.scale_y = -obj.sprite.scale_y


def Wind(game, obj, state: str, x:int=0, y:int=0):
    if state == "enter":
        pass
    elif state == "stay":
        obj.xSpeed += x
        obj.ySpeed -= y
    elif state == "leave":
        pass


effects = {
    'None': (DummyPlugSystem, (255, 0, 0, 20)),
    'Anti gravity': (AntiGravity, (0, 255, 0, 20)),
    'Wind Left': (Wind, (0, 0, 255, 20)),
}