# maps key codes to names identified by the backends (pynput and keyboard, respectively)
import pygame

from backends.keyboard import Keyboard
from backends.pynput import Pynput
from constants import SOUND_FILE, BackendOption, ProfileOption
from utils import backend_option_to_class, get_sound_path_by_code_and_profile

CODE_TO_NAME = {
    "1": ["esc", "esc"],
    "59": ["f1", "f1"],
    "60": ["f2", "f2"],
    "61": ["f3", "f3"],
    "62": ["f4", "f4"],
    "63": ["f5", "f5"],
    "64": ["f6", "f6"],
    "65": ["f7", "f7"],
    "66": ["f8", "f8"],
    "67": ["f9", "f9"],
    "68": ["f10", "f10"],
    "87": ["f11", "f11"],
    "88": ["f12", "f12"],
    "91": ["f13", "f13"],
    "92": ["f14", "f14"],
    "93": ["f15", "f15"],
    "41": ["`", "`"],
    "2": ["1", "1"],
    "3": ["2", "2"],
    "4": ["3", "3"],
    "5": ["4", "4"],
    "6": ["5", "5"],
    "7": ["6", "6"],
    "8": ["7", "7"],
    "9": ["8", "8"],
    "10": ["9", "9"],
    "11": ["0", "0"],
    "12": ["-", "-"],
    "13": ["=", "="],
    "14": ["backspace", "backspace"],
    "15": ["tab", "tab"],
    "58": ["capslock", "capslock"],
    "30": ["a", "a"],
    "48": ["b", "b"],
    "46": ["c", "c"],
    "32": ["d", "d"],
    "18": ["e", "e"],
    "33": ["f", "f"],
    "34": ["g", "g"],
    "35": ["h", "h"],
    "23": ["i", "i"],
    "36": ["j", "j"],
    "37": ["k", "k"],
    "38": ["l", "l"],
    "50": ["m", "m"],
    "49": ["n", "n"],
    "24": ["o", "o"],
    "25": ["p", "p"],
    "16": ["q", "q"],
    "19": ["r", "r"],
    "31": ["s", "s"],
    "20": ["t", "t"],
    "22": ["u", "u"],
    "47": ["v", "v"],
    "17": ["w", "w"],
    "45": ["x", "x"],
    "21": ["y", "y"],
    "44": ["z", "z"],
    "26": ["[", "["],
    "27": ["]", "]"],
    "43": ["\\", "\\"],
    "39": [";", ";"],
    "40": ["'", "'"],
    "28": ["enter", "enter"],
    "51": [",", ","],
    "52": [".", "."],
    "53": ["/", "/"],
    "57": ["space", "space"],
    "3639": ["prtsc", "prtsc"],
    "70": ["scrlk", "scrlk"],
    "3653": ["pause", "pause"],
    "3666": ["ins", "ins"],
    "3667": ["del", "del"],
    "3655": ["home", "home"],
    "3663": ["end", "end"],
    "3657": ["pgup", "pgup"],
    "3665": ["pgdn", "pgdn"],
    "57416": ["\u2191", "\u2191"],
    "57419": ["\u2190", "\u2190"],
    "57421": ["\u2192", "\u2192"],
    "57424": ["\u2193", "\u2193"],
    "42": ["shift", "shift"],
    "54": ["shift_r", "shift"],
    "29": ["ctrl", "ctrl"],
    "3613": ["ctrl_r", "ctrl"],
    "56": ["alt", "alt"],
    "3640": ["alt", "alt"],
    "3675": ["cmd", "meta"],
    "3676": ["cmd_r", "meta"],
    "3677": ["menu", "menu"],
    "69": ["num_lock", "num lock"],
}


def get_sounds(backend: BackendOption, profile: ProfileOption):
    pygame.mixer.init()

    backend_cls = backend_option_to_class(backend)
    if backend_cls == Pynput:
        idx = 0
    elif backend_cls == Keyboard:
        idx = 1
    else:
        raise NotImplementedError
    sounds = {}
    default = get_default_sound(profile)
    for code, names in CODE_TO_NAME.items():
        name = names[idx]
        sound_file = get_sound_path_by_code_and_profile(code, profile)
        if sound_file.exists():
            sound = pygame.mixer.Sound(sound_file)
        else:
            sound = default
        sounds[name] = sound

    return sounds


def get_default_sound(profile: ProfileOption):
    sound_file = get_sound_path_by_code_and_profile("1", profile)
    if not sound_file.exists():
        sound_file = SOUND_FILE
    return pygame.mixer.Sound(sound_file)
