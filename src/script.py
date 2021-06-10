import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
from typing import Callable


def welch_satterhwaithe_dof(sample_1: pd.DataFrame, sample_2: pd.DataFrame) -> float:
    ss1 = len(sample_1)
    ss2 = len(sample_2)
    dof = (
        ((np.var(sample_1)/ss1 + np.var(sample_2)/ss2)**(2.0)) / 
        ((np.var(sample_1)/ss1)**(2.0)/(ss1 - 1) + (np.var(sample_2)/ss2)**(2.0)/(ss2 - 1))
    )
    return dof


def pop_proportions_test(m: int, X: int, n: int, Y: int, alfa: float=0.05) -> list[float, float, Callable[[float], float], float]:
    '''Calculates p-value for two sample test of population proportions (binomial distribution).
    
    Keyword arguments:
    m, n -- population of first, second sample
    X, Y -- number of `successes` in first, second sample
    
    returns:
    proportion -- total proportion of 'successes'
    test_V -- variance of two sample test 
    test_dist -- stats.norm frozen rvs
    p_value  -- test p-value
    '''
    diff_p = (X / float(m)) - (Y / float(n))
    proportion = (X + Y) / float(m + n)
    test_V = ((X + Y) * proportion * (1 - proportion)) / (m + n)
    test_dist = stats.norm(0, np.sqrt(test_V))
    p_value = 1 - test_dist.cdf(diff_p)
    z_alpha = test_dist.ppf(alfa)
    return proportion, test_V, test_dist, p_value, z_alpha


def plot_test_results(ax, func, p_value, title, alfa=0.05):
    '''plots results of p_value against test distribution
    '''
    x = np.linspace(-1, 1, num=250)
    ax.plot(x, func.pdf(x), linewidth=3, c='purple')
    ax.fill_between(x, func.pdf(x), where=(x <= func.ppf(alfa)),
                    color="red", alpha=0.5)
    ax.fill_between(x, func.pdf(x), where=(x >= func.ppf(1- alfa)),
                    color="red", alpha=0.5)
    ax.axvline(p_value)
    # ax.axvline(diff.ppf(0.95))
    ax.set_title(title);
    return ax


def plot_edu(ax, ed_pdf):
    labels = ed_pdf.AgeGroup
    Pop = ed_pdf.Pop
    lt_hs = ed_pdf.lt_HS
    hs_grad = ed_pdf.HS_Grad
    aa  = ed_pdf.AA
    bach = ed_pdf.Bachelors
    mas = ed_pdf.Masters
    prof = ed_pdf.Professional
    doc = ed_pdf.Doctorate
    width = 0.35

    ax.bar(labels, lt_hs, width, label='Less than HS')
    ax.bar(labels, hs_grad, width, bottom=lt_hs, label='HS Grad')
    ax.bar(labels, aa, width, bottom=lt_hs+hs_grad, label='AA')
    ax.bar(labels, bach, width, bottom=lt_hs+hs_grad+aa, label='Bachelors')
    ax.bar(labels, mas, width, bottom=lt_hs+hs_grad+aa+bach, label='Masters')
    ax.bar(labels, prof, width, bottom=lt_hs+hs_grad+aa+bach+mas, label='Professional')
    ax.bar(labels, doc, width, bottom=lt_hs+hs_grad+aa+bach+mas+prof, label='Doctorate')

    ax.set_ylabel('Population')
    ax.set_title('Educational Degrees')
    ax.legend()

    return ax


def plot_edu_pct(ax, ed_pdf):

    labels = ed_pdf.AgeGroup
    Pop = ed_pdf.Pop
    lt_hs = ed_pdf.lt_HS_pct
    hs_grad = ed_pdf.HS_pct
    aa  = ed_pdf.AA_pct
    bach = ed_pdf.Bach_pct
    mas = ed_pdf.M_pct
    prof = ed_pdf.Prof_pct
    doc = ed_pdf.Doc_pct
    width = 0.35 

    ax.bar(labels, lt_hs, width, label='Less than HS')
    ax.bar(labels, hs_grad, width, bottom=lt_hs, label='HS Grad')
    ax.bar(labels, aa, width, bottom=lt_hs+hs_grad, label='AA')
    ax.bar(labels, bach, width, bottom=lt_hs+hs_grad+aa, label='Bachelors')
    ax.bar(labels, mas, width, bottom=lt_hs+hs_grad+aa+bach, label='Masters')
    ax.bar(labels, prof, width, bottom=lt_hs+hs_grad+aa+bach+mas, label='Professional')
    ax.bar(labels, doc, width, bottom=lt_hs+hs_grad+aa+bach+mas+prof, label='Doctorate')

    ax.set_ylabel('Population')
    ax.set_title('Educational Degrees')
    ax.legend()

    return ax