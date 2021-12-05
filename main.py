from sys import exit
try:
    import data.core as core
except:
    exit('Critical error - Core is corrupt or non-existent!!!')

print('Preinitialization calls initialization')

core.initial()

core.logger('Postinitialization completed', 'POST')

