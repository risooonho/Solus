from nose.tools import *
from solus.game import *

def test_player_fight_win():
    player = Player('NAME', 3)
    alien = Alien('GLOOB', 1)
    fight(player, alien)
    assert_equal(player.is_alive, True)
    assert_equal(alien.is_alive, False)
    player2 = Player('NAME2', 3)
    alien2 = Alien('GLOOB2', 1)
    fight(alien2, player2)
    assert_equal(player2.is_alive, True)
    assert_equal(alien2.is_alive, False)

def test_player_fight_lose():
    player = Player('NAME', 1)
    alien = Alien('GLOOB', 3)
    fight(player, alien)
    assert_equal(player.is_alive, False)
    assert_equal(alien.is_alive, True)
    player2 = Player('NAME2', 1)
    alien2 = Alien('GLOOB2', 3)
    fight(player2, alien2)
    assert_equal(player2.is_alive, False)
    assert_equal(alien2.is_alive, True)    
