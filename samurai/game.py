import copy

PERSON_TYPE_1=1
PERSON_TYPE_2=2
PERSON_TYPE_3=3

HOUSE_TYPE_1=1
HOUSE_TYPE_2=2
HOUSE_TYPE_3=3
HOUSE_TYPE_4=4

class NoMoreRaiderCardsException(Exception):
    pass

class PlayerDiedException(Exception):
    pass

class NoMoreBarricadesException(Exception):
    pass

class NoMoreHousesException(Exception):
    pass

class GameWonException(Exception):
    pass 

class GameLostException(Exception):
    pass 

class NoMorePersonsException(Exception):
    pass

class Village(object):

    def __init__(self, max_num_fences):
        self.max_num_fences = max_num_fences
        self.num_fences = max_num_fences
        self.persons = [PERSON_TYPE_1, PERSON_TYPE_2, PERSON_TYPE_3]
        self.removed_persons = []
        self.farms = [HOUSE_TYPE_1, HOUSE_TYPE_1, HOUSE_TYPE_2, HOUSE_TYPE_2, HOUSE_TYPE_3, HOUSE_TYPE_4]
        self.removed_farms = []

    def __deepcopy__(self, memodict={}):
        cls = self.__class__
        village_copy = cls.__new__(cls)
        village_copy.max_num_fences = self.max_num_fences
        village_copy.num_fences = self.num_fences
        village_copy.persons = copy.deepcopy(self.persons)
        village_copy.removed_persons = copy.deepcopy(self.removed_persons)
        village_copy.farms = copy.deepcopy(self.farms)
        village_copy.removed_farms = copy.deepcopy(self.removed_farms)
        return village_copy

    def remove_barricade(self):
        print("Removing barricade from village") 
        if self.num_fences == 0:
            print("  there are no more barricades")
            raise NoMoreBarricadesException()
        else:
            self.num_fences -= 1

    def remove_farm(self):
        
        print("Removing farm from village") 
        if len(self.farms) == 0:
            print("  there are no more farmsteads")
            raise NoMoreHousesException()
        else:
            farm = self.farms.pop()
            self.removed_farms.append(farm)
        
    def remove_person(self):
        
        print("Removing person from village") 
        if len(self.persons) == 0:
            print("  there are no more persons")
            raise NoMorePersonsException()
        else:
            person = self.persons.pop()
            self.removed_persons.append(person)

    def __str__(self):
        return "Village: fences={} farmsteads = {} persons = {}".format(self.num_fences, self.farms, self.persons)


HAT="hat"
FARM="farmstead"
PERSON="person"

PENALTY_BARRICADE="barricade"
PENALTY_WOUND="wound"
PENALTY_INTRUDER="intruder"
PENALTY_NO_DEFENSE="no defense"
PENALTY_NO_SUPPORT="no support"
PENALTY_LEFT_DRAW="left draw"
PENALTY_RIGHT_DRAW="right draw"

class Intruder(object):

    def __init__(self, level, has_fire, benefit, penalty):
        self.level = level
        self.benefit = benefit
        self.penalty = penalty
        self.has_fire = has_fire

    def __str__(self):
        return "Card L{} Benefit:{} Penalty:{} Fire:{}".format(self.level, self.benefit, self.penalty, self.has_fire)

    def __deepcopy__(self, memodict={}):
        cls = self.__class__
        intruder_copy = cls.__new__(cls)
        intruder_copy.level = self.level
        intruder_copy.benefit = self.benefit
        intruder_copy.penalty = self.penalty
        intruder_copy.has_fire = self.has_fire
        return intruder_copy


def get_raider_stack(round):
    return_list = []
    return_list.append(Intruder(1, False, HAT, PENALTY_INTRUDER))
    return_list.append(Intruder(2, False, FARM, PENALTY_INTRUDER))
    return_list.append(Intruder(2, False, PERSON, None))
    return_list.append(Intruder(3, True, FARM, PENALTY_BARRICADE))
    return_list.append(Intruder(2, False, FARM, PENALTY_WOUND))
    return_list.append(Intruder(1, False, PERSON, None))
    return_list.append(Intruder(4, True, FARM, PENALTY_BARRICADE))
    return_list.append(Intruder(4, False, PERSON, None))
    return_list.append(Intruder(1, True, FARM, PENALTY_WOUND))
    return_list.append(Intruder(1, True, FARM, PENALTY_WOUND))
    return_list.append(Intruder(4, False, None, PENALTY_WOUND))
    return_list.append(Intruder(1, True, HAT, PENALTY_WOUND))
    return_list.append(Intruder(4, False, PERSON, PENALTY_RIGHT_DRAW))
    return_list.append(Intruder(4, False, FARM, PENALTY_RIGHT_DRAW))
    return return_list

