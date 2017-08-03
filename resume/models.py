from resume import *


def extension(filename):
    return '.' + filename.split('.')[-1].lower()


@Session.model_mixin
class User:
    about_me = Column(UnicodeText, default="The rest is still unwritten.")
    contact_items = relationship('ContactItem', backref='user')
    job_experiences = relationship('JobExperience', backref='user')
    life_experiences = relationship('LifeExperience', backref='user')
    hobbies = relationship('Hobby', backref='user')
    languages = relationship('Language', backref='user')
    skills = relationship('Skill', backref='user')
    pic_filename = Column(UnicodeText)
    pic_content_type = Column(UnicodeText)

    @property
    def pic_url(self):
        return '../bands/view_bio_pic?id={}'.format(self.band.id) if self.uploaded_pic else ''

    @property
    def pic_fpath(self):
        return os.path.join(resume_config['root'], 'resume', 'static', 'images', 'bio_pics', self.id) + self.pic_extension

    @property
    def pic_src(self):
        return c.URL_BASE + '/' + os.path.join('static', 'images', 'bio_pics', self.id) + self.pic_extension

    @property
    def uploaded_pic(self):
        return os.path.exists(self.pic_fpath)

    @property
    def pic_extension(self):
        return extension(self.pic_filename)

    @property
    def download_filename(self):
        return self.user.full_name + "_bio_pic." + self.pic_extension

class ContactItem(MainModel):
    name = Column(UnicodeText)
    link = Column(UnicodeText)
    description = Column(UnicodeText)
    icon = Column(UnicodeText, default="link")
    user_id = Column(UUID, ForeignKey('user.id'))

    @property
    def display_name(self):
        return "%s - %s" % (self.name, self.description)


class JobExperience(MainModel):
    name = Column(UnicodeText)
    link = Column(UnicodeText)
    description = Column(UnicodeText)
    icon = Column(UnicodeText, default="link")
    user_id = Column(UUID, ForeignKey('user.id'))
    start_date = Column(Date)
    end_date = Column(Date, default=None, nullable=True)
    job_title = Column(UnicodeText)

    @property
    def display_name(self):
        return "%s - %s" % (self.name, self.description)


class LifeExperience(MainModel):
    name = Column(UnicodeText)
    description = Column(UnicodeText)
    icon = Column(UnicodeText, default="link")
    user_id = Column(UUID, ForeignKey('user.id'))
    date = Column(Date, default=datetime.now(UTC))

    @property
    def display_name(self):
        return "%s - %s" % (self.name, self.date)

    @property
    def year(self):
        return self.date.year

    @presave_adjustment
    def _misc_adjustments(self):
        if self.date == '':
            self.date = None


class Hobby(MainModel):
    name = Column(UnicodeText)
    user_id = Column(UUID, ForeignKey('user.id'))

    @property
    def display_name(self):
        return "%s" % (self.name)


class Language(MainModel):
    name = Column(UnicodeText)
    user_id = Column(UUID, ForeignKey('user.id'))
    level = Column(Integer, default=99)


class Skill(MainModel):
    name = Column(UnicodeText)
    user_id = Column(UUID, ForeignKey('user.id'))
    level = Column(Integer, default=99)

    @property
    def display_name(self):
        return "%s - %s" % (self.name, self.level)