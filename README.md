![foodgram-project](https://github.com/Riyce/foodgram-project-react/actions/workflows/main.yaml/badge.svg)
<hr>
<hr>
<h1> Foodgram </h1>
Проект Foodgram предназначен для размещения рецептов.
<hr>
В данном репозитории представлен проект Foodgram с возможностью запуска в контейнеах Docker со всеми необходимыми зависимостями.
<hr>
Развернутый проект доступен по ссылке: http://selkieproject.tk/
Тестовый пользователь: username - Testuser, password - t1e1s1t1U

Создайте для проекта директорию:
`mkdir <название директории>`
<br>И сразу перейдите в нее:
`cd <название директории>` <br>
<br>Чтобы загрузить проект необходмо выполнить команду:<br>
`git clone https://github.com/Riyce/foodgram-project-react`

<h4>
Для запуска проекта необходимо установить Docker.<br>
Инструкции по установке можно найти здесь - https://docs.docker.com/engine/install/ <br>
</h4>

Для развертывания контейнеров необходимо выполнить команду: `docker-compose up -d --build`
<br>Теперь проект доступен по адресу: http://127.0.0.1/
<br> Для корректной работы с приложением необходимо выполнить миграции.
<br> По команде `docker-compose exec web bash` перед вами откроется оболочка Bash контейнера web.
<br> Далее, для выполнения миграций нужно последовательно выполнить следующие команды:
<li> python manage.py makemigrations api
<li> python manage.py migrate
<br> Для создания супрепользователя с доступом в админку выполните следующую команду:
<li> python manage.py createsuperuser
<br> Для заполнения базы данных тестовыми данными выполните следующую команду:
<li> python manage.py load_data
<br> Для выхода из оболочки Bash контейнера просто пропишите команду:
<li> exit
<br> Для остановки работы всех контейнеров выполните команду:
<li> docker-compose stop
<br> Для удаления контейнеров выполните команду:
<li> docker-compose down

