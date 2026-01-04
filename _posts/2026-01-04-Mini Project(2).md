---
title: "Mini Project 2"
excerpt_separator: "<!--more-->"
categories:
  - project1
tags:
  - experiments
  - Mini Project
image: images/158bfa00-3556-11f0-8519-3b5a01ebe413.jpg
---

### Mini Project Proposal: Digital Analysis of Trust, Risk, and Reputation in Undocumented Migrant Labour Networks

  My research question is: Which employment sectors are most frequently associated with illegal working in London according to BBC News reporting?
  <!--more-->

  For my corpus, I collected articles from BBC News about illegal workers. I ensured that each article included its title and publication date, but I faced challenges in removing unrelated text such as sidebars, navigation links, or related-article suggestions. I attempted to address this using AI-assisted text cleaning, but during code adjustments, some information—such as dates or titles—sometimes disappeared, and occasionally the article text was condensed into a single line. I am still exploring more reliable methods to clean the corpus and retain only the main article content.
## Keyword Tagging
  The corpus consisted of BBC News articles initially stored in CSV format. I applied keyword tagging, searching for terms related to illegal migrant labour (e.g., illegal, undocumented, foreign worker) and employment sectors (e.g., construction, restaurant, agriculture). Each article was automatically tagged based on the presence of sector keywords, and frequency counts were then used to identify the most commonly mentioned sectors. By identifying recurring lexical markers related to migration status and work domains, the corpus was transformed from unstructured text into analysable data, enabling frequency-based comparison across sectors.
During this process, I encountered a formatting issue: although I initially thought the corpus was in CSV format, it was actually an Excel spreadsheet. After converting it to CSV, the keyword tagging process worked correctly.

## Visualization

  I also visualized my findings to make the results more interpretable. The bar chart showed that BBC News reporting most frequently associates illegal migrant labour with the restaurant, construction, and delivery sectors, while agriculture and cleaning are mentioned less often. Initially, I had considered using a network graph, but it proved too confusing to implement, so I opted for the simpler and clearer bar chart instead.



  There is still a lot of work to do. I need to further clean my corpus by removing text that is not part of the main articles, such as sidebars, navigation links, or related-article suggestions. In the visualization part, more work is needed as the current bar chart is quite simple and limited. I hope that future feedback will help me improve both the analysis and the presentation. Additionally, I am planning to identify the nationalities of illegal workers mentioned in BBC News reporting, which could provide further insight into patterns across employment sectors.
