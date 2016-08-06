import quandl
import pandas as pd
import numpy as np
import pickle 


def CATO_list():
    CATOs = pd.read_html('http://www.cpaontario.ca/admissions/apps/catos/catosdetail.aspx?VAL=955787')
    return CATOs[0].transpose()

print(CATO_list())
