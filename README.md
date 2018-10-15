RT_tests - батарея тестов для оценки времени реакции
======================================================

_Description in English below_

Эта батарея тестов предназначена для оценки индивидуальных различий времени ответа в различных заданиях на принятие решения: простое время реакции (SRT, CRT2, CRT4, SRT_rel, CRT2_rel), задача Струпа с двумя и тремя цветами (stroop2_1, stroop2_2, stroop3_1, stroop3_2), классификация вербальных стимулов (VerbCRT) и классификация зрительных стимулов (VisCRT).

_Запуск батареи:_ 
bash/cmd: `python launch.py`  
или: `launch.bat`

Описание батареи тестов
=======================
Батарея тестов разрабатывалась как автономная программа для сбора данных в школах. В то же время она составляет набор средств, призванных облегчить дальнейшую разработку и применение простых когнитивных тестов. Батарея включает следующий функционал:
1. Тесты реализованы как классы, наследующие классам CogTest или CogTestRelease. Эти общие классы описывают методы, свойства и логику тестов в целом. CogTest реализует тесты, в которых ответ дается путем нажатия клавиши на клавиатуре, CogTestRelease реализует тесты, в которых ответ дается путем освобождения клавиши. Список тестов в батарее хранится в файле `testlist.py`, состав батареи легко изменяется исключением/перемещением тестов в списке.
2. Каждый тест начинается с инструкции или демонстрации теста, тренировочной серии и одной или нескольких основных серий проб.
3. Тестовая батарея была разработана для использования в школах при минимальном контроле со стороны тестера или учителя. Ряд функций введены для того, чтобы повысить качество данных:
* Программа проверяет, что точность ответов (доля правильных ответов) находится выше заданного предела (по умолчанию 70%). Если респондент делает много ошибок, выполнение теста прекращается и респондент смотрит инструкцию/демонстрацию еще раз. Если точность ответов остается низкой, тест прерывается и начинается следующий.
* Аналогичная логика применяется в ситуации, когда респондент дает несколько невалидных ответов подряд (по умолчанию 10). Невалидным ответом, в частности, является преждевременный ответ.
* Чтобы снизить утомление респондентов - это школьники - тест прерывается короткими паузами (по умолчанию каждые 40 проб, длительность паузы составляет 6с).
* По каждой пробе, по тесту и по батарее в целом записывается подробная информация (временная отметка, статус выполнения). Программа также пишет логи и спецификацию компьютера (характеристики процессора, рабочей памяти и экрана).
4. Скрипт `test_summary.py` собирает и записывает характеристики тестов, вошедших в тестовую батарею, в том числе общее количество проб.
5. Пользователь может выбрать прохождение полной или демо-версии теста. Демо-версия включает по 20 проб в каждом тесте, не считая тренировочную серию.

Описание тестов
===============
_SRT, CRT2, CRT4:_ респондент отвечает на стимул, которые появляется в одной, двух или четырех позициях. Ответ дается нажатием клавиши.

_VerbCRT:_ респондент отвечает, относится ли слово, предъявляемое на экране, к животным или к растениям.

_stroop2_1:_ респондент отвечает, какого цвета предъявляемый на экране нейтральный стимул (XXXXXXX), красного или зеленого.

_stroop2_2:_ респондент отвечает, какого цвета слово ('красный' или 'зеленый'), предъявляемое на экране, красного или зеленого.

_stroop3_1:_ респондент отвечает, какого цвета предъявляемый на экране нейтральный стимул (XXXXXXX), красного, зеленого или синего.

_stroop3_2:_ респондент отвечает, какого цвета слово ('красный', 'зеленый' или 'голубой'), предъявляемое на экране, красного, зеленого или синего.

_VisCRT:_ респондент отвечает, совпадают ли две фигуры на экране по какому-то признаку (по форме или по цвету). Название признака предъявляется вместе с фигурами на экране. 
_Из набора исключены полностью совпадающие фигуры._

