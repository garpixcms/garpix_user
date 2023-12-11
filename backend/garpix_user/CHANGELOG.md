### 3.10.0-rc18 (11.12.2023)

- `password_validity_passed` task fixed
- Logs fixed

### 3.10.0-rc17 (05.12.2023)

- Permissions and groups logs fixed
- `password_validity_passed` task fixed
- - Upgrade `garpix_utils` to version 1.10.0-rc23

### 3.10.0-rc16 (05.12.2023)

- Block user log added

### 3.10.0-rc15 (05.12.2023)

- Upgrade `garpix_utils` to version 1.10.0-rc21

### 3.10.0-rc14 (01.12.2023)

- Upgrade `garpix_utils` to version 1.10.0-rc17

### 3.10.0-rc13 (27.11.2023)

- Upgrade `garpix_utils` to version 1.10.0-rc14

### 3.10.0-rc12 (27.11.2023)

- Upgrade `garpix_utils` to version 1.10.0-rc13

### 3.10.0-rc11 (27.11.2023)

- `keycloak_auth_only` field added to `GarpixUser` model
- `password_validity_passed` task fixed
- Login/logout logging added

### 3.10.0-rc10 (24.11.2023)

- Upgrade `garpix_utils` to version 1.10.0-rc6

### 3.10.0-rc9 (24.11.2023)

- Upgrade `garpix_utils` to version 1.10.0-rc4
- Password history logs added

### 3.10.0-rc7-3.10.0-rc8 (22.11.2023)

- `GARPIX_ACCESS_TOKEN_TTL_SECONDS` and `GARPIX_REFRESH_TOKEN_TTL_SECONDS` settings deprecated
- `ACCESS_TOKEN_TTL_SECONDS` and `REFRESH_TOKEN_TTL_SECONDS` settings added to `GARPIX_USER`
- translate bugs fixed

### 3.10.0-rc5-3.10.0-rc6 (17.11.2023)

- `PASSWORD_VALIDITY_INFORM_DAYS` setting added
- `PASSWORD_INVALID_EVENT` notify added
- `password_valifity_passed` celery task added
- restore password bug fixed

### 3.10.0-rc3-3.10.0-rc4 (13.11.2023)

- login error messages updated
- `change_password_unauthorized` bug fixed

### 3.10.0-rc2 (08.11.2023)

- `change_password_unauthorized` response updated

### 3.10.0-rc1 (02.11.2023)

- `GarpixUserPasswordConfiguration` model added
- `ADMIN_PASSWORD_SETTINGS` setting added
- `MIN_SPECIAL_PASSWORD` setting added
- `AVAILABLE_ATTEMPT` settings added
- `PASSWORD_HISTORY` setting added
- `PASSWORD_VALIDITY_PERIOD` setting added
- `PASSWORD_FIRST_CHANGE` setting added
- `is_blocked`, `login_attempts_count`, `password_updated_date`, `needs_password_update` fields added to `GarpixUser` model
- `PasswordHistory` model added
- `change_password_unauthorized` endpoint added

### 3.9.1 (29.08.2023)

- `login_view` redirect bug fixed

### 3.9.0 (14.07.2023)

