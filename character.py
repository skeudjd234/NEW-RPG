class Character:
    def __init__(self, name, hp, atk, gold=0):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.gold = gold
        self.inventory = []

    def add_inv(self, target, amount, type, grade):
        found = False

        for item in self.inventory:
            if item["name"] == target:
                found = True
                item["count"] += amount
                break

        if found == False:
            new_item = {}
            new_item["name"] = target
            new_item["count"] = amount
            new_item["type"] = type
            new_item["grade"] = grade
            self.inventory.append(new_item)

    def get_status(self):
        return self.name, self.hp, self.atk, self.gold, self.inventory

    def del_inv(self, target, amount):
        found = False

        for item in self.inventory:
            if item["name"] == target:
                if item["count"] < amount:
                    raise ValueError("보유 수량보다 더 많이 제거할 수 없습니다.")
                found = True
                item["count"] -= amount
                if item["count"] == 0:
                    self.inventory.remove(item)
                    break
                break

        if found == False:
            raise ValueError("아이템을 발견하지 못했습니다.")

    def to_dict(self):
        return {
            "name": self.name,
            "hp": self.hp,
            "atk": self.atk,
            "gold": self.gold,
            "inventory": self.inventory
        }

    @classmethod
    def from_dict(cls, data):
        required_keys = ["name", "hp", "atk"]
        exists = all(key in data for key in required_keys)

        expected_types = {
            "name": str,
            "hp": int,
            "atk": int,
        }

        item_require = ["name", "count", "type", "grade"]
        item_expected_types = {
            "name": str,
            "count": int,
            "type": str,
            "grade": str
        }

        if exists:
            valid_types = all(
                isinstance(data[key], expected_types[key])
                for key in expected_types
            )

            if valid_types:
                if "gold" in data:
                    if not isinstance(data["gold"], int):
                        raise ValueError("딕셔너리 손상됨")
                passed_items = []
                if "inventory" not in data:
                    to_search = []
                else:
                    if isinstance(data["inventory"], list):
                        to_search = data["inventory"]
                    else:
                        raise ValueError("딕셔너리 손상됨")
                
                for item in to_search:
                    if isinstance(item, dict):
                        normal_item = all(
                            key in item
                            for key in item_require
                        )

                        if normal_item:
                            item_valid_types = all(
                                isinstance(item[key], item_expected_types[key])
                                for key in item_expected_types
                            )
                            if item_valid_types:
                                passed_items.append(item)

                
                Char = cls(
                    data["name"],
                    data["hp"],
                    data["atk"],
                    data.get("gold", 0)
                )
            else:
                raise ValueError("딕셔너리 손상됨")
        else:
            raise ValueError("딕셔너리 손상됨")

        Char.inventory = passed_items
        return Char