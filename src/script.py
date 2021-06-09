def welch_satterhwaithe_dof(sample_1, sample_2):
    ss1 = len(sample_1)
    ss2 = len(sample_2)
    dof = (
        ((np.var(sample_1)/ss1 + np.var(sample_2)/ss2)**(2.0)) / 
        ((np.var(sample_1)/ss1)**(2.0)/(ss1 - 1) + (np.var(sample_2)/ss2)**(2.0)/(ss2 - 1))
    )
    return dof