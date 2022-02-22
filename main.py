"""
Copyright (C) 2022 Nathan Lim (a.k.a NateNate60)
    This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 
"""

import provablyfair

def main () :
    seed = provablyfair.genseed()
    print("The seed's hash is", provablyfair.hashseed(seed))
    nonce = 0
    while (True) :
        guess = ""
        while (guess != "h" and guess != "t") :
            guess = input("Guess the coin toss (h/t): ").lower()
        result = provablyfair.genrandom(seed, nonce)
        nonce += 1
        if (int(result, 16) % 2 == 0) :
            result = "h"
        else :
            result = "t"
        
        if (guess == result) :
            print("Congrats, you guessed right!")
        else :
            print("Sorry, you lost.")

        seeseed = input("Would you like to see the seed? (y/N) ").lower()
        if (seeseed == "y") :
            print ("The seed was", seed)
            print ("NOTE: To verify the seed, you must treat it as an ASCII/UTF-8 string, not as a hex encoding of raw bytes")
            break
    

if (__name__ == "__main__") :
    main()