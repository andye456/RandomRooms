import random

###
# serverutils - these functions are called by methods that run on the python web server - mazeserver.
###
def adjust_hit_points(const):
    if const < 6:
        return -1
    if 5 < const < 10:
        return 0
    if const > 9:
        return 1

def adjust_dmg(strength):
    if strength < 6:
        return -1
    if 5 < strength < 10:
        return 1
    if strength > 9:
        return 1
'''
 This function deals with the attack command.
 1) The characters hit points are adjusted according to their constitution
 2) Each contestant takes it in turn to throw a blow 
 3) The probability of landing the blow is calculated based on the players dexterity - if the dexterity is 8 then there
    is a 1:8 chance of missing.
 4) if the blow is successful then teh damage is done according to whether the opponent is a small or large character
 5) if the opponents hit points reach zero then they are dead and removed from the matrix and they drop all the 
    items they were carrying, you can then gather them up.
'''
def attack(room_coords, char_ref, item_ref):
    turns = 2
    turn = 0
    your_turn = True
    txt = ""

    while turn < turns:
        player1 = None
        player2 = None
        if your_turn:
            # get a reference to your character object - this reference will update the object as well.
            player1 = char_ref[(0, 0)]
            # Get a reference to the monster character object
            player2 = char_ref[room_coords]
        else:
            # Get a reference to the monster character object
            player1 = char_ref[room_coords]
            # get a reference to your character object
            player2 = char_ref[(0, 0)]

        # Get the chance of an attack being successful
        # by selecting a random value in range 0..dexterity
        player1_attack_success = random.randint(1, player1.abilities['dexterity'])
        # player 1 attacks player 2 if the swing is successful
        # if the players dexterity is not the rand selected val then success
        # this means that the higher the dexterity then the less chance it has of being chosen at random therefore
        # less chance of missing.
        if player1.abilities['dexterity'] != player1_attack_success:
            # Get the damage figures from their current weapons player2_dmg is the damage player 2 receives
            # Large character
            if player2.race in ['Elf', 'Half_Elf', 'Half_Orc', 'Human']:
                player2_dmg = random.randint(player1.weapon['min_damage_large_opponent'],
                                             player1.weapon['max_damage_large_opponent'])
            # small character
            elif player2.race in ['Dwarf', 'Gnome', 'Halfling']:
                player2_dmg = random.randint(player1.weapon['min_damage_small_opponent'],
                                             player1.weapon['max_damage_small_opponent'])
            else:  # shouldn't get here
                player2_dmg = random.randint(player1.weapon['min_damage_small_opponent'],
                                             player1.weapon['max_damage_small_opponent'])

            print("p1 hit points a = ", end='')
            print(player1.hit_points)
            print("p2 hit points a = ", end='')
            print(player2.hit_points)
            # adjust the hit points according to your constitution
            print("_+_+_+_+_+_+_")
            print("p1 hit points b = ", end='')
            print(player1.hit_points)
            print("p2 hit points b = ", end='')
            print(player2.hit_points)


            # Adjust the damage according to the strength of the character
            player2_total_dmg = player2_dmg + adjust_dmg(player1.abilities['strength'])

            if your_turn:
                txt += "You land your hit for " + str(player2_total_dmg) + " hit-points<br>"
            else:
                txt += "They land their hit for "+str(player2_total_dmg)+" hit-points<br>"

            player2.hit_points -= player2_total_dmg
            if player2.hit_points < 1:
                char_data = '{"char_data":"' + txt + player1.name + ' wins"}'
                if player2.name == char_ref[(0, 0)].name:
                    char_ref.pop((0, 0))
                elif player2.name == char_ref[room_coords].name:
                    char_ref[(0, 0)].experience += 1
                    # Change the ownership of any items to room so they can be picked up
                    for d in item_ref[room_coords]:
                        d.owner = "room"
                    char_ref.pop(room_coords)
                    return char_data
            else:
                if your_turn:
                    txt += 'hit-points remaining.... You: ' + str(player1.hit_points) + ' Them: ' + str(player2.hit_points) + '<br>'
                    char_ref[(0, 0)].hit_points = player1.hit_points
                else:
                    txt += 'hit-points remaining.... You: ' + str(player2.hit_points) + ' Them: ' + str(player1.hit_points) + '<br>'
                    char_ref[room_coords].hit_points = player1.hit_points
                char_data = '{"char_data":"' + txt + '"}'


        else:
            if your_turn:
                txt += "You swing but miss!<br/>"
            else:
                txt += "They swing but miss!<br/>"
            char_data = '{"char_data":"' + txt + '"}'

        turn += 1
        your_turn = not your_turn
    return char_data
