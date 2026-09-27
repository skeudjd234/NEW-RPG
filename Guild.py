from character import Character
from expedition import get_expeditions
import json
import logging
from api import send_weather


logging.basicConfig(
    filename="game.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


class Game:

    def __init__(self):
        self.player_list = []
        self.expedition_list = get_expeditions()
        self.settings = {
            "autosave": True,
            "confirm_delete": True
        }

    def search_inv(self, target):
        if target in self.player_list:
            return target.inventory
        else:
            logging.warning("탐험가를 찾지 못했습니다.")
            raise ValueError("플레이어를 찾지 못했습니다.")

    def add_char(self, name, hp, atk):
        for character in self.player_list:
            if character.name == name:
                logging.warning("이름이 중복된 캐릭터는 만들 수 없습니다.")
                raise ValueError("이름이 중복된 캐릭터는 만들 수 없습니다.")

        char = Character(name, hp, atk)
        self.player_list.append(char)

        logging.info(f"탐험가 생성 완료: {name}")

        if self.settings["autosave"]:
            self.save_game()

        return char

    def del_char(self, target):
        if self.settings["confirm_delete"]:
            whether_do = input("제거하시려면 1을 입력하세요: ")

            if whether_do == "1":
                for char in self.player_list:
                    if char.name == target:
                        self.player_list.remove(char)

                        logging.info(f"탐험가 삭제 완료: {target}")

                        if self.settings["autosave"]:
                            self.save_game()

                        return "제거 완료."
            else:
                return None

        else:
            for char in self.player_list:
                if char.name == target:
                    self.player_list.remove(char)

                    logging.info(f"탐험가 삭제 완료: {target}")

                    if self.settings["autosave"]:
                        self.save_game()

                    return "제거 완료."

        logging.warning("탐험가를 찾지 못했습니다.")
        raise ValueError("탐험가를 찾지 못했습니다.")

    def search_char(self, target):
        for char in self.player_list:
            if char.name == target:
                return char

        logging.warning("탐험가를 찾지 못했습니다.")
        raise ValueError("탐험가를 찾지 못했습니다.")

    def search_all(self):
        result = []

        for char in self.player_list:
            result.append(char)

        return result

    def add_inv(self, target, item, amount, type, grade):
        to_give = self.search_char(target)
        to_give.add_inv(item, amount, type, grade)

        logging.info(
            f"아이템 지급 완료: 탐험가={target}, "
            f"아이템={item}, 수량={amount}, 타입={type}, 등급={grade}"
        )

        if self.settings["autosave"]:
            self.save_game()

    def show_expedition(self):
        return self.expedition_list

    def search_expedition(self, target):
        for expedition in self.expedition_list:
            if expedition.name == target:
                return expedition

        logging.warning("존재하지 않는 탐험 이름입니다.")
        raise ValueError("존재하지 않는 탐험 이름입니다.")

    def run_expedition(self, char, expedition):
        char_obj = self.search_char(char)
        expedition_obj = self.search_expedition(expedition)

        if expedition_obj.status != "available":
            logging.warning(
                f"탐험 진행 불가: {char_obj.name} / "
                f"{expedition_obj.name} / "
                f"상태: {expedition_obj.status}"
            )
            raise ValueError("탐험을 진행할 수 없습니다.")

        expedition_obj.start_expedition()

        logging.info(
            f"탐험 시작: {char_obj.name} -> {expedition_obj.name}"
        )

        whether_success = expedition_obj.judge_expedition(char_obj)

        expedition_obj.give_reward(char_obj, whether_success)

        if whether_success:
            logging.info(
                f"탐험 성공: {char_obj.name} / "
                f"{expedition_obj.name} / "
                f"보상: {expedition_obj.reward_gold} 골드"
            )
        else:
            logging.info(
                f"탐험 실패: {char_obj.name} / "
                f"{expedition_obj.name}"
            )

        if self.settings["autosave"]:
            self.save_game()

        return whether_success

    def del_inv(self, target, item, amount):
        to_del = self.search_char(target)

        try:
            to_del.del_inv(item, amount)

        except ValueError as e:
            logging.warning(
                f"아이템 제거 실패: 탐험가={target}, "
                f"아이템={item}, 이유={e}"
            )
            raise

        logging.info(
            f"아이템 제거 완료: 탐험가={target}, "
            f"아이템={item}, 수량={amount}"
        )

        if self.settings["autosave"]:
            self.save_game()

    def get_weather_risk(self):
        weather_code = send_weather()

        if weather_code is None:
            logging.warning("날씨 정보를 불러오지 못해 날씨 리스크를 적용하지 않습니다.")
            return 0

        # 맑음 / 구름
        if weather_code in (0, 1, 2, 3):
            return 0

        # 안개
        elif weather_code in (45, 48):
            return 2

        # 이슬비
        elif weather_code in (51, 53, 55):
            return 3

        # 어는 이슬비
        elif weather_code in (56, 57):
            return 5

        # 비
        elif weather_code in (61, 63, 65):
            return 5

        # 어는 비
        elif weather_code in (66, 67):
            return 7

        # 눈
        elif weather_code in (71, 73, 75, 77):
            return 7

        # 소나기
        elif weather_code in (80, 81, 82):
            return 6

        # 눈 소나기
        elif weather_code in (85, 86):
            return 8

        # 뇌우 / 우박
        elif weather_code in (95, 96, 97, 99):
            return 10

        # 혹시 모르는 코드
        else:
            logging.warning(f"알 수 없는 날씨 코드: {weather_code}")
            return 0

    def to_dict(self):
        result = []

        for char in self.player_list:
                result.append(char.to_dict())

        return {
            "version": 1,
            "players": result
        }

    @classmethod
    def from_dict(cls, data):
        game = cls()

        if "version" not in data:
            data["version"] = 1

        if data["version"] != 1:
            logging.warning(
                f"지원하지 않는 세이브 버전: {data['version']}"
            )
            return game

        if "players" not in data:
            logging.warning(
                "세이브 파일에 players 데이터가 없습니다."
            )
            return game

        if not isinstance(data["players"], list):
            logging.warning(
                "players 데이터가 리스트 형식이 아닙니다."
            )
            return game

        for char in data["players"]:
            if not isinstance(char, dict):
                logging.warning(
                    "잘못된 캐릭터 데이터를 건너뜁니다."
                )
                continue

            try:
                restored_char = Character.from_dict(char)

            except ValueError as e:
                logging.warning(
                    f"손상된 캐릭터 데이터를 건너뜁니다: {e}"
                )
                continue

            game.player_list.append(restored_char)

        return game

    def save_game(self):
        data = self.to_dict()

        try:
            with open("save.json", "w", encoding="utf-8") as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

        except Exception as e:
            logging.error(
                "저장 과정에서 예기치 못한 오류가 발생하였습니다."
            )
            print(
                "저장 과정에서 예기치 못한 오류가 발생하였습니다."
            )
            print(f"예외 코드: {e}")

        else:
            logging.info("저장 완료!")
            print("저장 완료!")

    @classmethod
    def load_game(cls):
        try:
            with open("save.json", "r", encoding="utf-8") as file:
                data = json.load(file)

        except json.JSONDecodeError:
            logging.warning("파일 손상됨.")
            print("파일 손상됨")
            return cls()

        except FileNotFoundError:
            logging.warning("파일이 존재하지 않음.")
            print("파일이 존재하지 않음")
            return cls()

        except Exception as e:
            logging.error(
                "데이터를 로드하는 과정에서 "
                "예기치 못한 오류가 발생하였습니다."
            )
            print(
                "데이터를 로드하는 과정에서 "
                "예기치 못한 오류가 발생하였습니다."
            )
            print(f"예외 코드: {e}")
            return cls()

        else:
            logging.info("불러오기 완료!")
            print("불러오기 완료!")
            return cls.from_dict(data)

    def save_settings(self):
        try:
            with open(
                "settings.json",
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    self.settings,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

        except Exception as e:
            logging.error("예상치 못한 오류 발생")
            print("예상치 못한 오류 발생")
            print(f"예외 코드: {e}")

        else:
            logging.info("설정 저장 완료")

    def load_settings(self):
        try:
            with open(
                "settings.json",
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

        except FileNotFoundError:
            logging.warning(
                "설정 파일이 존재하지 않습니다."
            )
            print("설정 파일이 존재하지 않습니다.")

        except json.JSONDecodeError:
            logging.error(
                "설정 파일이 손상되었습니다."
            )
            print("설정 파일이 손상되었습니다.")

        except Exception as e:
            logging.error(
                "설정 로드 중 예상치 못한 오류 발생."
            )
            print("예상치 못한 오류 발생")
            print(f"예외 코드: {e}")

        else:
            self.settings.update(data)
            logging.info("설정 불러오기 완료")