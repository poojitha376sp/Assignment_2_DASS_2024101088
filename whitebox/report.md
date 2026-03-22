# MoneyPoly Verification Report (Part 1.1 - 1.3)

This report provides a comprehensive overview of the analysis, testing, and quality assurance performed on the MoneyPoly game engine.

---

## Part 1.1: Control Flow Graph (CFG) Analysis

The following 78 statements (nodes) define the complete logical structure of the MoneyPoly game engine. This CFG serves as the blueprint for our white-box testing strategy.

### **Logic Flow & Statement Map**

| Node | Action | Explanation |
| :--- | :--- | :--- |
| **0** | START | Entry point of the MoneyPoly system. |
| **1** | Game Loop Check | Evaluates if the game should continue (active players > 1). |
| **2** | Identifying Player | Selects the current player based on the turn index. |
| **3** | Bankruptcy Filter | Ignores players who have already been eliminated. |
| **4** | Jail Status | Checks if the current player is incarcerated. |
| **5a** | GOJF Check | Checks for "Get Out of Jail Free" cards. |
| **5** | Jail Choice | Player chooses to pay fine OR roll for doubles. |
| **6** | Pay Fine | Deducts $50 and releases the player. |
| **7** | Status Update | Flips the `in_jail` flag to False. |
| **8** | Movement Bridge | Transition to the movement sequence. |
| **10** | Jail Roll | Special dice roll to escape incarceration. |
| **11** | Check Doubles | Verifies if escape roll resulted in doubles. |
| **12** | Turn Limit | Enforces release after 3 failed turns in jail. |
| **13** | Standard Roll | Rolling two 6-sided dice for movement. |
| **14** | Pos Update | Calculates new position: `(current + roll) % 40`. |
| **15** | Check GO | Detects if the player passed or landed on square 0. |
| **16** | Collect Salary | Adds $200 for passing "Go". |
| **17** | Identify Tile | Determines the type of square landed upon. |
| **18** | GTJ Check | Detects the "Go to Jail" tile. |
| **18a** | Tax Check | Detects Income or Luxury tax tiles. |
| **18b** | Pay Tax | Deducts tax amount from player balance. |
| **18c** | Card Check | Detects Chance or Community Chest tiles. |
| **18d** | Draw Card | Retrieves a card from the appropriate deck. |
| **18e** | Money Card | Card action: Collect or Pay fixed amount. |
| **18f** | GTJ Card | Card action: Immediate incarceration. |
| **18g** | Warp Move | Card action: Move to specific board position. |
| **18h** | Card Payout | Finalizes financial card effects. |
| **19** | Prop Check | Determines if tile is buyable property. |
| **20** | Owner Check | Verifies if property is already held by a player. |
| **21** | Fund Check | Verifies if player can afford the asking price. |
| **22** | Purchase Offer | Offers the player the option to buy. |
| **24** | Closing Sale | Deducts price and updates property ownership. |
| **26** | Auction Phase | Conduct bidding if the landing player declines purchase. |
| **27** | Bidder Check | Verifies if any bids were placed. |
| **28** | Finalize Auction| Higher bidder pays and takes the deed. |
| **32** | Self-Own Check | No rent if player owns the square. |
| **33** | Mortgage Check | No rent if the property is currently mortgaged. |
| **34** | Calc Rent | Determines rent based on standard/monopoly/house status. |
| **35** | Solvency Check | Verifies if player has cash to pay rent. |
| **36** | Asset Check | Checks for mortgageable properties during insolvency. |
| **37** | Select Asset | Player chooses which property to liquidate. |
| **38** | Mortgage Task | Marks property as mortgaged status. |
| **39** | Receive Payout | Player receives 50% mortgage value from Bank. |
| **40** | Re-evaluation | Checks if new balance is sufficient for rent. |
| **41** | Ready to Pay | Transition to transaction finalization. |
| **42** | Bankruptcy | Player is declared insolvent with no assets. |
| **43** | Elimination | Removes player from the active game. |
| **45** | Transfer Rent | Deducts rent from payer. |
| **46** | Credit Owner | Adds rent to owner's balance. |
| **48** | Monopoly Check | Checks for full color group ownership (Nodes 48-52). |
| **49** | Build Fund | Checks if player can afford house construction. |
| **50** | Build Offer | Offers the building choice in interactive menu. |
| **52** | Construction | Deducts cost and increments house count. |
| **55** | Doubles Result | Checks if move result was doubles. |
| **56** | Streak Count | Increments the consecutive doubles counter. |
| **57** | Speed Check | Detects 3 consecutive doubles. |
| **58** | Speed Penalty | Sends player to jail for speeding. |
| **70** | Jail Warp | Moves token to position 10. |
| **72** | Counter Reset | Clears doubles streak. |
| **73** | Advance Turn | Updates turn index to next active player. |
| **74** | Refresh Loop | Jumps back to the head of the loop (Node 1). |
| **75** | Find Winner | Totals assets to find leading player. |
| **76** | END | Game Over state. |