class Game(object):
    
    def __init__(self, players):
    
        self.village = Village(max_num_fences = len(players) + 2)
        self.players = players
        self.current_player_index = 0
        self.raider_stack = None
        self.intruder_stack = []
        self.discard_pile = []
        self.round = 1

    def __deepcopy__(self, memodict={}):
        cls = self.__class__
        game_copy = cls.__new__(cls)
        game_copy.village = copy.deepcopy(self.village)
        game_copy.players = copy.deepcopy(self.players)
        game_copy.current_player_index = copy.deepcopy(self.current_player_index)
        game_copy.raider_stack = copy.deepcopy(self.raider_stack)
        game_copy.intruder_stack = copy.deepcopy(self.intruder_stack)
        game_copy.discard_pile = copy.deepcopy(self.discard_pile)
        game_copy.round = copy.deepcopy(self.round)
        return game_copy

    def get_player_by_name(self, player_name):
        for player in self.players:
            if player.name == player_name:
                return player

    def draw_card(self):
        
        if self.raider_stack:
            return self.raider_stack.pop()
        else:
            raise NoMoreRaiderCardsException()

    def move_raider_to_intruder_stack(self):
        
        if self.raider_stack:
            self.intruder_stack.append(self.raider_stack.pop())
        else:
            raise NoMoreRaiderCardsException()


    def start_game(self):
        try:
            self.start_round()
        except GameLostException:
            print("Game Lost!")

    def start_round(self):
        
        print("Starting round {}".format(self.round))
        for player in self.players:
            player.reset_for_new_round()

        self.raider_stack = get_raider_stack(round=self.round)
        self.intruder_stack = []
        self.discard_pile = []
        while True:
            
            all_passed = True
            for player in self.players:
                if not player.passed:
                    all_passed = False
                    break

            if all_passed:
                print("All players passed - ending round")
                self.end_round()
                return

            if not self.raider_stack:
                print("Raider stack is empty - ending round")
                self.end_round()
                return

            player = self.players[self.current_player_index]
            self.current_player_index += 1
            if self.current_player_index >= len(self.players):
                self.current_player_index = 0
            player.take_turn(game=self)

    def end_round(self):
        print("Processing end of round {}".format(self.round))

        print("Moving {} raideres to intruder stack".format(len(self.raider_stack))) 
        while len(self.raider_stack):
            c = self.raider_stack.pop()
            self.intruder_stack.append(c)

        for player in self.players:
            if not player.has_hat():
                print("Player {} has no hat and takes damage".format(player.name))
                player.take_damage()
                
        for player in self.players:
            if not player.has_farm():
                print("Player {} has no farm - removing farm from village".format(player.name))
                self.village.remove_farm()
                
        for player in self.players:
            if not player.has_person():
                print("Player {} has no person - removing person from village".format(player.name))
                try:
                    self.village.remove_person()
                except NoMorePersonsException:
                    raise GameLostException()
            
        # Reward for persons that are still there
        #


        # Fire from Intruders
        #        
        print("Processing Intruders")
        for i in self.intruder_stack:
            if not i.has_fire:
                continue
            try:
                game.village.remove_barricade()
            except NoMoreBarricadesException:
                game.village.remove_farm()

        print("End of round village: {}".format(self.village))
        if self.village.persons and self.village.farms:
            print("Round survived!")

            if self.round == 3:
                raise GameWonException()

            self.round = self.round + 1
            self.start_round()

        else:
            raise GameLostException()
    

ABILITY_IGNORE_246=1
ABILITY_PASS_246=2


ACTION_PASS=1
ACTION_SUPPORT=2
ACTION_FIGHT=3