_SRT_rel, CRT2_rel:_ респондент отвечает на стимул, которые появляется в одной или двух. Ответ дается освобождением клавиши.

Технические требования
======================
Реалицация батареи опирается на функционал PsychoPy. Standalone-версии PsychoPy (v.1.90.3, or PsychoPy2) достаточно.
Для полноценной работы PsychoPy2 необходим исправный OpenGL 2.0 (подробнее [здесь][requirements]).


Планирую реализовать
====================
1. Хранение данных в зашифрованном виде.
2. Автономный экзешник для OS Windows.

----------------------------------------------------------------------------------------------------------------------------

This is Reaction Time test battery
==================================

This test battery is implemented to assess individual differences in response time across various decision tasks: simple and choice reaction time (SRT, CRT2, CRT4, SRT_rel, CRT2_rel), Stroop task with two and three colors (stroop2_1, stroop2_2, stroop3_1, stroop3_2), verbal classification (VerbCRT) and visual classification (VisCRT).

_Quick start:_  
bash/cmd: `python launch.py`  
also: `launch.bat`

Description of test battery
===========================
This battery aims to serve as a selfcontained software to be used for assessment at school. At the same time it simplifies development of the tests and allows modification of test workflow across the whole test battery. It includes following functionality:
1. The tests are implemented as instances of CogTest and CogTestRelease classes. This eases modification of the whole battery and separate tests. CogTest implements press responses, CogTestRelease - release responses. The list of tests is stored in `testlist.py`. The battery can be modified by commenting out or rearranging the tests in a test list.
2. Each test starts with instruction/demonstration, training session and one or several main sessions. 
3. The test battery has been developed to be used at school with minimum intervention from tester/teacher. This is why the script performs additional checks to help to ensure that the date are valid:
* The script checks that accuracy lies above certain level (default is 70%). When participant performs poor, the script interrupts and repeats demonstration. If performance remains low, the test interrupts execution and passes to the next.
* The logic applies when participant gives a sequence of invalid answers (e.g., preterm responses), 10 by default.
* At regular intervals (each 40 trials by default) the test pauses to let a participant have a short break (6s by default).
* For each trial within the test and for the whole battery the detailed information is recorded (timestamp, execution status). The script also writes the log and computer specifications (CPU, RAM, screen resolution).
4. The script `test_summary.py` gathers specifications of test battery, including total number of trials.
5. The user can choose to pass either full or demo version of the test battery. Demo version сuts number of trials in ach test to 20 (let alone training session that remains unchanged).

Description of tests
====================
_SRT, CRT2, CRT4:_ participant has to respond to a stimulus appearing in one, two or four possible positions by pressing the key.

_VerbCRT:_ participant has to reply whether a word on the screen means plant or animal.

_stroop2_1:_ participant has to reply whether neutral stimulus (XXXXXXX) on the screen is red or green.

_stroop2_2:_ participant has to reply whether a word ('red' or 'green') on the screen is written in red or green.

_stroop3_1:_ participant has to reply whether neutral stimulus (XXXXXXX) on the screen is red, green or blue.

_stroop3_2:_ participant has to reply whether a word ('red', 'green' or 'blue') on the screen is written in red, green or blue.

_VisCRT:_ participant has to compare two shapes by either shape or color, depending on the cue (a word 'shape' or 'color').

_SRT_rel, CRT2_rel:_ participant has to respond to a stimulus appearing in one or two possible positions by releasing the key.


Requirements
============
The implementation is based on PsychoPy. The standalone version of PsychoPy (v.1.90.3, or PsychoPy2) is supposedly sufficient. PsychoPy2 requires fully finctional OpenGL 2.0 (details [here][requirements]).

To be implemented
=================
1. Encrypted storage of personal data.
2. Self-contained executable for OS Windows.

[requirements]: http://psychopy.org/installation.html
