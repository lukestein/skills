# Farzad Saidi - Aging at The Very Top

## Opening

Thank you very much for putting the paper on the program. This is joint work with Valentin Klotzki, who is with us here today, and Alessandro Lizzeri.

Given the theme of this conference, what we mean by the very top is, of course, the very top of corporations, and therefore CEOs. It seems that they are getting older, not only here but also in Europe, leading some commentators to go so far as to call this America's corporate gerontocracy. Whether that is concerning or not is an open question.

What we are going to do today is ask three questions: how have age structures among CEOs changed, how could this be related to employment histories and career paths before becoming CEO, and which market features can explain these trends?

To answer those questions, we first document the development of CEO age across firms and over time, then use granular data to discern structural changes in employment histories leading up to CEO appointment, and then explore factors that have contributed to older CEO appointments since 2000.

## Main Results

As a short preview of the results, CEO age at appointment has increased substantially since 2000, by up to eight years. For comparison, that is much more than the aging of the college-educated labor force, about three times as much. Not only has CEO age gone up, but the career paths of prospective CEOs have also changed: they now amass much more external experience and exhibit greater labor market mobility.

Our interpretation is that this reflects the accumulation of generalist skills. On the one hand, firms increasingly demand generalist skills in order to navigate an uncertain and complex world. On the other hand, executives, being career-minded individuals, respond to that greater demand by steering their career paths accordingly. We show causal evidence for both the demand and supply sides of generalist skills, and then engage in a quantitative decomposition of the aggregate trend. Our conclusion is that the demand side seems to hold the greatest explanatory power for the observed increase in CEO age.

## Data and Stylized Facts

Before getting to the stylized facts, let me say a word about the data. On the one hand, we use BoardEx. I do not think I have to introduce that data set to this audience. But we also complement BoardEx with LinkedIn data. The way I would like you to think about the LinkedIn data is as a poor person's matched employer-employee data set that lets you dig deeper into people's employment histories. We combine it with BoardEx at the firm level using a fuzzy merge algorithm and have been fairly successful with that, matching 65%.

Without further ado, the raw facts. As I mentioned before, CEOs have aged more than the college-educated labor force or the regular labor force. You might immediately think this is due to entrenchment or longer tenure, but the slope of this phenomenon is, for most of our sample period, similar for sitting CEOs and CEOs upon appointment, so that does not seem to be the driver.

We can also see this in cumulative distribution functions. Every decade they move further to the right, with CEOs getting older upon appointment. This is especially pronounced for smaller firms. When we zoom in on what could be correlated with higher CEO age, it seems that years of external experience have gone up rather than internal experience.

Regardless of whether we are looking at internally promoted or externally appointed CEOs, both groups have amassed more external experience before becoming CEO. Again, this is more pronounced for smaller firms. Looking more closely at where that external experience comes from, it reflects a larger number of positions at more firms, and more sector switching. Along the intensive margin, they spend fewer years per position and per firm, but the net effect is still positive.

## Model

What I would like to do next is walk you through the bare bones of the theoretical model we have in the paper, to discipline our thinking about the determinants of CEO age.

In short, we have a frictionless many-to-one matching model with transfers among heterogeneous workers and heterogeneous firms. Workers are heterogeneous along two dimensions: ability and experience. Both have components that are concave functions of age. Firms are heterogeneous in productivity, which is related to firm size. Each firm also has a fixed number of hierarchically ordered positions with different productivity requirements.

As a result of assortative matching, each firm picks the most productive worker for its most important job, namely the CEO position. From this, we derive a set of key results that we develop further in the paper.

First, on average, CEOs of smaller, lower-productivity firms are younger. Then, in a comparative static, we increase alpha, the weight placed on experience in determining a worker's productivity at a given firm. When alpha rises, CEO age rises across the board, but especially at smaller firms. The reason is that large firms already benefit from assortative matching and self-selection into highly experienced, highly productive workers, so the reordering is stronger among smaller firms.

We also provide a simple numerical example that captures this intuition. It helps explain how firms' demand for experience can drive CEO age. Why might firms demand experience in this way? Possibly because experience comes with generalist skills. And why might firms want generalist skills in a CEO? Potentially to navigate an increasingly uncertain and complex world.

## Demand for Generalists

In the paper, we are fairly open about what exactly defines that uncertain and complex world, but you can think of it in terms of industry-level uncertainty, such as more volatile cash flows, business diversification across segments, spatial diversification as firms spread operations across the country, or trade complexity as firms expand international networks and face more unfamiliar environments. For all these reasons, it can be extremely valuable ex ante to have a generalist CEO.

To address the potential endogeneity of CEO age at appointment to industry-level uncertainty, we use plausibly exogenous spatial variation in the availability of young generalists. The idea is that if industry-level uncertainty truly increases demand for generalist skills, then the local availability of young generalists should matter for the age of the subsequently appointed CEO.

Who are these young generalists? We focus on top strategy consultants, specifically from McKinsey, BCG, and Bain. These are pressure cookers for generalists. In your first few years there, you see many industries and many firms at a very fast pace, so these workers accumulate generalist skills unusually quickly.

Our measure uses metro-area variation in flight time to the closest McKinsey, BCG, or Bain office. This exploits two sources of variation: first, the opening of new offices since 2000, and second, changes in air-route connectivity. Together these generate time variation in access to nearby generalist talent.

We then relate CEO age at appointment to an interaction between uncertainty and a measure of low supply of young generalists, proxied by flight time to the nearest McKinsey, BCG, or Bain office. The identifying variation is at the industry by metro-area by time level, allowing us to control simultaneously for time-varying unobserved heterogeneity at both the metro-area and industry levels.

