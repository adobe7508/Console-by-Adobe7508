import os

class MyLangInterpreter:
    def __init__(self):
        self.variables = {}
        self.characters = {}
        self.current_character = None

    def interpret(self, line):
        parts = line.split(" ", 1)
        command = parts[0]

        if command == "p":
            if len(parts) > 1:
                self.handle_print(parts[1])
            else:
                print()

        elif command == "i":
            if len(parts) > 1:
                self.handle_input(parts[1])
            else:
                print("Usage: i <variable_name>")

        elif command == "new":
            if len(parts) > 1:
                self.handle_new(parts[1])
            else:
                print("Usage: new <variable_name> <value>")

        elif command == "open":
            if len(parts) > 1:
                self.handle_open(parts[1])
            else:
                print("Usage: open <filename.cla>")

        elif command == "import":
            if len(parts) > 1:
                self.handle_import(parts[1])
            else:
                print("Usage: import <filename.cla>")

        elif command == "if":
            if len(parts) > 1:
                self.handle_if(parts[1])
            else:
                print("Usage: if <condition>")

        elif command == "while":
            if len(parts) > 1:
                self.handle_while(parts[1])
            else:
                print("Usage: while <condition>")

        else:
            print(f"Unknown command: {command}")

    def handle_if(self, condition):
        condition_parts = condition.split(" ", 1)
        if len(condition_parts) < 2:
            print("Usage: if <variable> <operator> <value>")
            return

        var_name, operator_value = condition_parts[0], condition_parts[1].split(" ", 1)
        if len(operator_value) != 2:
            print("Usage: if <variable> <operator> <value>")
            return

        operator, value = operator_value
        value = int(value) if value.isdigit() else value
        var_value = self.variables.get(var_name)
        if var_value.isdigit():
            var_value = int(var_value)

        if operator == "==":
            if var_value == value:
                print(f"Condition is true for: {var_name} {operator} {value}")
        elif operator == "!=":
            if var_value != value:
                print(f"Condition is true for: {var_name} {operator} {value}")
        elif operator == ">":
            if var_value > value:
                print(f"Condition is true for: {var_name} {operator} {value}")
        elif operator == "<":
            if var_value < value:
                print(f"Condition is true for: {var_name} {operator} {value}")
        elif operator == ">=":
            if var_value >= value:
                print(f"Condition is true for: {var_name} {operator} {value}")
        elif operator == "<=":
            if var_value <= value:
                print(f"Condition is true for: {var_name} {operator} {value}")
        else:
            print(f"Unknown operator: {operator}")

    def handle_while(self, condition):
        condition_parts = condition.split(" ", 1)
        if len(condition_parts) < 2:
            print("Usage: while <variable> <operator> <value>")
            return

        var_name, operator_value = condition_parts[0], condition_parts[1].split(" ", 1)
        if len(operator_value) != 2:
            print("Usage: while <variable> <operator> <value>")
            return

        operator, value = operator_value
        value = int(value) if value.isdigit() else value
        print(f"Starting loop while {var_name} {operator} {value}")

        while True:
            var_value = self.variables.get(var_name)
            if var_value.isdigit():
                var_value = int(var_value)

            if operator == "==":
                if var_value != value:
                    break
            elif operator == "!=":
                if var_value == value:
                    break
            elif operator == ">":
                if var_value <= value:
                    break
            elif operator == "<":
                if var_value >= value:
                    break
            elif operator == ">=":
                if var_value < value:
                    break
            elif operator == "<=":
                if var_value > value:
                    break
            else:
                print(f"Unknown operator: {operator}")
                break

            print(f"Looping with {var_name}: {var_value}")
            # Modify the variable within the loop to prevent an infinite loop
            self.variables[var_name] = var_value - 1  # Example modification

    def handle_import(self, filename):
        if not filename.endswith('.cla'):
            print("Error: File must have a .cla extension.")
            return

        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found.")
            return

        print(f"Importing from '{filename}'...")
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    print(f"Executing: {line}")
                    self.interpret(line)

    def handle_open(self, filename):
        if not filename.endswith('.cla'):
            print("Error: File must have a .cla extension.")
            return

        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found.")
            return

        print(f"Opening '{filename}'...")
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    print(f"Executing: {line}")
                    self.interpret(line)

    def handle_print(self, text):
        for var in self.variables:
            text = text.replace(f"${var}", str(self.variables[var]))
        print(text)

    def handle_input(self, variable_name):
        value = input(f"Enter value for {variable_name}: ")
        self.variables[variable_name] = value

    def handle_new(self, command):
        parts = command.split(" ", 1)
        if len(parts) == 2:
            var_name, value = parts
            self.variables[var_name] = value
        else:
            print("Usage: new <variable_name> <value>")

    def handle_create_character(self, command):
        parts = command.split(" ")
        name = parts[0]
        health = int(parts[1]) if len(parts) > 1 else 100
        self.characters[name] = {'health': health, 'inventory': []}
        print(f"Character '{name}' created with {health} health.")

    def handle_attack(self, target_name):
        if target_name in self.characters:
            damage = 10
            self.characters[target_name]['health'] -= damage
            print(f"{self.current_character} attacked {target_name} for {damage} damage!")
            print(f"{target_name}'s health is now {self.characters[target_name]['health']}.")
        else:
            print(f"Character '{target_name}' not found!")

    def handle_add_item(self, item_name):
        if self.current_character:
            self.characters[self.current_character]['inventory'].append(item_name)
            print(f"{item_name} added to {self.current_character}'s inventory.")
        else:
            print("No active character.")

    def handle_show_inventory(self):
        if self.current_character:
            inventory = self.characters[self.current_character]['inventory']
            print(f"{self.current_character}'s inventory: {', '.join(inventory) if inventory else 'Empty'}")
        else:
            print("No active character.")

    def handle_narrate(self, story):
        print(story)

if __name__ == "__main__":
    interpreter = MyLangInterpreter()
    while True:
        try:
            command = input("> ")
            interpreter.interpret(command)
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
