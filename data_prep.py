# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 12:31:12 2024

@author: may7e
"""

'''
Majority of the methods used for getting data like get_comp, get_matches, get_events are taken
from Benjamin Larrouse (https://github.com/BenjaminLarrousse/statsbomb-messi/tree/master), but rewritten. 

All data used were taken from Statsbomb github page. 

'''


import pandas as pd
import requests
import json
from tqdm import tqdm
from pandas import json_normalize


#load the .json variable file
json_filename = 'messi_config.json'

with open(json_filename, 'r') as file:
    config = json.load(file)


class dataprep:
    
    '''
    This project is all about messi and trying to figure his most important attribute. To do this, we'd 
    need his data from statsbomb. This class gets his data and puts them in the right format for analysis.
    
    '''
    
    def __init__(self, base_url: str =f"{config['base_url']}competitions.json" ):
        
        
        #define the base url for the data retrival 
        self.base_url = f"{config['base_url']}competitions.json"
        

        
    def get_comp(self):
        
        '''
        This function gets the free competitions available on statsbomb github page. 
        
        Parameters
        ----------
        None

        Returns
        -------
        data_df
        
        '''
        
        raw_data = requests.get(self.base_url)
        raw_data.encoding = 'utf-8'
        
        raw_data = raw_data.json()
        
        data_df = pd.DataFrame(raw_data)
        
        return data_df
    
    
    
    
    def get_matches(self, competitions):
        '''
        This function gets the free matches needed for the analysis.

        Parameters
        ----------
        competitions : pd.DataFrame
            Df for the 

        Returns
        -------
        matches_df

        '''
        
        #Instantiate an empty df for appending the matches into. 
        matches_df = pd.DataFrame()
        for i in tqdm(range(len(competitions)), desc = 'Getting Match Ids'):
            comp_id = str(competitions['competition_id'][i])
            season_id = str(competitions['season_id'][i])
            matches_url = f"{config['base_url']}/matches/{comp_id}/{season_id}.json"
            raw_matches = requests.get(url=matches_url)
            matches = json_normalize(raw_matches.json())
            matches_df = matches_df.append(matches, ignore_index=True, sort=False)
            
        return matches_df
    
    
    
    
    def get_match_event(self, match_id: str):
        
        '''
        This function gets the events from the free matches.
        Events are essentially things that happens in a football game, from kickoff to throw-ins
        and offsides etc.

        Parameters
        ----------
        match_id : String
            Match Id for the specific match of interest. 

        Returns
        -------
        events: pd.DataFrame
            Returns a df of events from the match id provided. This is the event from a single match.

        '''
        events_url = f"{config['base_url']}events/{match_id}.json"
        raw_events_api = requests.get(url=events_url)
        raw_events_api.encoding = 'utf-8'
        events = pd.DataFrame(json_normalize(raw_events_api.json()))
        
        
        #assign the match id to the events from each match.
        events.loc[:, 'match_id'] = match_id
        
        return events
    
    
    
    def get_events(self, match_df):
        '''
        This function gets the events from the free matches and returns a combined df of events from 
        all those matches. Events are essentially things that happens in a football game, from kickoff to throw-ins
        and offsides etc.

        Parameters
        ----------
        match_df : pd.DataFrame
            Df of match ids and other varaiables.

        Returns
        -------
        event_df: pd.DataFrame
            Concatenated df of events from multiple matches.

        '''
        result = []
        
        for ind in tqdm(match_df.index, desc = 'Getting Events from all the Matches.'):
            events = self.get_match_event(match_df[match_df.index == ind]['match_id'].values[0])
            events.loc[:, 'competition_id'] = match_df[match_df.index == ind
                                                        ]['competition.competition_id'].values[0]
            events.loc[:, 'season_id'] = match_df[match_df.index == ind
                                                   ]['season.season_id'].values[0]
            result.append(events)
        event_df = pd.concat(result, sort=True)
        
        
        return event_df    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            