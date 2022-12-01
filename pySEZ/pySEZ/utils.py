from django.db import models
from django.contrib.auth import get_user_model



# rgb = tuple(R, G, B)
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


# value = '#bedead'
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))


def opposite_color(color, version=None):
    R, G, B = hex_to_rgb(color)
    match version:
        case 1:
            R += -196 if R >= 220 else 196 if R <= 59 else -R//2
            G += -196 if G >= 220 else 196 if G <= 59 else -G//2
            B += -196 if B >= 220 else 196 if B <= 59 else -B//2
        case 2:
            R = 8 if R > 128 else 248
            G = 8 if G > 128 else 248
            B = 8 if B > 128 else 248
        case default:
            R, G, B = (0, 0, 0) if (R+G+B)//3 > 128 else (255, 255, 255)
    return rgb_to_hex((R, G, B))

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

