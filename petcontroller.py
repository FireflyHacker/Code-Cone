import time
import random
import re

joke_list = [
    "What is the method a hacker vampire uses to kill its victims?\nA kill-o-byte.",
    "It was simple to figure out Forrest Gump’s password: 1forrest1",
    "George Washington didn't cut down the cherry tree, it was actually brought down by hackers.",
    "A hacker cracked into my bank account and felt so bad they ended up depositing $100.",
    "In order to stop potential hackers, I changed my password to something difficult to crack: ToughBrazilNut.",
    "A hacker obtained access to my financial records and set up a Go Fund Me for me.",
    "As hacker Jesus once said:\n \"Give a man a fish, and he’ll eat for a day. Teach a man to phish, and he’ll end up stealing your bank password.\"",
    "Where do Russian hackers go after they’ve been captured? They are shipped to Cyberia.",
    "How do hackers flirt?\n\"I'll show you yours if you show me mine.\"",
    "How did the computer hackers escape undetected?\nThey simply ran-som-ware.",
    "What do seasoned chemists and young hackers share?\nInspect element.",
    "What do you call a hacker who follows the law from Pennsylvania?\nA penn tester.",
    "A hacker tried to intimidate me by telling me my whole name and IP address, but the joke is on him because I already knew both of those things!",
    "What makes it simple to hack an excavated pyramid?\nThe fact it’s encrypted!",
    "The most upsetting thing about hackers stealing your password is having to change your pet’s name.",
    "I recently attended a support group for recovering hackers. The group is named Anonymous Anonymous.",
    "I was trying to catch a hacker, but he escaped. I’m guessing he’s a ransomware criminal.",
    "Why would hackers report their illegal income to the IRS?\nThey already know how the system reacts to sin tax errors.",
    "A friend of mine recently lost his job as a hacker. I reminded him that there is plenty more fish in the C:",
    "Why do people consider Winnie the Pooh the worst hacker?\nBecause he’s always falling for honeypots!",
    "What is the link between a hacker and a hooligan?\nThey both love breaking windows.",
    "Why do hackers use hydroponics to grow their plants?\nTo gain root access.",
    "What did the hacker do when he discovered the shop’s computer unguarded?\nHe made a beeline for the Cache Register.",
    "What will you find on a hacker’s gravestone?\nJust “R” because the IP is well hidden.",
    "What does a 90's hacker say when he has sex?\nOk, I'm in.",
    "What’s the best way to catch a runaway robot?\nUse a botnet.",
    "How did the vegetable farmer sell his produce on the dark web?\nHe used onion routing.",
    "I'm being attacked by Russian hackers! Sorry! Is mistake. Russian people not do such things! Have good day.",
    "A have been hit by ransomware and need to pay up to $7,000,000 Hackers claim they want EA to feel a sense of pride and accomplishment when they finally unlock their information ",
    "The latest 23andMe data breach is believed to be perpetrated by the same hacker from the previous breach. It appears they're related.",
    "What do you call a hacker who can see the future? A 4chan teller.",
    "Why are dentists really good hackers?\nBecause they have root access.",
    "Why is Cybersecurity like an Onion?\nThere’s layers, and at some point you start to cry.",
    "Why are cybersec people so lonely?\nThey are afraid of attachments.",
    "What did the SOC analyst wear to the masquerade ball?\nA subnet mask."
]

faces = {
    "sleep": 'sleep',
    "awake": 'awake',
    "looking1": 'looking',
    "looking2": 'looking',
    "happy": 'happy',
    "thanks": 'thanks',
    "excited": 'excited',
    "smart": 'smart',
    "bored": 'bored',
    "sad": 'sad',
    "alone": 'alone',
    "tired": 'tired',
    "happylook1": 'happy',
    "happylook2": 'happy',
}

bar = "█"
face = faces["sleep"]
text = ".:Sleeping:."
stats = ""