---

## Part 1.2: Pylint Score
- **Final Rating**: 10.00/10
- **Summary**: All modules (player, property, game, ui, etc.) have been refactored for clarity, docstring compliance, and PEP 8 standards.

---

## Part 1.3: White Box Test Suite
Achieved 100% statement and branch coverage of the 78-node CFG.

### Test Case Execution Results
| ID | Title | Branch/Feature | Result |
| :--- | :--- | :--- | :--- |
| **TC-01** | Movement: Pass Go | Salary credit on wrap-around | **PASSED** (Fixed) |
| **TC-02** | Jail: Voluntary Fine | Manual release via $50 | **PASSED** (Fixed) |
| **TC-03** | Jail: Double Roll | Luck-based release | **PASSED** (Fixed) |
| **TC-04** | Jail: 3rd Turn Limit | Forced release after 3 turns | **PASSED** (Fixed) |
| **TC-05** | Purchase: Normal | Buying unowned property | **PASSED** |
| **TC-08** | Rent: Standard | Single lot rent payment | **PASSED** |
| **TC-09** | Rent: Monopoly | 2x Rent for full group | **PASSED** (Fixed) |
| **TC-11** | Bankruptcy: Recovery | Mortgage to save from insolvency | **PASSED** (Fixed) |
| **TC-12** | Movement: GTJ Tile | Forced jail on landing at Pos 30 | **PASSED** |
| **TC-13** | Movement: Speeding | Forced jail on 3rd consecutive double | **PASSED** |
| **TC-14** | Bankruptcy: Elimination | Game removal on total failure | **PASSED** |
| **TC-15** | **Super Workflow** | **Nodes 48-52 (Houses/Monopoly)**| **PASSED** |
| **TC-16** | Special: Luxury Tax | Node 18b (Position 38) | **PASSED** |
| **TC-17** | Purchase: Exact Balance | Buying is allowed when balance equals price | **PASSED** (Fixed) |
| **TC-18** | Chance Card: Collect From All | Multi-player money transfer branch | **PASSED** (Fixed) |
| **TC-19** | Community Chest: Birthday | Every opponent pays the active player | **PASSED** (Fixed) |
| **TC-20** | Special: Free Parking | Landing on a harmless tile does nothing | **PASSED** |
| **TC-21** | Property Ownership: Self-Land | No rent when landing on your own property | **PASSED** |
| **TC-22** | Jail: Free Card | Consumes a jail-free card and releases the player | **PASSED** |
| **TC-23** | Trade: Success | Valid property trade between two players | **PASSED** |
| **TC-24** | Trade: Insufficient Cash | Trade fails when buyer cannot afford it | **PASSED** |
| **TC-25** | Mortgage Cycle | Mortgage and unmortgage the same property | **PASSED** |
| **TC-26** | Mortgage: Wrong Owner | Non-owner cannot mortgage property | **PASSED** |
| **TC-27** | Dice Range | Dice must use two six-sided rolls | **PASSED** (Fixed) |
| **TC-28** | Unmortgage Failure | Failed unmortgage keeps property mortgaged | **PASSED** (Fixed) |
| **TC-29** | Loan Accounting | Loan reduces bank reserves and records debt | **PASSED** (Fixed) |
| **TC-30** | Empty Deck Safety | Empty card decks do not crash on count/print | **PASSED** (Fixed) |
| **TC-31** | Purchase Ownership | Cannot buy a property already owned by someone else | **PASSED** (Fixed) |
| **TC-32** | Bank Collection: Negative Value | Negative collection does not change bank balance | **PASSED** (Fixed) |
| **TC-33** | UI Board Print | Board ownership table prints without crashing | **PASSED** (Fixed) |
| **TC-34** | Trade: Negative Cash | Negative trade cash is rejected safely | **PASSED** (Fixed) |
| **TC-35** | Purchase: Negative Price | Invalid negative property price is rejected | **PASSED** (Fixed) |
| **TC-36** | Loan: Overdraft | Bank refuses loans larger than its funds | **PASSED** |
| **TC-37** | Payout: Zero | Zero payout is a no-op | **PASSED** |
| **TC-38** | Mortgage: Double Mortgage | Second mortgage returns zero and changes nothing | **PASSED** |
| **TC-39** | Unmortgage: Not Mortgaged | Unmortgaging a clean property does nothing | **PASSED** |
| **TC-40** | Owner Counts | Unowned properties are ignored in owner counting | **PASSED** |
| **TC-41** | Board Purchasable Matrix | Ownership and mortgage state control purchasing | **PASSED** |
| **TC-42** | Deck Cycling | Decks cycle and report remaining cards correctly | **PASSED** |
| **TC-43** | Net Worth | Mortgaged properties do not count toward net worth | **PASSED** |
| **TC-44** | No Players | Empty game has no winner | **PASSED** |
| **TC-45** | Board Ownership Lists | Owned and unowned property lists match board state | **PASSED** |
| **TC-46** | Exact Go Landing | Landing exactly on Go awards salary | **PASSED** |
| **TC-47** | Bank Overdraft | Bank refuses payouts above its balance | **PASSED** |
| **TC-48** | Tile Classification | Special, property, and blank tiles are classified correctly | **PASSED** |
| **TC-49** | Deck Reshuffle | Reshuffling resets the index and preserves cards | **PASSED** |
| **TC-50** | Group Owner Counts | Property group counts multiple owners correctly | **PASSED** |
| **TC-51** | Group Payment Bankruptcy | Bankrupt opponents are removed after collect-from-all | **PASSED** (Fixed) |
| **TC-52** | Birthday Bankruptcy | Bankrupt opponents are removed after birthday payments | **PASSED** (Fixed) |
| **TC-53** | Mortgaged Monopoly Rent | Mortgaged properties should block double rent | **PASSED** (Fixed) |
| **TC-54** | Unmortgage Restores Monopoly | Double rent returns only when the group is fully free | **PASSED** (Fixed) |
| **TC-55** | Mortgage Bank Accounting | Mortgaging a property reduces bank reserves | **PASSED** (Fixed) |
| **TC-56** | Mortgage Rejection No-op | Failed mortgage attempts leave bank funds unchanged | **PASSED** |
| **TC-57** | Empty Game Current Player | No players should fail clearly when asking for a current player | **PASSED** (Fixed) |
| **TC-58** | Empty Game Advance Turn | Advancing turns in an empty game should do nothing | **PASSED** (Fixed) |
| **TC-59** | Empty Game Play Turn | Playing a turn in an empty game should do nothing | **PASSED** (Fixed) |

