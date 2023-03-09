#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Kev.in - a coding learning platform
# Copyright (C) 2022 to 2023  Max Linke and others
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import flask_unittest
from flask_sqlalchemy.query import sqlalchemy
from flask_unittest import ClientTestCase
from flask_unittest.case import FlaskClient

from backend import create_app
from backend.database.models import UserModel, UserRole, db


class BaseTest(ClientTestCase):
    app = create_app("testing.cfg")
    base_header = {"Content-Type": "application/json"}

    def setUp(self, client: FlaskClient) -> None:
        raise NotImplementedError

    def tearDown(self, client: FlaskClient) -> None:
        raise NotImplementedError


class ExternalTest(BaseTest):
    user_id = None
    user_name = "Willie Baldomero"
    user_mail = "willie.baldomero@example.com"
    user_pass = "eiZach2shoh4yo6kieBieFei"
    user_role = UserRole.User
    external_header = BaseTest.base_header.copy()

    def setUp(self, client: FlaskClient) -> None:
        # create user
        self.assertTrue(client is not None)
        self.assertTrue(isinstance(client, FlaskClient))
        user = UserModel(
            user_name=ExternalTest.user_name,
            user_pass=ExternalTest.user_pass,
            user_mail=ExternalTest.user_mail,
            user_role=ExternalTest.user_role,
        )
        with ExternalTest.app.app_context():
            db.session.add(user)
            try:
                db.session.commit()
            except sqlalchemy.exc.IntegrityError as e:
                db.session.rollback()
                user = db.session.execute(db.select(UserModel).filter_by(user_mail=ExternalTest.user_mail)).scalar_one()
            ExternalTest.user_id = user.user_id
        self.assertTrue(ExternalTest.user_id is not None)
        self.assertTrue(isinstance(ExternalTest.user_id, int))

    def tearDown(self, client: FlaskClient) -> None:
        # delete user
        self.assertTrue(client is not None)
        self.assertTrue(isinstance(client, FlaskClient))
        with ExternalTest.app.app_context():
            users = db.session.execute(db.select(UserModel)).scalars()
            for user in users:
                db.session.delete(user)
                db.session.commit()
        ExternalTest.user_id = None

    # --- GET ---

    def test_get(self, client: FlaskClient) -> None:
        """Check whether the GET method requires an access token on the 'user' route."""
        self.assertTrue(ExternalTest.user_id is not None)
        r = client.get(f"/user?user_id={ExternalTest.user_id}")
        self.assertEqual(r.status_code, 401)

    # --- POST ---

    def test_post(self, client: FlaskClient) -> None:
        """Check whether the POST method requires an access token on the 'user' route."""
        self.assertTrue(ExternalTest.user_id is not None)
        r = client.post("/user", json={"user_id": ExternalTest.user_id})
        self.assertNotEqual(r.status_code, 401)

    def test_post_user(self, client: FlaskClient) -> None:
        """Check whether creating a user is possible and returns the JWT and CSRF tokens."""
        r = client.post(
            "/user",
            json={
                "user_name": "Hulbert Loring",
                "user_mail": "hulber.loring@example.com",
                "user_pass": "ahfahvai9AhCho8eiKei4Zoo",
            },
        )
        self.assertEqual(r.status_code, 201)
        self.assertTrue(r.is_json)
        self.assertIn("access_token_cookie", [cookie.name for cookie in client.cookie_jar])
        self.assertIn("csrf_access_token", [cookie.name for cookie in client.cookie_jar])

    def test_post_duplicate_user(self, client: FlaskClient) -> None:
        r = client.post(
            "/user",
            json={
                "user_name": ExternalTest.user_name,
                "user_mail": ExternalTest.user_mail,
                "user_pass": ExternalTest.user_pass,
            },
        )
        self.assertEqual(r.status_code, 409)

    def test_post_user_with_empty_name(self, client: FlaskClient) -> None:
        r = client.post(
            "/user",
            json={"user_name": "", "user_mail": "diedrick.berdy@example.com", "user_pass": "oinae3Chac8Ighai4oi6shui"},
        )
        self.assertEqual(r.status_code, 400)

    def test_post_user_with_empty_mail(self, client: FlaskClient) -> None:
        r = client.post(
            "/user",
            json={"user_name": "Diedrick Berdy", "user_mail": "", "user_pass": "oinae3Chac8Ighai4oi6shui"},
        )
        self.assertEqual(r.status_code, 400)

    def test_post_user_with_empty_password(self, client: FlaskClient) -> None:
        r = client.post(
            "/user",
            json={"user_name": "Diedrick Berdy", "user_mail": "diedrick.berdy@example.com", "user_pass": ""},
        )
        self.assertEqual(r.status_code, 400)

    def test_post_user_with_long_name(self, client: FlaskClient) -> None:
        long_name = """\
Cee2buenie9Ooque3Aep9TheiZ7EeSh6Itie8thapheexoo0aiph3oliedelaoch\
o6Uub3zeer5quie1lik7Quadae2ohl1ohBah0nah1neiSh7kueb0Eef5queequoo\
5ohva2sai5geigeethian7Thaucei3ahxuiL9OhghiediuGhedothaiC0Phe0eul\
5teekie6Qui9kohth7ooRaelohv3ainae5Goo1ooko1Phah3phohiiPaethae6Ph\
eaYieboofei7Ees5tah9iaPaerah1faeng1eeh2aep2obohree8Qua0iexeighae\
n8cheit5eijiwieghe4eithiekooquaiHahbeed4eichohpheuToow0faingiang\
ohNgoht1eiy3ahgh0ootooshi3quie0eiHei6foo3kauhongiuj1ahm2aek1geth\
ooPhaic9tohf6eeTh9chi6kaedephahnoov0oiseijooJ2ahhoofohwai4Raesh0\
ShaiT6aaZ4haeWah9eix6laezietho3aeshaeb8wahti4eeSo3voolo3ohjei2th\
atah9uyiGh0ipaikuchohDuorelee9phingooju3vah0eiSae1Uekohphee2omah\
4ahr0zoozoaWei1teejebaethohthu7hoJu0Eewahl8Iek1xooD4aew7iePhoo6l\
iese3uu2hae7equai2eizo9ovaoPeeth6ichiengaeThohk7doocaileitheez0A\
hsh6Aemeez9ieHahniexooxoo8CifohpauSa3hip4AiCain7gaid7vizehee1cee\
6noo5uhu4xahNuag0tu2eigi6Eich9Ailahnahrahzibier4ESh0eTutheu3zah6\
uow3Adei0ahpaotheeshoht0nee2edei9quui8IeJ4ei2queehohsi6aetailaoN\
agaev3reighoh3tiewoh8ahd6saevuquu2isheiko6them5iegh2Oochohsheeg7"""
        r = client.post(
            "/user",
            json={
                "user_name": long_name,
                "user_mail": "long.mail@example.com",
                "user_pass": "Iacoovie8UthahKeelai3our",
            },
        )
        self.assertEqual(r.status_code, 201)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["user_name"], long_name)
        self.assertIn("access_token_cookie", [cookie.name for cookie in client.cookie_jar])
        self.assertIn("csrf_access_token", [cookie.name for cookie in client.cookie_jar])

    def test_post_user_with_strange_name(self, client: FlaskClient) -> None:
        strange_name = "⚗〠ൠᴥ௵ஔ∰ጃ෴ᅘ༽໒✺"
        r = client.post(
            "/user",
            json={
                "user_name": strange_name,
                "user_mail": "strange.mail@example.com",
                "user_pass": "uiTong5cho1IaZee5eef2Pie",
            },
        )
        self.assertEqual(r.status_code, 201)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["user_name"], strange_name)
        self.assertIn("access_token_cookie", [cookie.name for cookie in client.cookie_jar])
        self.assertIn("csrf_access_token", [cookie.name for cookie in client.cookie_jar])

    # --- PUT ---

    def test_put(self, client: FlaskClient) -> None:
        """Check whether the PUT method requires an access token on the 'user' route."""
        self.assertTrue(ExternalTest.user_id is not None)
        r = client.put("/user", json={"user_id": ExternalTest.user_id})
        self.assertEqual(r.status_code, 401)

    # --- DELETE ---

    def test_delete(self, client: FlaskClient) -> None:
        """Check whether the DELETE method requires an access token on the 'user' route."""
        self.assertTrue(ExternalTest.user_id is not None)
        r = client.delete("/user", json={"user_id": ExternalTest.user_id})
        self.assertEqual(r.status_code, 401)


