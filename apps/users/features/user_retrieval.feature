Feature: Получение информации о пользователе
  As a user
  I want to be able to retrieve information about a specific user
  So that I can see the user's details

  Scenario: Успешное получение информации о пользователе по ID
    Given существует пользователь с ID "1"
    When я отправляю GET-запрос на "/users/1/"
    Then я получаю ответ со статусом "200 OK"
    And ответ содержит следующие данные о пользователе:
      | поле       | значение               |
      | username   | "user1"                |
      | first_name | "John"                 |
      | last_name  | "Doe"                  |
      | email      | "user1@example.com"    |
      | phone      | "+123456789"           |
      | position   | "Developer"            |
      | project    | "AgileProject"         |

  Scenario: Получение информации о пользователе с несуществующим ID
    Given не существует пользователя с ID "999"
    When я отправляю GET-запрос на "/users/999/"
    Then я получаю ответ со статусом "404 Not Found"
    And ответ содержит сообщение "User not found"