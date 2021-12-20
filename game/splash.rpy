## Splash.rpy

# Checks to see if all of DDLC's files are inside for PC
# You may remove 'scripts' if you recieve conflict with scripts.rpa
## Note: For building a mod for PC/Android, you must keep the DDLC RPAs 
## and decompile them for the builds to work.
init -100 python:
    if not renpy.android:
        for archive in ['audio','images','fonts']:
            if archive not in config.archives:
                renpy.error("DDLC archive files not found in /game folder. Check your installation and try again.")

# Splash Message
init python:
    menu_trans_time = 1
    # Default message everyone sees in the game
    splash_message_default = "This game is an unofficial fan game, unaffiliated with Team Salvato."
    # Used sometimes to change splash messages if called upon
    splash_messages = [
        "Please support Doki Doki Literature Club.",
        "Monika is watching you code."
    ]

image splash_warning = ParameterizedText(style="splash_text", xalign=0.5, yalign=0.5)
image splash_nosignal = ParameterizedText(style="splash_text", xalign=0.5, yalign=0.5, size=48)

# Main Menu Images
image menu_logo:
    "/mod_assets/DDLCModTemplateLogo.png"
    subpixel True
    xcenter 240
    ycenter 120
    zoom 0.60
    menu_logo_move

image menu_bg:
    topleft
    "gui/menu_bg.png"
    menu_bg_move

image game_menu_bg:
    topleft
    "gui/menu_bg.png"
    menu_bg_loop

image menu_fade:
    "white"
    menu_fadeout

image menu_art_y:
    subpixel True
    "gui/menu_art_y.png"
    xcenter 600
    ycenter 335
    zoom 0.60
    menu_art_move(0.54, 600, 0.60)

image menu_art_n:
    subpixel True
    "gui/menu_art_n.png"
    xcenter 750
    ycenter 385
    zoom 0.58
    menu_art_move(0.58, 750, 0.58)

image menu_art_s:
    subpixel True
    "gui/menu_art_s.png"
    xcenter 510
    ycenter 500
    zoom 0.68
    menu_art_move(0.68, 510, 0.68)

image menu_art_m:
    subpixel True
    "gui/menu_art_m.png"
    xcenter 1000
    ycenter 640
    zoom 1.00
    menu_art_move(1.00, 1000, 1.00)

# Ghost Main Menu Images
image menu_art_y_ghost:
    subpixel True
    "gui/menu_art_y_ghost.png"
    xcenter 600
    ycenter 335
    zoom 0.60
    menu_art_move(0.54, 600, 0.60)

image menu_art_n_ghost:
    subpixel True
    "gui/menu_art_n_ghost.png"
    xcenter 750
    ycenter 385
    zoom 0.58
    menu_art_move(0.58, 750, 0.58)

image menu_art_s_ghost:
    subpixel True
    "gui/menu_art_s_ghost.png"
    xcenter 510
    ycenter 500
    zoom 0.68
    menu_art_move(0.68, 510, 0.68)

image menu_art_m_ghost:
    subpixel True
    "gui/menu_art_m_ghost.png"
    xcenter 1000
    ycenter 640
    zoom 1.00
    menu_art_move(1.00, 1000, 1.00)

# Sayori Image After Game 1st Restart
image menu_art_s_glitch:
    subpixel True
    "gui/menu_art_s_break.png"
    xcenter 470
    ycenter 600
    zoom 0.68
    menu_art_move(.8, 470, .8)

image menu_nav:
    "gui/overlay/main_menu.png"
    menu_nav_move

# Main Menu Effects

image menu_particles:
    2.481
    xpos 224
    ypos 104
    ParticleBurst("gui/menu_particle.png", explodeTime=0, numParticles=40, particleTime=2.0, particleXSpeed=3, particleYSpeed=3).sm
    particle_fadeout

transform particle_fadeout:
    easeout 1.5 alpha 0

transform menu_bg_move:
    subpixel True
    topleft
    parallel:
        xoffset 0 yoffset 0
        linear 3.0 xoffset -100 yoffset -100
        repeat
    parallel:
        ypos 0
        time 0.65
        ease_cubic 2.5 ypos -500

transform menu_bg_loop:
    subpixel True
    topleft
    parallel:
        xoffset 0 yoffset 0
        linear 3.0 xoffset -100 yoffset -100
        repeat

transform menu_logo_move:
    subpixel True
    yoffset -300
    time 1.925
    easein_bounce 1.5 yoffset 0

transform menu_nav_move:
    subpixel True
    xoffset -500
    time 1.5
    easein_quint 1 xoffset 0

transform menu_fadeout:
    easeout 0.75 alpha 0
    time 2.481
    alpha 0.4
    linear 0.5 alpha 0

transform menu_art_move(z, x, z2):
    subpixel True
    yoffset 0 + (1200 * z)
    xoffset (740 - x) * z * 0.5
    zoom z2 * 0.75
    time 1.0
    parallel:
        ease 1.75 yoffset 0
    parallel:
        pause 0.75
        ease 1.5 zoom z2 xoffset 0

