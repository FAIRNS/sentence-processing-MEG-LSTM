
# Pipeline for extracting model behav performance

## Italian

### Transform to Linzen format:
Before starting, make sure that the following files are in `Data/Stimuli` (if not, run `Italian_0_*.sh`):  
Italian_embedding_mental_4032.txt  
Italian_embedding_mental_SR_4000.txt  
Italian_objrel_nounpp_4032.txt  
Italian_objrel_that_4000.txt  
These are the output files from the `Code/Stimuli/NA_task_generator.py` for the 4 structures. 

Next, run:  
`Italian_1_transform_to_Linzen_format.sh` 

This will generate the following Linzen-style files in `Data/Stimuli`:
Italian_1_transform_to_Linzen_format.sh  
Italian_2_extract_predictions_from_model.sh  
Italian_3_get_performance_gender.sh  
Italian_3_get_performance_number.sh  
Italian_3_get_performance_two_attractors.sh  

### Extract predictions from NLM:
Next, run:  
`Italian_2_extract_predictions_from_model.sh`  
This will generate abl files in `Output/` folder.

Italian_objrel_that_V1_4000.abl
Output/Italian_objrel_that_V2_4000.abl
Output/Italian_objrel_nounpp_V1_4032.abl
Italian_objrel_nounpp_V2_4032.abl
Italian_sc_short_V1_4000.abl
Italian_sc_long_V1_4032.abl

- Note that the model name is hard-coded in the bash file. This can be modified by providing a path to the model as an argument to bash from the command. 

### Print predictions to screen/file:
For the short embedded dependency cases, run:  
`Italian_3_get_performance_number.sh`

For the long cases, run:
`Italian_3_get_performance_two_attractors.sh`

