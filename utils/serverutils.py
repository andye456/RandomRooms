import random

def adjust_hit_points(const):
    if const < 6:
        return -1
    if 5 < const < 10:
        return 1
    if const > 9:
        return 1


def adjust_dmg(strength):
    if strength < 6:
        return -1
    if 5 < strength < 10:
        return 1
    if strength > 9:
        return 1


def attack(room_coords, char_ref, item_ref):
    turns = 2
    turn = 0
    your_turn = True
    txt = ""
    while turn < turns:
        player1 = None
        player2 = None
        if your_turn:
            # get a reference to your character object
            player1 = char_ref[(0, 0)]
            # Get a reference to the monster character object
            player2 = char_ref[room_coords]
        else:
            # Get a reference to the monster character object
            player1 = char_ref[room_coords]
            # get a reference to your character object
            player2 = char_ref[(0, 0)]

        # Get the chance of an attack begin successful
        player1_attack_success = random.randint(1, player1.abilities['dexterity'])
        # player 1 attacks player 2 if the swing is successful
        if player1.abilities['dexterity'] != player1_attack_success:
            # Get the damage figures from their current weapons
            # Large character
            if player1.char_class in ['Elf', 'Half_Elf', 'Half_Orc', 'Human']:
                player2_dmg = random.randint(player1.weapon['min_damage_large_opponent'],
                                             player1.weapon['max_damage_large_opponent'])
            # small character
            elif player1.char_class in ['Dwarf', 'Gnome', 'Halfling']:
                player2_dmg = random.randint(player1.weapon['min_damage_small_opponent'],
                                             player1.weapon['max_damage_small_opponent'])
            else:  # shouldn't get here
                player2_dmg = random.randint(player1.weapon['min_damage_small_opponent'],
                                             player1.weapon['max_damage_small_opponent'])

            # Take the damage
            player2.hit_points = player2.hit_points + adjust_hit_points(player2.abilities['constitution'])

            # Adjust the damage according to the strength of the character
            player2_total_dmg = player2_dmg + adjust_dmg(player2.abilities['strength'])

            player2.hit_points -= player2_total_dmg
            if player2.hit_points < 1:
                char_data = '{"char_data":"' + player1.name + ' wins"}'
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
                    txt += 'You attack, hit-points remaining.... You: ' + str(
                        player1.hit_points) + ' Them: ' + str(player2.hit_points) + '<br>'
                    char_ref[(0, 0)].hit_points = player1.hit_points
                else:
                    txt += 'They Attack, hit-points remaining.... You: ' + str(
                        player2.hit_points) + ' Them: ' + str(player1.hit_points) + '<br>'
                    char_ref[room_coords].hit_points = player1.hit_points
                char_data = '{"char_data":"' + txt + '"}'


        else:
            txt = "You swing but miss!<br/>"
            char_data = '{"char_data":"' + txt + '"}'

        turn += 1
        your_turn = not your_turn
    return char_data
