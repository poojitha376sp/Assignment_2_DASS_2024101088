"""
This module serves as the main controller for the MoneyPoly game. It manages 
the game setup, player turn rotation, and the core game loop.
"""

from moneypoly.config import (
    JAIL_FINE,
    INCOME_TAX_AMOUNT,
    LUXURY_TAX_AMOUNT,
    GO_SALARY,
)
from moneypoly.player import Player
from moneypoly.board import Board
from moneypoly.bank import Bank
from moneypoly.dice import Dice
from moneypoly.cards import CardDeck, CHANCE_CARDS, COMMUNITY_CHEST_CARDS
from moneypoly import ui


class Game:
    """
    The main controller class for the MoneyPoly game engine.
    Coordinates players, the board, the bank, and the dice.
    """
    def __init__(self, player_names):
        self.resources = {
            "board": Board(),
            "bank": Bank()
        }
        self.dice = Dice()
        self.players = [Player(name) for name in player_names]
        self.turn_info = {
            "index": 0,
            "count": 0
        }
        self.running = True
        self.decks = {
            "chance": CardDeck(CHANCE_CARDS),
            "community": CardDeck(COMMUNITY_CHEST_CARDS)
        }

    def current_player(self):
        """Return the Player whose turn it currently is."""
        return self.players[self.turn_info["index"]]

    def advance_turn(self):
        """Move to the next player in the rotation."""
        self.turn_info["index"] = (self.turn_info["index"] + 1) % len(self.players)
        self.turn_info["count"] += 1

    def play_turn(self):
        """Execute one complete turn for the current player."""
        player = self.current_player()
        ui.print_banner(
            f"Turn {self.turn_info['count'] + 1}  |  {player.name}  |  ${player.balance}"
        )

        if player.jail_info["in_jail"]:
            self._handle_jail_turn(player)
            self.advance_turn()
            return

        roll = self.dice.roll()
        print(f"  {player.name} rolled: {self.dice.describe()}")

        # Three consecutive doubles sends a player to jail
        if self.dice.doubles_streak >= 3:
            print(f"  {player.name} rolled doubles three times in a row — go to jail!")
            player.go_to_jail()
            self.advance_turn()
            return

        self._move_and_resolve(player, roll)

        # Rolling doubles earns an extra turn
        if self.dice.is_doubles():
            print(f"  Doubles! {player.name} rolls again.")
            return

        self.advance_turn()

    def _move_and_resolve(self, player, steps):
        """Move `player` by `steps` and trigger whatever tile they land on."""
        player.move(steps)
        position = player.position
        tile = self.resources["board"].get_tile_type(position)
        print(f"  {player.name} moved to position {position}  [{tile}]")

        if tile == "go_to_jail":
            player.go_to_jail()
            print(f"  {player.name} has been sent to Jail!")

        elif tile == "income_tax":
            player.deduct_money(INCOME_TAX_AMOUNT)
            self.resources["bank"].collect(INCOME_TAX_AMOUNT)
            print(f"  {player.name} paid income tax: ${INCOME_TAX_AMOUNT}.")

        elif tile == "luxury_tax":
            player.deduct_money(LUXURY_TAX_AMOUNT)
            self.resources["bank"].collect(LUXURY_TAX_AMOUNT)
            print(f"  {player.name} paid luxury tax: ${LUXURY_TAX_AMOUNT}.")

        elif tile == "free_parking":
            print(f"  {player.name} rests on Free Parking. Nothing happens.")

        elif tile == "chance":
            card = self.decks["chance"].draw()
            self._apply_card(player, card)

        elif tile == "community_chest":
            card = self.decks["community"].draw()
            self._apply_card(player, card)

        elif tile in ("railroad", "property"):
            prop = self.resources["board"].get_property_at(position)
            if prop is not None:
                self._handle_property_tile(player, prop)

        self._check_bankruptcy(player)


    def _handle_property_tile(self, player, prop):
        """Decide what to do when `player` lands on a property tile."""
        if prop.owner is None:
            print(f"  {prop.name} is unowned — asking price ${prop.financials['price']}.")
            choice = input("  Buy (b), Auction (a), or Skip (s)? ").strip().lower()
            if choice == "b":
                self.buy_property(player, prop)
            elif choice == "a":
                self.auction_property(prop)
            else:
                print(f"  {player.name} passes on {prop.name}.")
        elif prop.owner == player:
            print(f"  {player.name} owns {prop.name}. No rent due.")
        else:
            self.pay_rent(player, prop)

    def buy_property(self, player, prop):
        """Purchase `prop` on behalf of `player`."""
        if player.balance < prop.financials["price"]:
            print(f"  {player.name} cannot afford {prop.name}.")
            return False
        player.deduct_money(prop.financials["price"])
        prop.owner = player
        player.add_property(prop)
        self.resources["bank"].collect(prop.financials["price"])
        print(f"  {player.name} purchased {prop.name} for ${prop.financials['price']}.")
        return True

    def pay_rent(self, player, prop):
        """Charge `player` the rent and transfer to owner."""
        if prop.is_mortgaged or prop.owner is None:
            return
        rent = prop.get_rent()
        player.deduct_money(rent)
        prop.owner.add_money(rent)
        print(f"  {player.name} paid ${rent} rent on {prop.name} to {prop.owner.name}.")

    def mortgage_property(self, player, prop):
        """Mortgage `prop` owned by `player`."""
        if prop.owner != player:
            return False
        payout = prop.mortgage()
        if payout == 0:
            return False
        player.add_money(payout)
        self.resources["bank"].collect(-payout)
        print(f"  {player.name} mortgaged {prop.name} and received ${payout}.")
        return True

    def unmortgage_property(self, player, prop):
        """Lift the mortgage on `prop`."""
        if prop.owner != player:
            return False
        cost = prop.unmortgage()
        if cost == 0:
            return False
        if player.balance < cost:
            return False
        player.deduct_money(cost)
        self.resources["bank"].collect(cost)
        print(f"  {player.name} unmortgaged {prop.name} for ${cost}.")
        return True

    def _menu_unmortgage(self, player):
        """Interactively unmortgage properties."""
        mortgaged = [p for p in player.properties if p.is_mortgaged]
        if not mortgaged:
            print("  No mortgaged properties.")
            return
        for i, prop in enumerate(mortgaged):
            print(f"  {i+1}. {prop.name} (Cost: ${int(prop.financials['mortgage']*1.1)})")
        idx = ui.safe_int_input("  Select: ", default=0) - 1
        if 0 <= idx < len(mortgaged):
            self.unmortgage_property(player, mortgaged[idx])

    def trade(self, seller, buyer, prop, cash_amount):
        """Execute a property trade."""
        if prop.owner != seller or buyer.balance < cash_amount:
            return False
        buyer.deduct_money(cash_amount)
        seller.add_money(cash_amount)
        prop.owner = buyer
        seller.remove_property(prop)
        buyer.add_property(prop)
        print(f"  Trade: {seller.name} sold {prop.name} to {buyer.name} for ${cash_amount}.")
        return True

    def auction_property(self, prop):
        """Run an auction for `prop`."""
        highest_bid = 0
        highest_bidder = None
        for player in self.players:
            bid = ui.safe_int_input(f"  {player.name}'s bid: ", default=0)
            if highest_bid < bid <= player.balance:
                highest_bid = bid
                highest_bidder = player
        if highest_bidder:
            highest_bidder.deduct_money(highest_bid)
            prop.owner = highest_bidder
            highest_bidder.add_property(prop)
            self.resources["bank"].collect(highest_bid)
            print(f"  {highest_bidder.name} won {prop.name} at auction for ${highest_bid}.")

    def _handle_jail_turn(self, player):
        """Process jail mechanics."""
        if player.jail_info["cards"] > 0 and ui.confirm("  Use card? "):
            player.jail_info["cards"] -= 1
            player.jail_info["in_jail"] = False
            player.jail_info["turns"] = 0
            self._move_and_resolve(player, self.dice.roll())
            return
        if ui.confirm(f"  Pay ${JAIL_FINE}? "):
            player.deduct_money(JAIL_FINE)
            self.resources["bank"].collect(JAIL_FINE)
            player.jail_info["in_jail"] = False
            player.jail_info["turns"] = 0
            self._move_and_resolve(player, self.dice.roll())
            return
        roll = self.dice.roll()
        if self.dice.is_doubles():
            player.jail_info["in_jail"] = False
            player.jail_info["turns"] = 0
            self._move_and_resolve(player, roll)
            return
        player.jail_info["turns"] += 1
        if player.jail_info["turns"] >= 3:
            player.deduct_money(JAIL_FINE)
            self.resources["bank"].collect(JAIL_FINE)
            player.jail_info["in_jail"] = False
            player.jail_info["turns"] = 0
            self._move_and_resolve(player, roll)

    def _apply_card(self, player, card):
        """Apply card results."""
        if not card:
            return
        action, value = card["action"], card["value"]
        if action == "collect":
            player.add_money(value)
        elif action == "pay":
            player.deduct_money(value)
        elif action == "jail":
            player.go_to_jail()
        elif action == "jail_free":
            player.jail_info["cards"] += 1
        elif action == "move_to":
            self._handle_card_move_to(player, value)

    def _handle_card_move_to(self, player, target):
        old = player.position
        player.position = target
        if target < old:
            player.add_money(GO_SALARY)
        tile = self.resources["board"].get_tile_type(target)
        if tile in ("property", "railroad"):
            prop = self.resources["board"].get_property_at(target)
            if prop:
                self._handle_property_tile(player, prop)

    def _check_bankruptcy(self, player):
        """Bankruptcy rescue loop."""
        while player.is_bankrupt():
            if not [p for p in player.properties if not p.is_mortgaged]:
                break
            if ui.confirm("  Mortgage to save yourself? "):
                self._menu_mortgage(player)
            else:
                break
        if player.is_bankrupt():
            player.is_eliminated = True
            for p in list(player.properties):
                p.owner = None
                p.is_mortgaged = False
            player.properties.clear()
            self.players.remove(player)

    def find_winner(self):
        """Return the player with the highest net worth."""
        return max(self.players, key=lambda p: p.net_worth()) if self.players else None

    def interactive_menu(self, player):
        """The pre-roll menu."""
        while True:
            print("\n  1. Standings | 3. Mortgage | 4. Unmortgage | 5. Trade | 7. Build | 0. Roll")
            choice = ui.safe_int_input("  Choice: ", default=0)
            if choice == 0:
                break
            if choice == 1:
                ui.print_standings(self.players)
            elif choice == 3:
                self._menu_mortgage(player)
            elif choice == 4:
                self._menu_unmortgage(player)
            elif choice == 5:
                # Placeholder trade
                self._menu_trade(player, player)
            elif choice == 7:
                self._menu_build(player)

    def _menu_mortgage(self, player):
        m = [p for p in player.properties if not p.is_mortgaged]
        for i, p in enumerate(m):
            print(f"  {i+1}. {p.name}")
        idx = ui.safe_int_input("  Select: ", default=0) - 1
        if 0 <= idx < len(m):
            self.mortgage_property(player, m[idx])

    def _menu_build(self, player):
        b = [p for p in player.properties if p.group.all_owned_by(player)]
        if not b:
            return
        for i, p in enumerate(b):
            print(f"  {i+1}. {p.name} ({p.houses} houses)")
        idx = ui.safe_int_input("  Select: ", default=0) - 1
        if 0 <= idx < len(b):
            if player.balance >= 100:
                player.deduct_money(100)
                b[idx].houses += 1

    def _menu_trade(self, player, partner):
        # Extremely simplified trade for verification
        pass
