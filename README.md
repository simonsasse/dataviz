# The impact of HIV on the life expectancy in Africa 

## Domain problem characterization
With our visualization, we want to show the spread of HIV and Aids from 1990 until 2019 and raise awareness about the impact that HIV had on the development of the life expectancy in some countries. We want to demonstrate this on the example of the African continent. Our target audience are high school students from different countries. Since we are focusing on students, we included some informational texts, that describe what is seen in the visualization. Nevertheless, we also think it should be a little challenging since it is for educational purposes.
 
## Data / task abstraction:
Three different data sets from ourworldindata.org were used. One describes the Life Expectancy, a second one regarding HIV death rates and lastly a data set that contains the share of death by cause in different countries to take other reasons for the development of the life expectancy into consideration. Each Data Set consists of entity, ISO-Code and year. The Life Expectancy Set additionally includes the average life expectancy from 1950 until 2019 and the HIV Set the death rate caused by HIV and Aids from 1990 until 2019.  The last data set shows the percentage of different death causes, e.g. Cardiovascular diseases or Malaria, in each country from 1990 until 2019. The data of the two sets regarding death rates originate from the Global Burden of Disease Collaborative Network of the Institute for Health Metrics and Evaluation. The Life expectancy data is based on the estimates of James C. Riley.<br>
Since the data sets contained information about all countries of the world, we filtered the data by using the Alpha 3 country codes of Africa (source: https://www.nro.net/list-of-country-codes-in-the-afrinic-region/).  We also shortened the Data Set regarding Life expectancy to the years from 1990 to 2019 since we did not have data for the HIV and Aids rates before 1990. 
<br>
<br>
Life Expectacy https://ourworldindata.org/grapher/life-expectancy?time=1544&country=BWA~NAM~ZAF~SWZ~TZA~ZMB<br>
Aids death Rate: https://ourworldindata.org/grapher/hiv-death-rates?time=2018<br>
Share of death by cause: https://ourworldindata.org/grapher/share-of-deaths-by-cause?time=2002..2003<br>

## Visual encoding / interaction design:	
The landing page shows a map of the African continent. Underneath the map, a timeline going from 1990 until 2019 is displayed. Each country is colored in a tone of red. The intensity shows the number of HIV deaths per 100,000 residents in the selected year. An animation can be started via a play button which shows the development of the HIV deaths over time. To see the values of a specific year, the animation can be paused or alternatively clicked on in the timeline. Hovering over a country shows the name of the country, the rate of HIV deaths in this country and the life expectancy. <br>
Clicking on a country opens two diagrams underneath the map: a bubble chart and a bar chart. In the bubble chart, the y-axis describes the life expectancy, while the x-axis shows the year. The circle size represents the HIV death rate in the selected country. This way it can be recognized that in many countries the circle size correlates in a way to the life expectancy (the bigger the circles get the lower the life expectancy is). By clicking on another country, the bubble chart gets added in a different color and two or more countries can be compared. Alternatively, the countries can be selected via a drop-down menu and deselected by clicking the cross next to the countries listed above the diagram. The bar chart shows the top ten death causes (y-axis) in one country in percent (x-axis) in a year. By hovering over the different circles in the bubble graph, the bar charts are changing according to the chosen year. HIV/Aids is colored in red to make it more prominent, the other causes are colored in a range of grey.



		
