
title: "Evaluate OCR Output Quality with Character Error Rate (CER) and Word Error Rate (WER)"
excerpt_separator: "<!--more-->"
categories:
 - blog
tags:
 - digital-humanities
   
 - projects





---
 
**Project title:** Evaluate OCR Output Quality with Character Error Rate (CER) and Word Error Rate (WER) 


The article discusses the use of Character Error Rate (CER) and Word Error Rate (WER) as metrics for evaluating OCR performance. Various metrics are used to assess text accuracy, and CER is one of the most common. It measures the number of character-level errors in OCR output, including substitution errors (incorrect characters), deletion errors (missing characters), and insertion errors (extra characters).
To quantify these errors, the Levenshtein distance is used, which represents the minimum number of character substitutions, deletions, or insertions required to transform one text sequence into another. The CER formula calculates the percentage of mispredicted characters in relation to the total number of characters in the reference text. A lower CER indicates better OCR performance, with 0 representing a perfect transcription. In some cases, normalized CER is applied, dividing the number of errors by the sum of edit operations and the number of correct characters.

The article also provides examples of acceptable CER values depending on the application. For printed texts, such as Australian newspapers, a CER of 1–2% is considered very good, 2–10% is average, and over 10% is poor. For more difficult texts, such as handwritten forms, a CER of up to 20% may still be acceptable.

While CER is useful for sequences of characters (e.g., social security numbers, phone numbers), WER is more appropriate for longer, meaningful texts, such as paragraphs, book pages, or newspaper articles. WER measures the number of word-level substitutions, deletions, or insertions needed to convert one sentence into another.

Overall, the article highlights that although CER and WER are helpful metrics, they are not perfect indicators of OCR performance. Factors such as handwriting quality, image resolution, and document clarity can affect OCR accuracy as much as, or even more than, the OCR model itself.



 
