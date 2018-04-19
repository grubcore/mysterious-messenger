
init python:

    ## This is the object that each chat is stored in
    ##  Who = the speaker, What = the text they're saying, thetime is a currently
    ##  unused variable that keeps track of the current time in case you wanted
    ##  to post that to the screen, 'bounce' indicates whether the message is
    ##  supposed to animate in with a bounce or not (by default is false), and
    ##  specBubble is a variable that holds the name of any special speech bubbles
    ##  that should be used when displaying the text (by default is empty and a regular
    ##  bubble is used)
    class Chatentry(object):
        def __init__(self, who, what, thetime, img=False, bounce=False, specBubble=None):
            self.who = who
            self.what = what
            self.thetime = thetime
            self.img = img
            self.bounce = bounce
            self.specBubble = specBubble
            
    # This class just makes it simpler to type out character dialogue
    class Chat(object):
        def __init__(self, who):
            self.who = who
            
        def __call__(self, what, pauseVal=None, img=False, bounce=False, specBubble=None, **kwargs):
            addchat(self.who, what, pauseVal=pauseVal, img=img, bounce=bounce, specBubble=specBubble)
            
           
    ##****************************
    ##DECLARE CHARACTERS HERE
    ##****************************
    
    ## Character declarations
    s = Chat("Sev")
    y = Chat("Yoo")
    m = Chat("MC")
    ja = Chat("Ja")
    ju = Chat("Ju")
    z = Chat("Zen")
    r = Chat("Rika")
    ra = Chat("Ray")
    sa = Chat("Sae")
    u = Chat("Unk")
    v = Chat("V")
    msg = Chat("msg")
    answertest = Chat("answer")
    
    chatlog = []
    # Currently these are unused
    chathistory = []    # this keeps track of old chats
                        # when chatlog[] gets too long
    chatArchive = []    # this will be an array of chatlogs
                        # that stores an entire chatroom per index
                       
    ## You can declare characters here and their profile pictures
    ## As of now, you can either change profile pictures here or by updating
    ## the variable (see the example when MC is changed in script.rpy)
    ## Each entry is of the style:
    ## "Short Form": "address of profile photo"
    chatportrait = {'Sev': 'Profile Pics/Seven/sev-1.png', 
                    'Zen': 'Profile Pics/Zen/zen-1.png', 
                    'Ja': 'Profile Pics/Jaehee/ja-1.png', 
                    'Ju': 'Profile Pics/Jumin/ju-1.png', 
                    'Yoo' : 'Profile Pics/Yoosung/yoo-1.png', 
                    'MC' : 'Profile Pics/MC/MC-1.png', 
                    'Rika' : 'Profile Pics/Rika/rika-1.png',
                    'Ray' : 'Profile Pics/Ray/ray-1.png',
                    'V' : 'Profile Pics/V/V-1.jpg',
                    'Unk' : 'Profile Pics/Unknown/Unknown-1.png',
                    'Sae' : 'Profile Pics/Saeran/sae-1.png',
                    'msg' : 'transparent.png', 
                    "filler" : "transparent.png",
                    "answer" : "transparent.png"} 

    ## This is where you store character nicknames so you don't
    ##  have to type out their full name every time
    ##  To be honest this is somewhat moot as I've declared variables
    ##  to hold the name of their nickname elsewhere, but it's still useful
    ## Format:
    ## "Nickname/Short Form": "Full Name as it should appear in the chat"
    chatnick = {'Sev': '707', 
                'Zen': 'ZEN', 
                'Ja' : 'Jaehee Kang', 
                'Ju' : 'Jumin Han', 
                'Yoo' : 'Yoosung★', 
                'MC' : 'MC♥',     # This is the default name and is replaced when the user enters a custom one
                'Rika' : 'Rika',
                'V' : 'V',
                'Sae' : 'Saeran',
                'Unk' : 'Unknown',
                "msg" : "msg", 
                "filler" : "filler",
                'Ray' : 'Ray',
                "answer" : "answer"} 
                
    ### Set a variable to infinity, to be used later -- it keeps the viewport scrolling to the bottom
    yadjValue = float("inf")
    ### Create a ui.adjustment object and assign it to a variable so that we can reference it later. 
    # I'll assign it to the yadjustment property of our viewport later.
    yadj = ui.adjustment()
    
    # This is mostly changed automatically for you when you call
    # chat_begin("night") etc, but if you want to change it on an
    # individual basis this is the colour of the characters' nicknames
    nickColour = "#000000"   