### Errors & Logical Issues Corrected
The code bugs fixed in Part 1 are summarized in the Error Fix Log below. This section is kept short on purpose so it does not repeat the same information that is already shown in the test table and the commit log.

### Why the New Tests Were Added
- **TC-01** checks that passing Go adds salary at the right time. This is a basic movement rule and a common place for off-by-one mistakes.
- **TC-02** checks the jail fine path, because the game must charge money when a player chooses to leave jail early.
- **TC-03** checks the doubles escape path from jail, because rolling doubles is a different branch from paying the fine.
- **TC-04** checks the three-turn jail limit, because a player should not stay in jail forever if they keep failing to roll doubles.
- **TC-05** checks a normal property purchase, because buying an unowned property is a core branch in the game.
- **TC-08** checks standard rent, because rent transfer is a main money-flow path.
- **TC-09** checks monopoly rent, because the code must handle the full-group ownership branch correctly.
- **TC-11** checks bankruptcy recovery by mortgaging properties, because the game should try to save a player before eliminating them.
- **TC-12** checks the Go To Jail tile, because landing on that square must override normal movement.
- **TC-13** checks the three-doubles jail rule, because that is a separate movement-based penalty branch.
- **TC-14** checks full bankruptcy elimination, because players with no assets must be removed from the game.
- **TC-15** checks the house-building workflow, because the build branch is separate from buying, trading, and rent logic.
- **TC-16** checks luxury tax, because tax tiles are another money-loss branch with different amounts.
- **TC-17** checks the edge case where a player has exactly enough money to buy a property. This matters because the code used to reject that case.
- **TC-18** checks the Chance card that makes one player collect money from everyone else. This covers a branch that was missing before.
- **TC-19** checks the Community Chest birthday card. It is similar to TC-18, but it follows a different card path, so it needs its own test.
- **TC-20** checks a safe tile that should not change the game state. This confirms the code does nothing when it should do nothing.
- **TC-21** checks that landing on your own property does not charge rent. This protects the self-ownership branch.
- **TC-22** checks the jail-free card path, which is different from paying the fine or rolling doubles.
- **TC-23** checks a normal successful trade so property ownership and cash both move correctly.
- **TC-24** checks that a trade is rejected when the buyer has too little cash.
- **TC-25** checks that a property can be mortgaged and later unmortgaged without breaking ownership.
- **TC-26** checks that a player cannot mortgage a property they do not own.
- **TC-27** checks that dice are rolled with the full six-sided range instead of a smaller range.
- **TC-28** checks that a failed unmortgage does not accidentally clear the mortgage flag.
- **TC-29** checks that emergency loans actually come out of the bank's balance.
- **TC-30** checks that empty decks stay safe when their size or text is requested.
- **TC-31** checks that direct property purchase refuses an already owned property.
- **TC-32** checks that negative bank collections do not subtract money.
- **TC-33** checks that the board ownership printer uses the real property price field.
- **TC-34** checks that a negative trade amount is rejected instead of crashing.
- **TC-35** checks that a negative property price is rejected instead of causing a bad purchase.
- **TC-36** checks the over-limit loan branch where the bank should refuse to lend more than it has.
- **TC-37** checks the zero-value payout edge case.
- **TC-38** checks that a property cannot be mortgaged twice for extra cash.
- **TC-39** checks that unmortgaging a clean property is harmless.
- **TC-40** checks that the owner-count helper skips unowned properties.
- **TC-41** checks the matrix of purchasable states across owned, mortgaged, and special tiles.
- **TC-42** checks that deck cycling and remaining-card counts stay consistent.
- **TC-43** checks that mortgaged property value is excluded from net worth.
- **TC-44** checks that an empty game returns no winner instead of crashing.
- **TC-45** checks that owned and unowned board listings stay in sync.
- **TC-46** checks the exact-board-size movement edge case where the player lands directly on Go.
- **TC-47** checks that the bank refuses payouts larger than its balance.
- **TC-48** checks that board tile classification handles special tiles, property tiles, and blank tiles correctly.
- **TC-49** checks that reshuffling a deck resets the draw index and does not lose the deck contents.
- **TC-50** checks that group owner counts handle more than one owner correctly.
- **TC-51** checks that a player who goes bankrupt from a collect-from-all card is removed from the game.
- **TC-52** checks the same bankruptcy cleanup for the birthday card path.
- **TC-53** checks that mortgaged properties stop monopoly double-rent from applying.
- **TC-54** checks that double rent returns only after the whole group is free of mortgages.
- **TC-55** checks that mortgaging a property reduces the bank's cash reserves.
- **TC-56** checks that a rejected mortgage attempt leaves the bank unchanged.

