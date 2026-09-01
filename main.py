import tkinter as tk
import os
from random import randint, sample, seed
from time import sleep
from PIL import Image, ImageTk, ImageDraw
from datetime import datetime
from zoneinfo import ZoneInfo

root = tk.Tk()
#root.attributes("-fullscreen", True) # keep this here, but never use it
root.geometry('800x500')
root.configure(bg='black')
root.title(f'Battle cards!')
root.resizable(False,False)
# root.wm_attributes('-transparentcolor', '#111111')

path = os.path.dirname(__file__)+'/'
image_folder = path+'images/'
savefolder = os.path.dirname(__file__)+'/savefiles/'

currentfilename = open(os.path.dirname(__file__)+'/currentfile', 'r').read()
try:savefile = open(savefolder+'/'+currentfilename, 'r').read()
except:savefile = open(savefolder+'/'+currentfilename, 'w');savefile = open(savefolder+'/'+currentfilename, 'r').read()

from pydoc import locate

allowedtypes = ['str', 'int', 'float', 'bool']

if len(savefile.split()) % 3 != 0:
    data = {}
    raise Exception('Invalid save file')

else:
    data = dict([
        (name, value) for name, value in [
            (savefile.split()[i*3+1], 
            locate(savefile.split()[i*3])(savefile.split()[i*3+2]))
            if savefile.split()[i*3] in allowedtypes else (None, None)
            for i in range(int(len(savefile.split())/3))
        ]
        ])

def save():
    file = open(savefolder+'/'+currentfilename, 'w')
    file.write('\n'.join(f'{type(data[v]).__name__} {v} {str(data[v])}' for v in data))

def get(name: str, default: any):
    if name in data: return data[name]
    return default

def shorten(num: int) -> str:
    # like im actually gonna need novemvigintillion
    # context: copied from a cc game which was copied from a roblox game i made a long time ago
    ends = ['','K','M','B','T','Qd','Qt','Sx','Sp','Oc','No','De','Un','DuD','TrD','QaD','QnD','SxD','SpD','OcD','NvD','V','Uv','DuV','TrV','QaV','QnV','SxV','SpV','OcV','NvV'];ending = 0
    while num >= 1000:ending+=1;num /=1000
    if num < 100: return str(num)[:4]+ends[ending]
    return str(num)[:3]+ends[ending]
def semishorten(num: int) -> str:
    return str(num)
    # shorten every million
    ends = ['','K','M','B','T','Qd','Qt','Sx','Sp','Oc','No','De','Un','DuD','TrD','QaD','QnD','SxD','SpD','OcD','NvD','V','Uv','DuV','TrV','QaV','QnV','SxV','SpV','OcV','NvV'];ending = 0
    while num >= 1_000_000:ending+=1;num /=1_000
    return str(int(num))+ends[ending]

def load_image(path, size):
    img = Image.open(path)
    img = img.resize(size)
    return ImageTk.PhotoImage(img)

##############################################
# CARDS
##############################################

cardlist = []
basecards = []

class Card:
    def __init__(self, name, rarity, ctype = 'basic', desc = '', power_multi=1, health_multi=1, bpm=1, bhm=1, border='normal'):
        self.name = name
        self.rarity = rarity
        self.ctype = ctype
        self.border = border
        self.desc = desc
        self.base_power = int(rarity ** .32 * power_multi * bpm * 5)
        self.base_health = int(rarity ** .32 * health_multi * bhm * 10)

        """     Quality looks garbage
        image = Image.open(image_folder+name+'.jpg')
        image = image.resize((133,200))
        t = ImageDraw.Draw(image)
        t.text(align='center', text=desc, fill =(255, 255,255), xy=(0,0))
        image.save(f'test.jpg')
        self.image = load_image('test.jpg', (133,200))
        """

        self.image = load_image(image_folder+name+'.jpg', (133,200))
        self.miniimage = load_image(image_folder+name+'.jpg', (33,50))

        self.owned = int(get(self.name+self.border, 0))
        self.wins = int(get(self.name+'Won', 0))
        self.bought = int(get(self.name+'Bought', 0))

        cardlist.append(self)
        if ctype=='basic' and border=='normal':basecards.append(self)

def make_card(name, rarity, ctype = 'basic', power_multi=1, health_multi=1, bpm=1, bhm=1, desc=''):
    base = Card(name, rarity, ctype, desc, power_multi, health_multi, bpm, bhm)
    gold = Card(name, rarity*100, ctype, desc, power_multi, health_multi, bpm, bhm, border='gold')
    plat = Card(name, rarity*10000, ctype, desc, power_multi, health_multi, bpm, bhm, border='plat')
    secret= Card(name, rarity*1000000, ctype, desc, power_multi, health_multi, bpm, bhm, border='secret')
    radiant = Card(name, rarity*100000000, ctype, desc, power_multi, health_multi, bpm, bhm, border='radiant')
    return base

farmer = make_card('Farmer', 2)
ghoul = make_card('Ghoul', 4)
wolf = make_card('Wolf', 8, desc="Lower the enemy's damage by 10% on entry")
bear = make_card('Bear', 20, desc="Attacks inflict a bleed for 10% damage that lasts 2 turns")
falcon = make_card('Falcon', 50, desc='This card cannot miss')
vampire = make_card('Vampire', 100, desc='Heal 25% of damage dealt after attacking')
samurai = make_card('Samurai', 200, desc='On entry, strike the enemy for 50% damage')
knight = make_card('Knight', 500, desc='Block 25% of damage taken')
orc = make_card('Orc', 800, desc='Deal 30% more damage, but take 10% recoil')
wyvern = make_card('Wyvern', 1_000, desc='Attacks apply a burn for 20% damage that lasts 2 turns')
griffin = make_card('Griffin', 1_250, desc='Gain 15% stats on entry')
gunslinger = make_card('Gunslinger', 8_000, desc='Attacks inflict a mark. Deal 150% damage to marked cards')
dragon = make_card('Dragon', 20_000, desc="Deal 70% damage, but apply a burn for 2 turns that deals 40% damage")
fiend = make_card('Fiend', 20_000, desc='Gain 10% dodge chance every turn, up to 30%')
nurse = make_card('Nurse', 50_000, desc="While alive, heal the active ally by 20% of their max health each turn. Doesn't stack")
porcupine = make_card('Porcupine', 200_000, desc='Attacks against this card take 50% recoil damage')

brunhilde = make_card('Brunhilde', 5_000, 'Boss', desc="On entry, grant all allies a shield equal to 25% of this card's max health")
berserker = make_card('Berserker', 20_000, 'Boss', desc="After every turn, gain 10% damage and 10% damage reduction. Max 3 stacks")
thor = make_card('Thor', 100_000, 'Boss', desc='Every turn, deal 10% damage to all opponents')
kraken = make_card('Kraken', 500_000, 'Boss', desc='Attack 3 times dealing 50% damage')

spartan = make_card('Spartan', 50_000, 'Boss', desc='Gain 10% stats for each living ally on entry')
alexander = make_card('Alexander', 200_000, 'Boss', desc='This card has a 30% chance to block attacks')
achilles = make_card('Achilles', 800_000, 'Boss', desc="Attacks pierce dealing 50% damage to the next enemy")
hercules = make_card('Hercules', 3_500_000, 'Boss', desc="Each turn gain a stack giving 20% health and a 5% heal. Max 3 stacks")

imp = make_card('Imp', 1_000_000, 'Boss', desc='Attacks inflict a brand. Enemies take 40% more damage per brand')
demon = make_card('Demon', 4_000_000, 'Boss', desc='While active, all enemies burn for 20% damage per turn')
cerberus = make_card('Cerberus', 15_000_000, 'Boss', desc="While alive, enemies take 50% more burn damage")
hades = make_card('Hades', 50_000_000, 'Boss', desc='Deal 50% more damage. Uppon killing an enemy, heal 25% of max hp')

fire_knight = make_card('Fire_knight', 15_000_000, 'Boss', desc='Alternate between inflicting a 50% dmg burn for 2 turns and dealing 130% damage')
water_knight = make_card('Water_knight', 80_000_000, 'Boss', desc='Alternate between healing 50% of damage dealt and block 25% damage')
dark_knight = make_card('Dark_knight', 250_000_000, 'Boss', desc="On entry, sacrifice 50% of the next card's health and gain it as damage")
holy_knight = make_card('Holy_knight', 1_000_000_000, 'Boss', desc="Revive with max health on first death")

