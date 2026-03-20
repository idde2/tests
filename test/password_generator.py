import random
import argparse
import pyperclip

def convert(raw):
    procced = {
        1 : "a",
        2 : "b",
        3 : "c",
        4 : "d",
        5 : "e",
        6 : "f",
        7 : "g",
        8 : "h",
        9 : "i",
        10 : "j",
        11 : "k",
        12 : "l",
        13 : "m",
        14 : "n",
        15 : "o",
        16 : "p",
        17 : "q",
        18 : "r",
        19 : "s",
        20 : "t",
        21 : "u",
        22 : "v",
        23 : "w",
        24 : "x",
        25 : "y",
        26 : "z",
        27 : "0",
        28 : "1",
        29 : "2",
        30 : "3",
        31 : "4",
        32 : "5",
        33 : "6",
        34 : "7",
        35 : "8",
        36 : "9",
        37 : "A",
        38 : "B",
        39 : "C",
        40 : "D",
        41 : "E",
        42 : "F",
        43 : "G",
        44 : "H",
        45 : "I",
        46 : "J",
        47 : "K",
        48 : "L",
        49 : "M",
        50 : "N",
        51 : "O",
        52 : "P",
        53 : "Q",
        54 : "R",
        55 : "S",
        56 : "T",
        57 : "U",
        58 : "V",
        59 : "W",
        60 : "X",
        61 : "Y",
        62 : "Z",
        63 : "!",
        64 : "#",
        65 : "§",
        66 : "*",
        67 : "+",
        68 : "=",
        69 : "-",
        70 : " "
    }
    return procced[raw]

parser = argparse.ArgumentParser()
parser.add_argument("--len", type=int)
args = parser.parse_args()

if not args.len:
    length = int(input("enter length: "))
else:
    length = args.len
key = ""

for i in range(length):
    key += (convert(random.randint(1, 70)))


print(key)
copy = input("copy to clipboard? (y/n): ")
if copy == "y":
    pyperclip.copy(key)
    print("Copied to clipboard")