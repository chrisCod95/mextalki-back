from types import MappingProxyType

MAX_EXP_POINTS = 1200

SILVER_CYCLONE = {
    'name': 'Silver Cyclone',
    'image': 'masks/mask1.png',
}

MR_KNOCK_OUT = {
    'name': 'Mr. Knock Out',
    'image': 'masks/mask2.png',
}

WARMONGER = {
    'name': 'Warmonger',
    'image': 'masks/mask3.png',
}

RED_REAPER = {
    'name': 'Red Reaper',
    'image': 'masks/mask4.png',
}

GOLDEN_WONDER = {
    'name': 'Golden Wonder',
    'image': 'masks/mask5.png',
}

TYPHON = {
    'name': 'Typhon',
    'image': 'masks/mask6.png',
}

masks = MappingProxyType({
    'SILVER_CYCLONE': SILVER_CYCLONE,
    'MR_KNOCK_OUT': MR_KNOCK_OUT,
    'WARMONGER': WARMONGER,
    'RED_REAPER': RED_REAPER,
    'GOLDEN_WONDER': GOLDEN_WONDER,
    'TYPHON': TYPHON,
})


def get_mask(exp_points: int):
    if exp_points <= 100:
        return masks['SILVER_CYCLONE']
    elif 100 < exp_points <= 200:
        return masks['MR_KNOCK_OUT']
    elif 200 < exp_points <= 400:
        return masks['WARMONGER']
    elif 400 < exp_points <= 800:
        return masks['RED_REAPER']
    elif 800 < exp_points < MAX_EXP_POINTS:
        return masks['GOLDEN_WONDER']
    return masks['TYPHON']
