import shutil
import tkinter as tk
import tkinter.messagebox as messagebox
import customtkinter
import subprocess
import keyboard
import threading
import time
import cv2
import numpy as np
import pyautogui
import json
import sys
import psutil
import os
from contextlib import contextmanager
import datetime  # Добавлен импорт datetime

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

VERSION = "v1.01"

PATTERNS = {
    "vergeland_bank": cv2.imread("patterns/locations/vergeland/vergeland_bank.png", cv2.IMREAD_COLOR),
    "vergeland_banka": cv2.imread("patterns/locations/vergeland/vergeland_banka.png", cv2.IMREAD_COLOR),
    "vergeland_shop": cv2.imread("patterns/locations/vergeland/vergeland_shop.png", cv2.IMREAD_COLOR),
    "vergeland_shopa": cv2.imread("patterns/locations/vergeland/vergeland_shopa.png", cv2.IMREAD_COLOR),

    "harangerfjord_bank": cv2.imread("patterns/locations/harangerfjord/harangerfjord_bank.png", cv2.IMREAD_COLOR),
    "harangerfjord_banka": cv2.imread("patterns/locations/harangerfjord/harangerfjord_banka.png", cv2.IMREAD_COLOR),
    "harangerfjord_shop": cv2.imread("patterns/locations/harangerfjord/harangerfjord_shop.png", cv2.IMREAD_COLOR),
    "harangerfjord_shopa": cv2.imread("patterns/locations/harangerfjord/harangerfjord_shopa.png", cv2.IMREAD_COLOR),

    "heimskringla_bank": cv2.imread("patterns/locations/heimskringla/heimskringla_bank.png", cv2.IMREAD_COLOR),
    "heimskringla_banka": cv2.imread("patterns/locations/heimskringla/heimskringla_banka.png", cv2.IMREAD_COLOR),
    "heimskringla_shop": cv2.imread("patterns/locations/heimskringla/heimskringla_shop.png", cv2.IMREAD_COLOR),
    "heimskringla_shopa": cv2.imread("patterns/locations/heimskringla/heimskringla_shopa.png", cv2.IMREAD_COLOR),

    "sorian_bank": cv2.imread("patterns/locations/sorian/sorian_bank.png", cv2.IMREAD_COLOR),
    "sorian_banka": cv2.imread("patterns/locations/sorian/sorian_banka.png", cv2.IMREAD_COLOR),
    "sorian_shop": cv2.imread("patterns/locations/sorian/sorian_shop.png", cv2.IMREAD_COLOR),
    "sorian_shopa": cv2.imread("patterns/locations/sorian/sorian_shopa.png", cv2.IMREAD_COLOR),

    "ortre_shop": cv2.imread("patterns/locations/ortre/ortre_shop.png", cv2.IMREAD_COLOR),
    "ortre_shopa": cv2.imread("patterns/locations/ortre/ortre_shopa.png", cv2.IMREAD_COLOR),
    "ortre_bank": cv2.imread("patterns/locations/ortre/ortre_bank.png", cv2.IMREAD_COLOR),
    "ortre_banka": cv2.imread("patterns/locations/ortre/ortre_banka.png", cv2.IMREAD_COLOR),

    "almeric_bank": cv2.imread("patterns/locations/almeric/almeric_bank.png", cv2.IMREAD_COLOR),
    "almeric_banka": cv2.imread("patterns/locations/almeric/almeric_banka.png", cv2.IMREAD_COLOR),
    "almeric_shop": cv2.imread("patterns/locations/almeric/almeric_shop.png", cv2.IMREAD_COLOR),
    "almeric_shopa": cv2.imread("patterns/locations/almeric/almeric_shopa.png", cv2.IMREAD_COLOR),

    "metanoia_bank": cv2.imread("patterns/locations/metanoia/metanoia_bank.png", cv2.IMREAD_COLOR),
    "metanoia_banka": cv2.imread("patterns/locations/metanoia/metanoia_banka.png", cv2.IMREAD_COLOR),
    "metanoia_shop": cv2.imread("patterns/locations/metanoia/metanoia_shop.png", cv2.IMREAD_COLOR),
    "metanoia_shopa": cv2.imread("patterns/locations/metanoia/metanoia_shopa.png", cv2.IMREAD_COLOR),

    "panfobion_bank": cv2.imread("patterns/locations/panfobion/panfobion_bank.png", cv2.IMREAD_COLOR),
    "panfobion_banka": cv2.imread("patterns/locations/panfobion/panfobion_banka.png", cv2.IMREAD_COLOR),
    "panfobion_shop": cv2.imread("patterns/locations/panfobion/panfobion_shop.png", cv2.IMREAD_COLOR),
    "panfobion_shopa": cv2.imread("patterns/locations/panfobion/panfobion_shopa.png", cv2.IMREAD_COLOR),

    "vjuh": cv2.imread("patterns/vjuh.png", cv2.IMREAD_COLOR),
    "vjuh_ok": cv2.imread("patterns/vjuh_ok.png", cv2.IMREAD_COLOR),
    "error2032": cv2.imread("patterns/error2032.png", cv2.IMREAD_COLOR),
    "empty_bag": cv2.imread("patterns/empty_bag.png", cv2.IMREAD_COLOR),
    "null_bag": cv2.imread("patterns/null_bag.png", cv2.IMREAD_COLOR),
    "alm": cv2.imread("patterns/alm.png", cv2.IMREAD_COLOR),
    "alm_osk": cv2.imread("patterns/alm_osk.png", cv2.IMREAD_COLOR),
    "shop_enter": cv2.imread("patterns/shop_enter.png", cv2.IMREAD_COLOR),
    "bank_enter": cv2.imread("patterns/bank_enter.png", cv2.IMREAD_COLOR),
    "door_back": cv2.imread("patterns/door_back.png", cv2.IMREAD_COLOR),
    "door_next": cv2.imread("patterns/door_next.png", cv2.IMREAD_COLOR),
    "door_next2": cv2.imread("patterns/door_next2.png", cv2.IMREAD_COLOR),
    "efir": cv2.imread("patterns/efir.png", cv2.IMREAD_COLOR),
    "efir_use": cv2.imread("patterns/efir_use.png", cv2.IMREAD_COLOR),
    "fight_no": cv2.imread("patterns/fight_no.png", cv2.IMREAD_COLOR),
    "go_away": cv2.imread("patterns/go_away.png", cv2.IMREAD_COLOR),
    "inventar": cv2.imread("patterns/inventar.png", cv2.IMREAD_COLOR),
    "loc_enter": cv2.imread("patterns/loc_enter.png", cv2.IMREAD_COLOR),
    "login_1": cv2.imread("patterns/login_1.png", cv2.IMREAD_COLOR),
    "login_2": cv2.imread("patterns/login_2.png", cv2.IMREAD_COLOR),
    "vip": cv2.imread("patterns/vip.png", cv2.IMREAD_COLOR),
    "you_dead1": cv2.imread("patterns/you_dead1.png", cv2.IMREAD_COLOR),
    "you_dead2": cv2.imread("patterns/you_dead2.png", cv2.IMREAD_COLOR),
    "achievement": cv2.imread("patterns/achievement.png", cv2.IMREAD_COLOR),
    "map_choice": cv2.imread("patterns/map_choice.png", cv2.IMREAD_COLOR),
    "oreh": cv2.imread("patterns/oreh.png", cv2.IMREAD_COLOR),
    "chastica_boj": cv2.imread("patterns/chastica_boj.png", cv2.IMREAD_COLOR),
    "chastica_leg": cv2.imread("patterns/chastica_leg.png", cv2.IMREAD_COLOR),
    "chastica_mif": cv2.imread("patterns/chastica_mif.png", cv2.IMREAD_COLOR),
    "pool_2": cv2.imread("patterns/pool_2.png", cv2.IMREAD_COLOR),
    "boss": cv2.imread("patterns/boss.png", cv2.IMREAD_COLOR),  # Добавляем шаблон босса
    "chest_old": cv2.imread("patterns/chest_old.png", cv2.IMREAD_COLOR),
    "chest_middle": cv2.imread("patterns/chest_middle.png", cv2.IMREAD_COLOR),
    "chest_little": cv2.imread("patterns/chest_little.png", cv2.IMREAD_COLOR),
    "chest_big": cv2.imread("patterns/chest_big.png", cv2.IMREAD_COLOR),
    "chest_carved": cv2.imread("patterns/chest_carved.png", cv2.IMREAD_COLOR),
    "chest_precious": cv2.imread("patterns/chest_precious.png", cv2.IMREAD_COLOR),
    "repair_confirm": cv2.imread("patterns/repair_confirm.png", cv2.IMREAD_COLOR),
    "repair_ok": cv2.imread("patterns/repair_ok.png", cv2.IMREAD_COLOR),
    "repair": cv2.imread("patterns/repair.png", cv2.IMREAD_COLOR),
    "tprune": cv2.imread("patterns/tprune.png", cv2.IMREAD_COLOR),
    "tprune_choice": cv2.imread("patterns/tprune_choice.png", cv2.IMREAD_COLOR),
    "tprune_choice_up": cv2.imread("patterns/tprune_choice_up.png", cv2.IMREAD_COLOR),
    "tprune_choice_down": cv2.imread("patterns/tprune_choice_down.png", cv2.IMREAD_COLOR),
    "tprune_choice_down_end": cv2.imread("patterns/tprune_choice_down_end.png", cv2.IMREAD_COLOR),
    "tprune_go": cv2.imread("patterns/tprune_go.png", cv2.IMREAD_COLOR),
    "tprune_fail": cv2.imread("patterns/tprune_fail.png", cv2.IMREAD_COLOR),

    "tprune_vergeland": cv2.imread("patterns/tprune_vergeland.png", cv2.IMREAD_COLOR),
    "tprune_vergeland1": cv2.imread("patterns/tprune_vergeland1.png", cv2.IMREAD_COLOR),
    "tprune_vergeland2": cv2.imread("patterns/tprune_vergeland2.png", cv2.IMREAD_COLOR),
    "tprune_vergeland3": cv2.imread("patterns/tprune_vergeland3.png", cv2.IMREAD_COLOR),
    "tprune_vergeland4": cv2.imread("patterns/tprune_vergeland4.png", cv2.IMREAD_COLOR),

    "tprune_harangerfjord": cv2.imread("patterns/tprune_harangerfjord.png", cv2.IMREAD_COLOR),
    "tprune_harangerfjord5": cv2.imread("patterns/tprune_harangerfjord5.png", cv2.IMREAD_COLOR),
    "tprune_harangerfjord6": cv2.imread("patterns/tprune_harangerfjord6.png", cv2.IMREAD_COLOR),
    "tprune_harangerfjord7": cv2.imread("patterns/tprune_harangerfjord7.png", cv2.IMREAD_COLOR),
    "tprune_harangerfjord8": cv2.imread("patterns/tprune_harangerfjord8.png", cv2.IMREAD_COLOR),

    "tprune_heimskringla": cv2.imread("patterns/tprune_heimskringla.png", cv2.IMREAD_COLOR),
    "tprune_heimskringla9": cv2.imread("patterns/tprune_heimskringla9.png", cv2.IMREAD_COLOR),
    "tprune_heimskringla10": cv2.imread("patterns/tprune_heimskringla10.png", cv2.IMREAD_COLOR),
    "tprune_heimskringla11": cv2.imread("patterns/tprune_heimskringla11.png", cv2.IMREAD_COLOR),

    "tprune_sorian": cv2.imread("patterns/tprune_sorian.png", cv2.IMREAD_COLOR),
    "tprune_sorian12": cv2.imread("patterns/tprune_sorian12.png", cv2.IMREAD_COLOR),
    "tprune_sorian13": cv2.imread("patterns/tprune_sorian13.png", cv2.IMREAD_COLOR),
    "tprune_sorian14": cv2.imread("patterns/tprune_sorian14.png", cv2.IMREAD_COLOR),
    "tprune_sorian15": cv2.imread("patterns/tprune_sorian15.png", cv2.IMREAD_COLOR),

    "tprune_ortre": cv2.imread("patterns/tprune_ortre.png", cv2.IMREAD_COLOR),
    "tprune_ortre16": cv2.imread("patterns/tprune_ortre16.png", cv2.IMREAD_COLOR),
    "tprune_ortre17": cv2.imread("patterns/tprune_ortre17.png", cv2.IMREAD_COLOR),
    "tprune_ortre18": cv2.imread("patterns/tprune_ortre18.png", cv2.IMREAD_COLOR),

    "tprune_almeric": cv2.imread("patterns/tprune_almeric.png", cv2.IMREAD_COLOR),
    "tprune_almeric19": cv2.imread("patterns/tprune_almeric19.png", cv2.IMREAD_COLOR),
    "tprune_almeric20": cv2.imread("patterns/tprune_almeric20.png", cv2.IMREAD_COLOR),
    "tprune_almeric21": cv2.imread("patterns/tprune_almeric21.png", cv2.IMREAD_COLOR),
    "tprune_almeric22": cv2.imread("patterns/tprune_almeric22.png", cv2.IMREAD_COLOR),

    "tprune_metanoia": cv2.imread("patterns/tprune_metanoia.png", cv2.IMREAD_COLOR),
    "tprune_metanoia23": cv2.imread("patterns/tprune_metanoia23.png", cv2.IMREAD_COLOR),
    "tprune_metanoia24": cv2.imread("patterns/tprune_metanoia24.png", cv2.IMREAD_COLOR),
    "tprune_metanoia25": cv2.imread("patterns/tprune_metanoia25.png", cv2.IMREAD_COLOR),
    "tprune_metanoia26": cv2.imread("patterns/tprune_metanoia26.png", cv2.IMREAD_COLOR),

    "tprune_panfobion": cv2.imread("patterns/tprune_panfobion.png", cv2.IMREAD_COLOR),
    "tprune_panfobion27": cv2.imread("patterns/tprune_panfobion27.png", cv2.IMREAD_COLOR),
    "tprune_panfobion28": cv2.imread("patterns/tprune_panfobion28.png", cv2.IMREAD_COLOR),

    "vergeland": {
        "loc1": cv2.imread("patterns/locations/vergeland/loc1.png", cv2.IMREAD_COLOR),
        "loc2": cv2.imread("patterns/locations/vergeland/loc2.png", cv2.IMREAD_COLOR),
        "loc3": cv2.imread("patterns/locations/vergeland/loc3.png", cv2.IMREAD_COLOR),
        "loc4": cv2.imread("patterns/locations/vergeland/loc4.png", cv2.IMREAD_COLOR),
        "loc5": cv2.imread("patterns/locations/vergeland/loc5.png", cv2.IMREAD_COLOR),
        "loc6": cv2.imread("patterns/locations/vergeland/loc6.png", cv2.IMREAD_COLOR),
        "loc7": cv2.imread("patterns/locations/vergeland/loc7.png", cv2.IMREAD_COLOR),
        "loc8": cv2.imread("patterns/locations/vergeland/loc8.png", cv2.IMREAD_COLOR),
        "loc9": cv2.imread("patterns/locations/vergeland/loc9.png", cv2.IMREAD_COLOR),
        "loc10": cv2.imread("patterns/locations/vergeland/loc10.png", cv2.IMREAD_COLOR),
        "loc11": cv2.imread("patterns/locations/vergeland/loc11.png", cv2.IMREAD_COLOR),
        "loc12": cv2.imread("patterns/locations/vergeland/loc12.png", cv2.IMREAD_COLOR),
        "loc13": cv2.imread("patterns/locations/vergeland/loc13.png", cv2.IMREAD_COLOR),
        "loc14": cv2.imread("patterns/locations/vergeland/loc14.png", cv2.IMREAD_COLOR),
        "loc15": cv2.imread("patterns/locations/vergeland/loc15.png", cv2.IMREAD_COLOR),
        "loc16": cv2.imread("patterns/locations/vergeland/loc16.png", cv2.IMREAD_COLOR),
        "loc17": cv2.imread("patterns/locations/vergeland/loc17.png", cv2.IMREAD_COLOR),
        "loc18": cv2.imread("patterns/locations/vergeland/loc18.png", cv2.IMREAD_COLOR),
        "loc1a": cv2.imread("patterns/locations/vergeland/loc1a.png", cv2.IMREAD_COLOR),
        "loc2a": cv2.imread("patterns/locations/vergeland/loc2a.png", cv2.IMREAD_COLOR),
        "loc3a": cv2.imread("patterns/locations/vergeland/loc3a.png", cv2.IMREAD_COLOR),
        "loc4a": cv2.imread("patterns/locations/vergeland/loc4a.png", cv2.IMREAD_COLOR),
        "loc5a": cv2.imread("patterns/locations/vergeland/loc5a.png", cv2.IMREAD_COLOR),
        "loc6a": cv2.imread("patterns/locations/vergeland/loc6a.png", cv2.IMREAD_COLOR),
        "loc7a": cv2.imread("patterns/locations/vergeland/loc7a.png", cv2.IMREAD_COLOR),
        "loc8a": cv2.imread("patterns/locations/vergeland/loc8a.png", cv2.IMREAD_COLOR),
        "loc9a": cv2.imread("patterns/locations/vergeland/loc9a.png", cv2.IMREAD_COLOR),
        "loc10a": cv2.imread("patterns/locations/vergeland/loc10a.png", cv2.IMREAD_COLOR),
        "loc11a": cv2.imread("patterns/locations/vergeland/loc11a.png", cv2.IMREAD_COLOR),
        "loc12a": cv2.imread("patterns/locations/vergeland/loc12a.png", cv2.IMREAD_COLOR),
        "loc13a": cv2.imread("patterns/locations/vergeland/loc13a.png", cv2.IMREAD_COLOR),
        "loc14a": cv2.imread("patterns/locations/vergeland/loc14a.png", cv2.IMREAD_COLOR),
        "loc15a": cv2.imread("patterns/locations/vergeland/loc15a.png", cv2.IMREAD_COLOR),
        "loc16a": cv2.imread("patterns/locations/vergeland/loc16a.png", cv2.IMREAD_COLOR),
        "loc17a": cv2.imread("patterns/locations/vergeland/loc17a.png", cv2.IMREAD_COLOR),
        "loc18a": cv2.imread("patterns/locations/vergeland/loc18a.png", cv2.IMREAD_COLOR),
    },
    "harangerfjord": {
        "loc1": cv2.imread("patterns/locations/harangerfjord/loc1.png", cv2.IMREAD_COLOR),
        "loc2": cv2.imread("patterns/locations/harangerfjord/loc2.png", cv2.IMREAD_COLOR),
        "loc3": cv2.imread("patterns/locations/harangerfjord/loc3.png", cv2.IMREAD_COLOR),
        "loc4": cv2.imread("patterns/locations/harangerfjord/loc4.png", cv2.IMREAD_COLOR),
        "loc5": cv2.imread("patterns/locations/harangerfjord/loc5.png", cv2.IMREAD_COLOR),
        "loc6": cv2.imread("patterns/locations/harangerfjord/loc6.png", cv2.IMREAD_COLOR),
        "loc7": cv2.imread("patterns/locations/harangerfjord/loc7.png", cv2.IMREAD_COLOR),
        "loc8": cv2.imread("patterns/locations/harangerfjord/loc8.png", cv2.IMREAD_COLOR),
        "loc9": cv2.imread("patterns/locations/harangerfjord/loc9.png", cv2.IMREAD_COLOR),
        "loc10": cv2.imread("patterns/locations/harangerfjord/loc10.png", cv2.IMREAD_COLOR),
        "loc11": cv2.imread("patterns/locations/harangerfjord/loc11.png", cv2.IMREAD_COLOR),
        "loc12": cv2.imread("patterns/locations/harangerfjord/loc12.png", cv2.IMREAD_COLOR),
        "loc13": cv2.imread("patterns/locations/harangerfjord/loc13.png", cv2.IMREAD_COLOR),
        "loc14": cv2.imread("patterns/locations/harangerfjord/loc14.png", cv2.IMREAD_COLOR),
        "loc15": cv2.imread("patterns/locations/harangerfjord/loc15.png", cv2.IMREAD_COLOR),
        "loc16": cv2.imread("patterns/locations/harangerfjord/loc16.png", cv2.IMREAD_COLOR),
        "loc17": cv2.imread("patterns/locations/harangerfjord/loc17.png", cv2.IMREAD_COLOR),
        "loc18": cv2.imread("patterns/locations/harangerfjord/loc18.png", cv2.IMREAD_COLOR),
        "loc19": cv2.imread("patterns/locations/harangerfjord/loc19.png", cv2.IMREAD_COLOR),
        "loc20": cv2.imread("patterns/locations/harangerfjord/loc20.png", cv2.IMREAD_COLOR),
        "loc21": cv2.imread("patterns/locations/harangerfjord/loc21.png", cv2.IMREAD_COLOR),
        "loc22": cv2.imread("patterns/locations/harangerfjord/loc22.png", cv2.IMREAD_COLOR),
        "loc23": cv2.imread("patterns/locations/harangerfjord/loc23.png", cv2.IMREAD_COLOR),
        "loc1a": cv2.imread("patterns/locations/harangerfjord/loc1a.png", cv2.IMREAD_COLOR),
        "loc2a": cv2.imread("patterns/locations/harangerfjord/loc2a.png", cv2.IMREAD_COLOR),
        "loc3a": cv2.imread("patterns/locations/harangerfjord/loc3a.png", cv2.IMREAD_COLOR),
        "loc4a": cv2.imread("patterns/locations/harangerfjord/loc4a.png", cv2.IMREAD_COLOR),
        "loc5a": cv2.imread("patterns/locations/harangerfjord/loc5a.png", cv2.IMREAD_COLOR),
        "loc6a": cv2.imread("patterns/locations/harangerfjord/loc6a.png", cv2.IMREAD_COLOR),
        "loc7a": cv2.imread("patterns/locations/harangerfjord/loc7a.png", cv2.IMREAD_COLOR),
        "loc8a": cv2.imread("patterns/locations/harangerfjord/loc8a.png", cv2.IMREAD_COLOR),
        "loc9a": cv2.imread("patterns/locations/harangerfjord/loc9a.png", cv2.IMREAD_COLOR),
        "loc10a": cv2.imread("patterns/locations/harangerfjord/loc10a.png", cv2.IMREAD_COLOR),
        "loc11a": cv2.imread("patterns/locations/harangerfjord/loc11a.png", cv2.IMREAD_COLOR),
        "loc12a": cv2.imread("patterns/locations/harangerfjord/loc12a.png", cv2.IMREAD_COLOR),
        "loc13a": cv2.imread("patterns/locations/harangerfjord/loc13a.png", cv2.IMREAD_COLOR),
        "loc14a": cv2.imread("patterns/locations/harangerfjord/loc14a.png", cv2.IMREAD_COLOR),
        "loc15a": cv2.imread("patterns/locations/harangerfjord/loc15a.png", cv2.IMREAD_COLOR),
        "loc16a": cv2.imread("patterns/locations/harangerfjord/loc16a.png", cv2.IMREAD_COLOR),
        "loc17a": cv2.imread("patterns/locations/harangerfjord/loc17a.png", cv2.IMREAD_COLOR),
        "loc18a": cv2.imread("patterns/locations/harangerfjord/loc18a.png", cv2.IMREAD_COLOR),
        "loc19a": cv2.imread("patterns/locations/harangerfjord/loc19a.png", cv2.IMREAD_COLOR),
        "loc20a": cv2.imread("patterns/locations/harangerfjord/loc20a.png", cv2.IMREAD_COLOR),
        "loc21a": cv2.imread("patterns/locations/harangerfjord/loc21a.png", cv2.IMREAD_COLOR),
        "loc22a": cv2.imread("patterns/locations/harangerfjord/loc22a.png", cv2.IMREAD_COLOR),
        "loc23a": cv2.imread("patterns/locations/harangerfjord/loc23a.png", cv2.IMREAD_COLOR),
    },
    "heimskringla": {
        "loc1": cv2.imread("patterns/locations/heimskringla/loc1.png", cv2.IMREAD_COLOR),
        "loc2": cv2.imread("patterns/locations/heimskringla/loc2.png", cv2.IMREAD_COLOR),
        "loc3": cv2.imread("patterns/locations/heimskringla/loc3.png", cv2.IMREAD_COLOR),
        "loc4": cv2.imread("patterns/locations/heimskringla/loc4.png", cv2.IMREAD_COLOR),
        "loc5": cv2.imread("patterns/locations/heimskringla/loc5.png", cv2.IMREAD_COLOR),
        "loc6": cv2.imread("patterns/locations/heimskringla/loc6.png", cv2.IMREAD_COLOR),
        "loc7": cv2.imread("patterns/locations/heimskringla/loc7.png", cv2.IMREAD_COLOR),
        "loc8": cv2.imread("patterns/locations/heimskringla/loc8.png", cv2.IMREAD_COLOR),
        "loc9": cv2.imread("patterns/locations/heimskringla/loc9.png", cv2.IMREAD_COLOR),
        "loc10": cv2.imread("patterns/locations/heimskringla/loc10.png", cv2.IMREAD_COLOR),
        "loc11": cv2.imread("patterns/locations/heimskringla/loc11.png", cv2.IMREAD_COLOR),
        "loc12": cv2.imread("patterns/locations/heimskringla/loc12.png", cv2.IMREAD_COLOR),
        "loc13": cv2.imread("patterns/locations/heimskringla/loc13.png", cv2.IMREAD_COLOR),
        "loc14": cv2.imread("patterns/locations/heimskringla/loc14.png", cv2.IMREAD_COLOR),
        "loc15": cv2.imread("patterns/locations/heimskringla/loc15.png", cv2.IMREAD_COLOR),
        "loc16": cv2.imread("patterns/locations/heimskringla/loc16.png", cv2.IMREAD_COLOR),
        "loc17": cv2.imread("patterns/locations/heimskringla/loc17.png", cv2.IMREAD_COLOR),
        "loc18": cv2.imread("patterns/locations/heimskringla/loc18.png", cv2.IMREAD_COLOR),
        "loc19": cv2.imread("patterns/locations/heimskringla/loc19.png", cv2.IMREAD_COLOR),
        "loc20": cv2.imread("patterns/locations/heimskringla/loc20.png", cv2.IMREAD_COLOR),
        "loc21": cv2.imread("patterns/locations/heimskringla/loc21.png", cv2.IMREAD_COLOR),
        "loc22": cv2.imread("patterns/locations/heimskringla/loc22.png", cv2.IMREAD_COLOR),
        "loc23": cv2.imread("patterns/locations/heimskringla/loc23.png", cv2.IMREAD_COLOR),
        "loc1a": cv2.imread("patterns/locations/heimskringla/loc1a.png", cv2.IMREAD_COLOR),
        "loc2a": cv2.imread("patterns/locations/heimskringla/loc2a.png", cv2.IMREAD_COLOR),
        "loc3a": cv2.imread("patterns/locations/heimskringla/loc3a.png", cv2.IMREAD_COLOR),
        "loc4a": cv2.imread("patterns/locations/heimskringla/loc4a.png", cv2.IMREAD_COLOR),
        "loc5a": cv2.imread("patterns/locations/heimskringla/loc5a.png", cv2.IMREAD_COLOR),
        "loc6a": cv2.imread("patterns/locations/heimskringla/loc6a.png", cv2.IMREAD_COLOR),
        "loc7a": cv2.imread("patterns/locations/heimskringla/loc7a.png", cv2.IMREAD_COLOR),
        "loc8a": cv2.imread("patterns/locations/heimskringla/loc8a.png", cv2.IMREAD_COLOR),
        "loc9a": cv2.imread("patterns/locations/heimskringla/loc9a.png", cv2.IMREAD_COLOR),
        "loc10a": cv2.imread("patterns/locations/heimskringla/loc10a.png", cv2.IMREAD_COLOR),
        "loc11a": cv2.imread("patterns/locations/heimskringla/loc11a.png", cv2.IMREAD_COLOR),
        "loc12a": cv2.imread("patterns/locations/heimskringla/loc12a.png", cv2.IMREAD_COLOR),
        "loc13a": cv2.imread("patterns/locations/heimskringla/loc13a.png", cv2.IMREAD_COLOR),
        "loc14a": cv2.imread("patterns/locations/heimskringla/loc14a.png", cv2.IMREAD_COLOR),
        "loc15a": cv2.imread("patterns/locations/heimskringla/loc15a.png", cv2.IMREAD_COLOR),
        "loc16a": cv2.imread("patterns/locations/heimskringla/loc16a.png", cv2.IMREAD_COLOR),
        "loc17a": cv2.imread("patterns/locations/heimskringla/loc17a.png", cv2.IMREAD_COLOR),
        "loc18a": cv2.imread("patterns/locations/heimskringla/loc18a.png", cv2.IMREAD_COLOR),
        "loc19a": cv2.imread("patterns/locations/heimskringla/loc19a.png", cv2.IMREAD_COLOR),
        "loc20a": cv2.imread("patterns/locations/heimskringla/loc20a.png", cv2.IMREAD_COLOR),
        "loc21a": cv2.imread("patterns/locations/heimskringla/loc21a.png", cv2.IMREAD_COLOR),
        "loc22a": cv2.imread("patterns/locations/heimskringla/loc22a.png", cv2.IMREAD_COLOR),
        "loc23a": cv2.imread("patterns/locations/heimskringla/loc23a.png", cv2.IMREAD_COLOR),
    },
    "sorian": {
        "loc1": cv2.imread("patterns/locations/sorian/loc1.png", cv2.IMREAD_COLOR),
        "loc2": cv2.imread("patterns/locations/sorian/loc2.png", cv2.IMREAD_COLOR),
        "loc3": cv2.imread("patterns/locations/sorian/loc3.png", cv2.IMREAD_COLOR),
        "loc4": cv2.imread("patterns/locations/sorian/loc4.png", cv2.IMREAD_COLOR),
        "loc5": cv2.imread("patterns/locations/sorian/loc5.png", cv2.IMREAD_COLOR),
        "loc6": cv2.imread("patterns/locations/sorian/loc6.png", cv2.IMREAD_COLOR),
        "loc7": cv2.imread("patterns/locations/sorian/loc7.png", cv2.IMREAD_COLOR),
        "loc8": cv2.imread("patterns/locations/sorian/loc8.png", cv2.IMREAD_COLOR),
        "loc9": cv2.imread("patterns/locations/sorian/loc9.png", cv2.IMREAD_COLOR),
        "loc10": cv2.imread("patterns/locations/sorian/loc10.png", cv2.IMREAD_COLOR),
        "loc11": cv2.imread("patterns/locations/sorian/loc11.png", cv2.IMREAD_COLOR),
        "loc12": cv2.imread("patterns/locations/sorian/loc12.png", cv2.IMREAD_COLOR),
        "loc13": cv2.imread("patterns/locations/sorian/loc13.png", cv2.IMREAD_COLOR),
        "loc14": cv2.imread("patterns/locations/sorian/loc14.png", cv2.IMREAD_COLOR),
        "loc15": cv2.imread("patterns/locations/sorian/loc15.png", cv2.IMREAD_COLOR),
        "loc16": cv2.imread("patterns/locations/sorian/loc16.png", cv2.IMREAD_COLOR),
        "loc17": cv2.imread("patterns/locations/sorian/loc17.png", cv2.IMREAD_COLOR),
        "loc18": cv2.imread("patterns/locations/sorian/loc18.png", cv2.IMREAD_COLOR),
        "loc19": cv2.imread("patterns/locations/sorian/loc19.png", cv2.IMREAD_COLOR),
        "loc20": cv2.imread("patterns/locations/sorian/loc20.png", cv2.IMREAD_COLOR),
        "loc21": cv2.imread("patterns/locations/sorian/loc21.png", cv2.IMREAD_COLOR),
        "loc22": cv2.imread("patterns/locations/sorian/loc22.png", cv2.IMREAD_COLOR),
        "loc23": cv2.imread("patterns/locations/sorian/loc23.png", cv2.IMREAD_COLOR),
        "loc24": cv2.imread("patterns/locations/sorian/loc24.png", cv2.IMREAD_COLOR),
        "loc25": cv2.imread("patterns/locations/sorian/loc25.png", cv2.IMREAD_COLOR),
        "loc26": cv2.imread("patterns/locations/sorian/loc26.png", cv2.IMREAD_COLOR),
        "loc27": cv2.imread("patterns/locations/sorian/loc27.png", cv2.IMREAD_COLOR),
        "loc28": cv2.imread("patterns/locations/sorian/loc28.png", cv2.IMREAD_COLOR),
        "loc29": cv2.imread("patterns/locations/sorian/loc29.png", cv2.IMREAD_COLOR),
        "loc30": cv2.imread("patterns/locations/sorian/loc30.png", cv2.IMREAD_COLOR),
        "loc31": cv2.imread("patterns/locations/sorian/loc31.png", cv2.IMREAD_COLOR),
        "loc32": cv2.imread("patterns/locations/sorian/loc32.png", cv2.IMREAD_COLOR),
        "loc1a": cv2.imread("patterns/locations/sorian/loc1a.png", cv2.IMREAD_COLOR),
        "loc2a": cv2.imread("patterns/locations/sorian/loc2a.png", cv2.IMREAD_COLOR),
        "loc3a": cv2.imread("patterns/locations/sorian/loc3a.png", cv2.IMREAD_COLOR),
        "loc4a": cv2.imread("patterns/locations/sorian/loc4a.png", cv2.IMREAD_COLOR),
        "loc5a": cv2.imread("patterns/locations/sorian/loc5a.png", cv2.IMREAD_COLOR),
        "loc6a": cv2.imread("patterns/locations/sorian/loc6a.png", cv2.IMREAD_COLOR),
        "loc7a": cv2.imread("patterns/locations/sorian/loc7a.png", cv2.IMREAD_COLOR),
        "loc8a": cv2.imread("patterns/locations/sorian/loc8a.png", cv2.IMREAD_COLOR),
        "loc9a": cv2.imread("patterns/locations/sorian/loc9a.png", cv2.IMREAD_COLOR),
        "loc10a": cv2.imread("patterns/locations/sorian/loc10a.png", cv2.IMREAD_COLOR),
        "loc11a": cv2.imread("patterns/locations/sorian/loc11a.png", cv2.IMREAD_COLOR),
        "loc12a": cv2.imread("patterns/locations/sorian/loc12a.png", cv2.IMREAD_COLOR),
        "loc13a": cv2.imread("patterns/locations/sorian/loc13a.png", cv2.IMREAD_COLOR),
        "loc14a": cv2.imread("patterns/locations/sorian/loc14a.png", cv2.IMREAD_COLOR),
        "loc15a": cv2.imread("patterns/locations/sorian/loc15a.png", cv2.IMREAD_COLOR),
        "loc16a": cv2.imread("patterns/locations/sorian/loc16a.png", cv2.IMREAD_COLOR),
        "loc17a": cv2.imread("patterns/locations/sorian/loc17a.png", cv2.IMREAD_COLOR),
        "loc18a": cv2.imread("patterns/locations/sorian/loc18a.png", cv2.IMREAD_COLOR),
        "loc19a": cv2.imread("patterns/locations/sorian/loc19a.png", cv2.IMREAD_COLOR),
        "loc20a": cv2.imread("patterns/locations/sorian/loc20a.png", cv2.IMREAD_COLOR),
        "loc21a": cv2.imread("patterns/locations/sorian/loc21a.png", cv2.IMREAD_COLOR),
        "loc22a": cv2.imread("patterns/locations/sorian/loc22a.png", cv2.IMREAD_COLOR),
        "loc23a": cv2.imread("patterns/locations/sorian/loc23a.png", cv2.IMREAD_COLOR),
        "loc24a": cv2.imread("patterns/locations/sorian/loc24a.png", cv2.IMREAD_COLOR),
        "loc25a": cv2.imread("patterns/locations/sorian/loc25a.png", cv2.IMREAD_COLOR),
        "loc26a": cv2.imread("patterns/locations/sorian/loc26a.png", cv2.IMREAD_COLOR),
        "loc27a": cv2.imread("patterns/locations/sorian/loc27a.png", cv2.IMREAD_COLOR),
        "loc28a": cv2.imread("patterns/locations/sorian/loc28a.png", cv2.IMREAD_COLOR),
        "loc29a": cv2.imread("patterns/locations/sorian/loc29a.png", cv2.IMREAD_COLOR),
        "loc30a": cv2.imread("patterns/locations/sorian/loc30a.png", cv2.IMREAD_COLOR),
        "loc31a": cv2.imread("patterns/locations/sorian/loc31a.png", cv2.IMREAD_COLOR),
        "loc32a": cv2.imread("patterns/locations/sorian/loc32a.png", cv2.IMREAD_COLOR),
    },
    "ortre": {
        "loc1": cv2.imread("patterns/locations/ortre/loc1.png", cv2.IMREAD_COLOR),
        "loc2": cv2.imread("patterns/locations/ortre/loc2.png", cv2.IMREAD_COLOR),
        "loc3": cv2.imread("patterns/locations/ortre/loc3.png", cv2.IMREAD_COLOR),
        "loc4": cv2.imread("patterns/locations/ortre/loc4.png", cv2.IMREAD_COLOR),
        "loc5": cv2.imread("patterns/locations/ortre/loc5.png", cv2.IMREAD_COLOR),
        "loc6": cv2.imread("patterns/locations/ortre/loc6.png", cv2.IMREAD_COLOR),
        "loc7": cv2.imread("patterns/locations/ortre/loc7.png", cv2.IMREAD_COLOR),
        "loc8": cv2.imread("patterns/locations/ortre/loc8.png", cv2.IMREAD_COLOR),
        "loc9": cv2.imread("patterns/locations/ortre/loc9.png", cv2.IMREAD_COLOR),
        "loc10": cv2.imread("patterns/locations/ortre/loc10.png", cv2.IMREAD_COLOR),
        "loc1a": cv2.imread("patterns/locations/ortre/loc1a.png", cv2.IMREAD_COLOR),
        "loc2a": cv2.imread("patterns/locations/ortre/loc2a.png", cv2.IMREAD_COLOR),
        "loc3a": cv2.imread("patterns/locations/ortre/loc3a.png", cv2.IMREAD_COLOR),
        "loc4a": cv2.imread("patterns/locations/ortre/loc4a.png", cv2.IMREAD_COLOR),
        "loc5a": cv2.imread("patterns/locations/ortre/loc5a.png", cv2.IMREAD_COLOR),
        "loc6a": cv2.imread("patterns/locations/ortre/loc6a.png", cv2.IMREAD_COLOR),
        "loc7a": cv2.imread("patterns/locations/ortre/loc7a.png", cv2.IMREAD_COLOR),
        "loc8a": cv2.imread("patterns/locations/ortre/loc8a.png", cv2.IMREAD_COLOR),
        "loc9a": cv2.imread("patterns/locations/ortre/loc9a.png", cv2.IMREAD_COLOR),
        "loc10a": cv2.imread("patterns/locations/ortre/loc10a.png", cv2.IMREAD_COLOR),
    },
    "almeric": {
        "loc1": cv2.imread("patterns/locations/almeric/loc1.png", cv2.IMREAD_COLOR),
        "loc2": cv2.imread("patterns/locations/almeric/loc2.png", cv2.IMREAD_COLOR),
        "loc3": cv2.imread("patterns/locations/almeric/loc3.png", cv2.IMREAD_COLOR),
        "loc4": cv2.imread("patterns/locations/almeric/loc4.png", cv2.IMREAD_COLOR),
        "loc5": cv2.imread("patterns/locations/almeric/loc5.png", cv2.IMREAD_COLOR),
        "loc6": cv2.imread("patterns/locations/almeric/loc6.png", cv2.IMREAD_COLOR),
        "loc7": cv2.imread("patterns/locations/almeric/loc7.png", cv2.IMREAD_COLOR),
        "loc8": cv2.imread("patterns/locations/almeric/loc8.png", cv2.IMREAD_COLOR),
        "loc9": cv2.imread("patterns/locations/almeric/loc9.png", cv2.IMREAD_COLOR),
        "loc10": cv2.imread("patterns/locations/almeric/loc10.png", cv2.IMREAD_COLOR),
        "loc11": cv2.imread("patterns/locations/almeric/loc11.png", cv2.IMREAD_COLOR),
        "loc12": cv2.imread("patterns/locations/almeric/loc12.png", cv2.IMREAD_COLOR),
        "loc13": cv2.imread("patterns/locations/almeric/loc13.png", cv2.IMREAD_COLOR),
        "loc14": cv2.imread("patterns/locations/almeric/loc14.png", cv2.IMREAD_COLOR),
        "loc15": cv2.imread("patterns/locations/almeric/loc15.png", cv2.IMREAD_COLOR),
        "loc16": cv2.imread("patterns/locations/almeric/loc16.png", cv2.IMREAD_COLOR),
        "loc17": cv2.imread("patterns/locations/almeric/loc17.png", cv2.IMREAD_COLOR),
        "loc1a": cv2.imread("patterns/locations/almeric/loc1a.png", cv2.IMREAD_COLOR),
        "loc2a": cv2.imread("patterns/locations/almeric/loc2a.png", cv2.IMREAD_COLOR),
        "loc3a": cv2.imread("patterns/locations/almeric/loc3a.png", cv2.IMREAD_COLOR),
        "loc4a": cv2.imread("patterns/locations/almeric/loc4a.png", cv2.IMREAD_COLOR),
        "loc5a": cv2.imread("patterns/locations/almeric/loc5a.png", cv2.IMREAD_COLOR),
        "loc6a": cv2.imread("patterns/locations/almeric/loc6a.png", cv2.IMREAD_COLOR),
        "loc7a": cv2.imread("patterns/locations/almeric/loc7a.png", cv2.IMREAD_COLOR),
        "loc8a": cv2.imread("patterns/locations/almeric/loc8a.png", cv2.IMREAD_COLOR),
        "loc9a": cv2.imread("patterns/locations/almeric/loc9a.png", cv2.IMREAD_COLOR),
        "loc10a": cv2.imread("patterns/locations/almeric/loc10a.png", cv2.IMREAD_COLOR),
        "loc11a": cv2.imread("patterns/locations/almeric/loc11a.png", cv2.IMREAD_COLOR),
        "loc12a": cv2.imread("patterns/locations/almeric/loc12a.png", cv2.IMREAD_COLOR),
        "loc13a": cv2.imread("patterns/locations/almeric/loc13a.png", cv2.IMREAD_COLOR),
        "loc14a": cv2.imread("patterns/locations/almeric/loc14a.png", cv2.IMREAD_COLOR),
        "loc15a": cv2.imread("patterns/locations/almeric/loc15a.png", cv2.IMREAD_COLOR),
        "loc16a": cv2.imread("patterns/locations/almeric/loc16a.png", cv2.IMREAD_COLOR),
        "loc17a": cv2.imread("patterns/locations/almeric/loc17a.png", cv2.IMREAD_COLOR),
    },
    "metanoia": {
        "loc1": cv2.imread("patterns/locations/metanoia/loc1.png", cv2.IMREAD_COLOR),
        "loc2": cv2.imread("patterns/locations/metanoia/loc2.png", cv2.IMREAD_COLOR),
        "loc3": cv2.imread("patterns/locations/metanoia/loc3.png", cv2.IMREAD_COLOR),
        "loc4": cv2.imread("patterns/locations/metanoia/loc4.png", cv2.IMREAD_COLOR),
        "loc5": cv2.imread("patterns/locations/metanoia/loc5.png", cv2.IMREAD_COLOR),
        "loc6": cv2.imread("patterns/locations/metanoia/loc6.png", cv2.IMREAD_COLOR),
        "loc7": cv2.imread("patterns/locations/metanoia/loc7.png", cv2.IMREAD_COLOR),
        "loc8": cv2.imread("patterns/locations/metanoia/loc8.png", cv2.IMREAD_COLOR),
        "loc9": cv2.imread("patterns/locations/metanoia/loc9.png", cv2.IMREAD_COLOR),
        "loc10": cv2.imread("patterns/locations/metanoia/loc10.png", cv2.IMREAD_COLOR),
        "loc11": cv2.imread("patterns/locations/metanoia/loc11.png", cv2.IMREAD_COLOR),
        "loc12": cv2.imread("patterns/locations/metanoia/loc12.png", cv2.IMREAD_COLOR),
        "loc13": cv2.imread("patterns/locations/metanoia/loc13.png", cv2.IMREAD_COLOR),
        "loc14": cv2.imread("patterns/locations/metanoia/loc14.png", cv2.IMREAD_COLOR),
        "loc15": cv2.imread("patterns/locations/metanoia/loc15.png", cv2.IMREAD_COLOR),
        "loc16": cv2.imread("patterns/locations/metanoia/loc16.png", cv2.IMREAD_COLOR),
        "loc17": cv2.imread("patterns/locations/metanoia/loc17.png", cv2.IMREAD_COLOR),
        "loc18": cv2.imread("patterns/locations/metanoia/loc18.png", cv2.IMREAD_COLOR),
        "loc19": cv2.imread("patterns/locations/metanoia/loc19.png", cv2.IMREAD_COLOR),
        "loc20": cv2.imread("patterns/locations/metanoia/loc20.png", cv2.IMREAD_COLOR),
        "loc21": cv2.imread("patterns/locations/metanoia/loc21.png", cv2.IMREAD_COLOR),
        "loc1a": cv2.imread("patterns/locations/metanoia/loc1a.png", cv2.IMREAD_COLOR),
        "loc2a": cv2.imread("patterns/locations/metanoia/loc2a.png", cv2.IMREAD_COLOR),
        "loc3a": cv2.imread("patterns/locations/metanoia/loc3a.png", cv2.IMREAD_COLOR),
        "loc4a": cv2.imread("patterns/locations/metanoia/loc4a.png", cv2.IMREAD_COLOR),
        "loc5a": cv2.imread("patterns/locations/metanoia/loc5a.png", cv2.IMREAD_COLOR),
        "loc6a": cv2.imread("patterns/locations/metanoia/loc6a.png", cv2.IMREAD_COLOR),
        "loc7a": cv2.imread("patterns/locations/metanoia/loc7a.png", cv2.IMREAD_COLOR),
        "loc8a": cv2.imread("patterns/locations/metanoia/loc8a.png", cv2.IMREAD_COLOR),
        "loc9a": cv2.imread("patterns/locations/metanoia/loc9a.png", cv2.IMREAD_COLOR),
        "loc10a": cv2.imread("patterns/locations/metanoia/loc10a.png", cv2.IMREAD_COLOR),
        "loc11a": cv2.imread("patterns/locations/metanoia/loc11a.png", cv2.IMREAD_COLOR),
        "loc12a": cv2.imread("patterns/locations/metanoia/loc12a.png", cv2.IMREAD_COLOR),
        "loc13a": cv2.imread("patterns/locations/metanoia/loc13a.png", cv2.IMREAD_COLOR),
        "loc14a": cv2.imread("patterns/locations/metanoia/loc14a.png", cv2.IMREAD_COLOR),
        "loc15a": cv2.imread("patterns/locations/metanoia/loc15a.png", cv2.IMREAD_COLOR),
        "loc16a": cv2.imread("patterns/locations/metanoia/loc16a.png", cv2.IMREAD_COLOR),
        "loc17a": cv2.imread("patterns/locations/metanoia/loc17a.png", cv2.IMREAD_COLOR),
        "loc18a": cv2.imread("patterns/locations/metanoia/loc18a.png", cv2.IMREAD_COLOR),
        "loc19a": cv2.imread("patterns/locations/metanoia/loc19a.png", cv2.IMREAD_COLOR),
        "loc20a": cv2.imread("patterns/locations/metanoia/loc20a.png", cv2.IMREAD_COLOR),
        "loc21a": cv2.imread("patterns/locations/metanoia/loc21a.png", cv2.IMREAD_COLOR),
    },
    "panfobion": {
        "loc1": cv2.imread("patterns/locations/panfobion/loc1.png", cv2.IMREAD_COLOR),
        "loc2": cv2.imread("patterns/locations/panfobion/loc2.png", cv2.IMREAD_COLOR),
        "loc3": cv2.imread("patterns/locations/panfobion/loc3.png", cv2.IMREAD_COLOR),
        "loc4": cv2.imread("patterns/locations/panfobion/loc4.png", cv2.IMREAD_COLOR),
        "loc5": cv2.imread("patterns/locations/panfobion/loc5.png", cv2.IMREAD_COLOR),
        "loc6": cv2.imread("patterns/locations/panfobion/loc6.png", cv2.IMREAD_COLOR),
        "loc7": cv2.imread("patterns/locations/panfobion/loc7.png", cv2.IMREAD_COLOR),
        "loc8": cv2.imread("patterns/locations/panfobion/loc8.png", cv2.IMREAD_COLOR),
        "loc9": cv2.imread("patterns/locations/panfobion/loc9.png", cv2.IMREAD_COLOR),
        "loc10": cv2.imread("patterns/locations/panfobion/loc10.png", cv2.IMREAD_COLOR),
        "loc11": cv2.imread("patterns/locations/panfobion/loc11.png", cv2.IMREAD_COLOR),
        "loc12": cv2.imread("patterns/locations/panfobion/loc12.png", cv2.IMREAD_COLOR),
        "loc13": cv2.imread("patterns/locations/panfobion/loc13.png", cv2.IMREAD_COLOR),
        "loc14": cv2.imread("patterns/locations/panfobion/loc14.png", cv2.IMREAD_COLOR),
        "loc15": cv2.imread("patterns/locations/panfobion/loc15.png", cv2.IMREAD_COLOR),
        "loc16": cv2.imread("patterns/locations/panfobion/loc16.png", cv2.IMREAD_COLOR),
        "loc17": cv2.imread("patterns/locations/panfobion/loc17.png", cv2.IMREAD_COLOR),
        "loc18": cv2.imread("patterns/locations/panfobion/loc18.png", cv2.IMREAD_COLOR),
        "loc19": cv2.imread("patterns/locations/panfobion/loc19.png", cv2.IMREAD_COLOR),
        "loc20": cv2.imread("patterns/locations/panfobion/loc20.png", cv2.IMREAD_COLOR),
        "loc21": cv2.imread("patterns/locations/panfobion/loc21.png", cv2.IMREAD_COLOR),
        "loc1a": cv2.imread("patterns/locations/panfobion/loc1a.png", cv2.IMREAD_COLOR),
        "loc2a": cv2.imread("patterns/locations/panfobion/loc2a.png", cv2.IMREAD_COLOR),
        "loc3a": cv2.imread("patterns/locations/panfobion/loc3a.png", cv2.IMREAD_COLOR),
        "loc4a": cv2.imread("patterns/locations/panfobion/loc4a.png", cv2.IMREAD_COLOR),
        "loc5a": cv2.imread("patterns/locations/panfobion/loc5a.png", cv2.IMREAD_COLOR),
        "loc6a": cv2.imread("patterns/locations/panfobion/loc6a.png", cv2.IMREAD_COLOR),
        "loc7a": cv2.imread("patterns/locations/panfobion/loc7a.png", cv2.IMREAD_COLOR),
        "loc8a": cv2.imread("patterns/locations/panfobion/loc8a.png", cv2.IMREAD_COLOR),
        "loc9a": cv2.imread("patterns/locations/panfobion/loc9a.png", cv2.IMREAD_COLOR),
        "loc10a": cv2.imread("patterns/locations/panfobion/loc10a.png", cv2.IMREAD_COLOR),
        "loc11a": cv2.imread("patterns/locations/panfobion/loc11a.png", cv2.IMREAD_COLOR),
        "loc12a": cv2.imread("patterns/locations/panfobion/loc12a.png", cv2.IMREAD_COLOR),
        "loc13a": cv2.imread("patterns/locations/panfobion/loc13a.png", cv2.IMREAD_COLOR),
        "loc14a": cv2.imread("patterns/locations/panfobion/loc14a.png", cv2.IMREAD_COLOR),
        "loc15a": cv2.imread("patterns/locations/panfobion/loc15a.png", cv2.IMREAD_COLOR),
        "loc16a": cv2.imread("patterns/locations/panfobion/loc16a.png", cv2.IMREAD_COLOR),
        "loc17a": cv2.imread("patterns/locations/panfobion/loc17a.png", cv2.IMREAD_COLOR),
        "loc18a": cv2.imread("patterns/locations/panfobion/loc18a.png", cv2.IMREAD_COLOR),
        "loc19a": cv2.imread("patterns/locations/panfobion/loc19a.png", cv2.IMREAD_COLOR),
        "loc20a": cv2.imread("patterns/locations/panfobion/loc20a.png", cv2.IMREAD_COLOR),
        "loc21a": cv2.imread("patterns/locations/panfobion/loc21a.png", cv2.IMREAD_COLOR),
    },
    "boss": cv2.imread("patterns/boss.png", cv2.IMREAD_COLOR),  # Добавляем паттерн босса
}

STUN_LOCATIONS = {
    "vergeland_loc3", "vergeland_loc6", "vergeland_loc12", "vergeland_loc13",
    "harangerfjord_loc4", "harangerfjord_loc5", "harangerfjord_loc13", "harangerfjord_loc15", "harangerfjord_loc18",
    "heimskringla_loc2", "heimskringla_loc3", "heimskringla_loc5", "heimskringla_loc7", "heimskringla_loc9", "heimskringla_loc11", "heimskringla_loc23",
    "sorian_loc7", "sorian_loc8", "sorian_loc9", "sorian_loc11", "sorian_loc13", "sorian_loc18", "sorian_loc19", "sorian_loc20", "sorian_loc26", "sorian_loc27", "sorian_loc28", "sorian_loc31",
    "almeric_loc6"
}

SLOW_LOCATIONS = {
    "harangerfjord_loc3", "harangerfjord_loc7", "harangerfjord_loc8", "harangerfjord_loc11", "harangerfjord_loc19", "harangerfjord_loc20",
    "heimskringla_loc8", "heimskringla_loc15", "heimskringla_loc21",
    "sorian_loc1", "sorian_loc2", "sorian_loc3", "sorian_loc10", "sorian_loc14", "sorian_loc15", "sorian_loc23",
    "almeric_loc9", "almeric_loc10", "almeric_loc14"
}

EPIC_LOCATIONS = {
    "metanoia_loc4",
    "panfobion_loc20", "panfobion_loc21",
    "almeric_loc9"
}

# После импортов, до начала класса GUI
CHEST_VALUES = {
    "big": {"silver": 30, "copper": 0, "name": "Большой сундук с ресурсами"},
    "carved": {"silver": 45, "copper": 30, "name": "Резной сундук с ресурсами"},
    "little": {"silver": 5, "copper": 60, "name": "Маленький сундук с ресурсами"},
    "middle": {"silver": 10, "copper": 0, "name": "Средний сундук с ресурсами"},
    "old": {"silver": 2, "copper": 40, "name": "Старый сундук с ресурсами"},
    "precious": {"silver": 70, "copper": 0, "name": "Драгоценный сундук с ресурсами"}
}

def find_template(label, gui, threshold=0.85):
    """Ищет шаблон на экране"""
    # Добавляем отладочное логирование
    gui.log_message(f"[DEBUG find_template] Начинаем поиск шаблона '{label}' с порогом {threshold}")
    
    # Если путь содержит информацию о регионе и локации (например "vergeland/loc1")
    if "/" in label:
        region, location = label.split("/")
        if region in PATTERNS and location in PATTERNS[region]:
            template = PATTERNS[region][location]
            gui.log_message(f"[DEBUG find_template] Разбор пути шаблона: регион='{region}', локация='{location}'")
    else:
        # Для обычных шаблонов
        if label not in PATTERNS:
            gui.log_message(f"[DEBUG find_template] Шаблон для {label} не найден в PATTERNS")
            return None
        template = PATTERNS[label]
        gui.log_message(f"[DEBUG find_template] Найден шаблон для {label}")
    
    # Делаем скриншот
    gui.log_message(f"[DEBUG find_template] Делаем скриншот для поиска '{label}'")
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # Специальная обработка для fight_no
    if label == "fight_no":
        gui.log_message("[DEBUG find_template] Используем специальный метод поиска для fight_no")
        result = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        gui.log_message(f"[DEBUG find_template] fight_no: match_value={min_val}, threshold={threshold}")
        if min_val <= threshold:
            x = min_loc[0] + template.shape[1] // 2
            y = min_loc[1] + template.shape[0] // 2
            gui.log_message(f"[DEBUG find_template] Шаблон '{label}' найден в позиции ({x}, {y}) с точностью {min_val}")
            return (x, y)
        else:
            gui.log_message(f"[DEBUG find_template] Шаблон '{label}' НЕ найден (лучшее совпадение: {min_val})")
            return None
    
    # Стандартный метод поиска
    gui.log_message("[DEBUG find_template] Используем стандартный метод поиска")
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    gui.log_message(f"[DEBUG find_template] Стандартный поиск: match_value={max_val}, threshold={threshold}")
    
    if max_val >= threshold:
        x = max_loc[0] + template.shape[1] // 2
        y = max_loc[1] + template.shape[0] // 2
        gui.log_message(f"[DEBUG find_template] Шаблон '{label}' найден в позиции ({x}, {y}) с точностью {max_val}")
        return (x, y)
    else:
        gui.log_message(f"[DEBUG find_template] Шаблон '{label}' НЕ найден (лучшее совпадение: {max_val})")
        return None

def human_click(x, y, double=False):
    """
    Выполняет клик мышью с имитацией человеческого поведения.
    :param x: координата X
    :param y: координата Y
    :param double: выполнить двойной клик
    """
    try:
        # Проверяем, что координаты имеют смысл
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            print(f"[ERROR human_click] Ошибка в координатах клика: x={x}, y={y}")
            return
        
        # Проверяем, что координаты в пределах экрана
        screen_width, screen_height = pyautogui.size()
        if x < 0 or y < 0 or x >= screen_width or y >= screen_height:
            print(f"[ERROR human_click] Координаты клика за пределами экрана: x={x}, y={y}, размер экрана: {screen_width}x{screen_height}")
            return
        
        print(f"[DEBUG human_click] Начинаем клик: x={x}, y={y}, двойной={double}")
        
        print(f"[DEBUG human_click] Перемещаем курсор к x={x}, y={y}")
        pyautogui.moveTo(x, y, duration=0.2)
        time.sleep(0.1)
        
        print(f"[DEBUG human_click] Нажимаем кнопку мыши")
        pyautogui.mouseDown()
        time.sleep(0.1)
        
        print(f"[DEBUG human_click] Отпускаем кнопку мыши")
        pyautogui.mouseUp()
        
        if double:
            print(f"[DEBUG human_click] Выполняем второй клик для double click")
            time.sleep(0.1)
            pyautogui.mouseDown()
            time.sleep(0.1)
            pyautogui.mouseUp()
        
        time.sleep(0.1)
        print(f"[DEBUG human_click] Клик выполнен успешно")
    except Exception as e:
        print(f"[ERROR human_click] Ошибка при клике: {str(e)}")

@contextmanager
def hold_key(key):
    """
    Контекстный менеджер для удержания клавиши.
    :param key: клавиша для удержания
    """
    pyautogui.keyDown(key)
    try:
        yield
    finally:
        pyautogui.keyUp(key)

def mark_location_completed(gui):
    """Отмечает текущую локацию как завершенную и сохраняет это состояние"""
    gui.log_message(f"[DEBUG mark_location_completed] Локация {gui.current_location_key} пройдена")
    gui.completed_locations[gui.current_location_key] = time.time()
    gui.save_location_memory()
    return True

def handle_safe_drop(gui, region_id):
    """
    Обработка сохранного дропа с возвратом к фарму
    """
    try:
        gui.log_message(f"[DEBUG handle_safe_drop] Начинаем обработку safe_drop для региона {region_id}")
        
        # Определяем номер телепорта для каждого региона
        region_teleports = {
            "vergeland": 4, "harangerfjord": 8, "heimskringla": 11,
            "sorian": 15, "ortre": 18, "almeric": 22,
            "metanoia": 26, "panfobion": 28
        }
        
        # Определяем номер региона для магазина/банка
        region_numbers = {
            "vergeland": 1, "harangerfjord": 2, "heimskringla": 3,
            "sorian": 4, "ortre": 5, "almeric": 6,
            "metanoia": 7, "panfobion": 8
        }
        
        # Получаем номер телепорта для текущего региона
        teleport_number = region_teleports.get(region_id)
        if not teleport_number:
            gui.log_message(f"[ERROR handle_safe_drop] Неизвестный регион: {region_id}")
            return False
            
        # Получаем номер региона для магазина/банка
        region_number = region_numbers.get(region_id, 1)
        gui.log_message(f"[DEBUG handle_safe_drop] Определены номера: телепорт={teleport_number}, регион={region_number}")
        
        # Сначала телепортируемся в нужный телепорт
        gui.log_message(f"[DEBUG handle_safe_drop] Телепортируемся в телепорт {teleport_number}")
        teleport(teleport_number, gui)
        time.sleep(2)
        
        # Проверяем успешность телепортации
        pool_2 = find_template("pool_2", gui)
        if not pool_2:
            gui.log_message("[DEBUG handle_safe_drop] Первая попытка телепортации не удалась, пробуем еще раз")
            teleport(teleport_number, gui)
            time.sleep(2)
            pool_2 = find_template("pool_2", gui)
            if not pool_2:
                gui.log_message("[ERROR handle_safe_drop] Телепортация не удалась после двух попыток")
                return False
        
        # После успешной телепортации выполняем PostFarm
        gui.log_message("[DEBUG handle_safe_drop] Телепортация успешна, начинаем PostFarm")
        
        # 1. Ремонт инвентаря
        if gui.running:
            gui.log_message("[DEBUG handle_safe_drop] Шаг 1: Ремонт инвентаря")
            PostFarm.inventory(gui)
            time.sleep(3)
        
        # 2. Продажа предметов
        if gui.running:
            gui.log_message("[DEBUG handle_safe_drop] Шаг 2: Продажа предметов")
            PostFarm.shop(region_number, gui)
            time.sleep(3)
        
        # 3. Сохранение в банк
        if gui.running:
            gui.log_message("[DEBUG handle_safe_drop] Шаг 3: Сохранение в банк")
            PostFarm.bank(region_number, gui)
            time.sleep(3)
        
        # Снимаем фарм с паузы
        gui.farming_paused = False
        gui.log_message("[DEBUG handle_safe_drop] Safe_drop завершен успешно, фарм возобновлен")
        
        return True
    except Exception as e:
        gui.log_message(f"[ERROR handle_safe_drop] Ошибка при обработке safe_drop: {str(e)}")
        gui.farming_paused = False
        return False

def run_location_step(self, region, location_key, map_x_offset, map_y_offset):
    """Выполняет один шаг обработки локации"""
    if not self.gui.running:
        self.scenario_running = False
        return
            
    if self.farming_paused:
        self.log_message("[DEBUG run_location_step] Фарм на паузе, ожидаем...")
        self.after(2000, lambda: self.run_location_step(region, location_key, map_x_offset, map_y_offset))
        return
            
    loc_enter = find_template("loc_enter", self.gui)
    if not loc_enter:
        # Ищем шаблон локации в соответствующем подсловаре PATTERNS
        loc_temp = None
        if region in PATTERNS:
            loc_number = location_key.split('_')[1]
            if loc_number in PATTERNS[region]:
                loc_temp = find_template(f"{region}/{loc_number}", self.gui)
                if not loc_temp and f"{location_key}" in self.completed_locations:
                    self.log_message(f"[DEBUG run_location_step] Локация {location_key} уже пройдена")
                    return True
                    
        map_choice = find_template("map_choice", self.gui)
        # Проверка координат: карта должна быть в правом верхнем углу
        if map_choice:
            x, y = map_choice
            if x < 1200 or y > 100:  # Примерные координаты для миникарты
                self.log_message("[DEBUG run_location_step] Игнорируем ложное срабатывание map_choice (координаты не совпадают)")
                map_choice = None
                
        if not map_choice:
            missclick_enter_loc = find_template("door_back", self.gui)
            if missclick_enter_loc:
                self.log_message(f"[DEBUG run_location_step] Мисскликнули по входу. Вошли в {location_key}.")
                pve(self.gui)  # Вызываем pve напрямую
                return True
        else:
            # Кликаем по карте с учетом позиции map_choice и смещения
            human_click(map_choice[0] + map_x_offset, map_choice[1] + map_y_offset)
            self.log_message(f"[DEBUG run_location_step] Кликаем по карте с оффсетом: x={map_x_offset}, y={map_y_offset}")
            self.after(1000, lambda: self.run_location_step(region, location_key, map_x_offset, map_y_offset))
            return
                
        if not loc_temp:
            self.log_message(f"[DEBUG run_location_step] Не найден шаблон для {location_key}")
            return False
                
        # Нашли шаблон локации - кликаем по нему и ждем появления входа
        self.log_message("[DEBUG run_location_step] Найден основной шаблон локации")
        human_click(*loc_temp)
        # Повторяем клик каждые 3 секунды, пока не появится вход
        self.after(3000, lambda: self.run_location_step(region, location_key, map_x_offset, map_y_offset))
        return
            
    # Нашли кнопку входа
    self.log_message(f"[DEBUG run_location_step] Найдена кнопка входа в локацию {location_key}")
    human_click(*loc_enter)
    time.sleep(3)
    pve(self.gui)  # Вызываем pve напрямую
    return True

def run_location(self, region, location_key, map_x_offset, map_y_offset):
    """Запускает обработку локации через after"""
    # Сохраняем информацию о текущей локации
    self.current_location_key = location_key
    
    # Запускаем первый шаг
    self.run_location_step(region, location_key, map_x_offset, map_y_offset)

def teleport(variant, gui):
    while gui.running:
        if not gui.running:
            break
        tprune_go = find_template("tprune_go", gui)
        if not tprune_go:
            if variant in (1, 2, 3, 4): region_place = find_template(f"tprune_vergeland{variant}", gui)
            if variant in (5, 6, 7, 8): region_place = find_template(f"tprune_harangerfjord{variant}", gui)
            if variant in (9, 10, 11): region_place = find_template(f"tprune_heimskringla{variant}", gui)
            if variant in (12, 13, 14, 15): region_place = find_template(f"tprune_sorian{variant}", gui)
            if variant in (16, 17, 18): region_place = find_template(f"tprune_ortre{variant}", gui)
            if variant in (19, 20, 21, 22): region_place = find_template(f"tprune_almeric{variant}", gui)
            if variant in (23, 24, 25, 26): region_place = find_template(f"tprune_metanoia{variant}", gui)
            if variant in (27, 28): region_place = find_template(f"tprune_panfobion{variant}", gui)
            if not region_place:
                if variant in (1, 2, 3, 4): region = find_template("tprune_vergeland", gui)
                if variant in (5, 6, 7, 8): region = find_template("tprune_harangerfjord", gui)
                if variant in (9, 10, 11): region = find_template("tprune_heimskringla", gui)
                if variant in (12, 13, 14, 15): region = find_template("tprune_sorian", gui)
                if variant in (16, 17, 18): region = find_template("tprune_ortre", gui)
                if variant in (19, 20, 21, 22): region = find_template("tprune_almeric", gui)
                if variant in (23, 24, 25, 26): region = find_template("tprune_metanoia", gui)
                if variant in (27, 28): region = find_template("tprune_panfobion", gui)
                if not region:
                    if variant in (1, 2, 3, 4, 19, 20, 21, 22): tprune_choice_up_down = find_template("tprune_choice_up", gui)
                    if variant in (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 23, 24, 25, 26, 27, 28): tprune_choice_up_down = find_template("tprune_choice_down", gui)
                    if not tprune_choice_up_down:
                        tprune_choice = find_template("tprune_choice", gui)
                        if not tprune_choice:
                            tprune = find_template("tprune", gui)
                            if not tprune:
                                pool_2 = pool_2 = find_template("pool_2", gui)
                                if pool_2:
                                    human_click(*pool_2)
                                else:
                                    pyautogui.moveRel(0, -100, duration=0.2)
                            else:
                                human_click(*tprune)
                        else:
                            human_click(*tprune_choice)
                    else:
                        if variant in (12, 13, 14, 15, 16, 17, 18, 23, 24, 25, 26, 27, 28): 
                            human_click(tprune_choice_up_down[0] - 5, tprune_choice_up_down[1] - 90, double=True)
                            human_click(tprune_choice_up_down[0] - 5, tprune_choice_up_down[1] - 57)
                        else: human_click(*tprune_choice_up_down)
                else:
                    human_click(*region)
            else:
                human_click(*region_place)
        else:
            human_click(*tprune_go)
            time.sleep(2)
            break
    tprune_fail = find_template("tprune_fail", gui)
    if tprune_fail:
        human_click(*tprune_fail)
        return
    else:
        return

class PostFarm:
    @staticmethod
    def inventory(gui):
        """
        Обрабатывает инвентарь: ремонтирует экипировку, использует VIP сундуки и темные кристаллы
        """
        gui.log_message("[DEBUG inventory] Начинаем ремонт экипировки")
        
        # Ремонтируем экипировку
        while gui.running:
            if not gui.running:
                break
            repair_confirm = find_template("repair_confirm", gui) or find_template("repair_ok", gui)
            if not repair_confirm:
                repair = find_template("repair", gui)
                if not repair:
                    inventar = find_template("inventar", gui)
                    if not inventar:
                        fight_no = find_template("fight_no", gui)
                        if not fight_no:
                            pyautogui.moveRel(0, -100, duration=0.2)
                        else:
                            human_click(*fight_no)
                    else:
                        human_click(*inventar)
                else:
                    human_click(*repair)
            else:
                human_click(*repair_confirm)
                break

        # Проверяем настройки использования VIP сундуков и темных кристаллов
        if not gui.use_vip_chests.get() and not gui.use_dark_crystals.get():
            gui.log_message("[DEBUG inventory] Пропускаем проверку сундуков и кристаллов - использование отключено")
            go_away = find_template("go_away", gui)
            if go_away:
                human_click(*go_away)
                time.sleep(0.5)
            return

        gui.log_message("[DEBUG inventory] Проверяем сундуки и кристаллы")
        bag_offsets = [-380, -328, -276, -224]
        
        # Проверяем ВИП сундуки
        if gui.use_vip_chests.get():
            for offset in bag_offsets:
                go_away = find_template("go_away", gui)
                if go_away:
                    human_click(go_away[0] + offset, go_away[1] - 100)
                    time.sleep(0.5)
                    while gui.running:
                        vip = find_template("vip", gui)
                        if vip:
                            human_click(vip[0], vip[1], double=True)
                            time.sleep(0.5)
                            gui.log_message("[DEBUG inventory] Используем VIP сундук")
                        else:
                            break

        # Проверяем темные кристаллы
        if gui.use_dark_crystals.get():
            for offset in bag_offsets:
                go_away = find_template("go_away", gui)
                if go_away:
                    human_click(go_away[0] + offset, go_away[1] - 100)
                    time.sleep(0.5)
                    while gui.running:
                        efir = find_template("efir", gui)
                        efir_use = find_template("efir_use", gui)
                        if efir and not efir_use:
                            human_click(efir[0], efir[1], double=True)
                            time.sleep(0.5)
                            efir_use = find_template("efir_use", gui)
                            if efir_use:
                                human_click(efir_use[0], efir_use[1])
                                time.sleep(0.5)
                                gui.log_message("[DEBUG inventory] Используем темный кристалл")
                        else:
                            break

        # Закрываем инвентарь
        go_away = find_template("go_away", gui)
        if go_away:
            human_click(*go_away)
            time.sleep(0.5)
            gui.log_message("[DEBUG inventory] Закрываем инвентарь")

    @staticmethod
    def shop(variant, gui):
        """Продает предметы в магазине с учетом настроек чекбоксов"""
        BAGS = [(-310, -85), (-258, -85), (-206, -85), (-154, -85)]
        BAG_SLOTS = [
            [(-310, -240), (-258, -240), (-206, -240), (-154, -240), (-102, -240), (-50, -240)],
            [(-310, -187), (-258, -187), (-206, -187), (-154, -187), (-102, -187), (-50, -187)],
            [(-310, -134), (-258, -134), (-206, -134), (-154, -134), (-102, -134), (-50, -134)]
        ]
        
        # Выводим состояние настроек
        print(f"Настройки продажи сундуков:")
        print(f"- sell_resource_chests: {gui.sell_resource_chests.get()}")
        print(f"- use_dark_crystals: {gui.use_dark_crystals.get()}")
        print(f"- use_vip_chests: {gui.use_vip_chests.get()}")
        
        while gui.running:
            if not gui.running:
                break
            go_away = find_template("go_away", gui)
            if not go_away:
                shop_enter = find_template("shop_enter", gui)
                if not shop_enter:
                    if variant == 1: shop = find_template("vergeland_shop", gui) or find_template("vergeland_shopa", gui)
                    if variant == 2: shop = find_template("harangerfjord_shop", gui) or find_template("harangerfjord_shopa", gui)
                    if variant == 3: shop = find_template("heimskringla_shop", gui) or find_template("heimskringla_shopa", gui)
                    if variant == 4: shop = find_template("sorian_shop", gui) or find_template("sorian_shopa", gui)
                    if variant == 5: shop = find_template("ortre_shop", gui) or find_template("ortre_shopa", gui)
                    if variant == 6: shop = find_template("almeric_shop", gui) or find_template("almeric_shopa", gui)
                    if variant == 7: shop = find_template("metanoia_shop", gui) or find_template("metanoia_shopa", gui)
                    if variant == 8: shop = find_template("panfobion_shop", gui) or find_template("panfobion_shopa", gui)
                    if not shop:
                        map_choice = find_template("map_choice", gui)
                        if map_choice:
                            # Сначала кликаем по карте для активации
                            human_click(map_choice[0], map_choice[1])
                            time.sleep(1)  # Даем время на обновление карты
                            
                            # Теперь кликаем по нужной точке
                            if variant == 1: human_click(map_choice[0] -85, map_choice[1] +150)
                            if variant == 2: human_click(map_choice[0] -75, map_choice[1] +128)
                            if variant == 3: human_click(map_choice[0] -145, map_choice[1] +185)
                            if variant == 4: human_click(map_choice[0] -20, map_choice[1] +174)
                            if variant == 5: human_click(map_choice[0] -20, map_choice[1] +171)
                            if variant == 6: human_click(map_choice[0] -112, map_choice[1] +50)
                            if variant == 7: human_click(map_choice[0] -139, map_choice[1] +68)
                            if variant == 8: human_click(map_choice[0] -131, map_choice[1] +166)
                            time.sleep(1)  # Даем время на обновление после клика
                    else:
                        human_click(shop[0], shop[1], double=True)
                        time.sleep(4)
                else:
                    human_click(*shop_enter)
                    time.sleep(4)
            else:
                # В магазине всегда проверяем сумки, но продаем или не продаем предметы в зависимости от настроек
                gui.log_message("Начинаем проверку сумок в магазине")
                
                # Проходим по всем сумкам
                for bag in BAGS:
                    if not gui.running:  # Проверка состояния перед обработкой каждой сумки
                        gui.log_message("Остановка обработки сумок")
                        return
                        
                    # Вычисляем абсолютную координату для BAG
                    bag_abs = (go_away[0] + bag[0], go_away[1] + bag[1])
                    gui.log_message(f"Клик по сумке")
                    human_click(bag_abs[0], bag_abs[1])
                    time.sleep(0.2)  # Пауза после клика по сумке
                    
                    # Проверяем сумку на пустоту
                    print(f"Проверяем сумку {bag} на пустоту...")
                    empty_bag = find_template("empty_bag", gui, threshold=0.75)
                    if empty_bag:
                        gui.log_message("Сумка пустая.")
                        continue  # Переходим к следующей сумке
                    
                    if not gui.running:  # Дополнительная проверка после проверки пустой сумки
                        gui.log_message("Остановка обработки содержимого сумки")
                        return
                        
                    msg = f"Сумка не пустая, начинаем продажу предметов"
                    gui.log_message(msg)
                    print(msg)
                    
                    # ШАГ 1: Делаем скриншот один раз для всех проверок
                    frame = np.array(pyautogui.screenshot())
                    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    
                    # ШАГ 2: Найдем все пустые ячейки на экране заранее
                    all_empty_cells = []
                    null_template = PATTERNS.get("null_bag")
                    if null_template is not None:
                        # Используем matchTemplate для поиска всех пустых ячеек
                        res = cv2.matchTemplate(frame_bgr, null_template, cv2.TM_CCOEFF_NORMED)
                        threshold = 0.7
                        loc = np.where(res >= threshold)
                        for pt in zip(*loc[::-1]):
                            x = pt[0] + null_template.shape[1] // 2
                            y = pt[1] + null_template.shape[0] // 2
                            all_empty_cells.append((x, y))
                            print(f"Найдена пустая ячейка в координатах: ({x}, {y})")
                    
                    print(f"Найдено всего пустых ячеек: {len(all_empty_cells)}")
                    
                    # Для каждого ряда слотов
                    for slot_row in BAG_SLOTS:
                        if not gui.running:  # Проверка состояния перед обработкой каждого ряда
                            gui.log_message("Остановка обработки ряда слотов")
                            return
                            
                        for slot in slot_row:
                            if not gui.running:  # Проверка состояния перед обработкой каждого слота
                                gui.log_message("Остановка обработки слота")
                                return
                                
                            # Вычисляем абсолютную координату для слота
                            slot_abs = (go_away[0] + slot[0], go_away[1] + slot[1])
                            
                            # ШАГ 3: Проверяем, совпадает ли эта ячейка с какой-либо из пустых ячеек
                            is_empty = False
                            for empty_cell in all_empty_cells:
                                if abs(empty_cell[0] - slot_abs[0]) <= 30 and abs(empty_cell[1] - slot_abs[1]) <= 30:
                                    print(f"Слот {slot} пропускаем, т.к. он пустой (координаты пустой ячейки: {empty_cell})")
                                    is_empty = True
                                    break
                            
                            # Если это пустая ячейка - сразу пропускаем без наведения мыши
                            if is_empty:
                                continue
                            
                            if not gui.running:  # Проверка состояния перед проверкой предметов
                                gui.log_message("Остановка проверки предметов")
                                return
                                
                            # ШАГ 4: Проверяем на предметы, которые нельзя продавать
                            
                            # 4.1 Проверка на орехалк (всегда не продаем)
                            oreh = find_template("oreh", gui)
                            if oreh and abs(oreh[0] - slot_abs[0]) <= 30 and abs(oreh[1] - slot_abs[1]) <= 30:
                                print(f"В слоте {slot} найден ореолхалк, пропускаем клик.")
                                continue
                            
                            # 4.2 Проверка на важные предметы (всегда не продаем)
                            exception = find_template("chastica_boj", gui) or find_template("chastica_mif", gui) or find_template("chastica_leg", gui)
                            if exception and abs(exception[0] - slot_abs[0]) <= 30 and abs(exception[1] - slot_abs[1]) <= 30:
                                print(f"В слоте {slot} найден важный предмет, пропускаем клик.")
                                continue
                            
                            if not gui.running:  # Проверка состояния перед проверкой специальных предметов
                                gui.log_message("Остановка проверки специальных предметов")
                                return
                                
                            # 4.3 Проверка на эфир (зависит от настроек)
                            efir = find_template("efir", gui)
                            if efir and not gui.use_dark_crystals.get() and abs(efir[0] - slot_abs[0]) <= 30 and abs(efir[1] - slot_abs[1]) <= 30:
                                print(f"В слоте {slot} найден эфир, пропускаем клик.")
                                continue
                                
                            # 4.4 Проверка на вип-сундуки (зависит от настроек)
                            vip = find_template("vip", gui)
                            if vip and not gui.use_vip_chests.get() and abs(vip[0] - slot_abs[0]) <= 30 and abs(vip[1] - slot_abs[1]) <= 30:
                                print(f"В слоте {slot} найден ВИП сундук, пропускаем клик.")
                                continue
                            
                            if not gui.running:  # Проверка состояния перед проверкой сундуков
                                gui.log_message("Остановка проверки сундуков")
                                return
                                
                            # 4.5 Проверка на сундуки с ресурсами (зависит от настроек)
                            should_sell_chests = gui.sell_resource_chests.get()
                                
                            # Проверяем каждый тип сундука отдельно
                            chest_found = False
                            chest_type = ""
                            
                            chest_types = {
                                "chest_old": "старый сундук",
                                "chest_middle": "средний сундук", 
                                "chest_little": "маленький сундук", 
                                "chest_big": "большой сундук", 
                                "chest_carved": "резной сундук", 
                                "chest_precious": "драгоценный сундук"
                            }
                            
                            # Проверяем каждый тип сундука
                            for chest_key, chest_desc in chest_types.items():
                                if not gui.running:  # Проверка состояния во время проверки сундуков
                                    gui.log_message("Остановка проверки типа сундука")
                                    return
                                    
                                chest = find_template(chest_key, gui)
                                if chest and abs(chest[0] - slot_abs[0]) <= 30 and abs(chest[1] - slot_abs[1]) <= 30:
                                    chest_found = True
                                    chest_type = chest_desc
                                    break  # Нашли сундук, прекращаем проверку других типов
                            
                            # Если нашли сундук и настройки запрещают продажу - пропускаем
                            if chest_found and not should_sell_chests:
                                print(f"В слоте {slot} найден {chest_type}, не продаем по настройкам (sell_resource_chests={should_sell_chests})")
                                continue
                            
                            if not gui.running:  # Финальная проверка перед продажей
                                gui.log_message("Остановка перед продажей предмета")
                                return
                                
                            # 5. Если дошли до этой точки - продаем предмет
                            print(f"Продаем предмет в слоте {slot}")
                            human_click(slot_abs[0], slot_abs[1], double=True)
                    
                    if not gui.running:  # Проверка состояния после обработки всех слотов
                        gui.log_message("Остановка после обработки всех слотов")
                        return
                
                go_away = find_template("go_away", gui)
                if go_away and gui.running:  # Проверяем состояние перед закрытием магазина
                    gui.log_message("Хлам продан")
                    human_click(go_away[0], go_away[1])
                break

    @staticmethod
    def bank(variant, gui):
        """Сохраняет предметы в банк"""
        BAGS = [(-310, -85), (-258, -85), (-206, -85), (-154, -85)]
        BAG_SLOTS = [
            [(-310, -240), (-258, -240), (-206, -240), (-154, -240), (-102, -240), (-50, -240)],
            [(-310, -187), (-258, -187), (-206, -187), (-154, -187), (-102, -187), (-50, -187)],
            [(-310, -134), (-258, -134), (-206, -134), (-154, -134), (-102, -134), (-50, -134)]
        ]
        
        while gui.running:
            if not gui.running:
                break
            go_away = find_template("go_away", gui)
            if not go_away:
                bank_enter = find_template("bank_enter", gui)
                if not bank_enter:
                    if variant == 1: bank = find_template("vergeland_bank", gui) or find_template("vergeland_banka", gui)
                    if variant == 2: bank = find_template("harangerfjord_bank", gui) or find_template("harangerfjord_banka", gui)
                    if variant == 3: bank = find_template("heimskringla_bank", gui) or find_template("heimskringla_banka", gui)
                    if variant == 4: bank = find_template("sorian_bank", gui) or find_template("sorian_banka", gui)
                    if variant == 5: bank = find_template("ortre_bank", gui) or find_template("ortre_banka", gui)
                    if variant == 6: bank = find_template("almeric_bank", gui) or find_template("almeric_banka", gui)
                    if variant == 7: bank = find_template("metanoia_bank", gui) or find_template("metanoia_banka", gui)
                    if variant == 8: bank = find_template("panfobion_bank", gui) or find_template("panfobion_banka", gui)
                    if not bank:
                        map_choice = find_template("map_choice", gui)
                        if map_choice:
                            # Сначала кликаем по карте для активации
                            human_click(map_choice[0], map_choice[1])
                            time.sleep(1)  # Даем время на обновление карты
                            
                            # Теперь кликаем по нужной точке
                            if variant == 1: human_click(map_choice[0] -85, map_choice[1] +150)
                            if variant == 2: human_click(map_choice[0] -75, map_choice[1] +128)
                            if variant == 3: human_click(map_choice[0] -145, map_choice[1] +185)
                            if variant == 4: human_click(map_choice[0] -20, map_choice[1] +174)
                            if variant == 5: human_click(map_choice[0] -20, map_choice[1] +171)
                            if variant == 6: human_click(map_choice[0] -112, map_choice[1] +50)
                            if variant == 7: human_click(map_choice[0] -139, map_choice[1] +68)
                            if variant == 8: human_click(map_choice[0] -131, map_choice[1] +166)
                            time.sleep(1)  # Даем время на обновление после клика
                    else:
                        human_click(bank[0], bank[1], double=True)
                        time.sleep(4)
                else:
                    human_click(*bank_enter)
                    time.sleep(4)
            else:
                # В банке проверяем сумки
                gui.log_message("Начинаем проверку сумок в банке")
                
                # Проходим по всем сумкам
                for bag in BAGS:
                    if not gui.running:
                        return
                        
                    # Вычисляем абсолютную координату для BAG
                    bag_abs = (go_away[0] + bag[0], go_away[1] + bag[1])
                    gui.log_message(f"Клик по сумке")
                    human_click(bag_abs[0], bag_abs[1])
                    time.sleep(0.2)
                    
                    # Проверяем сумку на пустоту
                    empty_bag = find_template("empty_bag", gui, threshold=0.75)
                    if empty_bag:
                        gui.log_message("Сумка пустая.")
                        continue
                    
                    # Для каждого ряда слотов
                    for slot_row in BAG_SLOTS:
                        if not gui.running:
                            return
                            
                        for slot in slot_row:
                            if not gui.running:
                                return
                                
                            # Вычисляем абсолютную координату для слота
                            slot_abs = (go_away[0] + slot[0], go_away[1] + slot[1])
                            
                            # Проверяем только на пустую ячейку
                            null_bag = find_template("null_bag", gui)
                            if null_bag and abs(null_bag[0] - slot_abs[0]) <= 30 and abs(null_bag[1] - slot_abs[1]) <= 30:
                                continue
                            
                            # Все остальные предметы кладем в банк
                            human_click(slot_abs[0], slot_abs[1], double=True)
                
                go_away = find_template("go_away", gui)
                if go_away:
                    gui.log_message("Предметы сохранены в банк")
                    human_click(go_away[0], go_away[1])
                break

    @staticmethod
    def cache_cleaner(gui):
        """Очищает кэш игры и перезапускает клиент"""
        cache_path = os.path.join(os.getenv('APPDATA'), "overkings", "Local Store", "cache")
        overkings_path = r"C:\Program Files (x86)\Overkings\Overkings\Overkings.exe"
        
        if os.path.exists(cache_path):
            gui.log_message("Удаляем файлы кеша...")
            try:
                for item in os.listdir(cache_path):
                    item_path = os.path.join(cache_path, item)
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                gui.log_message("Кеш успешно очищен.")
            except Exception as e:
                gui.log_message(f"[ERROR] Ошибка при удалении кеша: {e}")
        else:
            gui.log_message("[WARNING] Папка кеша не найдена.")
            
        gui.log_message("Завершаем процесс Overkings...")
        subprocess.run(["taskkill", "/F", "/IM", "Overkings.exe"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        
        gui.log_message("Запускаем Overkings...")
        try:
            subprocess.Popen(overkings_path, shell=True,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            gui.log_message("Overkings запущен.")
        except Exception as e:
            gui.log_message(f"[ERROR] Ошибка при запуске Overkings: {e}")

        while gui.running:
            if not gui.running:
                break
            pool_2 = find_template("pool_2", gui)
            if not pool_2:
                login_2 = find_template("login_2", gui)
                if not login_2:
                    login_1 = find_template("login_1", gui)
                    if not login_1:
                        gui.log_message("Overkings еще не загрузился, ждем...")
                        time.sleep(2)
                    else:
                        human_click(*login_1)
                else:
                    human_click(*login_2)
            else:
                gui.log_message("Overkings запущен, кэш очищен успешно!")
                break
        return

class RegionRunner:
    def __init__(self, gui, region_name, locations):
        self.gui = gui
        self.region_name = region_name
        self.locations = locations
        self.current_step = 0
        self.combat_start_time = None
        self.gui.log_message(f"[DEBUG RegionRunner] Инициализация RegionRunner для региона {region_name}")
        self.gui.log_message(f"[DEBUG RegionRunner] Количество шагов в сценарии: {len(locations)}")
        
        # Проверяем память локаций при инициализации
        self.check_region_memory()
        
    def check_region_memory(self):
        """Проверяет память локаций для региона и логирует статистику"""
        completed_count = 0
        total_locations = sum(1 for step in self.locations if "teleport" not in step)
        
        for i, step in enumerate(self.locations):
            if "teleport" in step:
                continue
                
            location_counter = sum(1 for s in self.locations[:i] if "teleport" not in s)
            key = f"{self.region_name.lower()}_loc{location_counter + 1}"
            
            if key in self.gui.completed_locations:
                last_time = self.gui.completed_locations[key]
                time_since = time.time() - last_time
                if time_since < 2 * 3600:  # 2 часа
                    completed_count += 1
                    
        self.gui.log_message(f"[DEBUG check_region_memory] Статистика памяти для {self.region_name}:")
        self.gui.log_message(f"[DEBUG check_region_memory] - Всего локаций: {total_locations}")
        self.gui.log_message(f"[DEBUG check_region_memory] - На откате: {completed_count}")
        self.gui.log_message(f"[DEBUG check_region_memory] - Доступно: {total_locations - completed_count}")
        
    def start(self):
        """Начинает выполнение последовательности шагов"""
        self.gui.log_message(f"[DEBUG start] Запуск сценария {self.region_name}")
        self.gui.scenario_running = True
        self.gui.current_region_key = self.region_name.lower()
        self.gui.current_region_start_time = time.time()
        self.gui.log_message(f"[DEBUG start] Установлены: scenario_running=True, current_region_key={self.gui.current_region_key}")
        
        # Проверяем, есть ли доступные локации
        available_locations = self.get_available_locations()
        if not available_locations:
            self.gui.log_message(f"[DEBUG start] Все локации в {self.region_name} на откате, пропускаем регион")
            self.finish()
            return
            
        self.process_next_step()
        
    def get_available_locations(self):
        """Возвращает список доступных локаций (не на откате)"""
        available = []
        for i, step in enumerate(self.locations):
            if "teleport" in step:
                continue
                
            location_counter = sum(1 for s in self.locations[:i] if "teleport" not in s)
            key = f"{self.region_name.lower()}_loc{location_counter + 1}"
            
            # Проверяем все условия пропуска локации
            if not self.should_skip_location(key):
                available.append(i)
                    
        return available

    def process_next_step(self):
        """Обрабатывает следующий шаг в последовательности"""
        if not self.gui.running:
            self.gui.log_message("[DEBUG process_next_step] Бот остановлен, завершаем сценарий")
            self.finish()
            return
            
        if self.current_step >= len(self.locations):
            self.gui.log_message("[DEBUG process_next_step] Достигнут конец сценария, переходим к завершению")
            self.handle_completion()
            return
            
        step = self.locations[self.current_step]
        self.gui.log_message(f"[DEBUG process_next_step] Обработка шага {self.current_step + 1}/{len(self.locations)}: {step}")
                
        if "teleport" in step:
            variant = step["teleport"]
            self.gui.log_message(f"[DEBUG process_next_step] Шаг телепортации {variant}")
            teleport(variant, self.gui)
            self.current_step += 1
            self.gui.after(2000, self.process_next_step)
            return
            
        location_counter = sum(1 for s in self.locations[:self.current_step] if "teleport" not in s)
        location_counter += 1
        key = f"{self.region_name.lower()}_loc{location_counter}"
        self.gui.log_message(f"[DEBUG process_next_step] Определен ключ локации: {key}")
                
        # Запускаем обработку локации
        self.gui.log_message(f"[DEBUG process_next_step] Начинаем обработку локации {key}")
        self.gui.current_location_key = key
                
        def on_location_complete(result):
            if result:
                self.gui.log_message(f"[DEBUG process_next_step] Локация {key} успешно пройдена")
                self.gui.completed_locations[key] = time.time()
                self.gui.save_location_memory()
                # Обновляем статистику
                self.gui.instances_count_var.set(self.gui.instances_count_var.get() + 1)
                region_key = self.region_name.lower()
                if region_key in self.gui.region_instances_count:
                    new_count = self.gui.region_instances_count[region_key].get() + 1
                    self.gui.region_instances_count[region_key].set(new_count)
                    self.gui.log_message(f"[DEBUG process_next_step] Обновлена статистика региона {region_key}: {new_count} инстансов")
            else:
                self.gui.log_message(f"[DEBUG process_next_step] Локация {key} не пройдена")
            
            self.current_step += 1
            self.gui.after(1000, self.process_next_step)
        
        # Запускаем обработку локации
        self.run_location_step(key, step["x_offset"], step["y_offset"], on_location_complete)
        
    def should_skip_location(self, key):
        """Проверяет, нужно ли пропустить локацию"""
        self.gui.log_message(f"[DEBUG should_skip_location] Проверка условий пропуска для локации {key}")
        
        # Проверка на откат
        if key in self.gui.completed_locations:
            last_time = self.gui.completed_locations[key]
            time_since_completion = time.time() - last_time
            self.gui.log_message(f"[DEBUG should_skip_location] Время с последнего прохождения: {time_since_completion:.1f} секунд")
            if time_since_completion < 2 * 3600:
                self.gui.log_message(f"[DEBUG should_skip_location] {key} пропущена(ОТКАТ)")
                return True
                
        # Проверка на СТАН
        if self.gui.skip_stun_locations.get() and key in STUN_LOCATIONS:
            self.gui.log_message(f"[DEBUG should_skip_location] {key} пропущена(СТАНЯЩАЯ)")
            return True
                
        # Проверка на ЗАМЕДЛЕНИЕ
        if self.gui.skip_slow_locations.get() and key in SLOW_LOCATIONS:
            self.gui.log_message(f"[DEBUG should_skip_location] {key} пропущена(ЗАМЕДЛЯЮЩАЯ)")
            return True

        # Проверка на ЭПИК
        if self.gui.skip_epic_locations.get() and key in EPIC_LOCATIONS:
            self.gui.log_message(f"[DEBUG should_skip_location] {key} пропущена(ЭПИЧЕСКИЙ БОСС)")
            return True

        self.gui.log_message(f"[DEBUG should_skip_location] Локация {key} не подлежит пропуску")
        return False
        
    def run_location_step(self, key, x_offset, y_offset, callback):
        """Выполняет один шаг обработки локации"""
        if not self.gui.running:
            self.gui.log_message("[DEBUG run_location_step] Бот остановлен, прерываем обработку локации")
            return
            
        if self.gui.farming_paused:
            self.gui.log_message("[DEBUG run_location_step] Фарм на паузе, ожидаем...")
            self.gui.after(2000, lambda: self.run_location_step(key, x_offset, y_offset, callback))
            return
            
        # Проверяем память локаций
        if key in self.gui.completed_locations:
            last_time = self.gui.completed_locations[key]
            time_since = time.time() - last_time
            if time_since < 2 * 3600:  # 2 часа
                self.gui.log_message(f"[DEBUG run_location_step] Локация {key} на откате еще {int((2*3600 - time_since)/60)} минут")
                callback(False)
                return
            else:
                self.gui.log_message(f"[DEBUG run_location_step] Локация {key} доступна (откат прошел)")
                
        self.gui.log_message(f"[DEBUG run_location_step] Поиск входа в локацию {key}")
        loc_enter = find_template("loc_enter", self.gui)
        if not loc_enter:
            # Проверяем наличие карты
            map_choice = find_template("map_choice", self.gui)
            # Проверка координат: карта должна быть в правом верхнем углу
            if map_choice:
                x, y = map_choice
                if x < 1200 or y > 100:  # Примерные координаты для миникарты
                    self.gui.log_message("[DEBUG run_location_step] Игнорируем ложное срабатывание map_choice (координаты не совпадают)")
                    map_choice = None
            if not map_choice:
                # Если нет карты, проверяем не вошли ли мы случайно в локацию
                missclick_enter_loc = find_template("door_back", self.gui)
                if missclick_enter_loc:
                    self.gui.log_message(f"[DEBUG run_location_step] Мисскликнули по входу. Вошли в {key}")
                    self.combat_start_time = None
                    self.pve()
                    return
                else:
                    # Если нет ни карты, ни входа в локацию - что-то пошло не так
                    self.gui.log_message(f"[ERROR run_location_step] Не найдена карта для локации {key}")
                    callback(False)
                    return
            # Сначала пробуем кликнуть по карте с оффсетом
            self.gui.log_message(f"[DEBUG run_location_step] Кликаем по карте с оффсетом: x={x_offset}, y={y_offset}")
            human_click(map_choice[0] + x_offset, map_choice[1] + y_offset)
            # Ищем шаблон локации
            region = key.split('_')[0]
            loc_number = key.split('_')[1]
            if region in PATTERNS:
                self.gui.log_message(f"[DEBUG run_location_step] Поиск шаблона для {region}/{loc_number}")
                loc_temp = None
                
                # Пробуем найти основной шаблон
                if loc_number in PATTERNS[region]:
                    loc_temp = find_template(f"{region}/{loc_number}", self.gui)
                    if loc_temp:
                        self.gui.log_message(f"[DEBUG run_location_step] Найден основной шаблон локации")
                        human_click(*loc_temp, double=True)
                        self.gui.after(2500, lambda: self.check_location_state(key, x_offset, y_offset, callback))
                        return
                        
                # Если основной не найден, пробуем альтернативный
                if not loc_temp and f"{loc_number}a" in PATTERNS[region]:
                    loc_temp = find_template(f"{region}/{loc_number}a", self.gui)
                    if loc_temp:
                        self.gui.log_message(f"[DEBUG run_location_step] Найден альтернативный шаблон локации")
                        human_click(*loc_temp, double=True)
                        self.gui.after(2500, lambda: self.check_location_state(key, x_offset, y_offset, callback))
                        return
                
                # Если шаблон не найден после клика по карте
                if not loc_temp:
                    self.gui.log_message(f"[DEBUG run_location_step] Шаблон локации не найден после клика по карте")
                    self.gui.after(1000, lambda: self.run_location_step(key, x_offset, y_offset, callback))
                    return
            else:
                self.gui.log_message(f"[ERROR run_location_step] Регион {region} не найден в PATTERNS")
                callback(False)
                return
        else:
            self.gui.log_message(f"[DEBUG run_location_step] Найден вход в локацию, входим в {key}")
            human_click(*loc_enter)
            self.combat_start_time = None
            self.gui.after(1000, lambda: self.verify_location_entry(key, x_offset, y_offset, callback))
            return True
            
        callback(False)

    def check_location_state(self, key, x_offset, y_offset, callback, attempts=0):
        """Проверяет состояние локации после клика по шаблону"""
        if not self.gui.running:
            return
            
        # Проверяем карту и кликаем по ней с оффсетом для обновления позиции
        map_choice = find_template("map_choice", self.gui)
        if map_choice:
            self.gui.log_message(f"[DEBUG check_location_state] Обновляем позицию на карте (попытка {attempts})")
            human_click(map_choice[0] + x_offset, map_choice[1] + y_offset)
            time.sleep(0.5)  # Даем время на обновление экрана
        
        # Проверяем, появилась ли кнопка входа
        loc_enter = find_template("loc_enter", self.gui)
        if loc_enter:
            self.gui.log_message(f"[DEBUG check_location_state] Найдена кнопка входа в локацию {key}")
            human_click(*loc_enter)
            self.gui.after(2000, lambda: self.verify_location_entry(key, x_offset, y_offset, callback))
            return
            
        # Проверяем, не вошли ли мы случайно в локацию
        door_back = find_template("door_back", self.gui)
        if door_back:
            self.gui.log_message(f"[DEBUG check_location_state] Уже в локации {key}")
            self.combat_start_time = None
            self.pve()
            return
            
        if not map_choice:
            # Если карта пропала - значит мы уже в локации
            self.gui.log_message(f"[DEBUG check_location_state] Карта не видна, возможно уже в локации {key}")
            self.combat_start_time = None
            self.pve()
            return
            
        # Ищем шаблон локации
        region = key.split('_')[0]
        loc_number = key.split('_')[1]
        
        if region in PATTERNS:
            loc_temp = None
            if loc_number in PATTERNS[region]:
                loc_temp = find_template(f"{region}/{loc_number}", self.gui)
            if not loc_temp and f"{loc_number}a" in PATTERNS[region]:
                loc_temp = find_template(f"{region}/{loc_number}a", self.gui)
                
            if loc_temp:
                self.gui.log_message(f"[DEBUG check_location_state] Найден шаблон локации, кликаем")
                human_click(*loc_temp, double=True)
            
        # Продолжаем попытки в любом случае
        self.gui.after(2000, lambda: self.check_location_state(key, x_offset, y_offset, callback, attempts + 1))

    def verify_location_entry(self, key, x_offset, y_offset, callback, verify_attempts=1):
        """Проверяет успешность входа в локацию"""
        if not self.gui.running:
            return
            
        if verify_attempts > 5:  # Максимум 5 попыток (5 секунд)
            self.gui.log_message(f"[ERROR verify_location_entry] Не удалось подтвердить вход в локацию {key}")
            callback(False)
            return
            
        # Проверяем наличие кнопки входа или карты
        door_back = find_template("door_back", self.gui)
        map_choice = find_template("map_choice", self.gui)
        loc_enter = find_template("loc_enter", self.gui)
        
        # Если видим карту в правом верхнем углу - локация не доступна
        if map_choice:
            x, y = map_choice
            if x >= 1200 and y <= 100:
                self.gui.log_message(f"[DEBUG verify_location_entry] Локация {key} не доступна (видна карта)")
                callback(False)
                return
                
        # Если все еще видим вход - значит не вошли
        if loc_enter:
            self.gui.log_message("[DEBUG verify_location_entry] Все еще видим вход, пробуем войти снова...")
            human_click(*loc_enter)
            self.gui.after(1000, lambda: self.verify_location_entry(key, x_offset, y_offset, callback, verify_attempts + 1))
            return
            
        # Если не видим ни карту, ни вход - мы в локации, начинаем бой
        self.gui.log_message(f"[DEBUG verify_location_entry] Вошли в локацию {key}, начинаем бой")
        self.combat_start_time = None
        
        # Начинаем бой
        pool_coords = find_template("pool_2", self.gui)
        if pool_coords:
            self.gui.log_message("[DEBUG verify_location_entry] Бежим в конец локации.")
            with hold_key("alt"):
                human_click(pool_coords[0] - 160, pool_coords[1] - 50)
                time.sleep(1.1)
            # Бежим до конца локации в цикле
            while self.gui.running:
                self.gui.log_message("[DEBUG verify_location_entry] Бежим к концу локации.")
                with hold_key("alt"):
                    human_click(pool_coords[0] - 160, pool_coords[1] - 50)
                    time.sleep(1.1)
                    human_click(pool_coords[0] - 160, pool_coords[1] - 250)
                    
                # Проверяем на засаду
                fight_no = find_template("fight_no", self.gui)
                if not fight_no:
                    self.gui.log_message("[DEBUG verify_location_entry] Обнаружена возможная засада! Отступаем.")
                    door_back = find_template("door_back", self.gui)
                    if door_back:
                        human_click(*door_back)
                    callback(False)
                    return
                    
                # Проверяем, дошли ли до конца локации
                door_next = find_template("door_next", self.gui) or find_template("door_next2", self.gui)
                if door_next:
                    self.gui.log_message("[DEBUG verify_location_entry] Дошли до конца локации!")
                    break
                    
                # Если не дошли - продолжаем бежать
                time.sleep(0.5)
                
            # Проверяем наличие босса
            boss = find_template("boss", self.gui)
            found_boss = boss and self.gui.save_drops.get()
            
            # Начинаем бой
            self.gui.log_message("[DEBUG verify_location_entry] Начинаем бой")
            human_click(*pool_coords)
            self.gui.log_message("[DEBUG verify_location_entry] Призываем сигил.")
            human_click(pool_coords[0] - 170, pool_coords[1])
            
            # Цикл атаки
            while not find_template("fight_no", self.gui):
                if not self.gui.running:
                    break
                    
                you_dead1 = find_template("you_dead1", self.gui)
                achievement = find_template("achievement", self.gui)
                
                if you_dead1 or achievement:
                    break
                    
                human_click(pool_coords[0], pool_coords[1] - 505, double=True)
                self.gui.log_message("[DEBUG verify_location_entry] Атакуем противника.")
                human_click(pool_coords[0] - 530, pool_coords[1])
                self.gui.log_message("[DEBUG verify_location_entry] Используем скиллы.")
                human_click(pool_coords[0] - 470, pool_coords[1])
                time.sleep(0.5)
            
            # Проверяем успешное завершение боя
            if find_template("fight_no", self.gui):
                if found_boss:
                    self.gui.log_message("[DEBUG verify_location_entry] Бой с боссом завершен! Телепортируемся для PostFarm")
                    
                    # Определяем номер телепорта для текущего региона
                    region_teleports = {
                        "vergeland": 4,      # телепорты 1-4
                        "harangerfjord": 8,  # телепорты 5-8
                        "heimskringla": 11,  # телепорты 9-11
                        "sorian": 15,        # телепорты 12-15
                        "ortre": 18,         # телепорты 16-18
                        "almeric": 22,       # телепорты 19-22
                        "metanoia": 26,      # телепорты 23-26
                        "panfobion": 28      # телепорты 27-28
                    }
                    
                    # Получаем номер телепорта для текущего региона
                    region = self.region_name.lower()
                    teleport_number = region_teleports.get(region)
                    if teleport_number:
                        self.gui.log_message(f"[DEBUG verify_location_entry] Телепортируемся в телепорт {teleport_number} для PostFarm")
                        teleport(teleport_number, self.gui)
                        time.sleep(2)
                        
                        # Проверяем успешность телепортации
                        pool_2 = find_template("pool_2", self.gui)
                        if pool_2:
                            self.gui.log_message("[DEBUG verify_location_entry] Телепортация успешна, начинаем PostFarm")
                            self.gui.farming_paused = True
                            self.handle_post_location()
                        else:
                            self.gui.log_message("[DEBUG verify_location_entry] Телепортация не удалась, пробуем еще раз")
                            teleport(teleport_number, self.gui)
                            time.sleep(2)
                            self.gui.farming_paused = True
                            self.handle_post_location()
                    return
                else:
                    door_next = find_template("door_next", self.gui) or find_template("door_next2", self.gui)
                    if door_next:
                        self.gui.log_message("[DEBUG verify_location_entry] Бой завершен, идем через дверь")
                        human_click(*door_next)
            else:
                self.gui.log_message("[DEBUG verify_location_entry] Телепортация не удалась, пробуем еще раз")
                teleport(teleport_number, self.gui)
                time.sleep(2)
                self.gui.farming_paused = True
                self.handle_post_location()
            return
            
        callback(True)  # Сообщаем, что вход успешен

    def handle_next_door(self, door_next):
        """Обрабатывает переход к следующей двери"""
        if not self.gui.running:
            return
            
        achievement = find_template("achievement", self.gui)
        if achievement:
            human_click(*achievement)
            self.gui.after(1000, lambda: self.handle_next_door(door_next))
            return
            
        # Проверяем наличие босса
        boss = find_template("boss", self.gui)
        if boss and self.gui.save_drops.get():
            self.gui.log_message("[DEBUG handle_next_door] Обнаружен босс! Это последний уровень локации.")
            
            # Ставим фарм на паузу
            self.gui.log_message("[DEBUG handle_next_door] Фарм поставлен на паузу для защиты от засад")
            
            # Определяем номер телепорта для текущего региона
            region_teleports = {
                "vergeland": 4,      # телепорты 1-4
                "harangerfjord": 8,  # телепорты 5-8
                "heimskringla": 11,  # телепорты 9-11
                "sorian": 15,        # телепорты 12-15
                "ortre": 18,         # телепорты 16-18
                "almeric": 22,       # телепорты 19-22
                "metanoia": 26,      # телепорты 23-26
                "panfobion": 28      # телепорты 27-28
            }
            
            # Получаем номер телепорта для текущего региона
            teleport_number = region_teleports.get(self.region_name.lower())
            if teleport_number:
                self.gui.log_message(f"[DEBUG handle_next_door] Телепортируемся в телепорт {teleport_number} для PostFarm")
                self.gui.after(2000, lambda: teleport(teleport_number, self.gui))
                self.gui.after(4000, lambda: self.handle_post_location())
            return
            
        # Если босса нет или safe_drops выключен, продолжаем обычное прохождение
        human_click(*door_next)
        self.gui.after(2000, self.pve_combat)

    def handle_post_location(self):
        """Обработка действий после завершения локации"""
        if not self.gui.running:
            return
            
        # Определяем номер региона для магазина/банка
        region_numbers = {
            "vergeland": 1,
            "harangerfjord": 2,
            "heimskringla": 3,
            "sorian": 4,
            "ortre": 5,
            "almeric": 6,
            "metanoia": 7,
            "panfobion": 8
        }
        region_number = region_numbers.get(self.region_name.lower(), 1)
        
        # Выполняем последовательность действий PostFarm
        self.gui.log_message("[DEBUG handle_post_location] Выполняем действия PostFarm")
        PostFarm.inventory(self.gui)  # Ремонт
        self.gui.after(3000, lambda: PostFarm.shop(region_number, self.gui))  # Продажа
        self.gui.after(6000, lambda: PostFarm.bank(region_number, self.gui))  # Банк
        
        # Снимаем фарм с паузы после завершения всех операций
        def resume_farming():
            self.gui.farming_paused = False
            self.gui.log_message("[DEBUG handle_post_location] Фарм возобновлен после PostFarm")
            mark_location_completed(self.gui)  # Отмечаем локацию как завершенную
            
        # Планируем возобновление фарма после завершения всех операций PostFarm
        self.gui.after(9000, resume_farming)

    def handle_safe_drop_teleport(self):
        """Обрабатывает телепортацию для safe_drop"""
        if not self.gui.running:
            return
        
        tprune = find_template("tprune", self.gui)
        if tprune:
            human_click(*tprune)
            self.gui.after(1000, self.handle_safe_drop_start)
            return
        
        self.gui.log_message("[DEBUG handle_safe_drop_teleport] Не удалось найти камень телепортации")
        self.gui.farming_paused = False
        
    def handle_safe_drop_start(self):
        """Начинает обработку safe_drop"""
        if not self.gui.running:
            return
        
        region = self.gui.current_location_key.split('_')[0]
        handle_safe_drop(self.gui, region)

class Regions:
    def __init__(self, gui):
        self.gui = gui
        
    def optimize_route(self, locations, region_name):
        """Оптимизирует маршрут с учетом памяти локаций"""
        optimized = []
        current_teleport = None
        locations_in_current_group = []
        
        for step in locations:
            if "teleport" in step:
                # Если есть накопленные локации, проверяем их
                if locations_in_current_group:
                    available_locations = []
                    for loc in locations_in_current_group:
                        loc_index = len([x for x in optimized if "teleport" not in x]) + len(available_locations) + 1
                        key = f"{region_name.lower()}_loc{loc_index}"
                        
                        if key not in self.gui.completed_locations:
                            available_locations.append(loc)
                        else:
                            last_time = self.gui.completed_locations[key]
                            if time.time() - last_time >= 2 * 3600:  # 2 часа
                                available_locations.append(loc)
                                
                    # Если есть доступные локации в группе, добавляем телепорт и локации
                    if available_locations:
                        if current_teleport:
                            optimized.append(current_teleport)
                        optimized.extend(available_locations)
                        
                # Сохраняем новый телепорт и очищаем группу
                current_teleport = step
                locations_in_current_group = []
            else:
                locations_in_current_group.append(step)
                
        # Обрабатываем последнюю группу
        if locations_in_current_group:
            available_locations = []
            for loc in locations_in_current_group:
                loc_index = len([x for x in optimized if "teleport" not in x]) + len(available_locations) + 1
                key = f"{region_name.lower()}_loc{loc_index}"
                
                if key not in self.gui.completed_locations:
                    available_locations.append(loc)
                else:
                    last_time = self.gui.completed_locations[key]
                    if time.time() - last_time >= 2 * 3600:
                        available_locations.append(loc)
                        
            if available_locations:
                if current_teleport:
                    optimized.append(current_teleport)
                optimized.extend(available_locations)
                
        return optimized

    def vergeland(self):
        locations = [
            {"teleport": 1},
            {"x_offset": -150, "y_offset": 185},  # 1
            {"x_offset": -50,  "y_offset": 160},  # 2
            {"x_offset": -60,  "y_offset": 135},  # 3
            {"x_offset": -20,  "y_offset": 105},  # 4
            {"x_offset": -20,  "y_offset": 125},  # 5
            {"x_offset": -20,  "y_offset": 100},  # 6
            {"x_offset": -20,  "y_offset": 100},  # 7
            {"x_offset": -20,  "y_offset": 100},  # 8
            {"teleport": 2},
            {"x_offset": -20,  "y_offset": 50},   # 9
            {"x_offset": -20,  "y_offset": 50},   # 10
            {"x_offset": -65,  "y_offset": 50},   # 11
            {"x_offset": -65,  "y_offset": 50},   # 12
            {"teleport": 3},
            {"x_offset": -110, "y_offset": 70},   # 13
            {"x_offset": -110, "y_offset": 50},   # 14
            {"x_offset": -140, "y_offset": 75},   # 15
            {"x_offset": -140, "y_offset": 75},   # 16
            {"x_offset": -140, "y_offset": 95},   # 17
            {"x_offset": -140, "y_offset": 125},  # 18
            {"teleport": 4}
        ]
        
        # Оптимизируем маршрут перед запуском
        optimized_locations = self.optimize_route(locations, "Vergeland")
        if not optimized_locations:
            self.gui.log_message("[DEBUG RegionRunner] Все локации Vergeland на откате, пропускаем регион")
            return
            
        runner = RegionRunner(self.gui, "Vergeland", optimized_locations)
        runner.start()

    def harangerfjord(self):
        locations = [
            {"teleport": 5},
            {"x_offset": -20,  "y_offset": 180},  # 1
            {"x_offset": -20,  "y_offset": 157},  # 2
            {"x_offset": -25,  "y_offset": 176},  # 3
            {"x_offset": -61,  "y_offset": 168},  # 4
            {"x_offset": -25,  "y_offset": 145},  # 5
            {"x_offset": -20,  "y_offset": 128},  # 6
            {"x_offset": -42,  "y_offset": 105},  # 7
            {"x_offset": -42,  "y_offset": 105},  # 8
            {"x_offset": -20,  "y_offset": 70},   # 9
            {"x_offset": -20,  "y_offset": 70},   # 10
            {"x_offset": -20,  "y_offset": 50},   # 11
            {"x_offset": -20,  "y_offset": 50},   # 12
            {"x_offset": -75,  "y_offset": 50},   # 13
            {"teleport": 6},
            {"x_offset": -142, "y_offset": 92},   # 14
            {"x_offset": -142, "y_offset": 92},   # 15
            {"x_offset": -141, "y_offset": 52},   # 16
            {"x_offset": -115, "y_offset": 83},   # 17
            {"x_offset": -115, "y_offset": 83},   # 18
            {"x_offset": -97,  "y_offset": 75},   # 19
            {"x_offset": -105, "y_offset": 50},   # 20
            {"x_offset": -115, "y_offset": 122},  # 21
            {"teleport": 7},
            {"x_offset": -138, "y_offset": 165},  # 22
            {"x_offset": -138, "y_offset": 179},  # 23
            {"teleport": 8}
        ]
        
        optimized_locations = self.optimize_route(locations, "Harangerfjord")
        if not optimized_locations:
            self.gui.log_message("[DEBUG] Все локации Harangerfjord на откате, пропускаем регион")
            return
            
        runner = RegionRunner(self.gui, "Harangerfjord", optimized_locations)
        runner.start()

    def heimskringla(self):
        locations = [
            {"teleport": 9},
            {"x_offset": -105, "y_offset": 175},  # 1
            {"x_offset": -105, "y_offset": 175},  # 2
            {"teleport": 10},
            {"x_offset": -45,  "y_offset": 185},  # 3
            {"x_offset": -18,  "y_offset": 171},  # 4
            {"x_offset": -20,  "y_offset": 122},  # 5
            {"x_offset": -20,  "y_offset": 122},  # 6
            {"x_offset": -40,  "y_offset": 118},  # 7
            {"x_offset": -40,  "y_offset": 118},  # 8
            {"x_offset": -43,  "y_offset": 85},   # 9
            {"x_offset": -69,  "y_offset": 100},  # 10
            {"x_offset": -69,  "y_offset": 100},  # 11
            {"x_offset": -20,  "y_offset": 50},   # 12
            {"x_offset": -20,  "y_offset": 50},   # 13
            {"x_offset": -20,  "y_offset": 91},   # 14
            {"x_offset": -20,  "y_offset": 91},   # 15
            {"teleport": 11},
            {"x_offset": -145, "y_offset": 50},   # 16
            {"x_offset": -145, "y_offset": 50},   # 17
            {"x_offset": -105, "y_offset": 76},   # 18
            {"x_offset": -105, "y_offset": 76},   # 19
            {"x_offset": -87,  "y_offset": 96},   # 20
            {"x_offset": -135, "y_offset": 113},  # 21
            {"x_offset": -135, "y_offset": 113},  # 22
            {"x_offset": -140, "y_offset": 79},   # 23
            {"teleport": 9}
        ]
        runner = RegionRunner(self.gui, "Heimskringla", locations)
        runner.start()
import shutil
import tkinter as tk
import tkinter.messagebox as messagebox
import customtkinter
import subprocess
import keyboard
import threading
import time
import cv2
import numpy as np
import pyautogui
import json
import sys
import psutil
import os
from contextlib import contextmanager
import datetime  # Добавлен импорт datetime

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

VERSION = "v1.01"

PATTERNS = {
    "vergeland_bank": cv2.imread("patterns/locations/vergeland/vergeland_bank.png", cv2.IMREAD_COLOR),
    "vergeland_banka": cv2.imread("patterns/locations/vergeland/vergeland_banka.png", cv2.IMREAD_COLOR),
    "vergeland_shop": cv2.imread("patterns/locations/vergeland/vergeland_shop.png", cv2.IMREAD_COLOR),
    "vergeland_shopa": cv2.imread("patterns/locations/vergeland/vergeland_shopa.png", cv2.IMREAD_COLOR),

    "harangerfjord_bank": cv2.imread("patterns/locations/harangerfjord/harangerfjord_bank.png", cv2.IMREAD_COLOR),
    "harangerfjord_banka": cv2.imread("patterns/locations/harangerfjord/harangerfjord_banka.png", cv2.IMREAD_COLOR),
    "harangerfjord_shop": cv2.imread("patterns/locations/harangerfjord/harangerfjord_shop.png", cv2.IMREAD_COLOR),
    "harangerfjord_shopa": cv2.imread("patterns/locations/harangerfjord/harangerfjord_shopa.png", cv2.IMREAD_COLOR),

    "heimskringla_bank": cv2.imread("patterns/locations/heimskringla/heimskringla_bank.png", cv2.IMREAD_COLOR),
    "heimskringla_banka": cv2.imread("patterns/locations/heimskringla/heimskringla_banka.png", cv2.IMREAD_COLOR),
    "heimskringla_shop": cv2.imread("patterns/locations/heimskringla/heimskringla_shop.png", cv2.IMREAD_COLOR),
    "heimskringla_shopa": cv2.imread("patterns/locations/heimskringla/heimskringla_shopa.png", cv2.IMREAD_COLOR),

    "sorian_bank": cv2.imread("patterns/locations/sorian/sorian_bank.png", cv2.IMREAD_COLOR),
    "sorian_banka": cv2.imread("patterns/locations/sorian/sorian_banka.png", cv2.IMREAD_COLOR),
    "sorian_shop": cv2.imread("patterns/locations/sorian/sorian_shop.png", cv2.IMREAD_COLOR),
    "sorian_shopa": cv2.imread("patterns/locations/sorian/sorian_shopa.png", cv2.IMREAD_COLOR),

    "ortre_shop": cv2.imread("patterns/locations/ortre/ortre_shop.png", cv2.IMREAD_COLOR),
    "ortre_shopa": cv2.imread("patterns/locations/ortre/ortre_shopa.png", cv2.IMREAD_COLOR),
    "ortre_bank": cv2.imread("patterns/locations/ortre/ortre_bank.png", cv2.IMREAD_COLOR),
    "ortre_banka": cv2.imread("patterns/locations/ortre/ortre_banka.png", cv2.IMREAD_COLOR),

    "almeric_bank": cv2.imread("patterns/locations/almeric/almeric_bank.png", cv2.IMREAD_COLOR),
    "almeric_banka": cv2.imread("patterns/locations/almeric/almeric_banka.png", cv2.IMREAD_COLOR),
    "almeric_shop": cv2.imread("patterns/locations/almeric/almeric_shop.png", cv2.IMREAD_COLOR),
    "almeric_shopa": cv2.imread("patterns/locations/almeric/almeric_shopa.png", cv2.IMREAD_COLOR),

    "metanoia_bank": cv2.imread("patterns/locations/metanoia/metanoia_bank.png", cv2.IMREAD_COLOR),
    "metanoia_banka": cv2.imread("patterns/locations/metanoia/metanoia_banka.png", cv2.IMREAD_COLOR),
    "metanoia_shop": cv2.imread("patterns/locations/metanoia/metanoia_shop.png", cv2.IMREAD_COLOR),
    "metanoia_shopa": cv2.imread("patterns/locations/metanoia/metanoia_shopa.png", cv2.IMREAD_COLOR),

    "panfobion_bank": cv2.imread("patterns/locations/panfobion/panfobion_bank.png", cv2.IMREAD_COLOR),
    "panfobion_banka": cv2.imread("patterns/locations/panfobion/panfobion_banka.png", cv2.IMREAD_COLOR),
    "panfobion_shop": cv2.imread("patterns/locations/panfobion/panfobion_shop.png", cv2.IMREAD_COLOR),
    "panfobion_shopa": cv2.imread("patterns/locations/panfobion/panfobion_shopa.png", cv2.IMREAD_COLOR),

    "vjuh": cv2.imread("patterns/vjuh.png", cv2.IMREAD_COLOR),
    "vjuh_ok": cv2.imread("patterns/vjuh_ok.png", cv2.IMREAD_COLOR),
    "error2032": cv2.imread("patterns/error2032.png", cv2.IMREAD_COLOR),
    "empty_bag": cv2.imread("patterns/empty_bag.png", cv2.IMREAD_COLOR),
    "null_bag": cv2.imread("patterns/null_bag.png", cv2.IMREAD_COLOR),
    "alm": cv2.imread("patterns/alm.png", cv2.IMREAD_COLOR),
    "alm_osk": cv2.imread("patterns/alm_osk.png", cv2.IMREAD_COLOR),
    "shop_enter": cv2.imread("patterns/shop_enter.png", cv2.IMREAD_COLOR),
    "bank_enter": cv2.imread("patterns/bank_enter.png", cv2.IMREAD_COLOR),
    "door_back": cv2.imread("patterns/door_back.png", cv2.IMREAD_COLOR),
    "door_next": cv2.imread("patterns/door_next.png", cv2.IMREAD_COLOR),
    "door_next2": cv2.imread("patterns/door_next2.png", cv2.IMREAD_COLOR),
    "efir": cv2.imread("patterns/efir.png", cv2.IMREAD_COLOR),
    "efir_use": cv2.imread("patterns/efir_use.png", cv2.IMREAD_COLOR),
    "fight_no": cv2.imread("patterns/fight_no.png", cv2.IMREAD_COLOR),
    "go_away": cv2.imread("patterns/go_away.png", cv2.IMREAD_COLOR),
    "inventar": cv2.imread("patterns/inventar.png", cv2.IMREAD_COLOR),
    "loc_enter": cv2.imread("patterns/loc_enter.png", cv2.IMREAD_COLOR),
    "login_1": cv2.imread("patterns/login_1.png", cv2.IMREAD_COLOR),
    "login_2": cv2.imread("patterns/login_2.png", cv2.IMREAD_COLOR),
    "vip": cv2.imread("patterns/vip.png", cv2.IMREAD_COLOR),
    "you_dead1": cv2.imread("patterns/you_dead1.png", cv2.IMREAD_COLOR),
    "you_dead2": cv2.imread("patterns/you_dead2.png", cv2.IMREAD_COLOR),
    "achievement": cv2.imread("patterns/achievement.png", cv2.IMREAD_COLOR),
    "map_choice": cv2.imread("patterns/map_choice.png", cv2.IMREAD_COLOR),
    "oreh": cv2.imread("patterns/oreh.png", cv2.IMREAD_COLOR),
    "chastica_boj": cv2.imread("patterns/chastica_boj.png", cv2.IMREAD_COLOR),
    "chastica_leg": cv2.imread("patterns/chastica_leg.png", cv2.IMREAD_COLOR),
    "chastica_mif": cv2.imread("patterns/chastica_mif.png", cv2.IMREAD_COLOR),
    "pool_2": cv2.imread("patterns/pool_2.png", cv2.IMREAD_COLOR),
    "boss": cv2.imread("patterns/boss.png", cv2.IMREAD_COLOR),  # Добавляем шаблон босса
    "chest_old": cv2.imread("patterns/chest_old.png", cv2.IMREAD_COLOR),
    "chest_middle": cv2.imread("patterns/chest_middle.png", cv2.IMREAD_COLOR),
    "chest_little": cv2.imread("patterns/chest_little.png", cv2.IMREAD_COLOR),
    "chest_big": cv2.imread("patterns/chest_big.png", cv2.IMREAD_COLOR),
    "chest_carved": cv2.imread("patterns/chest_carved.png", cv2.IMREAD_COLOR),
    "chest_precious": cv2.imread("patterns/chest_precious.png", cv2.IMREAD_COLOR),
    "repair_confirm": cv2.imread("patterns/repair_confirm.png", cv2.IMREAD_COLOR),
    "repair_ok": cv2.imread("patterns/repair_ok.png", cv2.IMREAD_COLOR),
    "repair": cv2.imread("patterns/repair.png", cv2.IMREAD_COLOR),
    "tprune": cv2.imread("patterns/tprune.png", cv2.IMREAD_COLOR),
    "tprune_choice": cv2.imread("patterns/tprune_choice.png", cv2.IMREAD_COLOR),
    "tprune_choice_up": cv2.imread("patterns/tprune_choice_up.png", cv2.IMREAD_COLOR),
    "tprune_choice_down": cv2.imread("patterns/tprune_choice_down.png", cv2.IMREAD_COLOR),
    "tprune_choice_down_end": cv2.imread("patterns/tprune_choice_down_end.png", cv2.IMREAD_COLOR),
    "tprune_go": cv2.imread("patterns/tprune_go.png", cv2.IMREAD_COLOR),
    "tprune_fail": cv2.imread("patterns/tprune_fail.png", cv2.IMREAD_COLOR),

    "tprune_vergeland": cv2.imread("patterns/tprune_vergeland.png", cv2.IMREAD_COLOR),
    "tprune_vergeland1": cv2.imread("patterns/tprune_vergeland1.png", cv2.IMREAD_COLOR),
    "tprune_vergeland2": cv2.imread("patterns/tprune_vergeland2.png", cv2.IMREAD_COLOR),
    "tprune_vergeland3": cv2.imread("patterns/tprune_vergeland3.png", cv2.IMREAD_COLOR),
    "tprune_vergeland4": cv2.imread("patterns/tprune_vergeland4.png", cv2.IMREAD_COLOR),

    "tprune_harangerfjord": cv2.imread("patterns/tprune_harangerfjord.png", cv2.IMREAD_COLOR),
    "tprune_harangerfjord5": cv2.imread("patterns/tprune_harangerfjord5.png", cv2.IMREAD_COLOR),
    "tprune_harangerfjord6": cv2.imread("patterns/tprune_harangerfjord6.png", cv2.IMREAD_COLOR),
    "tprune_harangerfjord7": cv2.imread("patterns/tprune_harangerfjord7.png", cv2.IMREAD_COLOR),
    "tprune_harangerfjord8": cv2.imread("patterns/tprune_harangerfjord8.png", cv2.IMREAD_COLOR),

    "tprune_heimskringla": cv2.imread("patterns/tprune_heimskringla.png", cv2.IMREAD_COLOR),
    "tprune_heimskringla9": cv2.imread("patterns/tprune_heimskringla9.png", cv2.IMREAD_COLOR),
    "tprune_heimskringla10": cv2.imread("patterns/tprune_heimskringla10.png", cv2.IMREAD_COLOR),
    "tprune_heimskringla11": cv2.imread("patterns/tprune_heimskringla11.png", cv2.IMREAD_COLOR),

    "tprune_sorian": cv2.imread("patterns/tprune_sorian.png", cv2.IMREAD_COLOR),
    "tprune_sorian12": cv2.imread("patterns/tprune_sorian12.png", cv2.IMREAD_COLOR),
    "tprune_sorian13": cv2.imread("patterns/tprune_sorian13.png", cv2.IMREAD_COLOR),
    "tprune_sorian14": cv2.imread("patterns/tprune_sorian14.png", cv2.IMREAD_COLOR),
    "tprune_sorian15": cv2.imread("patterns/tprune_sorian15.png", cv2.IMREAD_COLOR),

    "tprune_ortre": cv2.imread("patterns/tprune_ortre.png", cv2.IMREAD_COLOR),
    "tprune_ortre16": cv2.imread("patterns/tprune_ortre16.png", cv2.IMREAD_COLOR),
    "tprune_ortre17": cv2.imread("patterns/tprune_ortre17.png", cv2.IMREAD_COLOR),
    "tprune_ortre18": cv2.imread("patterns/tprune_ortre18.png", cv2.IMREAD_COLOR),

    "tprune_almeric": cv2.imread("patterns/tprune_almeric.png", cv2.IMREAD_COLOR),
    "tprune_almeric19": cv2.imread("patterns/tprune_almeric19.png", cv2.IMREAD_COLOR),
    "tprune_almeric20": cv2.imread("patterns/tprune_almeric20.png", cv2.IMREAD_COLOR),
    "tprune_almeric21": cv2.imread("patterns/tprune_almeric21.png", cv2.IMREAD_COLOR),
    "tprune_almeric22": cv2.imread("patterns/tprune_almeric22.png", cv2.IMREAD_COLOR),

    "tprune_metanoia": cv2.imread("patterns/tprune_metanoia.png", cv2.IMREAD_COLOR),
    "tprune_metanoia23": cv2.imread("patterns/tprune_metanoia23.png", cv2.IMREAD_COLOR),
    "tprune_metanoia24": cv2.imread("patterns/tprune_metanoia24.png", cv2.IMREAD_COLOR),
    "tprune_metanoia25": cv2.imread("patterns/tprune_metanoia25.png", cv2.IMREAD_COLOR),
    "tprune_metanoia26": cv2.imread("patterns/tprune_metanoia26.png", cv2.IMREAD_COLOR),

    "tprune_panfobion": cv2.imread("patterns/tprune_panfobion.png", cv2.IMREAD_COLOR),
    "tprune_panfobion27": cv2.imread("patterns/tprune_panfobion27.png", cv2.IMREAD_COLOR),
    "tprune_panfobion28": cv2.imread("patterns/tprune_panfobion28.png", cv2.IMREAD_COLOR),

    "vergeland": {
        "loc1": cv2.imread("patterns/locations/vergeland/loc1.png", cv2.IMREAD_COLOR),
        "loc2": cv2.imread("patterns/locations/vergeland/loc2.png", cv2.IMREAD_COLOR),
        "loc3": cv2.imread("patterns/locations/vergeland/loc3.png", cv2.IMREAD_COLOR),
        "loc4": cv2.imread("patterns/locations/vergeland/loc4.png", cv2.IMREAD_COLOR),
        "loc5": cv2.imread("patterns/locations/vergeland/loc5.png", cv2.IMREAD_COLOR),
        "loc6": cv2.imread("patterns/locations/vergeland/loc6.png", cv2.IMREAD_COLOR),
        "loc7": cv2.imread("patterns/locations/vergeland/loc7.png", cv2.IMREAD_COLOR),
        "loc8": cv2.imread("patterns/locations/vergeland/loc8.png", cv2.IMREAD_COLOR),
        "loc9": cv2.imread("patterns/locations/vergeland/loc9.png", cv2.IMREAD_COLOR),
        "loc10": cv2.imread("patterns/locations/vergeland/loc10.png", cv2.IMREAD_COLOR),
        "loc11": cv2.imread("patterns/locations/vergeland/loc11.png", cv2.IMREAD_COLOR),
        "loc12": cv2.imread("patterns/locations/vergeland/loc12.png", cv2.IMREAD_COLOR),
        "loc13": cv2.imread("patterns/locations/vergeland/loc13.png", cv2.IMREAD_COLOR),
        "loc14": cv2.imread("patterns/locations/vergeland/loc14.png", cv2.IMREAD_COLOR),
        "loc15": cv2.imread("patterns/locations/vergeland/loc15.png", cv2.IMREAD_COLOR),
        "loc16": cv2.imread("patterns/locations/vergeland/loc16.png", cv2.IMREAD_COLOR),
        "loc17": cv2.imread("patterns/locations/vergeland/loc17.png", cv2.IMREAD_COLOR),
        "loc18": cv2.imread("patterns/locations/vergeland/loc18.png", cv2.IMREAD_COLOR),
        "loc1a": cv2.imread("patterns/locations/vergeland/loc1a.png", cv2.IMREAD_COLOR),
        "loc2a": cv2.imread("patterns/locations/vergeland/loc2a.png", cv2.IMREAD_COLOR),
        "loc3a": cv2.imread("patterns/locations/vergeland/loc3a.png", cv2.IMREAD_COLOR),
        "loc4a": cv2.imread("patterns/locations/vergeland/loc4a.png", cv2.IMREAD_COLOR),
        "loc5a": cv2.imread("patterns/locations/vergeland/loc5a.png", cv2.IMREAD_COLOR),
        "loc6a": cv2.imread("patterns/locations/vergeland/loc6a.png", cv2.IMREAD_COLOR),
        "loc7a": cv2.imread("patterns/locations/vergeland/loc7a.png", cv2.IMREAD_COLOR),
        "loc8a": cv2.imread("patterns/locations/vergeland/loc8a.png", cv2.IMREAD_COLOR),
        "loc9a": cv2.imread("patterns/locations/vergeland/loc9a.png", cv2.IMREAD_COLOR),
        "loc10a": cv2.imread("patterns/locations/vergeland/loc10a.png", cv2.IMREAD_COLOR),
        "loc11a": cv2.imread("patterns/locations/vergeland/loc11a.png", cv2.IMREAD_COLOR),
        "loc12a": cv2.imread("patterns/locations/vergeland/loc12a.png", cv2.IMREAD_COLOR),
        "loc13a": cv2.imread("patterns/locations/vergeland/loc13a.png", cv2.IMREAD_COLOR),
        "loc14a": cv2.imread("patterns/locations/vergeland/loc14a.png", cv2.IMREAD_COLOR),
        "loc15a": cv2.imread("patterns/locations/vergeland/loc15a.png", cv2.IMREAD_COLOR),
        "loc16a": cv2.imread("patterns/locations/vergeland/loc16a.png", cv2.IMREAD_COLOR),
        "loc17a": cv2.imread("patterns/locations/vergeland/loc17a.png", cv2.IMREAD_COLOR),
        "loc18a": cv2.imread("patterns/locations/vergeland/loc18a.png", cv2.IMREAD_COLOR),
    },
    "harangerfjord": {
        "loc1": cv2.imread("patterns/locations/harangerfjord/loc1.png", cv2.IMREAD_COLOR),
        "loc2": cv2.imread("patterns/locations/harangerfjord/loc2.png", cv2.IMREAD_COLOR),
        "loc3": cv2.imread("patterns/locations/harangerfjord/loc3.png", cv2.IMREAD_COLOR),
        "loc4": cv2.imread("patterns/locations/harangerfjord/loc4.png", cv2.IMREAD_COLOR),
        "loc5": cv2.imread("patterns/locations/harangerfjord/loc5.png", cv2.IMREAD_COLOR),
        "loc6": cv2.imread("patterns/locations/harangerfjord/loc6.png", cv2.IMREAD_COLOR),
        "loc7": cv2.imread("patterns/locations/harangerfjord/loc7.png", cv2.IMREAD_COLOR),
        "loc8": cv2.imread("patterns/locations/harangerfjord/loc8.png", cv2.IMREAD_COLOR),
        "loc9": cv2.imread("patterns/locations/harangerfjord/loc9.png", cv2.IMREAD_COLOR),
        "loc10": cv2.imread("patterns/locations/harangerfjord/loc10.png", cv2.IMREAD_COLOR),
        "loc11": cv2.imread("patterns/locations/harangerfjord/loc11.png", cv2.IMREAD_COLOR),
        "loc12": cv2.imread("patterns/locations/harangerfjord/loc12.png", cv2.IMREAD_COLOR),
        "loc13": cv2.imread("patterns/locations/harangerfjord/loc13.png", cv2.IMREAD_COLOR),
        "loc14": cv2.imread("patterns/locations/harangerfjord/loc14.png", cv2.IMREAD_COLOR),
        "loc15": cv2.imread("patterns/locations/harangerfjord/loc15.png", cv2.IMREAD_COLOR),
        "loc16": cv2.imread("patterns/locations/harangerfjord/loc16.png", cv2.IMREAD_COLOR),
        "loc17": cv2.imread("patterns/locations/harangerfjord/loc17.png", cv2.IMREAD_COLOR),
        "loc18": cv2.imread("patterns/locations/harangerfjord/loc18.png", cv2.IMREAD_COLOR),
        "loc19": cv2.imread("patterns/locations/harangerfjord/loc19.png", cv2.IMREAD_COLOR),
        "loc20": cv2.imread("patterns/locations/harangerfjord/loc20.png", cv2.IMREAD_COLOR),
        "loc21": cv2.imread("patterns/locations/harangerfjord/loc21.png", cv2.IMREAD_COLOR),
        "loc22": cv2.imread("patterns/locations/harangerfjord/loc22.png", cv2.IMREAD_COLOR),
        "loc23": cv2.imread("patterns/locations/harangerfjord/loc23.png", cv2.IMREAD_COLOR),
        "loc1a": cv2.imread("patterns/locations/harangerfjord/loc1a.png", cv2.IMREAD_COLOR),
        "loc2a": cv2.imread("patterns/locations/harangerfjord/loc2a.png", cv2.IMREAD_COLOR),
        "loc3a": cv2.imread("patterns/locations/harangerfjord/loc3a.png", cv2.IMREAD_COLOR),
        "loc4a": cv2.imread("patterns/locations/harangerfjord/loc4a.png", cv2.IMREAD_COLOR),
        "loc5a": cv2.imread("patterns/locations/harangerfjord/loc5a.png", cv2.IMREAD_COLOR),
        "loc6a": cv2.imread("patterns/locations/harangerfjord/loc6a.png", cv2.IMREAD_COLOR),
        "loc7a": cv2.imread("patterns/locations/harangerfjord/loc7a.png", cv2.IMREAD_COLOR),
        "loc8a": cv2.imread("patterns/locations/harangerfjord/loc8a.png", cv2.IMREAD_COLOR),
        "loc9a": cv2.imread("patterns/locations/harangerfjord/loc9a.png", cv2.IMREAD_COLOR),
        "loc10a": cv2.imread("patterns/locations/harangerfjord/loc10a.png", cv2.IMREAD_COLOR),
        "loc11a": cv2.imread("patterns/locations/harangerfjord/loc11a.png", cv2.IMREAD_COLOR),
        "loc12a": cv2.imread("patterns/locations/harangerfjord/loc12a.png", cv2.IMREAD_COLOR),
        "loc13a": cv2.imread("patterns/locations/harangerfjord/loc13a.png", cv2.IMREAD_COLOR),
        "loc14a": cv2.imread("patterns/locations/harangerfjord/loc14a.png", cv2.IMREAD_COLOR),
        "loc15a": cv2.imread("patterns/locations/harangerfjord/loc15a.png", cv2.IMREAD_COLOR),
        "loc16a": cv2.imread("patterns/locations/harangerfjord/loc16a.png", cv2.IMREAD_COLOR),
        "loc17a": cv2.imread("patterns/locations/harangerfjord/loc17a.png", cv2.IMREAD_COLOR),
        "loc18a": cv2.imread("patterns/locations/harangerfjord/loc18a.png", cv2.IMREAD_COLOR),
        "loc19a": cv2.imread("patterns/locations/harangerfjord/loc19a.png", cv2.IMREAD_COLOR),
        "loc20a": cv2.imread("patterns/locations/harangerfjord/loc20a.png", cv2.IMREAD_COLOR),
        "loc21a": cv2.imread("patterns/locations/harangerfjord/loc21a.png", cv2.IMREAD_COLOR),
        "loc22a": cv2.imread("patterns/locations/harangerfjord/loc22a.png", cv2.IMREAD_COLOR),
        "loc23a": cv2.imread("patterns/locations/harangerfjord/loc23a.png", cv2.IMREAD_COLOR),
    },
    "heimskringla": {
        "loc1": cv2.imread("patterns/locations/heimskringla/loc1.png", cv2.IMREAD_COLOR),
        "loc2": cv2.imread("patterns/locations/heimskringla/loc2.png", cv2.IMREAD_COLOR),
        "loc3": cv2.imread("patterns/locations/heimskringla/loc3.png", cv2.IMREAD_COLOR),
        "loc4": cv2.imread("patterns/locations/heimskringla/loc4.png", cv2.IMREAD_COLOR),
        "loc5": cv2.imread("patterns/locations/heimskringla/loc5.png", cv2.IMREAD_COLOR),
        "loc6": cv2.imread("patterns/locations/heimskringla/loc6.png", cv2.IMREAD_COLOR),
        "loc7": cv2.imread("patterns/locations/heimskringla/loc7.png", cv2.IMREAD_COLOR),
        "loc8": cv2.imread("patterns/locations/heimskringla/loc8.png", cv2.IMREAD_COLOR),
        "loc9": cv2.imread("patterns/locations/heimskringla/loc9.png", cv2.IMREAD_COLOR),
        "loc10": cv2.imread("patterns/locations/heimskringla/loc10.png", cv2.IMREAD_COLOR),
        "loc11": cv2.imread("patterns/locations/heimskringla/loc11.png", cv2.IMREAD_COLOR),
        "loc12": cv2.imread("patterns/locations/heimskringla/loc12.png", cv2.IMREAD_COLOR),
        "loc13": cv2.imread("patterns/locations/heimskringla/loc13.png", cv2.IMREAD_COLOR),
        "loc14": cv2.imread("patterns/locations/heimskringla/loc14.png", cv2.IMREAD_COLOR),
        "loc15": cv2.imread("patterns/locations/heimskringla/loc15.png", cv2.IMREAD_COLOR),
        "loc16": cv2.imread("patterns/locations/heimskringla/loc16.png", cv2.IMREAD_COLOR),
        "loc17": cv2.imread("patterns/locations/heimskringla/loc17.png", cv2.IMREAD_COLOR),
        "loc18": cv2.imread("patterns/locations/heimskringla/loc18.png", cv2.IMREAD_COLOR),
        "loc19": cv2.imread("patterns/locations/heimskringla/loc19.png", cv2.IMREAD_COLOR),
        "loc20": cv2.imread("patterns/locations/heimskringla/loc20.png", cv2.IMREAD_COLOR),
        "loc21": cv2.imread("patterns/locations/heimskringla/loc21.png", cv2.IMREAD_COLOR),
        "loc22": cv2.imread("patterns/locations/heimskringla/loc22.png", cv2.IMREAD_COLOR),
        "loc23": cv2.imread("patterns/locations/heimskringla/loc23.png", cv2.IMREAD_COLOR),
        "loc1a": cv2.imread("patterns/locations/heimskringla/loc1a.png", cv2.IMREAD_COLOR),
        "loc2a": cv2.imread("patterns/locations/heimskringla/loc2a.png", cv2.IMREAD_COLOR),
        "loc3a": cv2.imread("patterns/locations/heimskringla/loc3a.png", cv2.IMREAD_COLOR),
        "loc4a": cv2.imread("patterns/locations/heimskringla/loc4a.png", cv2.IMREAD_COLOR),
        "loc5a": cv2.imread("patterns/locations/heimskringla/loc5a.png", cv2.IMREAD_COLOR),
        "loc6a": cv2.imread("patterns/locations/heimskringla/loc6a.png", cv2.IMREAD_COLOR),
        "loc7a": cv2.imread("patterns/locations/heimskringla/loc7a.png", cv2.IMREAD_COLOR),
        "loc8a": cv2.imread("patterns/locations/heimskringla/loc8a.png", cv2.IMREAD_COLOR),
        "loc9a": cv2.imread("patterns/locations/heimskringla/loc9a.png", cv2.IMREAD_COLOR),
        "loc10a": cv2.imread("patterns/locations/heimskringla/loc10a.png", cv2.IMREAD_COLOR),
        "loc11a": cv2.imread("patterns/locations/heimskringla/loc11a.png", cv2.IMREAD_COLOR),
        "loc12a": cv2.imread("patterns/locations/heimskringla/loc12a.png", cv2.IMREAD_COLOR),
        "loc13a": cv2.imread("patterns/locations/heimskringla/loc13a.png", cv2.IMREAD_COLOR),
        "loc14a": cv2.imread("patterns/locations/heimskringla/loc14a.png", cv2.IMREAD_COLOR),
        "loc15a": cv2.imread("patterns/locations/heimskringla/loc15a.png", cv2.IMREAD_COLOR),
        "loc16a": cv2.imread("patterns/locations/heimskringla/loc16a.png", cv2.IMREAD_COLOR),
        "loc17a": cv2.imread("patterns/locations/heimskringla/loc17a.png", cv2.IMREAD_COLOR),
        "loc18a": cv2.imread("patterns/locations/heimskringla/loc18a.png", cv2.IMREAD_COLOR),
        "loc19a": cv2.imread("patterns/locations/heimskringla/loc19a.png", cv2.IMREAD_COLOR),
        "loc20a": cv2.imread("patterns/locations/heimskringla/loc20a.png", cv2.IMREAD_COLOR),
        "loc21a": cv2.imread("patterns/locations/heimskringla/loc21a.png", cv2.IMREAD_COLOR),
        "loc22a": cv2.imread("patterns/locations/heimskringla/loc22a.png", cv2.IMREAD_COLOR),
        "loc23a": cv2.imread("patterns/locations/heimskringla/loc23a.png", cv2.IMREAD_COLOR),
    },
    "sorian": {
        "loc1": cv2.imread("patterns/locations/sorian/loc1.png", cv2.IMREAD_COLOR),
        "loc2": cv2.imread("patterns/locations/sorian/loc2.png", cv2.IMREAD_COLOR),
        "loc3": cv2.imread("patterns/locations/sorian/loc3.png", cv2.IMREAD_COLOR),
        "loc4": cv2.imread("patterns/locations/sorian/loc4.png", cv2.IMREAD_COLOR),
        "loc5": cv2.imread("patterns/locations/sorian/loc5.png", cv2.IMREAD_COLOR),
        "loc6": cv2.imread("patterns/locations/sorian/loc6.png", cv2.IMREAD_COLOR),
        "loc7": cv2.imread("patterns/locations/sorian/loc7.png", cv2.IMREAD_COLOR),
        "loc8": cv2.imread("patterns/locations/sorian/loc8.png", cv2.IMREAD_COLOR),
        "loc9": cv2.imread("patterns/locations/sorian/loc9.png", cv2.IMREAD_COLOR),
        "loc10": cv2.imread("patterns/locations/sorian/loc10.png", cv2.IMREAD_COLOR),
        "loc11": cv2.imread("patterns/locations/sorian/loc11.png", cv2.IMREAD_COLOR),
        "loc12": cv2.imread("patterns/locations/sorian/loc12.png", cv2.IMREAD_COLOR),
        "loc13": cv2.imread("patterns/locations/sorian/loc13.png", cv2.IMREAD_COLOR),
        "loc14": cv2.imread("patterns/locations/sorian/loc14.png", cv2.IMREAD_COLOR),
        "loc15": cv2.imread("patterns/locations/sorian/loc15.png", cv2.IMREAD_COLOR),
        "loc16": cv2.imread("patterns/locations/sorian/loc16.png", cv2.IMREAD_COLOR),
        "loc17": cv2.imread("patterns/locations/sorian/loc17.png", cv2.IMREAD_COLOR),
        "loc18": cv2.imread("patterns/locations/sorian/loc18.png", cv2.IMREAD_COLOR),
        "loc19": cv2.imread("patterns/locations/sorian/loc19.png", cv2.IMREAD_COLOR),
        "loc20": cv2.imread("patterns/locations/sorian/loc20.png", cv2.IMREAD_COLOR),
        "loc21": cv2.imread("patterns/locations/sorian/loc21.png", cv2.IMREAD_COLOR),
        "loc22": cv2.imread("patterns/locations/sorian/loc22.png", cv2.IMREAD_COLOR),
        "loc23": cv2.imread("patterns/locations/sorian/loc23.png", cv2.IMREAD_COLOR),
        "loc24": cv2.imread("patterns/locations/sorian/loc24.png", cv2.IMREAD_COLOR),
        "loc25": cv2.imread("patterns/locations/sorian/loc25.png", cv2.IMREAD_COLOR),
        "loc26": cv2.imread("patterns/locations/sorian/loc26.png", cv2.IMREAD_COLOR),
        "loc27": cv2.imread("patterns/locations/sorian/loc27.png", cv2.IMREAD_COLOR),
        "loc28": cv2.imread("patterns/locations/sorian/loc28.png", cv2.IMREAD_COLOR),
        "loc29": cv2.imread("patterns/locations/sorian/loc29.png", cv2.IMREAD_COLOR),
        "loc30": cv2.imread("patterns/locations/sorian/loc30.png", cv2.IMREAD_COLOR),
        "loc31": cv2.imread("patterns/locations/sorian/loc31.png", cv2.IMREAD_COLOR),
        "loc32": cv2.imread("patterns/locations/sorian/loc32.png", cv2.IMREAD_COLOR),
        "loc1a": cv2.imread("patterns/locations/sorian/loc1a.png", cv2.IMREAD_COLOR),
        "loc2a": cv2.imread("patterns/locations/sorian/loc2a.png", cv2.IMREAD_COLOR),
        "loc3a": cv2.imread("patterns/locations/sorian/loc3a.png", cv2.IMREAD_COLOR),
        "loc4a": cv2.imread("patterns/locations/sorian/loc4a.png", cv2.IMREAD_COLOR),
        "loc5a": cv2.imread("patterns/locations/sorian/loc5a.png", cv2.IMREAD_COLOR),
        "loc6a": cv2.imread("patterns/locations/sorian/loc6a.png", cv2.IMREAD_COLOR),
        "loc7a": cv2.imread("patterns/locations/sorian/loc7a.png", cv2.IMREAD_COLOR),
        "loc8a": cv2.imread("patterns/locations/sorian/loc8a.png", cv2.IMREAD_COLOR),
        "loc9a": cv2.imread("patterns/locations/sorian/loc9a.png", cv2.IMREAD_COLOR),
        "loc10a": cv2.imread("patterns/locations/sorian/loc10a.png", cv2.IMREAD_COLOR),
        "loc11a": cv2.imread("patterns/locations/sorian/loc11a.png", cv2.IMREAD_COLOR),
        "loc12a": cv2.imread("patterns/locations/sorian/loc12a.png", cv2.IMREAD_COLOR),
        "loc13a": cv2.imread("patterns/locations/sorian/loc13a.png", cv2.IMREAD_COLOR),
        "loc14a": cv2.imread("patterns/locations/sorian/loc14a.png", cv2.IMREAD_COLOR),
        "loc15a": cv2.imread("patterns/locations/sorian/loc15a.png", cv2.IMREAD_COLOR),
        "loc16a": cv2.imread("patterns/locations/sorian/loc16a.png", cv2.IMREAD_COLOR),
        "loc17a": cv2.imread("patterns/locations/sorian/loc17a.png", cv2.IMREAD_COLOR),
        "loc18a": cv2.imread("patterns/locations/sorian/loc18a.png", cv2.IMREAD_COLOR),
        "loc19a": cv2.imread("patterns/locations/sorian/loc19a.png", cv2.IMREAD_COLOR),
        "loc20a": cv2.imread("patterns/locations/sorian/loc20a.png", cv2.IMREAD_COLOR),
        "loc21a": cv2.imread("patterns/locations/sorian/loc21a.png", cv2.IMREAD_COLOR),
        "loc22a": cv2.imread("patterns/locations/sorian/loc22a.png", cv2.IMREAD_COLOR),
        "loc23a": cv2.imread("patterns/locations/sorian/loc23a.png", cv2.IMREAD_COLOR),
        "loc24a": cv2.imread("patterns/locations/sorian/loc24a.png", cv2.IMREAD_COLOR),
        "loc25a": cv2.imread("patterns/locations/sorian/loc25a.png", cv2.IMREAD_COLOR),
        "loc26a": cv2.imread("patterns/locations/sorian/loc26a.png", cv2.IMREAD_COLOR),
        "loc27a": cv2.imread("patterns/locations/sorian/loc27a.png", cv2.IMREAD_COLOR),
        "loc28a": cv2.imread("patterns/locations/sorian/loc28a.png", cv2.IMREAD_COLOR),
        "loc29a": cv2.imread("patterns/locations/sorian/loc29a.png", cv2.IMREAD_COLOR),
        "loc30a": cv2.imread("patterns/locations/sorian/loc30a.png", cv2.IMREAD_COLOR),
        "loc31a": cv2.imread("patterns/locations/sorian/loc31a.png", cv2.IMREAD_COLOR),
        "loc32a": cv2.imread("patterns/locations/sorian/loc32a.png", cv2.IMREAD_COLOR),
    },
    "ortre": {
        "loc1": cv2.imread("patterns/locations/ortre/loc1.png", cv2.IMREAD_COLOR),
        "loc2": cv2.imread("patterns/locations/ortre/loc2.png", cv2.IMREAD_COLOR),
        "loc3": cv2.imread("patterns/locations/ortre/loc3.png", cv2.IMREAD_COLOR),
        "loc4": cv2.imread("patterns/locations/ortre/loc4.png", cv2.IMREAD_COLOR),
        "loc5": cv2.imread("patterns/locations/ortre/loc5.png", cv2.IMREAD_COLOR),
        "loc6": cv2.imread("patterns/locations/ortre/loc6.png", cv2.IMREAD_COLOR),
        "loc7": cv2.imread("patterns/locations/ortre/loc7.png", cv2.IMREAD_COLOR),
        "loc8": cv2.imread("patterns/locations/ortre/loc8.png", cv2.IMREAD_COLOR),
        "loc9": cv2.imread("patterns/locations/ortre/loc9.png", cv2.IMREAD_COLOR),
        "loc10": cv2.imread("patterns/locations/ortre/loc10.png", cv2.IMREAD_COLOR),
        "loc1a": cv2.imread("patterns/locations/ortre/loc1a.png", cv2.IMREAD_COLOR),
        "loc2a": cv2.imread("patterns/locations/ortre/loc2a.png", cv2.IMREAD_COLOR),
        "loc3a": cv2.imread("patterns/locations/ortre/loc3a.png", cv2.IMREAD_COLOR),
        "loc4a": cv2.imread("patterns/locations/ortre/loc4a.png", cv2.IMREAD_COLOR),
        "loc5a": cv2.imread("patterns/locations/ortre/loc5a.png", cv2.IMREAD_COLOR),
        "loc6a": cv2.imread("patterns/locations/ortre/loc6a.png", cv2.IMREAD_COLOR),
        "loc7a": cv2.imread("patterns/locations/ortre/loc7a.png", cv2.IMREAD_COLOR),
        "loc8a": cv2.imread("patterns/locations/ortre/loc8a.png", cv2.IMREAD_COLOR),
        "loc9a": cv2.imread("patterns/locations/ortre/loc9a.png", cv2.IMREAD_COLOR),
        "loc10a": cv2.imread("patterns/locations/ortre/loc10a.png", cv2.IMREAD_COLOR),
    },
    "almeric": {
        "loc1": cv2.imread("patterns/locations/almeric/loc1.png", cv2.IMREAD_COLOR),
        "loc2": cv2.imread("patterns/locations/almeric/loc2.png", cv2.IMREAD_COLOR),
        "loc3": cv2.imread("patterns/locations/almeric/loc3.png", cv2.IMREAD_COLOR),
        "loc4": cv2.imread("patterns/locations/almeric/loc4.png", cv2.IMREAD_COLOR),
        "loc5": cv2.imread("patterns/locations/almeric/loc5.png", cv2.IMREAD_COLOR),
        "loc6": cv2.imread("patterns/locations/almeric/loc6.png", cv2.IMREAD_COLOR),
        "loc7": cv2.imread("patterns/locations/almeric/loc7.png", cv2.IMREAD_COLOR),
        "loc8": cv2.imread("patterns/locations/almeric/loc8.png", cv2.IMREAD_COLOR),
        "loc9": cv2.imread("patterns/locations/almeric/loc9.png", cv2.IMREAD_COLOR),
        "loc10": cv2.imread("patterns/locations/almeric/loc10.png", cv2.IMREAD_COLOR),
        "loc11": cv2.imread("patterns/locations/almeric/loc11.png", cv2.IMREAD_COLOR),
        "loc12": cv2.imread("patterns/locations/almeric/loc12.png", cv2.IMREAD_COLOR),
        "loc13": cv2.imread("patterns/locations/almeric/loc13.png", cv2.IMREAD_COLOR),
        "loc14": cv2.imread("patterns/locations/almeric/loc14.png", cv2.IMREAD_COLOR),
        "loc15": cv2.imread("patterns/locations/almeric/loc15.png", cv2.IMREAD_COLOR),
        "loc16": cv2.imread("patterns/locations/almeric/loc16.png", cv2.IMREAD_COLOR),
        "loc17": cv2.imread("patterns/locations/almeric/loc17.png", cv2.IMREAD_COLOR),
        "loc1a": cv2.imread("patterns/locations/almeric/loc1a.png", cv2.IMREAD_COLOR),
        "loc2a": cv2.imread("patterns/locations/almeric/loc2a.png", cv2.IMREAD_COLOR),
        "loc3a": cv2.imread("patterns/locations/almeric/loc3a.png", cv2.IMREAD_COLOR),
        "loc4a": cv2.imread("patterns/locations/almeric/loc4a.png", cv2.IMREAD_COLOR),
        "loc5a": cv2.imread("patterns/locations/almeric/loc5a.png", cv2.IMREAD_COLOR),
        "loc6a": cv2.imread("patterns/locations/almeric/loc6a.png", cv2.IMREAD_COLOR),
        "loc7a": cv2.imread("patterns/locations/almeric/loc7a.png", cv2.IMREAD_COLOR),
        "loc8a": cv2.imread("patterns/locations/almeric/loc8a.png", cv2.IMREAD_COLOR),
        "loc9a": cv2.imread("patterns/locations/almeric/loc9a.png", cv2.IMREAD_COLOR),
        "loc10a": cv2.imread("patterns/locations/almeric/loc10a.png", cv2.IMREAD_COLOR),
        "loc11a": cv2.imread("patterns/locations/almeric/loc11a.png", cv2.IMREAD_COLOR),
        "loc12a": cv2.imread("patterns/locations/almeric/loc12a.png", cv2.IMREAD_COLOR),
        "loc13a": cv2.imread("patterns/locations/almeric/loc13a.png", cv2.IMREAD_COLOR),
        "loc14a": cv2.imread("patterns/locations/almeric/loc14a.png", cv2.IMREAD_COLOR),
        "loc15a": cv2.imread("patterns/locations/almeric/loc15a.png", cv2.IMREAD_COLOR),
        "loc16a": cv2.imread("patterns/locations/almeric/loc16a.png", cv2.IMREAD_COLOR),
        "loc17a": cv2.imread("patterns/locations/almeric/loc17a.png", cv2.IMREAD_COLOR),
    },
    "metanoia": {
        "loc1": cv2.imread("patterns/locations/metanoia/loc1.png", cv2.IMREAD_COLOR),
        "loc2": cv2.imread("patterns/locations/metanoia/loc2.png", cv2.IMREAD_COLOR),
        "loc3": cv2.imread("patterns/locations/metanoia/loc3.png", cv2.IMREAD_COLOR),
        "loc4": cv2.imread("patterns/locations/metanoia/loc4.png", cv2.IMREAD_COLOR),
        "loc5": cv2.imread("patterns/locations/metanoia/loc5.png", cv2.IMREAD_COLOR),
        "loc6": cv2.imread("patterns/locations/metanoia/loc6.png", cv2.IMREAD_COLOR),
        "loc7": cv2.imread("patterns/locations/metanoia/loc7.png", cv2.IMREAD_COLOR),
        "loc8": cv2.imread("patterns/locations/metanoia/loc8.png", cv2.IMREAD_COLOR),
        "loc9": cv2.imread("patterns/locations/metanoia/loc9.png", cv2.IMREAD_COLOR),
        "loc10": cv2.imread("patterns/locations/metanoia/loc10.png", cv2.IMREAD_COLOR),
        "loc11": cv2.imread("patterns/locations/metanoia/loc11.png", cv2.IMREAD_COLOR),
        "loc12": cv2.imread("patterns/locations/metanoia/loc12.png", cv2.IMREAD_COLOR),
        "loc13": cv2.imread("patterns/locations/metanoia/loc13.png", cv2.IMREAD_COLOR),
        "loc14": cv2.imread("patterns/locations/metanoia/loc14.png", cv2.IMREAD_COLOR),
        "loc15": cv2.imread("patterns/locations/metanoia/loc15.png", cv2.IMREAD_COLOR),
        "loc16": cv2.imread("patterns/locations/metanoia/loc16.png", cv2.IMREAD_COLOR),
        "loc17": cv2.imread("patterns/locations/metanoia/loc17.png", cv2.IMREAD_COLOR),
        "loc18": cv2.imread("patterns/locations/metanoia/loc18.png", cv2.IMREAD_COLOR),
        "loc19": cv2.imread("patterns/locations/metanoia/loc19.png", cv2.IMREAD_COLOR),
        "loc20": cv2.imread("patterns/locations/metanoia/loc20.png", cv2.IMREAD_COLOR),
        "loc21": cv2.imread("patterns/locations/metanoia/loc21.png", cv2.IMREAD_COLOR),
        "loc1a": cv2.imread("patterns/locations/metanoia/loc1a.png", cv2.IMREAD_COLOR),
        "loc2a": cv2.imread("patterns/locations/metanoia/loc2a.png", cv2.IMREAD_COLOR),
        "loc3a": cv2.imread("patterns/locations/metanoia/loc3a.png", cv2.IMREAD_COLOR),
        "loc4a": cv2.imread("patterns/locations/metanoia/loc4a.png", cv2.IMREAD_COLOR),
        "loc5a": cv2.imread("patterns/locations/metanoia/loc5a.png", cv2.IMREAD_COLOR),
        "loc6a": cv2.imread("patterns/locations/metanoia/loc6a.png", cv2.IMREAD_COLOR),
        "loc7a": cv2.imread("patterns/locations/metanoia/loc7a.png", cv2.IMREAD_COLOR),
        "loc8a": cv2.imread("patterns/locations/metanoia/loc8a.png", cv2.IMREAD_COLOR),
        "loc9a": cv2.imread("patterns/locations/metanoia/loc9a.png", cv2.IMREAD_COLOR),
        "loc10a": cv2.imread("patterns/locations/metanoia/loc10a.png", cv2.IMREAD_COLOR),
        "loc11a": cv2.imread("patterns/locations/metanoia/loc11a.png", cv2.IMREAD_COLOR),
        "loc12a": cv2.imread("patterns/locations/metanoia/loc12a.png", cv2.IMREAD_COLOR),
        "loc13a": cv2.imread("patterns/locations/metanoia/loc13a.png", cv2.IMREAD_COLOR),
        "loc14a": cv2.imread("patterns/locations/metanoia/loc14a.png", cv2.IMREAD_COLOR),
        "loc15a": cv2.imread("patterns/locations/metanoia/loc15a.png", cv2.IMREAD_COLOR),
        "loc16a": cv2.imread("patterns/locations/metanoia/loc16a.png", cv2.IMREAD_COLOR),
        "loc17a": cv2.imread("patterns/locations/metanoia/loc17a.png", cv2.IMREAD_COLOR),
        "loc18a": cv2.imread("patterns/locations/metanoia/loc18a.png", cv2.IMREAD_COLOR),
        "loc19a": cv2.imread("patterns/locations/metanoia/loc19a.png", cv2.IMREAD_COLOR),
        "loc20a": cv2.imread("patterns/locations/metanoia/loc20a.png", cv2.IMREAD_COLOR),
        "loc21a": cv2.imread("patterns/locations/metanoia/loc21a.png", cv2.IMREAD_COLOR),
    },
    "panfobion": {
        "loc1": cv2.imread("patterns/locations/panfobion/loc1.png", cv2.IMREAD_COLOR),
        "loc2": cv2.imread("patterns/locations/panfobion/loc2.png", cv2.IMREAD_COLOR),
        "loc3": cv2.imread("patterns/locations/panfobion/loc3.png", cv2.IMREAD_COLOR),
        "loc4": cv2.imread("patterns/locations/panfobion/loc4.png", cv2.IMREAD_COLOR),
        "loc5": cv2.imread("patterns/locations/panfobion/loc5.png", cv2.IMREAD_COLOR),
        "loc6": cv2.imread("patterns/locations/panfobion/loc6.png", cv2.IMREAD_COLOR),
        "loc7": cv2.imread("patterns/locations/panfobion/loc7.png", cv2.IMREAD_COLOR),
        "loc8": cv2.imread("patterns/locations/panfobion/loc8.png", cv2.IMREAD_COLOR),
        "loc9": cv2.imread("patterns/locations/panfobion/loc9.png", cv2.IMREAD_COLOR),
        "loc10": cv2.imread("patterns/locations/panfobion/loc10.png", cv2.IMREAD_COLOR),
        "loc11": cv2.imread("patterns/locations/panfobion/loc11.png", cv2.IMREAD_COLOR),
        "loc12": cv2.imread("patterns/locations/panfobion/loc12.png", cv2.IMREAD_COLOR),
        "loc13": cv2.imread("patterns/locations/panfobion/loc13.png", cv2.IMREAD_COLOR),
        "loc14": cv2.imread("patterns/locations/panfobion/loc14.png", cv2.IMREAD_COLOR),
        "loc15": cv2.imread("patterns/locations/panfobion/loc15.png", cv2.IMREAD_COLOR),
        "loc16": cv2.imread("patterns/locations/panfobion/loc16.png", cv2.IMREAD_COLOR),
        "loc17": cv2.imread("patterns/locations/panfobion/loc17.png", cv2.IMREAD_COLOR),
        "loc18": cv2.imread("patterns/locations/panfobion/loc18.png", cv2.IMREAD_COLOR),
        "loc19": cv2.imread("patterns/locations/panfobion/loc19.png", cv2.IMREAD_COLOR),
        "loc20": cv2.imread("patterns/locations/panfobion/loc20.png", cv2.IMREAD_COLOR),
        "loc21": cv2.imread("patterns/locations/panfobion/loc21.png", cv2.IMREAD_COLOR),
        "loc1a": cv2.imread("patterns/locations/panfobion/loc1a.png", cv2.IMREAD_COLOR),
        "loc2a": cv2.imread("patterns/locations/panfobion/loc2a.png", cv2.IMREAD_COLOR),
        "loc3a": cv2.imread("patterns/locations/panfobion/loc3a.png", cv2.IMREAD_COLOR),
        "loc4a": cv2.imread("patterns/locations/panfobion/loc4a.png", cv2.IMREAD_COLOR),
        "loc5a": cv2.imread("patterns/locations/panfobion/loc5a.png", cv2.IMREAD_COLOR),
        "loc6a": cv2.imread("patterns/locations/panfobion/loc6a.png", cv2.IMREAD_COLOR),
        "loc7a": cv2.imread("patterns/locations/panfobion/loc7a.png", cv2.IMREAD_COLOR),
        "loc8a": cv2.imread("patterns/locations/panfobion/loc8a.png", cv2.IMREAD_COLOR),
        "loc9a": cv2.imread("patterns/locations/panfobion/loc9a.png", cv2.IMREAD_COLOR),
        "loc10a": cv2.imread("patterns/locations/panfobion/loc10a.png", cv2.IMREAD_COLOR),
        "loc11a": cv2.imread("patterns/locations/panfobion/loc11a.png", cv2.IMREAD_COLOR),
        "loc12a": cv2.imread("patterns/locations/panfobion/loc12a.png", cv2.IMREAD_COLOR),
        "loc13a": cv2.imread("patterns/locations/panfobion/loc13a.png", cv2.IMREAD_COLOR),
        "loc14a": cv2.imread("patterns/locations/panfobion/loc14a.png", cv2.IMREAD_COLOR),
        "loc15a": cv2.imread("patterns/locations/panfobion/loc15a.png", cv2.IMREAD_COLOR),
        "loc16a": cv2.imread("patterns/locations/panfobion/loc16a.png", cv2.IMREAD_COLOR),
        "loc17a": cv2.imread("patterns/locations/panfobion/loc17a.png", cv2.IMREAD_COLOR),
        "loc18a": cv2.imread("patterns/locations/panfobion/loc18a.png", cv2.IMREAD_COLOR),
        "loc19a": cv2.imread("patterns/locations/panfobion/loc19a.png", cv2.IMREAD_COLOR),
        "loc20a": cv2.imread("patterns/locations/panfobion/loc20a.png", cv2.IMREAD_COLOR),
        "loc21a": cv2.imread("patterns/locations/panfobion/loc21a.png", cv2.IMREAD_COLOR),
    },
    "boss": cv2.imread("patterns/boss.png", cv2.IMREAD_COLOR),  # Добавляем паттерн босса
}

STUN_LOCATIONS = {
    "vergeland_loc3", "vergeland_loc6", "vergeland_loc12", "vergeland_loc13",
    "harangerfjord_loc4", "harangerfjord_loc5", "harangerfjord_loc13", "harangerfjord_loc15", "harangerfjord_loc18",
    "heimskringla_loc2", "heimskringla_loc3", "heimskringla_loc5", "heimskringla_loc7", "heimskringla_loc9", "heimskringla_loc11", "heimskringla_loc23",
    "sorian_loc7", "sorian_loc8", "sorian_loc9", "sorian_loc11", "sorian_loc13", "sorian_loc18", "sorian_loc19", "sorian_loc20", "sorian_loc26", "sorian_loc27", "sorian_loc28", "sorian_loc31",
    "almeric_loc6"
}

SLOW_LOCATIONS = {
    "harangerfjord_loc3", "harangerfjord_loc7", "harangerfjord_loc8", "harangerfjord_loc11", "harangerfjord_loc19", "harangerfjord_loc20",
    "heimskringla_loc8", "heimskringla_loc15", "heimskringla_loc21",
    "sorian_loc1", "sorian_loc2", "sorian_loc3", "sorian_loc10", "sorian_loc14", "sorian_loc15", "sorian_loc23",
    "almeric_loc9", "almeric_loc10", "almeric_loc14"
}

EPIC_LOCATIONS = {
    "metanoia_loc4",
    "panfobion_loc20", "panfobion_loc21",
    "almeric_loc9"
}

# После импортов, до начала класса GUI
CHEST_VALUES = {
    "big": {"silver": 30, "copper": 0, "name": "Большой сундук с ресурсами"},
    "carved": {"silver": 45, "copper": 30, "name": "Резной сундук с ресурсами"},
    "little": {"silver": 5, "copper": 60, "name": "Маленький сундук с ресурсами"},
    "middle": {"silver": 10, "copper": 0, "name": "Средний сундук с ресурсами"},
    "old": {"silver": 2, "copper": 40, "name": "Старый сундук с ресурсами"},
    "precious": {"silver": 70, "copper": 0, "name": "Драгоценный сундук с ресурсами"}
}

def find_template(label, gui, threshold=0.85):
    """Ищет шаблон на экране"""
    # Добавляем отладочное логирование
    gui.log_message(f"[DEBUG find_template] Начинаем поиск шаблона '{label}' с порогом {threshold}")
    
    # Если путь содержит информацию о регионе и локации (например "vergeland/loc1")
    if "/" in label:
        region, location = label.split("/")
        if region in PATTERNS and location in PATTERNS[region]:
            template = PATTERNS[region][location]
            gui.log_message(f"[DEBUG find_template] Разбор пути шаблона: регион='{region}', локация='{location}'")
    else:
        # Для обычных шаблонов
        if label not in PATTERNS:
            gui.log_message(f"[DEBUG find_template] Шаблон для {label} не найден в PATTERNS")
            return None
        template = PATTERNS[label]
        gui.log_message(f"[DEBUG find_template] Найден шаблон для {label}")
    
    # Делаем скриншот
    gui.log_message(f"[DEBUG find_template] Делаем скриншот для поиска '{label}'")
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # Специальная обработка для fight_no
    if label == "fight_no":
        gui.log_message("[DEBUG find_template] Используем специальный метод поиска для fight_no")
        result = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        gui.log_message(f"[DEBUG find_template] fight_no: match_value={min_val}, threshold={threshold}")
        if min_val <= threshold:
            x = min_loc[0] + template.shape[1] // 2
            y = min_loc[1] + template.shape[0] // 2
            gui.log_message(f"[DEBUG find_template] Шаблон '{label}' найден в позиции ({x}, {y}) с точностью {min_val}")
            return (x, y)
        else:
            gui.log_message(f"[DEBUG find_template] Шаблон '{label}' НЕ найден (лучшее совпадение: {min_val})")
            return None
    
    # Стандартный метод поиска
    gui.log_message("[DEBUG find_template] Используем стандартный метод поиска")
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    gui.log_message(f"[DEBUG find_template] Стандартный поиск: match_value={max_val}, threshold={threshold}")
    
    if max_val >= threshold:
        x = max_loc[0] + template.shape[1] // 2
        y = max_loc[1] + template.shape[0] // 2
        gui.log_message(f"[DEBUG find_template] Шаблон '{label}' найден в позиции ({x}, {y}) с точностью {max_val}")
        return (x, y)
    else:
        gui.log_message(f"[DEBUG find_template] Шаблон '{label}' НЕ найден (лучшее совпадение: {max_val})")
        return None

def human_click(x, y, double=False):
    """
    Выполняет клик мышью с имитацией человеческого поведения.
    :param x: координата X
    :param y: координата Y
    :param double: выполнить двойной клик
    """
    try:
        # Проверяем, что координаты имеют смысл
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            print(f"[ERROR human_click] Ошибка в координатах клика: x={x}, y={y}")
            return
        
        # Проверяем, что координаты в пределах экрана
        screen_width, screen_height = pyautogui.size()
        if x < 0 or y < 0 or x >= screen_width or y >= screen_height:
            print(f"[ERROR human_click] Координаты клика за пределами экрана: x={x}, y={y}, размер экрана: {screen_width}x{screen_height}")
            return
        
        print(f"[DEBUG human_click] Начинаем клик: x={x}, y={y}, двойной={double}")
        
        print(f"[DEBUG human_click] Перемещаем курсор к x={x}, y={y}")
        pyautogui.moveTo(x, y, duration=0.2)
        time.sleep(0.1)
        
        print(f"[DEBUG human_click] Нажимаем кнопку мыши")
        pyautogui.mouseDown()
        time.sleep(0.1)
        
        print(f"[DEBUG human_click] Отпускаем кнопку мыши")
        pyautogui.mouseUp()
        
        if double:
            print(f"[DEBUG human_click] Выполняем второй клик для double click")
            time.sleep(0.1)
            pyautogui.mouseDown()
            time.sleep(0.1)
            pyautogui.mouseUp()
        
        time.sleep(0.1)
        print(f"[DEBUG human_click] Клик выполнен успешно")
    except Exception as e:
        print(f"[ERROR human_click] Ошибка при клике: {str(e)}")

@contextmanager
def hold_key(key):
    """
    Контекстный менеджер для удержания клавиши.
    :param key: клавиша для удержания
    """
    pyautogui.keyDown(key)
    try:
        yield
    finally:
        pyautogui.keyUp(key)

def mark_location_completed(gui):
    """Отмечает текущую локацию как завершенную и сохраняет это состояние"""
    gui.log_message(f"[DEBUG mark_location_completed] Локация {gui.current_location_key} пройдена")
    gui.completed_locations[gui.current_location_key] = time.time()
    gui.save_location_memory()
    return True

def handle_safe_drop(gui, region_id):
    """
    Обработка сохранного дропа с возвратом к фарму
    """
    try:
        gui.log_message(f"[DEBUG handle_safe_drop] Начинаем обработку safe_drop для региона {region_id}")
        
        # Определяем номер телепорта для каждого региона
        region_teleports = {
            "vergeland": 4, "harangerfjord": 8, "heimskringla": 11,
            "sorian": 15, "ortre": 18, "almeric": 22,
            "metanoia": 26, "panfobion": 28
        }
        
        # Определяем номер региона для магазина/банка
        region_numbers = {
            "vergeland": 1, "harangerfjord": 2, "heimskringla": 3,
            "sorian": 4, "ortre": 5, "almeric": 6,
            "metanoia": 7, "panfobion": 8
        }
        
        # Получаем номер телепорта для текущего региона
        teleport_number = region_teleports.get(region_id)
        if not teleport_number:
            gui.log_message(f"[ERROR handle_safe_drop] Неизвестный регион: {region_id}")
            return False
            
        # Получаем номер региона для магазина/банка
        region_number = region_numbers.get(region_id, 1)
        gui.log_message(f"[DEBUG handle_safe_drop] Определены номера: телепорт={teleport_number}, регион={region_number}")
        
        # Сначала телепортируемся в нужный телепорт
        gui.log_message(f"[DEBUG handle_safe_drop] Телепортируемся в телепорт {teleport_number}")
        teleport(teleport_number, gui)
        time.sleep(2)
        
        # Проверяем успешность телепортации
        pool_2 = find_template("pool_2", gui)
        if not pool_2:
            gui.log_message("[DEBUG handle_safe_drop] Первая попытка телепортации не удалась, пробуем еще раз")
            teleport(teleport_number, gui)
            time.sleep(2)
            pool_2 = find_template("pool_2", gui)
            if not pool_2:
                gui.log_message("[ERROR handle_safe_drop] Телепортация не удалась после двух попыток")
                return False
        
        # После успешной телепортации выполняем PostFarm
        gui.log_message("[DEBUG handle_safe_drop] Телепортация успешна, начинаем PostFarm")
        
        # 1. Ремонт инвентаря
        if gui.running:
            gui.log_message("[DEBUG handle_safe_drop] Шаг 1: Ремонт инвентаря")
            PostFarm.inventory(gui)
            time.sleep(3)
        
        # 2. Продажа предметов
        if gui.running:
            gui.log_message("[DEBUG handle_safe_drop] Шаг 2: Продажа предметов")
            PostFarm.shop(region_number, gui)
            time.sleep(3)
        
        # 3. Сохранение в банк
        if gui.running:
            gui.log_message("[DEBUG handle_safe_drop] Шаг 3: Сохранение в банк")
            PostFarm.bank(region_number, gui)
            time.sleep(3)
        
        # Снимаем фарм с паузы
        gui.farming_paused = False
        gui.log_message("[DEBUG handle_safe_drop] Safe_drop завершен успешно, фарм возобновлен")
        
        return True
    except Exception as e:
        gui.log_message(f"[ERROR handle_safe_drop] Ошибка при обработке safe_drop: {str(e)}")
        gui.farming_paused = False
        return False

def run_location_step(self, region, location_key, map_x_offset, map_y_offset):
    """Выполняет один шаг обработки локации"""
    if not self.gui.running:
        self.scenario_running = False
        return
            
    if self.farming_paused:
        self.log_message("[DEBUG run_location_step] Фарм на паузе, ожидаем...")
        self.after(2000, lambda: self.run_location_step(region, location_key, map_x_offset, map_y_offset))
        return
            
    loc_enter = find_template("loc_enter", self.gui)
    if not loc_enter:
        # Ищем шаблон локации в соответствующем подсловаре PATTERNS
        loc_temp = None
        if region in PATTERNS:
            loc_number = location_key.split('_')[1]
            if loc_number in PATTERNS[region]:
                loc_temp = find_template(f"{region}/{loc_number}", self.gui)
                if not loc_temp and f"{location_key}" in self.completed_locations:
                    self.log_message(f"[DEBUG run_location_step] Локация {location_key} уже пройдена")
                    return True
                    
        map_choice = find_template("map_choice", self.gui)
        # Проверка координат: карта должна быть в правом верхнем углу
        if map_choice:
            x, y = map_choice
            if x < 1200 or y > 100:  # Примерные координаты для миникарты
                self.log_message("[DEBUG run_location_step] Игнорируем ложное срабатывание map_choice (координаты не совпадают)")
                map_choice = None
                
        if not map_choice:
            missclick_enter_loc = find_template("door_back", self.gui)
            if missclick_enter_loc:
                self.log_message(f"[DEBUG run_location_step] Мисскликнули по входу. Вошли в {location_key}.")
                pve(self.gui)  # Вызываем pve напрямую
                return True
        else:
            # Кликаем по карте с учетом позиции map_choice и смещения
            human_click(map_choice[0] + map_x_offset, map_choice[1] + map_y_offset)
            self.log_message(f"[DEBUG run_location_step] Кликаем по карте с оффсетом: x={map_x_offset}, y={map_y_offset}")
            self.after(1000, lambda: self.run_location_step(region, location_key, map_x_offset, map_y_offset))
            return
                
        if not loc_temp:
            self.log_message(f"[DEBUG run_location_step] Не найден шаблон для {location_key}")
            return False
                
        # Нашли шаблон локации - кликаем по нему и ждем появления входа
        self.log_message("[DEBUG run_location_step] Найден основной шаблон локации")
        human_click(*loc_temp)
        # Повторяем клик каждые 3 секунды, пока не появится вход
        self.after(3000, lambda: self.run_location_step(region, location_key, map_x_offset, map_y_offset))
        return
            
    # Нашли кнопку входа
    self.log_message(f"[DEBUG run_location_step] Найдена кнопка входа в локацию {location_key}")
    human_click(*loc_enter)
    time.sleep(3)
    pve(self.gui)  # Вызываем pve напрямую
    return True

def run_location(self, region, location_key, map_x_offset, map_y_offset):
    """Запускает обработку локации через after"""
    # Сохраняем информацию о текущей локации
    self.current_location_key = location_key
    
    # Запускаем первый шаг
    self.run_location_step(region, location_key, map_x_offset, map_y_offset)

def teleport(variant, gui):
    while gui.running:
        if not gui.running:
            break
        tprune_go = find_template("tprune_go", gui)
        if not tprune_go:
            if variant in (1, 2, 3, 4): region_place = find_template(f"tprune_vergeland{variant}", gui)
            if variant in (5, 6, 7, 8): region_place = find_template(f"tprune_harangerfjord{variant}", gui)
            if variant in (9, 10, 11): region_place = find_template(f"tprune_heimskringla{variant}", gui)
            if variant in (12, 13, 14, 15): region_place = find_template(f"tprune_sorian{variant}", gui)
            if variant in (16, 17, 18): region_place = find_template(f"tprune_ortre{variant}", gui)
            if variant in (19, 20, 21, 22): region_place = find_template(f"tprune_almeric{variant}", gui)
            if variant in (23, 24, 25, 26): region_place = find_template(f"tprune_metanoia{variant}", gui)
            if variant in (27, 28): region_place = find_template(f"tprune_panfobion{variant}", gui)
            if not region_place:
                if variant in (1, 2, 3, 4): region = find_template("tprune_vergeland", gui)
                if variant in (5, 6, 7, 8): region = find_template("tprune_harangerfjord", gui)
                if variant in (9, 10, 11): region = find_template("tprune_heimskringla", gui)
                if variant in (12, 13, 14, 15): region = find_template("tprune_sorian", gui)
                if variant in (16, 17, 18): region = find_template("tprune_ortre", gui)
                if variant in (19, 20, 21, 22): region = find_template("tprune_almeric", gui)
                if variant in (23, 24, 25, 26): region = find_template("tprune_metanoia", gui)
                if variant in (27, 28): region = find_template("tprune_panfobion", gui)
                if not region:
                    if variant in (1, 2, 3, 4, 19, 20, 21, 22): tprune_choice_up_down = find_template("tprune_choice_up", gui)
                    if variant in (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 23, 24, 25, 26, 27, 28): tprune_choice_up_down = find_template("tprune_choice_down", gui)
                    if not tprune_choice_up_down:
                        tprune_choice = find_template("tprune_choice", gui)
                        if not tprune_choice:
                            tprune = find_template("tprune", gui)
                            if not tprune:
                                pool_2 = pool_2 = find_template("pool_2", gui)
                                if pool_2:
                                    human_click(*pool_2)
                                else:
                                    pyautogui.moveRel(0, -100, duration=0.2)
                            else:
                                human_click(*tprune)
                        else:
                            human_click(*tprune_choice)
                    else:
                        if variant in (12, 13, 14, 15, 16, 17, 18, 23, 24, 25, 26, 27, 28): 
                            human_click(tprune_choice_up_down[0] - 5, tprune_choice_up_down[1] - 90, double=True)
                            human_click(tprune_choice_up_down[0] - 5, tprune_choice_up_down[1] - 57)
                        else: human_click(*tprune_choice_up_down)
                else:
                    human_click(*region)
            else:
                human_click(*region_place)
        else:
            human_click(*tprune_go)
            time.sleep(2)
            break
    tprune_fail = find_template("tprune_fail", gui)
    if tprune_fail:
        human_click(*tprune_fail)
        return
    else:
        return

class PostFarm:
    @staticmethod
    def inventory(gui):
        """
        Обрабатывает инвентарь: ремонтирует экипировку, использует VIP сундуки и темные кристаллы
        """
        gui.log_message("[DEBUG inventory] Начинаем ремонт экипировки")
        
        # Ремонтируем экипировку
        while gui.running:
            if not gui.running:
                break
            repair_confirm = find_template("repair_confirm", gui) or find_template("repair_ok", gui)
            if not repair_confirm:
                repair = find_template("repair", gui)
                if not repair:
                    inventar = find_template("inventar", gui)
                    if not inventar:
                        fight_no = find_template("fight_no", gui)
                        if not fight_no:
                            pyautogui.moveRel(0, -100, duration=0.2)
                        else:
                            human_click(*fight_no)
                    else:
                        human_click(*inventar)
                else:
                    human_click(*repair)
            else:
                human_click(*repair_confirm)
                break

        # Проверяем настройки использования VIP сундуков и темных кристаллов
        if not gui.use_vip_chests.get() and not gui.use_dark_crystals.get():
            gui.log_message("[DEBUG inventory] Пропускаем проверку сундуков и кристаллов - использование отключено")
            go_away = find_template("go_away", gui)
            if go_away:
                human_click(*go_away)
                time.sleep(0.5)
            return

        gui.log_message("[DEBUG inventory] Проверяем сундуки и кристаллы")
        bag_offsets = [-380, -328, -276, -224]
        
        # Проверяем ВИП сундуки
        if gui.use_vip_chests.get():
            for offset in bag_offsets:
                go_away = find_template("go_away", gui)
                if go_away:
                    human_click(go_away[0] + offset, go_away[1] - 100)
                    time.sleep(0.5)
                    while gui.running:
                        vip = find_template("vip", gui)
                        if vip:
                            human_click(vip[0], vip[1], double=True)
                            time.sleep(0.5)
                            gui.log_message("[DEBUG inventory] Используем VIP сундук")
                        else:
                            break

        # Проверяем темные кристаллы
        if gui.use_dark_crystals.get():
            for offset in bag_offsets:
                go_away = find_template("go_away", gui)
                if go_away:
                    human_click(go_away[0] + offset, go_away[1] - 100)
                    time.sleep(0.5)
                    while gui.running:
                        efir = find_template("efir", gui)
                        efir_use = find_template("efir_use", gui)
                        if efir and not efir_use:
                            human_click(efir[0], efir[1], double=True)
                            time.sleep(0.5)
                            efir_use = find_template("efir_use", gui)
                            if efir_use:
                                human_click(efir_use[0], efir_use[1])
                                time.sleep(0.5)
                                gui.log_message("[DEBUG inventory] Используем темный кристалл")
                        else:
                            break

        # Закрываем инвентарь
        go_away = find_template("go_away", gui)
        if go_away:
            human_click(*go_away)
            time.sleep(0.5)
            gui.log_message("[DEBUG inventory] Закрываем инвентарь")

    @staticmethod
    def shop(variant, gui):
        """Продает предметы в магазине с учетом настроек чекбоксов"""
        BAGS = [(-310, -85), (-258, -85), (-206, -85), (-154, -85)]
        BAG_SLOTS = [
            [(-310, -240), (-258, -240), (-206, -240), (-154, -240), (-102, -240), (-50, -240)],
            [(-310, -187), (-258, -187), (-206, -187), (-154, -187), (-102, -187), (-50, -187)],
            [(-310, -134), (-258, -134), (-206, -134), (-154, -134), (-102, -134), (-50, -134)]
        ]
        
        # Выводим состояние настроек
        print(f"Настройки продажи сундуков:")
        print(f"- sell_resource_chests: {gui.sell_resource_chests.get()}")
        print(f"- use_dark_crystals: {gui.use_dark_crystals.get()}")
        print(f"- use_vip_chests: {gui.use_vip_chests.get()}")
        
        while gui.running:
            if not gui.running:
                break
            go_away = find_template("go_away", gui)
            if not go_away:
                shop_enter = find_template("shop_enter", gui)
                if not shop_enter:
                    if variant == 1: shop = find_template("vergeland_shop", gui) or find_template("vergeland_shopa", gui)
                    if variant == 2: shop = find_template("harangerfjord_shop", gui) or find_template("harangerfjord_shopa", gui)
                    if variant == 3: shop = find_template("heimskringla_shop", gui) or find_template("heimskringla_shopa", gui)
                    if variant == 4: shop = find_template("sorian_shop", gui) or find_template("sorian_shopa", gui)
                    if variant == 5: shop = find_template("ortre_shop", gui) or find_template("ortre_shopa", gui)
                    if variant == 6: shop = find_template("almeric_shop", gui) or find_template("almeric_shopa", gui)
                    if variant == 7: shop = find_template("metanoia_shop", gui) or find_template("metanoia_shopa", gui)
                    if variant == 8: shop = find_template("panfobion_shop", gui) or find_template("panfobion_shopa", gui)
                    if not shop:
                        map_choice = find_template("map_choice", gui)
                        if map_choice:
                            # Сначала кликаем по карте для активации
                            human_click(map_choice[0], map_choice[1])
                            time.sleep(1)  # Даем время на обновление карты
                            
                            # Теперь кликаем по нужной точке
                            if variant == 1: human_click(map_choice[0] -85, map_choice[1] +150)
                            if variant == 2: human_click(map_choice[0] -75, map_choice[1] +128)
                            if variant == 3: human_click(map_choice[0] -145, map_choice[1] +185)
                            if variant == 4: human_click(map_choice[0] -20, map_choice[1] +174)
                            if variant == 5: human_click(map_choice[0] -20, map_choice[1] +171)
                            if variant == 6: human_click(map_choice[0] -112, map_choice[1] +50)
                            if variant == 7: human_click(map_choice[0] -139, map_choice[1] +68)
                            if variant == 8: human_click(map_choice[0] -131, map_choice[1] +166)
                            time.sleep(1)  # Даем время на обновление после клика
                    else:
                        human_click(shop[0], shop[1], double=True)
                        time.sleep(4)
                else:
                    human_click(*shop_enter)
                    time.sleep(4)
            else:
                # В магазине всегда проверяем сумки, но продаем или не продаем предметы в зависимости от настроек
                gui.log_message("Начинаем проверку сумок в магазине")
                
                # Проходим по всем сумкам
                for bag in BAGS:
                    if not gui.running:  # Проверка состояния перед обработкой каждой сумки
                        gui.log_message("Остановка обработки сумок")
                        return
                        
                    # Вычисляем абсолютную координату для BAG
                    bag_abs = (go_away[0] + bag[0], go_away[1] + bag[1])
                    gui.log_message(f"Клик по сумке")
                    human_click(bag_abs[0], bag_abs[1])
                    time.sleep(0.2)  # Пауза после клика по сумке
                    
                    # Проверяем сумку на пустоту
                    print(f"Проверяем сумку {bag} на пустоту...")
                    empty_bag = find_template("empty_bag", gui, threshold=0.75)
                    if empty_bag:
                        gui.log_message("Сумка пустая.")
                        continue  # Переходим к следующей сумке
                    
                    if not gui.running:  # Дополнительная проверка после проверки пустой сумки
                        gui.log_message("Остановка обработки содержимого сумки")
                        return
                        
                    msg = f"Сумка не пустая, начинаем продажу предметов"
                    gui.log_message(msg)
                    print(msg)
                    
                    # ШАГ 1: Делаем скриншот один раз для всех проверок
                    frame = np.array(pyautogui.screenshot())
                    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    
                    # ШАГ 2: Найдем все пустые ячейки на экране заранее
                    all_empty_cells = []
                    null_template = PATTERNS.get("null_bag")
                    if null_template is not None:
                        # Используем matchTemplate для поиска всех пустых ячеек
                        res = cv2.matchTemplate(frame_bgr, null_template, cv2.TM_CCOEFF_NORMED)
                        threshold = 0.7
                        loc = np.where(res >= threshold)
                        for pt in zip(*loc[::-1]):
                            x = pt[0] + null_template.shape[1] // 2
                            y = pt[1] + null_template.shape[0] // 2
                            all_empty_cells.append((x, y))
                            print(f"Найдена пустая ячейка в координатах: ({x}, {y})")
                    
                    print(f"Найдено всего пустых ячеек: {len(all_empty_cells)}")
                    
                    # Для каждого ряда слотов
                    for slot_row in BAG_SLOTS:
                        if not gui.running:  # Проверка состояния перед обработкой каждого ряда
                            gui.log_message("Остановка обработки ряда слотов")
                            return
                            
                        for slot in slot_row:
                            if not gui.running:  # Проверка состояния перед обработкой каждого слота
                                gui.log_message("Остановка обработки слота")
                                return
                                
                            # Вычисляем абсолютную координату для слота
                            slot_abs = (go_away[0] + slot[0], go_away[1] + slot[1])
                            
                            # ШАГ 3: Проверяем, совпадает ли эта ячейка с какой-либо из пустых ячеек
                            is_empty = False
                            for empty_cell in all_empty_cells:
                                if abs(empty_cell[0] - slot_abs[0]) <= 30 and abs(empty_cell[1] - slot_abs[1]) <= 30:
                                    print(f"Слот {slot} пропускаем, т.к. он пустой (координаты пустой ячейки: {empty_cell})")
                                    is_empty = True
                                    break
                            
                            # Если это пустая ячейка - сразу пропускаем без наведения мыши
                            if is_empty:
                                continue
                            
                            if not gui.running:  # Проверка состояния перед проверкой предметов
                                gui.log_message("Остановка проверки предметов")
                                return
                                
                            # ШАГ 4: Проверяем на предметы, которые нельзя продавать
                            
                            # 4.1 Проверка на орехалк (всегда не продаем)
                            oreh = find_template("oreh", gui)
                            if oreh and abs(oreh[0] - slot_abs[0]) <= 30 and abs(oreh[1] - slot_abs[1]) <= 30:
                                print(f"В слоте {slot} найден ореолхалк, пропускаем клик.")
                                continue
                            
                            # 4.2 Проверка на важные предметы (всегда не продаем)
                            exception = find_template("chastica_boj", gui) or find_template("chastica_mif", gui) or find_template("chastica_leg", gui)
                            if exception and abs(exception[0] - slot_abs[0]) <= 30 and abs(exception[1] - slot_abs[1]) <= 30:
                                print(f"В слоте {slot} найден важный предмет, пропускаем клик.")
                                continue
                            
                            if not gui.running:  # Проверка состояния перед проверкой специальных предметов
                                gui.log_message("Остановка проверки специальных предметов")
                                return
                                
                            # 4.3 Проверка на эфир (зависит от настроек)
                            efir = find_template("efir", gui)
                            if efir and not gui.use_dark_crystals.get() and abs(efir[0] - slot_abs[0]) <= 30 and abs(efir[1] - slot_abs[1]) <= 30:
                                print(f"В слоте {slot} найден эфир, пропускаем клик.")
                                continue
                                
                            # 4.4 Проверка на вип-сундуки (зависит от настроек)
                            vip = find_template("vip", gui)
                            if vip and not gui.use_vip_chests.get() and abs(vip[0] - slot_abs[0]) <= 30 and abs(vip[1] - slot_abs[1]) <= 30:
                                print(f"В слоте {slot} найден ВИП сундук, пропускаем клик.")
                                continue
                            
                            if not gui.running:  # Проверка состояния перед проверкой сундуков
                                gui.log_message("Остановка проверки сундуков")
                                return
                                
                            # 4.5 Проверка на сундуки с ресурсами (зависит от настроек)
                            should_sell_chests = gui.sell_resource_chests.get()
                                
                            # Проверяем каждый тип сундука отдельно
                            chest_found = False
                            chest_type = ""
                            
                            chest_types = {
                                "chest_old": "старый сундук",
                                "chest_middle": "средний сундук", 
                                "chest_little": "маленький сундук", 
                                "chest_big": "большой сундук", 
                                "chest_carved": "резной сундук", 
                                "chest_precious": "драгоценный сундук"
                            }
                            
                            # Проверяем каждый тип сундука
                            for chest_key, chest_desc in chest_types.items():
                                if not gui.running:  # Проверка состояния во время проверки сундуков
                                    gui.log_message("Остановка проверки типа сундука")
                                    return
                                    
                                chest = find_template(chest_key, gui)
                                if chest and abs(chest[0] - slot_abs[0]) <= 30 and abs(chest[1] - slot_abs[1]) <= 30:
                                    chest_found = True
                                    chest_type = chest_desc
                                    break  # Нашли сундук, прекращаем проверку других типов
                            
                            # Если нашли сундук и настройки запрещают продажу - пропускаем
                            if chest_found and not should_sell_chests:
                                print(f"В слоте {slot} найден {chest_type}, не продаем по настройкам (sell_resource_chests={should_sell_chests})")
                                continue
                            
                            if not gui.running:  # Финальная проверка перед продажей
                                gui.log_message("Остановка перед продажей предмета")
                                return
                                
                            # 5. Если дошли до этой точки - продаем предмет
                            print(f"Продаем предмет в слоте {slot}")
                            human_click(slot_abs[0], slot_abs[1], double=True)
                    
                    if not gui.running:  # Проверка состояния после обработки всех слотов
                        gui.log_message("Остановка после обработки всех слотов")
                        return
                
                go_away = find_template("go_away", gui)
                if go_away and gui.running:  # Проверяем состояние перед закрытием магазина
                    gui.log_message("Хлам продан")
                    human_click(go_away[0], go_away[1])
                break

    @staticmethod
    def bank(variant, gui):
        """Сохраняет предметы в банк"""
        BAGS = [(-310, -85), (-258, -85), (-206, -85), (-154, -85)]
        BAG_SLOTS = [
            [(-310, -240), (-258, -240), (-206, -240), (-154, -240), (-102, -240), (-50, -240)],
            [(-310, -187), (-258, -187), (-206, -187), (-154, -187), (-102, -187), (-50, -187)],
            [(-310, -134), (-258, -134), (-206, -134), (-154, -134), (-102, -134), (-50, -134)]
        ]
        
        while gui.running:
            if not gui.running:
                break
            go_away = find_template("go_away", gui)
            if not go_away:
                bank_enter = find_template("bank_enter", gui)
                if not bank_enter:
                    if variant == 1: bank = find_template("vergeland_bank", gui) or find_template("vergeland_banka", gui)
                    if variant == 2: bank = find_template("harangerfjord_bank", gui) or find_template("harangerfjord_banka", gui)
                    if variant == 3: bank = find_template("heimskringla_bank", gui) or find_template("heimskringla_banka", gui)
                    if variant == 4: bank = find_template("sorian_bank", gui) or find_template("sorian_banka", gui)
                    if variant == 5: bank = find_template("ortre_bank", gui) or find_template("ortre_banka", gui)
                    if variant == 6: bank = find_template("almeric_bank", gui) or find_template("almeric_banka", gui)
                    if variant == 7: bank = find_template("metanoia_bank", gui) or find_template("metanoia_banka", gui)
                    if variant == 8: bank = find_template("panfobion_bank", gui) or find_template("panfobion_banka", gui)
                    if not bank:
                        map_choice = find_template("map_choice", gui)
                        if map_choice:
                            # Сначала кликаем по карте для активации
                            human_click(map_choice[0], map_choice[1])
                            time.sleep(1)  # Даем время на обновление карты
                            
                            # Теперь кликаем по нужной точке
                            if variant == 1: human_click(map_choice[0] -85, map_choice[1] +150)
                            if variant == 2: human_click(map_choice[0] -75, map_choice[1] +128)
                            if variant == 3: human_click(map_choice[0] -145, map_choice[1] +185)
                            if variant == 4: human_click(map_choice[0] -20, map_choice[1] +174)
                            if variant == 5: human_click(map_choice[0] -20, map_choice[1] +171)
                            if variant == 6: human_click(map_choice[0] -112, map_choice[1] +50)
                            if variant == 7: human_click(map_choice[0] -139, map_choice[1] +68)
                            if variant == 8: human_click(map_choice[0] -131, map_choice[1] +166)
                            time.sleep(1)  # Даем время на обновление после клика
                    else:
                        human_click(bank[0], bank[1], double=True)
                        time.sleep(4)
                else:
                    human_click(*bank_enter)
                    time.sleep(4)
            else:
                # В банке проверяем сумки
                gui.log_message("Начинаем проверку сумок в банке")
                
                # Проходим по всем сумкам
                for bag in BAGS:
                    if not gui.running:
                        return
                        
                    # Вычисляем абсолютную координату для BAG
                    bag_abs = (go_away[0] + bag[0], go_away[1] + bag[1])
                    gui.log_message(f"Клик по сумке")
                    human_click(bag_abs[0], bag_abs[1])
                    time.sleep(0.2)
                    
                    # Проверяем сумку на пустоту
                    empty_bag = find_template("empty_bag", gui, threshold=0.75)
                    if empty_bag:
                        gui.log_message("Сумка пустая.")
                        continue
                    
                    # Для каждого ряда слотов
                    for slot_row in BAG_SLOTS:
                        if not gui.running:
                            return
                            
                        for slot in slot_row:
                            if not gui.running:
                                return
                                
                            # Вычисляем абсолютную координату для слота
                            slot_abs = (go_away[0] + slot[0], go_away[1] + slot[1])
                            
                            # Проверяем только на пустую ячейку
                            null_bag = find_template("null_bag", gui)
                            if null_bag and abs(null_bag[0] - slot_abs[0]) <= 30 and abs(null_bag[1] - slot_abs[1]) <= 30:
                                continue
                            
                            # Все остальные предметы кладем в банк
                            human_click(slot_abs[0], slot_abs[1], double=True)
                
                go_away = find_template("go_away", gui)
                if go_away:
                    gui.log_message("Предметы сохранены в банк")
                    human_click(go_away[0], go_away[1])
                break

    @staticmethod
    def cache_cleaner(gui):
        """Очищает кэш игры и перезапускает клиент"""
        cache_path = os.path.join(os.getenv('APPDATA'), "overkings", "Local Store", "cache")
        overkings_path = r"C:\Program Files (x86)\Overkings\Overkings\Overkings.exe"
        
        if os.path.exists(cache_path):
            gui.log_message("Удаляем файлы кеша...")
            try:
                for item in os.listdir(cache_path):
                    item_path = os.path.join(cache_path, item)
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                gui.log_message("Кеш успешно очищен.")
            except Exception as e:
                gui.log_message(f"[ERROR] Ошибка при удалении кеша: {e}")
        else:
            gui.log_message("[WARNING] Папка кеша не найдена.")
            
        gui.log_message("Завершаем процесс Overkings...")
        subprocess.run(["taskkill", "/F", "/IM", "Overkings.exe"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        
        gui.log_message("Запускаем Overkings...")
        try:
            subprocess.Popen(overkings_path, shell=True,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            gui.log_message("Overkings запущен.")
        except Exception as e:
            gui.log_message(f"[ERROR] Ошибка при запуске Overkings: {e}")

        while gui.running:
            if not gui.running:
                break
            pool_2 = find_template("pool_2", gui)
            if not pool_2:
                login_2 = find_template("login_2", gui)
                if not login_2:
                    login_1 = find_template("login_1", gui)
                    if not login_1:
                        gui.log_message("Overkings еще не загрузился, ждем...")
                        time.sleep(2)
                    else:
                        human_click(*login_1)
                else:
                    human_click(*login_2)
            else:
                gui.log_message("Overkings запущен, кэш очищен успешно!")
                break
        return

class RegionRunner:
    def __init__(self, gui, region_name, locations):
        self.gui = gui
        self.region_name = region_name
        self.locations = locations
        self.current_step = 0
        self.combat_start_time = None
        self.gui.log_message(f"[DEBUG RegionRunner] Инициализация RegionRunner для региона {region_name}")
        self.gui.log_message(f"[DEBUG RegionRunner] Количество шагов в сценарии: {len(locations)}")
        
        # Проверяем память локаций при инициализации
        self.check_region_memory()
        
    def check_region_memory(self):
        """Проверяет память локаций для региона и логирует статистику"""
        completed_count = 0
        total_locations = sum(1 for step in self.locations if "teleport" not in step)
        
        for i, step in enumerate(self.locations):
            if "teleport" in step:
                continue
                
            location_counter = sum(1 for s in self.locations[:i] if "teleport" not in s)
            key = f"{self.region_name.lower()}_loc{location_counter + 1}"
            
            if key in self.gui.completed_locations:
                last_time = self.gui.completed_locations[key]
                time_since = time.time() - last_time
                if time_since < 2 * 3600:  # 2 часа
                    completed_count += 1
                    
        self.gui.log_message(f"[DEBUG check_region_memory] Статистика памяти для {self.region_name}:")
        self.gui.log_message(f"[DEBUG check_region_memory] - Всего локаций: {total_locations}")
        self.gui.log_message(f"[DEBUG check_region_memory] - На откате: {completed_count}")
        self.gui.log_message(f"[DEBUG check_region_memory] - Доступно: {total_locations - completed_count}")
        
    def start(self):
        """Начинает выполнение последовательности шагов"""
        self.gui.log_message(f"[DEBUG start] Запуск сценария {self.region_name}")
        self.gui.scenario_running = True
        self.gui.current_region_key = self.region_name.lower()
        self.gui.current_region_start_time = time.time()
        self.gui.log_message(f"[DEBUG start] Установлены: scenario_running=True, current_region_key={self.gui.current_region_key}")
        
        # Проверяем, есть ли доступные локации
        available_locations = self.get_available_locations()
        if not available_locations:
            self.gui.log_message(f"[DEBUG start] Все локации в {self.region_name} на откате, пропускаем регион")
            self.finish()
            return
            
        self.process_next_step()
        
    def get_available_locations(self):
        """Возвращает список доступных локаций (не на откате)"""
        available = []
        for i, step in enumerate(self.locations):
            if "teleport" in step:
                continue
                
            location_counter = sum(1 for s in self.locations[:i] if "teleport" not in s)
            key = f"{self.region_name.lower()}_loc{location_counter + 1}"
            
            # Проверяем все условия пропуска локации
            if not self.should_skip_location(key):
                available.append(i)
                    
        return available

    def process_next_step(self):
        """Обрабатывает следующий шаг в последовательности"""
        if not self.gui.running:
            self.gui.log_message("[DEBUG process_next_step] Бот остановлен, завершаем сценарий")
            self.finish()
            return
            
        if self.current_step >= len(self.locations):
            self.gui.log_message("[DEBUG process_next_step] Достигнут конец сценария, переходим к завершению")
            self.handle_completion()
            return
            
        step = self.locations[self.current_step]
        self.gui.log_message(f"[DEBUG process_next_step] Обработка шага {self.current_step + 1}/{len(self.locations)}: {step}")
                
        if "teleport" in step:
            variant = step["teleport"]
            self.gui.log_message(f"[DEBUG process_next_step] Шаг телепортации {variant}")
            teleport(variant, self.gui)
            self.current_step += 1
            self.gui.after(2000, self.process_next_step)
            return
            
        location_counter = sum(1 for s in self.locations[:self.current_step] if "teleport" not in s)
        location_counter += 1
        key = f"{self.region_name.lower()}_loc{location_counter}"
        self.gui.log_message(f"[DEBUG process_next_step] Определен ключ локации: {key}")
                
        # Запускаем обработку локации
        self.gui.log_message(f"[DEBUG process_next_step] Начинаем обработку локации {key}")
        self.gui.current_location_key = key
                
        def on_location_complete(result):
            if result:
                self.gui.log_message(f"[DEBUG process_next_step] Локация {key} успешно пройдена")
                self.gui.completed_locations[key] = time.time()
                self.gui.save_location_memory()
                # Обновляем статистику
                self.gui.instances_count_var.set(self.gui.instances_count_var.get() + 1)
                region_key = self.region_name.lower()
                if region_key in self.gui.region_instances_count:
                    new_count = self.gui.region_instances_count[region_key].get() + 1
                    self.gui.region_instances_count[region_key].set(new_count)
                    self.gui.log_message(f"[DEBUG process_next_step] Обновлена статистика региона {region_key}: {new_count} инстансов")
            else:
                self.gui.log_message(f"[DEBUG process_next_step] Локация {key} не пройдена")
            
            self.current_step += 1
            self.gui.after(1000, self.process_next_step)
        
        # Запускаем обработку локации
        self.run_location_step(key, step["x_offset"], step["y_offset"], on_location_complete)
        
    def should_skip_location(self, key):
        """Проверяет, нужно ли пропустить локацию"""
        self.gui.log_message(f"[DEBUG should_skip_location] Проверка условий пропуска для локации {key}")
        
        # Проверка на откат
        if key in self.gui.completed_locations:
            last_time = self.gui.completed_locations[key]
            time_since_completion = time.time() - last_time
            self.gui.log_message(f"[DEBUG should_skip_location] Время с последнего прохождения: {time_since_completion:.1f} секунд")
            if time_since_completion < 2 * 3600:
                self.gui.log_message(f"[DEBUG should_skip_location] {key} пропущена(ОТКАТ)")
                return True
                
        # Проверка на СТАН
        if self.gui.skip_stun_locations.get() and key in STUN_LOCATIONS:
            self.gui.log_message(f"[DEBUG should_skip_location] {key} пропущена(СТАНЯЩАЯ)")
            return True
                
        # Проверка на ЗАМЕДЛЕНИЕ
        if self.gui.skip_slow_locations.get() and key in SLOW_LOCATIONS:
            self.gui.log_message(f"[DEBUG should_skip_location] {key} пропущена(ЗАМЕДЛЯЮЩАЯ)")
            return True

        # Проверка на ЭПИК
        if self.gui.skip_epic_locations.get() and key in EPIC_LOCATIONS:
            self.gui.log_message(f"[DEBUG should_skip_location] {key} пропущена(ЭПИЧЕСКИЙ БОСС)")
            return True

        self.gui.log_message(f"[DEBUG should_skip_location] Локация {key} не подлежит пропуску")
        return False
        
    def run_location_step(self, key, x_offset, y_offset, callback):
        """Выполняет один шаг обработки локации"""
        if not self.gui.running:
            self.gui.log_message("[DEBUG run_location_step] Бот остановлен, прерываем обработку локации")
            return
            
        if self.gui.farming_paused:
            self.gui.log_message("[DEBUG run_location_step] Фарм на паузе, ожидаем...")
            self.gui.after(2000, lambda: self.run_location_step(key, x_offset, y_offset, callback))
            return
            
        # Проверяем память локаций
        if key in self.gui.completed_locations:
            last_time = self.gui.completed_locations[key]
            time_since = time.time() - last_time
            if time_since < 2 * 3600:  # 2 часа
                self.gui.log_message(f"[DEBUG run_location_step] Локация {key} на откате еще {int((2*3600 - time_since)/60)} минут")
                callback(False)
                return
            else:
                self.gui.log_message(f"[DEBUG run_location_step] Локация {key} доступна (откат прошел)")
                
        self.gui.log_message(f"[DEBUG run_location_step] Поиск входа в локацию {key}")
        loc_enter = find_template("loc_enter", self.gui)
        if not loc_enter:
            # Проверяем наличие карты
            map_choice = find_template("map_choice", self.gui)
            # Проверка координат: карта должна быть в правом верхнем углу
            if map_choice:
                x, y = map_choice
                if x < 1200 or y > 100:  # Примерные координаты для миникарты
                    self.gui.log_message("[DEBUG run_location_step] Игнорируем ложное срабатывание map_choice (координаты не совпадают)")
                    map_choice = None
            if not map_choice:
                # Если нет карты, проверяем не вошли ли мы случайно в локацию
                missclick_enter_loc = find_template("door_back", self.gui)
                if missclick_enter_loc:
                    self.gui.log_message(f"[DEBUG run_location_step] Мисскликнули по входу. Вошли в {key}")
                    self.combat_start_time = None
                    self.pve()
                    return
                else:
                    # Если нет ни карты, ни входа в локацию - что-то пошло не так
                    self.gui.log_message(f"[ERROR run_location_step] Не найдена карта для локации {key}")
                    callback(False)
                    return
            # Сначала пробуем кликнуть по карте с оффсетом
            self.gui.log_message(f"[DEBUG run_location_step] Кликаем по карте с оффсетом: x={x_offset}, y={y_offset}")
            human_click(map_choice[0] + x_offset, map_choice[1] + y_offset)
            # Ищем шаблон локации
            region = key.split('_')[0]
            loc_number = key.split('_')[1]
            if region in PATTERNS:
                self.gui.log_message(f"[DEBUG run_location_step] Поиск шаблона для {region}/{loc_number}")
                loc_temp = None
                
                # Пробуем найти основной шаблон
                if loc_number in PATTERNS[region]:
                    loc_temp = find_template(f"{region}/{loc_number}", self.gui)
                    if loc_temp:
                        self.gui.log_message(f"[DEBUG run_location_step] Найден основной шаблон локации")
                        human_click(*loc_temp, double=True)
                        self.gui.after(2500, lambda: self.check_location_state(key, x_offset, y_offset, callback))
                        return
                        
                # Если основной не найден, пробуем альтернативный
                if not loc_temp and f"{loc_number}a" in PATTERNS[region]:
                    loc_temp = find_template(f"{region}/{loc_number}a", self.gui)
                    if loc_temp:
                        self.gui.log_message(f"[DEBUG run_location_step] Найден альтернативный шаблон локации")
                        human_click(*loc_temp, double=True)
                        self.gui.after(2500, lambda: self.check_location_state(key, x_offset, y_offset, callback))
                        return
                
                # Если шаблон не найден после клика по карте
                if not loc_temp:
                    self.gui.log_message(f"[DEBUG run_location_step] Шаблон локации не найден после клика по карте")
                    self.gui.after(1000, lambda: self.run_location_step(key, x_offset, y_offset, callback))
                    return
            else:
                self.gui.log_message(f"[ERROR run_location_step] Регион {region} не найден в PATTERNS")
                callback(False)
                return
        else:
            self.gui.log_message(f"[DEBUG run_location_step] Найден вход в локацию, входим в {key}")
            human_click(*loc_enter)
            self.combat_start_time = None
            self.gui.after(1000, lambda: self.verify_location_entry(key, x_offset, y_offset, callback))
            return True
            
        callback(False)

    def check_location_state(self, key, x_offset, y_offset, callback, attempts=0):
        """Проверяет состояние локации после клика по шаблону"""
        if not self.gui.running:
            return
            
        # Проверяем карту и кликаем по ней с оффсетом для обновления позиции
        map_choice = find_template("map_choice", self.gui)
        if map_choice:
            self.gui.log_message(f"[DEBUG check_location_state] Обновляем позицию на карте (попытка {attempts})")
            human_click(map_choice[0] + x_offset, map_choice[1] + y_offset)
            time.sleep(0.5)  # Даем время на обновление экрана
        
        # Проверяем, появилась ли кнопка входа
        loc_enter = find_template("loc_enter", self.gui)
        if loc_enter:
            self.gui.log_message(f"[DEBUG check_location_state] Найдена кнопка входа в локацию {key}")
            human_click(*loc_enter)
            self.gui.after(2000, lambda: self.verify_location_entry(key, x_offset, y_offset, callback))
            return
            
        # Проверяем, не вошли ли мы случайно в локацию
        door_back = find_template("door_back", self.gui)
        if door_back:
            self.gui.log_message(f"[DEBUG check_location_state] Уже в локации {key}")
            self.combat_start_time = None
            self.pve()
            return
            
        if not map_choice:
            # Если карта пропала - значит мы уже в локации
            self.gui.log_message(f"[DEBUG check_location_state] Карта не видна, возможно уже в локации {key}")
            self.combat_start_time = None
            self.pve()
            return
            
        # Ищем шаблон локации
        region = key.split('_')[0]
        loc_number = key.split('_')[1]
        
        if region in PATTERNS:
            loc_temp = None
            if loc_number in PATTERNS[region]:
                loc_temp = find_template(f"{region}/{loc_number}", self.gui)
            if not loc_temp and f"{loc_number}a" in PATTERNS[region]:
                loc_temp = find_template(f"{region}/{loc_number}a", self.gui)
                
            if loc_temp:
                self.gui.log_message(f"[DEBUG check_location_state] Найден шаблон локации, кликаем")
                human_click(*loc_temp, double=True)
            
        # Продолжаем попытки в любом случае
        self.gui.after(2000, lambda: self.check_location_state(key, x_offset, y_offset, callback, attempts + 1))

    def verify_location_entry(self, key, x_offset, y_offset, callback, verify_attempts=1):
        """Проверяет успешность входа в локацию"""
        if not self.gui.running:
            return
            
        if verify_attempts > 5:  # Максимум 5 попыток (5 секунд)
            self.gui.log_message(f"[ERROR verify_location_entry] Не удалось подтвердить вход в локацию {key}")
            callback(False)
            return
            
        # Проверяем наличие кнопки входа или карты
        door_back = find_template("door_back", self.gui)
        map_choice = find_template("map_choice", self.gui)
        loc_enter = find_template("loc_enter", self.gui)
        
        # Если видим карту в правом верхнем углу - локация не доступна
        if map_choice:
            x, y = map_choice
            if x >= 1200 and y <= 100:
                self.gui.log_message(f"[DEBUG verify_location_entry] Локация {key} не доступна (видна карта)")
                callback(False)
                return
                
        # Если все еще видим вход - значит не вошли
        if loc_enter:
            self.gui.log_message("[DEBUG verify_location_entry] Все еще видим вход, пробуем войти снова...")
            human_click(*loc_enter)
            self.gui.after(1000, lambda: self.verify_location_entry(key, x_offset, y_offset, callback, verify_attempts + 1))
            return
            
        # Если не видим ни карту, ни вход - мы в локации, начинаем бой
        self.gui.log_message(f"[DEBUG verify_location_entry] Вошли в локацию {key}, начинаем бой")
        self.combat_start_time = None
        
        # Начинаем бой
        pool_coords = find_template("pool_2", self.gui)
        if pool_coords:
            self.gui.log_message("[DEBUG verify_location_entry] Бежим в конец локации.")
            with hold_key("alt"):
                human_click(pool_coords[0] - 160, pool_coords[1] - 50)
                time.sleep(1.1)
            # Бежим до конца локации в цикле
            while self.gui.running:
                self.gui.log_message("[DEBUG verify_location_entry] Бежим к концу локации.")
                with hold_key("alt"):
                    human_click(pool_coords[0] - 160, pool_coords[1] - 50)
                    time.sleep(1.1)
                    human_click(pool_coords[0] - 160, pool_coords[1] - 250)
                    
                # Проверяем на засаду
                fight_no = find_template("fight_no", self.gui)
                if not fight_no:
                    self.gui.log_message("[DEBUG verify_location_entry] Обнаружена возможная засада! Отступаем.")
                    door_back = find_template("door_back", self.gui)
                    if door_back:
                        human_click(*door_back)
                    callback(False)
                    return
                    
                # Проверяем, дошли ли до конца локации
                door_next = find_template("door_next", self.gui) or find_template("door_next2", self.gui)
                if door_next:
                    self.gui.log_message("[DEBUG verify_location_entry] Дошли до конца локации!")
                    break
                    
                # Если не дошли - продолжаем бежать
                time.sleep(0.5)
                
            # Проверяем наличие босса
            boss = find_template("boss", self.gui)
            found_boss = boss and self.gui.save_drops.get()
            
            # Начинаем бой
            self.gui.log_message("[DEBUG verify_location_entry] Начинаем бой")
            human_click(*pool_coords)
            self.gui.log_message("[DEBUG verify_location_entry] Призываем сигил.")
            human_click(pool_coords[0] - 170, pool_coords[1])
            
            # Цикл атаки
            while not find_template("fight_no", self.gui):
                if not self.gui.running:
                    break
                    
                you_dead1 = find_template("you_dead1", self.gui)
                achievement = find_template("achievement", self.gui)
                
                if you_dead1 or achievement:
                    break
                    
                human_click(pool_coords[0], pool_coords[1] - 505, double=True)
                self.gui.log_message("[DEBUG verify_location_entry] Атакуем противника.")
                human_click(pool_coords[0] - 530, pool_coords[1])
                self.gui.log_message("[DEBUG verify_location_entry] Используем скиллы.")
                human_click(pool_coords[0] - 470, pool_coords[1])
                time.sleep(0.5)
            
            # Проверяем успешное завершение боя
            if find_template("fight_no", self.gui):
                if found_boss:
                    self.gui.log_message("[DEBUG verify_location_entry] Бой с боссом завершен! Телепортируемся для PostFarm")
                    
                    # Определяем номер телепорта для текущего региона
                    region_teleports = {
                        "vergeland": 4,      # телепорты 1-4
                        "harangerfjord": 8,  # телепорты 5-8
                        "heimskringla": 11,  # телепорты 9-11
                        "sorian": 15,        # телепорты 12-15
                        "ortre": 18,         # телепорты 16-18
                        "almeric": 22,       # телепорты 19-22
                        "metanoia": 26,      # телепорты 23-26
                        "panfobion": 28      # телепорты 27-28
                    }
                    
                    # Получаем номер телепорта для текущего региона
                    region = self.region_name.lower()
                    teleport_number = region_teleports.get(region)
                    if teleport_number:
                        self.gui.log_message(f"[DEBUG verify_location_entry] Телепортируемся в телепорт {teleport_number} для PostFarm")
                        teleport(teleport_number, self.gui)
                        time.sleep(2)
                        
                        # Проверяем успешность телепортации
                        pool_2 = find_template("pool_2", self.gui)
                        if pool_2:
                            self.gui.log_message("[DEBUG verify_location_entry] Телепортация успешна, начинаем PostFarm")
                            self.gui.farming_paused = True
                            self.handle_post_location()
                        else:
                            self.gui.log_message("[DEBUG verify_location_entry] Телепортация не удалась, пробуем еще раз")
                            teleport(teleport_number, self.gui)
                            time.sleep(2)
                            self.gui.farming_paused = True
                            self.handle_post_location()
                    return
                else:
                    door_next = find_template("door_next", self.gui) or find_template("door_next2", self.gui)
                    if door_next:
                        self.gui.log_message("[DEBUG verify_location_entry] Бой завершен, идем через дверь")
                        human_click(*door_next)
            else:
                self.gui.log_message("[DEBUG verify_location_entry] Телепортация не удалась, пробуем еще раз")
                teleport(teleport_number, self.gui)
                time.sleep(2)
                self.gui.farming_paused = True
                self.handle_post_location()
            return
            
        callback(True)  # Сообщаем, что вход успешен

    def handle_next_door(self, door_next):
        """Обрабатывает переход к следующей двери"""
        if not self.gui.running:
            return
            
        achievement = find_template("achievement", self.gui)
        if achievement:
            human_click(*achievement)
            self.gui.after(1000, lambda: self.handle_next_door(door_next))
            return
            
        # Проверяем наличие босса
        boss = find_template("boss", self.gui)
        if boss and self.gui.save_drops.get():
            self.gui.log_message("[DEBUG handle_next_door] Обнаружен босс! Это последний уровень локации.")
            
            # Ставим фарм на паузу
            self.gui.log_message("[DEBUG handle_next_door] Фарм поставлен на паузу для защиты от засад")
            
            # Определяем номер телепорта для текущего региона
            region_teleports = {
                "vergeland": 4,      # телепорты 1-4
                "harangerfjord": 8,  # телепорты 5-8
                "heimskringla": 11,  # телепорты 9-11
                "sorian": 15,        # телепорты 12-15
                "ortre": 18,         # телепорты 16-18
                "almeric": 22,       # телепорты 19-22
                "metanoia": 26,      # телепорты 23-26
                "panfobion": 28      # телепорты 27-28
            }
            
            # Получаем номер телепорта для текущего региона
            teleport_number = region_teleports.get(self.region_name.lower())
            if teleport_number:
                self.gui.log_message(f"[DEBUG handle_next_door] Телепортируемся в телепорт {teleport_number} для PostFarm")
                self.gui.after(2000, lambda: teleport(teleport_number, self.gui))
                self.gui.after(4000, lambda: self.handle_post_location())
            return
            
        # Если босса нет или safe_drops выключен, продолжаем обычное прохождение
        human_click(*door_next)
        self.gui.after(2000, self.pve_combat)

    def handle_post_location(self):
        """Обработка действий после завершения локации"""
        if not self.gui.running:
            return
            
        # Определяем номер региона для магазина/банка
        region_numbers = {
            "vergeland": 1,
            "harangerfjord": 2,
            "heimskringla": 3,
            "sorian": 4,
            "ortre": 5,
            "almeric": 6,
            "metanoia": 7,
            "panfobion": 8
        }
        region_number = region_numbers.get(self.region_name.lower(), 1)
        
        # Выполняем последовательность действий PostFarm
        self.gui.log_message("[DEBUG handle_post_location] Выполняем действия PostFarm")
        PostFarm.inventory(self.gui)  # Ремонт
        self.gui.after(3000, lambda: PostFarm.shop(region_number, self.gui))  # Продажа
        self.gui.after(6000, lambda: PostFarm.bank(region_number, self.gui))  # Банк
        
        # Снимаем фарм с паузы после завершения всех операций
        def resume_farming():
            self.gui.farming_paused = False
            self.gui.log_message("[DEBUG handle_post_location] Фарм возобновлен после PostFarm")
            mark_location_completed(self.gui)  # Отмечаем локацию как завершенную
            
        # Планируем возобновление фарма после завершения всех операций PostFarm
        self.gui.after(9000, resume_farming)

    def handle_safe_drop_teleport(self):
        """Обрабатывает телепортацию для safe_drop"""
        if not self.gui.running:
            return
        
        tprune = find_template("tprune", self.gui)
        if tprune:
            human_click(*tprune)
            self.gui.after(1000, self.handle_safe_drop_start)
            return
        
        self.gui.log_message("[DEBUG handle_safe_drop_teleport] Не удалось найти камень телепортации")
        self.gui.farming_paused = False
        
    def handle_safe_drop_start(self):
        """Начинает обработку safe_drop"""
        if not self.gui.running:
            return
        
        region = self.gui.current_location_key.split('_')[0]
        handle_safe_drop(self.gui, region)

class Regions:
    def __init__(self, gui):
        self.gui = gui
        
    def optimize_route(self, locations, region_name):
        """Оптимизирует маршрут с учетом памяти локаций"""
        optimized = []
        current_teleport = None
        locations_in_current_group = []
        
        for step in locations:
            if "teleport" in step:
                # Если есть накопленные локации, проверяем их
                if locations_in_current_group:
                    available_locations = []
                    for loc in locations_in_current_group:
                        loc_index = len([x for x in optimized if "teleport" not in x]) + len(available_locations) + 1
                        key = f"{region_name.lower()}_loc{loc_index}"
                        
                        if key not in self.gui.completed_locations:
                            available_locations.append(loc)
                        else:
                            last_time = self.gui.completed_locations[key]
                            if time.time() - last_time >= 2 * 3600:  # 2 часа
                                available_locations.append(loc)
                                
                    # Если есть доступные локации в группе, добавляем телепорт и локации
                    if available_locations:
                        if current_teleport:
                            optimized.append(current_teleport)
                        optimized.extend(available_locations)
                        
                # Сохраняем новый телепорт и очищаем группу
                current_teleport = step
                locations_in_current_group = []
            else:
                locations_in_current_group.append(step)
                
        # Обрабатываем последнюю группу
        if locations_in_current_group:
            available_locations = []
            for loc in locations_in_current_group:
                loc_index = len([x for x in optimized if "teleport" not in x]) + len(available_locations) + 1
                key = f"{region_name.lower()}_loc{loc_index}"
                
                if key not in self.gui.completed_locations:
                    available_locations.append(loc)
                else:
                    last_time = self.gui.completed_locations[key]
                    if time.time() - last_time >= 2 * 3600:
                        available_locations.append(loc)
                        
            if available_locations:
                if current_teleport:
                    optimized.append(current_teleport)
                optimized.extend(available_locations)
                
        return optimized

    def vergeland(self):
        locations = [
            {"teleport": 1},
            {"x_offset": -150, "y_offset": 185},  # 1
            {"x_offset": -50,  "y_offset": 160},  # 2
            {"x_offset": -60,  "y_offset": 135},  # 3
            {"x_offset": -20,  "y_offset": 105},  # 4
            {"x_offset": -20,  "y_offset": 125},  # 5
            {"x_offset": -20,  "y_offset": 100},  # 6
            {"x_offset": -20,  "y_offset": 100},  # 7
            {"x_offset": -20,  "y_offset": 100},  # 8
            {"teleport": 2},
            {"x_offset": -20,  "y_offset": 50},   # 9
            {"x_offset": -20,  "y_offset": 50},   # 10
            {"x_offset": -65,  "y_offset": 50},   # 11
            {"x_offset": -65,  "y_offset": 50},   # 12
            {"teleport": 3},
            {"x_offset": -110, "y_offset": 70},   # 13
            {"x_offset": -110, "y_offset": 50},   # 14
            {"x_offset": -140, "y_offset": 75},   # 15
            {"x_offset": -140, "y_offset": 75},   # 16
            {"x_offset": -140, "y_offset": 95},   # 17
            {"x_offset": -140, "y_offset": 125},  # 18
            {"teleport": 4}
        ]
        
        # Оптимизируем маршрут перед запуском
        optimized_locations = self.optimize_route(locations, "Vergeland")
        if not optimized_locations:
            self.gui.log_message("[DEBUG RegionRunner] Все локации Vergeland на откате, пропускаем регион")
            return
            
        runner = RegionRunner(self.gui, "Vergeland", optimized_locations)
        runner.start()

    def harangerfjord(self):
        locations = [
            {"teleport": 5},
            {"x_offset": -20,  "y_offset": 180},  # 1
            {"x_offset": -20,  "y_offset": 157},  # 2
            {"x_offset": -25,  "y_offset": 176},  # 3
            {"x_offset": -61,  "y_offset": 168},  # 4
            {"x_offset": -25,  "y_offset": 145},  # 5
            {"x_offset": -20,  "y_offset": 128},  # 6
            {"x_offset": -42,  "y_offset": 105},  # 7
            {"x_offset": -42,  "y_offset": 105},  # 8
            {"x_offset": -20,  "y_offset": 70},   # 9
            {"x_offset": -20,  "y_offset": 70},   # 10
            {"x_offset": -20,  "y_offset": 50},   # 11
            {"x_offset": -20,  "y_offset": 50},   # 12
            {"x_offset": -75,  "y_offset": 50},   # 13
            {"teleport": 6},
            {"x_offset": -142, "y_offset": 92},   # 14
            {"x_offset": -142, "y_offset": 92},   # 15
            {"x_offset": -141, "y_offset": 52},   # 16
            {"x_offset": -115, "y_offset": 83},   # 17
            {"x_offset": -115, "y_offset": 83},   # 18
            {"x_offset": -97,  "y_offset": 75},   # 19
            {"x_offset": -105, "y_offset": 50},   # 20
            {"x_offset": -115, "y_offset": 122},  # 21
            {"teleport": 7},
            {"x_offset": -138, "y_offset": 165},  # 22
            {"x_offset": -138, "y_offset": 179},  # 23
            {"teleport": 8}
        ]
        
        optimized_locations = self.optimize_route(locations, "Harangerfjord")
        if not optimized_locations:
            self.gui.log_message("[DEBUG] Все локации Harangerfjord на откате, пропускаем регион")
            return
            
        runner = RegionRunner(self.gui, "Harangerfjord", optimized_locations)
        runner.start()

    def heimskringla(self):
        locations = [
            {"teleport": 9},
            {"x_offset": -105, "y_offset": 175},  # 1
            {"x_offset": -105, "y_offset": 175},  # 2
            {"teleport": 10},
            {"x_offset": -45,  "y_offset": 185},  # 3
            {"x_offset": -18,  "y_offset": 171},  # 4
            {"x_offset": -20,  "y_offset": 122},  # 5
            {"x_offset": -20,  "y_offset": 122},  # 6
            {"x_offset": -40,  "y_offset": 118},  # 7
            {"x_offset": -40,  "y_offset": 118},  # 8
            {"x_offset": -43,  "y_offset": 85},   # 9
            {"x_offset": -69,  "y_offset": 100},  # 10
            {"x_offset": -69,  "y_offset": 100},  # 11
            {"x_offset": -20,  "y_offset": 50},   # 12
            {"x_offset": -20,  "y_offset": 50},   # 13
            {"x_offset": -20,  "y_offset": 91},   # 14
            {"x_offset": -20,  "y_offset": 91},   # 15
            {"teleport": 11},
            {"x_offset": -145, "y_offset": 50},   # 16
            {"x_offset": -145, "y_offset": 50},   # 17
            {"x_offset": -105, "y_offset": 76},   # 18
            {"x_offset": -105, "y_offset": 76},   # 19
            {"x_offset": -87,  "y_offset": 96},   # 20
            {"x_offset": -135, "y_offset": 113},  # 21
            {"x_offset": -135, "y_offset": 113},  # 22
            {"x_offset": -140, "y_offset": 79},   # 23
            {"teleport": 9}
        ]
        runner = RegionRunner(self.gui, "Heimskringla", locations)
        runner.start()

    def sorian(self):
        locations = [
            {"teleport": 12},
            {"x_offset": -20,  "y_offset": 60},   # 1
            {"x_offset": -20,  "y_offset": 60},   # 2
            {"x_offset": -20,  "y_offset": 60},   # 3
            {"x_offset": -20,  "y_offset": 60},   # 4
            {"x_offset": -44,  "y_offset": 77},   # 5
            {"x_offset": -20,  "y_offset": 82},   # 6
            {"x_offset": -55,  "y_offset": 105},  # 7
            {"x_offset": -55,  "y_offset": 105},  # 8
            {"x_offset": -20,  "y_offset": 131},  # 9
            {"x_offset": -20,  "y_offset": 131},  # 10
            {"x_offset": -20,  "y_offset": 131},  # 11
            {"x_offset": -20,  "y_offset": 116},  # 12
            {"x_offset": -20,  "y_offset": 116},  # 13
            {"x_offset": -20,  "y_offset": 116},  # 14
            {"x_offset": -20,  "y_offset": 95},   # 15
            {"teleport": 13},
            {"x_offset": -140, "y_offset": 173},  # 16
            {"x_offset": -140, "y_offset": 173},  # 17
            {"x_offset": -111, "y_offset": 163},  # 18
            {"x_offset": -106, "y_offset": 134},  # 19
            {"x_offset": -95,  "y_offset": 155},  # 20
            {"x_offset": -80,  "y_offset": 155},  # 21
            {"x_offset": -80,  "y_offset": 167},  # 22
            {"x_offset": -86,  "y_offset": 112},  # 23
            {"x_offset": -130, "y_offset": 125},  # 24
            {"x_offset": -140, "y_offset": 111},  # 25
            {"teleport": 14},
            {"x_offset": -72,  "y_offset": 54},   # 26
            {"x_offset": -101, "y_offset": 81},   # 27
            {"x_offset": -101, "y_offset": 81},   # 28
            {"x_offset": -115, "y_offset": 100},  # 29
            {"x_offset": -115, "y_offset": 100},  # 30
            {"x_offset": -140, "y_offset": 83},   # 31
            {"x_offset": -140, "y_offset": 83},   # 32
            {"teleport": 15}
        ]
        runner = RegionRunner(self.gui, "Sorian", locations)
        runner.start()

    def ortre(self):
        locations = [
            {"teleport": 16},
            {"x_offset": -140,  "y_offset": 75},   # 1
            {"x_offset": -140,  "y_offset": 75},   # 2
            {"x_offset": -110,  "y_offset": 83},   # 3
            {"x_offset": -103,  "y_offset": 114},  # 4
            {"x_offset": -97,   "y_offset": 139},  # 5
            {"x_offset": -114,  "y_offset": 158},  # 6
            {"x_offset": -94,   "y_offset": 171},  # 7
            {"x_offset": -116,  "y_offset": 179},  # 8
            {"x_offset": -149,  "y_offset": 185},  # 9
            {"teleport": 17},
            {"x_offset": -20,   "y_offset": 90},   # 10
            {"teleport": 18}
        ]
        runner = RegionRunner(self.gui, "Ortre", locations)
        runner.start()

    def almeric(self):
        locations = [
            {"teleport": 19},
            {"x_offset": -132,  "y_offset": 76},   # 1
            {"x_offset": -135,  "y_offset": 93},   # 2
            {"x_offset": -109,  "y_offset": 142},  # 3
            {"x_offset": -137,  "y_offset": 163},  # 4
            {"x_offset": -137,  "y_offset": 163},  # 5
            {"teleport": 20},
            {"x_offset": -63,   "y_offset": 168},  # 6
            {"x_offset": -95,   "y_offset": 161},  # 7
            {"x_offset": -84,   "y_offset": 134},  # 8
            {"x_offset": -20,   "y_offset": 147},  # 9
            {"teleport": 21},
            {"x_offset": -92,   "y_offset": 119},  # 10
            {"x_offset": -80,   "y_offset": 102},  # 11
            {"x_offset": -80,   "y_offset": 102},  # 12
            {"x_offset": -71,   "y_offset": 86},   # 13
            {"x_offset": -20,   "y_offset": 103},  # 14
            {"teleport": 22},
            {"x_offset": -20,   "y_offset": 50},   # 15
            {"x_offset": -40,   "y_offset": 70},   # 16
            {"x_offset": -50,   "y_offset": 50},   # 17
            {"teleport": 19}
        ]
        runner = RegionRunner(self.gui, "Almeric", locations)
        runner.start()

    def metanoia(self):
        locations = [
            {"teleport": 23},
            {"x_offset": -132,  "y_offset": 76},   # 1
            {"teleport": 24},
            {"x_offset": -122,  "y_offset": 168},  # 2
            {"x_offset": -122,  "y_offset": 168},  # 3
            {"x_offset": -96,   "y_offset": 162},  # 4
            {"x_offset": -76,   "y_offset": 171},  # 5
            {"x_offset": -60,   "y_offset": 185},  # 6
            {"x_offset": -55,   "y_offset": 169},  # 7
            {"x_offset": -67,   "y_offset": 144},  # 8
            {"x_offset": -43,   "y_offset": 149},  # 9
            {"x_offset": -43,   "y_offset": 149},  # 10
            {"x_offset": -26,   "y_offset": 120},  # 11
            {"x_offset": -25,   "y_offset": 115},  # 12
            {"x_offset": -25,   "y_offset": 115},  # 13
            {"x_offset": -20,   "y_offset": 97},   # 14
            {"x_offset": -20,   "y_offset": 97},   # 15
            {"x_offset": -20,   "y_offset": 97},   # 16
            {"x_offset": -20,   "y_offset": 97},   # 17
            {"teleport": 25},
            {"x_offset": -132,  "y_offset": 149},  # 18
            {"x_offset": -98,   "y_offset": 128},  # 19
            {"x_offset": -98,   "y_offset": 128},  # 20
            {"x_offset": -142,  "y_offset": 106},  # 21
            {"teleport": 26}
        ]
        runner = RegionRunner(self.gui, "Metanoia", locations)
        runner.start()

    def panfobion(self):
        locations = [
            {"teleport": 27},
            {"x_offset": -64,   "y_offset": 178},  # 1
            {"x_offset": -69,   "y_offset": 166},  # 2
            {"x_offset": -129,  "y_offset": 137},  # 3
            {"x_offset": -129,  "y_offset": 137},  # 4
            {"x_offset": -93,   "y_offset": 98},   # 5
            {"x_offset": -80,   "y_offset": 80},   # 6
            {"x_offset": -105,  "y_offset": 60},   # 7
            {"x_offset": -105,  "y_offset": 60},   # 8
            {"x_offset": -53,   "y_offset": 53},   # 9
            {"x_offset": -41,   "y_offset": 69},   # 10
            {"x_offset": -20,   "y_offset": 50},   # 11
            {"x_offset": -20,   "y_offset": 50},   # 12
            {"x_offset": -20,   "y_offset": 50},   # 13
            {"x_offset": -41,   "y_offset": 108},  # 14
            {"x_offset": -41,   "y_offset": 108},  # 15
            {"x_offset": -41,   "y_offset": 108},  # 16
            {"x_offset": -25,   "y_offset": 138},  # 17
            {"x_offset": -20,   "y_offset": 129},  # 18
            {"x_offset": -20,   "y_offset": 138},  # 19
            {"x_offset": -42,   "y_offset": 165},  # 20
            {"x_offset": -20,   "y_offset": 168},  # 21
            {"teleport": 28}
        ]
        runner = RegionRunner(self.gui, "Panfobion", locations)
        runner.start()

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Определяем region_keys в самом начале
        self.region_keys = [
            "vergeland", "harangerfjord", "heimskringla", "sorian",
            "ortre", "almeric", "metanoia", "panfobion"
        ]
        
        # Инициализация базовых переменных для статистики
        self.total_uptime_seconds = 0
        self.start_time = None
        self.current_region_key = None
        self.current_region_start_time = None
        
        # Инициализация переменных для статистики регионов
        self.region_time_str = {key: tk.StringVar(value="00:00:00") for key in self.region_keys}
        self.region_time_spent = {key: tk.DoubleVar(value=0.0) for key in self.region_keys}
        self.region_instances_count = {key: tk.IntVar(value=0) for key in self.region_keys}
        self.instances_count_var = tk.IntVar(value=0)
        
        # Настройки вкладки фарма
        self.minimize_after_start = tk.BooleanVar(value=False)
        self.careful_farming = tk.BooleanVar(value=False)
        self.save_drops = tk.BooleanVar(value=True)
        self.hunt_enemies = tk.BooleanVar(value=False)
        self.protect_bot_pvp = tk.BooleanVar(value=False)
        self.farm_legendary = tk.BooleanVar(value=False)
        self.farm_mythic = tk.BooleanVar(value=False)
        self.farm_divine = tk.BooleanVar(value=False)
        self.skip_stun_locations = tk.BooleanVar(value=True)
        self.skip_slow_locations = tk.BooleanVar(value=True)
        self.skip_epic_locations = tk.BooleanVar(value=True)
        self.use_dark_crystals = tk.BooleanVar(value=True)
        self.use_vip_chests = tk.BooleanVar(value=True)
        self.sell_resource_chests = tk.BooleanVar(value=False)
        self.keep_important_items = tk.BooleanVar(value=True)
        
        # Инициализация переменных для выпадающих списков
        self.dropdown_vars = [tk.StringVar(value="") for _ in range(8)]
        
        # Инициализация переменных для навыков
        self.skill_priorities_left = [tk.StringVar(value="0") for _ in range(12)]
        self.skill_priorities_right = [tk.StringVar(value="0") for _ in range(12)]
        
        # Настройки автозапуска
        self.auto_start_bot = tk.BooleanVar(value=False)
        self.auto_start_scenario = tk.StringVar(value="")
        
        # Инициализация статистики предметов
        self.item_stats_vars = {
            "total_banked": tk.IntVar(value=0),
            "total_sold": tk.IntVar(value=0),
            "total_opened_vip": tk.IntVar(value=0),
            "total_sold_earnings": tk.IntVar(value=0),
            "total_dark_crystals_used": tk.IntVar(value=0),
            "total_dark_crystals_earned": tk.IntVar(value=0),
            "earnings_daily_gold": tk.IntVar(value=0),
            "earnings_daily_silver": tk.IntVar(value=0),
            "earnings_daily_copper": tk.IntVar(value=0),
            "earnings_monthly_gold": tk.IntVar(value=0),
            "earnings_monthly_silver": tk.IntVar(value=0),
            "earnings_monthly_copper": tk.IntVar(value=0),
            "earnings_total_gold": tk.IntVar(value=0),
            "earnings_total_silver": tk.IntVar(value=0),
            "earnings_total_copper": tk.IntVar(value=0)
        }
        
        # Инициализация статистики сундуков
        self.chest_stats = {
            "banked": {region: {} for region in self.region_keys},
            "sold": {region: {} for region in self.region_keys},
            "opened_vip": {region: 0 for region in self.region_keys},
            "dark_crystals_used": {region: 0 for region in self.region_keys},
            "dark_crystals_earned": {region: 0 for region in self.region_keys},
            "sold_earnings": {
                "daily": {region: {"gold": 0, "silver": 0, "copper": 0} for region in self.region_keys},
                "monthly": {region: {"gold": 0, "silver": 0, "copper": 0} for region in self.region_keys},
                "total": {region: {"gold": 0, "silver": 0, "copper": 0} for region in self.region_keys},
                "last_reset": {"daily": None, "monthly": None}
            }
        }
        
        # Инициализация статистики регионов
        self.region_stats = {}
        for key in self.region_keys:
            self.region_stats[key] = {
                "visits": 0,
                "time_spent": 0,
                "banked": tk.IntVar(value=0),
                "sold": tk.IntVar(value=0),
                "opened_vip": tk.IntVar(value=0),
                "earnings": tk.IntVar(value=0)
            }
        
        # Файлы для сохранения данных
        self.stats_file = "statistics.json"
        self.location_memory_file = "location_memory.json"
        self.location_memory_duration = 2
        
        # Загрузка сохраненных данных
        self.completed_locations = {}
        self.load_location_memory()
        self.load_statistics()
        
        # Остальная инициализация GUI
        self.title(f"TG @hiro0085 {VERSION}")
        self.geometry("800x800")
        
        # Состояние бота
        self.running = False
        self.scenario_thread = None
        self.vjuh_thread = None
        self.scenario_running = False
        self.selected_scenario = tk.StringVar(value="vergeland")
        self.current_index = 0
        
        # Обработка функций
        self.function_handler = Regions(self)
        
        # Сопоставление для выпадающих списков
        self.functions_mapping = {
            "Вергеленд": self.function_handler.vergeland,
            "Харангер-фьорд": self.function_handler.harangerfjord,
            "Хеймскрингла": self.function_handler.heimskringla,
            "Сориан": self.function_handler.sorian,
            "Ортрэ": self.function_handler.ortre,
            "Альмерик": self.function_handler.almeric,
            "Метанойя": self.function_handler.metanoia,
            "Панфобион": self.function_handler.panfobion
        }
        self.options = [""] + list(self.functions_mapping.keys())
        
        # Создание виджетов
        self._create_widgets()
        
        # Вместо этого запускаем периодические проверки через after
        self.after(100, self.check_vjuh)
        self.after(100, self.check_connection)
        self.after(1000, self.continuous_loop)
        
        # Добавление обработчика закрытия окна
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Запуск обновления статистики
        self._update_stats()
        
        self.farming_paused = False
        self.current_location = None
        self.current_location_key = None
        
        # Загрузка настроек после создания всех виджетов
        self.load_settings()

    def _create_widgets(self):
        # Настройка сетки макета (1 строка, 2 столбца: боковая панель | контент)
        self.grid_columnconfigure(1, weight=1)  # Столбец контента расширяется
        self.grid_rowconfigure(0, weight=1)     # Основная строка расширяется

        # --- Боковая панель ---
        self.sidebar_frame = customtkinter.CTkFrame(self, width=150, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")  # Охватывает 2 строки (основная + статус)
        self.sidebar_frame.grid_rowconfigure(7, weight=1)  # Сдвигает нижние элементы вниз

        # Добавить заголовок/логотип вверху боковой панели
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Over Kings", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Кнопки навигации
        self.farm_button = customtkinter.CTkButton(self.sidebar_frame, text="Фарм", command=lambda: self._switch_tab("farm"))
        self.farm_button.grid(row=1, column=0, padx=20, pady=10)

        self.skills_button = customtkinter.CTkButton(self.sidebar_frame, text="Навыки", command=lambda: self._switch_tab("skills"))
        self.skills_button.grid(row=2, column=0, padx=20, pady=10)

        self.log_button = customtkinter.CTkButton(self.sidebar_frame, text="Журнал", command=lambda: self._switch_tab("journal"))
        self.log_button.grid(row=3, column=0, padx=20, pady=10)

        self.stats_button = customtkinter.CTkButton(self.sidebar_frame, text="Статистика", command=lambda: self._switch_tab("stats"))
        self.stats_button.grid(row=4, column=0, padx=20, pady=10)

        # Добавляем кнопку Сброс памяти локаций между Статистикой и СТАРТ
        self.reset_memory_button = customtkinter.CTkButton(self.sidebar_frame, text="Сброс памяти", width=120, command=self.reset_location_memory)
        self.reset_memory_button.grid(row=5, column=0, padx=20, pady=10)

        # Добавляем кнопку СТАРТ
        self.toggle_button = customtkinter.CTkButton(self.sidebar_frame, text="СТАРТ (Insert)", width=120, command=self.toggle_running)
        self.toggle_button.grid(row=6, column=0, padx=20, pady=10)

        # Version label at the bottom
        version_label_bottom = customtkinter.CTkLabel(self.sidebar_frame, text=f"Production {VERSION}", font=customtkinter.CTkFont(size=10))
        spacer_frame = customtkinter.CTkFrame(self.sidebar_frame, fg_color="transparent")
        spacer_frame.grid(row=8, column=0, sticky="nsew")
        version_label_bottom.grid(row=9, column=0, padx=20, pady=(10, 20), sticky="s")

        # --- Content Frame ---
        self.content_frame = customtkinter.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, rowspan=2, padx=(0, 10), pady=10, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        # --- Header Frame within Content Area ---
        self.header_frame = customtkinter.CTkFrame(self.content_frame, corner_radius=0, fg_color="transparent", height=40)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 5))
        self.header_frame.grid_columnconfigure(0, weight=1)

        # --- Tab View Frame (holds the actual tab content) ---
        self.tab_view_frame = customtkinter.CTkFrame(self.content_frame, corner_radius=10, fg_color="transparent")
        self.tab_view_frame.grid(row=1, column=0, sticky="nsew")
        self.tab_view_frame.grid_columnconfigure(0, weight=1)
        self.tab_view_frame.grid_rowconfigure(0, weight=1)

        # Dictionary to hold tab frames
        self.tab_frames = {}

        # Create tab frames (initially hidden)
        self.tab_frames["farm"] = self._build_farm_tab()
        self.tab_frames["skills"] = self._build_skills_tab()
        self.tab_frames["journal"] = self._build_journal_tab()
        self.tab_frames["stats"] = self._build_stats_tab()

        # --- Status Bar ---
        self.status_frame = customtkinter.CTkFrame(self, height=30, corner_radius=10)
        self.status_frame.grid(row=1, column=1, padx=(0, 10), pady=(0, 10), sticky="sew")
        self.status_frame.grid_columnconfigure(1, weight=1)

        # Status Indicator
        self.status_indicator = customtkinter.CTkFrame(self.status_frame, width=10, height=10, fg_color="grey", corner_radius=5)
        self.status_indicator.grid(row=0, column=0, padx=(10, 5), pady=10)

        self.status_label = customtkinter.CTkLabel(self.status_frame, text="Бот не активен")
        self.status_label.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        # --- Initial Tab ---
        self._switch_tab("farm")


    def _switch_tab(self, tab_name):
        # Hide all tab frames
        for frame in self.tab_frames.values():
            frame.grid_forget()

        # Configure button states (optional visual feedback)
        buttons = {"farm": self.farm_button, "skills": self.skills_button, "journal": self.log_button, "stats": self.stats_button}
        for name, button in buttons.items():
             if name == tab_name:
                 # Highlight selected button (e.g., change color or use a specific state if theme supports it)
                 # button.configure(fg_color=customtkinter.ThemeManager.theme["CTkButton"]["hover_color"]) # Example: Use hover color
                 pass # CTkButton doesn't have a simple 'selected' state like ttk
             else:
                 # Reset other buttons to default appearance
                 # button.configure(fg_color=customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])
                 pass

        # Show the selected tab frame
        if tab_name in self.tab_frames:
            # Grid the tab frame inside the dedicated tab_view_frame
            self.tab_frames[tab_name].grid(row=0, column=0, sticky="nsew", padx=0, pady=0) # No padding needed here
        else:
            print(f"Error: Tab '{tab_name}' not found.")

    # Removed _create_rounded_frame as CTkFrame handles corners

    def _build_farm_tab(self):
        # Main frame for the farm tab content (intended for self.tab_view_frame)
        farm_tab_frame = customtkinter.CTkFrame(self.tab_view_frame, corner_radius=10, fg_color="transparent")
        farm_tab_frame.grid_columnconfigure(0, weight=1) # Allow first column to expand
        farm_tab_frame.grid_columnconfigure(1, weight=1) # Allow second column to expand
        farm_tab_frame.grid_rowconfigure(1, weight=1) # Allow sequence/param sections row to expand

        # Header with Start/Reset buttons (Now handled globally in self.header_frame)
        # header_placeholder = customtkinter.CTkFrame(farm_tab_frame, height=1, fg_color="transparent") # Optional placeholder if needed for spacing
        # header_placeholder.grid(row=0, column=0, columnspan=2, pady=5)

        # --- Location Sequence Section (Left Column) ---
        # Grid row starts from 1 (or 0 if no placeholder)
        loc_seq_frame = customtkinter.CTkFrame(farm_tab_frame, corner_radius=10)
        loc_seq_frame.grid(row=0, column=0, padx=(10, 5), pady=(0, 10), sticky="nsew") # Adjusted row and pady
        loc_seq_frame.grid_columnconfigure(0, weight=1)

        loc_seq_label = customtkinter.CTkLabel(loc_seq_frame, text="Последовательность локаций", font=customtkinter.CTkFont(size=14, weight="bold"))
        loc_seq_label.grid(row=0, column=0, padx=15, pady=(10, 10), sticky="w")

        # Dropdown menus for sequence
        for i, var in enumerate(self.dropdown_vars):
            option_menu = customtkinter.CTkOptionMenu(loc_seq_frame, variable=var, values=self.options)
            option_menu.grid(row=i+1, column=0, padx=15, pady=4, sticky="ew")

        # --- Parameters Section (Right Column) ---
        params_frame = customtkinter.CTkFrame(farm_tab_frame, corner_radius=10)
        params_frame.grid(row=0, column=1, padx=(5, 10), pady=(0, 10), sticky="nsew") # Adjusted row and pady
        params_frame.grid_columnconfigure(0, weight=1) # Allow checkboxes to align left

        params_label = customtkinter.CTkLabel(params_frame, text="Параметры", font=customtkinter.CTkFont(size=14, weight="bold"))
        params_label.grid(row=0, column=0, padx=15, pady=(10, 10), sticky="w")

        # Checkbuttons using CTkCheckBox
        # Group 1
        customtkinter.CTkCheckBox(params_frame, text="Сворачивать после запуска", variable=self.minimize_after_start).grid(row=1, column=0, padx=15, pady=3, sticky="w")
        cb_careful = customtkinter.CTkCheckBox(params_frame, text="Осторожный фарм (В разработке)", variable=self.careful_farming)
        cb_careful.grid(row=2, column=0, padx=15, pady=3, sticky="w")
        cb_careful.configure(state=tk.DISABLED)
        cb_hunt = customtkinter.CTkCheckBox(params_frame, text="Защита от засад", variable=self.save_drops).grid(row=3, column=0, padx=15, pady=3, sticky="w")
        cb_hunt = customtkinter.CTkCheckBox(params_frame, text="Охота на врагов (В разработке)", variable=self.hunt_enemies)
        cb_hunt.grid(row=4, column=0, padx=15, pady=3, sticky="w")
        cb_hunt.configure(state=tk.DISABLED)
        cb_protect = customtkinter.CTkCheckBox(params_frame, text="Защита бота в PVP (В разработке)", variable=self.protect_bot_pvp)
        cb_protect.grid(row=5, column=0, padx=15, pady=3, sticky="w")
        cb_protect.configure(state=tk.DISABLED)

        # Добавляем чекбокс для сохранения важных предметов
        customtkinter.CTkCheckBox(params_frame, text="Сохранять важные предметы", variable=self.keep_important_items).grid(row=6, column=0, padx=15, pady=3, sticky="w")

        # Group 2 (Farming targets)
        customtkinter.CTkLabel(params_frame, text="Цели фарма:").grid(row=7, column=0, padx=15, pady=(8, 3), sticky="w")
        # Add "Обычные" checkbox - assumed default, maybe enable later if needed
        # For now, just show the unimplemented ones as disabled
        # customtkinter.CTkCheckBox(params_frame, text="Обычные", variable=...).grid(row=7, column=0, padx=15, pady=3, sticky="w")
        cb_leg = customtkinter.CTkCheckBox(params_frame, text="Легендарки (В разработке)", variable=self.farm_legendary)
        cb_leg.grid(row=8, column=0, padx=15, pady=3, sticky="w") # Start row adjusted
        cb_leg.configure(state=tk.DISABLED)
        cb_myth = customtkinter.CTkCheckBox(params_frame, text="Мифический (В разработке)", variable=self.farm_mythic)
        cb_myth.grid(row=9, column=0, padx=15, pady=3, sticky="w")
        cb_myth.configure(state=tk.DISABLED)
        cb_div = customtkinter.CTkCheckBox(params_frame, text="Божественный (В разработке)", variable=self.farm_divine)
        cb_div.grid(row=10, column=0, padx=15, pady=3, sticky="w")
        cb_div.configure(state=tk.DISABLED)

        # Group 3 (Skipping & Item Handling)
        customtkinter.CTkLabel(params_frame, text="Прочее:").grid(row=11, column=0, padx=15, pady=(8, 3), sticky="w")
        customtkinter.CTkCheckBox(params_frame, text="Пропуск СТАН локаций", variable=self.skip_stun_locations).grid(row=12, column=0, padx=15, pady=3, sticky="w")
        customtkinter.CTkCheckBox(params_frame, text="Пропуск ЗАМЕДЛ. локаций", variable=self.skip_slow_locations).grid(row=13, column=0, padx=15, pady=3, sticky="w")
        customtkinter.CTkCheckBox(params_frame, text="Пропуск ЭПИКОВ", variable=self.skip_epic_locations).grid(row=14, column=0, padx=15, pady=3, sticky="w")
        customtkinter.CTkCheckBox(params_frame, text="Исп. темные кристаллы", variable=self.use_dark_crystals).grid(row=15, column=0, padx=15, pady=3, sticky="w")
        customtkinter.CTkCheckBox(params_frame, text="Исп. ВИП сундуки", variable=self.use_vip_chests).grid(row=16, column=0, padx=15, pady=3, sticky="w")
        customtkinter.CTkCheckBox(params_frame, text="Продавать сунд. ресурсов", variable=self.sell_resource_chests).grid(row=17, column=0, padx=15, pady=3, sticky="w")

        return farm_tab_frame


    def _build_skills_tab(self):
        # Main frame for the skills tab content (intended for self.tab_view_frame)
        skills_tab_frame = customtkinter.CTkFrame(self.tab_view_frame, corner_radius=10, fg_color="transparent")
        skills_tab_frame.grid_columnconfigure(0, weight=1)
        skills_tab_frame.grid_rowconfigure(1, weight=1) # Allow the main priority frame to expand

        # Reset button top right - REMOVED (now global)
        # reset_button = customtkinter.CTkButton(skills_tab_frame, text="Сбросить память", command=self.reset_location_memory, width=140)
        # reset_button.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ne") # Spanning not needed if only one column

        # --- Priority Settings Section ---
        priority_frame = customtkinter.CTkFrame(skills_tab_frame, corner_radius=10)
        priority_frame.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew") # Adjusted row and pady
        priority_frame.grid_columnconfigure(0, weight=1) # Left column
        priority_frame.grid_columnconfigure(1, weight=1) # Right column
        priority_frame.grid_rowconfigure(0, weight=0) # Title row
        priority_frame.grid_rowconfigure(1, weight=0) # Subtitle row
        priority_frame.grid_rowconfigure(2, weight=1) # Entries row container
        priority_frame.grid_rowconfigure(3, weight=0) # Button row

        priority_label = customtkinter.CTkLabel(priority_frame, text="Настройка приоритета", font=customtkinter.CTkFont(size=14, weight="bold"))
        priority_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 2), sticky="w")
        order_label = customtkinter.CTkLabel(priority_frame, text="Порядок активации: от 1 к 12")
        order_label.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="w")

        # Frame to contain the two columns of entries
        columns_frame = customtkinter.CTkFrame(priority_frame, fg_color="transparent")
        columns_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=5, sticky="nsew")
        columns_frame.grid_columnconfigure(0, weight=1)
        columns_frame.grid_columnconfigure(1, weight=1)

        # Left Column Frame
        left_frame = customtkinter.CTkFrame(columns_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        left_frame.grid_columnconfigure(1, weight=1) # Allow entry to expand
        customtkinter.CTkLabel(left_frame, text="Левая", font=customtkinter.CTkFont(size=12, weight="bold")).grid(row=0, column=0, columnspan=2, pady=(0, 5), sticky="w")

        # Right Column Frame
        right_frame = customtkinter.CTkFrame(columns_frame, fg_color="transparent")
        right_frame.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        right_frame.grid_columnconfigure(1, weight=1) # Allow entry to expand
        customtkinter.CTkLabel(right_frame, text="Правая", font=customtkinter.CTkFont(size=12, weight="bold")).grid(row=0, column=0, columnspan=2, pady=(0, 5), sticky="w")

        # Create C1-C12 entries using CTkEntry
        for i in range(12):
            # Left entry
            customtkinter.CTkLabel(left_frame, text=f"C{i+1}", width=25).grid(row=i+1, column=0, padx=(0, 5), pady=2, sticky="w")
            entry_left = customtkinter.CTkEntry(left_frame, textvariable=self.skill_priorities_left[i], width=50, justify=tk.CENTER, state=tk.DISABLED)
            entry_left.grid(row=i+1, column=1, padx=(0, 0), pady=2, sticky="ew")

            # Right entry
            customtkinter.CTkLabel(right_frame, text=f"C{i+1}", width=25).grid(row=i+1, column=0, padx=(0, 5), pady=2, sticky="w")
            entry_right = customtkinter.CTkEntry(right_frame, textvariable=self.skill_priorities_right[i], width=50, justify=tk.CENTER, state=tk.DISABLED)
            entry_right.grid(row=i+1, column=1, padx=(0, 0), pady=2, sticky="ew")

        # Clear button
        clear_button = customtkinter.CTkButton(priority_frame, text="Очистить", command=self._clear_skill_priorities, width=100, state=tk.DISABLED)
        clear_button.grid(row=3, column=0, columnspan=2, padx=20, pady=(10, 10))

        # Add label indicating it's under development
        dev_label = customtkinter.CTkLabel(priority_frame, text="(В разработке)", font=customtkinter.CTkFont(size=10))
        dev_label.grid(row=4, column=0, columnspan=2, padx=20, pady=(0, 10))

        return skills_tab_frame


    def _build_journal_tab(self):
        # Main frame for the journal tab content (intended for self.tab_view_frame)
        journal_tab_frame = customtkinter.CTkFrame(self.tab_view_frame, corner_radius=10, fg_color="transparent")
        journal_tab_frame.grid_columnconfigure(0, weight=1)
        journal_tab_frame.grid_rowconfigure(0, weight=1)

        # --- Log Display Section ---
        log_frame = customtkinter.CTkFrame(journal_tab_frame, corner_radius=10)
        log_frame.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew")
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        # Use CTkTextbox with dark theme colors
        self.log_text = customtkinter.CTkTextbox(
            log_frame,
            state="disabled",
            wrap=tk.WORD,
            fg_color="#2b2b2b",  # Темный фон
            text_color="#ffffff",  # Белый текст
            font=("Courier", 10)  # Моноширинный шрифт для лучшей читаемости логов
        )
        self.log_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        return journal_tab_frame

    def _build_stats_tab(self):
        """Creates the Statistics tab content."""
        stats_tab_frame = customtkinter.CTkFrame(self.tab_view_frame, corner_radius=10, fg_color="transparent")
        stats_tab_frame.grid_columnconfigure(0, weight=1)
        stats_tab_frame.grid_rowconfigure(0, weight=1)  # Позволяем содержимому расширяться

        # Создаем скроллируемый фрейм
        scrollable_frame = customtkinter.CTkScrollableFrame(stats_tab_frame)
        scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        scrollable_frame.grid_columnconfigure(0, weight=1)

        # --- General Statistics ---
        general_stats_frame = customtkinter.CTkFrame(scrollable_frame, corner_radius=10)
        general_stats_frame.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="ew")
        general_stats_frame.grid_columnconfigure(1, weight=1)

        general_label = customtkinter.CTkLabel(general_stats_frame, text="Общая статистика", font=customtkinter.CTkFont(size=14, weight="bold"))
        general_label.grid(row=0, column=0, columnspan=2, padx=15, pady=(10, 15), sticky="w")

        # Total Uptime
        customtkinter.CTkLabel(general_stats_frame, text="Время работы бота:").grid(row=1, column=0, padx=15, pady=5, sticky="w")
        self.uptime_label = customtkinter.CTkLabel(general_stats_frame, text="00:00:00")
        self.uptime_label.grid(row=1, column=1, padx=15, pady=5, sticky="w")

        # Total Instances Completed
        customtkinter.CTkLabel(general_stats_frame, text="Пройдено суммарно инстансов:").grid(row=2, column=0, padx=15, pady=5, sticky="w")
        self.instances_completed_label = customtkinter.CTkLabel(general_stats_frame, textvariable=self.instances_count_var)
        self.instances_completed_label.grid(row=2, column=1, padx=15, pady=5, sticky="w")

        # --- Item Statistics ---
        item_stats_frame = customtkinter.CTkFrame(scrollable_frame, corner_radius=10)
        item_stats_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        item_stats_frame.grid_columnconfigure(1, weight=1)

        item_label = customtkinter.CTkLabel(item_stats_frame, text="Статистика предметов", font=customtkinter.CTkFont(size=14, weight="bold"))
        item_label.grid(row=0, column=0, columnspan=2, padx=15, pady=(10, 15), sticky="w")

        # Total Items Banked
        customtkinter.CTkLabel(item_stats_frame, text="Всего сундуков в банке:").grid(row=1, column=0, padx=15, pady=5, sticky="w")
        customtkinter.CTkLabel(item_stats_frame, textvariable=self.item_stats_vars["total_banked"]).grid(row=1, column=1, padx=15, pady=5, sticky="w")

        # Total Items Sold
        customtkinter.CTkLabel(item_stats_frame, text="Всего сундуков продано:").grid(row=2, column=0, padx=15, pady=5, sticky="w")
        customtkinter.CTkLabel(item_stats_frame, textvariable=self.item_stats_vars["total_sold"]).grid(row=2, column=1, padx=15, pady=5, sticky="w")

        # Total VIP Chests Opened
        customtkinter.CTkLabel(item_stats_frame, text="Открыто VIP сундуков:").grid(row=3, column=0, padx=15, pady=5, sticky="w")
        customtkinter.CTkLabel(item_stats_frame, textvariable=self.item_stats_vars["total_opened_vip"]).grid(row=3, column=1, padx=15, pady=5, sticky="w")

        # Total Earnings from Sales
        customtkinter.CTkLabel(item_stats_frame, text="Заработано с продаж:").grid(row=4, column=0, padx=15, pady=5, sticky="w")
        earnings_label = customtkinter.CTkLabel(item_stats_frame, textvariable=self.item_stats_vars["total_sold_earnings"])
        earnings_label.grid(row=4, column=1, padx=15, pady=5, sticky="w")

        # Dark Crystals Used
        customtkinter.CTkLabel(item_stats_frame, text="Использовано темных кристаллов:").grid(row=5, column=0, padx=15, pady=5, sticky="w")
        customtkinter.CTkLabel(item_stats_frame, textvariable=self.item_stats_vars["total_dark_crystals_used"]).grid(row=5, column=1, padx=15, pady=5, sticky="w")

        # Dark Crystals Earned
        customtkinter.CTkLabel(item_stats_frame, text="Получено темных кристаллов:").grid(row=6, column=0, padx=15, pady=5, sticky="w")
        customtkinter.CTkLabel(item_stats_frame, textvariable=self.item_stats_vars["total_dark_crystals_earned"]).grid(row=6, column=1, padx=15, pady=5, sticky="w")

        # --- Per Region Statistics --- 
        region_stats_frame = customtkinter.CTkFrame(scrollable_frame, corner_radius=10)
        region_stats_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        region_stats_frame.grid_columnconfigure(1, weight=0)
        region_stats_frame.grid_columnconfigure(2, weight=1)

        region_title_label = customtkinter.CTkLabel(region_stats_frame, text="Статистика по регионам", font=customtkinter.CTkFont(size=14, weight="bold"))
        region_title_label.grid(row=0, column=0, columnspan=3, padx=15, pady=(10, 15), sticky="w")

        # Header row
        customtkinter.CTkLabel(region_stats_frame, text="Регион").grid(row=1, column=0, padx=15, pady=2, sticky="w")
        customtkinter.CTkLabel(region_stats_frame, text="Пройдено").grid(row=1, column=1, padx=5, pady=2, sticky="w")
        customtkinter.CTkLabel(region_stats_frame, text="Затрачено времени").grid(row=1, column=2, padx=5, pady=2, sticky="w")

        current_row = 2
        for display_name, internal_key in zip(self.functions_mapping.keys(), self.region_keys):
            customtkinter.CTkLabel(region_stats_frame, text=display_name + ":").grid(row=current_row, column=0, padx=15, pady=2, sticky="w")
            inst_label = customtkinter.CTkLabel(region_stats_frame, textvariable=self.region_instances_count[internal_key])
            inst_label.grid(row=current_row, column=1, padx=5, pady=2, sticky="w")
            time_label = customtkinter.CTkLabel(region_stats_frame, textvariable=self.region_time_str[internal_key])
            time_label.grid(row=current_row, column=2, padx=5, pady=2, sticky="w")
            self.region_time_spent[internal_key].trace_add("write", lambda *args, key=internal_key: self._update_region_time_label(key))
            current_row += 1

        # --- Per Region Item Statistics ---
        region_items_frame = customtkinter.CTkFrame(scrollable_frame, corner_radius=10)
        region_items_frame.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew")
        region_items_frame.grid_columnconfigure(1, weight=0)
        region_items_frame.grid_columnconfigure(2, weight=0)
        region_items_frame.grid_columnconfigure(3, weight=0)
        region_items_frame.grid_columnconfigure(4, weight=1)

        region_items_title = customtkinter.CTkLabel(region_items_frame, text="Статистика предметов по регионам", font=customtkinter.CTkFont(size=14, weight="bold"))
        region_items_title.grid(row=0, column=0, columnspan=5, padx=15, pady=(10, 15), sticky="w")

        # Header row for items
        customtkinter.CTkLabel(region_items_frame, text="Регион").grid(row=1, column=0, padx=15, pady=2, sticky="w")
        customtkinter.CTkLabel(region_items_frame, text="В банке").grid(row=1, column=1, padx=5, pady=2, sticky="w")
        customtkinter.CTkLabel(region_items_frame, text="Продано").grid(row=1, column=2, padx=5, pady=2, sticky="w")
        customtkinter.CTkLabel(region_items_frame, text="VIP").grid(row=1, column=3, padx=5, pady=2, sticky="w")
        customtkinter.CTkLabel(region_items_frame, text="Заработано").grid(row=1, column=4, padx=5, pady=2, sticky="w")

        current_row = 2
        for display_name, internal_key in zip(self.functions_mapping.keys(), self.region_keys):
            customtkinter.CTkLabel(region_items_frame, text=display_name + ":").grid(row=current_row, column=0, padx=15, pady=2, sticky="w")
            
            # Items banked
            banked_label = customtkinter.CTkLabel(region_items_frame, textvariable=self.region_stats[internal_key]["banked"])
            banked_label.grid(row=current_row, column=1, padx=5, pady=2, sticky="w")
            
            # Items sold
            sold_label = customtkinter.CTkLabel(region_items_frame, textvariable=self.region_stats[internal_key]["sold"])
            sold_label.grid(row=current_row, column=2, padx=5, pady=2, sticky="w")
            
            # VIP chests opened
            vip_label = customtkinter.CTkLabel(region_items_frame, textvariable=self.region_stats[internal_key]["opened_vip"])
            vip_label.grid(row=current_row, column=3, padx=5, pady=2, sticky="w")
            
            # Earnings
            earnings_label = customtkinter.CTkLabel(region_items_frame, textvariable=self.region_stats[internal_key]["earnings"])
            earnings_label.grid(row=current_row, column=4, padx=5, pady=2, sticky="w")
            
            current_row += 1

        # Reset button
        reset_stats_button = customtkinter.CTkButton(region_items_frame, text="Сбросить всю статистику", command=self._reset_statistics)
        reset_stats_button.grid(row=current_row, column=0, columnspan=5, pady=(10,10))

        # Daily earnings
        daily_earnings_frame = customtkinter.CTkFrame(scrollable_frame)
        daily_earnings_frame.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ew")
        daily_earnings_frame.grid_columnconfigure(0, weight=1)
        
        daily_earnings_label = customtkinter.CTkLabel(daily_earnings_frame, text="Заработок за день:")
        daily_earnings_label.pack(side="left", padx=5)
        
        daily_gold_label = customtkinter.CTkLabel(daily_earnings_frame, textvariable=self.item_stats_vars["earnings_daily_gold"])
        daily_gold_label.pack(side="left")
        customtkinter.CTkLabel(daily_earnings_frame, text="з").pack(side="left")
        
        daily_silver_label = customtkinter.CTkLabel(daily_earnings_frame, textvariable=self.item_stats_vars["earnings_daily_silver"])
        daily_silver_label.pack(side="left")
        customtkinter.CTkLabel(daily_earnings_frame, text="с").pack(side="left")
        
        daily_copper_label = customtkinter.CTkLabel(daily_earnings_frame, textvariable=self.item_stats_vars["earnings_daily_copper"])
        daily_copper_label.pack(side="left")
        customtkinter.CTkLabel(daily_earnings_frame, text="м").pack(side="left")

        # Monthly earnings
        monthly_earnings_frame = customtkinter.CTkFrame(scrollable_frame)
        monthly_earnings_frame.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="ew")
        monthly_earnings_frame.grid_columnconfigure(0, weight=1)
        
        monthly_earnings_label = customtkinter.CTkLabel(monthly_earnings_frame, text="Заработок за месяц:")
        monthly_earnings_label.pack(side="left", padx=5)
        
        monthly_gold_label = customtkinter.CTkLabel(monthly_earnings_frame, textvariable=self.item_stats_vars["earnings_monthly_gold"])
        monthly_gold_label.pack(side="left")
        customtkinter.CTkLabel(monthly_earnings_frame, text="з").pack(side="left")
        
        monthly_silver_label = customtkinter.CTkLabel(monthly_earnings_frame, textvariable=self.item_stats_vars["earnings_monthly_silver"])
        monthly_silver_label.pack(side="left")
        customtkinter.CTkLabel(monthly_earnings_frame, text="с").pack(side="left")
        
        monthly_copper_label = customtkinter.CTkLabel(monthly_earnings_frame, textvariable=self.item_stats_vars["earnings_monthly_copper"])
        monthly_copper_label.pack(side="left")
        customtkinter.CTkLabel(monthly_earnings_frame, text="м").pack(side="left")

        # Reset buttons section
        reset_buttons_frame = customtkinter.CTkFrame(scrollable_frame, corner_radius=10)
        reset_buttons_frame.grid(row=6, column=0, padx=10, pady=(0, 10), sticky="ew")
        reset_buttons_frame.grid_columnconfigure(0, weight=1)

        # Reset stats button
        reset_stats_button = customtkinter.CTkButton(reset_buttons_frame, text="Сброс статистики", command=self._reset_statistics)
        reset_stats_button.grid(row=0, column=0, pady=(10,10))

        return stats_tab_frame

    def _reset_statistics(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите сбросить ВСЮ статистику (время работы, инстансы)?"):
            self.total_uptime_seconds = 0
            self.start_time = None # Reset current session timer as well
            self.instances_count_var.set(0)
            for key in self.region_keys:
                self.region_instances_count[key].set(0)
                # self.region_time_spent[key].set(0.0) # DO NOT RESET TIME SPENT
                # self.region_time_str[key].set("00:00:00") # trace should handle this
            self.save_statistics() # Save the reset state
            self.log_message("Статистика (инстансы и общее время) сброшена. Время по регионам сохранено.")

    def _update_region_time_label(self, region_key):
        """Formats seconds from DoubleVar into HH:MM:SS for the label string var."""
        total_seconds = int(self.region_time_spent[region_key].get())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        self.region_time_str[region_key].set(time_str)

    def _clear_skill_priorities(self):
        for var in self.skill_priorities_left:
            var.set("0")
        for var in self.skill_priorities_right:
            var.set("0")
        self.log_message("Приоритеты навыков сброшены.")


    def log_message(self, message):
        """Логирует сообщение в GUI и файл."""
        current_time = datetime.datetime.now().strftime('[%H:%M:%S]')
        full_message = f"{current_time} {message}"
        print(full_message)

        def update_log_widget():
            if hasattr(self, 'log_text') and isinstance(self.log_text, customtkinter.CTkTextbox):
                try:
                    self.log_text.configure(state="normal")
                    self.log_text.insert(tk.END, full_message + "\n")
                    self.log_text.see(tk.END)
                    self.log_text.configure(state="disabled")
                except Exception as e:
                    print(f"Ошибка обновления текстового поля лога: {e}")
        
        self.after(0, update_log_widget)

        try:
            log_dir = "logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            log_file = os.path.join(log_dir, f"log_{today}.txt")
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(full_message + "\n")
        except Exception as e:
            print(f"Ошибка при записи в лог-файл: {str(e)}")


    def toggle_running(self):
        if not self.running:
            self.running = True
            self.current_index = 0  # Сброс индекса при запуске
            self.toggle_button.configure(text="СТОП (Insert)", fg_color="red")
            self.status_label.configure(text="Бот активен")
            self.status_indicator.configure(fg_color="#32CD32")
            self.log_message("Запускаем бота.")
            
            if self.minimize_after_start.get():
                self.after(100, self.iconify)
            
            if self.start_time is None:
                self.start_time = time.time()
                
            # Запускаем мониторинг процесса в отдельном потоке
            threading.Thread(target=self.connection_monitor, daemon=True).start()
            # Запускаем обработчик ошибок в отдельном потоке
            threading.Thread(target=self.vjuh_treatment, daemon=True).start()
            # Запускаем основной цикл через after
            self.after(100, self.continuous_loop)
        else:
            self.running = False
            self.scenario_running = False
            self.toggle_button.configure(text="СТАРТ (Insert)", fg_color=customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])
            self.status_label.configure(text="Бот не активен")
            self.status_indicator.configure(fg_color="grey")
            self.log_message("Останавливаем бота.")

            if self.start_time is not None:
                self.total_uptime_seconds += time.time() - self.start_time
                self.start_time = None

    # --- Keep other methods like vjuh_treatment, continuous_loop, reset_location_memory, save_location_memory, load/save_settings etc. ---
    # Make sure they reference 'self' correctly and use customtkinter widgets if needed.
    # The logic inside these methods should remain unchanged as requested.

    def vjuh_treatment(self):
        """Обработка ошибок подключения (Вжух и Error2032)"""
        while self.running:
            if not self.running:
                break
            vjuh = find_template("vjuh", self)
            error2032 = find_template("error2032", self)
            if not vjuh and not error2032:
                time.sleep(10)
                continue
            else:
                if vjuh:
                    self.log_message("[DEBUG vjuh_treatment] Обнаружена ошибка 'Вжух'!")
                if error2032:
                    self.log_message("[DEBUG vjuh_treatment] Обнаружена ошибка Error2032!")
                    
                vjuh_ok = find_template("vjuh_ok", self)
                if vjuh_ok:
                    human_click(*vjuh_ok)
                    self.log_message("[DEBUG vjuh_treatment] Нажата кнопка ОК")
                    time.sleep(3)
                    PostFarm.cache_cleaner(self)
        
        # Планируем следующую проверку
        self.after(1000, self.check_vjuh)

    def check_connection(self):
        """Проверка соединения через Tkinter after"""
        if self.running:
            try:
                overkings_running = False
                for proc in psutil.process_iter(['name']):
                    try:
                        if proc.info['name'] == 'Overkings.exe':
                            overkings_running = True
                            break
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

                if not overkings_running:
                    self.log_message("[DEBUG check_connection] Процесс Overkings.exe не найден! Перезапускаем клиент...")
                    self.check_vjuh()
            except Exception as e:
                self.log_message(f"[ERROR check_connection] Ошибка в мониторинге процесса: {e}")
        
        # Планируем следующую проверку
        self.after(2000, self.check_connection)

    def continuous_loop(self):
        """Обработка последовательности действий через Tkinter after"""
        if not self.running:
            return

        if not self.scenario_running:
            func_name = self.dropdown_vars[self.current_index].get()
            if func_name in self.functions_mapping:
                self.log_message(f"[DEBUG continuous_loop]Очередь {self.current_index+1}: запуск сценария '{func_name}'")
                self.scenario_running = True
                # Вместо создания потока запускаем функцию напрямую
                self.functions_mapping[func_name]()
            else:
                self.log_message(f"[DEBUG continuous_loop]Очередь {self.current_index+1}: пропущено (пустой выбор)")

            self.current_index = (self.current_index + 1) % len(self.dropdown_vars)

            if self.current_index == 0 and not self.dropdown_vars[0].get():
                self.log_message("[DEBUG continuous_loop]Цикл завершен (первый слот пуст). Остановка.")
                self.toggle_running()
                return

        # Планируем следующую итерацию
        self.after(1000, self.continuous_loop)

    def reset_location_memory(self):
        """Сбрасывает память локаций после подтверждения."""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите сбросить память пройденных локаций? Откат будет сброшен."):
            self.completed_locations = {}
            self.save_location_memory()
            self.log_message("Память локаций сброшена.")


    def load_location_memory(self):
        """Loads completed location timestamps from a JSON file."""
        try:
            if os.path.exists(self.location_memory_file):
                with open(self.location_memory_file, 'r') as f:
                    # Ensure values are loaded as floats (timestamps)
                    loaded_data = json.load(f)
                    self.completed_locations = {k: float(v) for k, v in loaded_data.items()}

                    # Optional: Clean up very old entries
                    current_time = time.time()
                    memory_duration_hours = self.location_memory_duration # Use the variable
                    self.completed_locations = {
                        loc: ts for loc, ts in self.completed_locations.items()
                        if current_time - ts < memory_duration_hours * 3600 # Keep memory for configured duration
                    }
                self.log_message("Память локаций загружена.")
            else:
                self.log_message("Файл памяти локаций не найден, создана новая память.")
                self.completed_locations = {} # Ensure it's initialized
        except json.JSONDecodeError as e:
             self.log_message(f"[ERROR] Ошибка декодирования JSON файла памяти локаций: {e}")
             self.completed_locations = {}
        except ValueError as e:
             self.log_message(f"[ERROR] Ошибка преобразования времени в файле памяти локаций: {e}")
             self.completed_locations = {}
        except Exception as e:
            self.log_message(f"[ERROR] Ошибка загрузки памяти локаций: {e}")
            self.completed_locations = {}

    # Keep update_memory_duration from previous edit if needed for settings tab
    # def update_memory_duration(self, event=None): ...

    def save_location_memory(self):
        """Saves the current location memory timestamps to a JSON file."""
        try:
            with open(self.location_memory_file, 'w') as f:
                json.dump(self.completed_locations, f, indent=4)
        except Exception as e:
            self.log_message(f"[ERROR] Ошибка сохранения памяти локаций: {e}")

    def load_settings(self):
        """Loads bot settings from a JSON file."""
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", 'r') as f:
                    settings = json.load(f)
                    # Load settings using .get() with defaults
                    self.minimize_after_start.set(settings.get('minimize_after_start', False))
                    self.careful_farming.set(settings.get('careful_farming', False))
                    self.save_drops.set(settings.get('save_drops', True))
                    self.hunt_enemies.set(settings.get('hunt_enemies', False))
                    self.protect_bot_pvp.set(settings.get('protect_bot_pvp', False))
                    self.farm_legendary.set(settings.get('farm_legendary', False))
                    self.farm_mythic.set(settings.get('farm_mythic', False))
                    self.farm_divine.set(settings.get('farm_divine', False))
                    self.skip_stun_locations.set(settings.get('skip_stun_locations', True))
                    self.skip_slow_locations.set(settings.get('skip_slow_locations', True))
                    self.skip_epic_locations.set(settings.get('skip_epic_locations', True))
                    self.use_dark_crystals.set(settings.get('use_dark_crystals', True))
                    self.use_vip_chests.set(settings.get('use_vip_chests', True))
                    self.sell_resource_chests.set(settings.get('sell_resource_chests', False))
                    self.keep_important_items.set(settings.get('keep_important_items', True))
                    # Load dropdown sequence
                    dropdown_values = settings.get('dropdown_sequence', [""] * 8)
                    for i, var in enumerate(self.dropdown_vars):
                         if i < len(dropdown_values):
                             var.set(dropdown_values[i])
                    # Load skill priorities
                    skill_left = settings.get('skill_priorities_left', ["0"] * 12)
                    skill_right = settings.get('skill_priorities_right', ["0"] * 12)
                    for i in range(12):
                         if i < len(skill_left): self.skill_priorities_left[i].set(skill_left[i])
                         if i < len(skill_right): self.skill_priorities_right[i].set(skill_right[i])

                    # Load auto-start settings
                    self.auto_start_bot.set(settings.get('auto_start_bot', False))
                    self.auto_start_scenario.set(settings.get('auto_start_scenario', "")) # Use empty default if sequence

                self.log_message("Настройки загружены.")
            else:
                self.log_message("Файл настроек не найден, используются значения по умолчанию.")
                # Save default settings if file doesn't exist
                self.save_settings()
        except json.JSONDecodeError as e:
            self.log_message(f"[ERROR] Ошибка декодирования JSON файла настроек: {e}")
        except Exception as e:
            self.log_message(f"[ERROR] Ошибка загрузки настроек: {e}")

    def save_settings(self):
        """Saves the current bot settings to a JSON file."""
        settings = {
            'minimize_after_start': self.minimize_after_start.get(),
            'careful_farming': self.careful_farming.get(),
            'save_drops': self.save_drops.get(),
            'hunt_enemies': self.hunt_enemies.get(),
            'protect_bot_pvp': self.protect_bot_pvp.get(),
            'farm_legendary': self.farm_legendary.get(),
            'farm_mythic': self.farm_mythic.get(),
            'farm_divine': self.farm_divine.get(),
            'skip_stun_locations': self.skip_stun_locations.get(),
            'skip_slow_locations': self.skip_slow_locations.get(),
            'skip_epic_locations': self.skip_epic_locations.get(),
            'use_dark_crystals': self.use_dark_crystals.get(),
            'use_vip_chests': self.use_vip_chests.get(),
            'sell_resource_chests': self.sell_resource_chests.get(),
            'keep_important_items': self.keep_important_items.get(),
            'dropdown_sequence': [var.get() for var in self.dropdown_vars],
            'skill_priorities_left': [var.get() for var in self.skill_priorities_left],
            'skill_priorities_right': [var.get() for var in self.skill_priorities_right],
            'auto_start_bot': self.auto_start_bot.get(),
            # Save the first dropdown's value as the auto-start scenario for simplicity
            'auto_start_scenario': self.dropdown_vars[0].get() if self.dropdown_vars else "",
        }
        try:
            with open("settings.json", 'w') as f:
                json.dump(settings, f, indent=4)
            # self.log_message("Настройки сохранены.") # Optional: uncomment if needed
        except Exception as e:
            self.log_message(f"[ERROR] Ошибка сохранения настроек: {e}")

    def on_closing(self):
        """Handles window closing: saves settings and stops threads."""
        self.log_message("Завершение работы...")
        self.running = False # Signal threads to stop

        # Save settings before exiting
        self.save_settings()
        self.save_location_memory()
        self.save_statistics() # Save statistics

        # Wait briefly for threads to notice the flag (optional)
        # time.sleep(0.1) # Daemon threads should exit automatically

        self.destroy() # Close the Tkinter window

    def _update_stats(self):
        """Обновляет статистику каждую секунду."""
        try:
            # Обновляем общее время работы
            current_session_uptime = 0
            if self.start_time is not None:
                current_session_uptime = time.time() - self.start_time
            
            total_seconds = int(self.total_uptime_seconds + current_session_uptime)
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            uptime_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            
            if hasattr(self, 'uptime_label'):
                self.uptime_label.configure(text=uptime_str)
            
            # Обновляем время по регионам
            if self.current_region_key and self.current_region_start_time:
                time_spent = time.time() - self.current_region_start_time
                self.region_time_spent[self.current_region_key].set(
                    self.region_time_spent[self.current_region_key].get() + time_spent
                )
                self.current_region_start_time = time.time()  # Сбрасываем для следующего обновления
            
            # Планируем следующее обновление
            self.after(1000, self._update_stats)
        except Exception as e:
            self.log_message(f"[ERROR _update_stats] Ошибка обновления статистики: {e}")
            # Всё равно планируем следующее обновление
            self.after(1000, self._update_stats)

    def load_statistics(self):
        """Загружает статистику из файла"""
        try:
            # Инициализация базовых значений по умолчанию
            self.total_uptime_seconds = 0.0
            self.instances_count_var.set(0)
            
            # Инициализация статистики по регионам
            for key in self.region_keys:
                if key not in self.region_instances_count:
                    self.region_instances_count[key] = tk.IntVar(value=0)
                if key not in self.region_time_spent:
                    self.region_time_spent[key] = tk.DoubleVar(value=0.0)
                if key not in self.region_time_str:
                    self.region_time_str[key] = tk.StringVar(value="00:00:00")
            
            # Инициализация статистики сундуков
            self.chest_stats = {
                "banked": {region: {} for region in self.region_keys},
                "sold": {region: {} for region in self.region_keys},
                "opened_vip": {region: 0 for region in self.region_keys},
                "dark_crystals_used": {region: 0 for region in self.region_keys},
                "dark_crystals_earned": {region: 0 for region in self.region_keys},
                "sold_earnings": {
                    "daily": {region: {"gold": 0, "silver": 0, "copper": 0} for region in self.region_keys},
                    "monthly": {region: {"gold": 0, "silver": 0, "copper": 0} for region in self.region_keys},
                    "total": {region: {"gold": 0, "silver": 0, "copper": 0} for region in self.region_keys},
                    "last_reset": {"daily": None, "monthly": None}
                }
            }
            
            # Инициализация статистики предметов
            if not hasattr(self, 'item_stats_vars'):
                self.item_stats_vars = {
                    "total_banked": tk.IntVar(value=0),
                    "total_sold": tk.IntVar(value=0),
                    "total_opened_vip": tk.IntVar(value=0),
                    "total_sold_earnings": tk.IntVar(value=0),
                    "total_dark_crystals_used": tk.IntVar(value=0),
                    "total_dark_crystals_earned": tk.IntVar(value=0),
                    "earnings_daily_gold": tk.IntVar(value=0),
                    "earnings_daily_silver": tk.IntVar(value=0),
                    "earnings_daily_copper": tk.IntVar(value=0),
                    "earnings_monthly_gold": tk.IntVar(value=0),
                    "earnings_monthly_silver": tk.IntVar(value=0),
                    "earnings_monthly_copper": tk.IntVar(value=0),
                    "earnings_total_gold": tk.IntVar(value=0),
                    "earnings_total_silver": tk.IntVar(value=0),
                    "earnings_total_copper": tk.IntVar(value=0)
                }
            
            # Загрузка сохраненной статистики из файла
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
                    
                    # Загрузка базовой статистики
                    self.total_uptime_seconds = float(stats.get('total_uptime_seconds', 0.0))
                    self.instances_count_var.set(int(stats.get('total_instances', 0)))
                    
                    # Загрузка статистики по регионам
                    region_instances = stats.get('region_instances', {})
                    region_times = stats.get('region_times', {})
                    
                    for key in self.region_keys:
                        self.region_instances_count[key].set(int(region_instances.get(key, 0)))
                        self.region_time_spent[key].set(float(region_times.get(key, 0.0)))
                        self._update_region_time_label(key)
                    
                    # Загрузка статистики сундуков
                    if 'chest_stats' in stats:
                        loaded_chest_stats = stats['chest_stats']
                        # Обновляем только существующие значения, сохраняя структуру по умолчанию
                        for category in ['banked', 'sold', 'opened_vip', 'dark_crystals_used', 'dark_crystals_earned']:
                            if category in loaded_chest_stats:
                                for region in self.region_keys:
                                    if region in loaded_chest_stats[category]:
                                        self.chest_stats[category][region] = loaded_chest_stats[category][region]
                        
                        # Загрузка статистики продаж
                        if 'sold_earnings' in loaded_chest_stats:
                            for period in ['daily', 'monthly', 'total']:
                                if period in loaded_chest_stats['sold_earnings']:
                                    for region in self.region_keys:
                                        if region in loaded_chest_stats['sold_earnings'][period]:
                                            self.chest_stats['sold_earnings'][period][region] = loaded_chest_stats['sold_earnings'][period][region]
                            
                            if 'last_reset' in loaded_chest_stats['sold_earnings']:
                                self.chest_stats['sold_earnings']['last_reset'] = loaded_chest_stats['sold_earnings']['last_reset']
                    
                    self._update_total_item_stats_display()
                    self.log_message("[DEBUG load_statistics] Статистика загружена успешно")
            else:
                self.log_message("[DEBUG load_statistics] Файл статистики не найден, используются значения по умолчанию")
                self.save_statistics()
                
        except json.JSONDecodeError as e:
            self.log_message(f"[DEBUG load_statistics] Ошибка при чтении файла статистики (неверный формат JSON): {str(e)}")
            self.save_statistics()  # Сохраняем значения по умолчанию
        except Exception as e:
            self.log_message(f"[DEBUG load_statistics] Ошибка при загрузке статистики: {str(e)}")
            self.save_statistics()  # Сохраняем значения по умолчанию

    def save_statistics(self):
        """Сохраняет статистику в файл"""
        try:
            self.log_message("[DEBUG save_statistics] Начало сохранения статистики...")
            
            # Подготавливаем chest_stats для сериализации
            serializable_chest_stats = {
                "banked": {},
                "sold": {},
                "opened_vip": {},
                "dark_crystals_used": {},
                "dark_crystals_earned": {},
                "sold_earnings": {
                    "daily": {},
                    "monthly": {},
                    "total": {},
                    "last_reset": {"daily": None, "monthly": None}
                }
            }
            
            if hasattr(self, 'chest_stats'):
                # Копируем banked и sold
                for region in self.region_keys:
                    serializable_chest_stats["banked"][region] = {}
                    serializable_chest_stats["sold"][region] = {}
                    if region in self.chest_stats.get("banked", {}):
                        for chest_type, value in self.chest_stats["banked"][region].items():
                            if isinstance(value, tk.IntVar):
                                serializable_chest_stats["banked"][region][chest_type] = value.get()
                            else:
                                serializable_chest_stats["banked"][region][chest_type] = value
                    if region in self.chest_stats.get("sold", {}):
                        for chest_type, value in self.chest_stats["sold"][region].items():
                            if isinstance(value, tk.IntVar):
                                serializable_chest_stats["sold"][region][chest_type] = value.get()
                            else:
                                serializable_chest_stats["sold"][region][chest_type] = value
                
                # Копируем opened_vip, dark_crystals_used, dark_crystals_earned
                for stat_type in ["opened_vip", "dark_crystals_used", "dark_crystals_earned"]:
                    serializable_chest_stats[stat_type] = {}
                    for region in self.region_keys:
                        if region in self.chest_stats.get(stat_type, {}):
                            value = self.chest_stats[stat_type][region]
                            if isinstance(value, tk.IntVar):
                                serializable_chest_stats[stat_type][region] = value.get()
                            else:
                                serializable_chest_stats[stat_type][region] = value
                        else:
                            serializable_chest_stats[stat_type][region] = 0
                
                # Копируем sold_earnings
                for period in ["daily", "monthly", "total"]:
                    serializable_chest_stats["sold_earnings"][period] = {}
                    for region in self.region_keys:
                        if region in self.chest_stats.get("sold_earnings", {}).get(period, {}):
                            serializable_chest_stats["sold_earnings"][period][region] = {
                                "gold": self.chest_stats["sold_earnings"][period][region].get("gold", 0),
                                "silver": self.chest_stats["sold_earnings"][period][region].get("silver", 0),
                                "copper": self.chest_stats["sold_earnings"][period][region].get("copper", 0)
                            }
                        else:
                            serializable_chest_stats["sold_earnings"][period][region] = {
                                "gold": 0,
                                "silver": 0,
                                "copper": 0
                            }
                
                # Копируем last_reset
                if "sold_earnings" in self.chest_stats and "last_reset" in self.chest_stats["sold_earnings"]:
                    serializable_chest_stats["sold_earnings"]["last_reset"] = {
                        "daily": self.chest_stats["sold_earnings"]["last_reset"].get("daily"),
                        "monthly": self.chest_stats["sold_earnings"]["last_reset"].get("monthly")
                    }
            
            stats = {
                'total_uptime_seconds': float(self.total_uptime_seconds),
                'total_instances': self.instances_count_var.get() if hasattr(self, 'instances_count_var') else 0,
                'region_instances': {},
                'region_times': {},
                'chest_stats': serializable_chest_stats,
                'total_earnings': {
                    'gold': self.total_gold.get() if hasattr(self, 'total_gold') else 0,
                    'silver': self.total_silver.get() if hasattr(self, 'total_silver') else 0,
                    'copper': self.total_copper.get() if hasattr(self, 'total_copper') else 0,
                    'dark_crystals': self.total_dark_crystals.get() if hasattr(self, 'total_dark_crystals') else 0
                }
            }
            
            # Статистика по регионам
            for key in self.region_keys:
                try:
                    if hasattr(self, 'region_instances_count') and key in self.region_instances_count:
                        stats['region_instances'][key] = int(self.region_instances_count[key].get())
                    else:
                        stats['region_instances'][key] = 0
                    
                    if hasattr(self, 'region_time_spent') and key in self.region_time_spent:
                        stats['region_times'][key] = float(self.region_time_spent[key].get())
                    else:
                        stats['region_times'][key] = 0.0
                except Exception as e:
                    self.log_message(f"[DEBUG save_statistics] Ошибка при сохранении статистики региона {key}: {str(e)}")
            
            # Статистика предметов
            if hasattr(self, 'item_stats_vars'):
                try:
                    stats['item_stats'] = {}
                    for key, var in self.item_stats_vars.items():
                        if isinstance(var, tk.IntVar):
                            stats['item_stats'][key] = int(var.get())
                        else:
                            stats['item_stats'][key] = var
                except Exception as e:
                    self.log_message(f"[DEBUG save_statistics] Ошибка при сохранении статистики предметов: {str(e)}")

            # Статистика по регионам
            if hasattr(self, 'region_stats'):
                try:
                    stats['region_stats'] = {}
                    for region, region_data in self.region_stats.items():
                        stats['region_stats'][region] = {}
                        for key, var in region_data.items():
                            if isinstance(var, tk.IntVar):
                                stats['region_stats'][region][key] = int(var.get())
                            else:
                                stats['region_stats'][region][key] = var
                except Exception as e:
                    self.log_message(f"[DEBUG save_statistics] Ошибка при сохранении статистики регионов: {str(e)}")

            # Сохраняем в файл
            with open(self.stats_file, 'w') as f:
                json.dump(stats, f, indent=4)
            self.log_message("[DEBUG save_statistics] Статистика успешно сохранена")
            
        except Exception as e:
            self.log_message(f"[DEBUG save_statistics] Ошибка при сохранении статистики: {str(e)}")

    def _update_total_item_stats_display(self):
        """Обновляет отображение общей статистики предметов."""
        try:
            # Подсчет общего количества сундуков в банке
            total_banked = 0
            for region_data in self.chest_stats["banked"].values():
                if isinstance(region_data, dict):
                    total_banked += sum(region_data.values())
            self.item_stats_vars["total_banked"].set(total_banked)
            
            # Подсчет общего количества проданных сундуков
            total_sold = 0
            for region_data in self.chest_stats["sold"].values():
                if isinstance(region_data, dict):
                    total_sold += sum(region_data.values())
            self.item_stats_vars["total_sold"].set(total_sold)
            
            # Подсчет общего количества открытых VIP сундуков
            total_opened_vip = sum(self.chest_stats["opened_vip"].values())
            self.item_stats_vars["total_opened_vip"].set(total_opened_vip)
            
            # Подсчет общего количества использованных темных кристаллов
            total_dark_crystals_used = sum(self.chest_stats["dark_crystals_used"].values())
            self.item_stats_vars["total_dark_crystals_used"].set(total_dark_crystals_used)
            
            # Подсчет общего количества полученных темных кристаллов
            total_dark_crystals_earned = sum(self.chest_stats["dark_crystals_earned"].values())
            self.item_stats_vars["total_dark_crystals_earned"].set(total_dark_crystals_earned)
            
            # Обновляем отображение заработка
            self._update_total_earnings_display()
        except Exception as e:
            self.log_message(f"[DEBUG _update_total_item_stats_display] Ошибка при обновлении отображения статистики: {str(e)}")

    def on_closing(self):
        """Handles window closing: saves settings and stops threads."""
        self.log_message("[DEBUG on_closing] Завершение работы...")
        self.running = False # Signal threads to stop

        # Save settings before exiting
        self.save_settings()
        self.save_location_memory()
        self.save_statistics() # Save statistics

        # Wait briefly for threads to notice the flag (optional)
        # time.sleep(0.1) # Daemon threads should exit automatically

        self.destroy() # Close the Tkinter window

    def _check_and_reset_periods(self):
        """Проверяет и сбрасывает дневную и месячную статистику при необходимости"""
        current_time = datetime.datetime.now()
        
        # Проверяем последний сброс дневной статистики
        if self.chest_stats["sold_earnings"]["last_reset"]["daily"] is None:
            self.chest_stats["sold_earnings"]["last_reset"]["daily"] = current_time
        else:
            last_reset = datetime.datetime.fromisoformat(self.chest_stats["sold_earnings"]["last_reset"]["daily"])
            if current_time.date() > last_reset.date():
                # Сброс дневной статистики
                for region in self.region_keys:
                    self.chest_stats["sold_earnings"]["daily"][region] = {"silver": 0, "copper": 0}
                self.chest_stats["sold_earnings"]["last_reset"]["daily"] = current_time.isoformat()

        # Проверяем последний сброс месячной статистики
        if self.chest_stats["sold_earnings"]["last_reset"]["monthly"] is None:
            self.chest_stats["sold_earnings"]["last_reset"]["monthly"] = current_time
        else:
            last_reset = datetime.datetime.fromisoformat(self.chest_stats["sold_earnings"]["last_reset"]["monthly"])
            if current_time.month != last_reset.month or current_time.year != last_reset.year:
                # Сброс месячной статистики
                for region in self.region_keys:
                    self.chest_stats["sold_earnings"]["monthly"][region] = {"silver": 0, "copper": 0}
                self.chest_stats["sold_earnings"]["last_reset"]["monthly"] = current_time.isoformat()

    def _update_earnings_stats(self, region, chest_type):
        """Обновляет статистику заработка при продаже сундука"""
        if chest_type not in CHEST_VALUES:
            return

        # Получаем значения серебра и меди для данного типа сундука
        silver = CHEST_VALUES[chest_type]["silver"]
        copper = CHEST_VALUES[chest_type]["copper"]

        # Проверяем и обновляем периоды
        self._check_and_reset_periods()

        # Обновляем статистику по всем периодам
        for period in ["daily", "monthly", "total"]:
            self.chest_stats["sold_earnings"][period][region]["silver"] += silver
            self.chest_stats["sold_earnings"][period][region]["copper"] += copper

        # Нормализуем медь (100 меди = 1 серебро)
        for period in ["daily", "monthly", "total"]:
            while self.chest_stats["sold_earnings"][period][region]["copper"] >= 100:
                self.chest_stats["sold_earnings"][period][region]["copper"] -= 100
                self.chest_stats["sold_earnings"][period][region]["silver"] += 1

            # Нормализуем серебро (100 серебра = 1 золото)
            gold = self.chest_stats["sold_earnings"][period][region]["silver"] // 100
            self.chest_stats["sold_earnings"][period][region]["silver"] %= 100
            if "gold" not in self.chest_stats["sold_earnings"][period][region]:
                self.chest_stats["sold_earnings"][period][region]["gold"] = 0
            self.chest_stats["sold_earnings"][period][region]["gold"] += gold

        # Обновляем отображение
        self._update_total_earnings_display()

    def _update_total_earnings_display(self):
        """Обновляет отображение общего заработка"""
        # Подсчитываем общие суммы для каждого периода
        for period in ["daily", "monthly", "total"]:
            total_gold = sum(self.chest_stats["sold_earnings"][period][region].get("gold", 0) for region in self.region_keys)
            total_silver = sum(self.chest_stats["sold_earnings"][period][region]["silver"] for region in self.region_keys)
            total_copper = sum(self.chest_stats["sold_earnings"][period][region]["copper"] for region in self.region_keys)
            
            # Нормализуем медь
            additional_silver = total_copper // 100
            total_copper = total_copper % 100
            total_silver += additional_silver

            # Нормализуем серебро
            additional_gold = total_silver // 100
            total_silver = total_silver % 100
            total_gold += additional_gold

            # Обновляем переменные отображения
            self.item_stats_vars[f"earnings_{period}_gold"].set(total_gold)
            self.item_stats_vars[f"earnings_{period}_silver"].set(total_silver)
            self.item_stats_vars[f"earnings_{period}_copper"].set(total_copper)

    def update_item_stats(self, item_type, action, count=1, region=None):
        """Обновляет статистику предметов.
        
        Args:
            item_type (str): Тип предмета ('old', 'middle', 'little', 'big', 'carved', 'precious', 'vip')
            action (str): Действие ('banked', 'sold', 'opened')
            count (int): Количество предметов
            region (str): Регион, в котором произошло действие
        """
        if region is None:
            region = self.current_region_key or "vergeland"
            
        # Преобразование старых типов сундуков в новые
        chest_type_mapping = {
            'old': 'common',
            'middle': 'rare',
            'little': 'epic',
            'big': 'legendary',
            'carved': 'mythic',
            'precious': 'divine',
            'vip': 'vip'
        }
        
        new_item_type = chest_type_mapping.get(item_type, item_type)
        
        if action in ['banked', 'sold']:
            if region in self.chest_stats[action]:
                if new_item_type not in self.chest_stats[action][region]:
                    self.chest_stats[action][region][new_item_type] = 0
                self.chest_stats[action][region][new_item_type] += count
        elif action == 'opened' and item_type == 'vip':
            if region in self.chest_stats['opened_vip']:
                self.chest_stats['opened_vip'][region] += count
        
        self.save_statistics()
        self._update_total_item_stats_display()

    def update_dark_crystals(self, amount, is_earned=True):
        """Обновляет статистику темных кристаллов
        
        Args:
            amount (int): Количество кристаллов
            is_earned (bool): True если получены, False если использованы
        """
        if is_earned:
            self.chest_stats['dark_crystals']['earned'] += amount
        else:
            self.chest_stats['dark_crystals']['used'] += amount
        
        self.save_statistics()
        self._update_total_item_stats_display()

    def update_earnings(self, gold=0, silver=0, copper=0):
        """Обновляет статистику заработка
        
        Args:
            gold (int): Количество золота
            silver (int): Количество серебра
            copper (int): Количество меди
        """
        # Конвертируем все в медь для подсчета
        total_copper = (gold * 10000) + (silver * 100) + copper
        
        # Обновляем дневную статистику
        self.chest_stats['sold']['earnings']['daily']['amount'] += total_copper
        
        # Обновляем месячную статистику
        self.chest_stats['sold']['earnings']['monthly']['amount'] += total_copper
        
        # Обновляем общую статистику
        self.chest_stats['sold']['earnings']['total'] += total_copper
        
        self._check_and_reset_periods()
        self.save_statistics()
        self._update_total_earnings_display()

    def update_region_stats(self, region_key, time_spent):
        """Обновляет статистику региона
        
        Args:
            region_key (str): Ключ региона
            time_spent (float): Затраченное время в секундах
        """
        if region_key in self.region_stats:
            self.region_stats[region_key]['visits'] += 1
            self.region_stats[region_key]['time_spent'] += time_spent
            self.save_statistics()

    def connection_monitor(self):
        """Отслеживает состояние процесса игры"""
        while True:
            try:
                if not self.running:
                    time.sleep(5)
                    continue

                # Проверка наличия процесса Overkings.exe
                overkings_running = False
                for proc in psutil.process_iter(['name']):
                    try:
                        if proc.info['name'] == 'Overkings.exe':
                            overkings_running = True
                            break
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

                if not overkings_running:
                    self.log_message("Процесс Overkings.exe не найден! Перезапускаем клиент...")
                    self.vjuh_treatment()
                    continue

            except Exception as e:
                self.log_message(f"[ERROR] Ошибка в мониторинге процесса: {e}")
                time.sleep(5)

            time.sleep(2)  # Пауза между проверками

    def check_vjuh(self):
        """Проверка ошибок подключения через Tkinter after"""
        if self.running:
            vjuh = find_template("vjuh", self)
            error2032 = find_template("error2032", self)
            
            if vjuh or error2032:
                if vjuh:
                    self.log_message("[DEBUG check_vjuh] Обнаружена ошибка 'Вжух'!")
                if error2032:
                    self.log_message("[DEBUG check_vjuh] Обнаружена ошибка Error2032!")
                    
                vjuh_ok = find_template("vjuh_ok", self)
                if vjuh_ok:
                    human_click(*vjuh_ok)
                    self.log_message("[DEBUG check_vjuh] Нажата кнопка ОК")
                    self.after(3000, lambda: PostFarm.cache_cleaner(self))
        
        # Планируем следующую проверку через 5 минут
        self.after(300000, self.check_vjuh)

    def pve(self):
        """Выполняет PVE бой через систему событий Tkinter"""
        self.gui.after(2000, self.pve_start)
        
    def pve_start(self):
        """Начинает PVE бой"""
        if not self.gui.running:
            return
            
        door_back = find_template("door_back", self.gui)
        if door_back:
            self.gui.log_message("[DEBUG pve_start] Начало боя найдено. НАЧИНАЕМ БОЙ!")
            self.gui.after(1000, self.pve_step)
            return
            
        map_choice = find_template("map_choice", self.gui)
        if map_choice:
            self.gui.log_message("[DEBUG pve_start] Начало локации не найдено! Возможно откат.")
            return
            
        self.gui.log_message("[DEBUG pve_start] Начало локации не найдено! Пробуем еще раз.")
        self.gui.after(1000, self.pve_start)
        
    def pve_step(self):
        """Выполняет один шаг PVE"""
        if not self.gui.running:
            return
            
        you_dead1 = find_template("you_dead1", self.gui)
        achievement = find_template("achievement", self.gui)
        
        if you_dead1:
            self.gui.after(5000, self.handle_death)
            return
            
        if achievement:
            human_click(*achievement)
            self.gui.after(1000, self.pve_step)
            return
            
        door_next = find_template("door_next", self.gui) or find_template("door_next2", self.gui)
        if door_next:
            # Проверяем босса перед дверью
            boss = find_template("boss", self.gui)
            if boss:
                self.gui.log_message("[DEBUG pve_step] Найден босс перед дверью")
            else:
                self.gui.log_message("[DEBUG pve_step] Босс перед дверью не найден")
                
            # Проверяем наличие босса и включенную защиту от засад
            if boss and self.gui.save_drops.get():
                self.gui.log_message("[DEBUG pve_step] Обнаружен босс! Это последний уровень локации.")
                
                # Ставим фарм на паузу
                self.gui.log_message("[DEBUG pve_step] Фарм поставлен на паузу для защиты от засад")
                
                # Определяем номер телепорта для текущего региона
                region_teleports = {
                    "vergeland": 4,      # телепорты 1-4
                    "harangerfjord": 8,  # телепорты 5-8
                    "heimskringla": 11,  # телепорты 9-11
                    "sorian": 15,        # телепорты 12-15
                    "ortre": 18,         # телепорты 16-18
                    "almeric": 22,       # телепорты 19-22
                    "metanoia": 26,      # телепорты 23-26
                    "panfobion": 28      # телепорты 27-28
                }
                
                # Получаем номер телепорта для текущего региона
                teleport_number = region_teleports.get(self.region_name.lower())
                if teleport_number:
                    self.gui.log_message(f"[DEBUG pve_step] Телепортируемся в телепорт {teleport_number} для PostFarm")
                    self.gui.after(2000, lambda: teleport(teleport_number, self.gui))
                    self.gui.after(4000, lambda: self.handle_post_location())
                return
                
            # Если босса нет или защита отключена - идем через дверь как обычно
            human_click(*door_next)
            self.gui.after(2000, self.pve_step)
            return
            
        # Ищем точку для движения и бежим к концу локации
        pool_coords = find_template("pool_2", self.gui)
        if pool_coords:
            # Проверяем, нужно ли вступать в бой
            fight_no = find_template("fight_no", self.gui, threshold=0.75)
            if not fight_no:
                self.gui.log_message("[DEBUG pve_step] Бежим в конец локации.")
                with hold_key("alt"):
                    human_click(pool_coords[0] - 150, pool_coords[1] - 50)
                    time.sleep(1.1)
                    human_click(pool_coords[0] - 500, pool_coords[1] - 200)
                    time.sleep(1.1)
                human_click(*pool_coords)
                self.gui.log_message("[DEBUG pve_step] Призываем сигил.")
                human_click(pool_coords[0] - 170, pool_coords[1])
                
                # Цикл атаки
                while not find_template("fight_no", self.gui):
                    fight_no = find_template("fight_no", self.gui)
                    you_dead1 = find_template("you_dead1", self.gui)
                    achievement = find_template("achievement", self.gui)
                    #boss = find_template("boss", self.gui)
                    
                    # Логируем проверку босса
                    if boss:
                        self.gui.log_message("[DEBUG pve_step] Найден босс во время боя")
                    
                    # Если бой закончен
                    if fight_no or you_dead1 or achievement:
                        # Проверяем босса еще раз после окончания боя
                        boss = find_template("boss", self.gui)
                        if boss:
                            self.gui.log_message("[DEBUG pve_step] Найден босс после окончания боя")
                            
                            # Если был найден босс и включена защита от засад
                            if self.gui.save_drops.get():
                                self.gui.log_message("[DEBUG pve_step] Обнаружен босс! Это последний уровень локации.")
                                self.gui.log_message("[DEBUG pve_step] Фарм поставлен на паузу для защиты от засад")
                                
                                # Определяем номер телепорта для текущего региона
                                region_teleports = {
                                    "vergeland": 4,      # телепорты 1-4
                                    "harangerfjord": 8,  # телепорты 5-8
                                    "heimskringla": 11,  # телепорты 9-11
                                    "sorian": 15,        # телепорты 12-15
                                    "ortre": 18,         # телепорты 16-18
                                    "almeric": 22,       # телепорты 19-22
                                    "metanoia": 26,      # телепорты 23-26
                                    "panfobion": 28      # телепорты 27-28
                                }
                                
                                # Получаем номер телепорта для текущего региона
                                teleport_number = region_teleports.get(self.region_name.lower())
                                if teleport_number:
                                    self.gui.log_message(f"[DEBUG pve_step] Телепортируемся в телепорт {teleport_number} для PostFarm")
                                    self.gui.after(2000, lambda: teleport(teleport_number, self.gui))
                                    self.gui.after(4000, lambda: self.handle_post_location())
                        else:
                            self.gui.log_message("[DEBUG pve_step] Босс после боя не найден")
                        break
                        
                    human_click(pool_coords[0], pool_coords[1] - 505, double=True)
                    self.gui.log_message("[DEBUG pve_step] Атакуем противника.")
                    human_click(pool_coords[0] - 530, pool_coords[1])
                    self.gui.log_message("[DEBUG pve_step] Используем скиллы.")
                    human_click(pool_coords[0] - 470, pool_coords[1])
                    self.gui.log_message("[DEBUG pve_step] Используем скиллы.")
                    time.sleep(0.5)
                    
        # Продолжаем цикл
        self.gui.after(4000, self.pve_step)

    def pve_combat(self):
        """Выполняет боевые действия"""
        if not self.gui.running:
            return
            
        you_dead1 = find_template("you_dead1", self.gui)
        achievement = find_template("achievement", self.gui)
        
        if you_dead1:
            self.gui.after(5000, self.handle_death)
            return
            
        if achievement:
            human_click(*achievement)
            self.gui.after(1000, self.pve_combat)
            return
            
def pve(gui):
    """
    Основная функция для PvE фарма
    
    Args:
        gui (GUI): Объект графического интерфейса
    """
    time.sleep(2)
    while gui.running:
        if not gui.running:
            break
        location_completed = False  # Сбрасываем флаг перед новой итерацией
        found_boss = False  # Флаг для отслеживания обнаружения босса

        attempt = 0  # Счетчик попыток
        while attempt < 5:
            door_back = find_template("door_back", gui)
            if door_back:
                # Проверяем на засаду
                pool_coords = find_template("pool_2", gui)
                if pool_coords:
                    with hold_key("alt"):
                        human_click(pool_coords[0] - 160, pool_coords[1] - 50)
                        time.sleep(0.5)
                        fight_no = find_template("fight_no", gui)
                        if not fight_no:
                            gui.log_message("[DEBUG pve] Обнаружена возможная засада! Отступаем.")
                            human_click(door_back[0], door_back[1])
                            return

                gui.log_message("[DEBUG pve] Начало локации найдено. НАЧИНАЕМ БОЙ!")
                break  # Выходим из цикла попыток, так как door_back найден
            else:
                time.sleep(1)
                map_choice = find_template("map_choice", gui)
                if map_choice:
                    gui.log_message("[DEBUG pve] Начало локации не найдено! Возможно откат.")
                    return
                else:
                    gui.log_message(f"[DEBUG pve] Начало локации не найдено! Попытка {attempt + 1} из 5.")
                    attempt += 1
                    time.sleep(1)
        if attempt >= 5:
            door_next = find_template("door_next", gui)
            if door_next:
                gui.log_message("[DEBUG pve] Напали? подождем))")
                time.sleep(1)
            else:
                map_choice = find_template("map_choice", gui)
                if map_choice:
                    gui.log_message("[DEBUG pve] Начало локации не найдено! Возможно откат.")
                    return

        while gui.running and not location_completed:
            if not gui.running:
                break
            you_dead1 = find_template("you_dead1", gui)
            achievement = find_template("achievement", gui)
            if not you_dead1:
                if not achievement:
                    door_next = find_template("door_next", gui) or find_template("door_next2", gui)                             
                    if not door_next:
                        pool_coords = find_template("pool_2", gui)
                        if pool_coords:
                            gui.log_message("[DEBUG pve] Бежим в конец локации.")
                            with hold_key("alt"):
                                human_click(pool_coords[0] - 160, pool_coords[1] - 50)
                                time.sleep(1.1)
                                human_click(pool_coords[0] - 160, pool_coords[1] - 250)
                    else:
                        # Проверяем наличие босса только когда дошли до конца (door_next)
                        boss = find_template("boss", gui)
                        if boss and gui.save_drops.get():
                            gui.log_message("[DEBUG pve] Обнаружен босс в конце локации!")
                            found_boss = True
                            
                            # Определяем номер телепорта для текущего региона
                            region_teleports = {
                                "vergeland": 4,      # телепорты 1-4
                                "harangerfjord": 8,  # телепорты 5-8
                                "heimskringla": 11,  # телепорты 9-11
                                "sorian": 15,        # телепорты 12-15
                                "ortre": 18,         # телепорты 16-18
                                "almeric": 22,       # телепорты 19-22
                                "metanoia": 26,      # телепорты 23-26
                                "panfobion": 28      # телепорты 27-28
                            }
                            
                            # Получаем номер телепорта для текущего региона
                            region = gui.current_region_key.lower() if gui.current_region_key else "vergeland"
                            teleport_number = region_teleports.get(region)
                            
                            if teleport_number:
                                gui.log_message(f"[DEBUG pve] Телепортируемся в телепорт {teleport_number} для PostFarm")
                                # Открываем камень телепортации
                                pool_2 = find_template("pool_2", gui)
                                if pool_2:
                                    tprune = find_template("tprune", gui)
                                    if not tprune:
                                        human_click(*pool_2)
                                        time.sleep(1)
                                
                                # Выполняем телепортацию
                                teleport(teleport_number, gui)
                                time.sleep(2)
                                
                                # Проверяем успешность телепортации
                                pool_2 = find_template("pool_2", gui)
                                if pool_2:
                                    gui.log_message("[DEBUG pve] Телепортация успешна, начинаем PostFarm")
                                    gui.farming_paused = True
                                    runner = RegionRunner(gui, region, [])
                                    runner.handle_post_location()
                                else:
                                    gui.log_message("[DEBUG pve] Телепортация не удалась, пробуем еще раз")
                                    teleport(teleport_number, gui)
                                    time.sleep(2)
                                    gui.farming_paused = True
                                    runner = RegionRunner(gui, region, [])
                                    runner.handle_post_location()
                            return

                        fight_no = find_template("fight_no", gui)
                        if not fight_no:
                            gui.log_message("[DEBUG pve] Конец локации найден, вступаем в бой.")
                            with hold_key("alt"):
                                human_click(pool_coords[0] - 150, pool_coords[1] - 50)
                                time.sleep(1.1)
                                human_click(pool_coords[0] - 500, pool_coords[1] - 200)
                                time.sleep(1.1)
                            human_click(*pool_coords)
                            # Призываем сигил только если не обнаружен босс
                            if not found_boss:
                                gui.log_message("[DEBUG pve] Призываем сигил для обычного боя.")
                                human_click(pool_coords[0] - 170, pool_coords[1])
                            while gui.running:
                                if not gui.running:
                                    break
                                fight_no = find_template("fight_no", gui)
                                you_dead1 = find_template("you_dead1", gui)
                                achievement = find_template("achievement", gui)
                                if you_dead1:
                                    break
                                if achievement:
                                    break
                                human_click(pool_coords[0], pool_coords[1] - 505, double=True)
                                gui.log_message("[DEBUG pve] Атакуем противника.")
                                human_click(pool_coords[0] - 530, pool_coords[1])
                                gui.log_message("[DEBUG pve] Используем скиллы.")
                                human_click(pool_coords[0] - 470, pool_coords[1])
                                gui.log_message("[DEBUG pve] Используем скиллы.")
                                time.sleep(0.5)
                            else:
                                continue
                        door_next = find_template("door_next", gui) or find_template("door_next2", gui)                             
                        if door_next:
                            achievement = find_template("achievement", gui)
                            if not achievement:
                                gui.log_message("[DEBUG pve] Конец локации найден, выходим.")
                                if gui.save_drops.get():
                                    gui.log_message("[DEBUG pve] Активируем защиту от засад")
                                    location_completed = True
                                    gui.farming_paused = True
                                    runner = RegionRunner(gui, gui.current_region_key, [])
                                    runner.handle_post_location()
                                    return
                                else:
                                    human_click(*door_next)
                                    location_completed = True
                            else:
                                human_click(*achievement)
                        else:
                            continue
                else:
                    human_click(*achievement)
            else:
                while gui.running:
                    if not gui.running:
                        break
                    you_dead2 = find_template("you_dead2", gui)
                    if you_dead2:
                        human_click(*you_dead2)
                        break
                    gui.log_message("[DEBUG pve] Ждем возможность возродиться.")
                    time.sleep(5)
                    map_choice = find_template("map_choice", gui)
                    if map_choice:
                        break

        time.sleep(2)  # Ждем перед повторным запуском

if __name__ == "__main__":
    # Check if patterns directory exists
    if not os.path.isdir("patterns"):
        messagebox.showerror("[DEBUG main] Ошибка", "Папка 'patterns' не найдена рядом с исполняемым файлом!")
        sys.exit(1)

    print("[DEBUG main] Перед созданием экземпляра GUI...")  # DEBUG
    try:
        app = GUI()  # Create instance of the CTk app
        print("[DEBUG main] Экземпляр GUI успешно создан.")  # DEBUG

        # Setup hotkeys after app is created
        print("[DEBUG main] Перед установкой горячих клавиш...")  # DEBUG
        try:
            keyboard.add_hotkey("Insert", app.toggle_running)
            keyboard.add_hotkey("Escape", lambda: app.toggle_running() if app.running else None)
            print("[DEBUG main] Горячие клавиши 'Insert' для СТАРТ/СТОП и 'Escape' для СТОП установлены.")
        except Exception as e:
            app.log_message(f"[ERROR main] Не удалось установить горячие клавиши: {e}")

        print("[DEBUG main] Перед запуском app.mainloop()...")  # DEBUG
        app.mainloop()  # Start the app loop
        print("[DEBUG main] app.mainloop() завершен.")  # DEBUG

    except Exception as e:
        # Fallback error display using tkinter messagebox
        error_message = f"Произошла критическая ошибка при запуске:\n{str(e)}\n\nПожалуйста, проверьте лог-файл logs/log_YYYY-MM-DD.txt для деталей."
        print(f"[DEBUG main] КРИТИЧЕСКАЯ ОШИБКА: {e}")  # Print to console as well
        try:
            messagebox.showerror("[DEBUG main] Критическая Ошибка", error_message)
        except Exception as final_e:
            print(f"[DEBUG main] Не удалось показать сообщение об ошибке: {final_e}")
        sys.exit(1)  # Exit after critical error

