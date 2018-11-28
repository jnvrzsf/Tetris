import pygame
import game
import leaderboard
from utility import Colors, Fonts, Actions

def main():

    pygame.init()
    pygame.display.set_caption("Tetris")
    pygame.key.set_repeat(150, 30)

    window = pygame.display.set_mode((400, 600))
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # S - start
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    # settings
                    settings_screen = game.SettingsScreen()
                    action = settings_screen.show()
                    if action == Actions.QUIT:
                        pygame.quit()
                        return
                    elif action == Actions.CANCEL:
                        continue

                    # game screen
                    game_model = game.GameModel(settings_screen.width,settings_screen.height)
                    game_screen = game.GameScreen(game_model)
                    action = game_screen.show()
                    if action == Actions.QUIT:
                        pygame.quit()
                        return
                
                    # name entry
                    name_entry_screen = leaderboard.NameEntryScreen()
                    action = name_entry_screen.show()
                    if action == Actions.QUIT:
                        pygame.quit()
                        return
                    elif action == Actions.CANCEL:
                        continue

                    # leaderboard
                    leaderboard_model = leaderboard.LeaderboardModel("ranglista.txt")
                    leaderboard_model.record_score(game_model.score, name_entry_screen.name)
                    leaderboard_screen = leaderboard.LeaderboardScreen(leaderboard_model)
                    action = leaderboard_screen.show()
                    if action == Actions.QUIT:
                        pygame.quit()
                        return
                    elif action == Actions.CANCEL:
                        continue

                # L - leaderboard
                elif event.key == pygame.K_l: 
                    leaderboard_model = leaderboard.LeaderboardModel("ranglista.txt")
                    leaderboard_screen = leaderboard.LeaderboardScreen(leaderboard_model)
                    action = leaderboard_screen.show()
                    if action == Actions.QUIT:
                        pygame.quit()
                        return
                    elif action == Actions.CANCEL:
                        continue

                # ESC - quit
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        window.fill(Colors.WHITE.value)

        # title, menu
        title = Fonts.BIGTITLE.value.render("TETRIS", False, Colors.BLUE.value)
        window.blit(title, (window.get_width() // 2 - title.get_width() // 2, 100))

        start_text = Fonts.SMALL.value.render("START (S)", False, Colors.PINK.value)
        window.blit(start_text, (window.get_width() // 2 - start_text.get_width() // 2, window.get_height() // 2))

        leaderboard_text = Fonts.SMALL.value.render("LEADERBOARD (L)", False, Colors.PINK.value)
        window.blit(leaderboard_text, (window.get_width() // 2 - leaderboard_text.get_width() // 2, window.get_height() // 2 + start_text.get_height() * 4))
        
        escape_text = Fonts.SMALL.value.render("QUIT (ESC)", False, Colors.PINK.value)
        window.blit(escape_text, (window.get_width() // 2 - escape_text.get_width() // 2, window.get_height() // 2 + start_text.get_height() * 8))
        
        pygame.display.update()

        clock.tick(60)
    
if __name__ == "__main__":
    main()
