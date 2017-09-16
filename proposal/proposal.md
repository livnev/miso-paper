# Proposal:
The goal of this project is to design, build, and study a set of agent-based models for the Maker Dai ecosystem.

### Justification:
While considerable attention has been and continues to be paid to the technical integrity of the system, as it stands, no detailed research has been undertaken to evaluate the economic foundations on which it rests. It is vital for the success of the Dai Credit System that its economic mechanisms function properly under a variety of realistic conditions.

A detailed theoretical invesigation into the economic behaviour of the system, informed by both analytic techniques and computer simulations, has the potential to indicate scenarios where the system is economically fragile and provide guidance on design improvements to increase stability. Additionally, the work could serve as a valuable tool for future governors who will be responsible for setting the system's risk parameters.

### Methods:

This project will draw heavily on techniques from the field of Complexity Science, in particular it will use agent-based models to simulate behaviour of individual ecosystem participants to draw conclusions about the risks and stability of the system as a whole. Inspiration should be taken from the existing ABM literature and from the financial stability research by regulators and academics, which in the post-2008 years has particularly focused on designing systems that are resilient to "black swan" risks. Throughout, an "alarmist" perspective should be chosen over a "reassuring" one: highlighting a realistic disaster scenario for the DCS should be seen as a more worthy goal than assuring the community of the system's integrity.

The simulation environment will be designed in a modular way, to make it easy to compare behaviour across varying designs and assumptions. For example, a different controler governing the the Target Rate Feedback Mechanism (`vox`) can be swapped in and compared, or different market structure simulations can be used to evaluate the robustness of the model to implementation details.

The modular design of the framework should allow the project to remain agnostic (to the extent that is practical) on the particular design of the DCS contracts. For example, it should be possible to model both Sai and Dai (i.e. their current folklore specifications), as well as modifications to them, by modifying some parameters of the model. The reason for this choice is to allow the project to also function as a testing environment for suggesting possible changes to the economic mechanisms of the DCS.

The project should be in continuous discussion with other researchers in the field: there is an active community working on ABM research from whom much can be learned, and the conversation should be mutually beneficial since theoreticians will be interested to learn from the case study and data that the DCS will generate.

### Plan:

First, a basic object-oriented Python framework will be built to provide the "plumbing" that links together generic components such as the agents, trading venues, the components of the DCS itself, etc. Then simple implementations of the individual components themselves will be created, this will include designing decision logic for some types of agents, simulating the market structure, making some exogeneous "signals", and implementing a model (replica) of the core DCS contracts themselves. This will be enough to produce a proof-of-concept model which can then be tested with a selection of "sane" parameters.

Based on the results of the above, some components might require more sophisticated modelling. For example, a simple aggregate trading model can initially be used as the market venue, later it can be replaced with a more sophisticated limit order book model (there are descriptions of these designs in the literature [citation needed]). Market maker agents and arbitrageur agents may need to be designed and introduced in order to simulate realistic behaviour. A more fine-grained time evolution model may need to be used.

A collection of realistic exogeneous signals must be designed: e.g. collateral bear markets, high volatility markets, trader derisking scenarios, interest rate swings, etc. These could be time series derived from real historical market data, or time series that are stochastically generated with a particular model (ideally such a model should be one that adequately conveys fat-tailed/black swan behaviour, see Mandelbrot e.g. [5]). In the simplest case, these exogeneous signals will be separate and causally unrelated to the evolution of the simulated environment, but later it will make sense to consider cases where the exogeneous signal is affected by the simulation in some realistic way (so that the signal is no longer an "independent variable").

As traditionally done in the ABM literature, it is best to start with agents that follow very simple rules. This way, it is much easier to justify that the scenarios appearing in the simulation are realistic. However, eventually a multiagent Reinforcement Learning approach could be used to train more advanced agents whose behaviour is learned by interacting with the simulated environment and attempting to maximise a utility function (see OpenAI multiagent stuff e.g. [6]). Designing this will certainly be much more involved, and one must be able to argue that the learned behaviour is representative of real-world actors. However, it will have a chance of finding more complicated behavioural patterns and the systemic risks that arise from them.

The Reinforcement Learning approach could also be used to find exogeneous signals that lead to more obscure disaster scenarios: an adversarially generated signal (subject to certain realism constraints) can be trained to try to deliberately move the system into an undesirable state.

### References/Suggested Reading:

[1] - LeBaron, Blake. "Agent-based computational finance: Suggested readings and early research." Journal of Economic Dynamics and Control 24.5 (2000): 679-702.

[2] - LeBaron, Blake. "A builder’s guide to agent-based financial markets." Quantitative Finance 1.2 (2001): 254-261.

[3] - Fricke, Daniel, and Thomas Lux. "The effects of a financial transaction tax in an artificial financial market." Journal of Economic Interaction and Coordination 10.1 (2015): 119-150.

[4] - LeBaron, Blake. "Agent-based financial markets: Matching stylized facts with style." Post Walrasian Macroeconomics: Beyond the DSGE Model (2006): 221-235.

[5] - Mandelbrot, Benoit B. "Scaling in financial prices: I. Tails and dependence." (2001): 113-123.

[6] - OpenAI. "Learning to cooperate, compete, and communicate." (https://blog.openai.com/learning-to-cooperate-compete-and-communicate/)
