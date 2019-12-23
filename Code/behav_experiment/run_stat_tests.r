library(lme4)
# Read CSV
Data <- read.csv(file="../../Paradigm/Results/dataframe_results_all_trials.csv", header=TRUE, sep=",")

# Subset Data, add new columns, remove others.
Data <- subset(Data, trial_type == "Violation") # Take only trials in which there was a violation
Data <- subset(Data, violation_position != "other") # Take only trials in which the violation was on the first or second verb (but not on nouns (fillers)).

# Remove the following columns (they will not be analyzed):
Data$violation_type <- NULL 
Data$valid_answer <- NULL
Data$block <- NULL
Data$trial_num <- NULL
Data$RT <- NULL
Data$slide_num_of_viol <- NULL

# Define a new column 'response', which will be '1' if subject was correct and '0' if wrong. 
Data$response <- ifelse(Data$correct_wrong == "CORRECT" | Data$correct_wrong == "CORRECT_DDC", 1, ifelse(Data$correct_wrong == "WRONG" | Data$correct_wrong == "WRONG_DDC", 0, "REJECTTED"))
Data <- subset(Data, response != "REJECTTED") # remove from it rejected trials (in which subject was inconsistent)

# Define 3 new binary columns that will classify all conditions ('SSS', 'SSP', 'SPS'...) based on whether the nouns agree on number.
Data$congruent_subjects <- ifelse(Data$condition == 'SSS' | Data$condition == 'SSP' | Data$condition == 'PPP' | Data$condition == 'PPS' | Data$condition == 'SS' | Data$condition == 'PP', 1, 0)
Data$number_v2 <- ifelse(Data$condition == 'SSS' | Data$condition == 'SSP' | Data$condition == 'PSS' | Data$condition == 'PSP' | Data$condition == 'PS',  "singular", "plural")
Data$congruent_attractor <- ifelse(Data$condition == 'SSS' | Data$condition == 'PSS' | Data$condition == 'SPP' | Data$condition == 'PPP', 1, ifelse(Data$condition == 'SSP' | Data$condition == 'SPS' | Data$condition == 'PSP' | Data$condition == 'PPS', 0, "NA"))
Data$correct_wrong <- NULL
Data$condition <- NULL

# Define the main fixed variables (nested and long), based on the type of syntactic structure. 
Data$nested <- ifelse(Data$sentence_type == "objrel" | Data$sentence_type == "objrel_nounpp", 1, 0)
Data$long <- ifelse(Data$sentence_type == "embedding_mental_LR" | Data$sentence_type == "objrel_nounpp", 1, 0)
Data$sentence_type <- NULL
Data$trial_type <- NULL
Data[] <- lapply(Data, function(x) if(is.factor(x)) factor(x) else x) # Remove all empty level in dataframe.
Data[] <- lapply(Data, factor) # change all variables to 'factor' type.


# GLMM model:
# VARS:
# nested:              1 if there's center embedding (objrect relatives), else 0 (right branching embedding). 
# long:                1 if one of the subject-verb dependencies is a long-range one, else 0.
# violation_position:  "inner" or "outer", based on which verb the violation occurred.     
# congruent_subjects:  1 if the two first nouns agree on number, else 0.
# number_v2:           "singular" or "plural", based on the number of the second noun.
# congruent_attractor: 1 if the two last nouns agree on number, else 0.

# 
# For example, the last three VARS defines: 'SSS' = (1, 'singular', 1), 'SSP' = (1, 'singular', 0), 'SPS' = (0, 'plural', 0), etc
# Note that when long=0 (i.e., no attractor noun), then there are only four conditions (SS, SP, PS, PP), and therefore congruent_attractor='NA': 'SS'=(1, 'singular', 'NA'), etc.
# However, it is not modelled for now.
# --------------------------------------------------------------------------------------------------------

glmm1 <- glmer(response ~ nested + long + violation_position + congruent_subjects + number_v2 + nested*long*congruent_subjects + (1|subject), data=Data, family="binomial")
# To test if the number of the second noun is important, construct another model:
glmm1_without_numberV2 <- glmer(response ~ violation_position + nested*long*congruent_subjects + (1|subject), data=Data, family="binomial")
# To test whether random effects should be added, construct another model:
glmm1_without_random <- glm(response ~ violation_position + number_v2 + nested*long*congruent_subjects, data=Data, family="binomial")

# Print results
summary(Data)
print("----------------------------------------------------------------------------------------------------------")
print("--------------------------------------MODELS---------------------------------------------------------")
print("----------------------------------------------------------------------------------------------------------")
summary(glmm1)

# Test whether the random effect is significant
print("----------------------------------------------------------------------------------------------------------")
print("--------------------------------------MODERL COMPARISON---------------------------------------------------------")
print("----------------------------------------------------------------------------------------------------------")
anova(glmm1,glmm1_without_random)
1-pchisq(344.71,12)
print("-----------------------")
anova(glmm1,glmm1_without_numberV2)
1-pchisq(0.0043,11)
