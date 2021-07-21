from itertools import cycle
from selenium import webdriver
import random
import Scraper as s
import numpy as np
import time
import pandas as pd
import yagmail
from pubproxpy import Level, Protocol, ProxyFetcher


# BODOG requires Canadian Ip's
def main():
    proxy_fetcher = ProxyFetcher(level=Level.ELITE, protocol=Protocol.HTTP, countries="CA")
    USER_AGENTS = \
        [
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
            ,
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
            ,
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
            ,
            'Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
            ,
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
            ,
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
            ,
            'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
            ,
            'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
            ,
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            ,
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
            ,
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36']

    yagmail.register('kyle.pyprojects@gmail.com', 'projectG12')
    yag = yagmail.SMTP("kyle.pyprojects@gmail.com")
    reciever = "kyle.pyprojects@gmail.com"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    user_agent = cycle(USER_AGENTS)
    # a few other things to avoid detection
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {'userAgent': next(user_agent)})
    match_data = [s.scrape_betus(driver), s.scrape_bodog(driver), s.scrape_fanduel(driver),
                  s.scrape_powerplay(driver)]
    display_data = find_arb(match_data)
    if len(display_data) > 0:
        display_data.sort(key=lambda x: x.arb_percent)
        body = "----------------Arb-Alert-------------------\n"
        for arb in display_data:
            body += "{}% Arbitrage; {}: {}:{}  & {}: {}:{} Hedge:${}\n".format(arb.arb_percent, arb.bet_site1,
                                                                      arb.team1, arb.odds1, arb.bet_site2,
                                                                      arb.team2, arb.odds2, arb.hedge)
        yag.send(to=reciever, subject="Arb Alert{}".format(random.randrange(1, 10000000)), contents=body)
    driver.close()
    yag.send(to=reciever, subject="completed run", contents="another one")



def find_arb(data):
    bet_site_names = []
    match_names = []
    match_row_names = []

    for site in data:
        site.sort(key=lambda x: x.match_name)
        for match in site:
            if match.match_name not in match_names and match.match_name.isalnum():
                match_names.append(match.match_name)
            if match.bet_site not in bet_site_names:
                bet_site_names.append(match.bet_site)
    base_array = np.zeros((2 * len(match_names), len(bet_site_names)))
    for name in match_names:
        match_row_names.append(name[0]+name[1])
        match_row_names.append(name[2]+name[3])

    df = pd.DataFrame(columns=bet_site_names, index=match_row_names, data=base_array)
    for site in data:
        for match in site:
            if match.match_name.isalnum() and match.match_name in match_names:
                j = match_names.index(match.match_name)
                i = bet_site_names.index(match.bet_site)
                df.iloc[2 * j][i] = match.odds1
                df.iloc[2 * j + 1][i] = match.odds2
    print(df)
    pre_arb_list = []
    for i in range(len(match_row_names)):
        team_name = match_row_names[i]
        max_index = 0
        max_odds = -9999
        bet_site = ""
        for j in range(len(bet_site_names)):
            if abs(df.iloc[i][j]) > max_odds:
                max_odds = df.iloc[i][j]
                bet_site = bet_site_names[j]
        ticket = preArbTicket(bet_site, max_odds, team_name, [i, max_index])
        pre_arb_list.append(ticket)

    # ok so we have all the best bets from each site/match, now need to check for arb opportunity
    arb_list = []
    for j in range(0, len(pre_arb_list), 2):
        odds1 = pre_arb_list[j].odds
        odds2 = pre_arb_list[j + 1].odds
        expected_val, hedge = calc_arb(odds1, odds2)
        hedge = round(hedge, 5)
        expected_val = round(expected_val, 5)
        if expected_val > 0:
            arb = arbTicket(pre_arb_list[j].bet_site, pre_arb_list[j + 1].bet_site, expected_val, odds1, odds2,
                            pre_arb_list[j].team_name, pre_arb_list[j + 1].team_name, hedge)
            arb_list.append(arb)

    return arb_list


def calc_arb(odds1, odds2):
    if odds1 <= 0 or odds2 <= 0:
        return 0
    if odds1 > odds2:
        positive_odds = odds1
        negative_odds = odds2
    else:
        positive_odds = odds2
        negative_odds = odds1
    payout = positive_odds * 100
    hedge_stake = payout / negative_odds
    return (payout - (hedge_stake + 100)), hedge_stake


class arbTicket:
    def __init__(self, betsite1, betsite2, arb, betsite1odds, betsite2odds, team1, team2, hedge):
        self.bet_site1 = betsite1
        self.bet_site2 = betsite2
        self.team1 = team1
        self.team2 = team2
        self.arb_percent = arb
        self.odds1 = betsite1odds
        self.odds2 = betsite2odds
        self.hedge = hedge


class preArbTicket:
    def __init__(self, betsite1, betsite1odds, team_name, data_index):
        self.bet_site = betsite1
        self.df_index = data_index
        self.team_name = team_name
        self.odds = betsite1odds


if __name__ == '__main__':
    main()