class Player(object):
    
    def __init__(self, name, ability, max_human_health, max_animal_health):
        self.name = name
        self.ability = ability
        self.max_human_health = max_human_health
        self.max_animal_health = max_animal_health
        self.passed = False
        self.defense_intruders = []
        self.attack_intruders = []
        self.damaged = False
        self.animal_activated = False

    def __deepcopy__(self, memodict={}):
        cls = self.__class__
        player_copy = cls.__new__(cls)
        player_copy.name = self.name
        player_copy.ability = self.ability
        player_copy.max_human_health = self.max_human_health
        player_copy.max_animal_health = self.max_animal_health
        player_copy.passed = self.passed
        player_copy.defense_intruders = copy.deepcopy(self.defense_intruders)
        player_copy.attack_intruders = copy.deepcopy(self.attack_intruders)
        player_copy.damaged = self.damaged
        player_copy.animal_activated = self.animal_activated
        return player_copy

    def __str__(self):
        attack_amount = self.get_attack_amount()
        max_health = self.get_health()
        benefits = []
        if self.has_hat():
            benefits.append(HAT)
        if self.has_farm():
            benefits.append(FARM)
        if self.has_person():
            benefits.append(PERSON)

        return "{} {}/{} {} Penalty: {}".format(self.name, attack_amount, max_health, benefits, self.get_current_penalty())

    def has_hat(self):
        for card in self.defense_intruders:
            if card.benefit == HAT:
                return True

    def has_farm(self):
        for card in self.defense_intruders:
            if card.benefit == FARM:
                return True

    def has_person(self):
        for card in self.defense_intruders:
            if card.benefit == PERSON:
                return True

    def reset_for_new_round(self):
        self.passed = False
        self.defense_intruders = []
        self.attack_intruders = []

    def get_current_penalty(self):
        if len(self.attack_intruders):
            last_intruder = self.attack_intruders[-1]
            return last_intruder.penalty
        
        return None 

    def take_penalty(self, game):
        if self.passed:
            return

        penalty = self.get_current_penalty()
        if penalty == PENALTY_BARRICADE:
            try:
                game.village.remove_barricade()
            except NoMoreBarricadesException:
                try:
                    game.village.remove_farm()
                except NoMoreHousesException:
                    self.take_damge()

        elif penalty == PENALTY_WOUND:
            self.take_damage()

        elif penalty == PENALTY_INTRUDER:
            try:
                game.move_raider_to_intruder_stack()
            except NoMoreRaiderCardsException:
               game.end_round()
             

    def take_damage(self):
        if self.damaged:
            if self.animal_activated:
                raise PlayerDiedException()
            else:
                self.damaged = False
                self.animal_activated = True
        else:
            self.damaged = True

    def get_attack_amount(self):
        return_amount = 0
        for attacker in self.attack_intruders:
            return_amount += attacker.level
        return return_amount

    def get_health(self):
        if self.animal_activated:   
            return self.max_animal_health
        else:
            return self.max_human_health
        
    def overwhelmed_by_amount(self, amount):
        """
            return true if the amount would overrwhlem the player 
        """
        if self.animal_activated:
            if amount > self.get_health():
                return True
            else:
                return False

    def _get_actions(self):
        
        return_list = [ACTION_FIGHT, ACTION_SUPPORT]
        if not self.overwhelmed_by_amount(self.get_attack_amount()):
            return_list.append(ACTION_PASS)
        return return_list

    def add_card_to_left(self, card):
        self.defense_intruders.append(card)

    def add_card_to_right(self, card):
        self.attack_intruders.append(card)

    def can_defend_card(self, card):
        if card.benefit == HAT and not self.has_hat():
            return True

        if card.benefit == PERSON and not self.has_person():
            return True

        if card.benefit == FARM and not self.has_farm():
            return True

    def fight(self, game):
        card = game.draw_card()
        print("Player {} drew card {}".format(self, card))
        # DECISION POINT
        
        if self.can_defend_card(card):
            print("  player added card to defense")
            self.add_card_to_left(card)
        else:
            print("  player added card to attack line")
            self.add_card_to_right(card) 

    def take_turn(self, game):
        if self.passed:
            return

        try:
            self.take_penalty(game=game)
        except PlayerDiedException:
            raise GameLostException()
        # First, we're going to have everyone pass

        actions = self._get_actions()
            
        for action in actions:
            gc = copy.deepcopy(game)
            copy_player = gc.get_player_by_name(self.name)
            if action == ACTION_FIGHT:
                try:
                    print("Fight!")
                except GameLostException:
                    print( "Lost!")
                    raise

        if ACTION_FIGHT in actions:
            print("Plauer {} is fighting".format(self.name))
            self.fight(game)
        else:
            print("Plauer {} is passing".format(self.name))
            self.passed = True



player_1 = Player(name="buck", ability=ABILITY_PASS_246, max_human_health=9, max_animal_health=11)
player_2 = Player(name="al", ability=ABILITY_IGNORE_246, max_human_health=9, max_animal_health=11)
print(player_1)
print(player_2)

game = Game(players = [player_1, player_2])
print(game.village)
game.start_game()

v1 = Village(max_num_fences=5)
v2 = copy.deepcopy(v1)
v1.remove_farm()
v1.remove_barricade()
v3 = copy.deepcopy(v1)

print(v1)
print(v2)
print(v2)
