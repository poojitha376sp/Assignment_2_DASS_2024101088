# Call Graph Visual Layout Guide (Part 2.1)

Use this Mermaid diagram as the blueprint for your **Hand-Drawn Call Graph**.
Every arrow below has been verified against the actual source code.

### **Integration Path Visualizer**

```mermaid
graph TD
    subgraph "Main Controller"
        M1["M1: run_race_sequence"]
        M2["M2: perform_tuning"]
        M3["M3: start_mission"]
    end

    subgraph "Registration"
        RG1["RG1: register_member"]
        RG2["RG2: is_registered"]
    end

    subgraph "Crew Management"
        C1["C1: assign_role"]
        C2["C2: is_role"]
    end

    subgraph "Inventory"
        I1["I1: add_cash"]
        I2["I2: deduct_cash"]
        I3["I3: add_car"]
        I4["I4: has_car"]
        I5["I5: add_parts"]
        I6["I6: use_parts"]
        I7["I7: set_damage"]
        I8["I8: is_damaged"]
    end

    subgraph "Race Mgmt"
        R1["R1: create_race"]
        R2["R2: get_race"]
    end

    subgraph "Results"
        RE1["RE1: finalize_race"]
    end

    subgraph "Missions"
        MS1["MS1: assign_mission"]
    end

    subgraph "Tuning"
        T1["T1: upgrade_car"]
    end

    subgraph "Sponsors"
        S1["S1: sign_sponsor"]
        S2["S2: trigger_win_bonus"]
    end

    subgraph "Trophy Room"
        TR1["TR1: add_trophy"]
    end

    %% === MAIN CONTROLLER CALLS ===
    M1 -->|"schedules"| R1
    M1 -->|"finalizes"| RE1
    M1 -->|"checks bonus"| S2
    M2 -->|"upgrades"| T1
    M3 -->|"assigns"| MS1

    %% === RACE MODULE CALLS ===
    R1 -->|"driver check"| C2
    R1 -->|"car check"| I4

    %% === RESULTS MODULE CALLS ===
    RE1 -->|"lookup race"| R2
    RE1 -->|"add prize $"| I1
    RE1 -->|"mark damage"| I7
    RE1 -->|"award trophy"| TR1

    %% === MISSION MODULE CALLS ===
    MS1 -->|"role check"| C2
    MS1 -->|"damage check"| I8
    MS1 -->|"repair car"| I7

    %% === TUNING MODULE CALLS ===
    T1 -->|"mechanic check"| C2
    T1 -->|"consume parts"| I6
    T1 -->|"pay cash"| I2
    T1 -.->|"rollback parts"| I5

    %% === SPONSOR MODULE CALLS ===
    S2 -->|"credit bonus $"| I1

    %% === CREW MODULE CALLS ===
    C1 -->|"verify member"| RG2
```

### **Drawing Instructions for Hand-Drawn Version:**

1.  **Modules = Boxes**: Draw 10 boxes (one per module). Each box is labeled with the module name.
2.  **Functions = Circles**: Inside each box, draw a circle for each function node (e.g., `R1`, `R2` inside the "Race Mgmt" box).
3.  **Arrows = Solid Lines**: Draw a solid arrow from the caller circle to the callee circle. Label each arrow with the action (e.g., "driver check").
4.  **Rollback = Dashed Line**: The `T1 -> I5` rollback should be drawn as a **dashed arrow** to indicate it's a conditional/error path.
5.  **Grouping**: Place the "Main Controller" box at the top, with arrows fanning downward to Race, Results, Sponsors, Tuning, and Missions. Place Inventory and Crew at the bottom since they are the most-called modules.
6.  **Cross-Module Highlighting**: Use a different color (e.g., red) for arrows that cross module boundaries to clearly show "inter-module" calls.
