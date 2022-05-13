from scipy.stats import pearsonr
from scipy.stats import spearmanr


compressors = ["NUHT", "bzip2", "MFC", "Jarvis", "zstd"]
realms = ["Viral", "Bacteria", "Archaea", "Fungi", "Protozoa"]
F1score = [0.5128, 0.5789, 0.5946, 0.6286, 0.6154,
           0.1053, 0.3077, 0.1250, 0.2069, 0.3529,
           0.4444, 0.2941, 0.2353, 0.3556, 0.5263,
           0.1379, 0.4375, 0.4324, 0.5625, 0.3571,
           0.3684, 0.3784, 0.4000, 0.4103, 0.4390]

Compression_rate=[0.2800,0.3103,0.2780,0.2522,0.3284,
                  0.2565,0.2790,0.2334,0.2322,0.2976,
                  0.2545,0.2780,0.2318,0.2305,0.2967,
                  0.2563,0.2879,0.2398,0.2393,0.3130,
                  0.2505,0.2742,0.2230,0.2208,0.2972]


"""
    Correlation
    The value must be interpreted, where often a value below -0.5 or above 0.5
    indicates a notable correlation, and values below those values suggests a 
    less notable correlation.
"""

corr, _ = pearsonr(F1score, Compression_rate)
print('Pearsons correlation: %.3f' % corr, end = '. ')
if corr<0.5 and corr>-0.5:
    print("NO notable correlation!")
else:
    print("Variables are correlated!!")


corr, _ = spearmanr(F1score, Compression_rate)
print('Spearmans correlation: %.3f' % corr, end = '. ')
if corr<0.5 and corr>-0.5:
    print("NO notable correlation!")
else:
    print("Variables are correlated!")