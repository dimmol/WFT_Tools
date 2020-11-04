# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 14:02:21 2020

@author: dmolokho
"""

import warnings
import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib
import matplotlib.pyplot as plt


matplotlib.rcParams['figure.figsize'] = (16.0, 12.0)
matplotlib.style.use('ggplot')

def best_fit_distribution(data, bins=200, ax=None):
    """Model data by finding best fit distribution to data"""
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0

    # Distributions to check

    
    DISTRIBUTIONS = [
        st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.burr12, st.cauchy,st.chi,st.chi2,st.cosine,
        st.erlang,st.expon,st.exponnorm,st.exponweib,st.exponpow,st.f,st.fatiguelife,st.fisk,
        st.foldnorm,st.frechet_r,st.frechet_l,st.genlogistic,st.genexpon, st.genpareto,
        st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
        st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
        st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace, st.levy, st.levy_l,
        st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
        st.nct,st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal, st.norminvgauss,
        st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,st.tukeylambda,
        st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy, st.trapz
    ] # These are crappy distributions: st.levy_stable, st.dweibull, st.gennorm, st.foldcauchy, st.dgamma,  

    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf

    # Estimate distribution parameters from data
    for distribution in DISTRIBUTIONS:

        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')

                # fit dist to data
                params = distribution.fit(data)

                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]

                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))

                # if axis pass in add to plot
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax)
                    end
                except Exception:
                    pass

                # identify if this distribution is better
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse

        except Exception:
            pass

    return (best_distribution.name, best_params)


def make_pdf(dist, params, size=10000):
    """Generate distributions's Probability Distribution Function """

    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]

    # Get sane start and end points of distribution
    start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
    end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)

    # Build PDF and turn into pandas Series
    x = np.linspace(start, end, size)
    y = dist.pdf(x, loc=loc, scale=scale, *arg)
    pdf = pd.Series(y, x)

    return pdf

if __name__ == '__main__':

    # USER INPUT
        
    # Data should be in the CSV file.
    # Column number in the CSV file. Note, column numbering starts with 0.
    # Ideally, top row of the CSV file should containt dataset name.
    
    # Path to the CSV file:
    file_path = r'.\DATA\rft.csv'
    
    # Just a bit that forms the header of the plot. Can be left unchanged.
    data_set_name = r'Loaded'
    
    # Number of the data column to load. Again, starts from 0!
    # col_number = [5]
    
    # END OF USER INPUT
    
    df = pd.read_csv('./LAS/XPT_HRLA_TLD_MCFL_037LTP.las', delim_whitespace=True, 
                 header=None, skiprows=67, usecols=[0,3,11,16], 
                 names=['Time', 'Depth', 'ETIM', 'QCP'])
    
    data = df.loc[(df['ETIM']>=524) & (df['ETIM']<=725), 'QCP']
    
    # data = pd.read_csv(file_path, header = 0, usecols = col_number)
    
    #data = data[data.iloc[:, 0] < 4500]
    
    # Plot for comparison
    plt.figure(figsize=(12,8))
    
    # ax = data.plot(kind='hist', bins=50, normed=True, alpha=0.5, color=list(matplotlib.rcParams['axes.prop_cycle'])[1]['color'])
    ax = data.plot(kind='hist', bins=50, density=True, alpha=0.5, color=plt.rcParams['axes.prop_cycle'].by_key()['color'][1])
    # Save plot limits
    dataYLim = ax.get_ylim()
    
    # Find best fit distribution
    best_fit_name, best_fit_params = best_fit_distribution(data, 1000, ax)
    best_dist = getattr(st, best_fit_name)
    
    # Update plots
    ax.set_ylim(dataYLim)
    ax.set_title(data_set_name + u' Data\n All Fitted Distributions')
    ax.set_xlabel(u'Gas Rate, MMscf/D')
    ax.set_ylabel('Frequency')
    
    # Make PDF with best params 
    pdf = make_pdf(best_dist, best_fit_params)
    
    # Display
    plt.figure(figsize=(12,8))
    ax = pdf.plot(lw=2, label='PDF', legend=True)
    data.plot(kind='hist', bins=1000, density=True, alpha=0.5, label='Data', legend=True, ax=ax)
    
    param_names = (best_dist.shapes + ', loc, scale').split(', ') if best_dist.shapes else ['loc', 'scale']
    param_str = ', '.join(['{}={:0.2f}'.format(k,v) for k,v in zip(param_names, best_fit_params)])
    dist_str = '{}({})'.format(best_fit_name, param_str)
    
    ax.set_title(data_set_name + u' data with best fit distribution \n' + dist_str)
    ax.set_xlabel(u'Gas Rate, MMscf/D')
    ax.set_ylabel('Frequency')