import os

styles_path = "ENTER FULL PATH TO STYLES FOLDER"
# styles_path = "/home/adrian/code/pr-qt/styles/"

styles = {}

with os.scandir(styles_path) as it:
    for entry in it:
        with open(entry.path, "r") as f:
            styles.update({entry.name: f.read()})

def set_styles(interface):
    interface.centralwidget.setStyleSheet(styles["main.css"])