# zkillstory
```
      _     _  _  _       _                       
     | |   (_)| || |     | |                      
 ____| | __ _ | || | ___ | |_   ___   _ __  _   _ 
|_  /| |/ /| || || |/ __|| __| / _ \ | '__|| | | |
 / / |   < | || || |\__ \| |_ | (_) || |   | |_| |
/___||_|\_\|_||_||_||___/ \__| \___/ |_|    \__, |
                                             __/ |
                                            |___/ 
```

**Create an AI story about a killmail in EVE Online**

This is a silly little tool that you can run to turn a zkillboard.com link into an AI-generated story of what might have happened. It is obviously wildly inaccurate and is purely for fun.

Zkillstory uses OpenAI's Davinci3 and you will need an API key from them to run this. 

Place the key in a file called `.env` as `OPENAI_SECRET=your_key_here`

https://openai.com/api/pricing/

---


### **Example output story:**

*The dark skies of deep space were filled with a menacing energy as a single Osprey Navy Issue was making its way towards the Foxholers holding station. Little did the pilot, Sin Dekko, know what lie in wait for her. As she passed through the orbital gate, she suddenly found herself under attack from 5 ships from Mutilate Retirement Fund.*

*Leading the charge was DaStampede in his Vargur, followed by Lukas Van Eind in an Astarte, Mir Lotus Kasenumi also in an Astarte, First Recon and lLong Shotl both piloting their own Astartes. And lastly, Carlos SirAHno in an Arazu to round out their ferocious assault.*

*DaStampede piloted his Vargur excellently as he quickly closed in on Sin Dekko's Osprey with punishing fire from his weapons. His attacks were quickly backed up by the rest of the attackers and soon Sin Dekko was overwhelmed and forced to surrender. As DaStampede emerged victorious and claimed the final blow on their victim's ship, the rest of Mutilate Retirement Fund cheered them on in triumph. The bold attack had been a success and now their fleet could move on to bigger things.And that was just another day in New Eden*

---

**Input format example:** https://zkillboard.com/kill/105988213/

You can adjust the tokens used to generate the story in the line: 

`zkillstory.response = get_story(zkillstory, tokens=75, topic="An EVE Online story")`

I recommend approx 400 tokens for a decent story. There is no need to go higher than 700 really. The topic can also be changed to alter the nature to the story entirely while still keeping the participants and outcome the same.