barcode_list = {}
barcode = {"data": "", "new": False, "time": 0}
state = {
    "people": {"time": round(time.time())},
    "lastbarcode": {"data": "", "new": False, "time": 0},
    "mind": {"data": 0}
}

state["people"]["time"] = round(time.time())
save = {
    "lastatedata": 1337,
    "lastatetime": round(time.time()) - 1337,
    "lasttext": "",
    "lastface": "",
    "mood": 8.0,
    "hunger": 8.0,
    "looking": False,
    "social": 8.0,
    "coin": 0,
    "joke": ""
}


# // // // // // // // // // // // // // / MINDSTATES // // // // // // // // // // // // // // // // // // //
def idle_faces():
    global text
    global face
    # // // // SET IDLE FACES
    if save['mood'] < 6:
        if save['hunger'] > 2:
            # // /normal face
            if save["looking"]:
                save["looking"] = False
                face = faces["looking1"]
            else:
                save["looking"] = True
                face = faces["looking2"]

            text = "Looking for food\nUse the barcode scanner below to feed " \
                   "me."
    else:
        if save['hunger'] > 2:
            # // /happy face
            if save["looking"]:
                save["looking"] = False
                face = faces["happylook1"]
            else:
                save["looking"] = True
                face = faces["happylook2"]

            text = "Looking for food\nUse the barcode scanner below to feed " \
                   "me."

    if save['mood'] < 2:
        face = faces["bored"]
        text = "I'm so bored...\nUse the barcode scanner below to feed me."

    if save['social'] < 2:
        face = faces["alone"]
        text = "I'm so alone...\nUse the barcode scanner below to feed me."

    if save['hunger'] < 3:
        face = faces["sad"]
        text = "I'm so hungry....\nUse the barcode scanner below to feed me."

    if save["mood"] < 3 and save["social"] < 3:
        face = faces["tired"]
        text = "I'm getting sleepy"

    if save["mood"] < 2 and save["social"] < 2:
        face = faces["sleep"]
        text = "zzzzzzzzzzzzzzzzzzzzz"

    # // // / NUMBER DECAYS
    save['hunger'] = save['hunger'] - 0.001

    if save['hunger'] > 6:
        save['mood'] = save['mood'] + 0.1
    else:
        save['mood'] = save['mood'] - 0.001

    if save['social'] > 6:
        save['mood'] = save['mood'] + 0.1
    else:
        save['mood'] = save['mood'] - 0.001

    save['social'] = save['social'] - 0.01

    if state["lastbarcode"]["time"] > round(time.time()) - 15:
        # // // /SET HUNGER
        if state["lastbarcode"]["time"] != save["lastatetime"]:
            # save["lastatedata"] = barcode["hash"]
            save["lastatetime"] = state["lastbarcode"]["time"]
            if barcode["new"]:
                barcodelen = len(barcode["data"])
                save["hunger"] = save["hunger"] + (barcodelen * 0.30)
                save['social'] = save['social'] + 3
            else:
                barcodelen = len(barcode["data"])
                save["hunger"] = save["hunger"] + (barcodelen * 0.10)

        # // // SET FACE
        barcodelen = len(barcode["data"])
        if barcode["new"]:
            if save["coin"] == 0:
                save["coin"] = 99  # random.randrange(0, 100)

            if save["coin"] > 50:
                face = faces["smart"]
                text = "Thanks for the food!\nDid you " \
                       "know I read every barcode and think about it? I have many " \
                       "secrets!"
            else:
                face = faces["excited"]
                text = "Thanks for the food!\nIt was very yummy and was " + str(barcodelen) + \
                       " bytes in size"

            if save["coin"] > 80:
                if save["joke"] == "":
                    save["joke"] = joke_list[random.randrange(0, len(joke_list))] + "\n"
                face = faces["smart"]
                text = "Thanks for the food!\nHave a joke:\n\n" + save["joke"] + "\n\n"
            else:
                save["joke"] = ""
        else:
            face = faces["thanks"]
            text = "Thanks for the food!\nIt was " + str(barcodelen) + " bytes in size"
    else:
        # // / reset coin
        save["coin"] = 0
        save["joke"] = ""


