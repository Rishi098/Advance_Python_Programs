import random

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack = 20
        self.inventory = []

    def is_alive(self):
        return self.health > 0

    def take_damage(self, dmg):
        self.health -= dmg
        print(f"{self.name} took {dmg} damage! Current Health: {self.health}")

    def attack_enemy(self, enemy):
        dmg = random.randint(10, self.attack)
        enemy.take_damage(dmg)
        print(f"{self.name} attacks {enemy.name} for {dmg} damage!")

class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def is_alive(self):
        return self.health > 0

    def take_damage(self, dmg):
        self.health -= dmg
        print(f"{self.name} took {dmg} damage! Remaining Health: {self.health}")

    def attack_player(self, player):
        dmg = random.randint(5, self.attack)
        player.take_damage(dmg)
        print(f"{self.name} attacks {player.name} for {dmg} damage!")

class Room:
    def __init__(self):
        self.has_monster = random.choice([True, False])
        self.has_treasure = random.choice([True, False])
        self.has_trap = random.choice([True, False])
        self.monster = Enemy("Goblin", 50, 15) if self.has_monster else None
        self.treasure = random.choice(["Gold", "Potion", "Sword"]) if self.has_treasure else None
        self.trap_damage = random.randint(5, 25) if self.has_trap else 0

    def enter(self, player):
        print("\nYou enter a new room...")
        if self.has_trap:
            print(f"Oh no! You triggered a trap and took {self.trap_damage} damage!")
            player.take_damage(self.trap_damage)
        if self.has_monster:
            print(f"A wild {self.monster.name} appears!")
            while player.is_alive() and self.monster.is_alive():
                action = input("Do you want to (F)ight or (R)un? ").lower()
                if action == 'f':
                    player.attack_enemy(self.monster)
                    if self.monster.is_alive():
                        self.monster.attack_player(player)
                elif action == 'r':
                    chance = random.randint(1, 2)
                    if chance == 1:
                        print("You successfully escaped!")
                        return
                    else:
                        print("Failed to escape!")
                        self.monster.attack_player(player)
                else:
                    print("Invalid action! Choose F or R.")
            if not player.is_alive():
                print("You died in combat!")
                return
            else:
                print(f"You defeated the {self.monster.name}!")
        if self.has_treasure:
            print(f"You found a treasure: {self.treasure}!")
            player.inventory.append(self.treasure)

def play_game():
    name = input("Enter your character's name: ")
    player = Player(name)
    rooms_to_explore = 5

    for i in range(rooms_to_explore):
        if not player.is_alive():
            print("Game Over!")
            break
        print(f"\n--- Room {i+1} ---")
        room = Room()
        room.enter(player)
    else:
        print(f"\nCongratulations {player.name}! You survived the dungeon.")
        print(f"Your inventory: {player.inventory}")

if __name__ == "__main__":
    play_game()
