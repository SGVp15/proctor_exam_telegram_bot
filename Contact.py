import datetime
import random
import hashlib
from translit import transliterate, transliterate_error


class Contact:
    def __init__(self):
        self.NameEng = None
        self.lastName = None
        self.firstName = None
        self.lastNameEng = None
        self.firstNameEng = None
        self.email = None
        self.username = None
        self.password = None
        self.exam = None
        self.course = None
        self.course_small = None
        self.lector = None
        self.date_from_file = None
        self.dateExam = None
        self.dateExamConnect = None
        self.removeAt = None
        self.deadline = None
        self.scheduledAt = None
        self.proctor = None
        self.subject = None
        self.dateExamForSubject = None
        self.url_proctor = None
        self.url_course = None
        self.id_ispring = None
        self.identifier = None
        self.is_create_enrollment: bool = False

    def normalize(self) -> bool:
        if self.firstNameEng == '':
            self.firstNameEng = transliterate(f'{self.firstName}').capitalize()
        else:
            self.firstNameEng = transliterate_error(self.firstNameEng)

        if self.lastNameEng == '':
            self.lastNameEng = transliterate(f'{self.lastName}').capitalize()
        else:
            self.lastNameEng = transliterate_error(self.lastNameEng)

        self.email = transliterate_error(self.email.strip())

        self.NameEng = f'{self.firstNameEng} {self.lastNameEng}'

        if datetime.datetime.now() > self.dateExam:
            return False

        self.dateExamConnect = self.dateExam - datetime.timedelta(minutes=5)
        self.scheduledAt = self.dateExam + datetime.timedelta(hours=-3)
        deadline = self.scheduledAt + datetime.timedelta(hours=2)
        remove_at = self.scheduledAt + datetime.timedelta(days=90)

        pattern_time = "%Y-%m-%dT%H:%M:%SZ"
        self.dateExamForSubject = self.dateExam.strftime(pattern_time)
        self.deadline = deadline.strftime(pattern_time)
        self.removeAt = remove_at.strftime(pattern_time)

        self.username = self.NameEng.replace(' ', '_')

        if self.proctor == '':
            self.proctor = None

        if self.password == '':
            self.password = f'{self.username}_{random.randint(1000, 9999)}'

        self.subject = f'{self.dateExamForSubject}_{self.username}_' \
                       f'{self.exam}_proctor-{self.proctor}'
        self.identifier = to_md5(f'{self.date_from_file.replace(".", "-")}_{self.username}_{self.exam}')
        return True

    def __str__(self) -> str:
        self.s = f'{datetime.datetime.now()}\tsubject={self.subject}\t' \
                 f'lastName={self.lastName}\tfirstName={self.firstName}\t' \
                 f'email={self.email}\tusername={self.username}\tpassword={self.password}\t' \
                 f'url={self.url_proctor}\n'
        return self.s


def to_md5(s: str):
    return hashlib.md5(s.encode()).hexdigest()