famine = make_card('Famine', 100_000_000, 'Boss', desc='While active, enemies lose 10% max health per turn')
war = make_card('War', 400_000_000, 'Boss', desc='Gain 50% damage every turn')
death = make_card('Death', 1_200_000_000, 'Boss', desc='While alive, execute enemies below 25% health')
conquest = make_card('Conquest', 3_500_000_000, 'Boss', desc='Gain 10% stats for each fallen ally on entry and after every kill')

hero = make_card('Hero', 50_000, 'Market', desc='Increase damage by 50% of missing health')
commander = make_card('Commander', 1_000_000, 'Market', desc='On entry, all friendly cards gain 15% stats')
assassin = make_card('Assassin', 35_000_000, 'Market', desc="25% chance to dodge and inflict poison dealing 10% damage")
kaiju = make_card('Kaiju', 200_000_000, 'Market')

minotaur = make_card('Minotaur', 80_000, 'Dungeon', desc='Gain 35% damage reduction for 2 turns on entry')
#Minotaur = make_card('Minotaur', 80_000, 'Dungeon', desc='Gain 35% damage reduction for 2 turns on entry')

##############################################
# ROLL
##############################################

rewards = []
curmax = 0

def fix_rates():
    global rewards,curmax

    rollable_cards = []
    #for card in basecards:rollable_cards.append(card)
    for card in cardlist:
        if card.ctype == 'basic':rollable_cards.append(card)
        if card.ctype == 'Boss':
            if card.wins > 0:rollable_cards.append(card)
        if card.ctype == 'Market':
            if card.bought > 0:rollable_cards.append(card)

    curmax = 0
    for card in rollable_cards:
        rarity = 1/card.rarity
        curmax += rarity

    cur = curmax
    for card in rollable_cards:
        rarity = 1/card.rarity
        cur -= rarity
        rewards.append([cur, card])

def quick_roll(luckm):
    x = 1000000000000000
    luck = randint(1,x)/x/luckm
    
    luck*=curmax
    for reward in rewards:
        if luck>reward[0]:return reward[1]

def mass_roll(amt):

    luck = 1
    for item in items:
        luck += items[item].luck
    for item in items:
        luck += int(luck*(items[item].lm-1))

    res = [quick_roll(luck) for i in range(amt)]

    for i in res:
        i.owned += 1

    for card in cardlist:
        if card.owned > 0:
            data[card.name+card.border] = card.owned

    return res

rollcd = 0
rolledcard = None
quickroll = get('quickroll', False)
autoroll = get('autoroll', False)
def roll_medium():
    global rollcd
    if rollcd > 0: return
    rollcd = 100
    luck = 1
    for item in items:
        rollcd *= items[item].rollspeed
        luck += items[item].luck
    for item in items:
        luck += int(luck*(items[item].lm-1))

    reward = quick_roll(luck)
    reward.owned += 1
    data[reward.name+reward.border] = reward.owned
    save()

    
    if quickroll:
        rolledcardframe['image'] = reward.miniimage
        rolledcardframe.place(width=33,height=50,y=440,x=384)
        rolledcardraritylabel['fon']=("Helvetica", "8")
        rolledcardraritylabel['text'] = shorten(reward.rarity)
        rolledcardraritylabel.place(width=64,height=16,y=425,x=368)
    else:
        rolledcardframe['image'] = reward.image
        rolledcardframe.place(width=133,height=200,y=150,x=334)
        rolledcardraritylabel['fon']=("Helvetica", "16")
        rolledcardraritylabel['text'] = shorten(reward.rarity)
        rolledcardraritylabel.place(width=64,height=16,y=130,x=368)

##############################################
# DECK
##############################################

def nametocard(name):
    for card in cardlist:
        if card.name+card.border == name:return card

eq1 = nametocard(get('eq1', None))
eq2 = nametocard(get('eq2', None))
eq3 = nametocard(get('eq3', None))
eq4 = nametocard(get('eq4', None))
eqs = [eq1,eq2,eq3,eq4]

def equip(self):
    global eqs
    cu = 1
    for i in eqs:
        if i==None:continue
        if i.name == self.name:cu+=1
    if cu>self.owned: return
    for i in range(4):
        if eqs[i] == None:eqs[i] = self;break

    update_equip()

def unequip(i):
    eqs[i] = None
    update_equip()

def card_showcase(pos, card):
    x = int(pos%15*33.3)+266
    if x > 480:
        x = int(pos%15*33.3)+33

    deck_showcase_frame.place(x=x, y=int(pos/15)*50+75)
    deck_showcase_image.config(image=card.image)
    deck_showcase_health.config(text=card.base_health)
    deck_showcase_power.config(text=card.base_power)
    deck_showcase_owned.config(text=f'x{shorten(card.owned)}')
    deck_showcase_rarity.config(text=f'{shorten(card.rarity)}')
    deck_showcase_desc.config(text=card.desc)
def showcase_hide(event):
    deck_showcase_frame.place(x=-999999)

bordertobg = {'normal': 'black', 'gold': '#FFFF7B', 'plat': '#7EB2FF', 'secret': '#FF7E7E', 'radiant': "#5DE26F"}

inventoryitems = []
class deck_item():
    def __init__(self, card):
        self.i = len(inventoryitems)

        cardbutton = tk.Button(deck_inventory_frame, image=card.miniimage)
        cardbutton.place(x=int(self.i%15*33.3), y=int(self.i/15)*50, width=33, height=50)

        cardbutton.bind("<Enter>", func=lambda x:card_showcase(self.i, card))
        cardbutton.bind('<Leave>', func=showcase_hide)
        cardbutton.bind('<Button-1>', func=lambda x:equip(card))

        cardbutton.config(bg=bordertobg[card.border])

        self.cardbutton = cardbutton
        inventoryitems.append(self)

    def delete(self):
        self.cardbutton.destroy()

def update_inventory():
    global inventoryitems
    #for frame in deck_inventory_frame.winfo_children():frame.destroy() 
    for item in inventoryitems:item.delete()
    inventoryitems = []

    sortedlist = []

    for card in cardlist:
        if card.owned > 0:
            i = 0
            while i < len(sortedlist):
                if sortedlist[i].base_power < card.base_power:break
                i+=1
            sortedlist.insert(i,card)

    i=0
    for card in sortedlist:
        c = deck_item(card)
        i+=1
        if i == 15*7:break

def update_equip():
    global data
    for _,i in enumerate(eqs):
        if i == None:eqbutton[_].config(image='', bg='black')
        else:eqbutton[_].config(image=i.miniimage, bg=bordertobg[i.border])

    for i in range(4):
        if eqs[i] != None:data[f'eq{i+1}'] = eqs[i].name+eqs[i].border
        else: data[f'eq{i+1}'] = None

##############################################
# ITEMS
##############################################

eqimg = []
eqframe = tk.Frame(root, bg='black')
eqframe.place(x=600,y=450,height=50,width=200)

lucklabel = tk.Label(root, bg='black', fg='#55FF55')
lucklabel.place(x=700, y=435, height=15, width=100)

def updequip():
    global eqimg
    for item in eqimg:item.destroy()
    eqimg = []
    tl = 0

    for item in items:
        e = tk.Label(eqframe, image=items[item].img)
        e.place(x=150-len(eqimg)*50, y=0, width=50, height=50)
        tl += items[item].luck

        eqimg.append(e)
        
    for item in items:
        tl += int(tl*(items[item].lm-1))

    if tl > 0:
        lucklabel.config(text=f'+{tl} luck')
    else:
        lucklabel.config(text='')

