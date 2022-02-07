# The impact of HIV on the life expectancy in Africa 
Group 7: Simon Sasse, Florian Suhre, Sina Hummerich
<br><br>
This visualization was developed within the context of the course "Data Visualization W21/22" at Freie Universität Berlin.

## Context

AIDS is the final stage of an HIV infection and was first diagnosed in 1981. It is an immunodeficiency disease which is so far not curable. HIV is most commonly contracted through unprotected sexual intercourse and drug consumption. Many lack the necessary education and thus do not know exactly how to protect themselves from the infection. Due too the missing education and since the medical treatment only developed over time, the deaths caused by HIV and Aids in the past left a visible mark in the development of the life expectancy and until this day, HIV/Aids is one of the main causes of death in some places. Three data sets were combined to show the described correlation, since we also wanted to take other causes of death that could have influenced the life expectancy into consideration.<br>
The purpose of our visualization is to raise awareness about this problem. The map shows the development of the spread of HIV and Aids over time and it can be seen that especially in the south of Africa many people lost their lifes because of this illness. It is important to educate about this topic and students could benefit by knowing about this disease since it helps to understand facts about the African continent. Especially, the option to compare multiple countries shows the different developments over time and the effect the death rates caused by HIV and Aids had on the life expectancy. Additionally, it is important to educate about how to stop the spread of this so far uncurable disease.


## Domain problem characterization
With our visualization, we want to show the spread of HIV and Aids from 1990 until 2019 and raise awareness about the impact that HIV had on the development of the life expectancy in some countries. We want to demonstrate this on the example of the African continent. Our target audience are high school students from different countries. Since we are focusing on students, we included some informational texts, that describe what is seen in the visualization. Nevertheless, we also think it should be a little challenging since it is for educational purposes.
 
## Data abstraction
For the visualization three different data sets from ourworldindata.org were used. One describes the Life Expectancy, a second one adresses the HIV death rates and lastly a data set that contains the share of death by cause in different countries to take other reasons for the development of the life expectancy into consideration. Each Data Set consists of entity, ISO-Code and year. The Life Expectancy Set additionally includes the average life expectancy from 1950 until 2019 and the HIV Set the death rate caused by HIV and Aids from 1990 until 2019.  The last data set shows the percentage of different death causes, e.g. Cardiovascular diseases or Malaria, in each country from 1990 until 2019. The data of the two sets regarding death rates originate from the Global Burden of Disease Collaborative Network of the Institute for Health Metrics and Evaluation. The information on life expectancy that was important for our time period is based on the data by United Nations Population Division, who update the data yearly. Since we did not have data reagrding HIV and Aids we shortened the set to a time period from 1990 until 2019. <br> 
Since the data sets contained information about all countries of the world, we filtered the data by using the Alpha 3 country codes of Africa (https://www.nro.net/list-of-country-codes-in-the-afrinic-region/).  
<br>
<br>
Life Expectacy https://ourworldindata.org/grapher/life-expectancy?time=1544&country=BWA~NAM~ZAF~SWZ~TZA~ZMB<br>
Aids death Rate: https://ourworldindata.org/grapher/hiv-death-rates?time=2018<br>
Share of death by cause: https://ourworldindata.org/grapher/share-of-deaths-by-cause?time=2002..2003<br>

## Visual encoding and interaction design	
The landing page shows a map of the African continent. Underneath the map, a timeline going from 1990 until 2019 is displayed. Each country is colored in a tone of red. The intensity shows the number of HIV deaths per 100,000 residents in the selected year. An animation can be started via a play button which shows the development of the HIV deaths over time. To see the values of a specific year, the animation can be paused or alternatively clicked on in the timeline. Hovering over a country shows the name of the country, the rate of HIV deaths in this country and the life expectancy. <br>
Clicking on a country opens two diagrams underneath the map: a bubble chart and a bar chart. In the bubble chart, the y-axis describes the life expectancy, while the x-axis shows the year. The circle size represents the HIV death rate in the selected country. It can be recognized that in many countries the circle size correlates in a way to the life expectancy, so the bigger the circles get, the lower the life expectancy is. By clicking on another country, the bubble chart gets added in a different color and two or more countries can be compared. Alternatively, the countries can be selected via a drop-down menu and deselected by clicking the cross next to the countries listed above the diagram. The bar chart next to the bubble chart shows the top ten death causes (y-axis) in one country in percent (x-axis) in a year. By hovering over the different circles in the bubble graph, the bar charts are changing according to the chosen year. HIV/Aids is colored in red to make it more prominent, while the other causes are colored in tones of grey.

## Reflection
Furthermore, reflect on your result and your learnings. What did not work as expected (and why)? What would you improve if you had more time? If you used other libraries or frameworks other than Altair please explain briefly why. <br>
Our result shows three different types of visualization. Overall all information, we wanted to show are integrated in our project. Nevertheless, not everything worked as expected. First of all, we would have liked to set the circle size of the bubble chart fixed between the minimum- and maximum-value of the data regarding the death rate. Unfortunatly, this did not work out but the comparison between multiple countries is still possible since the circle size between different countries in one graph is set into the  right relation. Also we wanted to add a legend for the bubble chart which did not work out as planned so we added an explenation in the desription as well as a notation in the diagramm.<br> 
If we would have had more time, we would have liked to see if different campaigns regarding the education of the society on how to prevent HIV and Aids from spreading had an impact on the rates represented. Unfortunatly, we did not find a suiting data set representing these events. Additionally, we probably would have included the overall incidence and not only the death rates to see the medical development over time.<br>
For the realisation of this project we used Dash by plotly.

## Screencast
A screencast of our visualization can be found here:
<br>
<br>
[![hiv](https://user-images.githubusercontent.com/93648313/152791310-7a0dacc0-4419-49a2-b4e1-2888a3b777e3.png)](https://youtu.be/y00YpJFRV_I)


