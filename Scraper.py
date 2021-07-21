import time
import random


# BODOG Scraping
def scrape_bodog(driver):
    driver.get('https://www.bodog.eu/sports/basketball/nba')
    time.sleep(random.randrange(8, 10))
    bodog_full_coupons = driver.find_elements_by_xpath('//section[@class="coupon-content more-info"]')
    bodog_coupon_list = []
    for i in range(len(bodog_full_coupons)):
        bodog_coupon_list.append(bodog_full_coupons[i].text)
    return parse_bodog(bodog_coupon_list)


def parse_bodog(bodog_list):
    # will split the data from each ticket into usable class data, data per match
    match_data = []
    for string in bodog_list:
        team_names = []
        win_bets = []
        data = string.split("\n")
        date = "shrug"
        team_names.append(data[-9])
        team_names.append(data[-8])
        win_bets.append(data[-4])
        win_bets.append(data[-3])
        match = MatchData(team_names, win_bets, date, "Bodog")
        match_data.append(match)

    return match_data


# POWERPLAY SCRAPING
def scrape_powerplay(driver):
    driver.get('https://www.powerplay.com/sportsbook/BASKETBALL/US_NBA/')
    time.sleep(random.randrange(8, 10))
    powerplay_data = driver.find_elements_by_xpath('//div[@class="events-app__event"]')
    powerplay_data_list = []
    for i in range(len(powerplay_data)):
        powerplay_data_list.append(powerplay_data[i].text)
    return parse_powerplay(powerplay_data_list)


def parse_powerplay(data_list):
    match_data = []
    for string in data_list:
        data = string.split("\n")
        names = data[-5]
        team_names = names.split(" @ ")
        win_bets = []
        win_bets.append(data[-4])
        win_bets.append(data[-3])
        date = data[0] + data[1]
        match = MatchData(team_names, win_bets, date, "Powerplay")
        match_data.append(match)

    return match_data


# BETUS SCRAPING
def scrape_betus(driver):
    driver.get('https://www.betus.com.pa/sportsbook/nba-basketball-odds.aspx')
    time.sleep(random.randrange(10, 12))
    betus_data = driver.find_elements_by_xpath('//div[@class="game-tbl row"]')
    betus_data_list = []
    for i in range(len(betus_data)):
        betus_data_list.append(betus_data[i].text)
    return parse_betus(betus_data_list)


def parse_betus(data_list):
    match_data = []
    for string in data_list:
        data = string.split("\n")
        team_names = []
        win_bets = []
        date = data[0]
        team_names.append(data[1])
        team_names.append(data[8])
        win_bets.append(data[3])
        win_bets.append(data[10])
        match = MatchData(team_names, win_bets, date, "BetUS")
        match_data.append(match)

    return match_data


# FANDUEL SCRAPING
def scrape_fanduel(driver):
    driver.get('https://sportsbook.fanduel.com/sports/navigation/830.1/10107.3')
    time.sleep(random.randrange(7, 10))
    fanduel_team_data = driver.find_elements_by_xpath('//div[@class="layout coupon-event big3-event BASKETBALL"]')
    fanduel_team_data_list = []
    for i in range(len(fanduel_team_data)):
        fanduel_team_data_list.append(fanduel_team_data[i].text)
    return parse_fanduel(fanduel_team_data_list)


def parse_fanduel(data_list):
    match_data = []
    for string in data_list:
        data = string.split("\n")
        team_names = []
        win_bets = []
        date = 'soon probably'
        team_names.append(data[0])
        team_names.append(data[1])
        if len(data) > 7:
            win_bets.append(data[6])
            win_bets.append(data[7])
        else:
            win_bets = [0,0]
        match = MatchData(team_names, win_bets, date, "Fanduel")
        match_data.append(match)
    return match_data


#  Sport888 SCRAPING
def scrape_sport888(driver):
    driver.get('https://www.888sport.com/basketball')
    time.sleep(random.randrange(10, 12))
    sport888_data = driver.find_elements_by_xpath('//div[@class="bet-card"]')
    sport888_data_list = []

    for i in range(len(sport888_data)):
        sport888_data_list.append(sport888_data[i].text)
    for match in sport888_data_list:
        print(match)

    # return parse_sport888(sport888_data_list)


def parse_sport888(data_list):
    match_data = []
    for string in data_list:
        data = string.split("\n")
        team_names = []
        win_bets = []
        date = 'soon probably'
        team_names.append(data[0])
        team_names.append(data[1])
        win_bets.append(data[6])
        win_bets.append(data[7])
        match = MatchData(team_names, win_bets, date, "Fanduel")
        match_data.append(match)
    return match_data


class MatchData:

    def __init__(self, teams, odds, date, bet_site):
        self.team1 = teams[0]
        self.team2 = teams[1]
        try:
            self.odds1 = float(odds[0])
            self.odds2 = float(odds[1])
            if abs(self.odds1) > 20 and abs(self.odds2) > 20:
                self.odds1 = american_to_decimal(self.odds1)
                self.odds2 = american_to_decimal(self.odds2)
        except ValueError:
            self.odds1 = 0
            self.odds2 = 0
        self.team_names = teams
        self.match_name = teams[0][0].upper() + teams[0][1].lower() + teams[1][0].upper() + teams[1][1].lower()
        self.date = date
        self.bet_site = bet_site


def american_to_decimal(odds):
    if odds == 0:
        return 0
    elif odds > 0:
        output = 1 + (odds/100)
    else:
        output = 1 - (100/odds)
    return round(output, 4)

