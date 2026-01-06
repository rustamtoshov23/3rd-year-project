# 3rd-year-project
Here I will include mainly coding but also later everything else I used and need for my 3rd year project on segmenting tightly packed cells that share boundaries using machine learning

## Update 04/01/2026
I wanted to fork in the code for the metrics to determine how good segmentation algorithms are. Did not manage to fork it, so just downloaded the files and uploaded them into my repository. Need to shorten down the code to only what I need, will hopefully do it tomorrow. 

## Update 05/01/2026
- To run the metrics.py code, created a virtual environment, uploaded all the packages needed to run it successfully. 
The environment data is loaded into GitHub along with some instructions. The only instructions I really need, is that to activate the environment, type this into Terminal:

```zsh
cd "Calculating metrics"
source .venv/bin/activate
```

- So did not shorten the code. Instead, to run the metrics.py code Copilot created the run_metrics.py code which allows me to input my .tif files and run them to generate a .json file with all the metrics. 
- Decided to keep it general, if I would need to run it for other images later.
- Uploaded ground truth image into GitHub. Now need to try to get the prediction data out of the models. 
- Got prediction data out of Nikhil's 3rd year project
- Now to run run_metrics.py and get data, every time do not forget to activate venv via code above and then every time you need to specify images and then I only want to see the summary .json file so next, put this into terminal (example with .tif files for Nikhil's 3rd year project, DO NOT FORGET TO CHANGE FILE NAME FOR PREDICTION EVERY TIME + CHANGE MODEL NAME TO PREDICTIOR ALGORITHM!):

```zsh
python run_metrics.py "Choosing best model images/Ground truth.tif" \
  "Choosing best model images/Predictions/Nikhil_3rd_year_thresholding.tif" \
  --model-name mymodel --outdir ./out --summary-only
# The script will report which detailed JSON files (if any) were removed.
```

- IT WORKS!!!
- [Nikhil's GitHub page with code](https://github.com/TechAvi-eng/cell-image-analysis)
