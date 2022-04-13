# Real Estate Flipping Houses - House Rocket

 <p align="center"><img width="40%" alt="drawing" src="/house_rocket/house-rocket-logo.jpg"></p>

This repository contains codes for the porfolio analysis of a real estate company. <br>

#### Real Estate Flipping Houses - House Rocket
The objetives of this project are:
* Perform exploratory data analysis on properties available on the dataset.
* Determine which properties should be purchased according to business criteria.
* Develop an online [dashboard](https://kc-house-dashboard2.herokuapp.com/) that can be acessed by the CEO from a mobile or computer.
<br>

## 1. Business Problem
* House Rocket is a Real Estate Flipping Houses business that goes on digital platform to buy and sell houses by using technology.
    
 * My goal is to help the company find the best business opportunities in the real estate market. The CEO of House Rocket would like to maximize the company's revenue by finding good business opportunities.
    
 * Their main strategy is to buy good homes in great locations at low prices and then resell them later at higher prices. The greater the difference between buying and selling, the greater the company's profit and therefore the greater its revenue.<br>

The [dashboard](https://kc-house-dashboard2.herokuapp.com/) must contain:

   * Which properties the company should buy.
   * A map view with properties available.
   * A table view with attributes filters.
   * Expected profit from each property.<br><br>


<!--<img src="https://user-images.githubusercontent.com/77681284/152690550-fc5b1c2e-6cf6-4bb5-ae7d-0b19b936ac0d.png"/>-->


<!-- <img src="https://user-images.githubusercontent.com/77681284/117519523-439a7900-af7a-11eb-8cf0-4900c78737e4.png" alt="image" width="200" align="right"/>
<img src="https://user-images.githubusercontent.com/77681284/152690450-089c6833-edbe-4eb2-bfa6-261973611e3a.png" alt="dashboard screenshot" width="300"  align="right"/> -->

## 2. Business Results

From all the 21,421 houses available in the dataset and based on business criteria, where we considered houses that should be bought only with great conditions (conditions 4 and 5) and low prices, **3,826** houses should be bought by House Rocket resulting on a US$451M profit.<br>

Maximum Invested Amount: US$1,506,297,223.00<br>
Maximum Revenue: US$1,958,186,389.90<br>
Maximum Expected Profit: US$451,889,166.90<br>

This results on a 30.0 % gross revenue.
<br><br>

## 3. Business Assumptions
* The data available is only from May 2014 to May 2015.
* Properties with bedrooms disproportional with interior living squarefoot were deleted, assuming it was a input error.
* Business criteria to determine whether a property should be bought are:
   * Property must have a 'condition' equal or higher than 4.
   * Property price must be below or equal the median price based on the zipcode.

<details><summary>The variables on original dataset goes as follows:</summary><br>

Features | Definition
------------ | -------------
|id | Unique ID for each property available|
|date | Date that the property was available|
|price | Sale price of each property |
|bedrooms | Number of bedrooms|
|bathrooms | Number of bathrooms, where .5 accounts for a room with a toilet but no shower, and .75 or ¾ bath is a bathroom that contains one sink, one toilet and either a shower or a bath.|
|sqft_living | Square footage of the apartments interior living space|
|sqft_lot | Square footage of the land space|
|floors | Number of floors|
|waterfront | A dummy variable for whether the apartment was overlooking the waterfront or not|
|view | An index from 0 to 4 of how good the view of the property was|
|condition | An index from 1 to 5 on the condition of the apartment|
|grade | An index from 1 to 13, where 1-3 falls short of building construction and design, 7 has an average level of construction and design, and 11-13 have a high quality level of construction and design.|
|sqft_above | The square footage of the interior housing space that is above ground level|
|sqft_basement | The square footage of the interior housing space that is below ground level|
|yr_built | The year the property was initially built|
|yr_renovated | The year of the property’s last renovation|
|zipcode | What zipcode area the property is in|
|lat | Lattitude|
|long | Longitude|
|sqft_living15 | The square footage of interior housing living space for the nearest 15 neighbors|
|sqft_lot15 | The square footage of the land lots of the nearest 15 neighbors|
</details>

<details><summary> Variables created during the project development goes as follow:</summary><br>

Variable | Definition
------------ | -------------
| decision | whether a property should be bought |
| median_price_zipcode | median price of zipcode region |
| sale_price | 30% more on buying price, if property should be bought |
| profit | difference between buying price and selling price suggestion  |
| dist_fromlake | distance from the center of Evergreen Point Floating Bridge |

</details>
<br>

## 4. Solution Strategy
1. Understanding the business problem
2. Collecting the data
3. Data Description
4. Data Filtering
5. Feature Engineering
6. Exploratory Data Analysis
7. Insights Conclusion
8. Dashboard deploy on [Heroku](https://kc-house-dashboard2.herokuapp.com/) 
<br>

## 5. Top 4 Data Insights

1. Houses prices with conditions 4 and 5 correspond to 48,45% of the total sum of the base prices.

2. 50% of the houses that should be bought are located within 15km radius from the lake, which correspond to 1888 houses.

3. Average house prices decrease as distance from lake increases 

4. Houses that were suggested to be bought within 15km radius from lake correspond to  63.23% of expected profit.
<br>

## 6. Conclusion
The objective of this project was to create a online dashboard to House Rocket's CEO. Deploying the dashboard on Heroku platforms provided the CEO access from anywhere and improve business decisions and insights.
<br><br>

## 7. Next Steps
* Determine which season of the year would be the best to execute a sale.
* Get more address data to fill NAs.
* Expand this methodology to other regions that House Rocket operates.
* Cross the available data with macroeconomics data such as GDP, Inflation Rate, Unemployment Rate, etc.
* Cross the available data with weather conditions data.
* Apply machine learning algorithms to predict prices.
<br>

---
## References:
* Dataset House Sales in King County (USA) from [Kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction)
* Features definitions [Kaggle discussion](https://www.kaggle.com/harlfoxem/housesalesprediction/discussion/207885)
* Python from Zero to DS lessons on [Youtube](https://www.youtube.com/watch?v=1xXK_z9M6yk&list=PLZlkyCIi8bMprZgBsFopRQMG_Kj1IA1WG&ab_channel=SejaUmDataScientist)
* Blog [Seja um Data Scientist](https://sejaumdatascientist.com/os-5-projetos-de-data-science-que-fara-o-recrutador-olhar-para-voce/)