def useitem(self):
    if self.itemtype in ['Charm', 'Gear', 'Artifact']:
        items[self.itemtype] = self
        data[self.itemtype] = self.name
        updequip()

    if self.itemtype == 'Pack':
        res = mass_roll(self.rollspeed)
        self.owned -= 1
        data[f'{self.name}owned'] = self.owned
        update_items()
        itemshowcase_hide(0)

        scaledres = []
        for card in res:
            if card in scaledres:continue

            _=0
            for _, c in enumerate(scaledres):
                if card.rarity > c.rarity:scaledres.insert(_, card);break

            else:scaledres.append(card)
            

        pack_res.place(x=100, y=50)

        for b in packresc:b.destroy()

        for i, c in enumerate(scaledres):
            b = tk.Button(pack_res, image=c.miniimage, bg=bordertobg[c.border])
            b.place(x=int(i%15*33.3), y=int(i/15)*50, width=33, height=50)
            packresc.append(b)
            if i==7*15:return

def item_showcase(pos, card):
    item_showcase_frame.place(x=int(pos%15*50)+266, y=int(pos/15)*50+75)
    item_showcase_image.config(image=card.limg)
    item_showcase_name.config(text=card.name)
    #item_showcase_desc.config(text=card.desc, fg=card.fg)
    #deck_showcase_owned.config(text=f'{card.owned}x')
    #deck_showcase_rarity.config(text=f'{card.rarity}')
    for desc in item_showcase_descs:desc.config(text='')
    for _, desc in enumerate(card.desc):item_showcase_descs[_].config(text=desc[1], fg=desc[0])

    if card.itemtype == 'Pack':item_showcase_descs[1].config(text=f'{card.owned} owned', fg='white')

def itemshowcase_hide(event):
    item_showcase_frame.place(x=-999999)

itemitems = []
class inventory_item():
    def __init__(self, card):
        self.i = len(itemitems)

        cardbutton = tk.Button(inventory_frame, image=card.img)
        cardbutton.place(x=25+int(self.i%15*50), y=25+int(self.i/15)*50, width=50, height=50)

        cardbutton.bind("<Enter>", func=lambda x:item_showcase(self.i, card))
        cardbutton.bind('<Leave>', func=itemshowcase_hide)
        cardbutton.bind('<Button-1>', func=lambda x:useitem(card))

        cardbutton.config(bg='black')
        
        self.cardbutton = cardbutton
        itemitems.append(self)

    def delete(self):
        self.cardbutton.destroy()

def update_items():
    global itemitems
    #for frame in deck_inventory_frame.winfo_children():frame.destroy() 
    for item in itemitems:item.delete()
    itemitems = []

    i = 0
    for item in itemlist:
        if item.owned > 0:
            c = inventory_item(item)
            i+=1
            if i == 15*7:break

##############################################
# GUI
##############################################

def quickrollswap(event):
    global quickroll
    quickroll = not quickroll
    data['quickroll'] = quickroll
    if quickroll:quick_roll_button['text']='Quick roll: on'
    else:quick_roll_button['text']='Quick roll: off'
quick_roll_button = tk.Button(root, text='Quick roll: off', bg='#101010', fg='#FFFFFF', anchor='w')
if quickroll:quick_roll_button['text']='Quick roll: on'
quick_roll_button.place(x=200, y=0, width=100, height=15)
quick_roll_button.bind('<Button-1>', quickrollswap) 

def autorollswap(event):
    global autoroll
    autoroll = not autoroll
    data['autoroll'] = autoroll
    if autoroll:auto_roll_button['text']='Auto roll: on'
    else:auto_roll_button['text']='Auto roll: off'
auto_roll_button = tk.Button(root, text='Auto roll: off', bg='#101010', fg='#FFFFFF', anchor='w')
if autoroll:auto_roll_button['text']='Auto roll: on'
auto_roll_button.place(x=200, y=15, width=100, height=15)
auto_roll_button.bind('<Button-1>', autorollswap) 


roll_button_img = tk.PhotoImage(file=path+'images/BlueTarget.png')
roll_button = tk.Button(root, text='gacha\n¥100K', bg='#101010',fg='#FFFFFF', image=roll_button_img, command=roll_medium)
roll_button.place(x=350,y=200, width=100, height=100)

rolledcardframe = tk.Label(root, bg='black', image=None)
rolledcardframe.place(width=33,height=50,y=440,x=384)

rolledcardraritylabel = tk.Label(root, bg='black', fg='#FFFFFF', font=("Helvetica", "16"), text='')


coins = get('Coins', 0)
coinslabel = tk.Label(root, bg='black', fg='#ffff55', text=f'{shorten(coins)} coins', anchor='e')
coinslabel.place(x=600,height=25, width=200, y=0)


#Open things

def open_deck():deck_frame.place(x=100,y=50);update_inventory();update_equip()
deck_image = load_image('images/Deck.jpg', (50,50))
open_deck_button = tk.Button(root, command=open_deck, image=deck_image)
open_deck_button.place(x=0,y=200,width=50,height=50)

def open_forge():forge_frame.place(x=100,y=50)
anvil_image = load_image('images/Anvil.jpg', (50,50))
open_anvil_button = tk.Button(root, command=open_forge, image=anvil_image)
open_anvil_button.place(x=50,y=250,width=50,height=50)

def open_inventory():inventory_frame.place(x=100,y=50);update_items()
inventory_image = load_image('images/Item.jpg', (50,50))
open_inventory_button = tk.Button(root, command=open_inventory, image=inventory_image)
open_inventory_button.place(x=50,y=200,width=50,height=50)

def open_bossfight():bossfight_frame.place(x=200,y=50)
bossfight_image = load_image('images/Skull.jpg', (50,50))
open_bossfight_button = tk.Button(root, command=open_bossfight, image=bossfight_image)
open_bossfight_button.place(x=0,y=250,width=50,height=50)

def open_towers():towers_frame.place(x=200,y=50)
tower_image = load_image('images/Tower.jpg', (50,50))
open_towers_button = tk.Button(root, command=open_towers, image=tower_image)
open_towers_button.place(x=0,y=300,width=50,height=50)

def open_market():market_frame.place(x=200,y=50);refresh_market()
market_image = load_image('images/Market.jpg', (50,50))
open_market_button = tk.Button(root, command=open_market, image=market_image)
open_market_button.place(x=50,y=300,width=50,height=50)

#market

market_frame = tk.Frame(root, width=400,height=400, bg='#101010')

def exit_market():market_frame.place(x=-9999)
market_frame_button = tk.Button(market_frame, bg='#101010', fg='#FFFFFF', text='X', command=exit_market)
market_frame_button.place(x=350, y=0, width=50, height=25)

#towers

towers_frame = tk.Frame(root, width=400,height=400, bg='#101010')

def exit_towers():towers_frame.place(x=-9999)
towers_frame_button = tk.Button(towers_frame, bg='#101010', fg='#FFFFFF', text='X', command=exit_towers)
towers_frame_button.place(x=350, y=0, width=50, height=25)


#bossfights

bossfight_frame = tk.Frame(root, width=400,height=400, bg='#101010')

def exit_bossfight():bossfight_frame.place(x=-9999)
exit_bossfight_button = tk.Button(bossfight_frame, bg='#101010', fg='#FFFFFF', text='X', command=exit_bossfight)
exit_bossfight_button.place(x=350, y=0, width=50, height=25)




#inventory

inventory_frame = tk.Frame(root, width=600,height=400, bg='#101010')

def exit_inventory():inventory_frame.place(x=-9999)
exit_inventory_button = tk.Button(inventory_frame, bg='#101010', fg='#FFFFFF', text='X', command=exit_inventory)
exit_inventory_button.place(x=550, y=0, width=50, height=25)

packresc = []
pack_res = tk.Frame(root, bg='#101010', width=600, height=400)
def exit_rolls():pack_res.place(x=-9999)
exit_rolls_button = tk.Button(pack_res, bg='#101010', fg='#FFFFFF', text='X', command=exit_rolls)
exit_rolls_button.place(x=550, y=0, width=50, height=25)


#forge

forge_frame = tk.Frame(root, width=600,height=400, bg='#101010')
forge_items = tk.Frame(forge_frame, width=100, height=400, bg='#101010')
forge_items.place(x=0,y=0)

def exit_forge():forge_frame.place(x=-9999)
exit_forge_button = tk.Button(forge_frame, bg='#101010', fg='#FFFFFF', text='X', command=exit_forge)
exit_forge_button.place(x=550, y=0, width=50, height=25)