class UserTest(BaseTest):
    user_id = None
    user_name = "Willie Baldomero"
    user_mail = "willie.baldomero@example.com"
    user_pass = "eiZach2shoh4yo6kieBieFei"
    user_role = UserRole.User
    user_header = BaseTest.base_header.copy()

    def setUp(self, client: FlaskClient) -> None:
        # create user
        self.assertTrue(client is not None)
        self.assertTrue(isinstance(client, FlaskClient))
        user = UserModel(
            user_name=UserTest.user_name,
            user_pass=UserTest.user_pass,
            user_mail=UserTest.user_mail,
            user_role=UserTest.user_role,
        )
        with UserTest.app.app_context():
            db.session.add(user)
            try:
                db.session.commit()
            except sqlalchemy.exc.IntegrityError as e:
                db.session.rollback()
                user = db.session.execute(db.select(UserModel).filter_by(user_mail=UserTest.user_mail)).scalar_one()
            UserTest.user_id = user.user_id
        self.assertTrue(UserTest.user_id is not None)
        self.assertTrue(isinstance(UserTest.user_id, int))
        # login user
        r = client.post(
            "/login",
            json={"user_mail": UserTest.user_mail, "user_pass": UserTest.user_pass},
            headers=UserTest.user_header,
        )
        self.assertEqual(r.status_code, 200)
        for cookie in client.cookie_jar:
            if cookie.name == UserTest.app.config["JWT_ACCESS_CSRF_COOKIE_NAME"]:
                UserTest.user_header.update({UserTest.app.config["JWT_ACCESS_CSRF_HEADER_NAME"]: cookie.value})

    def tearDown(self, client: FlaskClient) -> None:
        # TODO: logout user
        # delete user
        self.assertTrue(client is not None)
        self.assertTrue(isinstance(client, FlaskClient))
        with UserTest.app.app_context():
            users = db.session.execute(db.select(UserModel)).scalars()
            for user in users:
                db.session.delete(user)
                db.session.commit()
        client.delete_cookie("", UserTest.app.config["JWT_ACCESS_COOKIE_NAME"])
        client.delete_cookie("", UserTest.app.config["JWT_ACCESS_CSRF_COOKIE_NAME"])
        UserTest.user_id = None
        del UserTest.user_header[UserTest.app.config["JWT_ACCESS_CSRF_HEADER_NAME"]]

    # --- GET ---

    def test_get_existing_by_id(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        r = client.get(f"/user?user_id={UserTest.user_id}", headers=UserTest.user_header)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertIn(UserTest.user_id, [d["user_id"] for d in r.json["data"]])

    def test_get_existing_by_name(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        r = client.get(f"/user?user_name={UserTest.user_name}", headers=UserTest.user_header)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertIn(UserTest.user_id, [d["user_id"] for d in r.json["data"]])

    def test_get_existing_by_mail(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        r = client.get(f"/user?user_mail={UserTest.user_mail}", headers=UserTest.user_header)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertIn(UserTest.user_id, [d["user_id"] for d in r.json["data"]])

    def test_get_existing_by_role(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        r = client.get(f"/user?user_role={UserTest.user_role}", headers=UserTest.user_header)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertIn(UserTest.user_id, [d["user_id"] for d in r.json["data"]])

    def test_get_non_existing_by_id(self, client: FlaskClient) -> None:
        user_id = -1
        r = client.get(f"/user?user_id={user_id}", headers=UserTest.user_header)
        self.assertEqual(r.status_code, 204)

    def test_get_non_existing_by_name(self, client: FlaskClient) -> None:
        user_name = "Does Not Exist"
        r = client.get(f"/user?user_name={user_name}", headers=UserTest.user_header)
        self.assertEqual(r.status_code, 204)

    def test_get_non_existing_by_mail(self, client: FlaskClient) -> None:
        user_mail = "does.not.exist@example.com"
        r = client.get(f"/user?user_mail={user_mail}", headers=UserTest.user_header)
        self.assertEqual(r.status_code, 204)

    def test_get_non_existing_by_role(self, client: FlaskClient) -> None:
        user_role = -1
        r = client.get(f"/user?user_role={user_role}", headers=UserTest.user_header)
        self.assertEqual(r.status_code, 400)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["message"], {"user_role": f"{user_role} is not a valid UserRole"})

    def test_get_multiple_ids(self, client: FlaskClient) -> None:
        user = UserModel(
            user_name="Shermon Horst", user_pass="faiVairo3kaeFoa3Eeyuweah", user_mail="shermon.horst@example.com"
        )
        db.session.add(user)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            self.fail("Can not create second user: integrity constraint failed!")
        else:
            r = client.get(
                f"/user?user_id={UserTest.user_id}&user_id={user.user_id}",
                json={"user_id": user.user_id},
                headers=UserTest.user_header,
            )
            self.assertEqual(r.status_code, 200)
            self.assertTrue(r.is_json)
            self.assertEqual(r.json["meta"]["total"], 2)
            db.session.delete(user)
            db.session.commit()

    def test_get_id_type_int(self, client: FlaskClient) -> None:
        user_id = 1
        r = client.get(f"/user?user_id={user_id}", headers=UserTest.user_header)
        self.assertNotEqual(r.status_code, 400)

    def test_get_id_type_float(self, client: FlaskClient) -> None:
        user_id = 1.5
        r = client.get(f"/user?user_id={user_id}", headers=UserTest.user_header)
        self.assertEqual(r.status_code, 400)

    def test_get_id_type_str(self, client: FlaskClient) -> None:
        user_id = "aaa"
        r = client.get(f"/user?user_id={user_id}", headers=UserTest.user_header)
        self.assertEqual(r.status_code, 400)

    def test_get_id_type_bool(self, client: FlaskClient) -> None:
        user_id = True
        r = client.get(f"/user?user_id={user_id}", headers=UserTest.user_header)
        self.assertEqual(r.status_code, 400)

    def test_get_role_type_int(self, client: FlaskClient) -> None:
        user_role = 1
        r = client.get(f"/user?user_role={user_role}", headers=UserTest.user_header)
        self.assertNotEqual(r.status_code, 400)

    def test_get_role_type_float(self, client: FlaskClient) -> None:
        user_role = 1.5
        r = client.get(f"/user?user_role={user_role}", headers=UserTest.user_header)
        self.assertEqual(r.status_code, 400)

    def test_get_role_type_str(self, client: FlaskClient) -> None:
        user_role = "aaa"
        r = client.get(f"/user?user_role={user_role}", headers=UserTest.user_header)
        self.assertEqual(r.status_code, 400)

    def test_get_role_type_bool(self, client: FlaskClient) -> None:
        user_role = True
        r = client.get(f"/user?user_role={user_role}", headers=UserTest.user_header)
        self.assertEqual(r.status_code, 400)

    def test_get_restrict_page_size(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        user_limit = 1
        r = client.get(f"/user?user_role={UserTest.user_role}&user_limit={user_limit}", headers=UserTest.user_header)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(user_limit, r.json["meta"]["page_size"])

    def test_get_page_index_zero(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        user_page = 0
        r = client.get(f"/user?user_id={UserTest.user_id}&user_page={user_page}", headers=UserTest.user_header)
        self.assertEqual(r.status_code, 404)
        self.assertTrue(r.is_json)
        self.assertEqual(
            r.json["message"],
            "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
        )

    def test_get_self(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        r = client.get("/user", headers=UserTest.user_header)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(UserTest.user_id, r.json["user_id"])

    def test_get_user_pass(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        r = client.get(f"/user?user_id={UserTest.user_id}", headers=UserTest.user_header)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertNotIn("user_pass", r.json["data"][0].keys())

    # --- POST ---

    # --- PUT ---

    def test_put_mail_to_existing(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        user = UserModel("user_name", "user_pass", "user_mail")
        db.session.add(user)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            self.fail("Can not create second user: integrity constraint failed!")
        else:
            r = client.put(
                "/user",
                json={"user_id": UserTest.user_id, "user_mail": user.user_mail},
                headers=UserTest.user_header,
            )
            self.assertEqual(r.status_code, 409)
            self.assertTrue(r.is_json)
            self.assertEqual(r.json["message"], "An user with this mail does already exist")

    def test_put_name_to_empty(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        r = client.put("/user", json={"user_id": UserTest.user_id, "user_name": ""}, headers=UserTest.user_header)
        self.assertEqual(r.status_code, 400)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["message"], "user_name must not be empty")

    def test_put_mail_to_empty(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        r = client.put("/user", json={"user_id": UserTest.user_id, "user_mail": ""}, headers=UserTest.user_header)
        self.assertEqual(r.status_code, 400)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["message"], "user_mail must not be empty")

    def test_put_password_to_empty(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        r = client.put("/user", json={"user_id": UserTest.user_id, "user_pass": ""}, headers=UserTest.user_header)
        self.assertEqual(r.status_code, 400)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["message"], "user_pass must not be empty")

    def test_put_admin_elevation_as_user(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        r = client.put(
            "/user", json={"user_id": UserTest.user_id, "user_role": UserRole.Admin.value}, headers=UserTest.user_header
        )
        self.assertEqual(r.status_code, 403)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["message"], "No Access")

    def test_put_sadmin_elevation_as_user(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        r = client.put(
            "/user",
            json={"user_id": UserTest.user_id, "user_role": UserRole.SAdmin.value},
            headers=UserTest.user_header,
        )
        self.assertEqual(r.status_code, 403)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["message"], "No Access")

    def test_put_demotion_as_user(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        user = UserModel("user_name", "user_pass", "user_mail", UserRole.Admin)
        db.session.add(user)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            self.fail("Can not create second user: integrity constraint failed!")
        else:
            r = client.put(
                "/user",
                json={"user_id": user.user_id, "user_role": UserRole.User.value},
                headers=UserTest.user_header,
            )
            self.assertEqual(r.status_code, 403)
            self.assertTrue(r.is_json)
            self.assertEqual(r.json["message"], "No Access")

    def test_put_id_type_str(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        user_id = "aaa"
        r = client.put("/user", json={"user_id": user_id}, headers=UserTest.user_header)
        self.assertEqual(r.status_code, 400)

    def test_put_role_type_str(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        user_role = "aaa"
        r = client.put(
            "/user", json={"user_id": UserTest.user_id, "user_role": user_role}, headers=UserTest.user_header
        )
        self.assertEqual(r.status_code, 400)

    # --- DELETE ---

    def test_delete_self_as_user(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        r = client.delete("/user", json={"user_id": UserTest.user_id}, headers=UserTest.user_header)
        self.assertEqual(r.status_code, 200)

    def test_delete_other_as_user(self, client: FlaskClient) -> None:
        user = UserModel(
            user_name="Ekhard Sorrell", user_pass="pia8eingief1Uv5gie7Cho4p", user_mail="ekhard.sorrell@example.com"
        )
        db.session.add(user)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            self.fail("Can not create second user: integrity constraint failed!")
        else:
            r = client.delete("/user", json={"user_id": user.user_id}, headers=UserTest.user_header)
            self.assertEqual(r.status_code, 403)
            db.session.delete(user)
            db.session.commit()

    def test_delete_id_type_str(self, client: FlaskClient) -> None:
        user_id = "aaa"
        r = client.delete("/user", json={"user_id": user_id}, headers=UserTest.user_header)
        self.assertEqual(r.status_code, 400)


class AdminTest(BaseTest):
    user_id = None
    user_name = "Willie Baldomero"
    user_mail = "willie.baldomero@example.com"
    user_pass = "eiZach2shoh4yo6kieBieFei"
    user_role = UserRole.Admin
    admin_header = BaseTest.base_header.copy()

    def setUp(self, client: FlaskClient) -> None:
        # create admin
        self.assertTrue(client is not None)
        self.assertTrue(isinstance(client, FlaskClient))
        user = UserModel(
            user_name=AdminTest.user_name,
            user_pass=AdminTest.user_pass,
            user_mail=AdminTest.user_mail,
            user_role=AdminTest.user_role,
        )
        with AdminTest.app.app_context():
            db.session.add(user)
            try:
                db.session.commit()
            except sqlalchemy.exc.IntegrityError as e:
                db.session.rollback()
                user = db.session.execute(db.select(UserModel).filter_by(user_mail=AdminTest.user_mail)).scalar_one()
            AdminTest.user_id = user.user_id
        self.assertTrue(AdminTest.user_id is not None)
        self.assertTrue(isinstance(AdminTest.user_id, int))
        # login admin
        r = client.post(
            "/login",
            json={"user_mail": AdminTest.user_mail, "user_pass": AdminTest.user_pass},
            headers=AdminTest.admin_header,
        )
        for cookie in client.cookie_jar:
            if cookie.name == AdminTest.app.config["JWT_ACCESS_CSRF_COOKIE_NAME"]:
                AdminTest.admin_header.update({AdminTest.app.config["JWT_ACCESS_CSRF_HEADER_NAME"]: cookie.value})

    def tearDown(self, client: FlaskClient) -> None:
        # logout admin
        # delete admin
        self.assertTrue(client is not None)
        self.assertTrue(isinstance(client, FlaskClient))
        with AdminTest.app.app_context():
            users = db.session.execute(db.select(UserModel)).scalars()
            for user in users:
                db.session.delete(user)
                db.session.commit()
        AdminTest.user_id = None

    # --- GET ---

    def test_get_existing_by_id(self, client: FlaskClient) -> None:
        self.assertTrue(AdminTest.user_id is not None)
        r = client.get(
            f"/user?user_id={AdminTest.user_id}&user_role={AdminTest.user_role.value}", headers=AdminTest.admin_header
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertIn(AdminTest.user_id, [d["user_id"] for d in r.json["data"]])

    def test_get_existing_by_name(self, client: FlaskClient) -> None:
        self.assertTrue(AdminTest.user_id is not None)
        r = client.get(
            f"/user?user_name={AdminTest.user_name}&user_role={AdminTest.user_role.value}",
            headers=AdminTest.admin_header,
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertIn(AdminTest.user_id, [d["user_id"] for d in r.json["data"]])

    def test_get_existing_by_mail(self, client: FlaskClient) -> None:
        self.assertTrue(AdminTest.user_id is not None)
        r = client.get(
            f"/user?user_mail={AdminTest.user_mail}&user_role={AdminTest.user_role.value}",
            headers=AdminTest.admin_header,
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertIn(AdminTest.user_id, [d["user_id"] for d in r.json["data"]])

    def test_get_existing_by_role(self, client: FlaskClient) -> None:
        self.assertTrue(AdminTest.user_id is not None)
        r = client.get(
            f"/user?user_role={AdminTest.user_role.value}",
            headers=AdminTest.admin_header,
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertIn(AdminTest.user_id, [d["user_id"] for d in r.json["data"]])

    def test_get_non_existing_by_id(self, client: FlaskClient) -> None:
        user_id = -1
        r = client.get(f"/user?user_id={user_id}&user_role={AdminTest.user_role.value}", headers=AdminTest.admin_header)
        self.assertEqual(r.status_code, 204)

    def test_get_non_existing_by_name(self, client: FlaskClient) -> None:
        user_name = "Does not exist"
        r = client.get(
            f"/user?user_name={user_name}&user_role={AdminTest.user_role.value}", headers=AdminTest.admin_header
        )
        self.assertEqual(r.status_code, 204)

    def test_get_non_existing_by_mail(self, client: FlaskClient) -> None:
        user_mail = "does.not.exist@example.com"
        r = client.get(
            f"/user?user_mail={user_mail}&user_role={AdminTest.user_role.value}", headers=AdminTest.admin_header
        )
        self.assertEqual(r.status_code, 204)

    def test_get_non_existing_by_role(self, client: FlaskClient) -> None:
        user_role = -1
        r = client.get(f"/user?user_role={user_role}", headers=AdminTest.admin_header)
        self.assertEqual(r.status_code, 400)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["message"], {"user_role": f"{user_role} is not a valid UserRole"})

    def test_get_restrict_page_size(self, client: FlaskClient) -> None:
        self.assertTrue(AdminTest.user_id is not None)
        user_limit = 1
        r = client.get(f"/user?user_role={AdminTest.user_role}&user_limit={user_limit}", headers=AdminTest.admin_header)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(user_limit, r.json["meta"]["page_size"])

    def test_get_page_index_zero(self, client: FlaskClient) -> None:
        self.assertTrue(AdminTest.user_id is not None)
        user_page = 0
        r = client.get(f"/user?user_id={AdminTest.user_id}&user_page={user_page}", headers=AdminTest.admin_header)
        self.assertEqual(r.status_code, 404)
        self.assertTrue(r.is_json)
        self.assertEqual(
            r.json["message"],
            "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
        )

    def test_get_user_pass(self, client: FlaskClient) -> None:
        self.assertTrue(AdminTest.user_id is not None)
        r = client.get(
            f"/user?user_id={AdminTest.user_id}&user_role={AdminTest.user_role.value}", headers=AdminTest.admin_header
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertNotIn("user_pass", r.json["data"][0].keys())

    # --- POST ---

    # --- PUT ---

    def test_put_admin_elevation_as_admin(self, client: FlaskClient) -> None:
        self.assertTrue(AdminTest.user_id is not None)
        user = UserModel("user_name", "user_pass", "user_mail")
        db.session.add(user)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            self.fail("Can not create second user: integrity constraint failed!")
        else:
            r = client.put(
                "/user",
                json={"user_id": user.user_id, "user_role": UserRole.Admin.value},
                headers=AdminTest.admin_header,
            )
            self.assertEqual(r.status_code, 200)
            self.assertTrue(r.is_json)
            self.assertEqual(r.json["message"], "Changed properties successfully")

    def test_put_sadmin_elevation_as_admin(self, client: FlaskClient) -> None:
        self.assertTrue(AdminTest.user_id is not None)
        r = client.put(
            "/user",
            json={"user_id": AdminTest.user_id, "user_role": UserRole.SAdmin.value},
            headers=AdminTest.admin_header,
        )
        self.assertEqual(r.status_code, 403)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["message"], "No Access")

    def test_put_demotion_as_admin(self, client: FlaskClient) -> None:
        self.assertTrue(AdminTest.user_id is not None)
        user = UserModel("user_name", "user_pass", "user_mail", UserRole.Admin)
        db.session.add(user)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            self.fail("Can not create second user: integrity constraint failed!")
        else:
            r = client.put(
                "/user",
                json={"user_id": user.user_id, "user_role": UserRole.User.value},
                headers=AdminTest.admin_header,
            )
            self.assertEqual(r.status_code, 200)
            self.assertTrue(r.is_json)
            self.assertEqual(r.json["message"], "Changed properties successfully")

    # --- DELETE ---

    def test_delete_non_existing(self, client: FlaskClient) -> None:
        user_id = -1
        r = client.delete("/user", json={"user_id": user_id}, headers=AdminTest.admin_header)
        self.assertEqual(r.status_code, 404)

    def test_delete_self_as_admin(self, client: FlaskClient) -> None:
        self.assertTrue(AdminTest.user_id is not None)
        r = client.delete("/user", json={"user_id": AdminTest.user_id}, headers=AdminTest.admin_header)
        self.assertEqual(r.status_code, 200)

    def test_delete_other_as_admin(self, client: FlaskClient) -> None:
        user = UserModel(
            user_name="Jarvey Ingelbert", user_pass="on9gai3Kie5ephohNg6eiRie", user_mail="jarvey.ingelbert@example.com"
        )
        db.session.add(user)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            self.fail("Can not create second user: integrity constraint failed!")
        else:
            r = client.delete(
                "/user?",
                json={"user_id": user.user_id},
                headers=AdminTest.admin_header,
            )
            self.assertEqual(r.status_code, 200)
            self.assertTrue(r.is_json)


if __name__ == "__main__":
    flask_unittest.main()
