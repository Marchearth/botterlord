"""File for setting up adventures and information in nodes."""
import sqlite3, os, yaml, tools, ymlr

default_hp = 100
default_mp = 100
default_loc = "10:40"

def add_ncolumn(tab_name, col_name, col_type, df_val): # Items, exits columns are also needed.
    """Add a new column with default value."""
    conn = sqlite3.connect(os.path.join('data','botterlord.db'))
    db = conn.cursor()
    try:
        db.execute(" ALTER TABLE {tn} \
            ADD COLUMN '{cn}' {ct} DEFAULT '{df}'"\
            .format(tn=tab_name, cn=col_name, ct=col_type, df=df_val))
    except:
        print 'world: Column already exists.'
        pass
    conn.commit()
    conn.close()

def chcknode(_addr, _rtrn):
    """Check adventure and npc columns."""
    str_node = get_node(_addr)

    if _rtrn == 'NPC':
        rtrn = str_node[2]
    if _rtrn == 'ADVE':
        rtrn = str_node[3]
    return rtrn

def get_node(_addr_):
    """Fetch a node from the database file."""
    conn = sqlite3.connect(os.path.join('data','botterlord.db'))
    db = conn.cursor()
    _addrdb_ = (_addr_,)
    db.execute('SELECT * FROM NODES WHERE ADDR = ?', _addrdb_)
    return db.fetchone()
    conn.commit()
    conn.close()

def chck_bot_exist(np_row, np_col, world_file): # No errors
    """Check if there is a bot in given coordinates stored inside the world file."""
    with open(world_file, 'r') as stream:
        profile = yaml.load(stream)
        for bot_key in profile:
            if 'location' in profile[bot_key]:
                print 'loc in bot_key = True', profile[bot_key]
                addr = tools.parse_str_loc(profile[bot_key]['location'])
                chkd_row = int(addr[0]); chkd_col = int(addr[1])
                if np_row == chkd_row and np_col == chkd_col:
                    return True
                else:
                    return False


def show_bots(filesname): #WHY
    """Returns a list with all the bot locations in it."""
    stream__ = open(filesname, 'r')
    prof__ = yaml.load(stream__)
    bot_adrs = [] # It's a list
    for keyval in prof__: # Go through dictionaries in yaml file.
        if keyval.startswith('bot_') == False: # If it doesn't start with bot_
            continue # Go back and check another one.
        else:
            bot_adrs.append(prof__[keyval]['location'])
    return bot_adrs

def store_bot_location(filename): # WHYYYYYYY
    stream = open(filename, 'r')
    prof = yaml.load(stream) # Player information is stored here.
    bot_locations = []
    for botkey in prof:
        if botkey.startswith('bot_') == False:
            continue
        else:
            bot_locations.append(prof[botkey]['location'])
    ymlr.enter_data('locations', bot_locations, filename)
    return bot_locations

def create_bot(worldfile, namebot, hp = default_hp, mp = default_mp, loc = default_loc):
    """Check if bot with the same name exists."""
    stream = open(worldfile, 'r')
    prof = yaml.load(stream)
    torf = "bot_" + namebot in prof
    if torf == False:
        prof["bot_" + namebot] = {'energy': mp, 'health': hp, 'location': loc}
        with open(worldfile, 'w') as yaml_file:
            yaml_file.write(yaml.dump(prof, default_flow_style = False))

    else: return "exists"

    """Record bot in yaml file."""

create_bot(worldfile = "worlds/profile.yml", namebot = "testerrbot")
