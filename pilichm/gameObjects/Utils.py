from pilichm.gameObjects.Constants import RESOURCES_DIR
import PIL.Image


def load_fire_gif(fire_color):
    fire_animation = []
    if fire_color == 'red':
        fire_gif = PIL.Image.open(f"{RESOURCES_DIR}fire_red_gif.gif")
    elif fire_color == 'blue':
        fire_gif = PIL.Image.open(f"{RESOURCES_DIR}fire_blue_gif.gif")

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