default new_msg_clicked = False

    
        
screen messenger_screen:

    if yadj.value == yadj.range:
        $ yadj.value = yadjValue
    elif yadj.value == 0:
        $ yadj.value = yadjValue
                
    #else:
        #image "Phone UI/new_message_banner.png" ypos 170
        #$ new_msg_clicked = False
        #imagebutton:
        #    xanchor 0.0
        #    yanchor 0.0
        #    xpos 0
        #    ypos 169
        #    focus_mask True
        #    idle "new_messages"
        #    action [SetVariable("new_msg_clicked", True), renpy.restart_interaction]
        #if new_msg_clicked:
        #    $ new_msg_clicked = False
        #    $ yadj.value = yadjValue
        #    $ renpy.hide_screen("new_message_screen")
    # else: could have a "new_messages" notification


    window:
        style "phone_window"
        frame:
            background "transparent.png"
            align (0.5, 0.2)
            
            side "c r":
                area (0, 110, 750, 1050)
                
                viewport yadjustment yadj: # viewport id "VP":
                    draggable True
                    mousewheel True
                    
                    has vbox: ## displays the avatar and underneath it the nickname
                        spacing gui.phone_spacing  
                        if gui.phone_height:
                            vpgrid:
                                cols 1
                                yinitial 1.0

                                use chat_dialogue()

                        else:

                            use chat_dialogue()
                            
                            

screen chat_dialogue():
 
    python:
        chatLength = len(chatlog) - 1
        begin = chatLength - 10
        if begin >= 0:
            pass
        else:
            begin = 0
        
        if chatLength > 0:
            finalchat = chatlog[-1]
            if finalchat.who == "answer":
                if begin > 0:
                    begin -= 1
                
    vbox:
        for i in chatlog[begin:]:
            use character_animation(i)
                      
      
