from datetime import date


class Artist:
    __counter = 0

    def __init__(self, full_name, birth_date, country, rating=0.0):
        Artist.__counter += 1
        self.__artist_id = Artist.__counter
        self.full_name = full_name
        self.birth_date = birth_date
        self.country = country
        self.__rating = rating

    def __str__(self):
        return f"{self.__artist_id}. {self.full_name} ({self.country}), Rating: {self.__rating}"

    def update_rating(self, new_rating):
        if 0 <= new_rating <= 5:
            self.__rating = new_rating
        else:
            print("Рейтинг має бути в межах 0–5")

    def show_info(self):
        print(self)

    def get_rating(self):
        return self.__rating

    @staticmethod
    def total_artists():
        return Artist.__counter


class Painter(Artist):
    def __init__(self, full_name, birth_date, country, style, famous_work, rating=0.0):
        super().__init__(full_name, birth_date, country, rating)
        self.style = style
        self.famous_work = famous_work

    def __str__(self):
        return (super().__str__() +
                f" | Style: {self.style} | Famous work: '{self.famous_work}'")

    def paint(self, title):
        print(f"{self.full_name} is painting a new work titled '{title}'.")


class Critic:
    def __init__(self, critic_name, publication):
        self.critic_name = critic_name
        self.publication = publication

    def write_review(self, painting_title, rating, text):
        print(f"Critic {self.critic_name} rated '{painting_title}' {rating}/5.")
        print(f"Review: {text}")


class PaintingCritic(Painter, Critic):
    def __init__(self, full_name, birth_date, country, style, famous_work,
                 critic_name, publication, rating=0.0):
        Painter.__init__(self, full_name, birth_date, country, style, famous_work, rating)
        Critic.__init__(self, critic_name, publication)

    def __str__(self):
        return (Painter.__str__(self) +
                f" | Also a critic for '{self.publication}'")

    def review_self(self):
        print(f"{self.full_name} reviews their own painting '{self.famous_work}' "
              f"in {self.publication}.")


artist1 = Artist("Leonardo da Vinci", date(1452, 4, 15), "Italy", 5.0)
painter1 = Painter("Vincent van Gogh", date(1853, 3, 30), "Netherlands",
                    "Post-Impressionism", "Starry Night", 4.9)
critic_painter = PaintingCritic("John Smith", date(1980, 6, 10), "USA",
                                "Abstract", "Dream Shapes", "John Smith", "ArtDaily", 4.2)

artist1.show_info()
painter1.show_info()
critic_painter.show_info()

painter1.paint("Sunflowers II")
critic_painter.paint("Modern Vision")
critic_painter.write_review("Starry Night", 5, "A masterpiece full of emotion!")
critic_painter.review_self()

for a in [artist1, painter1, critic_painter]:
    a.show_info()

print(f"Total artists created: {Artist.total_artists()}")