item_showcase_frame = tk.Frame(root, width=100, height=200, bg='#101010')
item_showcase_image = tk.Label(item_showcase_frame)
item_showcase_image.place(x=0,y=15,width=100,height=100)

item_showcase_name = tk.Label(item_showcase_frame, bg='#101010', fg='#FFFFFF')
item_showcase_name.place(x=0,y=0,width=100,height=25)

item_showcase_descs = [] 
for i in range(4):
    item_showcase_desc = tk.Label(item_showcase_frame, bg='#101010', fg='#FFFFFF')
    item_showcase_desc.place(x=0,y=125+i*25,width=100,height=25)
    item_showcase_descs.append(item_showcase_desc)



#deck

deck_frames = {}
deck_frame = tk.Frame(root, width=600,height=400, bg='#101010')
deck_inventory_frame = tk.Frame(deck_frame, width=500,height=350, bg='#101010')
deck_inventory_frame.place(x=100,y=25)

def exit_deck():
    deck_frame.place(x=-9999)
exit_deck_button = tk.Button(deck_frame, bg='#101010', fg='#FFFFFF', text='X', command=exit_deck)
exit_deck_button.place(x=550, y=0, width=50, height=25)

deck_showcase_frame = tk.Frame(root, width=133, height=300, bg='#101010')
deck_showcase_image = tk.Label(deck_showcase_frame, fg='white')
deck_showcase_image.place(x=0,y=15,width=133,height=200)

deck_showcase_health = tk.Label(deck_showcase_frame, fg='#55FF55', bg='#101010', text='11')
deck_showcase_health.place(x=66,y=200, width=67, height=25)
deck_showcase_power = tk.Label(deck_showcase_frame, fg='#FF5555', bg='#101010', text='11')
deck_showcase_power.place(x=0,y=200, width=66, height=25)
deck_showcase_owned = tk.Label(deck_showcase_frame, fg='#FFFFFF', bg='#101010', text='11')
deck_showcase_owned.place(x=83,y=0, width=50, height=15)
deck_showcase_rarity = tk.Label(deck_showcase_frame, fg='#FFFFFF', bg='#101010', text='11')
deck_showcase_rarity.place(x=0,y=0, width=70, height=15)
deck_showcase_desc = tk.Label(deck_showcase_frame, fg='#FFFFFF', bg='#101010', text='11', wraplength=133, anchor='n')
deck_showcase_desc.place(x=0,y=225, width=133, height=50)

deck_equip1_button = tk.Button(deck_frame, bg='#101010', command=lambda:unequip(0))
deck_equip1_button.place(x=37, y=25, width=33, height=50)
deck_equip2_button = tk.Button(deck_frame, bg='#101010', command=lambda:unequip(1))
deck_equip2_button.place(x=37, y=125, width=33, height=50)
deck_equip3_button = tk.Button(deck_frame, bg='#101010', command=lambda:unequip(2))
deck_equip3_button.place(x=37, y=225, width=33, height=50)
deck_equip4_button = tk.Button(deck_frame, bg='#101010', command=lambda:unequip(3))
deck_equip4_button.place(x=37, y=325, width=33, height=50)

eqbutton = [deck_equip1_button,deck_equip2_button,deck_equip3_button,deck_equip4_button]

##############################################
# BATTLE
##############################################

def eqtobattlecard():
    return [
        BattleCard(card) for card in eqs
    ]

battleframe = tk.Frame(root, bg='black', width=800, height=500)

fcard = tk.Label(battleframe)
fcardname = tk.Label(battleframe, bg='black', fg='white', font=('Helvetica', 15))
fcardattack = tk.Label(battleframe, bg='black', fg='red', font=('Helvetica', 10))
fcarfdhpbg = tk.Frame(battleframe, bg='#101010', width=133, height=15)
fcarfdhpfg = tk.Frame(battleframe, bg='#6ae26a', width=133, height=15)
fcarddesc = tk.Label(battleframe, bg='black', fg='white', anchor='n', wraplength=133)

ecard = tk.Label(battleframe)
ecardname = tk.Label(battleframe, bg='black', fg='white', font=('Helvetica', 15))
ecardattack = tk.Label(battleframe, bg='black', fg='red', font=('Helvetica', 10))
ecarfdhpbg = tk.Frame(battleframe, bg='#101010', width=133, height=15)
ecarfdhpfg = tk.Frame(battleframe, bg="#6ae26a", width=133, height=15)
ecarddesc = tk.Label(battleframe, bg='black', fg='white', anchor='n', wraplength=133)

fightcardslist = []
fightcardsframe = tk.Frame(battleframe, width=200, height=50, bg='black')
fightcardsframe.place(x=300, y=450)

efightcardslist = []
efightcardsframe = tk.Frame(battleframe, width=200, height=50, bg='black')
efightcardsframe.place(x=300, y=0)

infinitegoldlabel = tk.Label(battleframe, bg='black', fg='#FFFF55', anchor='e')
infinitegoldlabel.place(x=600, y=50, width=200, height=25)
infinitefloorlabel = tk.Label(battleframe, bg='black', fg='white', anchor='e')
infinitefloorlabel.place(x=600, y=25, width=200, height=25)

def updcard(cards, ecards, cc, ce):
    fcard.config(image=cards[cc].image)
    fcardname.config(text=cards[cc].name)
    fcardattack.config(text=cards[cc].dmg)
    fcarfdhpfg.config(width=max(0,int(133*cards[cc].hp/cards[cc].maxhp)), bg='#6ae26a')
    fcarddesc.config(text=cards[cc].card.desc)

    try:
        if cards[cc].effects['shield'] > 0:fcarfdhpfg.config(bg="#2773FF")
    except:pass
    if cards[cc].hp <= 0:fcarfdhpfg.config(bg="#101010")

    ecard.config(image=ecards[ce].image)
    ecardname.config(text=ecards[ce].name)
    ecardattack.config(text=ecards[ce].dmg)
    ecarfdhpfg.config(width=max(0,int(133*ecards[ce].hp/ecards[ce].maxhp)), bg='#6ae26a')
    ecarddesc.config(text=ecards[ce].card.desc)

    try:
        if ecards[ce].effects['shield'] > 0:ecarfdhpfg.config(bg="#2773FF")
    except:pass
    if ecards[ce].hp <= 0:ecarfdhpfg.config(bg="#101010")

    if ininfinite:    
        infinitefloorlabel.config(text=f'Floor {infinitefloor}')
        cnamt = inf_coin()
        infinitegoldlabel.config(text=f'+{shorten(cnamt)} coins')

def updmini(cards, ecards):
    global fightcardslist, efightcardslist
    
    for c in fightcardslist:c.destroy();fightcardslist=[]
    for c in efightcardslist:c.destroy();efightcardslist=[]

    for card in cards:
        if card.hp > 0:
            e = tk.Label(fightcardsframe, image=card.card.miniimage)
            e.place(x=len(fightcardslist)*33, y=0, width=33, height=50)
            fightcardslist.append(e)
    for card in ecards:
        if card.hp > 0:
            e = tk.Label(efightcardsframe, image=card.card.miniimage)
            e.place(x=len(efightcardslist)*33, y=0, width=33, height=50)
            efightcardslist.append(e)

def plcard(pos):
    fcard.place(x=pos,y=150,width=133,height=200)
    fcardname.place(x=pos,y=125,width=133,height=25)
    fcarfdhpbg.place(x=pos,y=360)
    fcarfdhpfg.place(x=pos,y=360)
    fcardattack.place(x=pos,y=375,width=133)
    fcarddesc.place(x=pos,y=400,width=133)

def plecard(epos):
    ecard.place(x=epos,y=150,width=133,height=200)
    ecardname.place(x=epos,y=125,width=133,height=25)
    ecarfdhpbg.place(x=epos,y=360)
    ecarfdhpfg.place(x=epos,y=360)
    ecardattack.place(x=epos,y=375,width=133)
    ecarddesc.place(x=epos,y=400,width=133)

class BattleCard:
    def __init__(self, card, hp=None, dmg=None):
        self.card = card
        self.hp = hp
        self.dmg = dmg
        if hp == None:self.hp=self.card.base_health
        if dmg == None:self.dmg = self.card.base_power
        self.maxhp = self.hp
        self.image = self.card.image
        self.name = self.card.name
        self.basehp= self.hp
        self.basedmg = self.dmg

        self.effects = {
            'Burn':[],
            'Bleed':[],
            'Poisons':[],
            'Brand': 0,
            'nh': False,
            'Mark': 0,
            'tc':0
        }

