''' 
March 5, 2020

- Uses Pandas to manipulate files
- Added Elo Rater
- Added Menu interface

'''

import random
import operator
import sys
import pandas as pd
#from __builtin__ import True
#from Carbon.Aliases import true



class rater:
    
    def __init__(self, input_file, save_file):
          
        self.save_file = save_file
        self.film_df = pd.read_csv(input_file)
        self.keep_rating = True
            
    def return_film_rating (self, film_name):
        
        return int(self.film_df[self.film_df.Full_Title == film_name].Rating.iloc[0])

    def return_film_year (self, film_name):
        
        return str(self.film_df[self.film_df.Full_Title == film_name].Year.iloc[0])

    def return_film_index (self, film_name):

        return self.film_df.loc[self.film_df['Full_Title'] == film_name].index[0]
        
        
    def random_elo_rater (self, k=50):
        # This rater follows the ELO algorithm used in sports
        # It works well because the number of points awarded and subtracted depend on the difference in rating
        # Note: a larger k-value will cause bigger jumps
        # Note: '1'/'2' pick a film; 'C' exits the rater
        
        # Create a temporary dataframe that excludes unrated films
        tmp_df = self.film_df[pd.notna(self.film_df.Rating)]

        title_n = len(tmp_df.Title)
        
        # Change the sample range here
        selection = random.sample(range(0, title_n), k=2)
         
        m1_index = selection[0]
        m2_index = selection[1]   
        
        m1 = tmp_df.iloc[m1_index]['Full_Title']
        m2 = tmp_df.iloc[m2_index]['Full_Title']
        
        m1_index = self.return_film_index(m1)
        m2_index = self.return_film_index(m2)
        
        m1_old_rate = float(self.film_df.iloc[m1_index]['Rating'])
        m2_old_rate = float(self.film_df.iloc[m2_index]['Rating'])
        
        m1_new_rate = m1_old_rate
        m2_new_rate = m2_old_rate
        
        #print m1_old_rate
        #print m2_old_rate
        
        m1_expected_score = 1 / ( 1 + 10 ** ( (m2_old_rate - m1_old_rate) / 400 ) )
        m2_expected_score = 1 / ( 1 + 10 ** ( (m1_old_rate - m2_old_rate) / 400 ) )

        
        #print m1_expected_score
        #print m2_expected_score
        
        self.print_notice(m1, m2)
                
        user_choice = raw_input()


        if (user_choice == '1'):

            m1_new_rate = int(m1_old_rate + k * (1 - m1_expected_score))
            m2_new_rate = int(m2_old_rate + k * (0 - m2_expected_score))

            #print m1_new_rate
            #print m2_new_rate
          
                      
        if (user_choice == '2') :
            
            m1_new_rate = int(m1_old_rate + k * (0 - m1_expected_score))
            m2_new_rate = int(m2_old_rate + k * (1 - m2_expected_score))

            #print m1_new_rate
            #print m2_new_rate        
        

        if (user_choice == 'C'):
            
            self.keep_rating = False



        self.film_df.at[m1_index, 'Rating'] = m1_new_rate
        self.film_df.at[m2_index, 'Rating'] = m2_new_rate


        
    def random_comp_rater (self, win_pts = 5, lose_pts = -5, win_switch = True, bias_top = False, bias_bottom = False, bias_middle = False):
        # This rater assigns a set amount of winning points and losing points
        # If win_switch is True then the films switch places first
        
        # Create a temporary dataframe that excludes unrated films
        tmp_df = self.film_df[pd.notna(self.film_df.Rating)]

        title_n = len(tmp_df.Title)
        
        selection = random.sample(range(0,title_n), k=2)
         
        m1_index = selection[0]
        m2_index = selection[1]
        
        
        if bias_top:
            # 25% chance of being in the top 100
            if random.sample(range(0,4), k=1)[0] == 0: 
                m1_index = random.sample(range(0,100), k=1)[0]
            if random.sample(range(0,4), k=1)[0] == 0: 
                m2_index = random.sample(range(0,100), k=1)[0]
        
        if bias_bottom:
            # 25% chance of being in the bottom 10
            if random.sample(range(0,4), k=1)[0] == 0: 
                m1_index = random.sample(range(title_n-51, title_n-1), k=1)[0]
            if random.sample(range(0,4), k=1)[0] == 0: 
                m2_index = random.sample(range(title_n-101, title_n-1), k=1)[0]
        
        if bias_middle:      
            if random.sample(range(0,4), k=1)[0] == 0: 
                m1_index = int(len(self.film_df.Rating)/2 + 1)
            if random.sample(range(0,4), k=1)[0] == 0: 
                m2_index = int(len(self.film_df.Rating)/2)
            
        
        m1 = tmp_df.iloc[m1_index]['Full_Title']
        m2 = tmp_df.iloc[m2_index]['Full_Title']
        
        m1_index = self.return_film_index(m1)
        m2_index = self.return_film_index(m2)
        
        m1_old_rate = self.film_df.iloc[m1_index]['Rating']
        m2_old_rate = self.film_df.iloc[m2_index]['Rating']
        
        m1_new_rate = m1_old_rate
        m2_new_rate = m2_old_rate

        
        self.print_notice(m1, m2)
                
        user_choice = raw_input()

        if (user_choice == '1'):

            if ((win_switch) & (m1_old_rate <= m2_old_rate)):
                
                print ('Switch!')
                temp = m1_new_rate
                m1_new_rate = m2_new_rate
                m2_new_rate = temp
            
            m1_new_rate += win_pts
            m2_new_rate += lose_pts
         
                      
        if (user_choice == '2') :

            if ((win_switch)  & (m2_old_rate <= m1_old_rate)):
                
                print ('Switch!')
                temp = m1_new_rate
                m1_new_rate = m2_new_rate
                m2_new_rate = temp 
                             
            m2_new_rate += win_pts
            m1_new_rate += lose_pts  
            
        if (user_choice == 'C'):
            
            self.keep_rating = False


        #print m1_new_rate
        #print m2_new_rate
        
        self.film_df.at[m1_index, 'Rating'] = m1_new_rate
        self.film_df.at[m2_index, 'Rating'] = m2_new_rate

        #print (self.film_df.iloc[m1_index])
        #print (self.film_df.iloc[m2_index])
    
    
    def indv_place_rater(self):
        
        # Reorder a particular film in the database (somewhat approximate)
        # Warning: the film must already be rated in the database
        
        rater_complete = False
        tmp_df = self.film_df.sort_values(by=['Rating'], ascending=False) # Sort
        tmp_df = tmp_df[pd.notna(tmp_df.Rating)] # Exclude unrated
        
        # Request Film to Rate
        print ('Full Title (with year):')
        m1 = raw_input()
        # Throw up an error if it isn't found
        if (m1 not in tmp_df.values):
            print 'Error: Title not in database'
            rater_complete = True
        else:
            # Attributes of selected film
            m1_index = self.return_film_index(m1)
            m1_rating = self.return_film_rating(m1)
            
            # Drop it from the temporary dataframe
            tmp_df = tmp_df.drop([m1_index])
        while rater_complete == False:

            if len(tmp_df.Rating) > 3:
                
                
                m2_index = int(round(len(tmp_df.Rating) / 2))
                m2 = tmp_df.at[m2_index, 'Full_Title']
                
                self.print_notice(m1, m2)
                
                user_choice = raw_input()

                if (user_choice == '1'):
                    tmp_df = tmp_df[:m2_index]
                    
                if (user_choice == '2'):
                    tmp_df = tmp_df[m2_index:]
                    tmp_df = tmp_df.reset_index(drop=True) # Reset the index from 0
            
            else:
                
                m2_index = 1
                m2 =  tmp_df.at[m2_index, 'Full_Title']
                
                
                self.print_notice(m1, m2)
                
                user_choice = raw_input()

                if (user_choice == '1'):
                    m1_new_rating = int(tmp_df.at[m2_index, 'Rating'] + 5)
                if (user_choice == '2'):
                    m1_new_rating = int(tmp_df.at[m2_index, 'Rating'] - 5)

                print 'Complete!'
                #print tmp_df
                print 'Old rating:'
                print m1_rating
                print 'New Rating:'
                print m1_new_rating
                
                self.film_df.at[m1_index, 'Rating'] = m1_new_rating
                self.film_df = self.film_df.sort_values(by=['Rating'], ascending=False)
                rater_complete = True
                self.keep_rating = False


    def reorder_df(self):
        ## Change order of the dataframe based on the rating
        
        self.film_df = self.film_df.sort_values(by=['Rating'], ascending=False)
        self.film_df = self.film_df.reset_index(drop=True) # Reset the indices
        
        for i in range(0, len(self.film_df.Title)):
            
            # If highest, it gets ordered 1
            if i == 0:
                self.film_df.at[i, 'Order'] = 1
                
            else:
                
                # If rated the same as previous, then same order, else one higher
                if self.film_df.at[i, 'Rating'] == self.film_df.at[i-1, 'Rating']:
                    
                    self.film_df.at[i, 'Order'] = self.film_df.at[i-1, 'Order']
                
                else:
                    self.film_df.at[i, 'Order'] = self.film_df.at[i-1, 'Order'] + 1


        
    def save_df(self):

        self.reorder_df()        
        self.film_df.to_csv(self.save_file, index=False)
        
        
    
    def add_film(self):
        
        print 'Name of film:'
        
        prev_max_order = max(list(self.film_df['Order']))
                
        m_name = raw_input()
        
        print 'Year of release:'
        
        m_year = raw_input()
        
        m_rate = 100
        m_recently_added = max(self.film_df.Recently_Added) + 1
        
        df = pd.DataFrame({"Title":[m_name], 
                           "Full_Title":[m_name + ' (' + m_year + ')'],
                           "Year":[m_year],
                           "Rating":[m_rate],
                           "Recently_Added":[m_recently_added],
                           "Order": [prev_max_order + 1]
                           })
        
        self.film_df = self.film_df.append(df, sort=False)
        
        self.keep_rating = False
        
        
    def delete_film(self):
    
        # Request Film to Delete
        print ('Full Title (with year):')
        m1 = raw_input()
        # Throw up an error if it isn't found
        if (m1 not in self.film_df[['Full_Title']].values):
            print 'Error: Title not in database'
            
        else:
            self.film_df = self.film_df[self.film_df.Full_Title != m1]
            
        self.keep_rating = False
        
        
    def winnow_db(self):
        # The init_db has a value of NAN for the ratings of all films
        # This runs through each film with an NAN rating and asks you if you've seen it
        # If you have then it gives the film an initial rating of 100, otherwise the film is deleted
        

        # Create a temporary dataframe that includes only unrated films
        tmp_df = self.film_df[pd.isna(self.film_df.Rating)]    
        tmp_df = tmp_df.reset_index(drop=True) # Reset the indices
        
        title_n = len(tmp_df.Title)

        if title_n == 0:
            print 'No unrated films to winnow.'
            self.keep_rating = False
        
        t_index = 0 # index in temporary dataframe
        while (self.keep_rating):

            m = tmp_df.at[t_index, 'Full_Title'] 
            m_index = self.return_film_index(m) # index in full dataframe
            
            print "Have you seen this film? ('y' or 'n')"
            print m
            
            user_choice = raw_input()
            print

            if user_choice == 'y':
                self.film_df.at[m_index, 'Rating'] = 100

            if user_choice == 'n':
                self.film_df = self.film_df[self.film_df.Full_Title != m]

            if (user_choice == 'C'):
                self.keep_rating = False
            
            if (t_index == title_n-1):
                print 'Complete. No more unrated films to winnow (unless you skipped some).'
                self.keep_rating = False
                
            self.save_df()
            t_index += 1
            tmp_df = tmp_df[tmp_df.Full_Title != m]
            
    def print_notice(self, movie1, movie2):
        
        
        print 'Which do you like more:'
        print
        print '1. ' + str(movie1)
        print '2. ' + str(movie2) 
        
        
    def menu_options(self):
        
        
        print 'Pick a task:'
        print
        print '1. Random ELO rater'
        print '2. Random Comparison rater'
        print '3. Quick rate a film' 
        print '4. Add a film'
        print '5. Delete a film'
        print '6. Winnow the database'
        
        return raw_input()
               
    def begin_rater(self):
        
        while (True):
            
            self.keep_rating = True
            m_choice = self.menu_options()

            while (self.keep_rating):

                if (m_choice == '1'):
                    self.random_elo_rater()
                if (m_choice == '2'):
                    self.random_comp_rater()               
                if (m_choice == '3'):
                    self.indv_place_rater()   
                if (m_choice == '4'):
                    self.add_film()   
                if (m_choice == '5'):
                    self.delete_film()   
                if (m_choice == '6'):
                    self.winnow_db()              
                self.save_df()




'''
## For usage in Terminal, uncomment this
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python movierater2.py <input_movieratings> <output_movieratings>')
        sys.exit(1)
    in_f = sys.argv[1]
    out_f = sys.argv[2]
    x = rater(in_f, out_f)
    x.begin_rater()
'''



## For usage in IDE, uncomment this
x = rater('~/Desktop/output2.csv', '~/Desktop/output2.csv')
x.begin_rater()
