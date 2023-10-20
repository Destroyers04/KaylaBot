import requests
import urllib.parse

api_key = "RGAPI-7d410fe1-0011-46f5-ab74-31d794fed409"

class LeagueAPICog(commands.Cog):
    
    def fetch_accountID(api_url):
        dataset = requests.get(api_url)
        dataset = dataset.json() #converts json to dict 
        return dataset['accountId']

    def fetch_puuID(api_url):
        dataset = requests.get(api_url)
        dataset = dataset.json() #converts json to dict 
        return dataset['puuid']

    def fetch_matchID(api): 
        #def fetch_matchID(api, amnt_matches = 1):
        dataset = requests.get(api)
        dataset = dataset.json() #converts json to dict 
        return dataset[0]
        #can just loop this but changing the idx by the current loop
        """     else:
                match_IDS = []
                for i in range(amnt_matches):
                    match_IDS.append(dataset[i])
                return match_IDS """

    def fetch_matchData(api_url, puuID=None):
        dataset = requests.get(api_url)
        dataset = dataset.json() #converts json to dict 
        dictionaries = dataset['info']['participants']
        if puuID != None:
            for i in dictionaries:
                if i['puuid'] == puuID:
                    return i
        else:
            return dataset['info']
            

    def fetch_Display(participant_dict, game_info_dict, username, region_tag_old):
        deaths = participant_dict['deaths']
        totalTimeSpentDead = participant_dict['totalTimeSpentDead']
        challenges = participant_dict['challenges']
        visionScoreAdvantageLaneOpponent = challenges['visionScoreAdvantageLaneOpponent']
        visionScorePerMinute = challenges['visionScorePerMinute']
        visionScore = participant_dict['visionScore']
        visionWardsBoughtInGame = participant_dict['visionWardsBoughtInGame']
        wardsKilled = challenges['wardTakedowns']
        champion = participant_dict['championName']
        game_duration_minutes = game_info_dict['gameDuration'] // 60
        individual_position = participant_dict['individualPosition'].lower()
        wardsPlaced = participant_dict['challenges']['controlWardsPlaced']+ participant_dict['challenges']['stealthWardsPlaced']
        noPings = False

        # Vision quality calculation
        good_vision = "Bad, you can do better!"
        if individual_position == "support":
            if visionScorePerMinute >= 2:
                good_vision = "Good, keep it up!"
        else:
            if visionScorePerMinute >= 0.75:
                good_vision = "Good, keep it up!"

        # Win or lose?
        win = "won" if participant_dict['win'] else "lost"

        # Pings calculation
        type_pings = ["allInPings", "assistMePings", "baitPings", "basicPings", 
                    "dangerPings", "enemyMissingPings", "enemyVisionPings", 
                    "getBackPings", "holdPings", "onMyWayPings", "pushPings", "visionClearedPings"]
        total_pings = sum(participant_dict[ping] for ping in type_pings)

        # Toxic?
        toxicity = "you seem pretty chill"
        if total_pings / game_duration_minutes >= 1:
            toxicity = "you seem pretty toxic"
            if total_pings == 0:
                noPings = True

        # Constructing messages
        if deaths == 0:
            death_stat = f"You didn't die at all!"
        else:
            death_stat = f"You died {deaths} times and enjoyed {totalTimeSpentDead} seconds of grey screen."
        
        if visionScoreAdvantageLaneOpponent > 0:
            vision_stat = (f"You ended the game with a vision score of {visionScore}, "
                        f"which is equivalent to {visionScorePerMinute:.2f} vision per minute. "
                        f"This is {good_vision} You bought {visionWardsBoughtInGame} control wards, "
                        f"placed a total of {wardsPlaced} wards, and helped remove {wardsKilled} wards. "
                        f"You had {round(visionScoreAdvantageLaneOpponent,2)} higher vision score than your lane opponent!")
        elif visionScoreAdvantageLaneOpponent == 0:
            vision_stat = (f"You ended the game with a vision score of {visionScore}, "
                        f"which is equivalent to {visionScorePerMinute:.2f} vision per minute. "
                        f"This is {good_vision}! You bought {visionWardsBoughtInGame} control wards, "
                        f"placed a total of {wardsPlaced} wards, and helped remove {wardsKilled} wards. "
                        f"You had the same vision score as your lane opponent!")
        else: 
            vision_stat = (f"You ended the game with a vision score of {visionScore}, "
                        f"which is equivalent to {visionScorePerMinute:.2f} vision per minute. "
                        f"This is {good_vision}! You bought {visionWardsBoughtInGame} control wards, "
                        f"placed a total of {wardsPlaced} wards, and helped remove {wardsKilled} wards. "
                        f"You were down {round(visionScoreAdvantageLaneOpponent,2)} vision score compare to your lane opponent!")
        
        if individual_position == 'support' or 'jungle':
            intro_stat = (f"These are your stats, {username}!\n"
                        f"You played as {individual_position} {champion} and {win} your game "
                        f"after playing for {game_duration_minutes} minutes.")
        else:
            intro_stat = (f"These are your stats, {username}!\n"
                        f"You played as {champion} in the {individual_position} lane and {win} your game "
                        f"after playing for {game_duration_minutes} minutes.")
            
        if noPings:
            toxic_stat = f"You didn't ping at all,"
        else:
            toxic_stat = f"You sent {total_pings} pings, {toxicity}"

        # Link construction
        summoner_uGG = username.replace(' ', 'a')
        ugg_link = f"https://u.gg/lol/profile/{region_tag_old}/{summoner_uGG}/overview"

        return f"{intro_stat}\n{death_stat}\n{vision_stat}\n{toxic_stat}\nHere is your U.GG link for more information (I'm not sponsored):\n{ugg_link}"


        #f"{game1} \n{game2} \n{game3} \n{game4} \n{game5} \n{ugg_link}"
    def displayPlayerStats(user,region="EUW"):
        regionsDict = {
        "br1": "americas",
        "eun1": "europe",
        "euw1": "europe",
        "la1": "americas",
        "la2": "americas",
        "na1": "americas",
        "oc1": "sea",         
        "ru": "europe",
        "tr1": "europe",
        "jp1": "asia",
        "kr": "asia",
        "ph2": "sea",           
        "sg2": "sea",          
        "tw2": "asia",
        "th2": "sea",           
        "vn2": "sea"            
        }
        count = 0
        region_tag_old = None
        region_tag_new = None
        for i in regionsDict:
            if region.lower() in list(regionsDict.keys())[count]:
                region_tag_old = i
                region_tag_new = regionsDict[i]
                break
            count += 1

        username = user.split(':')[-1]
        username = urllib.parse.quote(username)
        api_url_account = "https://" + region_tag_old + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + username + "?api_key=" + api_key
        puuID = fetch_puuID(api_url_account)
        api_url_matches = "https://" + region_tag_new + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuID + "/ids?start=0&count=20" + "&api_key=" + api_key
        matchID = fetch_matchID(api_url_matches)
        api_url_match_info = "https://" + region_tag_new + ".api.riotgames.com/lol/match/v5/matches/"+ matchID + "?api_key=" + api_key
        playerMatchData = fetch_matchData(api_url_match_info, puuID)
        matchData = fetch_matchData(api_url_match_info)
        stats = fetch_Display(playerMatchData, matchData, user, region_tag_old)
        return stats

        """
        if 'help' in p_message:
            return 'here are my commands:\n- "Kayla! give me some league ideas"\n\
    - "kFetchmyStats "Username" "region"'

        if 'give me some league ideas' in p_message:
            with open(r"/Users/Aaron/Desktop/Skole: Universitet /InformasjonsVitenskap/KaylaBot/Extras/champions.txt") as fp:
                champions = fp.readlines()
                archetypes = ["bruiser", "enchanter", "tanky", "ADC", "mage", "assasin", "poke"]
                rand_idx= random.randint(0,len(champions))
                rand_champ = (champions[rand_idx]).strip("\n")
                rand_archetype = random.choice(archetypes)
                if rand_archetype[0] in ['a','e','i','o','u']:
                    resp1 = f"Have you tried playing {rand_champ} with an {rand_archetype} build?"
                    return resp1
                else:
                    resp2 = f"Have you tried playing {rand_champ} with a {rand_archetype} build?"
                    return resp2 """
    @commands.command()
    async def myStats(self, ctx, username, region="EUW"):
        try:
            results = LeagueofLegends.displayPlayerStats(username, region)
            await ctx.send(results)
        except:
            await ctx.send(f"I've searched everywhere, but I couldn't find {username}")