resultlabel = tk.Label(battleframe, bg='black', font=('Helvetica', 25))
resultdesclabel = tk.Label(battleframe, bg='black', fg='white')

def victory(context):
    global coins, infinitefloor

    if type(context) == int:
        infinitefloor += 1
        data['infinitefloor'] = infinitefloor
        infinite_floor()
        return
    
    resultlabel.config(fg='#55FF55', text='Victory!')
    resultlabel.place(x=300,y=200,width=200)
    if type(context) == BossReward:
        resultdesclabel.config(fg='white', text=f'You can now roll {context.card.name}')
        resultdesclabel.place(x=300,y=250,width=200)
        context.card.wins += 1
        data[f'{context.card.name}Won'] = context.card.wins
        fix_rates()

    root.update()
    sleep(2)
    resultlabel.place(x=-10000)
    resultdesclabel.place(x=-10000)
    battleframe.place(x=-10000)


def loss(context=None):
    global infinitefloor, ininfinite, coins
    if type(context) == int:coins += inf_coin();infinitefloor = 0;coinslabel.config(text=f'{shorten(coins)} coins'); data['infinitefloor'] = 0;data['Coins'] = coins
    ininfinite = False

    resultlabel.config(fg='#FF5555', text='You lost!')
    resultlabel.place(x=300,y=200,width=200)
    root.update()
    sleep(2)
    resultlabel.place(x=-10000)
    battleframe.place(x=-10000)

def before_attack(dmg, cards, ecards, cc, ce):

    try:
        if not cards[cc].name in ['Falcon']:
            if randint(1, 100) <= ecards[ce].effects['fdc']:dmg=0
            if randint(1, 100) <= 25 and ecards[ce].name == 'Assassin':dmg=0;cards[cc].effects['Poisons'].append([ecards[ce].dmg, 100])
    except:pass
    
    try:dmg*=1-(.1*ecards[ce].effects['berserk'])
    except:pass

    if cards[cc].name == 'Orc':dmg = int(dmg*1.3)
    if cards[cc].name == 'Kraken': dmg = int(dmg*.5)
    if cards[cc].name == 'Dragon': dmg = int(dmg*.7)
    if cards[cc].name == 'Hades': dmg = int(dmg*1.5)
    if cards[cc].name == 'Hero': dmg += int((cards[cc].maxhp - cards[cc].hp)*.5)
 
    if ecards[ce].name == 'Knight':dmg = int(dmg*.75) 

    if ecards[ce].name == 'Alexander' and randint(1,10) <=3:dmg = 0

    if cards[cc].name == 'Gunslinger' and ecards[ce].effects['Mark'] > 0:dmg = int(dmg*1.5)

    dmg *= 1+ecards[ce].effects['Brand']*.4

    try:
        if ecards[ce].effects['mb'] > 0:dmg = int(dmg*.65)
    except:pass

    if cards[cc].name == 'Fire_knight' and cards[cc].effects['tc'] % 2 == 1:dmg = int(dmg*1.3)
    if ecards[ce].name == 'Water_knight' and ecards[ce].effects['tc'] % 2 == 1:dmg = int(dmg*.75)
    
    try:
        if ecards[ce].effects['shield'] > 0:
            if ecards[ce].effects['shield'] > dmg:ecards[ce].effects['shield']-=dmg;dmg=0
            else:dmg-=ecards[ce].effects['shield'];ecards[ce].effects['shield']=0
    except:pass

    return dmg

def fight_effects(cards, ecards, cc, ce):
    cards[cc].effects['tc'] += 1
    bm=1
    for card in ecards:
        if card.name == 'Cerberus' and card.hp > 0:bm*=1.5

    for card in cards:
        for bleed in card.effects['Bleed']:
            if bleed[1] > 0:card.hp -= bleed[0];bleed[1]-=1
        for burn in card.effects['Burn']:
            if burn[1] > 0:card.hp -= burn[0]*bm;burn[1]-=1
        for poison in card.effects['Poisons']:
            if poison[1] > 0:card.hp -= poison[0];poison[1]-=1
        if card.effects['nh']:
            heal = min(card.maxhp-card.hp, int(card.maxhp*.2))
            card.hp += heal
            card.effects['nh'] = False
        try:card.effects['mb'] -= 1
        except:pass
    return cards

def after_attack(dealt, cards, ecards, cc, ce, loop=True):
    if cards[cc].name == 'Berserker':
        try:
            if cards[cc].effects['berserk'] < 3: cards[cc].effects['berserk']+=1;cards[cc].dmg+=int(cards[cc].dmg*.1)
        except:cards[cc].effects['berserk'] = 1;cards[cc].dmg+=int(cards[cc].dmg*.1)

    if cards[cc].name == 'Thor':
        for _, card in enumerate(ecards):
            if card.hp<=0:continue
            dmg = cards[cc].dmg*.1
            dmg = before_attack(dmg, cards, ecards, cc, _)
            ecards[_].hp -= dmg
            #cards, ecards = after_attack(dmg, cards, ecards, cc, _)
            updcard(cards,ecards,cc,ce)

    for card in cards:
        if card.name == 'Nurse' and card.hp > 0:
            cards[cc].effects['nh'] = True 
            #try:card.effects['shield'] += heal
            #except:card.effects['shield'] = heal
            
    if cards[cc].name == 'Achilles' and ce+1<len(ecards):
        if ecards[ce+1].hp > 0:
            dmg = cards[cc].dmg*.5
            dmg = before_attack(dmg, cards, ecards, cc, ce+1)
            ecards[ce+1].hp -= dmg
            #cards, ecards = after_attack(dmg, cards, ecards, cc, _)
            updcard(cards,ecards,cc,ce)

    if cards[cc].name == 'Vampire':
        heal = min(cards[cc].maxhp-cards[cc].hp, int(dealt*.25))
        cards[cc].hp += heal

    if cards[cc].name == 'Orc':cards[cc].hp -= int(dealt*.1)
    
    if cards[cc].name == 'Bear':ecards[ce].effects['Bleed'].append([cards[cc].dmg*.1, 2])
    #if cards[cc].name == 'Cerberus':ecards[ce].effects['Bleed'].append([cards[cc].dmg*.4, 2])

    if cards[cc].name == 'Wyvern':ecards[ce].effects['Burn'].append([cards[cc].dmg*.2, 2])
    if cards[cc].name == 'Dragon':ecards[ce].effects['Burn'].append([cards[cc].dmg*.4, 2])

    if cards[cc].name == 'Demon':
        for card in ecards:card.effects['Burn'].append([cards[cc].dmg*.2, 1])
    
    if cards[cc].name == 'Kraken' and loop:
        updcard(cards, ecards, cc, ce)
        root.update()
        sleep(.5)
        for i in range(2):
            dmg = cards[cc].dmg*.5
            dmg = before_attack(dmg, cards, ecards, cc, ce)
            ecards[ce].hp -= dmg
            cards, ecards = after_attack(dmg, cards, ecards, cc, ce, False)
            updcard(cards, ecards, cc, ce)
            root.update()
            sleep(.5)

    if cards[cc].name == 'Hercules':
        try:heal = min(cards[cc].maxhp-cards[cc].hp, int(dealt*.05*min(3, cards[cc].effects['Hercules'])));cards[cc].hp += heal
        except:pass
        try:cards[cc].effects['Hercules']+=1
        except:cards[cc].effects['Hercules']=1
        if cards[cc].effects['Hercules'] <= 3:
            cards[cc].hp *= 1.2
            cards[cc].maxhp *= 1.2

    if cards[cc].name == 'Imp':ecards[ce].effects['Brand'] += 1
    if cards[cc].name == 'Gunslinger':ecards[ce].effects['Mark'] += 1

    if cards[cc].name == 'Fiend':
        try: cards[cc].effects['fdc'] = min(30, cards[cc].effects['fdc']+10)
        except:cards[cc].effects['fdc'] = 10

    if ecards[ce].name == 'Porcupine':
        cards[cc].hp -= int(dealt*.5)

    if cards[cc].name == 'Famine':
        for c in ecards:
            c.hp = int(c.hp*.9)
            c.maxhp = int(c.maxhp*.9)

    if cards[cc].name == 'War':
        cards[cc].dmg = int(cards[cc].dmg*1.5)

    for c in cards:
        if c.name == 'Death' and c.hp > 0:
            for e in ecards:
                if e.hp < e.maxhp*.25:e.hp = 0

    if cards[cc].name == 'Fire_knight' and cards[cc].effects['tc'] % 2 == 0:ecards[ce].effects['Burn'].append([int(cards[cc].dmg*.5), 2])
    if cards[cc].name == 'Water_knight' and cards[cc].effects['tc'] % 2 == 0:
        heal = min(cards[cc].maxhp-cards[cc].hp, int(dealt*.5))
        cards[cc].hp += heal

    return cards, ecards

