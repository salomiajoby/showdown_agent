from poke_env.battle import AbstractBattle
from poke_env.player import Player

"""
Define your team here. You can use the team builder on https://play.pokemonshowdown.com/teambuilder 

Create a team and then copy the text here. 

Make sure to keep the triple quotes around the team text.

Make sure to use the Uber Format
"""

team = """
Necrozma-Dusk-Mane @ Leftovers
Ability: Prism Armor
Tera Type: Steel
EVs: 252 HP / 252 Atk / 4 SpD
Adamant Nature
- Dragon Dance
- Sunsteel Strike
- Earthquake
- Morning Sun

Arceus-Fairy @ Pixie Plate
Ability: Multitype
Tera Type: Fairy
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Calm Mind
- Judgment
- Recover
- Ice Beam

Ting-Lu @ Leftovers
Ability: Vessel of Ruin
Tera Type: Water
EVs: 252 HP / 252 Def / 4 SpD
Impish Nature
- Spikes
- Whirlwind
- Earthquake
- Ruination

Ho-Oh @ Leftovers
Ability: Regenerator
Tera Type: Water
EVs: 248 HP / 8 Def / 252 SpD
Careful Nature
- Sacred Fire
- Brave Bird
- Recover
- Whirlwind

Zacian-Crowned @ Rusted Sword
Ability: Intrepid Sword
Tera Type: Fire
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Behemoth Blade
- Play Rough
- Close Combat
- Substitute

Kyogre @ Leftovers
Ability: Drizzle
Tera Type: Water
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Calm Mind
- Origin Pulse
- Ice Beam
- Thunder
"""


class CustomAgent(Player):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, team=team, **kwargs)

    def choose_move(self, battle: AbstractBattle):
        """
        DO NOT EDIT THIS FUNCTION.
        """
        me = battle.active_pokemon
        opp = battle.opponent_active_pokemon

        if me is None or opp is None:
            return self.choose_random_move(battle)

        return self._choose_move(battle)

    def _choose_move(self, battle: AbstractBattle):
        """
        DO EDIT THIS FUNCTION
        """
        me = battle.active_pokemon
        opp = battle.opponent_active_pokemon

        best_move = None
        best_score = -1

        for move in battle.available_moves:
            # Base score starts with the move's raw power
            score = move.base_power

            # Type effectiveness multiplier against the opponent's typing
            multiplier = move.type.damage_multiplier(
                opp.type_1,
                opp.type_2,
                type_chart=battle.opponent_active_pokemon._data.type_chart,
            )
            score *= multiplier

            # STAB bonus if the move's type matches one of our types
            if move.type in (me.type_1, me.type_2):
                score *= 1.5

            # Slight preference for reliable (higher accuracy) moves when scores are close
            score *= move.accuracy if move.accuracy else 1.0

            if score > best_score:
                best_score = score
                best_move = move

        if best_move is not None:
            return self.create_order(best_move)

        # No attacking move available (e.g. forced switch) — fall back to random
        return self.choose_random_move(battle)

    def teampreview(self, battle: AbstractBattle):
        """
        SET THE TEAM ORDER HERE
        """
        return "/team 1"
