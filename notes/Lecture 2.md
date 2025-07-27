## [Uncertainty](https://cs50.harvard.edu/ai/notes/2/#uncertainty)

Last lecture, we discussed how AI can represent and derive new knowledge. However, often, in reality, the AI has only partial knowledge of the world, leaving space for uncertainty. Still, we would like our AI to make the best possible decision in these situations. For example, when predicting weather, the AI has information about the weather today, but there is no way to predict with 100% accuracy the weather tomorrow. Still, we can do better than chance, and today’s lecture is about how we can create AI that makes optimal decisions given limited information and uncertainty.

## [Probability](https://cs50.harvard.edu/ai/notes/2/#probability)

Uncertainty can be represented as a number of events and the likelihood, or probability, of each of them happening.

**Possible Worlds**

Every possible situation can be thought of as a world, represented by the lowercase Greek letter omega ω. For example, rolling a die can result in six possible worlds: a world where the die yields a 1, a world where the die yields a 2, and so on. To represent the probability of a certain world, we write P(_ω_).

**Axioms in Probability**

- 0 < P(_ω_) < 1: every value representing probability must range between 0 and 1.
    

- Zero is an impossible event, like rolling a standard die and getting a 7.

- One is an event that is certain to happen, like rolling a standard die and getting a value less than 10.

- - In general, the higher the value, the more likely the event is to happen.
- The probabilities of every possible event, when summed together, are equal to 1.