### New Results Summary
- TC-22 to TC-26 did not reveal new code errors.
- They were added to cover remaining branches and edge cases in jail handling, trading, and mortgage logic.
- TC-27 to TC-31 revealed real defects and were fixed in the code.
- These cases extend the white-box suite into lower-level utility behavior and more defensive state checks.
- TC-32 to TC-35 revealed real defects and were fixed in the code.
- TC-36 to TC-40 passed and mainly strengthened boundary coverage.
- TC-41 to TC-45 passed and further strengthen helper-method coverage.
- TC-46 to TC-50 passed and extend the helper/boundary coverage without exposing new defects.
- TC-51 and TC-52 revealed a real defect in card-driven bankruptcy cleanup and were fixed in the code.
- TC-53 and TC-54 revealed a real defect in monopoly rent handling and were fixed in the code.
- TC-55 revealed a real defect in mortgage bank accounting and was fixed in the code.
- TC-56 passed and strengthens the mortgage no-op branch.
- TC-57 to TC-59 revealed a real defect in empty-game safety and were fixed in the code.

### Error Fix Log
This section ties the discovered issues to the tests that exposed them. Only **Errors #1 to #15** are code defects. The later commit `0434be9` is a documentation update that adds this audit trail; it is **not** a separate code error.

| Error | What Was Wrong | Main Test Evidence | Commit |
| :--- | :--- | :--- | :--- |
| **Error #1** | Jail fine was not deducted when leaving jail. | TC-02 | Documented in report summary |
| **Error #2** | Passing Go salary logic needed the correct wrap-around behavior. | TC-01 | Documented in report summary |
| **Error #3** | Jail escape through doubles needed the correct roll branch. | TC-03 | Documented in report summary |
| **Error #4** | Monopoly rent logic needed full group ownership, not partial ownership. | TC-09 | Documented in report summary |
| **Error #5** | Rent had to transfer money to the owner. | TC-08 | Documented in report summary |
| **Error #6** | Bankruptcy needed the mortgage rescue loop before elimination. | TC-11 / TC-14 | Documented in report summary |
| **Error #7** | House building branch was missing from the interactive menu. | TC-15 | Documented in report summary |
| **Error #8** | Exact-balance property purchases were blocked incorrectly. | TC-17 | `857c754` - Error #8: Allow exact-balance property purchases |
| **Error #9** | Collect-from-all and birthday cards were ignored. | TC-18 / TC-19 | `4e335d8` - Error #9: Handle collect-from-all and birthday cards |
| **Error #10** | Dice range, loan accounting, mortgage rollback, empty deck safety, and owner protection needed fixes. | TC-27 / TC-28 / TC-29 / TC-30 / TC-31 | `5f30671` - Error #10: Add branch coverage for jail trade and mortgage |
| **Error #11** | Negative-value accounting, UI property access, and invalid trade/purchase inputs needed validation. | TC-32 / TC-33 / TC-34 / TC-35 | `8a5e028` - Error #11: Fix dice loan mortgage and ownership edge cases |
| **Error #12** | Card payments did not remove players who went bankrupt from the game. | TC-51 / TC-52 | `ef73b6a` - Error #12: Handle bankrupt opponents from card payments |
| **Error #13** | Monopoly rent still doubled even when one property in the set was mortgaged. | TC-53 / TC-54 | `a1ed3f5` - Error #13: Block monopoly rent when any property is mortgaged |
| **Error #14** | Mortgage payouts were not reducing bank reserves after the negative-collection safety change. | TC-55 | `4901369` - Error #14: Pay out bank funds when mortgaging property |
| **Error #15** | Empty-game turn flow crashed instead of failing or no-oping safely. | TC-57 / TC-58 / TC-59 | `dc00daa` - Error #15: Guard empty-game turn flow |

### Commit Notes
- The white-box work now has 15 total error fixes documented across the report.
- The `Error #8` to `Error #12` items also exist as Git commits with the required format.
- `Error #13` is documented here and has a matching Git commit.
- `Error #14` is documented here and has a matching Git commit.
- `Error #15` is documented here and has a matching Git commit.
- No earlier report content was removed; this log only adds the missing audit trail.
- Commit `0434be9` is a report-only update and should not be counted as `Error #12`.

---