# This screen animates the most recent dialogue bubble
screen character_animation(i):
    python:
        if i.bounce:
            transformVar = incoming_message_bounce
        else:
            transformVar = incoming_message

        if i.who == "MC":
            phoneStyle = "phone_label_MC"
        else:
            phoneStyle = "phone_label"
        
        if i.specBubble != None:
            bubbleBackground = "Bubble/Special/" + i.who + "_" + i.specBubble + ".png"    
        elif i.bounce:  # Not a special bubble; just glow
            bubbleBackground = "Bubble/" + i.who + "-Glow.png"
        elif i.who != "answer":
            bubbleBackground = "Bubble/" + i.who + "-Bubble.png"
                
        if i.specBubble != None:
            # Some characters have more than one round or square bubble
            # but they follow the same style as "round" or "square"
            if i.specBubble[:6] == "round2":
                bubbleStyle = "round_" + i.specBubble[-1:]
            elif i.specBubble[:7] == "square2":
                bubbleStyle = "square_" + i.specBubble[-1:]
            else:
                bubbleStyle = i.specBubble
        
        if i.img == True:
            if "{image=" in i.what:
                pass
            else:
                transformVar = small_CG
                
        global choosing

       

    if i.who != "msg" and i.who != "filler" and i.who != "answer" and i.who != "pause":
        vbox:
            if i.who == "MC":
                style "phone_profpic_MC"
            else:
                style "phone_profpic"
                
            add chatportrait[i.who] 
            
        text chatnick[i.who] style phoneStyle color nickColour
        # text i.thetime style "phone_time3" (for MC) or "phone_time2" (for others)
        
        window at transformVar:
            if i.img == True:
                # Check if it's an emoji
                if "{image=" in i.what:
                    # there's an image to display
                    style "phone_img"
                    text i.what
                else:   # presumably it's a CG
                    # Could have a key-dictionary here that unlocks CGs in a gallery
                    # if i.what in gallery -> gallery[i.what] = True and then it'd display
                    $ fullsizeCG = i.what
                    style "phone_img"
                    imagebutton:
                        bottom_margin -100
                        focus_mask True
                        idle fullsizeCG
                        if not choosing:
                            action [SetVariable("fullsizeCG", i.what), Call("viewCG"), Return]

            elif i.specBubble != None:                        
                style bubbleStyle background bubbleBackground # e.g. style "sigh_m" 
                text i.what style "special_bubble"
            else:
                if (i.bounce):  # The bubble is supposed to bounce)
                    if i.who == "MC":
                        style "MC_glow"
                    else:
                        style "reg_glow" background Frame(bubbleBackground, 25, 25) # style (i.who + "_glow")
                else:
                    if i.who == "MC":
                        style "MC_bubble"
                    else:
                        style "reg_bubble" background Frame(bubbleBackground, 25,18,18,18) # style (i.who + "_bubble")
                    
                ## This code is a bit odd, but it determines how long the line
                ## of text is, and then decides if it needs to wrap it or not
                ## If it does need to wrap it, it pads out a minimum width
                ## This is how it displays in-game, otherwise each bubble would
                ## only be exactly as wide as it needed to be
                $ t = Text(i.what)
                $ z = t.size()
                $ z1 = z[0]
                if z1 > gui.longer_than:
                    text i.what style "bubble_text_long" min_width gui.long_line_min_width
                else:            
                    text i.what style "bubble_text"

        use anti_animation(i)
    
    elif i.who == "msg" or i.who == "filler":
        window: # Note: no animation
            style (i.who + "_bubble")
            text i.what style (i.who + "_bubble")
            
    else:
        pass
            

#*************************************
# Very silly code that is just to    *
# cancel out the animation for MysMe *
#*************************************                
screen anti_animation(i):
    
    python:
        if i.bounce:
            transformVar = anti_incoming_message_bounce
        else:
            transformVar = anti_incoming_message
            
        if i.bounce:
            bubbleBackground = "Bubble/" + i.who + "-Glow.png"
        else:
            bubbleBackground = "Bubble/" + i.who + "-Bubble.png"
            
        if i.specBubble != None:
            if i.specBubble[:6] == "round2":
                bubbleStyle = "round_" + i.specBubble[-1:]
            elif i.specBubble[:7] == "square2":
                bubbleStyle = "square_" + i.specBubble[-1:]
            else:
                bubbleStyle = i.specBubble
                
        if i.specBubble != None:
            bubbleBackground = "Bubble/Special/" + i.who + "_" + i.specBubble + ".png"
            
        if i.img == True:
            if "{image=" in i.what:
                pass
            else:
                transformVar = anti_small_CG
        

    window at transformVar:
        if i.img == True:
            # Check if it's an emoji
            if "{image=" in i.what:
                # there's an image to display
                style "phone_img"
                text i.what
            else:   # presumably it's a CG
                style "phone_img" bottom_margin -100
                text "{image=" + i.what + "}" #"-small}"
                
        elif i.specBubble != None:                        
            style bubbleStyle background bubbleBackground # e.g. style "sigh_m" 
            text i.what style "special_bubble"
        else:
            if (i.bounce):  # The bubble is supposed to bounce)
                if i.who == "MC":
                    style "MC_glow"
                else:
                    style "reg_glow" background Frame(bubbleBackground, 45, 45) # style (i.who + "_glow")
            else:
                if i.who == "MC":
                    style "MC_bubble"
                else:
                    style "reg_bubble" background Frame(bubbleBackground, 25,18,18,18) # style (i.who + "_bubble")
                
            $ t = Text(i.what)
            $ z = t.size()
            $ z1 = z[0]
            if z1 > gui.longer_than:
                text i.what style "bubble_text_long" min_width gui.long_line_min_width
            else:
                text i.what style "bubble_text"
                
                

                
