init -50 python:
    ## Note: for this class to be standalone, you must import time and datetime
    ## You also need the get_random_screen_tag function from
    ## 01_mysme_engine/messenger/messenger_animations.rpy
    ## You only need the bit up to return_after_tag
    ## You can also use renpy.random instead of the random library if you
    ## don't want to import it

    class Achievement():
        """
        A class with information on in-game achievements which can be extended
        to use with other systems (e.g. Steam achievements).

        Attributes:
        -----------
        name : string
            The human-readable name of this achievement. May have spaces,
            apostrophes, dashes, etc.
        id : string
            The code-friendly name of this achievement (which can be used for
            things like Steam backend). May not include spaces, single or
            double quotes, or dashes. If not provided, name will be sanitized
            for this purpose.
        description : string
            A longer description for this achievement. Optional.
        unlocked_image : Displayable
            A displayable to use when this achievement is unlocked.
        locked_image : Displayable
            A displayable to use when this achievement is locked. If not
            provided, requires an image named "locked_achievement" is declared.
        stat_max : int
            If provided, an integer corresponding to the maximum progress of
            an achievement, if the achievement can be partially completed
            (e.g. your game has 24 chapters and you want this to tick up
            after every chapter, thus, stat_max is 24). The achievement is
            unlocked when it reaches this value.
        stat_progress : int
            The current progress for the stat.
        stat_modulo : int
            The formula (stat_progress % stat_modulo) is applied whenever
            achievement progress is updated. If the result is 0, the
            progress is shown to the user. By default this is 0 so all updates
            to stat_progress are shown. Useful if, for the supposed 24-chapter
            game progress stat, you only wanted to show updates every time the
            player got through a quarter of the chapters. In this case,
            stat_modulo would be 6 (24//4).
        hidden : bool
            True if this achievement's description and name should be hidden
            from the player.
        timestamp : Datetime
            The time this achievement was unlocked at.
        ignored : bool
            True if this achievement is being ignored (generally only
            relevant in order to omit tutorial achievements).
        """
        ## A list of all the achievements that exist in this game,
        ## to loop over in the achievements screen.
        all_achievements = [ ]
        def __init__(self, name, id=None, description=None, unlocked_image=None,
                locked_image=None, stat_max=None, stat_modulo=0, hidden=False):

            self._name = name
            # Try to sanitize the name for an id, if possible
            self.id = id or name.lower().replace(' ', '_').replace("'", '').replace('-', '_')

            self._description = description
            self.unlocked_image = unlocked_image or None
            self.locked_image = locked_image or "locked_achievement"

            self.stat_max = stat_max
            self.stat_modulo = stat_modulo

            self.hidden = hidden
            if persistent.achievement_timestamp is not None:
                self._timestamp = persistent.achievement_timestamp.get(self.id, None)

            # Add to list of all achievements
            if not getattr(store, 'IGNORE_ACHIEVEMENTS', False):
                self.all_achievements.append(self)

                # Register with backends
                achievement.register(self.id, stat_max=stat_max, stat_modulo=stat_modulo)

            self.ignored = getattr(store, 'IGNORE_ACHIEVEMENTS', False)

        @property
        def timestamp(self):
            """Return the timestamp when this achievement was granted."""
            if self.has():
                return "Unlocked {}".format(
                    datetime.fromtimestamp(
                        self._timestamp).strftime("%b %d, %Y @ %I:%M %p")
                )
            else:
                return ""

        @property
        def idle_img(self):
            """Return the idle image based on its locked status."""
            if self.has():
                return self.unlocked_image
            else:
                return self.locked_image

        @property
        def name(self):
            """
            Returns the name of the achievement based on whether it's
            hidden or not.
            """
            if self.hidden and not self.has():
                return "???"
            else:
                return self._name

        @property
        def description(self):
            """
            Returns the description of the achievement based on whether it's
            hidden or not.
            """
            if self.hidden and not self.has():
                return "???"
            else:
                return self._description

        def AddProgress(self, amount=1):
            """Add amount of progress to this achievement."""
            return Function(self.add_progress, amount=amount)

        def Progress(self, amount):
            """Set this achievement's progress to amount."""
            return Function(self.progress, amount)

        @property
        def stat_progress(self):
            """Return this achievement's progress stat."""
            return self.get_progress()

        def add_progress(self, amount=1):
            """
            Increment the progress towards this achievement by amount.
            """
            self.progress(min(self.stat_progress+amount, self.stat_max))

        ## Wrappers for various achievement functionality
        def clear(self):
            """Clear this achievement from memory."""
            return achievement.clear(self.id)

        def get_progress(self):
            """Return this achievement's progress."""
            return achievement.get_progress(self.id)

        def grant(self):
            """
            Grant the player this achievement, and show a popup if this is
            the first time they've gotten it.
            """
            has_achievement = self.has()
            x = achievement.grant(self.id)
            if not has_achievement:
                # First time this was granted
                self.achievement_popup()
                # Save the timestamp
                self._timestamp = time.time()
                store.persistent.achievement_timestamp[self.id] = self._timestamp
            return x

        def has(self):
            """Return True if the player has achieved this achievement."""
            return achievement.has(self.id)

        def progress(self, complete):
            """
            A plugin to the original Achievement class. Sets the current
            achievement progress to "complete".
            """
            has_achievement = self.has()
            x = achievement.progress(self.id, complete)
            if not has_achievement and self.has():
                # First time this was granted
                self.achievement_popup()
            return x

        def achievement_popup(self):
            """
            A function which shows an achievement screen to the user
            to indicate they were granted an achievement.
            """

            if not self.has():
                # Don't have this achievement
                return
            elif self.ignored:
                # Ignoring this achievement
                return

            # Otherwise, show the achievement screen
            for i in range(10):
                if store.onscreen_achievements.get(i, None) is None:
                    store.onscreen_achievements[i] = True
                    break
            ## Pick a random tag so that multiples of this screen can be
            ## shown at the same time
            tag = get_random_screen_tag(6, return_after_tag=True)
            renpy.show_screen('achievement_popup', a=self, tag=tag, num=i,
                _tag=tag)

        def Toggle(self):
            """
            A developer action to easily toggle the achieved status
            of a particular achievement.
            """
            return [SelectedIf(self.has()),
                If(self.has(),
                    Function(self.clear),
                    Function(self.grant))]

        def Grant(self):
            """
            An action to easily achieve a particular achievement.
            """
            return Function(self.grant)

    ## Actual achievements, for the tutorial
    ## These *can't* be removed (or else you'd need to comb through the
    ## rest of the game to get rid of the triggers, too), but if you change
    ## this value to True, it'll prevent them from activating or appearing
    ## in the achievements list.
    IGNORE_ACHIEVEMENTS = False
    ui_achievement = Achievement("Farewell, Old UI", "modified_ui",
        "Turn on the modified UI from the settings.",
        Crop((0, 0, 155, 155), Transform("Phone UI/bg_secure.webp", xsize=155, fit="contain"))
    )
    animated_bg_achievement = Achievement("Now for some Pizazz!", "animated_bgs",
        "Turn on the animated chatroom backgrounds from the settings.",
        Crop((0, 0, 155, 155), Transform("Phone UI/bg-rainy-day.webp", xsize=155, fit="contain"))
    )
    tutorial_ending1 = Achievement("Made it to the End", "tut_end_1",
        "See at least one ending on Tutorial Day.",
        Crop((0, 55, 155, 155), Transform("VN Mode/Backgrounds/normal_end.webp", xsize=155, fit="contain"))
    )
    tutorial_ending2 = Achievement("Gotta See 'Em All", "tut_end_2",
        "See all the endings on Tutorial Day.",
        Crop((0, 55, 155, 155), Transform("VN Mode/Backgrounds/good_end.webp", xsize=155, fit="contain"))
    )
    make_a_call_achievement = Achievement("Ring Ring", "make_a_call",
        "Try calling someone on the phone.",
        Transform("Phone Calls/call_contact_empty.webp", xsize=155, fit="contain")
    )
    try_real_time_achievement = Achievement("IRL", "irl",
        "Turn on real-time mode from the settings.",
        Fixed(
            Transform("Menu Screens/Main Menu/dlc.webp", xsize=155, fit="contain"),
            Transform("Phone Calls/call_icon_history.webp", align=(0.5, 0.53), matrixcolor=InvertMatrix(1.0)),
            fit_first=True
        )
    )
    expired_achievement = Achievement("Missed it by That Much", "expired",
        "Play through a chatroom that's expired.",
        "Menu Screens/Main Menu/save_load.webp"
    )
    first_cg_achievement = Achievement("New Image", "unlock_first_cg",
        "Unlock an image in the CG Gallery.",
        "CGs/common_album_cover.webp",
    )
    change_pfp_achievement = Achievement("Wait, I didn't pick that", "change_pfp",
        "Change a character's profile picture.",
        "Menu Screens/Main Menu/s_greeting.webp",
    )
    first_guest_achievement = Achievement("Get this Party Started", "first_guest",
        "Have one or more guests attend the party.",
        "Email/a_grade.webp",
        )
    change_your_pfp_achievement = Achievement("New Look, New Me", "change_my_pfp",
        "Unlock a bonus image for your own profile picture.",
        Crop((0, 60, 155, 155),
            Transform("CGs/common_album/cg-3.webp", xsize=155, fit="contain"))
        )
    malfunctioning_achievement = Achievement("I-it's malfunctioning!",
        "malfunction_achieve", "Hang up on Ray's Tutorial Day call.",
        "Phone Calls/call_button_hang_up.webp"
        )
    hidden_pfp_achievement = Achievement("Who Are You?",
        "hidden_pfp_achieve", "Change your profile picture to the black-haired man.",
        Crop((0, 0, 155, 155),
            Transform("CGs/common_album/cg-2.webp", xsize=155, fit="contain")),
        hidden=True)
    progress_stat_achievement = Achievement("Finish all the test achievements",
        "all_tutorial_achieve", "Complete all the achievements included with the base game.",
        "Menu Screens/Main Menu/menu_gift.webp",
        stat_max=13
    )





    ## Don't change this one or your achievements won't work
    IGNORE_ACHIEVEMENTS = False


## Track the time each achievement was earned at
default persistent.achievement_timestamp = dict()
## Tracks the number of onscreen achievements, for offsetting when
## multiple achievements are earned at once
default onscreen_achievements = dict()

image blue_ui_bg = Frame("Menu Screens/Day Select/daychat01_2.webp", 20, 15, 20, 15)