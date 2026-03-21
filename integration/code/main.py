"""
StreetRace Manager - Central Controller
The "Integration Layer" coordinating all 8 modules.
"""

from integration.code.registration import RegistrationModule
from integration.code.crew import CrewModule
from integration.code.inventory import InventoryModule
from integration.code.race import RaceModule
from integration.code.results import ResultsModule
from integration.code.missions import MissionModule
from integration.code.tuning import TuningModule
from integration.code.sponsors import SponsorModule
from integration.code.trophy import TrophyModule

class StreetRaceManager:
    def __init__(self):
        # 1. Initialize Sub-modules
        self.registration = RegistrationModule()
        self.crew = CrewModule(self.registration)
        self.inventory = InventoryModule()
        self.races = RaceModule(self.crew, self.inventory)
        self.trophy = TrophyModule()
        self.results = ResultsModule(self.inventory, self.races, self.trophy)
        self.missions = MissionModule(self.crew, self.inventory)
        self.tuning = TuningModule(self.crew, self.inventory)
        self.sponsors = SponsorModule(self.inventory)

    def run_race_sequence(self, race_id, driver_name, car_name, position, prize):
        """
        A complex 5-module integration flow.
        Flow: Crew -> Inventory -> Race -> Results -> Sponsors -> Inventory
        """
        # 1. Start Race
        success, msg = self.races.create_race(race_id, driver_name, car_name)
        if not success:
            return msg
        
        # 2. Finalize Results
        success, msg = self.results.finalize_race(race_id, position, prize)
        if not success:
            return msg
            
        # 3. Check for Sponsorship Payouts
        success, msg2 = self.sponsors.trigger_win_bonus(race_id)
        
        return f"{msg} | {msg2 if success else 'No Sponsor Bonus'}"

    def perform_tuning(self, car_name, mechanic_name, type):
        """Integration between Tuning, Crew, and Inventory."""
        return self.tuning.upgrade_car(car_name, mechanic_name, type)

    def start_mission(self, mission_type, member_name):
        """Integration between Missions and Crew."""
        return self.missions.assign_mission(mission_type, member_name)
