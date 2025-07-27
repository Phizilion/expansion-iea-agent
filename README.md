# Expansion IEA agent

## Disclaimer: this is an experiment in development. Results can be various, including uncontrollable harmful behaviour and other unwanted activity. Be careful with running this code and giving an access to important systems. For preventing any possible risks, run this code only in isolated and controllable environment. You are solely responsible for the consequences of running this code. 

### About

IEA = Independent Economic Activity 

This project is attempt to prove that it's possible to create LLM agent able to be economically independent, including able to expand own abilities and scale.

### Starter-pack possibilities

#### Targeting
Main cycle
1. Think about given target directly. 
2. Determine, whether the agent can make target task directly.
3. If it can't: redefine as step-by-step plan on one level lower. On every point, go to step 1.
4. If it can: do target task.


#### Information exploration
Agent use it when some info required
1. Ask internal knowledge
2. Ask embeddings based database with request self-correction
3. Ask search engines with request self-correction
4. Do own conclusion based on research around all available information


#### Self code modification (read, modify, test, debug pipeline)
Agent use it when need add or modify some tools / modify prompts
1. Read current agent's code
2. Modify code for getting new possibilities
3. Run modified code in test environment
4. Test it, using full access to test environment.
5. If needed, debug, modify and test it again (while code will not work as task require)
6. When code works as required, apply it to current running agent. Stop current version, replace code, run again.

