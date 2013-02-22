pyquizlet
=========

python wrapper for the quizlet API
https://quizlet.com/api/2.0/docs/

usage:

import pyquizlet

quizlet = pyquizlet.Quizlet('XXXX')
s = quizlet.search_sets('Spanish')
s = quizlet.get_set('6009523', paged=False)
