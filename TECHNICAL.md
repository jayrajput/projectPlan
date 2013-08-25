Why not just use python code in place of text parsing?
------------------------------------------------------

My view is that the text is terse (compare to python code) and accentuates the
schedule. I played with the idea of using python but did not liked it.

Example Project Schedule Text:
````
MYPROJECT [name = "HELLO WORLD", start = "08/08"] {

    WP [name = "White Paper", dur = 2];

    SCHEMA [name = "Configuration Schema"] {
        CODE [dur = 3, res = "E1"]
            <- UT [dur = 2, res = "E2"]
                <- REVIEW [dur = 4, res = "E1, E2"]
                    <- BCR [dur = 5, res = "E2"];
    };

    SIGNALING [name = "Signaling"] {

        MOD1 [name = "Module 1"] {
            CODE [dur = 3, res = "E1"]
                <- UT [dur = 2, res = "E2"]
                    <- REVIEW [dur = 4, res = "E1, E2"]
                        <- BCR [dur = 5, res = "E2"];
        };

        MOD2 [name = "Module 2"] {
            CODE   [dur = 3];
            UT     [dur = 2, res = "E2"     ] -> CODE;
            REVIEW [dur = 4, res = "E1, E2" ] -> CODE;
            REWORK [dur = 5, res = "E2"     ] -> CODE;
        } -> MOD1;

    } -> WP, SIGNALING;
};
````