- `CONFIRM_EMAIL_CODE_LIFE_TIME_TYPE` setting added (see `Readme.md)

### 3.8.2 (14.07.2023)

- Error messages localization fixed

### 3.8.1 (26.06.2023)

- Password restore by username fixed

### 3.8.0 (22.06.2023)

- JWT token authorization added (see `Readme.md`)
- `REST_AUTH_HEADER_KEY` setting added (see `Readme.md`)
- Password restore by username fixed

### 3.7.1 (21.06.2023)

- `USE_REGISTRATION` default value updated

### 3.7.0 (20.06.2023)

- `USE_REGISTRATION` setting added

### 3.6.1 (08.06.2023)

- `LoginView` fixed

### 3.6.0 (31.05.2023)

- `username` field added to `restore_password. step 2` endpoint
- `username` help_text added to `restore_password` endpoints
- non authenticated permission added to `login` form

### 3.5.0 (10.05.2023)

- `delete_unconfirmed_users` celery task added (see `Readme.md`)
- Authentication errors fixed
- Localization errors fixed
- `confirm_link_redirect_url` method added (see `Readme.md`)
- email/phone confirmation logic fixed
- `EMAIL_CONFIRMATION_LIFE_TIME` and `PHONE_CONFIRMATION_LIFE_TIME` settings added (see `Readme.md`)

### 3.4.0 (07.03.2023)

- Release fixes to pypi.org.

### 3.4.0-rc1-3.4.0-rc4 (01.03.2023)

- Bugs fixed

### 3.3.1-3.3.2 (28.02.2023)

- Localization error fixed
- Email lowercase error fixed

### 3.3.0 (24.02.2023)

- Localization error fixed
- Registration error fixed
- Delete user error fixed

### 3.2.1 (07.02.2023)

- Log in error fixed

### 3.2.0 (06.02.2023)

- Russian localization updated
- Restore password bugs fixed
- UserSession bugs fixed
- Registration bugs fixed
- Method `set_user_session` added to `User` model (see `Readme.md`)

### 3.1.0 (18.01.2023)

- Russian localization added
- `change_password` endpoint added
- Restore password logic updated

### 3.0.1 (07.11.2022)

- Tokens related names updated

### 3.0.0 (03.11.2022)

- Release on pypi.org.

### 3.0.0-rc5 - 3.0.0-rc6 (26.10.2022)

- Исправлена регистрация через подтверждение email и номера телефона
- Добавлен базовый класс для админ.панели (смотрите `Readme.md`)
- Исправлена связка моделей `User` и `UserSession`.
- Исправлены и дополнены автотесты

### 3.0.0-rc4 (21.10.2022)

- Удален миксин для `UserSession`
- Все миксины добавлены в модели из коробки, теперь все регулируется только настройками в `settings.py`
- Добавлена возможность настраивать список полей, используемых в `CustomAuthenticationBackend` качестве `username` (
  смотрите `Readme.md`)
- Исправлено swagger-документирование эндпоинтов
- Эндпоинт на восстановление пароля теперь принимает `username`.
- Добавлена настройка `REGISTRATION_SERIALIZER` - расширение сериалайзера регитсрации (смотрите `Readme.md`)

### 3.0.0-rc1 - 3.0.0-rc3 (05.10.2022)

- Проект преобразован в `garpix_user`
- Добавлена модель `UserSession` для работы с неавторизованным пользователем
- Добавлен функционал подтверждения номера телефона, email, восстановления и смены пароля (смотрите `Readme.md`)
- Добавлен функционал реферральных ссылок (смотрите `Readme.md`)
- Все настройки для модуля вынесены в единый объект в `settings.py`

### 2.2.0 (07.10.2021)

- Исправлен баг в CustomBackend.
- Добавлена модель AccessToken - создайте миграции!
- Теперь user - ForeignKey (а не OneToOneField) для AccessToken и RefreshToken. Это позволит при выходе с одного
  устройства не терять токен на другом.

### 2.1.0 (21.09.2021)

- Продление, а не изменение токена при протухании, если был рефреш. Без этого часто возникала ситуация, что с
  разных браузеров пропадал доступ.

### 2.0.2 (14.09.2021)

- Исправлена ошибка при получении истекшего токена.

### 2.0.1 (19.08.2021)

- Добавлен permission `IsAuthenticated` для `LogoutView`.

### 2.0.0 (18.08.2021)

- Изменен keyword с `Token` на более правильный - `Bearer` (
  см. https://datatracker.ietf.org/doc/html/rfc6750#section-1.2).
- Оптимизирована функция получения пользователя в токене.
- Добавлено протухание токена (если указано значение `GARPIX_ACCESS_TOKEN_TTL_SECONDS = 0`, то не протухает).
- Добавлен RefreshToken и возвращаемые данные при получении токена.
- Добавлена конечная точка для обновления токена, если он протух (через RefreshToken).
- В obtain_token переименовано поле `token` на `access_token`.

### 1.1.1 (16.06.2021)

- Исправлена ошибка с выключенными урлами для 'authorize'.

### 1.1.0 (16.06.2021)

- Добавлены тесты и логика переписана логика на django form.

### 1.0.1 (29.05.2021)

- Fixed README.

### 1.0.0 (29.05.2021)

- Release on pypi.org.