Our conjecture is that when uncertainty is high, CEO age should rise more when the supply of young generalists is low, because firms would like to hire generalists but cannot easily access them. In that case, they hire older CEOs who accumulated comparable experience elsewhere, but more slowly. That is exactly what we find. The key coefficient is positive and significant throughout. In economic terms, at one standard deviation above mean uncertainty, an additional hour of travel time translates into a CEO who is seven to eight months older at appointment.

We find analogous results for other drivers of demand for generalist skills, including trade-induced complexity, business diversification, and spatial diversification. The broader picture is that multiple forms of complexity push firms toward demanding more generalist skills.

## Effects of Older CEOs

This also gives us a unique opportunity to estimate the causal effects of appointing an older CEO on firm performance.

The strategy is a two-step procedure. In the first step, we estimate firm-level outcomes on CEO-by-firm fixed effects. These fixed effects capture the average performance of a given CEO in a given firm along particular dimensions. In the second step, we relate those fixed effects to the CEO's age at appointment, instrumenting CEO age with the low-supply-times-uncertainty interaction I showed earlier.

What do we find? Older CEOs at appointment have a negative effect on employment growth and on R&D growth. They also adversely affect patenting behavior, especially computing-related patenting, which may confirm the fear that older leaders are less likely to sit at the technological frontier.

There is, however, a brighter side. These firms are rational in hiring such CEOs. Older CEOs appear better at dampening the consequences of business-cycle shocks. So this may be a world with lower risk, but also lower return.

## Supply-Side Response

Now, outside the scope of the model, because we do not endogenize skill supply there, we can still look empirically at whether executives adapt their career paths in response to this secular increase in demand for generalist skills.

The sufficient statistic we use is downward job switching across firms, that is, moves to less senior positions. We focus on these because they are consistent with acquiring general skills while potentially sacrificing some salary growth. Imagine moving from pharma to tech in order to experience something new. You may start in a lower-ranked position, but you broaden your profile and become more of a generalist.

If we look at the share of CEOs who ever moved downward across firms in their careers, that fraction rises dramatically from 17% to 41%. So this increasingly seems to be part of the path to the top.

Of course, one might argue that these downward moves are involuntary. That is why we need an identification strategy to isolate voluntary moves. We do so by following the idea that workers emulate the successful career paths of former co-workers. If one of your former co-workers becomes a CEO elsewhere, you may ask what it took for that person to become successful, and whether downward mobility might be beneficial in the long run.

This gives rise to a difference-in-differences design centered on such information shocks. The treatment is a former co-worker becoming a CEO within ten years after leaving a firm, having switched firms at least once. We compare workers who had been in the same firm and same seniority level as that person, but where the treated group also shared the same metro area and the control group did not. We focus on firms operating in multiple metro areas so that this comparison is meaningful.

The treated group is thus more connected to the former co-worker who became CEO, so the information shock should be stronger. We regress worker outcomes on this information shock, which varies at the firm by seniority level, and exploit within-firm-by-seniority variation across metro areas while controlling for worker and firm-seniority-by-year fixed effects.

The coefficient of interest compares job-mobility changes around the CEO-promotion event for co-workers who were more connected versus less connected to the future CEO. We find that the more connected workers are 5% more likely to switch firms during the subsequent ten-year window. This is not driven by upward or lateral moves. It is driven entirely by downward moves, and because downward moves are a subset of all switches, the relative effect there is even larger, around 13%. They also switch industries more often, by about 6%.

We then look at several comparative statics. The effects are stronger for workers with longer shared tenure with the future CEO. In other words, the better you knew the future CEO, the more likely you are to emulate that person's subsequent career path. The effects are also stronger when the CEO's own path to the top involved downward moves.

Finally, to show that these downward moves are plausibly motivated by the pursuit of general skills, we show that treated workers exhibit lower short-run imputed salary growth. So they do appear to be sacrificing some salary growth, likely because they are moving into less senior roles in order to accumulate broader skills.

## Decomposition and Conclusion

The last thing we do, after establishing both demand-side and supply-side explanations for higher CEO age at appointment, is to decompose the trend.

We regress CEO age on different combinations of fixed effects. Our full model includes industry-by-MSA-by-year fixed effects plus industry-by-MSA fixed effects interacted with firm-level controls. This full model explains 57% of the variation.

We then move to less granular specifications, including industry-by-time effects, MSA-by-time effects, and their combination. The intuition is that demand-side factors are captured by sectoral shifts, while supply-side factors hinge more on spatial variation, such as local availability of generalists.

We then use Shapley values to uniquely decompose the R-squared of the full model, since Shapley values are invariant to the order in which regressors are added. We find that, of the 57% explained by the full model, demand accounts for 37%, supply accounts for 28%, and the interaction accounts for 35%.

So the vast majority of what we can explain involves a demand-side component in one way or another.

To conclude, in this paper we document a pervasive upward age trend among CEOs. We show that this is related to firms' greater demand for general skills, which help them navigate greater uncertainty and complexity. There is also a supply-side response, in that executives strategically increase job mobility in order to provide those generalist skill sets.

We provide evidence that having older CEOs at the helm has negative effects on firm growth and computing-related innovation, and that carries broader aggregate implications. First, this likely does not bode well for firms' adaptability to long-term challenges. Second, it may teach us something about changing life-cycle earnings patterns at the very top, though that is a topic for another day.

Thank you very much. I am very much looking forward to Charlie's expert comments.
