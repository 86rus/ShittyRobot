#!/usr/bin/env python3
import math


class RobotTurnCalculator:
    def __init__(self):
        # Ваши калибровочные данные
        self.calibration_data = {
            "left": {
                90: {"speed": 127, "time": 0.8},
                180: {"speed": 127, "time": 1.4},
                45: {"speed": 120, "time": 0.5},
                360: {"speed": 135, "time": 2.7},
            },
            "right": {
                90: {"speed": 118, "time": 0.8},
                180: {"speed": 118, "time": 1.5},
                45: {"speed": 118, "time": 0.5},
                360: {"speed": 125, "time": 3.5},
            },
        }

        # Вычисляем коэффициенты
        self.calculate_coefficients()

        # Граничные значения
        self.min_time = 0.3
        self.max_time = 3.0
        self.min_speed = 100
        self.max_speed = 255

    def calculate_coefficients(self):
        """Вычисляем коэффициенты k = угол / (скорость * время)"""
        self.left_coeffs = []
        self.right_coeffs = []

        for angle, data in self.calibration_data["left"].items():
            k = angle / (data["speed"] * data["time"])
            self.left_coeffs.append(k)

        for angle, data in self.calibration_data["right"].items():
            k = angle / (data["speed"] * data["time"])
            self.right_coeffs.append(k)

        # Средний коэффициент
        self.avg_k_left = sum(self.left_coeffs) / len(self.left_coeffs)
        self.avg_k_right = sum(self.right_coeffs) / len(self.right_coeffs)

    def calculate_turn(self, angle_degrees):
        """
        Рассчитать параметры поворота
        angle_degrees: положительный = влево, отрицательный = вправо
        возвращает: (direction, speed, time)
        """
        if angle_degrees > 0:
            direction = 3  # Влево
            angle = angle_degrees
            avg_k = self.avg_k_left
            default_speed = self.calibration_data["left"][90]["speed"]
        elif angle_degrees < 0:
            direction = 4  # Вправо
            angle = abs(angle_degrees)
            avg_k = self.avg_k_right
            default_speed = self.calibration_data["right"][90]["speed"]
        else:
            # Угол 0 - стоп
            return (5, 0, 0)

        # Рассчитываем время
        time = angle / (avg_k * default_speed)
        time = round(time, 1)

        # Корректируем если время выходит за пределы
        if time < self.min_time:
            new_speed = int(angle / (avg_k * self.min_time))
            new_speed = min(new_speed, self.max_speed)
            new_speed = max(new_speed, self.min_speed)
            time = angle / (avg_k * new_speed)
            return (direction, new_speed, round(time, 1))

        if time > self.max_time:
            new_speed = int(angle / (avg_k * self.max_time))
            new_speed = min(new_speed, self.max_speed)
            new_speed = max(new_speed, self.min_speed)
            time = angle / (avg_k * new_speed)
            return (direction, new_speed, round(time, 1))

        return (direction, default_speed, time)

    def predict_angle(self, direction, speed, time):
        """Предсказать угол поворота по параметрам"""
        if direction == 3:
            avg_k = self.avg_k_left
        else:
            avg_k = self.avg_k_right

        angle = avg_k * speed * time
        return round(angle, 1)


def main():
    calculator = RobotTurnCalculator()

    print("\n" + "=" * 60)
    print("🤖 КАЛЬКУЛЯТОР ПОВОРОТОВ РОБОТА")
    print("=" * 60)
    print("Введите угол поворота в градусах:")
    print("  положительный = влево (например: 30)")
    print("  отрицательный = вправо (например: -45)")
    print("  0 = остановка")
    print("\nКоманды:")
    print("  q, quit, exit - выход")
    print("  help, h, ?    - показать справку")
    print("=" * 60)

    while True:
        try:
            # Получаем ввод
            user_input = input("\n👉 Угол: ").strip().lower()

            # Проверка на выход
            if user_input in ["q", "quit", "exit", "выход"]:
                print("\n👋 До свидания!")
                break

            # Проверка на справку
            if user_input in ["help", "h", "?", "помощь"]:
                print("\n📖 СПРАВКА:")
                print("  Введите угол поворота в градусах")
                print("  Примеры:")
                print("    30  → поворот влево на 30°")
                print("    -45 → поворот вправо на 45°")
                print("    0   → остановка")
                print("    q   → выход")
                continue

            # Пропускаем пустой ввод
            if not user_input:
                continue

            # Преобразуем в число
            try:
                angle = float(user_input)
            except ValueError:
                print("❌ Ошибка: введите число (угол в градусах)")
                continue

            # Рассчитываем параметры
            direction, speed, time_val = calculator.calculate_turn(angle)

            # Предсказываем реальный угол
            if angle != 0:
                predicted = calculator.predict_angle(direction, speed, time_val)
            else:
                predicted = 0

            # Выводим результат
            print("\n" + "-" * 50)

            if angle > 0:
                print(f"📐 Желаемый угол: {angle}° ВЛЕВО")
            elif angle < 0:
                print(f"📐 Желаемый угол: {abs(angle)}° ВПРАВО")
            else:
                print(f"📐 Желаемый угол: 0° (СТОП)")

            if angle != 0:
                # Выводим команду
                print(f"\n🎮 КОМАНДА:")
                print(f"   {direction} {speed} {time_val}")

                # Детальные параметры
                dir_name = (
                    "ВЛЕВО"
                    if direction == 3
                    else "ВПРАВО" if direction == 4 else "СТОП"
                )
                print(f"\n📊 ПАРАМЕТРЫ:")
                print(f"   Направление: {direction} ({dir_name})")
                print(f"   Скорость: {speed}")
                print(f"   Время: {time_val} сек")

                # Прогноз
                print(f"\n🔮 Прогнозируемый угол: {predicted}°")

                # Погрешность
                error = abs(abs(angle) - predicted)
                if error > 0.5:
                    print(f"⚠️  Погрешность: ±{error}°")
                elif error > 0:
                    print(f"✅ Точность: ±{error}°")
                else:
                    print(f"✅ Идеально!")
            else:
                print(f"\n🎮 КОМАНДА:")
                print(f"   5 0 0")
                print(f"\n📊 ПАРАМЕТРЫ:")
                print(f"   Направление: 5 (СТОП)")
                print(f"   Скорость: 0")
                print(f"   Время: 0 сек")

            print("-" * 50)

        except KeyboardInterrupt:
            print("\n\n👋 Прервано пользователем. До свидания!")
            break
        except Exception as e:
            print(f"❌ Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()
