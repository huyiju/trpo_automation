РЕЛИЗ 0.0.0.6

Что нужно сделать чтобы получить первый релиз на вашем компьютере:

- Установить linux (любой: Ubuntu, CentOS, Debain)

- Зайти в консоль (Ctrl + Alt + t)

- Перейти в нужную вам папку (cd /home/$USER/path/to/your/dir)

- Склонировать наш репозиторий (git clone https://github.com/Students-of-the-city-of-Kostroma/trpo_automation.git)

- Перейти в папку с проектом (cd trpo_automation/)

- Перейти на ветку 18-ISbo-2b (git checkout 18-ISbo-2b)

- Если необходимо, скопировать папку с проектом в другое необходимое вам место (/path/to/dir/)

- Изменить путь к папке с логами в файле /path/to/dir/config.py (path_to_logs = "/path/to/dir/logs/")

- Сделать файл main.py исполняемым, инструкция в (instructions) (sudo chmod 0755 /path/to/dir/main.py)

- Чтобы запустить проект как демон, нужно ввести в консоль инструкцию в (instructions) (start-stop-daemon -Sbvx /path/to/dir/main.py) 

- Чтобы запустить проект в явном виде в консоли, нужно ввести в консоль инструкцию в (instructions) (python3 /path/to/dir/main.py)

- Чтобы остановить проект, ввести в консоль инструкцию в (instructions)(stop) (start-stop-daemon -Kvx /usr/bin/python3 /path/to/dir/main.py) либо в явном режиме Ctrl + C

Работу релиза можно проверить в папке /path/to/dir/logs, куда после каждого круга скидываются логи.

ЗАДАЧА НА РЕЛИЗ

- Протестировать

- Исправить баги

- Настроить CI

- Разобраться с логированием

