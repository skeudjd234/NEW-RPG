from Guild import Game
import logging


if __name__ == "__main__":
    game = Game.load_game()
    game.load_settings()

    logging.info("프로그램 시작")

    while True:
        print("1. 모험가 등록")
        print("2. 전체 모험가 조회")
        print("3. 특정 모험가 검색")
        print("4. 모험가 삭제")
        print("5. 아이템 지급")
        print("6. 아이템 제거")
        print("7. 특정 모험가 인벤토리 조회")
        print("8. 설정 변경")
        print("9. 탐험 목록 조회")
        print("10. 탐험 선택")
        print("11. 프로그램 종료")

        to_do = input("선택: ")

        if to_do == "1":
            name = input("캐릭터의 이름을 입력하세요: ")

            try:
                hp = int(input("캐릭터의 체력을 입력하세요: "))
                atk = int(input("캐릭터의 공격력을 입력하세요: "))
            except ValueError:
                print("숫자를 입력해주세요.")
                continue

            try:
                game.add_char(name, hp, atk)
            except ValueError as e:
                print(e)

        elif to_do == "2":
            for char in game.search_all():
                print(char.get_status())

        elif to_do == "3":
            to_search = input("검색할 모험가의 이름을 입력하세요: ")

            try:
                char = game.search_char(to_search)
                print(char.get_status())
            except ValueError as e:
                print(e)

        elif to_do == "4":
            to_del = input("삭제할 모험가의 이름을 입력하세요: ")

            try:
                game.del_char(to_del)
            except ValueError as e:
                print(e)

        elif to_do == "5":
            to_give = input("아이템을 지급할 모험가의 이름을 입력하세요: ")
            name = input("아이템의 이름을 입력하세요: ")

            try:
                amount = int(input("수량을 입력하세요: "))
            except ValueError:
                print("숫자를 입력해주세요.")
                continue

            type = input("일회성인지, 다회성인지 입력하세요: ")
            grade = input("등급을 입력하세요: ")

            try:
                game.add_inv(to_give, name, amount, type, grade)
            except ValueError as e:
                print(e)

        elif to_do == "6":
            to_del = input("아이템을 제거할 탐험가의 이름을 입력하세요: ")
            name = input("제거할 아이템의 이름을 입력하세요: ")

            try:
                amount = int(input("제거할 수량을 입력하세요: "))
            except ValueError:
                print("숫자를 입력해주세요.")
                continue

            try:
                game.del_inv(to_del, name, amount)
            except ValueError as e:
                print(e)

        elif to_do == "7":
            to_search = input("인벤토리를 조회할 탐험가의 이름을 입력하세요: ")

            try:
                print(game.search_inv(game.search_char(to_search)))
            except ValueError as e:
                print(e)

        elif to_do == "8":
            print("1. 자동 저장 설정 / 2. 삭제 확인 설정 / 3. 취소")
            setting_choice = input("여기에 입력: ")

            if setting_choice == "1":
                if game.settings["autosave"]:
                    game.settings["autosave"] = False
                else:
                    game.settings["autosave"] = True

                game.save_settings()

                logging.info(
                    f"자동 저장 설정 변경: {game.settings['autosave']}"
                )

            elif setting_choice == "2":
                if game.settings["confirm_delete"]:
                    game.settings["confirm_delete"] = False
                else:
                    game.settings["confirm_delete"] = True

                game.save_settings()

                logging.info(
                    f"삭제 확인 설정 변경: "
                    f"{game.settings['confirm_delete']}"
                )

        elif to_do == "9":
            for expedition in game.show_expedition():
                print(expedition.get_info())

        elif to_do == "10":
            expeditions = game.show_expedition()

            for num, expedition in enumerate(expeditions, start=1):
                print(f"{num}. {expedition.get_info()}")

            try:
                expedition_num = int(
                    input("탐험지 번호를 입력하세요: ")
                )

                if expedition_num < 1 or expedition_num > len(expeditions):
                    raise ValueError("존재하지 않는 탐험지 번호입니다.")

                char_name = input(
                    "탐험을 보낼 모험가의 이름을 입력하세요: "
                )

                expedition = expeditions[expedition_num - 1]

                success = game.run_expedition(
                    char_name,
                    expedition.name
                )

                if success:
                    print(
                        f"탐험 성공! "
                        f"{expedition.reward_gold} 골드를 획득했습니다."
                    )
                else:
                    print("탐험 실패!")

            except ValueError as e:
                print(e)

        elif to_do == "11":
            game.save_game()
            logging.info("프로그램 종료")
            break