from PIL import Image
hero_open = "sprites/pacman_open.png"
im = Image.open(hero_open)
im_rotate = im.rotate(360)
im_rotate.save('sprites/pacman_open_right.png')
im.close()