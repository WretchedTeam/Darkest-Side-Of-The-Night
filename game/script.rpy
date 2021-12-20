# Script.rpy
# This is the main script that DDLC/Ren'Py calls upon to start
# your mod's story!

label start:

    # Configures your mod to use a ID to prevent users from cheating.
    # Leave this as default and only change the value 'persistent.anticheat' has
    # in definitions.rpy if you want to change it
    $ anticheat = persistent.anticheat

    # Controls what chapter the game starts for the poem game.
    $ chapter = 0

    # This makes sure if the user quits during pause,
    # it is set to false after restarting the game. Precaution.
    $ _dismiss_pause = config.developer

    # Names of the Characters
    # To add a character -> $ mi_name = "Mike". Don't forget to
    # add them also in definitions.rpy!
    $ s_name = "Sayori"
    $ m_name = "Monika"
    $ n_name = "Natsuki"
    $ y_name = "Yuri"

    # Controls whether we have a menu in the textbox or not.
    $ quick_menu = True

    # Controls whether Sayori is dead. Leave this alone unless needed.
    $ in_sayori_kill = None

    # Controls whether we allow skipping dialogue.
    $ allow_skipping = True
    $ config.allow_skipping = True

    # Start of the script
    call test_start


# the end label of the game. Not the credits.
label endgame(pause_length=4.0):
    $ quick_menu = False
    stop music fadeout 2.0
    scene black
    show end
    with dissolve_scene_full
    pause pause_length
    $ quick_menu = True
    return
