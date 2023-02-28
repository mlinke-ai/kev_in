#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Kev.in - a coding learning platform
# Copyright (C) 2022  Max Linke
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

import unittest

import requests


class UserTest(unittest.TestCase):
    users = [
        ("Warrener Hamnett", "aj0Uk", "Warrener.Hamnett@example.com"),
        ("Bittan Myrl", "sai6X", "Bittan.Myrl@example.com"),
        ("Albert Ferdynand", "AeM6u", "Albert.Ferdynand@example.com"),
        ("Rolland Heinz", "jah2J", "Rolland.Heinz@example.com"),
        ("Kueffner Caedon", "kae5A", "Kueffner.Caedon@example.com"),
        ("Aldous Alphonso", "ii8aH", "Aldous.Alphonso@example.com"),
        ("Ellary Alan", "Axao6", "Ellary.Alan@example.com"),
        ("Curt Ludo", "eay6B", "Curt.Ludo@example.com"),
        ("Freddie Errol", "Tahv4", "Freddie.Errol@example.com"),
        ("Siegmund Stearne", "ma5oZ", "Siegmund.Stearne@example.com"),
    ]
    user_ids = list()

    @classmethod
    def setUpClass(cls) -> None:
        cls.content_header = {"Content-Type": "application/json"}
        for user_name, user_pass, user_mail in cls.users:
            r = requests.request(
                "POST",
                "http://127.0.0.1:5000/user",
                json={
                    "user_name": user_name,
                    "user_pass": user_pass,
                    "user_mail": user_mail,
                },
                headers=cls.content_header,
            )
            cls.user_ids.append(r.json()["user_id"])
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/login",
            json={"user_mail": "sadmin@example.com", "user_pass": "sadmin"},
            headers=cls.content_header,
        )
        cls.sadmin_header = cls.content_header.copy()
        cls.sadmin_header.update({"Cookie": r.headers["Set-Cookie"]})
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/login",
            json={"user_mail": "tuser@example.com", "user_pass": "tuser"},
            headers=cls.content_header,
        )
        cls.tuser_header = cls.content_header.copy()
        cls.tuser_header.update({"Cookie": r.headers["Set-Cookie"]})

    @classmethod
    def tearDownClass(cls) -> None:
        for user_id in cls.user_ids:
            if user_id != 0:
                requests.request(
                    "DELETE",
                    "http://127.0.0.1:5000/user",
                    json={"user_id": user_id},
                    headers=cls.sadmin_header,
                )

    # --- GET ---

    def test_get_existing_by_id(self) -> None:
        r = requests.request(
            "GET",
            "http://127.0.0.1:5000/user?user_id=2",
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["2"]["user_id"], 2)

    def test_get_existing_by_name(self) -> None:
        r = requests.request(
            "GET",
            "http://127.0.0.1:5000/user?user_name=tuser",
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["2"]["user_name"], "tuser")

    def test_get_existing_by_mail(self) -> None:
        r = requests.request(
            "GET",
            "http://127.0.0.1:5000/user?user_mail=tuser@example.com",
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["2"]["user_mail"], "tuser@example.com")

    def test_get_existing_by_role(self) -> None:
        r = requests.request(
            "GET",
            "http://127.0.0.1:5000/user?user_role=3",
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["2"]["user_role"], "User")

    def test_get_non_existing_by_id(self) -> None:
        r = requests.request(
            "GET",
            "http://127.0.0.1:5000/user?user_id=-1",
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 204)
        self.assertEqual(r.json(), {})

    def test_get_non_existing_by_name(self) -> None:
        r = requests.request(
            "GET",
            "http://127.0.0.1:5000/user?user_name=nuser",
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 204)
        self.assertEqual(r.json(), {})

    def test_get_non_existing_by_mail(self) -> None:
        r = requests.request(
            "GET",
            "http://127.0.0.1:5000/user?user_mail=nuser@example.com",
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 204)
        self.assertEqual(r.json(), {})

    def test_get_non_existing_by_role(self) -> None:
        r = requests.request(
            "GET",
            "http://127.0.0.1:5000/user?user_role=4",
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), {"message": {"user_role": "4 is not a valid UserRole"}})

    def test_get_restrict_page_size(self) -> None:
        r = requests.request(
            "GET",
            "http://127.0.0.1:5000/user?user_limit=5",
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 5)

    # --- POST ---

    def test_create_user(self) -> None:
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": "Josslin Aloj",
                "user_mail": "Josslin.Aloj@example.com",
                "user_pass": "ian80",
            },
            headers=UserTest.sadmin_header,
        )
        UserTest.user_ids.append(r.json()["user_id"])
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "The user was created successfully")

    def test_create_admin(self) -> None:
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": "Thurmon Uli",
                "user_mail": "Thurmon.Uli@example.com",
                "user_pass": "Pi5ta",
                "user_role": 2,
            },
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()["message"], "Unknown arguments: user_role")

    def test_create_user_without_token(self) -> None:
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": "Kon Archy",
                "user_mail": "Kon.Archy@example.com",
                "user_pass": "Fip5k",
            },
            headers=UserTest.content_header,
        )
        UserTest.user_ids.append(r.json()["user_id"])
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "The user was created successfully")

    def test_create_duplicate_user(self) -> None:
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": "Geoffrey Tretan",
                "user_mail": "Geoffrey.Tretan@example.com",
                "user_pass": "Abeo0",
            },
            headers=UserTest.sadmin_header,
        )
        UserTest.user_ids.append(r.json()["user_id"])
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "The user was created successfully")
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": "Geoffrey Tretan",
                "user_mail": "Geoffrey.Tretan@example.com",
                "user_pass": "Abeo0",
            },
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 409)
        self.assertEqual(r.json()["message"], "A user with this mail already exists")

    def test_create_user_with_empty_name(self) -> None:
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": "",
                "user_mail": "Gofried.Dietbald@example.com",
                "user_pass": "koh6P",
            },
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()["message"], "user_name must not be empty")

    def test_create_user_with_empty_mail(self) -> None:
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={"user_name": "Rane Loewe", "user_mail": "", "user_pass": "Lohw3"},
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()["message"], "user_mail must not be empty")

    def test_create_user_with_empty_password(self) -> None:
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": "Pepin Kuefer",
                "user_mail": "Pepin.Kuefer@example.com",
                "user_pass": "",
            },
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()["message"], "user_pass must not be empty")

    def test_create_user_with_long_name(self) -> None:
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
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": long_name,
                "user_mail": "long.mail@example.com",
                "user_pass": "Eiph9",
            },
            headers=UserTest.sadmin_header,
        )
        UserTest.user_ids.append(r.json()["user_id"])
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "The user was created successfully")
        self.assertEqual(r.json()["user_name"], long_name)

    def test_create_user_with_strange_name(self) -> None:
        strange_name = "⚗〠ൠᴥ௵ஔ∰ጃ෴ᅘ༽໒✺"
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": strange_name,
                "user_mail": "strange.mail@example.com",
                "user_pass": "ai2Ou",
            },
            headers=UserTest.sadmin_header,
        )
        UserTest.user_ids.append(r.json()["user_id"])
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "The user was created successfully")
        self.assertEqual(r.json()["user_name"], strange_name)

    # --- PUT ---

    def test_change_mail_to_existing(self) -> None:
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": "Aurick Kyland",
                "user_mail": "double.mail@example.com",
                "user_pass": "Hua4e",
            },
            headers=UserTest.sadmin_header,
        )
        UserTest.user_ids.append(r.json()["user_id"])
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "The user was created successfully")
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": "Bogohardt Fredrik",
                "user_mail": "unique.mail@example.com",
                "user_pass": "Tae0U",
            },
            headers=UserTest.sadmin_header,
        )
        UserTest.user_ids.append(r.json()["user_id"])
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "The user was created successfully")
        user_id = r.json()["user_id"]
        r = requests.request(
            "PUT",
            "http://127.0.0.1:5000/user",
            json={"user_id": user_id, "user_mail": "double.mail@example.com"},
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 409)
        self.assertEqual(r.json()["message"], "A user with this mail already exists")

    def test_change_to_empty_name(self) -> None:
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": "Amell Hernando",
                "user_mail": "Amell.Hernando@example.com",
                "user_pass": "iHoh6",
            },
            headers=UserTest.sadmin_header,
        )
        UserTest.user_ids.append(r.json()["user_id"])
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "The user was created successfully")
        user_id = r.json()["user_id"]
        r = requests.request(
            "PUT",
            "http://127.0.0.1:5000/user",
            json={"user_id": user_id, "user_name": ""},
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()["message"], "user_name must not be empty")

    def test_change_to_empty_mail(self) -> None:
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": "Heinie Barnie",
                "user_mail": "Heinie.Barnie@example.com",
                "user_pass": "Lief9",
            },
            headers=UserTest.sadmin_header,
        )
        UserTest.user_ids.append(r.json()["user_id"])
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "The user was created successfully")
        user_id = r.json()["user_id"]
        r = requests.request(
            "PUT",
            "http://127.0.0.1:5000/user",
            json={"user_id": user_id, "user_mail": ""},
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()["message"], "user_mail must not be empty")

    def test_change_to_empty_password(self) -> None:
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": "Alfonso Hamlen",
                "user_mail": "Alfonso.Hamlen@example.com",
                "user_pass": "ahS7e",
            },
            headers=UserTest.sadmin_header,
        )
        UserTest.user_ids.append(r.json()["user_id"])
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "The user was created successfully")
        user_id = r.json()["user_id"]
        r = requests.request(
            "PUT",
            "http://127.0.0.1:5000/user",
            json={"user_id": user_id, "user_pass": ""},
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()["message"], "user_pass must not be empty")

    def test_change_admin_elevation_as_user(self) -> None:
        r = requests.request(
            "PUT",
            "http://127.0.0.1:5000/user",
            json={"user_id": 2, "user_role": 2},
            headers=UserTest.tuser_header,
        )
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.json()["message"], "No Access")

    def test_change_sadmin_elevation_as_user(self) -> None:
        r = requests.request(
            "PUT",
            "http://127.0.0.1:5000/user",
            json={"user_id": 2, "user_role": 1},
            headers=UserTest.tuser_header,
        )
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.json()["message"], "No Access")

    def test_change_admin_elevation_as_admin(self) -> None:
        r = requests.request(
            "PUT", "http://127.0.0.1:5000/user", json={"user_id": 3, "user_role": 2}, headers=UserTest.sadmin_header
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["message"], "Changed properties successfully")

    def test_change_sadmin_elevation_as_admin(self) -> None:
        r = requests.request(
            "PUT", "http://127.0.0.1:5000/user", json={"user_id": 4, "user_role": 1}, headers=UserTest.sadmin_header
        )
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.json()["message"], "No Access")

    def test_change_user_demotion_as_user(self) -> None:
        r = requests.request(
            "PUT", "http://127.0.0.1:5000/user", json={"user_id": 1, "user_role": 3}, headers=UserTest.tuser_header
        )
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.json()["message"], "No Access")

    def test_change_user_demotion_as_admin(self) -> None:
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": "Markos Court",
                "user_mail": "Markos.Court@example.com",
                "user_pass": "eij0N",
            },
            headers=UserTest.sadmin_header,
        )
        user_id = r.json()["user_id"]
        UserTest.user_ids.append(user_id)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "The user was created successfully")
        r = requests.request(
            "PUT",
            "http://127.0.0.1:5000/user",
            json={"user_id": user_id, "user_role": 2},
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["message"], "Changed properties successfully")
        r = requests.request(
            "PUT",
            "http://127.0.0.1:5000/user",
            json={"user_id": user_id, "user_role": 3},
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["message"], "Changed properties successfully")

    # --- DELETE ---

    def test_delete_existing(self) -> None:
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": "Eberhart Rhinebeck",
                "user_mail": "Eberhart.Rhinebeck@example.com",
                "user_pass": "FoKa9",
            },
            headers=UserTest.sadmin_header,
        )
        UserTest.user_ids.append(r.json()["user_id"])
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "The user was created successfully")
        user_id = r.json()["user_id"]
        r = requests.request(
            "DELETE",
            "http://127.0.0.1:5000/user",
            json={"user_id": user_id},
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["message"], f"Successfully deleted user with user_id {user_id}")

    def test_delete_non_existing(self) -> None:
        user_id = 5000
        r = requests.request(
            "DELETE",
            "http://127.0.0.1:5000/user",
            json={"user_id": user_id},
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.json()["message"], f"User with user_id {user_id} does not exist")

    def test_delete_self_as_admin(self) -> None:
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": "Allcen Mila",
                "user_mail": "Allcen.Mila@example.com",
                "user_pass": "yae7C",
            },
            headers=UserTest.sadmin_header,
        )
        user_id = r.json()["user_id"]
        UserTest.user_ids.append(user_id)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "The user was created successfully")
        r = requests.request(
            "PUT",
            "http://127.0.0.1:5000/user",
            json={"user_id": user_id, "user_role": 2},
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["message"], "Changed properties successfully")
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/login",
            json={"user_mail": "Allcen.Mila@example.com", "user_pass": "yae7C"},
            headers=UserTest.content_header,
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["message"], "Welcome Allcen Mila!")
        header = UserTest.content_header.copy()
        header.update({"Cookie": r.headers["Set-Cookie"]})
        r = requests.request("DELETE", "http://127.0.0.1:5000/user", json={"user_id": user_id}, headers=header)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["message"], f"Successfully deleted user with user_id {user_id}")

    def test_delete_self_as_user(self) -> None:
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": "Freddie Selig",
                "user_mail": "Freddie.Selig@example.com",
                "user_pass": "Ufe0o",
            },
            headers=UserTest.sadmin_header,
        )
        UserTest.user_ids.append(r.json()["user_id"])
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "The user was created successfully")
        user_id = r.json()["user_id"]
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/login",
            json={"user_mail": "Freddie.Selig@example.com", "user_pass": "Ufe0o"},
            headers=UserTest.content_header,
        )
        user_header = UserTest.content_header.copy()
        user_header.update({"Cookie": r.headers["Set-Cookie"]})
        r = requests.request(
            "DELETE",
            "http://127.0.0.1:5000/user",
            json={"user_id": user_id},
            headers=user_header,
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["message"], f"Successfully deleted user with user_id {user_id}")

    def test_delete_other_as_admin(self) -> None:
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": "Hamblin Adie",
                "user_mail": "Hamblin.Adie@example.com",
                "user_pass": "zis4X",
            },
            headers=UserTest.sadmin_header,
        )
        UserTest.user_ids.append(r.json()["user_id"])
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "The user was created successfully")
        user_id = r.json()["user_id"]
        r = requests.request(
            "DELETE",
            "http://127.0.0.1:5000/user",
            json={"user_id": user_id},
            headers=UserTest.sadmin_header,
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["message"], f"Successfully deleted user with user_id {user_id}")

    def test_delete_other_as_user(self) -> None:
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": "Dusty Eberle",
                "user_mail": "Dusty.Eberle@example.com",
                "user_pass": "Ahg9k",
            },
            headers=UserTest.sadmin_header,
        )
        UserTest.user_ids.append(r.json()["user_id"])
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "The user was created successfully")
        user_id = 1
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/login",
            json={"user_mail": "Dusty.Eberle@example.com", "user_pass": "Ahg9k"},
            headers=UserTest.content_header,
        )
        user_header = UserTest.content_header.copy()
        user_header.update({"Cookie": r.headers["Set-Cookie"]})
        r = requests.request(
            "DELETE",
            "http://127.0.0.1:5000/user",
            json={"user_id": user_id},
            headers=user_header,
        )
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.json()["message"], "No Access")


if __name__ == "__main__":
    unittest.main()