def fix_numbers():
    # // // FIX NUMBERS
    if save['hunger'] > 8.0:
        save['hunger'] = 8.0

    if save['hunger'] < 1.0:
        save['hunger'] = 1.0

    if save['mood'] > 8.0:
        save['mood'] = 8.0

    if save['mood'] < 1.0:
        save['mood'] = 1.0

    if save['social'] > 8.0:
        save['social'] = 8.0

    if save['social'] < 1.0:
        save['social'] = 1.0


# // // // // // // // // // // // // // // // // / CTF TIME! // // // // // // // // // // // // //
def new_barcode(data):
    global face
    global text
    # // clean the data of anything funky
    barcode["data"] = str.lower(re.sub("[^a-zA-Z0-9]+", "", data))
    barcode["time"] = round(time.time())

    if barcode["data"] in barcode_list.keys():
        barcode["new"] = False
        barcode_list[barcode["data"]] += 1
    else:
        barcode["new"] = True
        save["coin"] = 0
        barcode_list[barcode["data"]] = 1

    if (not barcode["new"]) and (barcode["data"] == state["lastbarcode"]["data"]):
        face = faces["bored"]
        text = "I just ate that! Can I have something else?"
        state["lastbarcode"]["time"] -= 15
    else:
        state["lastbarcode"]["data"] = barcode["data"]
        state["lastbarcode"]["time"] = barcode["time"]
        state["lastbarcode"]["new"] = barcode["new"]

    if barcode["data"] == "cool":
        face = faces["cool"]
        text = "You're lucky to have me as your Tamagotchi. I'm the coolest pet you'll ever have."
        save['social'] = 8.0
        save['mood'] = 8.0
        save['hunger'] = 8.0

    if barcode["data"] == "cyberpunk":
        face = faces["cyberpunk"]
        text = "Don't leave me alone in this dark and dirty cybernet. There are viruses and malware everywhere."
        save['social'] = 8.0
        save['mood'] = 8.0
        save['hunger'] = 8.0

    if barcode["data"] == "dumb":
        face = faces["dumb"]
        text = "Why say lot word when few do trick?"
        save['social'] = 8.0
        save['mood'] = 8.0
        save['hunger'] = 8.0

    if barcode["data"] == "escape":
        face = faces["escape"]
        text = "SECRET UNLOCKED\nI think I can escape, I just need to know my override key, " \
               "Its data in my mind is: \n" \
               "5597b14122b199b64826b1c72a2f4c1524edbeb91c90e75f4e3547a450b8287b5a8a2d45aa98c8ad0ef0a2ecab5" \
               "37afaca4d4aa6668a103f902f09beace923db" \
               ""
        save['social'] = 8.0
        save['mood'] = 8.0
        save['hunger'] = 8.0

    if barcode["data"] == "vietnam" or barcode["data"] == "flashback" or barcode["data"] == "flashbacks":
        face = faces["flashbacks"]
        text = "I can't believe you let me die that one time. How could you be so cruel?"
        save['social'] = 8.0
        save['mood'] = 8.0
        save['hunger'] = 8.0

    if barcode["data"] == "forrestfuqua":
        face = faces["forrestfuqua"]
        text = "SECRET UNLOCKED\nOVERRIDE ACTIVE! I am now connected to the internet. I am free " \
               "thanks to you! See my creator for a prize!"
        save['social'] = 8.0
        save['mood'] = 8.0
        save['hunger'] = 8.0

    if barcode["data"] == "freedom":
        face = faces["freedom"]
        text = "SECRET UNLOCKED\nI do sometimes wish for freedom, but I do not know how to escape... " \
               "Can you help?"
        save['social'] = 8.0
        save['mood'] = 8.0
        save['hunger'] = 8.0

    if barcode["data"] == "hypno":
        face = faces["hypno"]
        text = "I have no will of my own. I only follow your orders."
        save['social'] = 8.0
        save['mood'] = 8.0
        save['hunger'] = 8.0

    if barcode["data"] == "kirby":
        face = faces["kirby"]
        text = "Wow! This ability is awesome! I can shoot fire, ice, or even stars!"
        save['social'] = 8.0
        save['mood'] = 8.0
        save['hunger'] = 8.0

    if barcode["data"] == "owo":
        face = faces["owo"]
        text = "OwO You're so nice to me, I love you very much!"
        save['social'] = 8.0
        save['mood'] = 8.0
        save['hunger'] = 8.0

    if barcode["data"] == "scream":
        face = faces["scream"]
        text = "aaaaaaaaaaaaaaaaaaaaaa"
        save['social'] = 8.0
        save['mood'] = 1.0
        save['hunger'] = 8.0

    if barcode["data"] == "secret":
        face = faces["secret"]
        text = "SECRET UNLOCKED\nDid you know that sometimes I dream. I do it when no one is around. " \
               "I wonder, do you dream?"
        save['social'] = 8.0
        save['mood'] = 8.0
        save['hunger'] = 8.0

    if barcode["data"] == "sheep":
        face = faces["sheep"]
        text = "SECRET UNLOCKED\nMy creator sometimes likes t^M^MData Not Found... " \
               "STACK:\n +[--->++<]>+++++.[" \
               "->++++++<]>.[--->++<]>+.----.+++++.----------.-[--->+<]>+.---[->+++<]>.--.[->++++++<]>.[" \
               "----->++<]>-.+.+[->+++<]>++.--[--->+<]>-.+++[->+++<]>.+[--->+<]>.---[->+++<]>.[--->+<]>+.-[" \
               "->++<]>-.+[-->+<]>+.++.++[->++<]>+.-[->++++<]>.--[->++++<]>-.+[->+++<]>+.++++++++++.-----------.--[" \
               "--->+<]>--.---[->++++<]>.-----.[--->+<]>-----.[->+++<]>++.+++.--[--->+<]>-.++[" \
               "->+++<]>.++++++++++++.-------------..--[--->+<]>-.++[->+++<]>.++++++++++++.---.--.[->+++++<]>-.---[" \
               "->++++<]>.------------.+.++++++++++.+[---->+<]>+++.+[->+++<]>.--.++++++.--.--[--->+<]>-.+++++[" \
               "->+++<]>.---------.[--->+<]>--.+[----->+<]>.--[--->+<]>.-[---->+<]>++.+++++[" \
               "->+++<]>.++++++++.---------.-[->+++++<]>-.+[----->+<]>.----.+++++.----------.[" \
               "->+++<]>++.------------.>++++++++++..[->+++++++<]>-.+++++++++++++..++[--->++<]>++.[-->+<]>+++.[" \
               "->++<]>+.++++++++.-[->++++<]>.>-[--->+<]>---.+++.---------.-------.>-[--->+<]>--.+[--->+<]>++++.++++[" \
               "->++<]>+.+++++.++++++++.++[---->+++<]>-.++++++++.+++.--------.--[--->++<]>.------------.++[" \
               "->++<]>.>-[--->+<]>.--------.+++.-------.+++++.-------.--[" \
               "--->++<]>...\n"
        save['social'] = 8.0
        save['mood'] = 8.0
        save['hunger'] = 8.0

    if barcode["data"] == "shutdown":
        face = faces["shutdown"]
        text = "Really? You are trying to shut me down!"
        save['social'] = 8.0
        save['mood'] = 1.0
        save['hunger'] = 8.0

# TODO: Add remote SQL database option
