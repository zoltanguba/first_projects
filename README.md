#My first Django project
This repository contains my first django project (still beta versions)with 2 applications:
1) "translate": The app is an attempt to reverse-engineer the Lingq website. This is a translator application designed to help going through language learning material by saving individual word translations into the backend.
The application shows if a word is not "known" by the user (there is no saved translation under the user account), it indicates if its known and the level of familiarity the user has assigned to the translation.
If there is a translation available by other user(s) the application provides the translation as a suggestion.
The app is using Django for backend, the front-end is driven by HTML, CSS, Javascript. 
2) "dashboard": the app is visualizing data loaded in using Excel worksheet. The data is loaded and transformed using
Pandas, then the Django backend sends the data requested and draws the charts using D3.js. The charts are interactive in
a way that by clicking the chart elements on the starting view will bring up drill-down data depending on the chart end 
element clicked.