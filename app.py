import os
import json
import requests
import sys

def get_banner(snap_json):
    return [s["url"] for s in snap_json["snap"]["media"] if s["type"] == "banner"]

def get_icon(snap_json):
    return [s["url"] for s in snap_json["snap"]["media"] if s["type"] == "icon"]

def get_snap(snap_name):
    url = "https://api.snapcraft.io/v2/snaps/info/{snap_name}?fields=title,media".format(snap_name=snap_name)

    headers={"Snap-Device-Series": "16"}
    
    response = requests.get(url, headers=headers)

    response_json = response.json()

    icon = get_icon(response_json)
    banner = get_banner(response_json)

    return {
        "name": response_json["name"],
        "icon": icon[0] if icon else "",
        "banner": banner[0] if banner else ""
    }


current_dir = os.path.dirname(os.path.realpath(__file__))

with open("/".join([current_dir, "snaps.txt"])) as f:
    lines = f.read().strip().splitlines()

snaps = []

print(str(len(lines)) + " snaps to find")

with open("/".join([current_dir, "_snap.html"])) as f:
    template = f.read()

for snap in lines:
    single_snap = get_snap(snap)
    snaps.append(template.format(snap_name=single_snap["name"], snap_icon=single_snap["icon"], snap_banner=single_snap["banner"]))

with open("/".join([current_dir, "_template.html"])) as f:
    template = f.read()

html = template.format(snaps="".join(snaps))

with open("/".join([current_dir, "index.html"]), "w") as f:
    f.write(html)

print("Done")
print("/".join(["Open file://", current_dir, "index.html"]))
