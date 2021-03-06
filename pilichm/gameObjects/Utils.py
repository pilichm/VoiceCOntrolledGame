from pilichm.gameObjects.Constants import SPRITE_FIRE_RED_GIF, SPRITE_FIRE_BLUE_GIF
import PIL.Image


def load_fire_gif(fire_color):
    fire_animation = []
    if fire_color == 'red':
        fire_gif = PIL.Image.open(SPRITE_FIRE_RED_GIF)
    elif fire_color == 'blue':
        fire_gif = PIL.Image.open(SPRITE_FIRE_BLUE_GIF)

    print(f"Frame count {fire_gif.n_frames}")

    try:
        index = 0
        while 1:
            fire_gif.seek(index)
            frame = fire_gif.copy()
            if index == 0:
                palette = frame.getpalette()
            else:
                frame.putpalette(palette)
            fire_animation.append(frame)
            index += 1
    except EOFError:
        pass

    return fire_animation