![Summing Probabilities](https://cs50.harvard.edu/ai/notes/2/lotp.png)

The probability of rolling a number _R_ with a standard die can be represented as P(_R_). In our case, P(_R_) = 1/6, because there are six possible worlds (rolling any number from 1 through 6) and each is equally likely to happen. Now, consider the event of rolling two dice. Now, there are 36 possible events, which are, again, equally as likely.

![36 Events](https://cs50.harvard.edu/ai/notes/2/36events1.png)

However, what happens if we try to predict the sum of the two dice? In this case, we have only 11 possible values (the sum has to range from 2 to 12), and they do not occur equally as often.

![Sum of Two Dice](https://cs50.harvard.edu/ai/notes/2/sumdice.png)

To get the probability of an event, we divide the number of worlds in which it occurs by the number of total possible worlds. For example, there are 36 possible worlds when rolling two dice. Only in one of these worlds, when both dice yield a 6, do we get the sum of 12. Thus, P(_12_) = 1/36, or, in words, the probability of rolling two dice and getting two numbers whose sum is 12 is 1/36. What is P(_7_)? We count and see that the sum 7 occurs in 6 worlds. Thus, P(_7_) = 6/36 = 1/6.

**Unconditional Probability**

Unconditional probability is the degree of belief in a proposition in the absence of any other evidence. All the questions that we have asked so far were questions of unconditional probability, because the result of rolling a die is not dependent on previous events.

## [Conditional Probability](https://cs50.harvard.edu/ai/notes/2/#conditional-probability)

Conditional probability is the degree of belief in a proposition given some evidence that has already been revealed. As discussed in the introduction, AI can use partial information to make educated guesses about the future. To use this information, which affects the probability that the event occurs in the future, we rely on conditional probability.

Conditional probability is expressed using the following notation: P(_a | b_), meaning “the probability of event _a_ occurring given that we know event _b_ to have occurred,” or, more succinctly, “the probability of _a_ given _b_.” Now we can ask questions like what is the probability of rain today given that it rained yesterday P(_rain today | rain yesterday_), or what is the probability of the patient having the disease given their test results P(_disease | test results_).

Mathematically, to compute the conditional probability of _a_ given _b_, we use the following formula:

![Conditional Probability Formula](https://cs50.harvard.edu/ai/notes/2/conditional.png)

To put it in words, the probability that _a_ given _b_ is true is equal to the probability of _a_ and _b_ being true, divided by the probability of _b_. An intuitive way of reasoning about this is the thought “we are interested in the events where both _a_ and _b_ are true (the numerator), but only from the worlds where we know _b_ to be true (the denominator).” Dividing by _b_ restricts the possible worlds to the ones where _b_ is true. The following are algebraically equivalent forms to the formula above:

![Equivalent Formulas](https://cs50.harvard.edu/ai/notes/2/conditionalequivalent.png)

For example, consider P(_sum 12 | roll six on one die_), or the probability of rolling two dice and getting a sum of twelve, given that we have already rolled one die and got a six. To calculate this, we first restrict our worlds to the ones where the value of the first die is six:

![Restricting the Worlds](https://cs50.harvard.edu/ai/notes/2/sumconditional1.png)

Now we ask how many times does the event _a_ (the sum being 12) occur in the worlds that we restricted the question to (dividing by P(_b_), or the probability of the first die yielding 6).

![Conditioned Probability](https://cs50.harvard.edu/ai/notes/2/sumconditional2.png)

## [Random Variables](https://cs50.harvard.edu/ai/notes/2/#random-variables)

A random variable is a variable in probability theory with a domain of possible values that it can take on. For example, to represent possible outcomes when rolling a die, we can define a random variable _Roll_, that can take on the values {_1, 2, 3, 4, 5, 6_}. To represent the status of a flight, we can define a variable _Flight_ that takes on the values {_on time, delayed, canceled_}.

Often, we are interested in the probability with which each value occurs. We represent this using a probability distribution. For example,

- P(_Flight = on time_) = 0.6
- P(_Flight = delayed_) = 0.3
- P(_Flight = canceled_) = 0.1

To interpret the probability distribution with words, this means that there is a 60% chance that the flight is on time, 30% chance that it is delayed, and 10% chance that it is canceled. Note that, as shown previously, the sum the probabilities of all possible outcomes is 1.

A probability distribution can be represented more succinctly as a vector. For example, **P**(_Flight_) = <_0.6, 0.3, 0.1_>. For this notation to be interpretable, the values have a set order (in our case, _on time, delayed, canceled_).

**Independence**

Independence is the knowledge that the occurrence of one event does not affect the probability of the other event. For example, when rolling two dice, the result of each die is independent from the other. Rolling a 4 with the first die does not influence the value of the second die that we roll. This is opposed to dependent events, like clouds in the morning and rain in the afternoon. If it is cloudy in the morning, it is more likely that it will rain in the afternoon, so these events are dependent.

Independence can be defined mathematically: events _a_ and _b_ are independent if and only if the probability of _a_ and _b_ is equal to the probability of _a_ times the probability of _b_: P(_a ∧ b_) = P(_a_)P(_b_).

## [Bayes’ Rule](https://cs50.harvard.edu/ai/notes/2/#bayes-rule)

Bayes’ rule is commonly used in probability theory to compute conditional probability. In words, Bayes’ rule says that the probability of _b_ given _a_ is equal to the probability of _a_ given _b_, times the probability of _b_, divided by the probability of _a_.

![Bayes' Rule](https://cs50.harvard.edu/ai/notes/2/bayesrule.png)

For example, we would like to compute the probability of it raining in the afternoon if there are clouds in the morning, or P(_rain | clouds_). We start with the following information:

- 80% of rainy afternoons start with cloudy mornings, or P(_clouds | rain_).
- 40% of days have cloudy mornings, or P(_clouds_).
- 10% of days have rainy afternoons, or P(_rain_).

Applying Bayes’ rule, we compute (0.1)(0.8)/(0.4) = 0.2. That is, the probability that it rains in the afternoon given that it was cloudy in the morning is 20%.

Knowing P(_a | b_), in addition to P(_a_) and P(_b_), allows us to calculate P(_b | a_). This is helpful, because knowing the conditional probability of a visible effect given an unknown cause, P(_visible effect | unknown cause_), allows us to calculate the probability of the unknown cause given the visible effect, P(_unknown cause | visible effect_). For example, we can learn P(_medical test results | disease_) through medical trials, where we test people with the disease and see how often the test picks up on that. Knowing this, we can calculate P(_disease | medical test results_), which is valuable diagnostic information.

## [Joint Probability](https://cs50.harvard.edu/ai/notes/2/#joint-probability)

Joint probability is the likelihood of multiple events all occurring.

Let us consider the following example, concerning the probabilities of clouds in the morning and rain in the afternoon.

|C = _cloud_|C = _¬cloud_|
|---|---|
|0.4|0.6|

|R = _rain_|R = _¬rain_|
|---|---|
|0.1|0.9|

Looking at these data, we can’t say whether clouds in the morning are related to the likelihood of rain in the afternoon. To be able to do so, we need to look at the joint probabilities of all the possible outcomes of the two variables. We can represent this in a table as follows:

|              | R = _rain_ | R = _¬rain_ |
| ------------ | ---------- | ----------- |
| C = _cloud_  | 0.08       | 0.32        |
| C = _¬cloud_ | 0.02       | 0.58        |

Now we are able to know information about the co-occurrence of the events. For example, we know that the probability of a certain day having clouds in the morning and rain in the afternoon is 0.08. The probability of no clouds in the morning and no rain in the afternoon is 0.58.

Using joint probabilities, we can deduce conditional probability. For example, if we are interested in the probability distribution of clouds in the morning given rain in the afternoon. P(_C | rain_) = P(_C, rain_)/P(_rain_) (a side note: in probability, commas and ∧ are used interchangeably. Thus, P(_C, rain_) = P(_C ∧ rain_)). In words, we divide the joint probability of rain and clouds by the probability of rain.

In the last equation, it is possible to view P(_rain_) as some constant by which P(_C, rain_) is multiplied. Thus, we can rewrite P(_C, rain_)/P(_rain_) = αP(_C, rain_), or α<0.08, 0.02>. Factoring out α leaves us with the proportions of the probabilities of the possible values of C given that there is rain in the afternoon. Namely, if there is rain in the afternoon, the proportion of the probabilities of clouds in the morning and no clouds in the morning is 0.08:0.02. Note that 0.08 and 0.02 don’t sum up to 1; however, since this is the probability distribution for the random variable C, we know that they should sum up to 1. Therefore, we need to normalize the values by computing α such that α0.08 + α0.02 = 1. Finally, we can say that P(_C | rain_) = <0.8, 0.2>.

## [Probability Rules](https://cs50.harvard.edu/ai/notes/2/#probability-rules)

- **Negation**: P(_¬a_) = 1 - P(_a_). This stems from the fact that the sum of the probabilities of all the possible worlds is 1, and the complementary literals _a_ and _¬a_ include all the possible worlds.
- **Inclusion-Exclusion**: P(_a ∨ b_) = P(_a_) + P(_b_) - P(_a ∧ b_). This can interpreted in the following way: the worlds in which _a_ or _b_ are true are equal to all the worlds where _a_ is true, plus the worlds where _b_ is true. However, in this case, some worlds are counted twice (the worlds where both _a_ and _b_ are true)). To get rid of this overlap, we subtract once the worlds where both _a_ and _b_ are true (since they were counted twice).
    
    > Here is an example from outside lecture that can elucidate this. Suppose I eat ice cream 80% of days and cookies 70% of days. If we’re calculating the probability that today I eat ice cream or cookies P(_ice cream ∨ cookies_) without subtracting P(_ice cream ∧ cookies_), we erroneously end up with ~~0.7 + 0.8 = 1.5~~. This contradicts the axiom that probability ranges between 0 and 1. To correct for counting twice the days when I ate both ice cream and cookies, we need to subtract P(_ice cream ∧ cookies_) once.
    
- **Marginalization**: P(_a_) = P(_a, b_) + P(_a, ¬b_). The idea here is that _b_ and _¬b_ are disjoint probabilities. That is, the probability of _b_ and _¬b_ occurring at the same time is 0. We also know _b_ and _¬b_ sum up to 1. Thus, when _a_ happens, _b_ can either happen or not. When we take the probability of both _a_ and _b_ happening in addition to the probability of _a_ and _¬b_, we end up with simply the probability of _a_.

Marginalization can be expressed for random variables the following way:

![Marginalization](https://cs50.harvard.edu/ai/notes/2/marginalization.png)

The left side of the equation means “The probability of random variable X having the value xᵢ.” For example, for the variable C we mentioned earlier, the two possible values are _clouds in the morning_ and _no clouds in the morning_. The right part of the equation is the idea of marginalization. P(_X = xᵢ_) is equal to the sum of all the joint probabilities of xᵢ and every single value of the random variable Y. For example, P(_C = cloud_) = P(_C = cloud, R = rain_) + P(_C = cloud, R = ¬rain_) = 0.08 + 0.32 = 0.4.

- **Conditioning**: P(_a_) = P(_a | b_)P(_b_) + P(_a | ¬b_)P(_¬b_). This is a similar idea to marginalization. The probability of event _a_ occurring is equal to the probability of _a_ given _b_ times the probability of _b_, plus the probability of _a_ given _¬b_ time the probability of _¬b_.

![Conditioning](https://cs50.harvard.edu/ai/notes/2/conditioning.png)

In this formula, the random variable X takes the value xᵢ with probability that is equal to the sum of the probabilities of xᵢ given each value of the random variable Y multiplied by the probability of variable Y taking that value. This makes sense if we remember that P(_a | b_) = P(_a, b_)/P(_b_). If we multiply this expression by P(_b_), we end up with P(_a, b_), and from here we do the same as we did with marginalization.

## [Bayesian Networks](https://cs50.harvard.edu/ai/notes/2/#bayesian-networks)

A Bayesian network is a data structure that represents the dependencies among random variables. Bayesian networks have the following properties:

- They are directed graphs.
- Each node on the graph represent a random variable.
- An arrow from X to Y represents that X is a parent of Y. That is, the probability distribution of Y depends on the value of X.
- Each node X has probability distribution P(_X | Parents(X)_).

Let’s consider an example of a Bayesian network that involves variables that affect whether we get to our appointment on time.

![Bayesian Network](https://cs50.harvard.edu/ai/notes/2/bayesiannetwork.png)

Let’s describe this Bayesian network from the top down:

- Rain is the root node in this network. This means that its probability distribution is not reliant on any prior event. In our example, Rain is a random variable that can take the values {_none, light, heavy_} with the following probability distribution:
    
|_none_|_light_|_heavy_|
|---|---|---|
|0.7|0.2|0.1|
    
- Maintenance, in our example, encodes whether there is train track maintenance, taking the values {_yes, no_}. Rain is a parent node of Maintenance, which means that the probability distribution of Maintenance is affected by Rain.
    
|R|_yes_|_no_|
|---|---|---|
|_none_|0.4|0.6|
|_light_|0.2|0.8|
|_heavy_|0.1|0.9|
    
- Train is the variable that encodes whether the train is on time or delayed, taking the values {_on time, delayed_}. Note that Train has arrows pointing to it from both Maintenance and Rain. This means that both are parents of Train, and their values affect the probability distribution of Train.
    
|R|M|_on time_|_delayed_|
|---|---|---|---|
|_none_|yes|0.8|0.2|
|_none_|no|0.9|0.1|
|_light_|yes|0.6|0.4|
|_light_|no|0.7|0.3|
|_heavy_|yes|0.4|0.6|
|_heavy_|no|0.5|0.5|
    
- Appointment is a random variable that represents whether we attend our appointment, taking the values {_attend, miss_}. Note that its only parent is Train. This point about Bayesian network is noteworthy: parents include only direct relations. It is true that maintenance affects whether the train is on time, and whether the train is on time affects whether we attend the appointment. However, in the end, what directly affects our chances of attending the appointment is whether the train came on time, and this is what is represented in the Bayesian network. For example, if the train came on time, it could be heavy rain and track maintenance, but that has no effect over whether we made it to our appointment.
    
|T|_attend_|_miss_|
|---|---|---|
|_on time_|0.9|0.1|
|_delayed_|0.6|0.4|
    

For example, if we want to find the probability of missing the meeting when the train was delayed on a day with no maintenance and light rain, or P(_light, no, delayed, miss_), we will compute the following: P(_light_)P(_no | light_)P(_delayed | light, no_)P(_miss | delayed_). The value of each of the individual probabilities can be found in the probability distributions above, and then these values are multiplied to produce P(_no, light, delayed, miss_).