# Team Salvato Splash Screen

image intro = "mod_assets/bg/splash.png"

# Special Mod Message Text

image warning:
    truecenter
    "white"
    "splash_warning" with Dissolve(0.5, alpha=True)
    2.5
    "white" with Dissolve(0.5, alpha=True)
    0.5

# Startup Disclaimer Images
image tos = "bg/warning.png"
image tos2 = "bg/warning2.png"

# Startup Disclaimer

label splashscreen:
    show layer master at old_tv
    # Sets First Run to False to Show Disclaimer
    default persistent.first_run = False

    # Startup Disclaimer

    if not persistent.first_run:
        python:
            restore_all_characters()
        $ quick_menu = False
        scene white
        pause 0.5
        scene tos
        with Dissolve(1.0)
        pause 1.0
        # You can edit this message but you MUST have say it's not affiliated with Team Salvato
        # must finish the official game and has spoilers, and where to get DDLC from."
        "[config.name] is a Doki Doki Literature Club fan mod that is not affiliated in anyway with Team Salvato."
        "It is designed to be played only after the official game has been completed, and contains spoilers for the official game."
        "Game files for Doki Doki Literature Club are required to play this mod and can be downloaded for free at: https://ddlc.moe or on Steam."
        menu:
            "By playing [config.name] you agree that you have completed Doki Doki Literature Club and accept any spoilers contained within."
            "I agree.":
                pass
        $ persistent.first_run = True
        scene tos2
        with Dissolve(1.5)
        pause 1.0
        scene white

        $ persistent.first_run = True

    $ basedir = config.basedir.replace('\\', '/')

    # Controls auto-load of certain scripts
    if persistent.autoload:
        jump autoload

    # Team Salvato/Splash Message

    $ starttime = datetime.datetime.now()

    show expression "#00f"

    python hide:
        config.allow_skipping = False
        # config.main_menu_music = audio.t1
        # renpy.music.play(config.main_menu_music)

    show screen vhs_overlay()
    show splash_nosignal "NO SIGNAL"
    play sound [ "<silence 1.0>", "mod_assets/sfx/insert-cassette.ogg" ]

    pause 5.5

    play audio "mod_assets/sfx/vhs-interference.ogg" volume 3.0

    hide splash_nosignal
    pause 0.5

    show intro at Transform(matrixcolor=SaturationMatrix(0.4))

    pause 2.5

    hide intro
    pause 1.5

    show splash_warning "[splash_message_default]"

    pause 0.5
    pause 2.0

    hide splash_warning
    # with Dissolve(0.5, alpha=True)
    pause 1.5

    python hide:
        renpy.pause(6.5 - (datetime.datetime.now() - starttime).total_seconds())
        config.allow_skipping = True

    return

# Warning Screen
label warningscreen:
    hide intro
    show warning
    pause 3.0

## If Monika.chr is deleted, this would play instead of the regular Chapter 1
## From Script-CH0.rpy
## Commented out for mod safety reasons.
# label ch0_kill:
#     $ s_name = "Sayori"
#     show sayori 1b zorder 2 at t11
#     s "..."
#     s "..."
#     s "W-What..."
#     s 1g "..."
#     s "This..."
#     s "What is this...?"
#     s "Oh no..."
#     s 1u "No..."
#     s "This can't be it."
#     s "This can't be all there is."
#     s 4w "What is this?"
#     s "What am I?"
#     s "Make it stop!"
#     s "PLEASE MAKE IT STOP!"

#     $ delete_character("sayori")
#     $ delete_character("natsuki")
#     $ delete_character("yuri")
#     $ delete_character("monika")
#     $ renpy.quit()
#     return

# Checks if Afterload is the same as the anticheat
label after_load:
    $ config.allow_skipping = allow_skipping
    $ _dismiss_pause = config.developer
    $ persistent.ghost_menu = False

    if anticheat != persistent.anticheat:
        stop music
        scene black
        "The save file could not be loaded."
        "Are you trying to cheat?"

        $ renpy.utter_restart()
    return

# Autoreloads the game 
label autoload:
    python:
        if "_old_game_menu_screen" in globals():
            _game_menu_screen = _old_game_menu_screen
            del _old_game_menu_screen
        if "_old_history" in globals():
            _history = _old_history
            del _old_history
        renpy.block_rollback()

        renpy.context()._menu = False
        renpy.context()._main_menu = False
        main_menu = False
        _in_replay = None

    $ renpy.pop_call()
    jump expression persistent.autoload

# starts the menu music once started
label before_main_menu:
    $ config.main_menu_music = audio.t1
    return

# Basic Quit.
label quit:
    if persistent.ghost_menu:
        hide screen main_menu
        scene white
        show expression "gui/menu_art_m_ghost.png":
            xpos -100 ypos -100 zoom 3.5
        pause 0.01
    return
