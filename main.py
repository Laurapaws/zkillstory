import json
import logging
import requests
import openai

# Set up logging
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('debug.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
root_logger.addHandler(handler)

openai.api_key = 'OPEN_AI_KEY'
KILL_URL = 'https://zkillboard.com/kill/106361130/'

class Story:
    def __init__(self, 
                 zkill_link=None, 
                 killmail_id=None, 
                 kill_hash=None, 
                 zkill_data=None, 
                 esi_data=None, 
                 topic="An EVE Online Story", 
                 attackers=None, 
                 attacking_corp=None, 
                 top_damage=None, 
                 final_blow=None, 
                 victims=None, 
                 victim_corp=None, 
                 response=None
                 ):
        self.zkill_link = zkill_link
        self.killmail_id = killmail_id
        self.kill_hash = kill_hash
        self.zkill_data = zkill_data
        self.esi_data = esi_data
        self.topic = topic
        self.attackers = attackers
        self.attacking_corp = attacking_corp
        self.top_damage = top_damage
        self.final_blow = final_blow
        self.victims = victims
        self.victim_corp = victim_corp
        self.response = response
               
class Character:
    def __init__(self, character_id=None, name="Missing Name", corp_id=None, corp="Missing Corp", ship_id=None, ship="Missing Ship"):
        self.id = character_id
        self.name = name
        self.corp_id = corp_id
        self.corp = corp
        self.ship_id = ship_id
        self.ship = ship

def get_zkill_data(zkill_link: str):
    """Get zkill data from zkill link

    Args:
        zkill_link (str): _description_

    Returns:
        str: killmail_id
        dict: JSON data from zkill
    """
    logging.debug("Getting zkill data for " + zkill_link + " from zkill")
    killmail_id = zkill_link.split('/')[-2]
    zkill_response = requests.get('https://zkillboard.com/api/killID/' + killmail_id + '/')
    zkill_data = json.loads(zkill_response.text)
    
    return killmail_id, zkill_data
    
def get_esi_data(kill_hash: str, killmail_id: str):
    """Get ESI data from zkill hash and killmail id

    Args:
        hash (str): zkill hash
        killmail_id (str): killmail id

    Returns:
        dict: JSON data from ESI
    """
    logging.debug("Getting ESI data for " + killmail_id + " from ESI")
    esi_response = requests.get('https://esi.evetech.net/latest/killmails/' + killmail_id + '/' + kill_hash + '/?datasource=tranquility')
    esi_data = json.loads(esi_response.text)
    
    return esi_data

def populate_character(character: Character):
    """Queries ESI for info on a character and their ship from the character, universe, and corporations endpoints

    Args:
        character (Character): Must contain the ID values for character, corp, and ship

    Returns:
        _type_: A Character object with the name, corp, and ship populated
    """
    logging.debug("Getting character info for " + str(character.id) + " from ESI")
    
    character_name_response = requests.get('https://esi.evetech.net/latest/characters/' + str(character.id) + '/?datasource=tranquility')
    character.name = json.loads(character_name_response.text)['name']
    
    try:
        character_ship_response = requests.get('https://esi.evetech.net/latest/universe/types/' + str(character.ship_id) + '/?datasource=tranquility&language=en')
        character.ship = json.loads(character_ship_response.text)['name']
    except:
        character.ship = "Unknown Ship"
    
    character_corp_response = requests.get('https://esi.evetech.net/latest/corporations/' + str(character.corp_id) + '/?datasource=tranquility')
    character.corp = json.loads(character_corp_response.text)['name']
    
    return character

def get_attackers(esi_data: dict):
    """Get attackers from ESI data

    Args:
        esi_data (dict): ESI data

    Returns:
        list: List of attacker objects
    """
    logging.debug("Getting attackers")
    attackers = []
    for attacker in esi_data['attackers']:
        try:
            character = Character(character_id=attacker['character_id'], corp_id=attacker['corporation_id'], ship_id=attacker['ship_type_id'])
        except:
            character = Character(character_id=attacker['character_id'], corp_id=attacker['corporation_id'], ship_id=670)
        character = populate_character(character)
        attackers.append(character)
    logging.debug("Got attackers")
    
    return attackers

def get_victim(esi_data: dict):
    
    victim = Character(character_id=esi_data['victim']['character_id'], corp_id=esi_data['victim']['corporation_id'], ship_id=esi_data['victim']['ship_type_id'])
    populate_character(victim)
    return victim

def create_attacker_string(attackers: list):
    """Create a string of attackers from a list of attacker objects

    Args:
        attackers (list): List of attacker objects

    Returns:
        str: String of attackers
    """
    logging.debug("Creating attacker string")
    attacker_string = ""
    for attacker in attackers:
        attacker_string += attacker.name + " in a " + attacker.ship + ", "
    attacker_string = attacker_string[:-2]
    return attacker_string

def create_victim_string(victim: Character):
    """Create a string of victim from a victim object

    Args:
        victim (Character): Victim object

    Returns:
        str: String of victim
    """
    logging.debug("Creating victim string")
    victim_string = victim.name + " in a " + victim.ship
    return victim_string

def find_damage_and_final_blow(esi_data: dict):
    
    logging.debug("Finding top damage and final blow")
    
    damage_list = []
    
    for attacker in esi_data['attackers']:
        damage_list.append(attacker['damage_done'])
    
        if attacker['final_blow'] == True:
            final_blow = json.loads(requests.get('https://esi.evetech.net/latest/characters/' + str(attacker['character_id']) + '/?datasource=tranquility').text)['name']
            
    top_damage = max(damage_list)
    top_damage_position = damage_list.index(top_damage)    
    top_damage = json.loads(requests.get('https://esi.evetech.net/latest/characters/' + str(esi_data['attackers'][top_damage_position]['character_id']) + '/?datasource=tranquility').text)['name']
    
    return top_damage, final_blow

def get_story(zkillstory, tokens=300):
    ai_prompt = '''Topic: {story_topic}
    Attackers: {story_attackers}
    Attacking Corporation: {story_attacking_corp}
    Top Damage: {story_top_damage}
    Final Blow: {story_final_blow}
    Victim: {story_victims}
    Victim Corporation: {story_victim_corp}

    Story:'''

    ai_prompt = ai_prompt.format(
        story_topic="EVE Online story",
        story_attackers=zkillstory.attackers,
        story_attacking_corp=zkillstory.attacking_corp,
        story_top_damage=zkillstory.top_damage,
        story_final_blow=zkillstory.final_blow,
        story_victims=zkillstory.victims,
        story_victim_corp=zkillstory.victim_corp,
    )
    
    logging.info("AI prompt: " + ai_prompt)

    openresponse = openai.Completion.create(
    model="text-davinci-003",
    prompt=ai_prompt,
    temperature=0.95,
    max_tokens=tokens,
    top_p=1.0,
    frequency_penalty=0.5,
    presence_penalty=0.0
    )
    
    return openresponse["choices"][0]["text"]


zkillstory = Story(zkill_link=KILL_URL)

zkillstory.killmail_id, zkillstory.zkill_data = get_zkill_data(zkillstory.zkill_link)
zkillstory.kill_hash = zkillstory.zkill_data[0]['zkb']['hash']
zkillstory.esi_data = get_esi_data(zkillstory.kill_hash, zkillstory.killmail_id)

attacker_list = get_attackers(zkillstory.esi_data)
victim = get_victim(zkillstory.esi_data)

zkillstory.attackers = create_attacker_string(attacker_list)
zkillstory.attacking_corp = attacker_list[0].corp
zkillstory.victims = create_victim_string(victim)
zkillstory.victim_corp = victim.corp

zkillstory.top_damage, zkillstory.final_blow = find_damage_and_final_blow(zkillstory.esi_data)

story = get_story(zkillstory, tokens=300)
print(story)
logging.info("Story: " + story)

print("And that was just another day in New Eden")



# TODO Add in extra consolidation of code into functions
# TODO Add an extra topic if you want to customise the story
# TODO Create a Discord bot to post the story to a channel
# TODO Add error handling
# TODO Add handling for when there are hundreds of attackers?
# TODO Add support for a battle report