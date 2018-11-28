import pygame
import os.path
import game
from utility import Colors, Fonts, Actions


class Record:
    def __init__(self, score, name):
        self.score = score
        self.name = name

class LeaderboardModel:
    def __init__(self, filename):
        self.filename = filename
        self.records = self.read_records()

    def record_score(self, score, name):
        # fájlhoz hozzáadás
        with open(self.filename, "at") as f:
            f.write("{}\t{}\n".format(score, name))
        # listához hozzáadás
        new_record = Record(score, name)
        for i in range(len(self.records)):
            if new_record.score >= self.records[i].score:
                self.records.insert(i, new_record)
                return
        self.records.append(new_record)

    def read_records(self):
        records = []
        if os.path.exists(self.filename):
            with open(self.filename, "rt") as f:
                for line in f:
                    line = line.rstrip("\n")
                    score, name = line.split("\t")
                    records.append(Record(int(score), name))
            records.sort(key=lambda record: record.score, reverse=True) # key - fv-t vár, lambda definiál egy anoním fv-t, megkapja: record paramétert, visszaadja: record.score-t
        return records

class LeaderboardScreen:
    def __init__(self, model):
        self.model = model

    def show(self):
        window = pygame.display.set_mode((400, 600))

        clock = pygame.time.Clock()

        page = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return Actions.QUIT
                elif event.type == pygame.KEYDOWN:
                    # go to next page
                    if event.key == pygame.K_DOWN and page < len(self.model.records) // 10:
                        page += 1
                    # go to previous page
                    elif event.key == pygame.K_UP and page > 0:
                        page -= 1
                    # ESC - back to menu
                    elif event.key == pygame.K_ESCAPE: 
                        return Actions.CANCEL

            window.fill(Colors.WHITE.value)

            # title, subtitle
            title = Fonts.SMALLTITLE.value.render("LEADERBOARD", False, Colors.BLUE.value)
            window.blit(title, (window.get_width() // 2 - title.get_width() // 2, window.get_height() // 5 - title.get_height() // 2))
            
            subtitle = Fonts.SMALL.value.render("{:4} {:^10}{:^10}".format("rank", "name", "score"), False, Colors.PINK.value)
            window.blit(subtitle, (window.get_width() // 2 - subtitle.get_width() // 2, window.get_height() // 2.5 - subtitle.get_height() // 2))

            # leaderboard
            y = 0
            # rank/page: 1-10, 11-20, ... -> i: 0-9, 10-19, ...
            for i in range(max(0, page * 10), min((page + 1) * 10, len(self.model.records))):
                line = Fonts.SMALL.value.render("{:4} {:10}{:10}".format(i + 1, self.model.records[i].name, self.model.records[i].score), False, Colors.BLACK.value)
                window.blit(line, (window.get_width() // 2 - line.get_width() // 2, window.get_height() // 2.25 - line.get_height() // 2 + y))
                y += line.get_height()

            # arrows
            arrows = pygame.transform.rotate(Fonts.SMALL.value.render("< >", False, Colors.PURPLE.value), 90)
            window.blit(arrows, (window.get_width() // 2 - arrows.get_width() // 2, window.get_height() // 5 * 4))

            # esc
            esc = Fonts.SMALL.value.render("< ESC", False, Colors.BLACK.value)
            window.blit(esc, (10, window.get_height() - esc.get_height() - 10))

            pygame.display.update()

            clock.tick(60)

class NameEntryScreen:
    def __init__(self):
        self.name = ""

    def show(self):
        window = pygame.display.set_mode((400, 600))

        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return Actions.QUIT
                elif event.type == pygame.KEYDOWN:
                    # input character
                    if event.unicode.isprintable() and len(self.name) < 10:
                        self.name += event.unicode
                    # delete character
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    elif event.key == pygame.K_RETURN and self.name != "":
                        return Actions.OK
                    elif event.key == pygame.K_ESCAPE:
                        return Actions.CANCEL

            window.fill(Colors.WHITE.value)

            # title
            title = Fonts.BIGTITLE.value.render("NAME?", False, Colors.BLUE.value)
            window.blit(title, (window.get_width() // 2 - title.get_width() // 2, window.get_height() // 4 - title.get_height() // 2))

            # name field
            name_entry = Fonts.SMALL.value.render("{:<10}".format(self.name), False, Colors.PINK.value, Colors.BLACK.value)
            window.blit(name_entry, (window.get_width() // 2 - name_entry.get_width() // 2, window.get_height() // 2 - name_entry.get_height() // 2))

            # esc, enter
            esc = Fonts.SMALL.value.render("< ESC", False, Colors.BLACK.value)
            window.blit(esc, (10, window.get_height() - esc.get_height() - 10))

            enter = Fonts.SMALL.value.render("ENTER >", False, Colors.BLACK.value)
            window.blit(enter, (window.get_width() - enter.get_width() - 10, window.get_height() - esc.get_height() - 10))

            pygame.display.update()

            clock.tick(60)
