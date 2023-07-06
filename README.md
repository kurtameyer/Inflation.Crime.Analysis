# Inflation.Crime.Analysis

This project was originally a group project written in R for my Statistics and Probability course taken Winter quarter 2023. I've reworked the data loading and cleaning portion of it in a Jupyter notebook and am turning it into a dashboard using Plotly and Dash. 




Our research focuses on the relationship between the inflation rate and crime rates, as well as the type of crime and its rate relative to the inflation. 
With this information, we would like to know if it is possible to predict an increase in crime and type of crime based on inflation rates. 

To measure the inflation rates, we used the Consumer Price Index (CPI) as our main metric, which is the measure of the average change in the prices paid by urban consumers for a market basket of consumer goods and services. 
The way CPI is calculated is: Value of Basket in the current year over the value of the basket in the prior year, times 100.


Data Sources and Definitions Explained

We based our research on data obtained from the St. Louis Federal Reserve [1] for the inflation rates data. Specifically, a dataset which includes data from the 1960s to the current era. 
As for crime rates, as well as types of crime, we obtained this information from the FBI Uniform Crime Reporting [2] dataset, which was supplemented with data obtained through Statista [3], for which we have access thanks to our student access through the University of Denver. 
Unfortunately, the FBI datasets are split by year, which would take too much time to put everything together. Fortunately, we could use disastercenter [4], which presents the same information already gathered.

[1]: https://fred.stlouisfed.org/
[2]: https://cde.ucr.cjis.gov/
[3]: https://www.statista.com
[4]: https://www.disastercenter.com/

Main Features of the Data Sets

We will first have to load the datasets and perform data cleaning. 

Rape statistics cannot be trusted, as prior to 2016, the FBI included only female-reported rapes, and from 2016 and forward, they included both male and female reported rapes. Therefore, we will not use it for our analysis, as it shows a massive jump in reports.
![image](https://github.com/kurtameyer/Inflation.Crime.Analysis/assets/107722456/2e780c4b-9338-4969-9335-750c75811e1d)
