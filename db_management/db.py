import os
from sqlite3 import connect
from contextlib import closing
import sqlite3

from PyQt5.QtWidgets import QMessageBox

from sys import stderr


def make_db_file(name, directory):
    try:
        sat_table = """
        CREATE TABLE IF NOT EXISTS sat_tests
        (
            datetime TEXT PRIMARY KEY NOT NULL,
            composite INTEGER NOT NULL,
            ebrw INTEGER NOT NULL,
            math INTEGER NOT NULL,
            hoa INTEGER,
            psda INTEGER,
            pam INTEGER,
            eoi INTEGER,
            sec INTEGER,
            wic INTEGER,
            coe INTEGER
        );
        """

        full_name = name + '.db'

        full_path = os.path.join(directory, full_name)

        with connect(full_path, uri=True) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(sat_table)
        
        return full_path

    except Exception as e:
        print(e, file=stderr)
        return None


def add_sat_score(database_url, params_dict, window):
    """
    Creates a record of an SAT practice test, taking
    in the following:
    * database_url - the path/link to the
    database being used
    * params_dict - a dictionary containing
    the following information on the SAT
    practice test:
        ---- Main Information ----
        + date and time taken (2021-10-22 16:00:00)
        + composite: Total score for SAT
        + ebrw: Section score for reading/writing section of SAT
        + math: Section score for math section of SAT
        ---- Subscores ----
        + hoa: SAT Heart of Algebra subscore
        + psda: SAT Problem Solving and Data Analysis subscore
        + pam: SAT Passport to Advanced Math subscore
        + eoi: SAT subscore for Expression of Ideas
        + sec: SAT subscore for Standard English Conventions
        + wic: SAT subscore for Words in Context
        + coe: SAT subscore for Command of Evidence
    """

    try:
        stmt = """
        INSERT INTO sat_tests (datetime,
        composite, ebrw, math, hoa, psda,
        pam, eoi, sec, wic, coe)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        params = [
            params_dict['datetime'],
            params_dict['composite'],
            params_dict['ebrw'],
            params_dict['math'],
            params_dict['hoa'],
            params_dict['psda'],
            params_dict['pam'],
            params_dict['eoi'],
            params_dict['sec'],
            params_dict['wic'],
            params_dict['coe']
        ]

        db_url = "file:{}?mode=rw".format(database_url)

        with connect(db_url, uri=True) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(stmt, params)

                QMessageBox.about(window, "Success!", "SAT successfully added!")

    except sqlite3.IntegrityError:
        QMessageBox.about(window, "Error!", "Date and time must be unique!")

    except Exception as ex:
        print(ex, file=stderr)
        QMessageBox.about(window, "Error!", "An unknown error has occurred!")


def get_sat_data(database_url, window):
    try:
        stmt = """
        SELECT * FROM sat_tests
        ORDER BY datetime ASC;
        """

        with connect(database_url, uri=True) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(stmt)

                row = cursor.fetchone()

                data_dict = {
                    'dates': [],
                    'composite': [],
                    'ebrw': [],
                    'math': [],
                    'hoa': [],
                    'psda': [],
                    'pam': [],
                    'eoi': [],
                    'sec': [],
                    'wic': [],
                    'coe': []
                }

                while row is not None:
                    datetime = str(row[0])
                    composite = int(row[1])
                    ebrw = int(row[2])
                    math = int(row[3])
                    hoa = int(row[4])
                    psda = int(row[5])
                    pam = int(row[6])
                    eoi = int(row[7])
                    sec = int(row[8])
                    wic = int(row[9])
                    coe = int(row[10])

                    data_dict['dates'].append(datetime)
                    data_dict['composite'].append(composite)
                    data_dict['ebrw'].append(ebrw)
                    data_dict['math'].append(math)
                    data_dict['hoa'].append(hoa)
                    data_dict['psda'].append(psda)
                    data_dict['pam'].append(pam)
                    data_dict['eoi'].append(eoi)
                    data_dict['sec'].append(sec)
                    data_dict['wic'].append(wic)
                    data_dict['coe'].append(coe)

                    row = cursor.fetchone()
        
        return data_dict

                
    except Exception as ex:
        print(ex, file=stderr)
        QMessageBox.about(window, "Error!", "An unknown error has occurred!")


def delete_sat(database_url, window, date_time):
    try:
        stmt = """
        DELETE FROM sat_tests
        WHERE datetime = ?;
        """

        with connect(database_url, uri=True) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(stmt, [date_time])
                
    except Exception as ex:
        print(ex, file=stderr)
        QMessageBox.about(window, "Error!", "An unknown error has occurred!")
