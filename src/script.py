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


def pop_proportions_test(m: int, X: int, n: int, Y: int, alfa: float=0.025) -> list[float, float, Callable[[float], float], float]:
    '''Calculates values for two sample test of population proportions.
    
    Keyword arguments:
    m, n -- population of first, second sample
    X, Y -- number of `successes` in first, second sample
    
    returns:
    diff_p -- difference between proportions of two samples
    proportion -- total proportion of 'successes'
    test_V -- variance of two sample test 
    test_dist -- stats.norm frozen rvs
    p_value  -- test p-value
    '''
    diff_p = (X / float(m)) - (Y / float(n))
    proportion = (X + Y) / float(m + n)
    test_V = ((X/m)*(1-(X/m))/m) + ((Y/n)*(1-(Y/n))/n)
    test_dist = stats.norm(0, np.sqrt(test_V))
    p_value = test_dist.cdf(diff_p)
    z_alpha = test_dist.ppf(alfa)
    return diff_p, proportion, test_V, test_dist, p_value, z_alpha

def plot_test_results(m, X, n, Y, title, savetofile, null_h=r'$H_0: p_1 = p_2$', alfa=0.025):
    '''plots results of p_value against test distribution
    '''
    diff_p, proportion, test_V, func, p_value, _ = pop_proportions_test(m, X, n, Y)
    fig, ax = plt.subplots(1, figsize=(16, 5))

    x = np.linspace(min(diff_p,2*func.ppf(alfa)), max(diff_p, 2*func.ppf(1- alfa)), num=250)
    ax.plot(x, func.pdf(x), linewidth=3, c='purple')
    ax.fill_between(x, func.pdf(x), where=(x <= func.ppf(alfa)),
                    color="red", alpha=0.5)
    ax.fill_between(x, func.pdf(x), where=(x >= func.ppf(1- alfa)),
                    color="red", alpha=0.5)
    fig.text(.36,.4, null_h, fontsize=40, color='b')
    fig.savefig(f'output/{savetofile}.png')
    fig.text(.2, .7, f'p-value = {p_value:.3}', fontsize='xx-large')
    ax.axvline(diff_p)
    fig.savefig(f'output/{savetofile}_p.png')

    ax.set_title(title)
    if func.ppf(alfa) < diff_p and diff_p < func.ppf(1- alfa):
        fig.text(.4,.3,'FAIL TO REJECT NULL HYPOTHESIS', fontsize='x-large', color='g')
    else:
        fig.text(.42,.3,'REJECT NULL HYPOTHESIS', fontsize='x-large', rotation=0, color='r')
    fig.savefig(f'output/{savetofile}_rej.png')

    return ax


def plot_edu(ed_pdf):
    fig, ax = plt.subplots()
    plt.style.use('bmh')

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

    ax.bar(labels, doc, width, bottom=lt_hs+hs_grad+aa+bach+mas+prof, label='Doctorate')
    ax.bar(labels, prof, width, bottom=lt_hs+hs_grad+aa+bach+mas, label='Professional')
    ax.bar(labels, mas, width, bottom=lt_hs+hs_grad+aa+bach, label='Masters')
    ax.bar(labels, bach, width, bottom=lt_hs+hs_grad+aa, label='Bachelors')
    ax.bar(labels, aa, width, bottom=lt_hs+hs_grad, label='AA')
    ax.bar(labels, hs_grad, width, bottom=lt_hs, label='HS Grad')
    ax.bar(labels, lt_hs, width, label='Less than HS')

    plt.xticks(fontsize=30)
    ax.set_xlabel('Age Categories',fontsize=30)
    ax.set_ylabel('Population',fontsize=30)
#     ax.set_title('Educational Degrees')
    ax.legend(loc='lower left', fontsize='xx-large')

    fig.savefig('output/edu_by_age.png')

    return ax


def plot_edu_pct(ed_pdf):
    fig, ax = plt.subplots()
    plt.style.use('bmh')
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
    
    ax.bar(labels, doc, width, bottom=lt_hs+hs_grad+aa+bach+mas+prof, label='Doctorate')
    ax.bar(labels, prof, width, bottom=lt_hs+hs_grad+aa+bach+mas, label='Professional')
    ax.bar(labels, mas, width, bottom=lt_hs+hs_grad+aa+bach, label='Masters')
    ax.bar(labels, bach, width, bottom=lt_hs+hs_grad+aa, label='Bachelors')
    ax.bar(labels, aa, width, bottom=lt_hs+hs_grad, label='AA')
    ax.bar(labels, hs_grad, width, bottom=lt_hs, label='HS Grad')
    ax.bar(labels, lt_hs, width, label='Less than HS')

    plt.xticks(fontsize=30)
    ax.set_title('Educational Degrees',fontsize=30)
    plt.yticks(fontsize=30)
    ax.set_ylabel('Population',fontsize=30)
    ax.legend(fontsize='xx-large')
    fig.savefig('output/edu_pct.png')

    return ax

def plot_workforce_proportions(m, X, n, Y, title, savetofile):
    p_1 = X / float(m)
    p_2 = Y / float(n)

    dist_1 = stats.norm(p_1, np.sqrt((p_1 * (1 - p_1)) / m))
    dist_2 = stats.norm(p_2, np.sqrt((p_2 * (1 - p_2)) / n))

    fig, ax = plt.subplots(1, figsize=(16, 3))
    lower = max(0., 0.95 * min(p_1, p_2))
    upper = min(1., 1.1 * max(p_1, p_2))
    x = np.linspace(lower, upper, num=2500)
    ax.plot(x, dist_1.pdf(x), linewidth=3, c='b', label='Veterans')
    ax.plot(x, dist_2.pdf(x), linewidth=3, c='r', label='Non-veterans')
    
    plt.xticks(fontsize=20)
    ax.set_title(title)
    ax.legend()
    fig.savefig(f'output/{savetofile}.png')
    
def test_report(m, X, n, Y, alfa=0.025):
    diff_p, proportion, test_V, dist, p_value, z_alpha = pop_proportions_test(m, X, n, Y)
    line0 = f'diff in proportion: {diff_p:2.4f}, total proportion: {proportion:2.3f}, variance: {test_V:2.5f}, p_value: {p_value:2.3f}, z_alpha: {z_alpha:2.3f}'
    line1 = f'Proportions - Sample 1: {X/m:2.3f}; Sample 2: {Y/n:2.3f}. Difference: {diff_p:2.3f}'
    line2 = f'The p-value is: {p_value:2.3f}, and the rejection thresholds are {dist.ppf(alfa):2.3f} and {dist.ppf(1 - alfa):2.3f}'
    if dist.ppf(alfa) < p_value and p_value < dist.ppf(1 - alfa):
        return line0, line1, line2, "For 'H_0 : p_1 = p_2', the tests fails to reject the null hypothesis"
    else:
        return line0, line1, line2, "For 'H_0 : p_1 = p_2', the test rejects the null hypothesis"
    
    
def one_dim_scatterplot(data, ax, jitter=0.2, **options):
    if jitter:
        jitter = np.random.uniform(-jitter, jitter, size=data.shape)
    else:
        jitter = np.repeat(0.0, len(data))
    ax.scatter(data, jitter, **options)
    ax.yaxis.set_ticklabels([])
    ax.set_ylim([-1, 1])
    ax.tick_params(axis='both', which='major', labelsize=15)