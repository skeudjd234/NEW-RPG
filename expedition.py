import random


class Expedition:
    def __init__(self, name, recommended_atk, risk, reward_gold, status="available"):
        self.name = name
        self.recommended_atk = recommended_atk
        self.risk = risk
        self.reward_gold = reward_gold
        self.status = status

    def get_info(self):
        return (
            self.name,
            self.recommended_atk,
            self.risk,
            self.reward_gold,
            self.status
        )

    def start_expedition(self):
        if self.status == "available":
            self.status = "running"

    def done_expedition(self):
        if self.status == "running":
            self.status = "completed"

    def judge_expedition(self, char, weather_risk=0):
        effective_risk = self.risk + weather_risk

        score = (
            ((char.hp / 2) * char.atk)
            / (char.hp / 50 + char.atk / 10)
            / ((effective_risk + self.recommended_atk) * 2)
        )

        success_rate = 7 * (score ** 2) - 12 * score
        success_rate = max(0, min(100, success_rate))

        roll = random.uniform(0, 100)

        return roll <= success_rate

    def give_reward(self, char, whether_success):
        if self.status != "running":
            return

        if whether_success:
            char.gold += self.reward_gold
            self.status = "completed"
        else:
            self.status = "failed"

    @classmethod
    def from_dict(cls, data):
        return cls(
            name = data["name"],
            recommended_atk = data["recommended_atk"],
            risk = data["risk"],
            reward_gold = data["reward_gold"],  
           )
    


EXPEDITIONS = [
    # 초보
    {
        "name": "목초지",
        "recommended_atk": 10,
        "risk": 5,
        "reward_gold": 100
    },

    # 쉬움
    {
        "name": "버려진 농장",
        "recommended_atk": 15,
        "risk": 5,
        "reward_gold": 150
    },
    {
        "name": "공업지대",
        "recommended_atk": 20,
        "risk": 7,
        "reward_gold": 200
    },

    # 보통
    {
        "name": "버려진 광산",
        "recommended_atk": 25,
        "risk": 13,
        "reward_gold": 500
    },
    {
        "name": "갱도",
        "recommended_atk": 30,
        "risk": 15,
        "reward_gold": 750
    },

    # 어려움
    {
        "name": "무법지대",
        "recommended_atk": 30,
        "risk": 20,
        "reward_gold": 1000
    },
    {
        "name": "버려진 일대",
        "recommended_atk": 30,
        "risk": 25,
        "reward_gold": 1500
    },

    # 최종 난이도
    {
        "name": "전선",
        "recommended_atk": 35,
        "risk": 30,
        "reward_gold": 2500
    }
]

def get_expeditions():
    result = []

    for data in EXPEDITIONS:
        result.append(Expedition.from_dict(data))

    return result