define the domain containing domain name, predicates, actions, effects.
define a problem by setting the domain, some initial values and the desired goal.
use a planner like fast downward/FF etc to solve the problem and get the corresponding plan as output. See practical slides '07 AI Planning Tools'.
Based on the output plan, call a function to carry out further steps (ex: switching on the fan, displaying a meesage)