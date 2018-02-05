# -*- coding:utf-8 -*-
import StringIO
import functools
import hashlib
import json
import random
import types

import math
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

json_dumps = functools.partial(json.dumps, ensure_ascii=False)


def split(t_str, t_sep=','):
    return t_str.split(t_sep) if t_str else []


def get_from_dict(t_dict, key, default_value=None):
    return t_dict[key] if key in t_dict else default_value


def get_key(t_dict, value, default_value=None):
    new_dict = {v: k for k, v in t_dict.items()}
    return new_dict[value] if value in new_dict else default_value


def list2map(items, prop_key, value_type=None, handler=None):
    t_dict = dict()
    for item in items:
        key = getattr(item, prop_key) if hasattr(item, prop_key) else item[prop_key]
        if value_type is None:
            t_dict[key] = handler(item) if handler else item
        elif isinstance(value_type, types.ListType):
            if key not in t_dict:
                t_dict[key] = []
            t_dict[key].append(handler(item) if handler else item)
    return t_dict


def get_vcode():
    return ''.join(random.Random().sample(map(str, range(10)), 6))


dataurl_font = ImageFont.truetype('msyh.ttf', 40)


def getdataurl(name):
    name = name[1:3] if len(name) > 2 else name
    t_md5 = hashlib.md5(name.encode('utf-8', 'ignore')).hexdigest()
    weight = 120
    hight = 120
    image = Image.new('RGB', (weight, hight), '#' + t_md5[:6])
    draw = ImageDraw.Draw(image)
    draw.text((20, 30), name, font=dataurl_font, fill=(255, 255, 255))

    output = StringIO.StringIO()
    image.save(output, format="png")
    contents = output.getvalue()
    output.close()
    # return 'data:image/png;base64,' + base64.b64encode(contents)
    return contents


def str2list(str, t_sep=','):
    t_list = str.split(t_sep) if str else []
    return t_list


def list2str(t_list, t_sep=','):
    t_list = [str(i) for i in t_list]
    return t_sep.join(t_list)


def vdt_diameter(timedelta, initial_diameter, final_diameter):
    # calculating doubling time
    # for diameter:Dt = Ti*log2/3*log(Di/Do)
    # for volume:Dt = (ln2*Ti)/(ln(Vi/Vo))
    # Ti = interval time;Di = initial diameter;Do = final diameter;Vi = initial volume;Vo = final volume
    # initial_volume = initial_diameter * initial_diameter * initial_diameter / 2
    # final_volume = final_diameter * final_diameter * final_diameter / 2
    # vdt = (math.log(2) * timedelta) / (math.log(final_volume / initial_volume))
    if initial_diameter == final_diameter:
        return 0
    vdt = timedelta * math.log(2) / 3 / math.log(final_diameter / initial_diameter)
    return int(round(vdt))