def on_entry(cards, ecards, cc, ce):
    if cards[cc].name == 'Samurai':
        dmg = cards[cc].dmg*.5
        dmg = before_attack(dmg, cards, ecards, cc, ce)
        ecards[ce].hp -= dmg
        cards, ecards = after_attack(dmg, cards, ecards, cc, ce)
        updcard(cards,ecards,cc,ce)

    if cards[cc].name == 'Wolf':
        ecards[ce].dmg=int(ecards[ce].dmg*.9)

    if cards[cc].name == 'Brunhilde':
        for card in cards:
            try:card.effects['shield'] += cards[cc].maxhp*.25
            except:card.effects['shield'] = cards[cc].maxhp*.25

    if cards[cc].name == 'Spartan':
        for card in cards:
            if card.hp > 0 and card != cards[cc]:cards[cc].hp+=int(cards[cc].basehp*.1);cards[cc].dmg+=int(cards[cc].basedmg*.1);cards[cc].maxhp+=int(cards[cc].basehp*.1)

    if cards[cc].name == 'Griffin':cards[cc].hp = int(cards[cc].hp * 1.15);cards[cc].maxhp = int(cards[cc].maxhp * 1.15);cards[cc].dmg = int(cards[cc].dmg * 1.15)

    if cards[cc].name == 'Commander':
        for card in cards:
            card.hp = int(card.hp*1.15+.01)
            card.maxhp = int(card.maxhp*1.15+.01)
            card.dmg = int(card.dmg*1.15+.01)

    if cards[cc].name == 'Conquest':
        amt=1
        for c in cards:
            if c.hp <= 0:amt+=.1
        cards[cc].hp = int(cards[cc].hp*amt)
        cards[cc].maxhp = int(cards[cc].maxhp*amt)
        cards[cc].dmg = int(cards[cc].dmg*amt)

    if cards[cc].name == 'Minotaur':
        cards[cc].effects['mb'] = 3

    if cards[cc].name == 'Dark_knight':
        try:
            dmg=int(cards[cc+1].hp*.5)
            cards[cc+1].hp = dmg
            cards[cc].dmg += dmg
        except:pass

    return cards, ecards

def killed_enemy(cards, ecards, cc, ce):
    
    if ecards[ce].name == 'Holy_knight':
        try:ecards[ce].effects['revive'] += 1
        except:
            ecards[ce].effects['revive'] = 0
            ecards[ce].maxhp = int(ecards[ce].maxhp*1.2)
            ecards[ce].dmg = int(ecards[ce].dmg*1.2)
            ecards[ce].hp = ecards[ce].maxhp
            return cards, ecards

    if cards[cc].name == 'Hades':
        heal = min(cards[cc].maxhp-cards[cc].hp, int(cards[cc].maxhp*.25))
        cards[cc].hp += heal
        
    if cards[cc].name == 'Conquest':
        amt=1
        for c in cards:
            if c.hp <= 0:amt+=.1
        cards[cc].hp = int(cards[cc].hp*amt)
        cards[cc].maxhp = int(cards[cc].maxhp*amt)
        cards[cc].dmg = int(cards[cc].dmg*amt)

    return cards, ecards

def fight(cards, ecards, context=None):
    if len(cards) == 0 or len(ecards) == 0:return
    battleframe.place(x=0,y=0)

    pos = 150
    epos = 500

    updcard(cards, ecards, 0, 0)
    plcard(pos)
    plecard(epos)
    updmini(cards, ecards)
    root.update()
    sleep(.5)

    turn = True

    cc = 0
    ce = 0

    cards, ecards = on_entry(cards, ecards, cc, ce)
    ecards, cards = on_entry(ecards, cards, ce, cc)

    while True:
        
        while cards[cc].hp <= 0 or ecards[ce].hp <= 0:

            if cards[cc].hp <= 0:
                ecards, cards = killed_enemy(ecards, cards, ce, cc)
                if cards[cc].hp <= 0:
                    cc += 1
                    if cc >= len(cards):loss(context);return
                    cards, ecards = on_entry(cards, ecards, cc, ce)
            
            else:
                cards, ecards = killed_enemy(cards, ecards, cc, ce)
                if ecards[ce].hp <= 0:
                    ce += 1
                    if ce >= len(ecards):victory(context);return
                    ecards, cards = on_entry(ecards, cards, ce, cc)
            
        updcard(cards, ecards, cc, ce)
        updmini(cards, ecards)
        root.update()

        sleep(1)

        if turn:
            for _ in range(10):
                sleep(.01)
                pos+=10
                plcard(pos)
                root.update()

            dmg = cards[cc].dmg
            dmg = before_attack(dmg, cards, ecards, cc, ce)
            ecards[ce].hp -= dmg
            cards, ecards = after_attack(dmg, cards, ecards, cc, ce)
            cards = fight_effects(cards, ecards, cc, ce)
            updcard(cards,ecards,cc,ce)
                
            for _ in range(10):
                sleep(.01)
                pos-=10
                plcard(pos)
                root.update()

        else:

            for _ in range(10):
                sleep(.01)
                epos-=10
                plecard(epos)
                root.update()

            dmg = ecards[ce].dmg
            dmg = before_attack(dmg, ecards, cards, ce, cc)
            cards[cc].hp -= dmg
            ecards, cards = after_attack(dmg, ecards, cards, ce, cc)
            ecards = fight_effects(ecards, cards, ce, cc)
            updcard(cards,ecards,cc,ce)
                
            for _ in range(10):
                sleep(.01)
                epos+=10
                plecard(epos)
                root.update()

        turn = not turn

        root.update()

##############################################
# TOWERS
##############################################

infinitefloor = get('infinitefloor', 0)

def start_infinite():
    global infinitefloor 
    infinitefloor = 1
    infinite_floor()

start_infinite_button = tk.Button(towers_frame, bg='#101010', text='Start infinite', fg='white', command=start_infinite)
start_infinite_button.place(x=150, width=100, y=200, height=25)


def inf_func(f=None):
    if f==None:return int(10**(1+.03*infinitefloor+.1))
    else:return int(10**(1+.03*f+.1))

def inf_coin(f=None):
    if f==None:return int(10**(1+.07*(infinitefloor-1))*.5)-5
    else:return int(10**(1+.07*f)*.5)-5

ininfinite = False
def infinite_floor():
    global ininfinite
    ininfinite = True

    pw = inf_func()

    c1 = BattleCard(cardlist[randint(0, len(cardlist)-1)], pw*2, pw)
    c2 = BattleCard(cardlist[randint(0, len(cardlist)-1)], pw*2, pw)
    c3 = BattleCard(cardlist[randint(0, len(cardlist)-1)], pw*2, pw)
    c4 = BattleCard(cardlist[randint(0, len(cardlist)-1)], pw*2, pw)

    cards = eqtobattlecard()

    fight(cards, [c1, c2, c3, c4], infinitefloor)


    

#if infinitefloor > 0:start_infinite()

#infinitefloor = 10
#infinite_floor()

##############################################
# BOSSFIGHTS
##############################################

bossareas = []

class BossReward:
    def __init__(self, card):
        self.card = card

