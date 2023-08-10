from une_ai.models import Agent

class SnakeAgent(Agent):
    def __init__(self, agent_program):
        super().__init__("Snake Agent", agent_program)

    def add_all_sensors(self):
        # Implement all the sensors here
        self.add_sensor("body-sensor", [], lambda x: isinstance(x, list))
        self.add_sensor("food-sensor", [], lambda x: isinstance(x, list))
        self.add_sensor("obstacles-sensor", [], lambda x: isinstance(x, list))
        self.add_sensor("clock", 0, lambda x: isinstance(x, (int, float)))

    def add_all_actuators(self):
        # Implement all the actuators here
        self.add_actuator("head", "up", lambda x: x in ["up", "down", "left", "right"])
        self.add_actuator("mouth", "close", lambda x: x in ["open", "close"])

    def add_all_actions(self):
        # Implement all the actions here
        self.add_action("move-up", self.move_up)
        self.add_action("move-down", self.move_down)
        self.add_action("move-left", self.move_left)
        self.add_action("move-right", self.move_right)
        self.add_action("open-mouth", self.open_mouth)
        self.add_action("close-mouth", self.close_mouth)

    # Helper methods for actions
    def move_up(self):
        current_head_direction = self.read_actuator_value("head")
        if current_head_direction != "down":
            return {"head": "up"}
        return {}

    def move_down(self):
        current_head_direction = self.read_actuator_value("head")
        if current_head_direction != "up":
            return {"head": "down"}
        return {}

    def move_left(self):
        current_head_direction = self.read_actuator_value("head")
        if current_head_direction != "right":
            return {"head": "left"}
        return {}

    def move_right(self):
        current_head_direction = self.read_actuator_value("head")
        if current_head_direction != "left":
            return {"head": "right"}
        return {}

    def open_mouth(self):
        return {"mouth": "open"}

    def close_mouth(self):
        return {"mouth": "close"}
