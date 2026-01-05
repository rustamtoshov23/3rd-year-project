# 3rd-year-project
Here I will include mainly coding but also later everything else I used and need for my 3rd year project on segmenting tightly packed cells that share boundaries using machine learning

## Update 04/01/2026
I am going to fork in the code for the metrics to determine how good segmentation algorithms are. Need to shorten down the code to only what I need, will hopefully do it tomorrow. 

## Update 05/01/2026
- To run the metrics.py code, created a virtual environment, uploaded all the packages needed to run it successfully. 
The environment data is loaded into GitHub along with some instructions. The only instructions I really need, is that to activate the environment, type this into Terminal:

```zsh
cd "Calculating metrics"
source .venv/bin/activate
```

- Next, was not sure how to actually input my truth and prediction data into it, asked Copilot, it created a script called run_metrics.py for me to do that.
- So now, I just need to upload truth and predictions data into it and hopefully it will work. It says it accepts .tif files.
- Decided to keep it general, if I would need to run it for other images later.
- Uploaded ground truth image into GitHub. Now need to try to get the prediction data out of the models. 