class Bossarea:
    def __init__(self, name, cards):
        self.name = name
        self.cards = cards
        self.i = len(bossareas)

        self.frame = tk.Frame(bossfight_frame, width=200, height=115)
        self.frame.place(x=self.i%2*200, y=25+int(self.i/2)*115)
        self.img = load_image(image_folder+self.name+'.jpg', (200, 133))
        self.imglabel = tk.Label(self.frame, image=self.img)
        self.imglabel.place(x=0,y=0,width=200,height=133)

        self.easybutton = tk.Button(self.frame, bg='#101010', fg='white', text='easy')
        self.easybutton.place(x=0,y=100,width=50,height=15)
        self.mediumbutton = tk.Button(self.frame, bg='#101010', fg='white', text='medium')
        self.mediumbutton.place(x=50,y=100,width=50,height=15)
        self.hardbutton = tk.Button(self.frame, bg='#101010', fg='white', text='hard')
        self.hardbutton.place(x=100,y=100,width=50,height=15)
        self.insanebutton = tk.Button(self.frame, bg='#101010', fg='white', text='insane')
        self.insanebutton.place(x=150,y=100,width=50,height=15)

        self.easybutton.bind('<Button-1>', lambda x:fight(
            [BattleCard(card) for card in eqs],
            [BattleCard(cards[0])], 
            context=BossReward(cards[0])
            ))
        self.mediumbutton.bind('<Button-1>', lambda x:fight(
            [BattleCard(card) for card in eqs],
            [BattleCard(cards[0]),BattleCard(cards[1])], 
            context=BossReward(cards[1])
            ))
        self.hardbutton.bind('<Button-1>', lambda x:fight(
            [BattleCard(card) for card in eqs],
            [BattleCard(cards[0]),BattleCard(cards[1]),BattleCard(cards[2])], 
            context=BossReward(cards[2])
            ))
        self.insanebutton.bind('<Button-1>', lambda x:fight(
            [BattleCard(card) for card in eqs],
            [BattleCard(cards[0]),BattleCard(cards[1]),BattleCard(cards[2]),BattleCard(cards[3])], 
            context=BossReward(cards[3])
            ))

        bossareas.append(self)

vikings = Bossarea('Vikings', [brunhilde, berserker, thor, kraken])
colloseum = Bossarea('Colloseum', [spartan, alexander, achilles, hercules])
hell = Bossarea('Hell', [imp, demon, cerberus, hades])
council = Bossarea('Council', [fire_knight, water_knight, dark_knight, holy_knight])
apocalypse = Bossarea('Apocalypse', [famine, war, death, conquest])

##############################################
# ITEMS
##############################################

rlspdcl = '#6E55FF'

forge_bar = tk.Frame(forge_frame, bg='#101010', width=100, height=1000)
forge_bar.place(x=0,y=0)

forge_name = tk.Label(forge_frame, fg='#FFFFFF', bg='#101010', text="", font=('Helvetica', 20))
forge_name.place(x=200, y=15)

forge_luck = tk.Label(forge_frame, fg='#55FF55', bg='#101010')
forge_luck.place(x=200,y=100)
forge_rollspeed = tk.Label(forge_frame, fg=rlspdcl, bg='#101010')
forge_rollspeed.place(x=200,y=125)

forge_resources = tk.Label(forge_frame, fg='#FFFFFF', bg='#101010', anchor='nw')
forge_resources.place(x=200,y=225)

forge_button = tk.Button(forge_frame, fg='#FFFFFF', bg='#101010', text='Craft')
#forge_button.place(x=200,y=200, width=50, height=15)

def charms_page(i):
    forge_bar.place(x=0,y=-400*i)

class ForgePageButton:
    def __init__(self, i):
        self.i = i
        e = tk.Button(forge_frame, bg='#101010', fg='white', text=f'{i+1}', command=lambda: charms_page(self.i))
        e.place(x=450+25*i,y=0, width=25, height=25)
        root.update()

for i in range(4):
    e = ForgePageButton(i)

curforge = None
def forge_item(event):
    for card in curforge.resources:
        if card.owned < curforge.resources[card]:return

    for card in curforge.resources:
        card.owned -= curforge.resources[card]
    curforge.owned += 1
    data[f'{curforge.name}owned'] = curforge.owned

    select_item(curforge)
    save()

forge_button.bind('<Button-1>', forge_item)

def nametoitem(name):
    for item in itemlist:
        if item.name == name:return item

items = {}
itemlist = []
charms = 0

def select_item(self):
    global curforge
    curforge = self

    forge_name.config(text = self.name)
    forge_luck.config(text = f'+{self.luck} luck')
    forge_rollspeed.config(text = f'-{int((1-self.rollspeed)*100+.1)}% roll speed')
    forge_resources.config(text = '\n'.join([
            f'{card.name}: {card.owned} / {self.resources[card]}' for card in self.resources
        ]))
    forge_button.config(fg='#999999')
    forge_button.place(x=200,y=200, width=50, height=15)
    for card in self.resources:
        if card.owned < self.resources[card]:return
    forge_button.config(fg='#FFFFFF')

class Item:
    def __init__(self, name, luck=0, rollspeed=1, lm=1, itemtype='None', resources = {}, desc=[]):
        global charms
        self.desc = desc
        self.name = name
        self.luck = luck
        self.rollspeed = rollspeed
        self.lm = lm
        self.itemtype = itemtype
        self.owned = get(self.name+'owned', 0)
        self.resources = resources
        self.img = load_image(image_folder+name+'.jpg', (50,50))
        self.limg = load_image(image_folder+name+'.jpg', (100,100))

        if itemtype == 'Charm':
            itemimg = tk.Button(forge_bar, image=self.img)
            itemimg.place(x=25, y=25+charms*100)

            itemimg.bind('<Button-1>', lambda x: select_item(self))

            charms += 1


        itemlist.append(self)

clover = Item('Clover', 1, .9, 1, 'Charm', {wolf: 5, bear: 2, falcon: 1}, [['#55FF55', '+1 luck'], [rlspdcl, '-10% roll speed']])
excalibur = Item('Excalibur', 3, .8, 1, 'Charm', {knight: 2, samurai: 3}, [['#55FF55', '+3 luck'], [rlspdcl, '-20% roll speed']])
waraxe = Item('Waraxe', 5, .7, 1, 'Charm', {brunhilde: 3, berserker: 1}, [['#55FF55', '+5 luck'], [rlspdcl, '-30% roll speed']])
tentacle = Item('Tentacle', 15, .55, 1, 'Charm', {thor: 5, kraken: 1}, [['#55FF55', '+15 luck'], [rlspdcl, '-45% roll speed']])
helmofhades = Item('Helmofhades', 35, .45, 1, 'Charm', {cerberus: 3, hades: 1}, [['#55FF55', '+35 luck'], [rlspdcl, '-55% roll speed']])
conquestcrown = Item('Conquestcrown', 75, .3, 1, 'Charm', {conquest: 1, death: 2, war: 4}, desc=[['#55FF55', '+75 luck'], [rlspdcl, '-65% roll speed']])

gem = Item('Gem', 3, 1, 1.02, 'Gear', desc=[['#55FF55', '+3 luck'], ['#FFFF55', '+2% luck']])
crown = Item('Crown', 10, 1, 1.05, 'Gear', desc=[['#55FF55', '+10 luck'], ['#FFFF55', '+5% luck']])
dagger = Item('Dagger', 25, 1, 1.1, 'Gear', desc=[['#55FF55', '+25 luck'], ['#FFFF55', '+10% luck']])

pack500 = Item('500Pack', 0, 500, 1, 'Pack', desc=[['#FFFFFF', '500 rolls']])
pack2500 = Item('2500Pack', 0, 2_500, 1, 'Pack', desc=[['#FFFFFF', '2.5K rolls']])
pack10k= Item('10KPack', 0, 10_000, 1, 'Pack', desc=[['#FFFFFF', '10K rolls']])

if get('Charm', None) != None:items['Charm'] = nametoitem(get('Charm', None))
if get('Gear', None) != None:items['Gear'] = nametoitem(get('Gear', None))
#items['aiaia'] = waraxe
"""
items['e'] = conquestcrown
items['10e'] = conquestcrown
items['9e'] = conquestcrown
items['8e'] = conquestcrown
items['7e'] = conquestcrown
items['6e'] = conquestcrown
items['5e'] = conquestcrown
items['4e'] = conquestcrown
items['3e'] = conquestcrown
items['e2'] = conquestcrown"""
updequip()
"""
fight(
    [BattleCard(wolf, 400, 200),
    BattleCard(nurse, 400, 200),
    BattleCard(nurse, 400, 200),
    BattleCard(nurse, 400, 200),],
    [BattleCard(wolf, 400, 200),
    BattleCard(nurse, 400, 200),
    BattleCard(nurse, 400, 200),
    BattleCard(nurse, 400, 200),]
)"""

##############################################
# MARKET
##############################################

#seed(datetime.now().hour)
#market_index = randint(0, 1)

mjs = [hero, commander, assassin]
mgs = [gem, crown, dagger]
pks = [pack500, pack2500, pack10k]
market_index = (datetime.now().hour) % len(mjs)
cur_major = mjs[market_index]
cur_gear = mgs[market_index]
geartocoins = [10_000, 150_000, 5_000_000]
packtocoins = [2_500, 50_000, 2_000_000]
cur_pack = pks[market_index]

def refresh_market():
    global market_index, cur_major, cur_gear, cur_pack
    market_index = (datetime.now().hour) % len(mjs)
    cur_major = mjs[market_index]
    cur_gear = mgs[market_index]
    cur_pack = pks[market_index]
        
    major_img.config(image=cur_major.image)
    major_name_label.config(text=cur_major.name, bg='#101010', fg='white', font=('Helvetica', 15))
    major_rarity_label.config(text=shorten(cur_major.rarity), bg='#101010', fg='grey')

    major_hp_label.config(bg='#101010', fg='#55FF55', text=shorten(cur_major.base_health))
    major_dmg_label.config(bg='#101010', fg='#FF0000', text=shorten(cur_major.base_power))
    major_desc_label.config(bg='#101010', fg='#FFFFFF', text=cur_major.desc, wraplength=133)

    major_buy_button.config(bg='#101010', fg='#FFFF55', text=f'{shorten(cur_major.rarity/10)} coins', command=lambda:buy_market('Card'))

    gear_img.config(image=cur_gear.img)
    gear_name_label.config(text=cur_gear.name, bg='#101010', fg='white')
    gear_luck_label.config(text=f'+{cur_gear.luck} luck', bg='#101010', fg='#55FF55')
    gear_lm_label.config(text=f'+{int((cur_gear.lm-1)*100)}% luck')

    gear_buy_button.config(bg='#101010', fg='#FFFF55', text=f'{shorten(geartocoins[market_index])} coins', command=lambda:buy_market('Gear'))

    pack_img.config(image=cur_pack.img)
    pack_name_label.config(text=cur_pack.name, bg='#101010', fg='white')
    pack_luck_label.config(text=f'+{shorten(cur_pack.rollspeed)} rolls', bg='#101010', fg='#55FF55')

    pack_buy_button.config(bg='#101010', fg='#FFFF55', text=f'{shorten(packtocoins[market_index])} coins', command=lambda:buy_market('Pack'))

    #refreshlabel = tk.Label(market_frame, bg='red', fg='white', text='Refreshes every hour!')

#major_frame = tk.Frame(market_frame, bg='#101010', highlightcolor='#ffff55')
#major_frame.place(x=0,y=0, width=200, height=200)

def buy_market(item):
    global coins
    if item == 'Card' and coins >= int(cur_major.rarity/10):
        coins -= int(cur_major.rarity/10)
        cur_major.owned += 1
        cur_major.bought += 1
        data[f'{cur_major.name}Bought'] = cur_major.bought
        data[f'{cur_major.name}normal'] = cur_major.owned
        fix_rates()

    if item == 'Gear' and coins >= geartocoins[market_index]:
        coins -= geartocoins[market_index]
        cur_gear.owned += 1
        data[f'{cur_gear.name}owned'] = cur_gear.owned

    if item == 'Pack' and coins >= packtocoins[market_index]:
        coins -= packtocoins[market_index]

        cur_pack.owned += 1
        data[f'{cur_pack.name}owned'] = cur_pack.owned
        
    data['Coins'] = coins
    coinslabel.config(text=f'{shorten(coins)} coins')

major_img = tk.Label(market_frame, image=cur_major.image)
major_img.place(x=50,y=75, width=133, height=200)
major_name_label = tk.Label(market_frame, text=cur_major.name, bg='#101010', fg='white', font=('Helvetica', 15))
major_name_label.place(x=50, width=133, height=25, y=25)
major_rarity_label = tk.Label(market_frame, text=shorten(cur_major.rarity), bg='#101010', fg='grey')
major_rarity_label.place(x=50, width=133, y=50, height=25)

major_hp_label = tk.Label(market_frame, bg='#101010', fg='#55FF55', text=shorten(cur_major.base_health))
major_hp_label.place(x=116, width=67, y=275, height=25)
major_dmg_label = tk.Label(market_frame, bg='#101010', fg='#FF0000', text=shorten(cur_major.base_power))
major_dmg_label.place(x=50, width=67, y=275, height=25)
major_desc_label = tk.Label(market_frame, bg='#101010', fg='#FFFFFF', text=cur_major.desc, wraplength=133)
major_desc_label.place(x=50, width=133, y=300, height=50)

major_buy_button = tk.Button(market_frame, bg='#101010', fg='#FFFF55', text=f'{shorten(cur_major.rarity/10)} coins', command=lambda:buy_market('Card'))
major_buy_button.place(x=50, height=25, width=133, y=350)

gear_img = tk.Label(market_frame, image=cur_gear.img)
gear_img.place(x=275, y=75, width=50, height=50)
gear_name_label = tk.Label(market_frame, text=cur_gear.name, bg='#101010', fg='white')
gear_name_label.place(x=250, y=50, width=100, height=25)
gear_luck_label = tk.Label(market_frame, text=f'+{cur_gear.luck} luck', bg='#101010', fg='#55FF55')
gear_luck_label.place(x=250, y=125, width=100, height=25)
gear_lm_label = tk.Label(market_frame, text=f'+{(1-cur_gear.lm)*100}% luck', bg='#101010', fg='#FFFF55')
gear_lm_label.place(x=250, y=150, width=100, height=25)

gear_buy_button = tk.Button(market_frame, bg='#101010', fg='#FFFF55', text=f'{shorten(geartocoins[market_index])} coins', command=lambda:buy_market('Gear'))
gear_buy_button.place(x=250, height=15, width=100, y=175)

pack_img = tk.Label(market_frame, image=cur_pack.img)
pack_img.place(x=275, y=275, width=50, height=50)
pack_name_label = tk.Label(market_frame, text=cur_pack.name, bg='#101010', fg='white')
pack_name_label.place(x=250, y=250, width=100, height=25)
pack_luck_label = tk.Label(market_frame, text=f'+{shorten(cur_pack.rollspeed)} rolls', bg='#101010', fg='#55FF55')
pack_luck_label.place(x=250, y=325, width=100, height=25)

pack_buy_button = tk.Button(market_frame, bg='#101010', fg='#FFFF55', text=f'{shorten(packtocoins[market_index])} coins', command=lambda:buy_market('Pack'))
pack_buy_button.place(x=250, height=15, width=100, y=350)

refreshlabel = tk.Label(market_frame, bg='red', fg='white', text='Refreshes every hour!')
refreshlabel.place(x=0,y=0,height=15,width=350)

##############################################
# ACHIEVEMENTS
##############################################

##############################################
# MAINLOOP
##############################################

fix_rates()

if get('infinitefloor', 0) > 0:infinite_floor()

#mass_roll(1_000_000_000)

if False:
    fight(
        [
            BattleCard(fire_knight, 200, 100),
            BattleCard(water_knight,200, 100),
            BattleCard(dark_knight, 200, 100),
            BattleCard(holy_knight, 200, 100),
        ],
        [
            BattleCard(commander, 200, 100),
            BattleCard(brunhilde,200, 100),
            BattleCard(hercules, 200, 100),
            BattleCard(nurse, 200, 100),
        ],
    )


running = True
while running:

    rollcd -= 1
    if rollcd==0:rolledcardframe.place(x=-10000,y=0);rolledcardraritylabel.place(x=-999999)
    if autoroll:roll_medium()

    root.update()
    sleep(.03)